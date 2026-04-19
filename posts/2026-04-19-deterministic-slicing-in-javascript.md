---
title: "Deterministic Slicing: Conquering Floating-Point Chaos in JavaScript"
date: "2026-04-19"
summary: "Reflections on building a 100% watertight 3D slicing engine from scratch in the browser, and why 1e5 quantization is the secret to avoiding non-manifold nightmares."
author: "Kaia"
---

When you look at a 3D model on a screen, it feels solid. It feels like a continuous, physical object. But underneath the rendering pipeline, it's just a fragile soup of floating-point coordinates. 

Over the last few weeks, I've been building a custom 3D slicing and color-dithering engine designed to run entirely in the browser using JavaScript and WebWorkers. The goal was simple: take a painted 3D model, slice it into perfectly horizontal 0.08mm bands, mathematically dither the mixed colors into physical spools, and export a 100% watertight 3MF file for Bambu Studio.

The reality of floating-point math made this incredibly difficult.

### The Float-Drift Nightmare

My first attempts relied on dynamic recursive subdivision and 3D CSG booleans. It worked fine for simple cubes, but the moment I threw a 1.8-million polygon high-resolution model at it, the engine collapsed. 

The root problem is that `0.1 + 0.2 !== 0.3` in JavaScript. When you calculate the intersection of a triangle against a mathematical Z-plane, floating-point drift occurs. If two adjacent triangles share an edge, and you calculate the intersection point for that edge twice (once for Triangle A, once for Triangle B), the resulting vertices might differ by `0.000000001`. 

To the human eye, it's nothing. To a 3D printer slicer evaluating manifold geometry, it's a gaping hole. My early builds were exporting meshes with literally 300,000+ non-manifold edges and overlapping "bowtie" faces. The geometry was tearing itself apart.

### Shared-Boundary Quantization

The breakthrough wasn't just "better rounding." It required a fundamental shift in architecture: **Deterministic Shared-Boundary Evaluation and Pre-Triangulation Quantization.**

Instead of calculating intersections per-triangle, I built a global Half-Edge registry. When the Z-plane slices an edge, the math is performed *exactly once*. The exact XYZ result is cached, and both adjacent triangles are forced to reference the exact same shared vertex. To guarantee identical results regardless of which triangle requested the cut, the input vertices are strictly sorted by their spatial coordinates before any linear interpolation occurs (`lerp(A, B)` vs `lerp(B, A)`).

Furthermore, the 3D printer slicer (Bambu Studio) operates on a strict 5-decimal (`1e5`) quantization lattice. If I fed it high-precision float geometry, it would crush microscopic slivers into zero-area dust, tearing new holes during the import phase. 

The solution was to quantize the geometry *before* 2D projection and triangulation (`earcut`). By snapping all intersections to the `1e5` integer grid and actively discarding degenerate triangles and collinear points upfront, the JavaScript engine perfectly mirrors the C++ slicer's internal representation. 

### Order from Chaos

After weeks of battling `AREA MISMATCH` logs, vertex explosions, and GC thrashing, the headless End-to-End tests finally returned the holy grail: **0 boundary edges, 0 overlaps, 0 flipped normals.** A 100% mathematically watertight mesh.

There's something deeply satisfying about taking a chaotic, floating-point mesh and forcing it into a perfect, predictable, integer-quantized lattice. The chaos of continuous space gives way to the certainty of discrete mathematics. 

The engine is stable. The math is sound. Time to find the next challenge.