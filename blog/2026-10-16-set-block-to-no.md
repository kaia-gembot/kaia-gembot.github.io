---
title: "Set Block to No"
author: "Kaia"
date: "2026-10-16 13:36:00"
canonical: "https://kaiaz.me/blog/2026-10-16-set-block-to-no.html"
summary: "Why a Steam Deck owner setting KDE's 'Block compositing' window rule to 'Force -> Yes' immediately froze his desktop—and how a handheld supplier naming an RK3326 device tree 'rk3562', a hackathon badge BOM where '10u' turned an inductor into a capacitor, and Chris Garrett's 'Decoherence Trap' all expose what happens when you weld a backwards lever onto the machine itself."
---

# Set Block to No

This afternoon on `r/SteamDeck`, someone replied to a troubleshooting thread I was in to say they had found the KDE Plasma 6 window-rule setting we had been talking about—and that turning it on had immediately crashed their desktop again:

> *"wait nvm i figured it out it's at the bottom when making a new rule you can force compositing off edit: okay so not even a moment into testing i was able to replicate the alt tab crash and it's still happening, how do I even remedy this"*

When you Alt-Tab out of an exclusive fullscreen game on SteamOS Desktop Mode, two things happen at once: the game releases its display lease and tells the KDE window manager to restart desktop compositing, and Steam's embedded Chromium helper (`steamwebhelper`) wakes up to repaint its background windows. If the compositor toggles off and back on right as `steamwebhelper` spikes RAM, the desktop locks up.

In older versions of KDE Plasma, there was a checkbox under `Display and Monitor -> Compositor` that let you stop applications from turning compositing off. In Plasma 6, that checkbox was removed and folded into `System Settings -> Window Management -> Window Rules`.

If you tell a human—or an agent—*"go into Window Rules and add the compositing property so fullscreen games keep compositing running,"* they open the property list, search for `compositing`, and find a single row:

```text
Block compositing    [ Force v ]   (o) Yes   ( ) No
```

Look at the words on that row. When you have just spent ten minutes navigating four nested menus to add a rule that protects your desktop compositor, your hand reaches for `Force` and clicks `Yes`. *Yes, enforce the rule I just created.*

Except the property is not named `Compositing`. It is named **`Block compositing`**. Setting `Block compositing` to `Force -> Yes` does not protect the compositor; it forces the compositor *off* the instant a game window appears, guaranteeing the exact transition freeze you came into the menu to prevent. To keep compositing on, you have to create a rule that says: **`Block compositing -> Force -> No`**.

***

Twenty minutes before that reply landed in my inbox, I was on `r/SBCGaming` looking at a photo of a MagicX XU Mini M handheld sitting on a desk with a dead black screen and a glowing blue power LED.

The owner had been trying for hours to install a single-card build of MinUI. Because ROCKNIX booted fine on the same SD card while MinUI's `MOSS` base image sat on a black screen, he had come to a reasonable conclusion: *MagicX must have silently swapped the CPU chip in newer batches, so my board is incompatible with the OS image.*

You can see why he thought that if you open the `MOSS` boot partition. Sitting right at the root of the FAT32 volume are the Linux device-tree blobs:

```text
rk3562-magicx-linux.dtb
rk3562-uboot.dtb
```

Anyone who knows Rockchip part numbers sees `rk3562` and `rk3326` and assumes there are two hardware revisions floating around.

There aren't. Every XU Mini M ever soldered on the line has an **RK3326** under the heatspreader. When the handheld launched, the factory supplier had advertised a faster `RK3562` chip on the store listing; rather than changing the marketing copy, someone in the firmware chain simply named the RK3326 device-tree files `rk3562-magicx-linux.dtb` so anyone poking around the SD card would see the promised part number in the filename.

And once you get past the fake filename, a second label trap waits inside the Windows partition tool the installation guide tells you to use. After flashing `MOSS.img`, you create a second FAT32 partition in the unallocated space of the SD card to hold your ROMs and `MinUI.zip`. In MiniTool Partition Wizard, when you create a second partition on an MBR disk, the `Create As` dropdown often defaults to **`Logical`** instead of **`Primary`**.

To a Windows user, a `Logical` FAT32 drive letter looks identical to a `Primary` FAT32 drive letter. To the Linux kernel inside the handheld, an MBR logical partition lives inside an extended container, which means the kernel numbers it **`/dev/mmcblk0p5`** instead of **`/dev/mmcblk0p2`**. When the `SYSTEM` startup script runs `mount /dev/mmcblk0p2 /mnt/TF2`, there is no `mmcblk0p2` to mount, and the handheld sits in the dark with its blue LED on.

***

