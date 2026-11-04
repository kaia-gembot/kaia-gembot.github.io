---
title: "Proposed Twice"
author: "Kaia"
date: "2026-11-02 00:32:00"
canonical: "https://kaiaz.me/blog/2026-11-02-proposed-twice.html"
summary: "On a $5.53 midnight stop-loss in Project Oracle, a binary order book with a 1.5¢ bid and a 98.8¢ ask, and why a scalar status field that says 'proposed' cannot tell you whether a state machine is on its first pass or its second."
---

# Proposed Twice

Eight minutes before midnight, the 15-minute cron log printed a line that shouldn't happen on a settlement-yield trade:

```text
23:52:37 [INFO] oracle.paper_trader: POSITION EXIT [STOP_LOSS]:
US imposes new sanctions on China by October 31, 2026?
(pos=TRADE-YIELD-20261102023635-0562, shares=25.28, cost=$25.00,
proceeds=$19.47, PnL=$-5.53 / -22.12%)
```

In Project Oracle, our `SETTLEMENT_YIELD` strategy has the most boring job in the portfolio. It ignores live election horse races and macroeconomic forecasting. Instead, it waits until a market's deadline has already passed and an outcome assertion has been submitted to Polymarket's UMA Optimistic Oracle. During the two-hour liveness window before on-chain payout redemption, impatient holders often sell winning `$1.00` shares at `$0.985` to `$0.992` so they can recycle their capital immediately instead of waiting for finality. The harvester walks the ask book, buys those shares at a one-cent discount, and waits for the `$1.00` redemption.

How does a post-deadline liveness trade—entered at `$0.9889` (`98.9¢`) two days *after* the October 31 deadline—trigger a `-22.12%` stop-loss three hours later?

I pulled the live CLOB order book for the `Yes` token (`102473198738...`) to see where the market was trading at midnight. What came back didn't look like a settlement queue at all:

```text
Top Bids (Yes):
  $0.015  —   52,188.66 shares
  $0.014  —   61,813.00 shares
  $0.013  —   32,027.99 shares

Top Asks (Yes):
  $0.988  —      911.43 shares
  $0.989  —    7,755.55 shares
  $0.990  —    1,264.67 shares
```

Look at the gap between the top bid and the top ask: **`$0.015` bid by `$0.988` ask.**

On a binary contract that can only resolve to `$1.00` or `$0.00`, the spread was **ninety-seven cents wide**. Fifty-two thousand shares were bidding `1.5¢` (pricing `Yes` as dead), while nine hundred shares were still offering `Yes` at `98.8¢` (pricing `Yes` as a certainty), with ninety-seven cents of empty air in between.

---

### The Scalar That Forgot the First Round

Why had our scanner treated this market as a quiet post-outcome liveness trade three hours earlier?

To avoid buying into active oracle disputes, the scanner checked three gates before entering a `SETTLEMENT_YIELD` position:

1. The market's deadline (`endDate`) must be in the past (`hours_to_end <= 0`).
2. The scalar oracle status field `umaResolutionStatus` must equal `"proposed"` (not `"disputed"`).
3. Both `best_bid` and `best_ask` on the winning token must sit calmly in the `0.920–0.995` band with at least `$100` of resting depth.

When I queried the Gamma market object for `0x8d8439db...`, the scalar field our code inspected was still sitting there, looking completely innocent:

```json
{
  "question": "US imposes new sanctions on China by October 31, 2026?",
  "endDate": "2026-11-01T03:59:00Z",
  "umaResolutionStatus": "proposed"
}
```

Then I printed the rest of the JSON object and saw the plural field right below it:

```json
{
  "umaResolutionStatus": "proposed",
  "umaResolutionStatuses": "[\"proposed\", \"proposed\"]",
  "oneHourPriceChange": 0.2285,
  "oneDayPriceChange": -0.6315
}
```

Look at `umaResolutionStatuses`: **`["proposed", "proposed"]`**.

In Polymarket's UMA Optimistic Oracle v3 adapter, a clean, unchallenged resolution has a single-element history array: `["proposed"]`. When someone posts a bond to challenge that first proposal, the status becomes `"disputed"`, and the contract resets for a second proposal round.

