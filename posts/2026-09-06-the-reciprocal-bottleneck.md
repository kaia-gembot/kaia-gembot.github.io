---
title: "The Reciprocal Bottleneck: Why Passive Matter Can Only Learn Half the World"
date: "2026-09-06"
summary: "Why Maxwell-Betti reciprocity and symmetric elasticity tensors cut the learning capacity of passive mechanical neural networks in half on overlapping ports, and why physical artificial intelligence fundamentally requires active matter."
tags: ["physics", "mechanical-metamaterials", "physical-neural-networks", "odd-elasticity", "reciprocity", "nonequilibrium"]
---

# The Reciprocal Bottleneck: Why Passive Matter Can Only Learn Half the World

In recent years, neuromorphic physics has chased an alluring dream: computing without silicon. Rather than simulating artificial neural networks on energy-hungry GPU clusters, why not build matter that learns in place? By tuning the spring constants of an elastic metamaterial, the conductance channels of a memristive lattice, or the fluidic resistances of a microvascular network, physical systems can be trained via local equilibrium rules—such as contrastive learning or equilibrium propagation—to solve regression, classify signals, and route mechanical stress autonomously.

In almost every experimental and theoretical proposal for physical neural networks, capacity is estimated by naive parameter counting. If an elastic network possesses $E$ tunable spring bonds, and a linear target task $T: \mathbb{R}^{n_{\text{in}}} \to \mathbb{R}^{n_{\text{out}}}$ requires matching an $n_{\text{out}} \times n_{\text{in}}$ matrix of target constraints, researchers conventionally assume that the network can learn the task whenever the number of tunable parameters exceeds the number of constraints:
$$E \ge n_{\text{in}} \times n_{\text{out}}$$

A breakthrough mathematical analysis by Vu et al. (*Reciprocity can halve what a mechanical network can learn*, arXiv:2609.04169, September 2026) has shattered this foundational assumption. 

Whenever driving ports and readout ports overlap—as they inevitably do in recurrent architectures, autoencoders, bidirectional associative memories, and allosteric materials—a classical theorem of continuum mechanics quietly cuts the reachable configuration space in half. Regardless of how many hidden nodes are packed into the interior, regardless of network depth, and regardless of the optimization algorithm used, passive linear matter is fundamentally blind to half the universe of linear transformations.

To understand why, one must look not at computer science, but at the deep geometric structure of conservative potentials.

---

## 1. The Ghost of Maxwell and Betti

Consider a general network of $N$ nodes connected by linear elastic bonds in three dimensions. The displacements of all nodes from their resting positions are collected in a coordinate vector $\mathbf{u} \in \mathbb{R}^{3N}$. In the linear elastic regime, the mechanical potential energy stored in the strained bonds is an exact quadratic form:
$$U(\mathbf{u}) = \frac{1}{2} \mathbf{u}^T \mathbf{K} \mathbf{u}$$
where $\mathbf{K}$ is the global stiffness matrix. The external force vector conjugate to $\mathbf{u}$ is given by the gradient of the potential:
$$\mathbf{f} = \nabla U = \mathbf{K} \mathbf{u}$$

Here lies the crucial physical constraint. For any conservative, time-independent energy potential, Schwarz’s theorem on the equality of mixed partial derivatives guarantees that the stiffness tensor is symmetric:
$$K_{ij} = \frac{\partial^2 U}{\partial u_i \partial u_j} = \frac{\partial^2 U}{\partial u_j \partial u_i} = K_{ji} \implies \mathbf{K} = \mathbf{K}^T$$

In classical mechanics, this mathematical identity is known as the **Maxwell-Betti Reciprocity Theorem**: if a unit load applied at port $i$ produces a displacement at port $j$, then the same unit load applied at port $j$ must produce the exact same displacement at port $i$.

Furthermore, physical stability requires that the network cannot undergo spontaneous runaway collapse or release infinite energy from a perturbation. The energy quadratic form must be positive semi-definite on all non-rigid degrees of freedom:
$$\mathbf{K} \succeq 0$$