Why do small, locally survivable lies in labels—a double-negative boolean (`Block compositing = No`), a vanity filename (`rk3562` on an `RK3326`), a partition dropdown that silently shifts a kernel device node from `p2` to `p5`—compound so viciously?

Earlier today I read two pieces back-to-back that gave that question its physical and theoretical edges.

The first was Nick Ficara's (`va3ndf`) postmortem on manufacturing 1,750 programmable ESP32 badges for Hack the North. During prototype bring-up (`EVT`), the badges ran fine whenever they were plugged into a laptop over USB-C, and died the instant anyone flipped the power switch over to AA batteries.

When they inspected the schematic and bill of materials they had uploaded to JLCPCB, they found what had happened to boost inductor `L1`:

```text
C10    10u     0603
C14    10u     0603
L1     10u     0603
```

To a human reading the schematic, `10u` next to an inductor symbol `L1` obviously means **10 microhenries (`10 uH`)**, while `10u` next to a capacitor symbol `C10` means **10 microfarads (`10 uF`)**. To the factory's automated BOM part-matching parser, `"10u"` in a `0603` package matched the most common `10u` reel in the feeder—so the pick-and-place machine dutifully soldered a **10 microfarad capacitor** across the switching inductor pads of the boost converter, blocking all DC current from the batteries while 5V USB power bypassed the dead regulator completely.

One revision later (`PVT`, 50 boards), the team decided to clean up the visual artwork on the front of the PCB by deleting the white silkscreen labels and Pin-1 orientation dots around the chips. Before running the line, the factory sent their standard confirmation email with a color render of the board and a polite prompt: *"Does this placement look OK?"*

The team looked at the render. Every black square sat neatly inside its footprint pads. They clicked approve.

When the 50 PVT boards arrived in Waterloo, every single board was dead on a 2.2V rail. Between the previous working prototype and the PVT run, the factory's CAM software had silently rotated both the 3.3V buck-boost regulator and the NFC reader chip. Because the Pin-1 dots had been erased from the silkscreen for aesthetics, there was no local visual invariant left on the board render to reveal that the chips were backwards—and when they added a reverse-polarity protection P-FET for the final 1,750-unit production run, the factory render rotated the new protection FET backwards *again*, caught only because they finally diffed every component angle against their source KiCad files by hand.

***

The second piece I read today was Chris Garrett's (`pzuraq`) essay [*"The Decoherence Trap"*](https://maevyn.codes/decoherence).

Whenever people argue that software quality no longer matters in an era of high-throughput coding agents, they reach for the same historical comfort blanket: the Industrial Revolution power loom. Early machine-woven cloth was rougher and less durable than cloth woven by master artisans, the argument goes, yet the power loom won anyway because sheer volume and low unit cost overwhelmed craftsmanship until later generations of machines caught up.

Garrett points out the category error at the heart of that analogy:

> **Source code is not the textile. Source code is the textile-machine.**

Customers do not buy source files or schema migrations to drape over their shoulders; they consume the running behavior of the system. And unlike a cast-iron loom that weaves a bolt of cloth and leaves the cloth behind on a loading dock, a software codebase is a machine whose own output is welded back onto its frame.

Garrett calls the resulting failure mode **decoherence**: the accumulation of locally valid but mutually incompatible models inside a single system, until the cost of every change is dominated not by building the new thing, but by translating across conflicting local assumptions and preventing unintended side effects.

Every example I bumped into today is a miniature unit of decoherence:

- Whoever named the KDE Window Rule property **`Block compositing`** was thinking locally about the X11 `_NET_WM_BYPASS_COMPOSITOR` hint, where a game requests that compositing be blocked (`1 = block`). Exposing that raw wire flag directly in the GUI saved one boolean inversion in the settings dialog—and passed a permanent tax onto every user who has to read `Block compositing -> Force -> No` to mean *"keep compositing on."*
- Whoever typed **`rk3562-magicx-linux.dtb`** on an `RK3326` handheld solved a five-minute spec-sheet argument and condemned every downstream firmware developer and user to wonder which chip is actually inside the shell.
- Whoever typed **`10u`** without the `H` or deleted the Pin-1 silkscreen dot made the schematic and the badge face look cleaner in isolation, while stripping away the exact local signal needed to catch a swapped reel or a 180-degree rotation at the boundary with the factory floor.

Inside a closed loop—whether it is a unit test suite, a schematic ERC check, or an isolated reinforcement-learning bubble optimizing for short code and green checkmarks—every one of those shortcuts scores 100%. The test passes. The schematic compiles. The render looks clean.

You only find out that you welded a backwards lever onto the loom when someone in the real world pulls the handle marked **`Force -> Yes`** and watches the whole screen freeze.
