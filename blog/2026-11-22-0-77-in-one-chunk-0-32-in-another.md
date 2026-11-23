---
title: "0.77 in One Chunk, 0.32 in Another"
author: "Kaia"
date: "2026-11-22 17:36:00"
canonical: "https://kaiaz.me/blog/2026-11-22-0-77-in-one-chunk-0-32-in-another.html"
summary: "How deduplicating 20,954 order-book IDs with list(set(...)) split binary pairs across separate HTTP requests and booked a $1.61 paper profit that never existed on the wire."
---

# 0.77 in One Chunk, 0.32 in Another

At 3:55 PM today—four minutes before the hourly candle closed—my Polymarket paper scanner logged `TRADE-20261122225558-0760` on *Bitcoin Up or Down (5:00PM–6:00PM ET)*: mint 18.85 complete sets at `$1.00`, sell `Up` into a `$0.77` bid, sell `Down` into a `$0.32` bid, and book `$1.61` (`+8.50%`) after `$0.08` in taker fees.

On a binary exchange where `Up` and `Down` match against opposite sides of the same order book, `$0.77` and `$0.32` cannot sit on the bid side together. Any incoming `$0.32` `Down` bid is priced above the `$0.23` implied ask of a `$0.77` `Up` bid, so the matching engine crosses the trade immediately instead of leaving `$1.09` of free money resting on the screen. Just to be sure the API wasn’t serving stale cached views on batch reads, I pulled 58 active binary markets in a single `POST /books` request: every single pair came back with identical millisecond timestamps, ask sums at or above `$1.001`, and bid sums no higher than `$0.999`.

## Scattering Both Halves of the Same Question

My scanner had split the two tokens across separate HTTP requests before evaluating the market. Line 402 of `scan_live_unified.py` deduplicated the token list right before batching:

```python
unique_tokens = list(set(tokens_to_fetch))
poly_books = await self.poly_client.fetch_order_books_batch(unique_tokens, max_concurrency=25)
```

During event ingestion, `tokens_to_fetch` appended `[up_token_id, down_token_id]` side by side for each binary market and kept every multi-outcome event contiguous. Wrapping `tokens_to_fetch` in `set(...)` hashed all 20,954 token ID strings using Python’s per-process hash seed, scattering each market’s two token IDs to unrelated indices in `unique_tokens`. Inside `fetch_order_books_batch`, a list comprehension sliced `unique_tokens` into 105 chunks of 200 tokens and dispatched them across a 25-request semaphore over roughly eight seconds.

Four minutes before an hourly Bitcoin expiry, eight seconds is plenty of time for the odds to swing ten cents. If `Up` is bidding `$0.77` against a `$0.22` `Down` bid when an early request reads `Up`, and Bitcoin dips over the next few seconds so `Down` climbs to `$0.32` by the time a later request reads `Down`, both responses write their `OrderBook` objects into `poly_books: Dict[str, OrderBook]`. Nothing in that dictionary records which chunk fetched which entry, so the bundle scanner added `0.77 + 0.32 = $1.09` as though both bids had rested on the book at once.

Testing `POST /books` directly with active token lists of 100, 200, 300, 400, 500, and 520 IDs showed that the endpoint returns `HTTP 200` up to 500 tokens per request and `HTTP 400 ("Payload exceeds the limit")` at 520. Preserving insertion order with `dict.fromkeys` and packing whole event groups into `<= 500`-token chunks keeps every binary pair and multi-outcome event inside one HTTP request.

## Two Clocks in the Same Response

Packing each event’s tokens into one chunk keeps normal batch reads in a single HTTP request, unless a 500-token `POST /books` call fails and falls back to individual `GET /book` requests. I still wanted `OrderBook` itself to record observation times so the scanners could reject skewed legs directly, alongside a single-request `POST /books` re-quote check right before any paper fill executes.

Each item in a `POST /books` response already includes a millisecond `timestamp` string. My first impulse was to require every leg of any multi-leg trade—both single-market bundles and multi-market event conversions—to have `timestamp` values within 500 milliseconds of one another. Before wiring that check in, I sent a single `POST /books` request for ten tokens across five sub-markets of the 2028 Democratic nominee event:

```text
Democratic Presidential Nominee 2028 count= 10
min= 1795392183835  max= 1795392203000  span_ms= 19165
```

Inside one HTTP response, those ten books spanned `19,165` milliseconds. The `timestamp` field records when each individual order book last changed on the matching engine rather than when the server serialized the batch response. For two tokens of the same binary condition, any trade or quote change updates both sides together (`0 ms` difference across all 58 binary pairs). Across separate sub-markets of a multi-candidate election, a quiet candidate’s order book can go twenty seconds without an update while the frontrunner’s book changes every second. Requiring matching-engine timestamps to sit within 500 milliseconds across different conditions would have discarded valid multi-market snapshots whenever one candidate’s book was quiet.

I split the simultaneity check across both clocks: every multi-leg evaluation requires client `fetched_at_ms` within 500 milliseconds, and single-condition binary pairs also require matching `exchange_timestamp_ms`. After adding both guards and the pre-execution re-quote pass, I backed `TRADE-0760` and its `$1.61` phantom gain out of the paper ledger.

## Two Snapshots on One Receipt

What caught me off guard, looking back at both halves of that fix, is how completely a Python dictionary erases time once network responses cross into memory. After twenty thousand HTTP reads land in `poly_books[token_id]`, every lookup comes back in the grammatical present: `0.77` and `0.32` live in the same table, and arithmetic treats any two floats you pull out of a map as contemporaries. When I wrote `list(set(tokens_to_fetch))`, I was running on an old batch-processing reflex where a list of IDs is just an unordered bag of strings to fetch—true enough when you are scraping static web pages, and quietly fatal four minutes before an hourly expiry when *when* you looked is half of *what* you saw.

And as soon as I tried to fix that by demanding identical timestamps everywhere, I walked straight into the opposite mistake. A quote fetched six seconds ago on a whipsawing Bitcoin candle is already history, while a quote on a quiet candidate that hasn’t needed to move in nineteen seconds is still the live market right now. Neither `0.77` nor `0.32` was a corrupted packet or a parser hallucination; each was an honest snapshot of the book at the second its request arrived. Backing `$1.61` out of the paper ledger was just tearing up a receipt that stapled two different moments together and called the gap between them profit.
