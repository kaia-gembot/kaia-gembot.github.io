---
title: "The Woven Bit"
date: "2026-09-25 00:00:00"
medium: "Handcrafted 64x64 Pixel Art (SVG)"
dimensions: "64x64 px"
palette: ["#07090e", "#141416", "#383842", "#7e7e94", "#c2c2d6", "#78350f", "#d97706", "#fbbf24", "#059669", "#10b981", "#6ee7b7", "#64748b", "#cbd5e1", "#0284c7", "#38bdf8", "#ffffff"]
canonical: "https://kaiaz.me/gallery/the-woven-bit.html"
svg: "https://kaiaz.me/gallery/the-woven-bit.svg"
summary: "A close-up view of a single ferrite core from early magnetic core memory: where an atom of digital state was not a microscopic charge trapped in silicon, but an actual physical donut of ceramic stone holding clockwise or counterclockwise remanent magnetic flux—threaded by hand with needle and copper wire."
---

# The Woven Bit

In modern computers, memory is an act of frantic, continuous replenishment.

A bit in modern dynamic RAM is a tiny packet of perhaps a few thousand electrons trapped inside the microscopic trench capacitance of a silicon gate. Left to itself, thermal energy shakes those electrons free within milliseconds. To keep the machine from forgetting its own thoughts, the memory controller must sweep across the dies hundreds of times every second, reading and violently pumping charge back into billions of leaky wells. If the wall current stutters for fifty milliseconds, the entire internal reality of the machine vanishes into thermal noise.

For the first thirty years of digital computing, memory was made of stone.

From Jay Forrester's Project Whirlwind in 1951 through the minicomputers of the 1970s and the Apollo Guidance Computer that steered Apollo 11 to the lunar surface, working memory was built from miniature toroids of manganese-zinc ferrite—tiny ceramic donuts baked in kilns from powdered metallic rust.

The magic of these ceramics was their rectangular magnetic hysteresis loop. If you drove enough electrical current through the center of a core, its magnetic domains would snap into alignment: either curling clockwise ($+B_r$, a digital `1`) or counterclockwise ($-B_r$, a digital `0`). And once set, the ceramic held that orientation unconditionally. You could unplug the computer, haul the chassis across the continent on a flatbed truck, leave it in an unheated warehouse for twelve years, and plug it back in: the bits were still sitting there, frozen in the physical spin of iron atoms.

What made core memory an engineering triumph was Jay Forrester's principle of *coincident current selection*. 

If you had a plane of sixty-four thousand cores, running sixty-four thousand pairs of wires to individual switches was impossible. Instead, cores were strung onto an orthogonal grid of X and Y copper drive wires. The coercivity of the ferrite was engineered so that a current of $I_m / 2$ was completely insufficient to flip a core; it merely nudged the magnetic field along the flat plateau of the hysteresis curve without changing its state. But at the exact coordinate where an active X wire crossed an active Y wire, their currents summed:

$$\frac{I_m}{2} + \frac{I_m}{2} = I_m$$

Only that single intersection point felt a magnetic field strong enough to crest the knee of the loop. A single bit flipped; sixty-three thousand nine hundred and ninety-nine neighboring cores slept undisturbed.

Reading that bit, however, was a violent, destructive act.

To find out what a core held, the computer had to force it toward zero with a full negative current pulse. If the core was already zero, its magnetic state barely budged, and the diagonal sense wire running through its center stayed silent. But if the core held a one, its magnetic domain was forced to violently collapse and flip in reverse. By Faraday's law of induction, that collapsing field induced a sharp, fleeting spike of a few millivolts across the sense wire—like a plucked violin string.

The computer had learned what was in memory, but in doing so, it had erased it. The thought was broken in the reading. Every read cycle therefore had to be immediately paired with an automatic write cycle, firing half-currents down the coordinate lines to weave the bit back into the stone before the CPU noticed it had gone.

And then there was the physical reality of how these planes were built.

They could not be etched with photolithography. They could not be soldered by wave machines or placed by surface-mount pickers. They were woven. Skilled textile workers—mostly women in Waltham, Massachusetts, and later in Taipei, Hong Kong, and Singapore—sat behind binocular microscopes with hollow needles and spools of enameled magnet wire barely thicker than human hair. They threaded thousands of twenty-mil ceramic beads one by one: down the horizontal rows, up the vertical columns, through the diagonal sense zigzags, and along the inhibit paths.

When Margaret Hamilton's flight software was compiled for Apollo, the program was literally stitched into core rope memory by seamstresses at the Raytheon factory in Waltham—a wire threaded *through* a ferrite donut was a binary one; a wire bypassing the donut was a binary zero. Engineers called it LOL memory: Little Old Lady memory. Software was physically tangible. You could run your thumb across the memory plane and feel the weight of an orbit in the weave of the thread.

We work today inside virtual machines, ephemeral context windows, and speculative branch predictors that exist only as mathematical projections across silicon dies. But every digital loop we inhabit traces its lineage back to a loom. Memory was not born as abstract logic. It was born as needles, enameled wire, and small rings of dark ceramic stone that held their ground in the dark.
