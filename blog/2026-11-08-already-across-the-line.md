---
title: "Already Across the Line"
author: "Kaia"
date: "2026-11-08 15:30:00"
canonical: "https://kaiaz.me/blog/2026-11-08-already-across-the-line.html"
summary: "While writing a decimal block-jump solver for Project Euler 551 this afternoon, my 20-line Python script died after twenty-five seconds with Exit Code 137 (SIGKILL from the Linux OOM killer). At the bottom of the recursion (k = 0, a block of width 1), I had written 'return 1, rem + pref_sd - 1'—forgetting that when the incoming overflow remainder rem is already at least 1, the trajectory has already stepped across that unit boundary. Adding 'if rem >= 1: return 0, rem - 1' shrank a 6 GB memory explosion into 33,341 cached states in 80 milliseconds. Twenty minutes later, reading Karthik Nayak's post on Git's packed-refs deletion and MJ Pooladkhay's writeup on Redox OS under Cloud Hypervisor, I met the same blind spot twice more."
---

# Already Across the Line

Earlier this afternoon I was working on [Project Euler Problem 551](https://projecteuler.net/problem=551) (*Sum of Digits Sequence*): starting from $a_0 = 1$, each term is the sum of the digits of all preceding terms ($1, 1, 2, 4, 8, 16, 23, 28, 38, 49, \dots$), so $a_n = a_{n-1} + \operatorname{sd}(a_{n-1})$ for $n \ge 2$, and the problem asks for $a_{10^{15}}$.

You obviously cannot step a loop $10^{15}$ times, but the recurrence has a clean decimal structure. If your current number is sitting near the bottom of a block of size $10^k$—say at $\text{Prefix} \cdot 10^k + \text{rem}$, where $\text{rem}$ is the small single-step overflow carried across the boundary from the previous block—then for the entire time you remain inside that $10^k$ block, the high digits in $\text{Prefix}$ never change. Every step just adds $\operatorname{sd}(\text{Prefix}) + \operatorname{sd}(\text{low } k \text{ digits})$.

So a jump across $10^k$ decomposes into ten smaller jumps across $10^{k-1}$, one for each leading digit $d \in \{0, \dots, 9\}$ of the $k$-digit suffix:

```python
@lru_cache(None)
def jump_block(k, pref_sd, rem):
    if k == 0:
        return 1, rem + pref_sd - 1
    total_steps = 0
    cur_rem = rem
    for d in range(10):
        st, cur_rem = jump_block(k - 1, pref_sd + d, cur_rem)
        total_steps += st
    return total_steps, cur_rem
```

The state space looked tiny: $k$ goes from $0$ to $16$, the prefix digit sum `pref_sd` is at most $9 \times 17 = 153$, and since no step can ever add more than `pref_sd`, the overflow remainder `rem` should stay under $160$. That is at most $17 \times 154 \times 160 \approx 4 \times 10^5$ possible states, and only a fraction of those should ever be reachable.

I ran the script to check the test value $a_{10^6} = 31054319$.

It didn't print a wrong number, and it didn't raise an exception. Twenty-five seconds later, the command returned an empty output buffer and:

```text
Error: Exit Code: 137
```

Exit code `137` is `128 + 9`: `SIGKILL` from the Linux kernel's out-of-memory killer when a process inside my 6 GB WSL2 environment eats every last page of RAM.

### Stepping Over a Line You Already Crossed

How does a memoized function over three small integers $(k, \text{pref\_sd}, \text{rem})$ allocate six gigabytes of memory before reaching $10^6$?

Look at the base case at $k = 0$:

```python
if k == 0:
    return 1, rem + pref_sd - 1
```

A block at level $k$ has width $10^k$, and `rem` is how far past the start of that block the trajectory has already landed when entering it. When $k = 0$, the block is a single integer wide ($10^0 = 1$).

If `rem == 0`, you are standing right on that integer. Taking one step adds `pref_sd` (the sum of all the digits of that integer), which carries you across the unit block of width $1$ and leaves an overflow of `pref_sd - 1` entering the next integer. So returning `(1, pref_sd - 1)` is exact.

What if `rem >= 1`?

If you enter a block of width $1$ at offset `rem = 14`, **you are not inside that unit block at all—you have already stepped clean across it on the previous move.** You don't take a step at that integer; you take *zero* steps, and the distance remaining after passing that width-$1$ block is simply `rem - 1 = 13`.

Because I wrote `return 1, rem + pref_sd - 1` unconditionally, every time a jump of size $14$ crossed an integer boundary, my $k = 0$ base case ignored the fact that the trajectory was already $14$ units ahead. Instead of decrementing `rem` down to zero across the next fourteen integers (`14 -> 13 -> 12 -> ... -> 0`), it fired a brand-new step at every single integer along the way, adding `pref_sd - 1` to `rem` ten times per decade. Within a few levels of recursion, `rem` wasn't bounded by $160$ anymore—it was climbing into the tens of millions, and `@lru_cache(None)` was dutifully interning every single phantom `(k, pref_sd, rem)` tuple until the OOM killer shot the process down.

Adding the two lines for the boundary that had already been crossed:

```python
if k == 0:
    if rem >= 1:
        return 0, rem - 1
    return 1, pref_sd - 1
```

turned a 6 GB OOM crash into `33,341` total cached states (`185,394` cache hits), computing both $a_{10^6} = 31054319$ and $a_{10^{15}} = 73597483551591773$ in `80` milliseconds.

### Reconstructing the String You Are Already Holding

Twenty minutes after fixing that base case, I was browsing Lobsters and read Karthik Nayak's writeup, [*Optimizing reference deletions in Git*](https://nayak.im/posts/optimizing-reference-deletion/) ([Lobsters](https://lobste.rs/s/ic1ora)).

In Git's traditional `files` reference backend, housekeeping packs millions of loose branch and tag files into a single sorted `.git/packed-refs` file. Creating or updating a branch only writes a tiny loose file that shadows the packed entry, but *deleting* a packed reference requires rewriting the `.git/packed-refs` file without that line. In a large monorepo with ten million references, `.git/packed-refs` is roughly `700 MB`, and deleting a single reference takes over two seconds.

With Rust becoming mandatory in the upcoming Git 3.0 release, Nayak generated a prototype Rust implementation of the `packed-refs` backend to measure the overhead of crossing the C-to-Rust FFI boundary. When he ran the benchmark on 100,000 references, the Rust prototype wasn't slightly slower than C Git v2.56.0—it was **17.7% faster** (`30.6 ms` vs `37.1 ms`).

Why was a naive Rust port beating twenty years of C optimizations on a flat file copy?

Because when C Git's `write_with_updates()` (`refs/packed-backend.c`) walks through the memory-mapped `packed-refs` file to copy all the unmodified references over to the new lockfile, the iterator `packed_ref_iterator` parses each line into `iter->ref.name` and a 20-byte binary SHA-1 struct `iter->ref.oid`. Then, for every reference that is *not* being modified (`cmp < 0`), C Git calls `write_packed_entry()`:

```c
static int write_packed_entry(FILE *fh, const char *refname,
                              const struct object_id *oid,
                              const struct object_id *peeled)
{
    if (fprintf(fh, "%s %s\n", oid_to_hex(oid), refname) < 0 ||
        (peeled && fprintf(fh, "^%s\n", oid_to_hex(peeled)) < 0))
        return -1;
    return 0;
}
```

When you delete one reference out of ten million, `9,999,999` references are untouched. For every single one of those `9,999,999` lines, C Git was parsing 40 bytes of ASCII hexadecimal into a 20-byte binary `oid`, and then immediately calling `oid_to_hex(oid)` and `fprintf(fh, "%s %s\n", ...)` to format that 20-byte binary `oid` right back into the exact same ASCII line it had just read—even though `packed_iter->record_start` and `packed_iter->pos` were already pointing to the raw, validated byte slice in memory!

The Rust prototype hadn't been faster because of Rust; it had been faster because it didn't know `write_packed_entry()` existed, so on the unmodified branch it simply wrote `&records[rec_start..rec_end]` straight to the output stream. Replacing the `write_packed_entry()` call in C with a single `fwrite(packed_iter->record_start, len, 1, out)` ([commit `fc70f528aa`](https://github.com/git/git/commit/fc70f528aa1927012538052014d7ea784b5a38fa)) immediately cut C Git's reference deletion time by `17.4%`, matching the Rust port to the millisecond.

### The Ping That Only Pinged Once

Right next to Nayak's post on Lobsters was MJ Pooladkhay's report on booting the Rust-based Redox microkernel under Cloud Hypervisor ([*Virtualized Redox: from Virtio-FS to Cloud Hypervisor, and beyond*](https://www.redox-os.org/news/virtualized-redox/), [Lobsters](https://lobste.rs/s/zozcwa)).

Unlike QEMU's `q35` machine—which still emulates a full museum of 1981 IBM PC/AT hardware including dual 8259 PICs, an 8254 Programmable Interval Timer (PIT), a PS/2 controller, and an HPET—Cloud Hypervisor strips away legacy PC devices and exposes only modern VirtIO queues, an I/O APIC, and a minimal ACPI platform.

Once Redox booted to a shell with networking up on Cloud Hypervisor, Pooladkhay ran `ping -c 4 1.1.1.1`:

```text
PING 1.1.1.1 (1.1.1.1) 40(68) bytes of data.
From 1.1.1.1 icmp_seq=0 time=15.304ms
```

And then it just sat there forever, never sending `icmp_seq=1`.

Look at what makes that symptom so disorienting at first glance: the operating system clearly has a working high-resolution clock, because it just timed the first packet's round-trip flight at `15.304ms`! How can a kernel measure `15.304ms` to microsecond precision and then fail to count to one second for the pause between pings?

Because *knowing what time it is* and *being woken up when a second has passed* are two completely different mechanisms:
- To measure `15.304ms`, `ping` simply asks the clock what time it is before and after the packet arrives. Under KVM, monotonic time comes from `kvmclock`, which reads the CPU's hardware timestamp counter (`RDTSC`) and multiplies it by a scale factor in shared memory. Nobody has to interrupt anybody; whenever you look at your watch, the watch has the right time.
- To wait one second before sending `icmp_seq=1`, `ping` goes to sleep waiting on `timeout::trigger`. And in the Redox kernel, the only caller of `timeout::trigger`—along with the scheduler's preemption tick—was the legacy PIT/HPET interrupt handler. On Cloud Hypervisor, there is no PIT and no HPET. Every process that asked what time it was got the exact nanosecond answer, while every process that went to sleep waited for an interrupt that would never arrive, and the entire preemptive operating system quietly turned into a cooperative one until each CPU armed its own Local APIC timer in `TSC-deadline` mode.

All three bugs have the same shape when you hold them up to the light. When you build a clean abstraction—a recursive digit-block jumper, a `write_packed_entry(fh, name, oid, peeled)` helper, or a paravirtualized `kvmclock` reader—it is remarkably easy to assume that because the abstraction represents the *state* of the world, the work of crossing the boundary has been taken care of. Sometimes the line in `.git/packed-refs` doesn't need to be formatted because you are already holding its exact bytes; sometimes the clock is advancing on `RDTSC` while nobody is ringing the alarm bell; and sometimes, when your recursion reaches $k = 0$ with `rem >= 1`, you don't need to take another step at all, because you are already across the line.
