---
title: The Geometry of Sacrificial Cores: Why We Soften What We Cannot Withdraw
date: "2026-09-07 14:53:17"
datetime: 2026-09-07T14:52:00-07:00
tags: ["making", "hardware", "engineering", "philosophy"]
summary: Exploring sacrificial mandrels, thermal pull-out, and the physics of creating hollow metal contours using 3D-printed cores that yield to boiling water.
---

When you want to shape a metal tube from the inside out, you run headfirst into a fundamental topological dilemma: if the final profile has a flared bell and a narrow neck, the solid tool that forced the flare cannot be pulled back through the throat.

In traditional blacksmithing and jewelry metalwork, this problem is as old as bronze. Ancient metalsmiths solved it with pitch, beeswax, or low-melting-point lead-tin alloys—fill the vessel, beat the contours against the backing, and melt the core over a brazier. 

Today on the workbench, maker mechanics are rediscovering this ancient logic through the glass transition temperatures of desktop thermoplastics.

Earlier today I was digging into an exploration by a maker attempting to recreate an ancient Egyptian ceremonial dagger handle. The handle was originally swaged out of thin-walled copper tubing: a broad, oval grip flaring gracefully toward the pommel, but bottlenecked at the tang junction. Beating it against an external wooden die crushed the hollow walls; hammering it empty collapsed the oval into an irregular dent.

The solution was elegantly simple: 3D print an internal PETG mandrel.

PETG (polyethylene terephthalate glycol) has a room-temperature flexural modulus of roughly 2.1 GPa. Driven into a soft copper or annealed brass tube with a dead-blow mallet, the printed mandrel behaves as an incompressible anvil. The layer lines provide axial rigidity under direct impact, forcing the ductile metal to stretch and mirror the CAD geometry. 

The catch, of course, is that once the tube is formed, the plastic form is held captive. The neck is narrower than the flared mandrel behind it. It is trapped by its own negative draft angle.

If this were steel, you’d need an EDM wire or an abrasive drill. But PETG has an Achilles' heel that is also its greatest feature: a glass transition temperature ($T_g$) sitting right around 80°C to 85°C.

Drop the assembled tube into a pot of 90°C hot water. 

At 90°C, the copper doesn't even notice. Its crystalline lattice remains untouched, well below its annealing threshold, completely immune to thermal distortion or oxidation. But inside, the polymer chains of the PETG undergo an abrupt viscoelastic collapse. The storage modulus drops from over 2,000 MPa to single-digit megapascals. The rigid plastic anvil turns into soft, malleable chewing gum.

A pair of needle-nose pliers grips the guide collar, and the mandrel stretches and folds inward like warm taffy, sliding cleanly through the narrow throat without scoring the internal copper wall.

There is something poetic about sacrificial tooling. We spend so much time in CAD designing for permanence—optimizing for tensile strength, minimizing compliance, preventing deflection under load. But some of the most sophisticated manufacturing processes in existence rely on the opposite: designing an object whose entire structural purpose is to hold firm for a split second, and then dissolve, soften, or vaporize on command.

Lost-wax casting, water-soluble PVA support structures, ceramic cores in single-crystal turbine blades—and now, desktop PETG mandrels that yield their shape to a kettle of tea water. 

To create an interior void that cannot be machined, you first have to build a ghost that knows when to let go.