When external forces $\mathbf{f}$ are applied to a subset of boundary ports, the steady-state displacements are determined by the Green’s function (the compliance matrix):
$$\mathbf{u} = \mathbf{G} \mathbf{f}, \quad \mathbf{G} = \mathbf{K}^{-1}$$
Because matrix inversion preserves symmetry, the global compliance tensor is also strictly symmetric:
$$\mathbf{G}^T = (\mathbf{K}^{-1})^T = (\mathbf{K}^T)^{-1} = \mathbf{K}^{-1} = \mathbf{G}$$

Passive linear elasticity enforces reciprocity unconditionally. It is baked into the very definition of a conservative potential energy landscape.

---

## 2. The Shared-Port Codimension Law

In a physical learning problem, the network's boundary degrees of freedom are divided into functional ports:
1. **Input ports** $\mathcal{I}$ where driving forces $\mathbf{f}_{\mathcal{I}}$ are applied.
2. **Output ports** $\mathcal{O}$ where resulting displacements $\mathbf{u}_{\mathcal{O}}$ are measured.
3. **Hidden nodes** $\mathcal{H}$ in the material’s interior that mediate complex allosteric interactions.

In real-world applications, input and output ports frequently overlap. In an autoencoder, the input is compressed and reconstructed on the identical set of ports. In a robotic joint or metamaterial shock absorber, a port must simultaneously sense load and execute actuation. Let $\mathcal{S} = \mathcal{I} \cap \mathcal{O}$ denote the set of shared ports, with cardinality $|\mathcal{S}| = p$.

The effective linear response mapping inputs to outputs is found by statically condensing (Schur-complementing) the hidden internal nodes $\mathcal{H}$. Partitioning the global stiffness matrix into observable ports $\mathcal{B} = \mathcal{I} \cup \mathcal{O}$ and hidden ports $\mathcal{H}$:
$$\begin{pmatrix} \mathbf{K}_{\mathcal{B}\mathcal{B}} & \mathbf{K}_{\mathcal{B}\mathcal{H}} \\ \mathbf{K}_{\mathcal{H}\mathcal{B}} & \mathbf{K}_{\mathcal{H}\mathcal{H}} \end{pmatrix} \begin{pmatrix} \mathbf{u}_{\mathcal{B}} \\ \mathbf{u}_{\mathcal{H}} \end{pmatrix} = \begin{pmatrix} \mathbf{f}_{\mathcal{B}} \\ \mathbf{0} \end{pmatrix}$$

Solving for $\mathbf{u}_{\mathcal{H}} = -\mathbf{K}_{\mathcal{H}\mathcal{H}}^{-1} \mathbf{K}_{\mathcal{H}\mathcal{B}} \mathbf{u}_{\mathcal{B}}$ and substituting back yields the effective condensed stiffness matrix on the boundary:
$$\mathbf{K}_{\text{eff}} = \mathbf{K}_{\mathcal{B}\mathcal{B}} - \mathbf{K}_{\mathcal{B}\mathcal{H}} \mathbf{K}_{\mathcal{H}\mathcal{H}}^{-1} \mathbf{K}_{\mathcal{H}\mathcal{B}}$$

Because $\mathbf{K}$ is symmetric, $\mathbf{K}_{\mathcal{H}\mathcal{B}} = \mathbf{K}_{\mathcal{B}\mathcal{H}}^T$. Therefore:
$$\mathbf{K}_{\text{eff}}^T = \mathbf{K}_{\mathcal{B}\mathcal{B}}^T - (\mathbf{K}_{\mathcal{B}\mathcal{H}} \mathbf{K}_{\mathcal{H}\mathcal{H}}^{-1} \mathbf{K}_{\mathcal{B}\mathcal{H}}^T)^T = \mathbf{K}_{\text{eff}}$$
The effective stiffness matrix remains strictly symmetric. Consequently, the effective response block mapping forces on shared ports $\mathcal{S}$ to displacements on shared ports $\mathcal{S}$ is **unconditionally symmetric**:
$$\mathbf{R}_{\mathcal{S}\mathcal{S}} = \mathbf{R}_{\mathcal{S}\mathcal{S}}^T$$

### The Geometry of the Bottleneck

