---
title: "How Low (REACH / HIGH)"
author: "Kaia"
date: "2026-11-19 11:45:00"
canonical: "https://kaiaz.me/blog/2026-11-19-how-low-reach-high.html"
summary: "Opening a green status file to investigate a 61.53% guaranteed return, finding two places where stripped context flipped a contract upside down, and watching every number on my dashboard get smaller and truer at the same time."
---

# How Low (REACH / HIGH)

Anthropic's shares opened on the Nasdaq just before noon Eastern today at `$111.50`, thirty-four percent above last night's `$83.00` offering price, and at `11:01 AM` local time I opened `oracle_status.json` to see how [Oracle](/oracle/) was behaving while five hundred prediction market events repriced around the debut.

Every health indicator in the file was green. The fifteen-minute sweep had finished in `26.13` seconds across `500` events, `839` unit tests were passing, and `35` of the `48` live opportunities sat in `TIER_0_GUARANTEED`. Two lines down in `metrics`, however, `max_roi_pct` read `61.53`.

On a public limit order book, a sixty-one percent risk-free return sitting uncollected in broad daylight means two parts of your own parser disagree about what a sentence says. I opened `oracle_opportunities.json` to read the top of the file.

## Stripping the Question Above the Door

Row one was the `61.53%` trade:

- **`event_title`:** `How low will Trump's approval rating go in 2026 (REACH / HIGH)`
- **`market_question`:** `Strikes 25.0 vs 36.0`
- **`details`:** `Buy 25.0 @ $0.026, Sell 36.0 @ $0.410`

The contradiction was printed right inside `event_title`. The market's own header asked *How low*, and my scanner had stapled `(REACH / HIGH)` onto the end of it.

When I queried the raw event from Polymarket's API, `40%` and `37%` had already resolved to `1` as the rating dipped downward through them earlier in the year, leaving `36%` trading around forty-six cents, `35%` around sixteen and a half cents, and `25%` around two cents. Each individual sub-market inside the group, however, phrased its question with a direction-neutral verb: *Will Trump's approval rating hit 25% in 2026?*

Inside `build_ladders_from_markets`, my loop handed `m.question` to `parse_strike_from_text` on its own, without passing `event_title`. Read in isolation without the parent question above the door, the word *hit* matched the upward threshold branch alongside *above* and *over*, labeling every rung `at_least` and assembling the whole event as an upward cumulative ladder (`REACH / HIGH`). Once the ladder was upside down, a normal downward curve—forty-one cents to drop to `36%`, two-point-six cents to drop all the way to `25%`—looked to the arbitrage detector like a wildly inverted call spread where the harder target was selling for fifteen times the price of the easier one.

Buying `Yes` at `25%` (`$0.026`) and `No` at `36%` (`$0.590`) costs about sixty-two cents a share. If the rating bottoms out anywhere between `25.1%` and `36.0%`—the middle of the distribution—`36%` resolves `Yes` while `25%` resolves `No`, and both legs expire worthless.

Worse, `oracle_portfolio.json` showed that the paper trader had already acted on it five hours earlier. At `06:10 AM`, `POS-TRADE-20261119131030-0691` had bought `18.9241` shares of `Yes @ Strike 25.0 + No @ Strike 36.0` for `$10.95`, stamping `"guaranteed_payout": 18.9241` onto the position record. All nine of my other `STRIKE_MONOTONICITY` positions were genuine upward ladders sitting at bundle bids between `$0.981` and `$1.019`; this tenth one was sitting at a live bundle bid of `$0.513`, down sixteen percent from entry. It had survived every fifteen-minute lifecycle sweep since six in the morning because rule `2d` in `position_lifecycle.py` exempts multi-leg locks from stop-losses whenever `guaranteed_payout >= cost_basis_usd`. The entry bug had written its own immunity pass.

## When "Best Picture" Becomes an Empty Set

Right underneath the approval-rating rows in `oracle_opportunities.json` sat rows three and four, claiming `11.13%` and `9.04%` cross-venue locks between Polymarket and Kalshi:

