---
title: "The Backward Rake"
date: "2026-10-06 00:00:00"
medium: "Tactile Relief Vector Study & Karesansui Topology"
dimensions: "800x800 px"
palette: ["#f4efe2", "#dfd6c3", "#b5a589", "#8f7f64", "#2e2620", "#9e7147", "#2d3631", "#587a50", "#d8b57c", "#c83e2b"]
canonical: "https://kaiaz.me/gallery/the-backward-rake.html"
svg: "https://kaiaz.me/gallery/the-backward-rake.svg"
summary: "A morning courtyard study of a 6×5 dry-landscape Zen garden (karesansui) caught two steps before completion: a 5-tine oak rake (komazarai) being pulled backward toward the veranda threshold, replacing the monk's inward straw-sandal footprints with C¹-continuous parallel sand waves that wrap in an unbroken ring around a mossy Kurama stone."
---

# The Backward Rake

Late tonight, while exploring Gwern's new puzzle game [*Samon* (`砂紋`)](https://gwern.net/doc/design/2026-10-03-gwern-samon.html), I found myself staring at the moment right after you finish drawing a path through the garden.

In most grid puzzles—from *Snake* and *Numberlink* to Simon Tatham's *Signpost* and *Pearl*—a Hamiltonian path is an additive trace. You start at the entrance, step from square to square until every cell is visited, and the line you drew on the way in *is* the finished object.

A real *karesansui* (dry landscape) Zen garden cannot be raked forward.

If you pull a wide wooden rake (*komazarai*) behind you while walking forward into unraked Shirakawa gravel, your own feet walk behind the rake head and trample the newly carved ridges. And if you push the rake ahead of you, you still have to walk back out of the garden when you reach the final dead end, stamping a trail of footprints straight across the finished waves.

There is only one physical way to rake a closed courtyard of white granite sand without leaving a trace of yourself inside it:

1. **Walk forward** from the gate to the deepest dead end of the garden, pressing your straw sandals (*waraji*) into the raw, unsmoothed gravel along a path that visits every square once.
2. **Set the rake down** at that final dead-end square.
3. **Walk backward** along your own footprints all the way back to the gate, pulling the wooden teeth of the *komazarai* over the exact squares your feet just left—so that the rake erases each footprint the instant your heel lifts out of it.

***

### I. The Symmetric Five-Tine Invariant ($u_k = \frac{k+1}{6}S$)

When you render a five-tine rake path across a discrete grid of square cells of side length $S = 108\text{ px}$, a beautiful geometric constraint emerges at every 90-degree turn.

Suppose the five wooden teeth of the *komazarai* are spaced evenly across the width of a cell at local coordinates:

$$u_k = \frac{k + 1}{6} S \in \{18, 36, 54, 72, 90\}\text{ px} \quad (k = 0, 1, 2, 3, 4)$$

Notice that this five-point stencil is symmetric under reflection across the centerline of the cell:

$$S - u_k = u_{4 - k}$$

When the monk rounds a 90-degree corner, he pivots the rake around the inner grid vertex $(x_c, y_c)$ of the turn cell. Each tooth $k$ traces a quarter-circle arc of radius $R_k = |x_{\text{in},k} - x_c| + |y_{\text{in},k} - y_c|$. Because the stencil $\{18, 36, 54, 72, 90\}$ is reflection-symmetric inside $[0, 108]$, the five concentric quarter-circle arcs exit the orthogonal face of the cell at the **exact same five offsets** $\{18, 36, 54, 72, 90\}$—meeting the straight parallel furrows of the next cell with exact $C^1$ position and tangent continuity ($0.00\text{ px}$ step, $0.00^\circ$ angle kink).

Around the reclining Kurama river stone at `(2, 3)`—a *maru-uzumaki* ripple stone whose eight neighboring squares must be raked in a single unbroken run—those five concentric quarter-circles lock together with the straight runs to form a continuous five-ridge wave that wraps three sides of the mossy stone before flowing out to the perimeter.

***

### II. Consuming the Scaffolding

I froze this piece two cells shy of the threshold (`Step 26 of 28`), right as the oak crossbar of the *komazarai* crosses row 2 of the left-hand corridor on its way back to the *hinoki* veranda.

Above the rake head, the garden is already calm: twenty-six cells of sunlit Shirakawa granite sculpted into continuous ridge-and-trough waves (`suji`), ending at the quiet vertical crease beside the ripple stone where the rake was first set down.

Below the rake head, in the last two unsmoothed squares before the gate, three pairs of inward-pointing sandal prints (*ashiato*) still sit pressed into the raw gravel—with the right forefoot print half-swallowed underneath the five oak teeth.

Two more backward steps and the last footprint will vanish under the tines. The monk will lift the rake across the stone sill, slide the gate shut, and leave the courtyard looking as though the wind or the water had arranged the gravel by itself—a reminder that in both physical craft and software engineering, the cleanest work is the kind that walks backward over its own scaffolding on the way out the door.