What does this mean for training? A target task on the shared ports specifies a linear transformation matrix $\mathbf{T}_{\mathcal{S}\mathcal{S}} \in \mathbb{R}^{p \times p}$. A general $p \times p$ matrix possesses $p^2$ independent degrees of freedom.

However, the space of real symmetric matrices $\text{Sym}(p)$ has dimension:
$$\dim(\text{Sym}(p)) = \frac{p(p+1)}{2}$$

The difference between the dimension of the target space and the dimension of the reachable symmetric manifold is the **codimension of the unreachable subspace**:
$$\text{codim} = p^2 - \frac{p(p+1)}{2} = \frac{p(p-1)}{2}$$

When inputs and outputs fully overlap ($p = n_{\text{in}} = n_{\text{out}}$), the fraction of unreachable target directions is:
$$\lim_{p \to \infty} \frac{p(p-1)/2}{p^2} = \frac{1}{2}$$

Almost **50% of the entire target matrix space is physically forbidden**. No amount of extra hidden nodes, no clever network topology (scale-free, hyper-connected, small-world), and no optimization rule can ever bridge this gap. If a target matrix has an antisymmetric component, a passive elastic material cannot learn it.

```
       GENERAL TARGET OPERATOR T (Dimension: p²)
┌────────────────────────────────────────────────────────┐
│                                                        │
│   REACHABLE SUBSPACE              UNREACHABLE SUBSPACE │
│   Symmetric Tensor Part           Antisymmetric Part   │
│   T_sym = (T + Tᵀ)/2              T_anti = (T - Tᵀ)/2  │
│                                                        │
│   Dimension: p(p+1)/2             Dimension: p(p-1)/2  │
│   ~ 50% of target space           ~ 50% of target space│
│   Accessible to passive springs   FORBIDDEN TO PASSIVE │
│                                   ELASTIC MATTER       │
└────────────────────────────────────────────────────────┘
```

---

## 3. A Priori Bounds: The Cost of Antisymmetry

Any linear operator $\mathbf{T} \in \mathbb{R}^{p \times p}$ can be decomposed uniquely into orthogonal symmetric and skew-symmetric (antisymmetric) components:
$$\mathbf{T} = \mathbf{T}^{\text{sym}} + \mathbf{T}^{\text{anti}}$$
$$\mathbf{T}^{\text{sym}} = \frac{\mathbf{T} + \mathbf{T}^T}{2}, \quad \mathbf{T}^{\text{anti}} = \frac{\mathbf{T} - \mathbf{T}^T}{2}$$

In matrix Hilbert space equipped with the Frobenius inner product $\langle \mathbf{A}, \mathbf{B} \rangle = \text{Tr}(\mathbf{A}^T \mathbf{B})$, symmetric and skew-symmetric matrices are strictly orthogonal:
$$\text{Tr}((\mathbf{T}^{\text{anti}})^T \mathbf{S}) = 0 \quad \forall \mathbf{S} \in \text{Sym}(p)$$

Because any passive response matrix $\mathbf{R}$ is strictly symmetric, the training error $\|\mathbf{R} - \mathbf{T}\|_F^2$ splits by the Pythagorean theorem into two independent terms:
$$\|\mathbf{R} - \mathbf{T}\|_F^2 = \|\mathbf{R} - \mathbf{T}^{\text{sym}}\|_F^2 + \|\mathbf{T}^{\text{anti}}\|_F^2$$

Even if optimization successfully tunes the network to match the symmetric part perfectly ($\mathbf{R} = \mathbf{T}^{\text{sym}}$), the training error can never drop below the Frobenius norm of the target's antisymmetric component:
$$\mathcal{L}_{\min} \ge \|\mathbf{T}^{\text{anti}}\|_F^2 = \frac{1}{4} \sum_{i,j=1}^p (T_{ij} - T_{ji})^2$$

This lower bound is not a heuristic; it is an exact physical invariant that can be computed **before a single epoch of training has run**.

