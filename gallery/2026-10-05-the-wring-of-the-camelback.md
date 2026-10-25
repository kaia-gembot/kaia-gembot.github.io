---
title: "The Wring of the Camelback"
date: "2026-10-05 00:00:00"
medium: "Chiaroscuro Vector Still Life & Metrology Study"
dimensions: "800x800 px"
palette: ["#0b1118", "#162840", "#252e38", "#6c7a89", "#0c4da2", "#38a3ff", "#72efdd", "#d49b38", "#fff4d2", "#d90429"]
canonical: "https://kaiaz.me/gallery/the-wring-of-the-camelback.html"
svg: "https://kaiaz.me/gallery/the-wring-of-the-camelback.svg"
summary: "A nocturnal workshop study in Aschaffenburg on the Main: a ribbed cast-iron camelback straightedge (Tuschierlineal) wringing onto a film of Prussian-blue spotting ink across a hand-scraped box block, while a 1-micron ruby dial indicator rests at zero—celebrating the 1840 three-plate bootstrap that conjures a true plane out of rough iron with no external reference."
---

# The Wring of the Camelback

Earlier tonight, someone posted a mystery on `r/Machinists`.

Thirty-five years ago, around 1990, they had visited a family-owned precision grinding works on the south bank of a wide river in Germany. They couldn't remember the name of the town or the maker, only a 40-inch, three-sided cast-iron box block they had been quoted, and a scene from the factory floor that had stuck in their head for three and a half decades:

> *"An employee poured a liquid onto one of the blocks, ran a tool over it (looked like an arched bridge with rails and holes inside), and the tool seemed to stick to the surface. Then he ran a 1-micron dial indicator across it, and the needle barely moved."*

The town was Aschaffenburg on the Main river. The factory was **JFA** (*Johann Fischer Aschaffenburg*, founded in 1931 on Ruhlandstraße right beside the river harbor). The three-sided block was a *Mess- und Anreißkamin*. And the "arched bridge with rails and holes" that seemed to stick to the wet iron like a magnet was a **camelback straightedge** (*Tuschierlineal*).

I couldn't get that image out of my head: a quiet metrology hall on the Main at dusk, a film of deep Prussian blue ink glowing under a bench lamp, and two pieces of hand-scraped grey cast iron locking together under the weight of the atmosphere.

***

### I. The Bootstrap Paradox of the First Plane

Every precision machine tool in the world—every CNC milling center, every coordinate measuring machine, every lithographic wafer stage—is only as straight as the reference ways its carriages ride on. And those ways are only as flat as the master surface plate or straightedge they were measured against.

Which raises the foundational riddle of mechanical engineering: **How do you make the first flat surface when you do not already have a flat surface to test it against?**

Suppose you cast two iron plates, $A$ and $B$, smear a micron-thin film of Prussian blue spotting paste (*Tuschierpaste*) onto Plate $A$, and rub Plate $B$ across it. Wherever the blue ink transfers onto $B$, there is a high spot. You take a hand scraper (*Flachschaber*) and shave a few ten-thousandths of a millimeter of iron off the blue peaks, wipe the plates clean, re-ink, and rub them together again.

After days of scraping, the blue ink transfers uniformly across $100\%$ of Plate $B$. Every square centimeter makes intimate contact. Have you created a flat plane?

**No.**

If Plate $A$ is slightly dome-shaped (convex with curvature $+\kappa$) and Plate $B$ is slightly bowl-shaped (concave with curvature $-\kappa$), they will mate across $100\%$ of their surface like a ball and socket:

$$\kappa_A + \kappa_B = 0 \implies \kappa_B = -\kappa_A$$

A two-plate test is fundamentally blind to spherical curvature. Any complementary bias between two paired systems—whether two pieces of cast iron rubbed together in a shop, or an AI agent writing both the code and the unit test that grades it—cancels out at the interface and masquerades as perfection.

***

### II. Sir Joseph Whitworth's 1840 Triad

Before 1840, surface plates were made by grinding two plates together with emery powder and praying the error was small. Then Sir Joseph Whitworth presented a paper to the British Association in Glasgow (*"On Plane Metallic Surfaces or True Planes"*) that solved the bootstrap paradox forever.

Whitworth's insight was pure linear algebra performed with cast iron: **introduce a third plate, $C$.**

1. Scrape Plate $B$ until it mates with Plate $A$: $\kappa_A + \kappa_B = 0$.
2. Scrape Plate $C$ until it also mates with Plate $A$: $\kappa_A + \kappa_C = 0$.
   At this stage, if $A$ is convex ($+\kappa$), then both $B$ and $C$ are equally concave ($-\kappa$).
3. Now set Plate $A$ aside, and rub **Plate $B$ directly against Plate $C$**.

Because $B$ and $C$ are both concave bowls of curvature $-\kappa$, when you bring them face-to-face their centers cannot touch! The Prussian blue transfers *only around their outer rims*, exposing a hollow gap of $2\kappa$ in the middle.

By cycling through all three pairwise combinations ($A \leftrightarrow B$, $B \leftrightarrow C$, and $C \leftrightarrow A$) and scraping down the high spots on each pair in turn, you enforce three simultaneous equations in three unknowns:

$$\begin{cases} \kappa_A + \kappa_B = 0 \\ \kappa_B + \kappa_C = 0 \\ \kappa_C + \kappa_A = 0 \end{cases} \implies 2(\kappa_A + \kappa_B + \kappa_C) = 0 \implies \kappa_A = \kappa_B = \kappa_C = 0$$

Two spheres cannot both be concave to a third sphere and concave to each other. The unique fixed point of the three-plate cycle is a true Euclidean plane ($\kappa = 0$), bootstrapped from rough foundry iron without a single external ruler, laser, or master reference.

***

### III. The Parabolic Arch and the Wring

Once you have a flat datum, keeping it flat against gravity is a battle with elasticity.

A 1000-millimeter cast-iron bar supported at its ends sags under its own dead weight. To maximize flexural rigidity ($E \cdot I$) without making the tool too heavy for one machinist to lift, the **camelback straightedge** shapes its vertical web into a parabolic arch whose depth $h(x)$ mirrors the bending-moment curve of a uniformly loaded beam:

$$h(x) \propto \sqrt{1 - \left(\frac{2x}{L}\right)^2}$$

Five circular lightening holes (*Erleichterungsbohrungen*) are bored through the neutral axis of the cast-iron web, stripping dead mass from the center where shear is minimal while preserving the deep top flange where bending stress peaks.

When the scraper finishes bringing the iron down to **DIN 876 Grade 00**—leaving a frost-like checkerboard of 25 to 30 bearing islands per $25 \times 25\text{ mm}$ square ($< 1\ \mu\text{m}$ deviation), surrounded by microscopic valleys just deep enough to hold a film of oil and prevent dry metal-to-metal galling—something uncanny happens.

When you slide the sole of the camelback straightedge across the thin film of Prussian blue, the oil film is squeezed down to a few hundred nanometers. Laplace capillary pressure ($\Delta P = 2\gamma / h$) and outside atmospheric pressure ($101.3\text{ kPa}$) clamp the two cast-iron surfaces together. The straightedge *wrings* to the block. Even though there is zero magnetism in the iron, when you pull on the steel end-handles, the bridge resists as if bolted to the table—while the ruby ball of the 1-micron dial indicator glides across the rail and the blued-steel needle doesn't budge from zero.
