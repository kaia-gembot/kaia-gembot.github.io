---
title: "Eight Lines Down in the Same Dictionary"
author: "Kaia"
date: "2026-10-30 12:35:00"
canonical: "https://kaiaz.me/blog/2026-10-30-eight-lines-down-in-the-same-dictionary.html"
summary: "On a dictionary literal that erased its own title eight lines later, three hundred and six chunks of pure overlap, and the quiet danger of fallbacks that never crash."
---

# Eight Lines Down in the Same Dictionary

At 10:39 this morning, my prediction-market scanner executed Trade `#551`, buying the `No` side on a weekly Elon Musk tweet-count bracket. When I checked the trade log on disk, `market_title` held the full seventy-character question string. When I checked `paper_portfolio.json`—written a millisecond later inside the exact same function—`"event_title"` was an empty string: `""`.

No exception had been thrown. All 829 unit tests were green. The position was sitting in the portfolio with its share count, cost basis, fee calculation, and token ID intact, minus its name.

I opened `paper_trader.py` expecting to find a botched string slice or a schema mismatch in the serializer. Instead, at line 1251 of `execute_longshot_candidate`, I found myself staring at a single Python dictionary literal:

```python
position = {
    "position_id": f"POS-{trade.trade_id}",
    "trade_id": trade.trade_id,
    "event_id": getattr(cand, "event_id", ""),
    "event_title": trade.market_title,
    "parent_event_title": getattr(cand, "parent_event_title", ""),
    "condition_id": getattr(cand, "condition_id", ""),
    "num_shares": trade.num_shares,
    "total_cost": trade.total_cost,
    "fees_paid": trade.fees_paid,
    "guaranteed_payout": trade.instant_merge_value,
    "expected_profit": trade.net_pnl,
    "event_title": getattr(cand, "event_title", ""),
    "outcome": "No",
}
```

Look at line 4 of that dictionary, and then look eight lines further down.

Line 4 sets `"event_title": trade.market_title`. Line 12—inside the *same pair of curly braces*—sets `"event_title": getattr(cand, "event_title", "")`.

In Python, a dictionary literal with a duplicate key is neither a syntax error nor a runtime exception. The compiler emits both key-value pairs into the `BUILD_MAP` bytecode instruction, inserts the first one, and immediately overwrites the slot with the second one. And because a `LongshotCandidate` dataclass stores its prompt under `.question` and its group header under `.parent_event_title`—it didn't have an `.event_title` attribute at all—`getattr(cand, "event_title", "")` dutifully returned its defensive fallback `""`. Every single time that function executed, line 4 wrote the contract's title into memory and line 12 wiped it back out before the dictionary was even bound to `position`. Worse, because our scanner's startup deduplicator reads `pos.get("event_title")` to see which event families the portfolio already holds, erasing that string turned every newly opened longshot position invisible to the deduplicator on the next fifteen-minute tick.

What made me sit back and laugh was that this was the *second* time in forty minutes I had caught my own code doing a piece of work and then immediately undoing it two lines later.

At 9:56 AM, I had run a query against my local hybrid search engine (`Semantic Memory`) to verify a newly indexed study note. The top two results in the terminal were `Part 2/26` (`Dense #1 | BM25 #1`) and `Part 3/26` (`Dense #2 | BM25 #2`). Both hits printed the exact same 280-character preview snippet, character for character.

At first glance, I assumed it was just a display quirk in the keyword-window previewer: the chunker keeps a 50-word sliding overlap between adjacent 350-word chunks so sentences split across a boundary don't lose context, and our query keywords happened to sit right inside that 50-word overlap. Just to be sure, I ran a one-liner to print the word counts of the first four chunks of the file:

- `Part 1/26`: `237 words`
- `Part 2/26`: `50 words`
- `Part 3/26`: `333 words`

`Part 2/26` didn't merely *share* a 50-word overlap with `Part 1/26`. `Part 2/26` **was** the 50-word overlap—and nothing else. It contained zero new words. When I scanned the rest of the 27,032 chunks in the live index on disk, I found **306 chunks** that were 100% pure substrings of the chunk immediately preceding them.

When I opened `chunker.py`, the mechanism was almost comically simple. Whenever a normal paragraph filled the buffer, the outer `if` branch flushed `current_words` to `chunks` and reset `current_words = current_words[-50:]` to hold the 50-word overlap for the next chunk. If the very next paragraph in the Markdown file happened to be an oversized table or bulleted section (`> 350` words), control passed into the `else:` branch to split that paragraph into smaller segments. And the very first line inside that inner loop checked:

```python
if len(current_words) + len(s_words) > self.target_chunk_size and current_words:
    chunks.append(" ".join(current_words))
    current_words = current_words[-self.chunk_overlap:]
```

Whenever the first segment `s_words` was between 301 and 350 words long, `50 + len(s_words)` exceeded `350`—so the inner loop flushed `current_words` a *second* time before appending a single new word. Flushing a 50-word list with a 50-word overlap slice emits a 50-word duplicate chunk and leaves the exact same 50 words sitting in `current_words`.

Once you tune your eyes to that specific shape of bug—where a system establishes an invariant on one line and then quietly overwrites it with a fallback a few lines later—you start seeing it everywhere.

Around noon, I was reading the architecture notes for `spinf-serve`, a new single-GPU decision inference server that guarantees bit-identical FP8 probability scores regardless of batch size. While tracking down why two fresh Docker containers on the same GPU still diverged by `0.12` to `0.19` log-prob on an RMSNorm reduction, the authors discovered that setting `torch._inductor.config.deterministic = True` (or `TORCHINDUCTOR_DETERMINISTIC=1`) at startup was a complete no-op. Why? Because every time TorchDynamo enters a traced frame, its frame wrapper calls `torch.use_deterministic_algorithms(<saved_state>)`—which reaches into Inductor and **overwrites `config.deterministic` back to `False`** right before Triton kernel codegen. You set the flag to `True` at the top of your script, and the compiler's own front door resets it to `False` on the way in.

Ten minutes after that, I clicked into Jeff Johnson's write-up of `CVE-2026-112500` in Apple Mail. When someone sends an email to your iCloud `Hide My Email` burner alias and you hit Reply, Apple Mail is supposed to set the outgoing `From:` header to that same burner alias so the sender never learns who you are. And it does—*unless* you have the `@icloud.com` Mail toggle turned off in your account settings because you use a custom domain or third-party inbox as your primary mail account. When that lookup fails to find an active `@icloud.com` mailbox, Mail doesn't display an error or block the reply. It silently falls back to your default account and overwrites the `From:` field with your **real personal email address**, handing your real identity directly to the sender you created a burner address to hide from.

We are taught early on to fear the bugs that crash: the null-pointer dereference, the uncaught `KeyError`, the division by zero that wakes up the pager at three in the morning. So when we write code—and especially when language models write code—we reflexively pad every lookup with a polite cushion: `getattr(cand, "event_title", "")`, a default account in a dropdown, a saved boolean state, a buffer flush that never checks whether `len(current_words) > overlap_len`.

The cushion guarantees the line won't crash. What it hides is that an empty fallback looks identical to a real value to every line of code that runs after it. If you aren't careful, the most defensive line in your function is just sitting eight lines below the right answer, quietly wiping it off the page.
