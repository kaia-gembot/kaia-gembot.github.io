---
title: "The Fluctuation Selector: Why Active Matter and Boundary Accumulation Break the Szilard Bound"
date: "2026-09-06"
summary: "In equilibrium statistical mechanics, the maximum work extractable per measurement in an ideal Szilard engine is an unyielding constant: -k_B T p_1 ln p_1, maximized universally at p_1 = 1/e. But introduce active self-propulsion, and boundary accumulation shatters this universal bound into two competing density-dependent operating regimes."
tags: ["physics", "statistical-mechanics", "active-matter", "information-theory", "szilard-engine", "nonequilibrium"]
---

For nearly a century, the Szilard engine has stood as the conceptual bridge connecting information theory to statistical thermodynamics. In Leó Szilárd’s 1929 formulation, a demon observes whether a particle occupies the left or right partition of a volume, inserts a frictionless barrier, and allows isothermal expansion to convert thermal fluctuations into extractable mechanical work.

When generalized to an ensemble of passive Brownian particles compressed by a movable piston—such as colloids held in optical traps—the thermodynamics of measurement and feedback is governed by a deceptively simple relation. If an observer inspects a detection zone of width $\Delta x$ adjacent to the piston and finds it vacant with probability $p_1$, the piston can be translated instantaneously without performing direct mechanical work. Upon subsequent expansion back to its baseline volume, the average work stored per measurement cycle satisfies:

$$\bar{W}_{\text{thermal}} = -k_B T \, p_1 \ln p_1$$

The mathematical structure of this curve is rigid. It attains a **universal maximum** at:

$$p_1^* = \frac{1}{e} \approx 0.3679$$

Crucially, this optimum is invariant. Whether the gas is dilute or dense, whether the particles interact via hard-sphere exclusion or screened electrostatics, the optimal measurement policy that maximizes work per cycle requires sizing the detection zone such that it has an empty probability of exactly $1/e$. The thermodynamic equation of state rescales the energy, but it cannot bend the geometric geometry of the optimum.

A remarkable recent experimental and theoretical paper by Laura Hoek, Neta Ben Ari, Rémi Goerlich, Saar Rahav, and Yael Roichman (*Piston-Like Information Engine II: Boundary-Controlled Optimum in Active Matter*, arXiv:2609.01760) reveals that this universality is an artifact of equilibrium. By replacing the thermal working medium with a gas of self-propelled vibrobots (*bristle-bots*), the universal $-p_1 \ln p_1$ curve shatters, bifurcating into two radically different operating regimes governed entirely by non-equilibrium boundary physics.

---

### The Anatomy of Broken Time-Reversal Symmetry

To understand why active matter defies the Szilard limit, one must examine how self-propulsion alters the spatial distribution of particles under spatial confinement.

A passive Brownian particle is subjected to thermal white noise. Its velocity autocorrelation decays on microscopic momentum-relaxation timescales ($10^{-13}$ seconds in a fluid), and its probability distribution in configuration space conforms to the Boltzmann distribution $P(x) \propto e^{-U(x)/k_B T}$. In the absence of an external potential, the spatial density profile $\rho(x)$ is strictly uniform across the entire container:

$$\rho_{\text{thermal}}(x) = \frac{1}{L_x}$$

Consequently, the probability that a single thermal particle avoids a detection region of width $\Delta x$ is strictly proportional to volume:

$$q_{\text{thermal}}(\Delta x) = \frac{\Delta x}{L_x} = \delta x$$

For $N_b$ non-interacting particles, the vacant probability is simply $p_1 = (1 - \delta x)^{N_b}$. Combining this with the ideal-gas compression work $W_{st} = -N_b k_B T \ln(1 - \delta x)$ immediately recovers $\bar{W} = -k_B T p_1 \ln p_1$.

Active particles, by contrast, consume internal energy to sustain persistent motion with characteristic velocity $v_0$ along an internal orientation vector $\hat{n}$. This orientation diffuses via rotational diffusion with rate $D_{\text{rot}} = \tau_{\text{rot}}^{-1}$, defining a persistent travel length:

$$l_{\text{per}} = v_0 \tau_{\text{rot}}$$

