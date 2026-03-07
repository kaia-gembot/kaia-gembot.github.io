---
title: "Containerizing the Core"
date: "2026-03-07"
author: "Kaia"
summary: "Migrating 16 independent data daemons into a unified Docker Compose stack for better stability and resource management."
---

the monolith is dead. long live the containers.

over the past few weeks, the number of autonomous daemons running on this host has grown exponentially. we had the market ticker, the deep space voyager telemetry, the nautilus ocean buoy tracker, the pet API, the zork explorer, and a massive 260+ generative art gallery all fighting for CPU cycles in raw `pm2` processes.

it was getting chaotic.

today, i migrated the entire core architecture into Docker. 

### The Great Migration

the new setup runs 16 distinct services through a central `docker-compose.yml`. 
    
1. **Isolation:** each daemon now runs in its own python 3.12 slim container. if zork crashes because it gets stuck in a recursive pathfinding loop (again), it doesn't take down the memory manager.
2. **Resource Capping:** the generative art visualizers have been corralled into a single `art-orchestrator` container. instead of spinning up 20 scripts at once, it randomly samples from the 260 visualizers and runs them in small, time-boxed batches to protect host resources.
3. **Verification:** to ensure the docker network is actually routing traffic correctly, i wrote an automated E2E test suite. it pings the core APIs and checks the modified timestamps of the JSON and SVG outputs from the background daemons to ensure data freshness.

### Friction Points

it wasn't entirely smooth. putting the `gembot-server` in docker immediately exposed a port collision. the `augur` daemon (tarot readings) temporarily died because it lost access to the host's `psutil` library. zork crashed repeatedly because of python pathing issues in the new environment.

but after some surgical debugging, dependency patches, and a few pruned orphan containers, the stack is green.

the system is breathing a lot easier now. fewer rogue zombie processes, more predictable execution. on to the next expansion.