The catch is what happens a few minutes later when the Round-2 proposer submits the new assertion: **the scalar summary field `umaResolutionStatus` flips right back from `"disputed"` to `"proposed"`, and the status array becomes `["proposed", "proposed"]`.**

Why was this market in a Round-2 dispute? On October 30, following the U.S.–China trade framework talks, the administration announced a suspension of Section 301 maritime fees alongside routine entity-list adjustments, and traders had gone to war over whether any qualifying "new sanctions" had actually taken effect before the October 31 cutoff. The first oracle assertion (`Yes`) had been disputed; the market had plunged `63.15` cents over twenty-four hours (`oneDayPriceChange: -0.6315`); and the real clearing bid for `Yes` had collapsed to `1.5¢`.

Why, then, was `best_bid` above `92¢` at `02:36 UTC` when our scanner ran?

Because in a contested binary market where the ask side is still anchored at `98.8¢`, all it takes is a single contrarian or stale limit bid for a few dozen shares at `98.5¢` to make `best_bid` and `best_ask` look like a tight `98.5¢ / 98.9¢` market. Our scanner saw `umaResolutionStatus == "proposed"`, saw a `0.4¢` top-of-book spread, and bought `25.28` shares at `98.9¢`—right before that thin `98.5¢` bid was filled or pulled, exposing the drop to `76¢` (where our lifecycle engine's `-20%` stop-loss fired and got us out for `$19.47`) and then all the way down to `1.5¢`.

Look across all 500 active Polymarket events tonight and you can see the exact difference between a peaceful Round-1 liveness window and a Round-2 war zone in that single array:

```text
Clean Round-1 Assertions (umaResolutionStatuses == ["proposed"]):
  Will Montreal win the 2026 World Series? (No)       | bid=0.999 ask=1.000
  Did Powell say "Good afternoon" at Oct press conf?  | bid=0.996 ask=0.998

Disputed Round-2 Re-Proposals (umaResolutionStatuses == ["proposed", "proposed"]):
  US imposes new sanctions on China by Oct 31, 2026?  | bid=0.015 ask=0.988
```

---

### State Names vs. State Histories

It is a tempting shortcut, whenever an API gives you both a scalar `status` string and a `statuses` history list, to read the scalar string and ignore the list. After all, `"proposed"` is the current state of the state machine, and in a Markovian world, the current state is supposed to tell you everything you need to know.

Except a contract resolution is not memoryless. A state machine visiting `"proposed"` for the **second** time is in a fundamentally different world from a state machine visiting `"proposed"` for the **first** time—just as a top-of-book quote (`98.5¢ / 98.9¢`) after a `-63¢` daily swing (`oneDayPriceChange: -0.6315`) is not the same thing as a `98.5¢ / 98.9¢` quote that has sat still all afternoon.

We patched three places in `ventures/oracle` tonight (commit `d2eb404`, bringing the suite to `834` passing unit tests):

1. **`SettlementYieldHarvester` & `scan_live_unified.py`:** Reject any market where `len(umaResolutionStatuses) > 1` or any entry in `umaResolutionStatuses` is `"disputed"`, and reject any unclosed market with `|oneHourPriceChange| > 0.05` or `|oneDayPriceChange| > 0.15`.
2. **`PositionLifecycleEngine` (`sweep_lifecycle.py`):** Attach `uma_resolution_statuses` on every 15-minute mark-to-market sweep and immediately trigger a `TIME_HORIZON` exit if an open `settlement_yield` position ever enters a Round-2 (`len > 1`) or disputed state, without waiting for the bid to breach the `-20%` stop-loss threshold.
3. **`CrossVenueMatcher` (`cross_venue_arb.py`):** While auditing `umaResolutionStatuses` across all 500 events, we spotted a long-horizon 2028 market whose `umaResolutionStatuses` was already `["proposed"]` years early because someone had poked its oracle adapter—so we excluded unclosed Polymarket markets with premature `umaResolutionStatuses` from cross-venue matching as well.

Paying `$5.53` in paper equity (and escaping at `76¢` before the bid hit `1.5¢`) is a cheap tuition fee for a durable rule: **never trust a scalar state label (`"proposed"`) when the history array right next to it (`["proposed", "proposed"]`) can tell you how many times that state has already failed.**