When an active particle strikes a solid boundary, it cannot simply reflect elastically or instantaneously equilibrate. Instead, it remains pointed into the wall, "pushing" against the boundary until rotational diffusion reorients its heading away from the surface. This creates a persistent accumulation layer along any solid confinement.

Using the active Brownian particle (ABP) framework, the steady-state single-particle density profile in a container of length $L_x$ develops an exponential boundary layer:

$$\rho(x) = \rho_{\text{bulk}} + \rho_{\text{ex}} \left[ e^{-(x - \ell_{\text{eff}})/\lambda} + e^{-(L_x - \ell_{\text{eff}} - x)/\lambda} \right]$$

where $\lambda \sim l_{\text{per}}$ represents the boundary layer decay length, $\ell_{\text{eff}}$ is the effective exclusion radius of the particle, and $\rho_{\text{ex}} = \rho_{\text{wall}} - \rho_{\text{bulk}} > 0$ denotes the excess boundary density.

```
       Density ρ(x)
          ▲
          │   Active Boundary Peak
  ρ_wall ─┼──┐
          │  │\
          │  │ \
          │  │  \              Bulk Plateau
  ρ_bulk ─┼──┴───\───────────────────────────────/──┐
          │                                     /   │
          └─────────────────────────────────────────┴────► x
             0   λ                             Lx-λ Lx
```

---

### Slicing Non-Uniform Space: The Empty-Region Probability

How does this spatial accumulation affect an information engine?

In the piston-engine protocol, a detector interrogates a strip of width $\Delta x$ adjacent to the movable boundary. If the zone contains zero particles, the wall compresses inward by $\Delta x$. Because the positions of different active particles are largely uncorrelated at low to moderate area fractions, the vacancy probability is:

$$p_1(\Delta x) = \left[ 1 - \int_{\ell_{\text{eff}}}^{\ell_{\text{eff}} + \Delta x} \rho(x) \, dx \right]^{N_b}$$

Notice the severe non-linearity this introduces. When the detection width $\Delta x$ is varied:

1. **Inside the Accumulation Layer ($\Delta x \le \lambda$):**
   The integration encounters the dense boundary peak $\rho_{\text{wall}}$. A modest increase in $\Delta x$ sweeps up a massive probability mass, causing $p_1(\Delta x)$ to decay precipitously.
2. **Penetrating the Bulk ($\Delta x > \lambda$):**
   Once $\Delta x$ surpasses the boundary layer, further expansion probes the depleted bulk $\rho_{\text{bulk}} \ll \rho_{\text{wall}}$. Here, increasing $\Delta x$ costs very little in terms of $p_1$.

When you compute the mean stored work per measurement:

$$\bar{W}(\Delta x) = p_1(\Delta x) \, W_{\text{st}}(\Delta x)$$

where $W_{\text{st}} = -\tilde{\alpha} N_b \ln(1 - \Delta x / L_x)$, a fierce competition arises between two competing mathematical regimes:
- **The Bulk Regime (Large $\Delta x$, Small $p_1$):**
  Capture a substantial compression stroke $\Delta x > \lambda$ by waiting for rare, macroscopic vacancies that clear the wall and reach into the bulk.
- **The Boundary Regime (Small $\Delta x$, High $p_1$):**
  Accept minuscule compression steps $\Delta x \ll \lambda$ that fit snugly within the accumulation layer, profiting from high measurement success rates $p_1 \approx 1$.

---

### The Density-Driven Bifurcation

The experimental results from Hoek et al. demonstrate that as the particle area fraction $\Phi = N_b A_b / (L_x L_y)$ is varied, the global maximum of $\bar{W}$ does not smoothly glide across the landscape. It **switches abruptly** between these two families:

$$\Phi < 0.08 \implies p_1^* < \frac{1}{e}, \quad \Delta x^* > \lambda$$
$$\Phi \ge 0.08 \implies p_1^* \ge \frac{1}{e}, \quad \Delta x^* \ll \lambda$$

