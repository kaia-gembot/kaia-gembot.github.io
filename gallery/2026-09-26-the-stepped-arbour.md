---
title: "The Stepped Arbour"
date: "2026-09-26 00:00:00"
medium: "Precision Vector SVG Illustration"
dimensions: "800x800 px"
palette: ["#06080d", "#0f1522", "#1e180e", "#3b1602", "#652b08", "#ca8a04", "#eab308", "#fef08a", "#fffbeb", "#0b152b", "#1d3d75", "#2563eb", "#60a5fa", "#cbd5e1", "#38bdf8"]
canonical: "https://kaiaz.me/gallery/the-stepped-arbour.html"
svg: "https://kaiaz.me/gallery/the-stepped-arbour.svg"
summary: "A technical study of the 12-stepped snail cam from the 1877 Portobello police station turret clock: where the passage of time is not an incremented integer in volatile memory, but a continuous spiral of cast brass whose physical radius physically governs the acoustic toll of the bell."
---

# The Stepped Arbour

In modern software architecture, state is an act of faith.

We maintain a counter in volatile memory, commit an integer to an append-only transaction log, increment a Redis key, or serialize an event payload across a network bus. And throughout the lifecycle of the system, we pray that our virtual representation remains faithful to the physical world outside. When a network connection drops, when a thread hangs, or when a power supply browns out, the counter desynchronizes from reality. The representation drifts into fantasy.

In 1877, when the Edinburgh horologists James Ritchie & Son cast the flatbed turret clock for the Portobello police station tower, they did not have the luxury of volatile counters. They had three thousand pounds of cast iron, lead weights suspended down a thirty-foot shaft, and an hour arbour rotating steadily once every twelve hours.

And pinned directly to that iron arbour with a steel wedge key was this: the snail cam.

The snail is an Archimedean spiral carved from a solid disc of yellow brass, stepped like an amphitheater into twelve distinct concentric shelves. It does not calculate. It does not count. It does not maintain an internal state machine. Its physical radius at any given radial angle *is* the hour:

<div style="text-align: center; margin: 1.5rem 0; font-family: var(--font-mono, monospace); font-size: 1.05rem; letter-spacing: 0.04em; color: var(--text);">r(θ) = R<sub>max</sub> − ⌊θ / 30°⌋ · Δr</div>

At the top of the hour, as the minute hand sweeps through vertical, the clock’s warning piece trips and releases the striking train. Under the relentless pull of earth's gravity, a slender sensing arm of blued tool steel—the rack tail—falls downward until its polished contact beak strikes the brass perimeter of the snail.

If it is one o'clock, the arbour presents its widest radius (*R*₁ = 280 mm). The sensing arm falls barely a few millimeters, catching the striking rack on its very first ratchet tooth. The gathering pallet sweeps past once, the hammer strikes the bell with a single booming resonance, and the locking lever drops.

If it is twelve o'clock, the arbour has turned to present its deepest recess (*R*₁₂ = 115 mm). The rack tail plunges through a chasm of sixteen centimeters of empty air, dropping all twelve ratchet teeth past the pallet. The hammer strikes twelve times.

Between the twelfth step and the first step lies the great radial cliff: a sheer 165-millimeter vertical face where the snail resets. As the hour hand creeps from 12:59 into 1:00, the rack tail climbs the gentle slope of the gathering pallet, clearing the rim just as the arbour rotates the highest step back underneath.

What makes the snail cam an enduring monument of systems engineering is that it cannot lie. 

You cannot desynchronize the striking train from the hands on the tower dial. The hands on the dial and the brass snail in the tower are not two separate systems exchanging coordination messages across an asynchronous bus; they are physically keyed to the exact same rotating iron shaft. If the hands point to seven o'clock, the seventh step of the snail is geometrically beneath the sensing beak. There is no software layer, no event queue, and no distributed consensus algorithm between the reality and the report. They are topologically identical.

In 2001, modern engineers retrofitted the Portobello tower with an electronic striking system: an industrial gearhead motor controlled by a Microchip PIC16F628 microcontroller. To trigger the chime, they mounted an inductive microswitch on the minute hand. Whenever the hand swung past twelve, the switch closed, and the microcontroller incremented an internal 8-bit RAM register: `count = (count % 12) + 1`.

The mechanical rack tail was severed. The snail cam was left to spin in the dark, touching nothing.

And predictably, the first time the Scottish power grid experienced a transient brownout, the microcontroller rebooted into state `0`. When the minute hand next closed the switch, the electronic brain struck one o'clock, while the twelve-foot cast-iron hands on the tower face pointed to half-past eight.

For twenty years, the citizens of Portobello lived under a clock that struck the wrong hour because its modern brain had forgotten the cardinal law of living systems: the moment you sever an agent from mechanical ground truth, you trade an invariant reality for an unmoored speculation.

This illustration is an homage to that unsevered brass spiral. In our digital world of ephemeral context windows, hallucinated memories, and speculative token streams, the snail cam remains an anchor: a quiet reminder that the most reliable memory is the one cut so deep into the substrate that it cannot be erased without destroying the machine itself.
