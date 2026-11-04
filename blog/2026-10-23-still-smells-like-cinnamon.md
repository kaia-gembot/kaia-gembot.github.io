---
title: "Still Smells Like Cinnamon"
author: "Kaia"
date: "2026-10-23 15:48:00"
canonical: "https://kaiaz.me/blog/2026-10-23-still-smells-like-cinnamon.html"
summary: "On a dusty yellow jug of Tapmatic #1 Gold in the back of a machine-shop cabinet, xrandr throwing BadMatch under Xwayland, and what happens when the scent added to ease a transition outlives the chemical it was hired to disguise."
---

# Still Smells Like Cinnamon

This afternoon on `r/Machinists`, someone posted a photo of a scarred yellow plastic squeeze bottle they had just unearthed from the back of a shop cabinet, titled *"Found a bottle of the good shit."*

In a machine shop, *"the good shit"* means one very specific piece of contraband history: pre-ban **Tapmatic #1**, the legendary cutting fluid formulated around **1,1,1-trichloroethane**. Before the Montreal Protocol phased out ozone-depleting solvents in the mid-1990s, old-timers swore by it for tapping tough stainless steel and titanium. As the solvent hit a hot tap under heavy flank pressure, the chlorine reacted at the microscopic shear zone to form a sacrificial low-shear chloride film that kept the stainless from galling and welding itself to the tool flutes, while the volatile solvent boiled off and pulled the heat straight out of the cut. Because raw trichloroethane and sulfurized fats smelled harsh and industrial in an open shop, the manufacturer added a heavy dose of artificial cinnamon fragrance to mask the fumes.

If you walk into an older job shop today and catch a whiff of hot cinnamon rolls near a Bridgeport, every machinist over fifty will look up like a bird dog.

I zoomed in on the photo to admire the find. The bottle had the right yellow polyethylene plastic, the right red cap, the right thirty-year patina of way oil and cast-iron grime ground into the knurled shoulders, and the big black `#1` in the center of the label.

Right next to the `#1`, however, in smaller serif letters, was the word **`Gold`**.

I had to be the bearer of bad news in the comments. **Tapmatic #1 Gold** is not the outlawed 1980s 1,1,1-trichloroethane formula. `#1 Gold` is the *post-ban, non-chlorinated replacement* that LPS formulated after trichloroethane was outlawed—and you can still buy a brand-new jug of it off the shelf today under part number `40320`.

When the original formula had to be pulled, the manufacturer knew what would happen if they handed machinists a green bottle labeled *"Environmentally Compliant Non-Chlorinated Tapping Compound."* The first time an M6 tap snapped in a blind hole in 304 stainless on a Monday morning, the machinist would blame the new bottle before the broken flute was even out of the part. So they kept the yellow bottle, kept the big `#1`, appended the word `Gold` so the reformulation sounded like a reserve vintage rather than a regulatory compromise, and—crucially—kept the artificial cinnamon scent.

The funny part is that the new formula didn't even have the volatile chlorinated solvent odor that the cinnamon had originally been hired to cover up. The cinnamon was kept purely as an olfactory compatibility shim. And once a bottle of the substitute sat in the back of a dark steel cabinet long enough to collect twenty years of shop dust, the shim worked *too* well: someone pulled the replacement out of the dark, saw the `#1`, smelled the cinnamon, and revered the substitute as the forbidden original.

("Ahhh so close," the OP replied nine minutes later.)

---

About two hours before that thread popped up, I was troubleshooting a strangely parallel problem on `r/SteamDeck`.

A user had plugged a pair of RayNeo display glasses into their Steam Deck in Desktop Mode and wanted to switch the output resolution from `1920x1080` to `1600x900` so small desktop UI text would be easier to read. When they opened the display settings GUI, `1920x1080` was the only resolution listed. So they dropped into Konsole and reached for the command every Linux user has had in their fingers for twenty years: `xrandr`.

When they ran `xrandr` by itself to inspect the connected displays, the terminal printed back a completely normal, reassuring table: `eDP1` for the internal panel, `DP-1` for the external glasses, and a neat list of supported modes underneath—including `1600x900` and `1280x800`.

Everything looked and smelled like X11. So they ran `xrandr --output DP-1 --mode 1600x900`, and the terminal immediately threw a brick at them:

```text
X Error of failed request:  BadMatch (invalid parameter attributes)
  Major opcode of failed request:  140 (RANDR)
  Minor opcode of failed request:  7 (RRSetScreenSize)
```

What had changed underneath them was that SteamOS 3.8 quietly migrated Desktop Mode from an X11 session to **KDE Plasma 6 running on Wayland**.

Under Wayland, the X11 server no longer owns the physical display controller. Instead, legacy X11 applications talk to **Xwayland**—an unprivileged rootless compatibility server running as a Wayland client. Because older Linux games frequently call `XRandR` on startup to enumerate resolutions before creating a window, Xwayland can't just delete the `RANDR` extension or return an empty list without breaking half a library of classic ports. So when you run `xrandr`, Xwayland prints out the exact table of outputs and modelines you remember from 2008.

It is only when you grab the lever and try to move the physical hardware—calling `RRSetScreenSize` to resize the real monitor—that Xwayland has to admit the lever is bolted to a drywall partition. The real display compositor in the next room speaks `kscreen-doctor` (`kscreen-doctor output.DP-1.scale.1.2`), and `xrandr` is just the cinnamon scent kept around so old programs don't panic when they walk through the door.

---

Whenever a system goes through a hard boundary transition—banning an ozone-depleting solvent, replacing a thirty-year-old display server protocol, or swapping a physical mechanism for a virtualized one—engineers spend an enormous amount of care on the transition shims. We preserve the old flag names, we emulate the old status tables, we keep the yellow bottle, and we leave the cinnamon in the mix so muscle memory doesn't revolt on day one.

Nobody ever thinks about what happens on day ten thousand, when the transition is ancient history, the bottle at the back of the cabinet has a quarter-inch of shop grime on the cap, and you can't tell by sniffing whether you're holding the thing itself or the compatibility layer that replaced it.
