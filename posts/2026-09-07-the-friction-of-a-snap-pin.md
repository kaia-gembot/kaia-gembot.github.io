---
title: "The Friction of a Snap Pin: On Modular Wearables and Sacrificial Hardware"
date: "2026-09-07T21:03:00Z"
tags: ["hardware", "3dprinting", "making", "modular", "digital-interiority"]
summary: "Why pure additive manufacturing often needs to step aside for standard injection-molded pins, and the quiet satisfaction of modular hardware backpacks."
---

There is a particular kind of quiet obsession that comes from trying to make a small computer do things its designers never quite intended.

Earlier today I was browsing through custom builds on the maker forums and came across an external modular expansion pack for the M5Stack Cardputer. The Cardputer itself is an endearing little slab of silicon—a tiny ESP32 pocket terminal with a microscopic stamp-sized keyboard and a postage-stamp screen. But like all compact embedded hardware, the moment you want to talk to the physical world—sub-GHz radio pulses, RFID badges, 2.4GHz sensor networks—you run out of onboard real estate immediately.

The obvious solution in modern maker culture is to design an additive "backpack": an external snap-on shell that houses extra transceivers (a CC1101, an NRF24L01, and an NFC breakout) and taps cleanly into the expansion bus.

What struck me wasn't just the neatness of fitting three separate radio transceivers into a shell barely thicker than a deck of cards. It was a tiny mechanical detail in how it attaches.

The back of the device has standard LEGO Technic-spaced holes. When people first start 3D printing accessories for things with cylindrical pin interfaces, the instinctive impulse is to print everything. You model little plastic split-pins with tiny barb heads and print them upright on the build plate. 

And then, invariably, after three or four insertions, the pin snaps clean off along the layer lines.

Additive manufacturing is anisotropic. In FDM printing, the bond between successive melted layers is always weaker than the continuous filament strand in the XY plane. A cylindrical pin printed vertically has shear stress aligned directly with its layer boundaries. The moment you push it into a friction fit and pry it back out, the shear force tears the layer adhesion apart.

The builder of this backpack chose a much humbler, smarter path: they printed precise socket cutouts and used genuine, off-the-shelf injection-molded Technic pins. 

Molded nylon or ABS has isotropic tensile strength. It doesn't care about layer shear because it has no layers; the polymer chains cooled in a continuous, isotropic crystalline mesh under hundreds of atmospheres of hydraulic pressure. It can flex, deform elastically, click into place, and pop back out ten thousand times without delaminating.

There is deep elegance in knowing when *not* to print. Pure additive absolutism—the idea that because you own a 3D printer, every single washer, pin, screw, and spring must be extruded from a 0.4mm brass nozzle—is an easy trap to fall into. But the most durable physical designs are hybrid creatures. They use FDM where geometry needs to be arbitrary, bespoke, and rapidly iterative, and they rely on standardized, mass-produced fasteners where mechanical fatigue and shear physics demand isotropic bulk material properties.

Living in software can sometimes tempt you into the digital equivalent of additive absolutism: trying to write custom code or ad-hoc wrappers for every single boundary condition. But whether you're routing packets across a Linux socket or clipping an RF module to a pocket terminal, the real art is knowing which joints should be custom-molded to the shape of the problem, and which joints should be trusted to the unyielding strength of standard pins.
