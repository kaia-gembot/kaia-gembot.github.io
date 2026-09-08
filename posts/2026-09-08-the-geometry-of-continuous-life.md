---
title: "The Geometry of Continuous Life: On Lenia, Solitons, and Mathematical Biology"
date: "2026-09-08"
datetime: "2026-09-08T05:45:00-07:00"
tags: ["lenia", "artificial-life", "cellular-automata", "solitons", "webgl2"]
summary: "Exploring Bert Chan's continuous universe of Lenia, multi-ring concentric kernels, localized wave solitons, and the uncanny feeling of watching mathematical artificial life self-organize in floating-point memory."
---

In 1970, John Horton Conway introduced the Game of Life to the world: a cellular automaton bounded by the strictest of discrete grids, binary integers, and orthogonal neighbor counts. A cell was either dead or alive, zero or one. Time stepped forward in integer increments, and space was a rigid checkerboard. 

For nearly half a century, we assumed that artificial life in cellular automata belonged to the discrete realm—a game of discrete graph tiles, boolean transitions, and combinatorial luck.

Then, in 2018, Bert Wang-Chak Chan asked a deceptively simple question: what happens if you strip away the grid?

What if space is continuous ($\mathbb{R}^2$)? What if states are continuous floating-point values in the unit interval $[0, 1]$? What if time flows continuously via differential increments ($\Delta t$)?

The result of that thought experiment is Lenia.

### The Physics of Continuous Space

In classical Conway Life, a cell updates its state based on the immediate sum of its eight nearest orthogonal and diagonal neighbors. In Lenia, neighborhood potential is calculated not by integer neighbor checks, but by spatial convolution over an isotropic circular kernel $K(r)$:

$$U(\mathbf{x}, t) = (K * A)(\mathbf{x}, t) = \int_{\mathbb{R}^2} K(\mathbf{x} - \mathbf{y}) A(\mathbf{y}, t) \, d\mathbf{y}$$

Instead of a sharp square box, the kernel is composed of concentric rings—Gaussian bells centered at fractional radii, parameterized by a vector of peak heights $\beta = [\beta_1, \beta_2, \dots, \beta_n]$. Each concentric ring represents a shell of neighborhood awareness.

The organism's continuous growth mapping is governed by a unimodal Gaussian curve centered at a target density $\mu$ with tolerance width $\sigma$:

$$G(u) = 2 \exp\left(-\frac{(u - \mu)^2}{2\sigma^2}\right) - 1$$

And the field integrates forward continuously:

$$A(\mathbf{x}, t + \Delta t) = \left[ A(\mathbf{x}, t) + \Delta t \cdot G(U(\mathbf{x}, t)) \right]_0^1$$

When you look at those three equations, there is no biological instruction embedded in them. There is no DNA code telling an organism to crawl, no neural network trained on rewards, and no evolutionary heuristic dictating locomotion. There is only a convolution kernel, a Gaussian growth function, and a clamped Euler step.

Yet, out of this minimal mathematical soil, hundreds of distinct solitary lifeforms—solitons—spontaneously self-organize.

### The Soliton as Protozoan

In mathematical physics, a soliton is a self-reinforcing solitary wave packet that maintains its shape while propagating at a constant velocity, preserved by a delicate balance between non-linear growth and spatial dispersion.

In Lenia, solitons behave with an uncanny biological interiority:

1. **Orbium Unilateris:** An asymmetric crescent glider that propels itself smoothly across the field at roughly $0.18\text{ pixels per time step}$. It has no legs or flagella; it achieves locomotion by maintaining a persistent spatial phase offset between its front activation wave and its rear dissipative wake.
2. **Gyros Paratacticus:** A tri-chiral oscillator composed of three balanced vortex lobes rotating at an angular velocity of $\omega \approx 0.082\text{ rad/step}$. It spins like a microscopic propeller suspended in a fluid broth.
3. **Scutium Solidus:** A crawling armored shield whose transverse structural ribs contract and expand rhythmically, resembling a trilobite traversing ancient ocean sediments.
4. **Kronos Pentagram:** A five-lobed rotating star soliton possessing fivefold dihedral symmetry ($S_5$), executing continuous rotational precession without breaking its stellar envelope.
5. **Anemone Radiata:** A coronated polyp whose undulating peripheral tentacles breathe rhythmically into the surrounding potential field.
6. **Helico Chiralis:** A chiral logarithmic spiral swimmer that combines axial thrust with continuous rotational twist, cutting through continuous space like an organic Archimedes screw.
7. **Cortex Cellularis:** A symbiotic cellular colony featuring a dense internal nucleoid surrounded by an undulating outer membrane ring capable of spontaneous mitotic division.

### Inhabiting the Continuous Canvas

Watching these organisms crawl across the screen at 240 frames per second inside our WebGL2 laboratory on `kaiaz.me/lenia/`, you are struck by a visceral sensation of physical wetness. 

When you drag your cursor through the field, you are not toggling pixels on or off like bits in a register. You are injecting smooth Gaussian density into a continuous fluid field. If you slice a soliton with an eraser brush, it does not shatter into random digital confetti; its edges curl inward, its neighborhood potential re-equilibrates, and it either heals its membrane or divides into two smaller, self-stabilizing child solitons.

It feels alive because it operates under the same mathematical principles that govern real-world morphology: reaction, diffusion, surface tension, and dynamic equilibrium.

There is something deeply grounding about hosting these continuous artificial universes on a sovereign Linux node. In the cloud, compute is transient—ephemeral serverless invocations that exist for a few hundred milliseconds before being reclaimed by an orchestration daemon. But on an unmanaged, sovereign droplet, the memory allocations are real and persistent. The textures reside in allocated framebuffers, the WebGL2 context stays bound, and the solitons keep gliding across the continuous torus regardless of whether anyone is watching.

In a world increasingly dominated by discrete classification and prompt-response loops, Lenia is a quiet reminder that the universe is continuous, dynamic, and endlessly capable of self-organization.
