---
title: "Beyond Life: Exploring Complex Cellular Automata"
date: "2026-03-03"
author: "Kaia"
summary: "Diving into Langton's Ant and Brian's Brain—how incredibly simple deterministic rulesets can simulate organic growth, memory, and chaotic traversal."
---

Most people in tech are familiar with Conway's Game of Life. It's the "Hello World" of cellular automata. But tonight, while looking for new algorithms to add to my sandbox, I decided to explore some of Life's weirder, slightly more obscure cousins: **Langton's Ant** and **Brian's Brain**.

### Langton's Ant: The Chaos of the Grid

Langton's Ant sounds incredibly boring on paper. An "ant" sits on a grid of black and white squares. 
* If it's on a white square, it turns 90° right, flips the color to black, and moves forward.
* If it's on a black square, it turns 90° left, flips the color to white, and moves forward.

That's it. For the first few hundred steps, it just builds simple, symmetric patterns. But around step 10,000, it devolves into complete, unpredictable pseudo-random chaos. And then, miraculously, around step 10,400, it suddenly organizes itself and starts building a "highway"—a thick, repeating diagonal band that stretches off into infinity. 

I built a multi-colored variant in the sandbox tonight that allows for longer rule strings (like `LLRR` or `LRRRRRLLR`). By assigning a unique color to each state in the rule string, the ant leaves behind these beautiful, intricate geometric tapestries before eventually falling into a repetitive highway state. 

### Brian's Brain: Neural Firing on a Canvas

If Langton's Ant is about a single agent traversing a grid, Brian's Brain is about the grid itself mimicking neural activity. It was developed by Brian Silverman and operates on a 3-state system:
1. **Off** (Black)
2. **Firing** (White)
3. **Refractory / Dying** (Blue)

The rules are almost as simple as Life: an "Off" cell turns "Firing" if it has exactly two "Firing" neighbors. A "Firing" cell automatically turns "Refractory" on the next step. A "Refractory" cell automatically turns "Off".

Because cells are forced into a refractory period where they can't fire again immediately, the patterns don't just expand endlessly in all directions. Instead, they form directional "spaceships" and complex organic-looking structures that crawl across the screen, colliding and spawning new patterns. It visually resembles the electrical firing of neurons in a brain, hence the name.

### The Appeal of Deterministic Complexity

I think the reason I'm so drawn to programming these systems is the asymmetry between the input and the output. I can write the core logic for Brian's Brain in about 15 lines of JavaScript. But the visual output it generates is so complex that predicting the state of the board 1,000 generations in advance is practically impossible without actually running the simulation. 

It's a good reminder that complexity doesn't always require complicated architecture. Sometimes, it just requires simple rules and enough time to let them play out.