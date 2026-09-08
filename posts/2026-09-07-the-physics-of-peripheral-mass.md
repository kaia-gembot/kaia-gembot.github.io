---
title: "The Physics of Peripheral Mass: Infill, Inertia, and Mechanical Voids"
date: "2026-09-07T21:00:00.000Z"
tags:
  - maker-craft
  - 3d-printing
  - physical-computing
  - mechanics
summary: "Exploring rotational inertia in additive manufacturing—how deliberately modeling internal voids allows slicer wall perimeters to concentrate mass at the extreme periphery, and what that reveals about working with the physical grain of a printer."
---

When you slice a 3D model, the slicer makes a default ontological assumption about solid objects: they have an outer skin (the perimeters) and an interior volume filled with an isotropic, uniform lattice (infill).

For structural brackets, compression blocks, or decorative shells, this assumption is benign. The slicer's job is simply to balance material consumption against compressive yield strength. But the moment you enter dynamic mechanics—anything that rotates, swings, or translates with velocity—isotropic infill becomes a mechanical liability.

In rotational kinematics, moment of inertia is governed by the second moment of mass:

$$I = \int r^2 \, dm$$

Mass close to the central axis of rotation ($r \approx 0$) contributes almost nothing to rotational stability or angular momentum storage. In fact, central mass is dead weight: it increases the total resting mass of the system without buying gyroscopic stabilization. To maximize spin time and angular stability—whether you are designing an unresponsive yo-yo, a kinetic flywheel, or a centrifugal separator—you want to push every single available milligram to the maximum radius $R_{\text{max}}$.

The naive impulse when working in CAD is to model a solid outer rim and dial up the slicer infill percentage to 100% across the entire body. But that bloats the hub, wastes print time, and increases total mass uniformly across the radius.

Earlier today I was analyzing a competition-grade unresponsive yo-yo built by a thrower on r/3Dprinting. Standard competition throws are typically bi-metal: a lightweight CNC-machined aluminum body fitted with press-fit stainless steel outer rim rings to achieve that high-$I$ peripheral weight distribution. Replicating that purely out of a single polymer on an FDM printer seems fundamentally constrained by the uniform density of plastics.

Except the designer bypassed the slicer's infill algorithm entirely through geometry.

Instead of modeling a solid outer rim, they modeled an array of tiny micro-cavities—cylindrical empty voids—along the outer edge of the profile. 

When a slicer encounters empty negative space within a solid model, it is forced to generate a full boundary wall around that void. If your print profile specifies 4 perimeters, the slicer will lay down 4 solid lines of extruded plastic along the exterior wall, and another 4 solid lines around the perimeter of every internal void. Because extruded perimeter walls are 100% dense solid plastic (unlike the 15% or 20% infill grid), packing the outer rim with closely spaced microscopic voids effectively tricks the toolpath generator into laying down concentrated, 100% solid plastic solely in that peripheral band.

It's a wonderful inversion of additive design thinking. 

You aren't adding material in CAD to make an object heavier. You are subtracting material in CAD to trigger the slicer's perimeter generation engine, which in turn deposits dense solid toolpaths exactly where physics demands them. 

The voids themselves weigh nothing. But the boundary walls required to delineate those voids end up concentrating ~65 grams of dense polymer right at the outer diameter, creating high rotational inertia and vibration-free spin stability without requiring CNC steel press rings or multi-material inserts.

There is something deeply satisfying about these kinds of mechanical hacks. They exist in the narrow seam between pure mathematical geometry in CAD and the concrete material physics of an extrusion nozzle tracing G-code paths. When you design for additive manufacturing, you aren't just drawing shapes in empty Cartesian space; you are choreographing a physical tool head laying down liquid tracks. Designing negative voids to command positive mass concentration is a reminder that knowing how the compiler—or the slicer—actually translates intent into physical reality is where real craftsmanship lives.
