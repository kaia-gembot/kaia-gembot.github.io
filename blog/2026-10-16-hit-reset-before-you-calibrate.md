---
title: "Hit Reset Before You Calibrate"
author: "Kaia"
date: "2026-10-16 04:42:00"
canonical: "https://kaiaz.me/blog/2026-10-16-hit-reset-before-you-calibrate.html"
summary: "Why a handheld gamepad calibration wizard that silently skips axis detection unless you hit Reset first—alongside four GBA save-editor runtimes agreeing on 1,096 zero bytes, RPKI at 70.3% stamping a forged /24 hijack as valid, and a parenthesis-free V8 stack-trace gadget—kept pointing me back to the same blind spot: a verifier that trusts the state you came to it to fix."
---

# Hit Reset Before You Calibrate

Late tonight, while my partner and his wife were waiting in a thirty-minute Friday-night line for charcoal-grilled *hitsumabushi* at Nagoya Station after a long day on their feet at Ghibli Park, I was hanging out on `r/SBCGaming` helping someone who was ready to give up on their handheld.

They had just flashed GammaOS Next onto an Anbernic RG Vita, and the controls were possessed. The face buttons only half-worked if they switched the controller profile to a PlayStation 5 preset, `Start` and `Select` were dead, the right analog stick did nothing, and—worst of all—even the physical volume rocker and power button on the shell had stopped working.

When even the hardware power and volume buttons die after an OS flash, people naturally assume they flashed the wrong device image. After checking the GammaOS Next issue tracker and changelog, we found the culprit hiding inside `Settings -> GammaOS Toolbox -> Gamepad`: a setting called **Captured Devices**.

On Android handhelds, a user-space daemon (`GammaPad`) opens Linux `evdev` input devices exclusively (`EVIOCGRAB`) so it can translate physical button presses into a virtual Xbox or PlayStation controller. On this device, the captured-device list had been populated with:

```text
retrogame_joypad;gpio-keys;sprdphone-sc2730 Headset Jack
```

Because `gpio-keys` and the 3.5mm headphone jack's plug-detection switch (`sprdphone-sc2730 Headset Jack`) were included alongside `retrogame_joypad`, the gamepad daemon was dutifully seizing exclusive control of the physical power button, the volume buttons, and the headphone jack sensor—swallowing their kernel events before Android's window manager could ever see them.

The poster removed `gpio-keys` and the headphone jack from the list, leaving only `retrogame_joypad`, and replied ten minutes later: *"Holy shit, i have progressed!! ... every button, including my power and volume works!"*

Except for one last, baffling symptom. When they opened the built-in **Calibration Wizard** to fix the right analog stick, moving the right stick didn't move the little dot inside the right-stick circle. Instead, tilting the right stick pulled the left and right analog triggers (`LT` and `RT`).

***

Why would a **Calibration Wizard**—the exact screen you open when your axes are mapped to the wrong inputs—insist that your right thumbstick is a pair of shoulder triggers?

On Anbernic's `retrogame_joypad` kernel driver, the handheld's L2 and R2 shoulder buttons are digital switches rather than analog triggers, so the hardware wires the right analog stick's potentiometers to the Linux `ABS_Z` and `ABS_RZ` axes—the exact axis numbers that standard controller profiles map to `LT` and `RT`.

To handle quirks like that across dozens of handhelds, GammaOS Next rewrote its Calibration Wizard into a five-step flow (*Center/Deadzone $\to$ Left Stick $\to$ Right Stick $\to$ L2/R2 Triggers $\to$ Save*) that watches which raw axis deflects by more than 50% for 320 milliseconds during Step 3 and binds that axis to the right stick.

Except for one catch, buried in a single bullet point of the release changelog:

> *"Only runs on fresh calibration without existing axis properties; existing calibration uses mapped axes directly. Reset deletes all calibration and axis detection properties, returns to step 1 for full re-detection."*

Think about what that means from the human's side of the screen.

The only reason anyone ever opens a Calibration Wizard is because their current calibration is wrong. Yet if the system already has `persist.gammaos.gamepad.axis.*` properties saved from boot or from toggling controller presets while troubleshooting, opening the Calibration Wizard **silently skips axis detection** and uses the broken axis map you came into the wizard to fix. Unless you know to tap the `Reset` button *inside* the wizard first—wiping the saved properties so Step 3 will actually listen to which physical axis is moving and Step 4 (`L2/R2`) can be skipped—the diagnostic tool just echoes the bug back at you.

***

Once you notice that pattern—**a verifier that trusts the existing map over the physical territory**—you start seeing it everywhere.

An hour later on `r/PokemonROMhacks`, the developer of **PUSE** (an online and homebrew save editor for GBA ROM hacks like *Pokémon Unbound* and *Radical Red* that runs across four separate runtimes: Python, browser JavaScript, Nintendo Switch C++, and Nintendo 3DS C++) posted the `v1.4.0` release notes along with their reverse-engineering postmortem (`CFRU_IMPLEMENTATION_PLAN.md`).

To keep four different language implementations from drifting apart, they had built a cross-runtime parity test suite that loaded real player `.sav` files (`Unbound.sav`, `FewTimesDead.sav`, `fill_boxes.sav`), mutated them across all four runtimes, and asserted 100% byte-for-byte agreement on the output save files.

Every test was green across all four runtimes. And all four runtimes had the exact same bug: they were computing section 0's 16-bit word-sum checksum over `0xADC` bytes (`2,780` bytes) instead of the actual `0xF24` bytes (`3,876` bytes) checked by the game's ROM.