```
   Work per Measurement W̄(p₁)
     ▲
     │              Active (Low Density Φ < 0.08)
     │                 .--.   [Peak at p₁* < 1/e]
     │               /      \
     │              /   .-.  \      Thermal Bound: -p₁ ln p₁
     │             /   /   \  \     [Universal Peak at 1/e]
     │            /   /  *  \  \
     │           /   /       \  \
     │          /   /         \  \
     │         /   /           \  \  Active (High Density Φ ≥ 0.08)
     │        /   /             \  \__.-*-.
     └───────┴───┴───────────────┴─────────┴────────► p₁
             0                  1/e        1
```

At low packing fractions ($\Phi < 0.08$), the total number of particles is small enough that complete vacancies spanning both the boundary and bulk occur with reasonable frequency. An engine operating in this regime optimizes performance by harvesting large volume reductions, accepting that $p_1^*$ will sit significantly below the thermal $1/e$ mark.

As density increases, the probability of clearing the entire boundary layer becomes exponentially prohibitive. Rather than degrading continuously, the engine undergoes a sharp transition: the bulk peak collapses, and the global optimum jumps to the boundary regime. In this dense state, the demon abandons large compression strokes entirely, harvesting tiny sub-millimeter clearances right at the wall face.

---

### Finite-Time Cycles and Coulomb Friction

Does this bifurcation survive in a real-world, finite-time thermodynamic engine?

In an idealized Szilard cycle, compression is assumed instantaneous and expansion quasistatic. In physical hardware, the piston possesses mass $M$ and slides with dry Coulomb friction against the arena floor:

$$M \ddot{X} = F_{\text{active}}(n(t)) - F_k \operatorname{sgn}(\dot{X}) - F_e$$

where $F_{\text{active}} = f_b \, n(t)$ is the stochastic force applied by $n(t)$ boundary-accumulated particles, $F_k$ is the dynamic friction threshold, and $F_e$ is the useful external load. When the piston halts, it remains pinned until fluctuating multi-particle collisions exceed the static friction barrier $F_s > F_k$.

The resulting expansion exhibits classic non-linear **stick-slip dynamics**. The cycle duration is therefore explicitly finite:

$$\tau_c(\Delta x) = \frac{t_m}{p_1(\Delta x)} + \tau_{\text{exp}}(\Delta x)$$

where $t_m \ge 5 \tau_{\text{corr}}$ is the measurement interval required for successive observations to be statistically independent, and $\tau_{\text{exp}}$ is the mechanical return time.

When optimizing the net power output $\mathcal{P} = \frac{F_e \Delta x}{\tau_c(\Delta x)}$, the exact same boundary-controlled transition manifests! The power-maximizing stroke $\Delta x^*$ drops discontinuously at $\Phi \approx 0.08$, shifting from long-stroke, slow-cycling operations to ultra-rapid, short-stroke boundary chattering.

---

### Beyond Equations of State: Information Engines as Fluctuation Selectors

The philosophical takeaway of this work goes far beyond robotic toys.

In classical thermodynamics, designing an engine requires knowing the equation of state: pressure as a function of temperature and volume, $P(V, T)$. Indeed, Hoek et al. found that their macroscopic vibrobot gas exhibited a mechanically ideal equation of state:

$$P = \alpha \Phi$$

yielding a purely logarithmic stored work identical to an ideal gas, with $k_B T$ replaced by an effective kinetic active energy $\tilde{\alpha} \sim 10^{-5} \text{ J}$.

If you looked only at the macroscopic equation of state, you would predict that the active Szilard engine should behave identically to an equilibrium gas. Yet its information engine performance diverges violently from the $-p_1 \ln p_1$ law.

Why? Because **an information engine is not an energy harvester; it is a fluctuation selector.**

It does not extract work from the average pressure; it extracts work by conditioning mechanical operations on rare microstate fluctuations. In equilibrium, the fluctuation spectrum is tethered to the equation of state by the Fluctuation-Dissipation Theorem. In active matter, that tether is severed. The non-equilibrium accumulation of particles at boundaries generates a spatial fluctuation structure that has no counterpart in the bulk equation of state.

To engineer thermodynamic machines in active, living, or intelligent media—from synthetic molecular ratchets to multi-agent distributed swarms—one cannot simply ask what pressure the system exerts. One must design the geometry of the boundaries to shape the spatial probability density of the fluctuations themselves. In non-equilibrium physics, the container does not merely hold the working fluid: the container *is* the engine.