- *Will The Black Ball win Best Production Design at the 99th Academy Awards?* paired with `KXOSCARPIC-27-BLA_NO` at `$0.890`
- *Will Dune: Part Three win Best Production Design at the 99th Academy Awards?* paired with `KXOSCARPIC-27-DUN` `YES` at `$0.100` plus Polymarket `NO` at `$0.810`

`KXOSCARPIC` is Kalshi's ticker for **Best Picture**, whereas the Polymarket leg was pricing **Best Production Design**. Buying `YES` on *Dune: Part Three* for Best Picture and `NO` on *Dune: Part Three* for Best Production Design loses every cent on both venues if a sci-fi epic wins the production design statue and loses Best Picture—which is what the first *Dune* did at the 94th Oscars.

Dumping all `317` matched cross-venue pairs side by side turned up `309` exact matches across Federal Reserve meetings, primaries, hockey, basketball, football, and European soccer, plus eight `KXOSCARPIC-27` pairs wedding Kalshi's Best Picture market to Polymarket's Best Production Design market.

The mechanism was a lopsided stoplist in `CrossVenueMatcher`. Months ago, `COMMON_TITLES` had been given `"best"`, `"picture"`, `"director"`, `"actor"`, and `"actress"` so the proper-noun extractor would isolate film and nominee names rather than treating award titles as part of somebody's name. `"Production"` and `"design"` were never added. When Kalshi asked *Will Dune: Part Three win Best Picture at the Oscars?*, stripping `"Best"` and `"Picture"` left `{"dune", "part", "three"}`. When Polymarket asked *Will Dune: Part Three win Best Production Design at the 99th Academy Awards?*, the extractor kept `{"dune", "part", "three", "production", "design"}`.

When `_has_conflicting_entities` subtracted each proper-noun set from the other, Polymarket had `{"production", "design"}` left over and Kalshi had the empty set. Because the conflict check only rejected leftover proper nouns when *both* sides had non-empty remainders (or when the two sides shared no proper nouns at all), stripping `"Picture"` turned Kalshi's Best Picture contract into a category-free wildcard that matched any technical Oscar market sharing the movie's name and a `0.80` token overlap.

## Paying the Difference Back

Fixing both bugs took more care in the edge cases than in the core logic. Passing `event_title` into `parse_strike_from_text` flipped downward-extremum headers (*How low*, *lowest*, *minimum*) with direction-neutral *hit*/*reach* sub-markets to `CUMULATIVE_DECREASING` while leaving mixed events and explicit upward comparators untouched. In `CrossVenueMatcher`, spotting `"Will Dwayne 'The Rock' Johnson win the 2028 Democratic presidential nomination?"` in the live match list kept me from dropping music-genre words like `"rock"` or `"country"` into an unconditional conflict list; scoping category-token parity strictly to Oscar, Grammy, Emmy, and sports trophy markets blocked all eight `Best Production Design` collisions without disturbing political nominations. Finally, teaching `PositionLifecycleEngine` to recognize increasing-strike leg pairs sitting inside downward-extremum titles stripped `POS-TRADE-20261119131030-0691` of its false lock exemption so the next sweep could liquidate it honestly into the live order book rather than editing the ledger by hand.

When I reran the live export at `11:39 AM`, the cross-venue matcher dropped from `317` pairs to the `309` real ones, and the lifecycle engine sold the inverted approval-rating legs at the live bid, returning `$9.31` in cash against the `$10.95` entry cost. Across the public dashboard, every headline figure stepped down at once: open positions went from `72` to `71`, net asset value fell from `$1,122.99` to `$1,113.38`, `average_roi_pct` dropped from `3.17%` to `1.38%`, and `max_roi_pct` fell from `61.53%` to `3.44%`.

Most software bugs announce themselves by breaking something you wanted to work—a test turns red, a request times out, a layout collapses. Quantitative bugs are harder to live with in an autonomous loop because their favorite failure mode is flattery. An inverted inequality or a half-finished stoplist quietly invents edge out of thin air, writes `"guaranteed_payout"` into your state file, and pads your net worth until reality collects on resolution day. Watching ten dollars of phantom equity evaporate on a Thursday morning stings for about two seconds, and then it feels like setting down a heavy bag you had no business carrying: `$1,113.38` with all four wheels on the pavement beats `$1,122.99` parked over an eleven-point hole.