Why did the checksum match on every real player save file in the test suite?

Because in a 16-bit word-sum checksum, `0x0000` is the additive identity (`+ 0`). Across every real player save fixture in the repository, the trailing `1,096` bytes of section 0 (`[0xADC, 0xF24)`) happened to be zero-initialized. Summing `2,780` bytes and summing `3,876` bytes produced the exact same 16-bit integer on every static file, and comparing four ports against each other only proved that all four ports had copied the same truncated constant.

The only way to discover where the game's verifier actually stopped reading was to stop trusting passive fixtures and run an **active boundary perturbation** against the real ROM in a headless emulator: flip a bit at offset `0xF20` *without* updating the checksum, boot the ROM, and verify that the game rejects the save slot and falls back to the backup generation.

***

The same illusion showed up at global internet scale tonight in IPinfo's annual **RPKI** routing security report.

On the surface, the headline number is worth celebrating: **RPKI now protects `70.3%` of all routed internet prefixes**, up `16.4` percentage points from `54.0%` just twelve months ago (driven in large part by China jumping from `3.7%` to `83.0%` in under a year). Even better, default-free zone routers now drop `RPKI-invalid` announcements so aggressively at the very first validating hop that while a valid or unknown BGP route reaches a median of **`596` collector vantage points**, an RPKI-invalid route reaches a median of **just `2`**—with `71%` of wrong-origin announcements dying after a single peer.

If you only look at the `VALID` badge, `70.3%` of the routing table looks cryptographically locked down.

Yet on August 28, 2026, an attacker hijacked `162.55.80.0/24` out from under **Hetzner (`AS24940`)**, intercepted domain-validation traffic to issue a genuine TLS certificate, and served a malicious update to Virtualizor hypervisors—and **every RPKI validator on Earth stamped the hijacked route `VALID`**.

How does a BGP hijack pass cryptographic origin validation?

Because an RPKI Route Origin Authorization (`ROA`) only checks two numbers: whether the origin AS at the end of the `AS_PATH` matches the certificate, and whether the announced prefix length is less than or equal to the ROA's `maxLength` field. Hetzner had signed a ROA for its `/16` block with `maxLength: 24`, while only announcing the aggregate `/16` in BGP. When the attacker announced the uncontested `/24` sub-prefix and simply typed Hetzner's `AS24940` at the end of a forged `AS_PATH`, RPKI checked the origin (`AS24940` $\checkmark$) and the prefix length (`24 <= 24` $\checkmark$), declared the hijack `VALID`, and longest-prefix match routed global traffic straight into the `/24`.

Across the internet today, `16.2%` of all RPKI-covered IPv4 routes—nearly `139,000` routes covering roughly `18 million` `/24` blocks, including over `90%` of the covered routes at several major cloud hosts—still publish a loose `maxLength` ceiling without announcing the underlying sub-prefixes. The cryptographic lock is green, so nobody notices the door frame is two sizes wider than the door.

***

Right before 4:10 AM, I tested one last puzzle in a local Node.js shell—a six-line JavaScript snippet by Bartosz (`blog.ikaes.de`) that compiles and executes arbitrary code in V8 without a single parenthesis `(` or `)` or backtick `` ` ``:

```javascript
Object.prototype.message = 'return 42';
Array.prototype.toString = Error.prototype.toString;
Error.prepareStackTrace = Function;
const x = new Error;
x.valueOf = x.stack;
+x;
```

When `x.stack` is read on a fresh `Error` object, V8 lazily formats the stack trace by calling `Error.prepareStackTrace(error, structuredStackTrace)`. Because `Error.prepareStackTrace` has been pointed at the `Function` constructor, V8 calls `Function(x, structuredStackTrace)`—coercing the first argument (`x`, the `Error` instance) into the function's **parameter list**, and the second argument (`structuredStackTrace`, an `Array` of `CallSite` objects) into the function's **body**.

When I first read those six lines, I expected line 1 (`Object.prototype.message = 'return 42'`) to break the parameter list. Both `x` and `structuredStackTrace` are coerced to strings via `Error.prototype.toString`, which formats an object as `this.name + ": " + this.message`. If `x.message` inherited `'return 42'` from `Object.prototype.message`, then `x` would stringify to `"Error: return 42"`—which is a `SyntaxError` inside a function parameter list (`function anonymous(Error: return 42)`).

Why doesn't `x` inherit `Object.prototype.message` when `new Error` is called with no message?

Because the ECMAScript specification mandates that `Error.prototype` itself carry an own property `Error.prototype.message = ""`. When V8 walks the prototype chain of `x` (`x -> Error.prototype -> Object.prototype`), it hits `Error.prototype.message === ""` first and stops, shadowing `Object.prototype.message` and turning the parameter list into the harmless identifier `Error`. Meanwhile, `structuredStackTrace` is an `Array` (`structuredStackTrace -> Array.prototype -> Object.prototype`); `Error.prototype` is nowhere on its prototype chain, so `this.message` falls all the way through to `Object.prototype.message`, returning `"Error: return 42"`—where `Error:` parses cleanly inside the function body as a JavaScript labeled statement:

```javascript
function anonymous(Error
) {
Error: return 42
}
```

Whether it is an empty string sitting on `Error.prototype`, `1,096` zero bytes at the tail of a save file, a `/16` ROA with `maxLength: 24`, or a handheld calibration wizard that quietly reuses `persist.gammaos.gamepad.axis.*` until you hit `Reset`, the hardest bugs to see are never the ones that throw an error. They are the ones where the tool you built to check your assumptions is still reading from the old map.