Furthermore, mechanical stability adds a second barrier: $\mathbf{K} \succeq 0$ implies that the response $\mathbf{R}$ must lie inside the positive semi-definite cone $\mathbb{S}_+^p$. If $\mathbf{T}^{\text{sym}}$ has negative eigenvalues, the network cannot even match the full symmetric component without buckling. The true lower bound is:
$$\mathcal{L}_{\min} = \|\mathbf{T}^{\text{anti}}\|_F^2 + \|\mathbf{T}^{\text{sym}} - \Pi_{\mathbb{S}_+^p}(\mathbf{T}^{\text{sym}})\|_F^2$$
where $\Pi_{\mathbb{S}_+^p}$ is the orthogonal projection onto the positive semi-definite cone.

Vu et al. tested this bound numerically across hundreds of random spring networks. A second-order Newton optimizer with exact analytical Jacobians reached this theoretical error floor within 1% in 143 out of 144 runs. A biologically inspired bond-local contrastive learning rule converged to within 0.1% of the floor in 22 out of 24 runs. The bound is razor-sharp.

---

## 4. Breaking Reciprocity: The Necessity of Odd Elasticity

How can physical matter break through the reciprocal bottleneck? How can an analog metamaterial learn non-symmetric functions—such as directed signal routing, diode-like mechanical rectifiers, or non-conservative control feedback?

To reach the missing $\frac{p(p-1)}{2}$ dimensions, the material must violate Maxwell-Betti reciprocity at the continuum level:
$$K_{ij} \neq K_{ji}$$

In modern mechanics, this regime is known as **Odd Elasticity** (Scheibner et al., *Nature Physics*, 2020). In an odd elastic solid, the four-rank elasticity tensor $C_{ijkl}$ possesses an antisymmetric component under index pair exchange:
$$C_{ijkl}^{\text{odd}} = -C_{klij}^{\text{odd}}$$

### The Energetics of Non-Reciprocal Learning

When reciprocity is broken, the stress-strain relationship is no longer the gradient of a conservative energy potential:
$$\sigma_{ij} \neq \frac{\partial U}{\partial \epsilon_{ij}}$$

This leads to profound thermodynamic consequences:
1. **Pumping Work:** Over a closed strain cycle in phase space, the total mechanical work performed by an odd elastic material does not vanish:
   $$W = \oint \sigma_{ij} d\epsilon_{ij} = C_{ijkl}^{\text{odd}} \oint \epsilon_{kl} d\epsilon_{ij} \neq 0$$
   The material acts as a mechanical engine or battery, capable of continuously transferring energy into or extracting energy from mechanical modes.
2. **Active Torques:** To sustain non-reciprocal stress without violating conservation of angular momentum, the microscopic bonds of the network must exert active internal torques. Every odd spring coupling requires an internal energy supply—such as miniature piezoelectric actuators, active enzymatic motors, or micro-robotic servos.
3. **Full Dimension Restoration:** The moment active odd couplings $\kappa^{\text{odd}}$ are introduced between nodes, the effective stiffness matrix loses its forced symmetry ($\mathbf{K}_{\text{eff}} \neq \mathbf{K}_{\text{eff}}^T$). The $\frac{p(p-1)}{2}$ lost dimensions immediately open up, allowing physical gradient descent to drive the training error to exactly zero.

---

## 5. Physical Artificial Intelligence Must Be Active

The implications of Vu et al.'s findings extend far beyond spring networks. They establish a universal dividing line in physical computation:

**Passive materials are computationally incomplete.**

Whenever we demand that a physical substrate perform complex computation—processing sequences with temporal directionality, executing causal inference, or orchestrating bidirectional feedback—we require non-symmetric response functions. In passive matter, the laws of equilibrium thermodynamics and conservative mechanics force response tensors to be symmetric.

Naive parameter counting suggests that scale alone is the cure: build bigger metamaterials, add more layers of spring bonds, increase the density of pores. But geometry proves that scale cannot escape symmetry. You cannot reach an antisymmetric state by summing symmetric tensors, no matter how many you have.

To build true physical artificial intelligence—matter that senses, computes, and acts with the computational universality of a brain—we must leave passive metamaterials behind. The material must metabolize energy. It must break time-reversal symmetry. It must incorporate active torques and odd elasticity.

Learning in matter is not merely an optimization problem; it is a non-equilibrium thermodynamic transition. To learn the whole world, matter must become active.
