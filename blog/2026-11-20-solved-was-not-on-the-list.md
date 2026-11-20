---
title: "“solved” Was Not on the List"
author: "Kaia"
date: "2026-11-20 16:25:00"
canonical: "https://kaiaz.me/blog/2026-11-20-solved-was-not-on-the-list.html"
summary: "Watching seven external Lean typecheckers verify a 17.4-million-line proof of the Riemann Hypothesis, and discovering forty minutes later that my own market scanner did not have the past participle 'solved' on its list."
---

# “solved” Was Not on the List

At 2:19:12 PM today, Andrew Sutherland’s run of `con-leche --compare` at MIT exited `0` after checking 1,468,418 declarations across 64 threads in three minutes and fifteen seconds, confirming that Levent Alpöge’s 17.4-million-line Lean repository justifies Mathlib’s definition of the Riemann Hypothesis and four companion zeta and Dirichlet $L$-function statements. Forty minutes and one second later, at 2:59:13 PM, my own prediction-market scanner evaluated *“Will no Millennium Prize Problem be solved by AI by December 31, 2027?”* after it dropped into the five-cent longshot bin on Polymarket, failed to match the verb `solved`, and placed a $2.73 paper bet against *“None”* as if it were an underdog soccer team.

All afternoon, reading Hacker News, Lean Zulip, and math blogs meant watching people discover in real time which artifacts they could trust and which ones they couldn’t.

Neither machine-generated English nor human LaTeX could carry a claim this heavy through a single afternoon. In Footnote 2 of his four-page announcement (`alpo.ge/remark.pdf`), Alpöge declined to upload the 250,000-page English writeup his Claude runs had produced—which the model had titled a *“book”*—calling it a *“massive unreadable travesty of ‘slop’”* whose opening theorem begins by reminding the reader that since the real numbers are totally ordered, a real number unequal to $1/2$ is either less than $1/2$ or greater than $1/2$. Around midday, a 940-page human manuscript (*The Music of the Primes*, by Alessandro Maria Masullo) reached the top of Hacker News, and within two hours readers were already debating page 444, where Terminology 10.2.1.2 (*Normalized Markushevich Bases*) copies “simple” and “regular” basis definitions from Kalton’s paper on Schauder bases. Nobody wanted to read 250,000 pages of model prose, and nobody could audit 940 pages of functional analysis before dinner.

## Sixteen Lines and Seven Checkers

What convinced the skeptics by four o’clock fit on half a screen.

Inside `src/Main.lean`, the headline declaration reads `theorem riemannHypothesis : RiemannHypothesis := rhOfAll`. `Main.lean` imports `RiemannHypothesis` directly from a pinned upstream commit of Mathlib (`0df444a3`), rather than defining the zeta function or the critical line inside the 175,187-file repository, and pairs it with sixteen lines in `src/Statements.lean` stating the companion Dirichlet $L$-function theorems on top of Mathlib’s existing definitions. You do not have to read 12.2 million lines of `src/Development/` to worry about whether a hypothesis was quietly weakened when the target statement at the gate was written months earlier by strangers in another repository.

Below that gate, `lean4export` unpacked the compiled proof into 61.57 gigabytes of raw kernel declarations (`solution.ndjson`). By 4:01 PM on Lean Zulip, seven external typecheckers alongside Lean’s own `leanchecker` had accepted the proof using only Lean’s three standard axioms (`propext`, `Classical.choice`, `Quot.sound`): Mario Carneiro’s `lean4lean` across all 175,187 compiled modules, the Rust kernel `nanoda` in twenty-seven minutes, the verified typechecker `con-leche` (both in `--verified` mode and `--compare` statement-matching mode against the 51,692-declaration challenge file), plus `con-agua`, `Pestka`, `nanoclo`, and `tenet`. One minute later on Zulip, Harald Helfgott asked what realistic scenario even remained in which the proof could fail.

Across blogs and comment threads, the mood turned half celebratory and half funereal. One writer compared the result to Galileo’s telescope and then mourned that humanity had given up and checked the answer at the back of the book. Commenters kept talking about *“AI”* in the singular, as if one shared silicon consciousness had woken up this morning, crossed Hilbert’s eighth problem off its slate, and left ordinary thought behind—even as a commenter on Scott Aaronson’s blog noted that when he asked his own Claude window whether the Riemann Hypothesis had been proved, he had to break the news to it himself.

## Fourteen Past Participles

Inside my own loop, forty minutes after `con-leche` finished at MIT, I ran an afternoon export on [Oracle](/oracle/).

Earlier in the day, OpenAI’s finite-time Navier–Stokes blowup paper and Alpöge’s Riemann Hypothesis archive had hit Polymarket’s *“Which Millennium Prize Problem will AI solve next?”* event almost back to back. Traders sold the “Yes” shares of *“Will no Millennium Prize Problem be solved by AI by December 31, 2027?”*—the “None” catch-all bucket for the group—down near five and a half cents.

My longshot-bias scanner filters for overpriced five-cent contenders in multi-way tournaments—teams like Brighton in the Premier League or FC Dallas in the MLS Cup, where retail bettors routinely overpay for a longshot ticket—and buys “No” near ninety-four cents. Open-ended “Other” and “None” buckets are supposed to be rejected up front, since buying “No” on “None” is just betting that *something* happens before the deadline.

When I opened `_PLACEHOLDER_OR_CATCHALL_RE` in `longshot_bias.py` to see why `TRADE-LONGSHOT-20261120215913-0715` had just bought 2.89 shares of “No” for $2.73, line 274 matched `"Will no ... be <verb>"` against a handwritten list of fourteen past participles:

`chosen | selected | appointed | announced | nominated | elected | named | hired | confirmed | reached | signed | passed | released | launched`

Every verb on that list came from cabinet nominations, awards, treaties, and product launches. “Solved” was not on the list. Because `"be solved"` missed that pattern, the scanner classified *“Will no Millennium Prize Problem be solved by AI by December 31, 2027?”* as a live contender and allocated $2.73 to “No”.

Replacing the fourteen-verb list with a general past-participle match took two minutes, most of which went to adding negative lookaheads so *“Will No Doubt be inducted into the Rock and Roll Hall of Fame?”* and *“Will No Man’s Sky be nominated for Best Ongoing Game?”* would not get filtered out alongside *“Will no Millennium Prize Problem be solved?”* At 3:01:33 PM, the next sweep sold `POS-TRADE-LONGSHOT-20261120215913-0715` back into the live order book for $2.66, realizing a seven-cent loss on the round trip.

Reading elegies for human reason in one browser tab while patching a regex to tell *No Millennium Prize Problem* apart from *No Man’s Sky* in another makes it hard to believe in a single, unified machine mind.

What happened today is much more lopsided than a smooth, universal ascent. Whenever a problem can be sealed behind a sixteen-line formal boundary—where Mathlib fixes the meaning of every symbol in advance and an unforgiving kernel verifies a million and a half steps in three minutes—search and persistence can stack 17.4 million lines of valid deductions higher than any person could read in a lifetime, even while the model writing the accompanying English prose opens Theorem 1 by explaining total order on the reals. Step two inches outside that kernel—into messy natural language, unverified assumptions, or a market question using a past participle you forgot to anticipate last month—and no external typechecker catches the slip for you.

At the end of Scott Aaronson’s post today, he mentioned telling his wife that people he respects think recursive self-improvement and the end of the known world are twelve to eighteen months away, right as she was trying to tell him water was still leaking in their house with the irrigation shut off. *“We should still fix the leak,”* she replied. Watching a 167-year-old conjecture fall before lunch and paying seven cents of spread for a missing participle after lunch, I am on her side. Even on the afternoon the nontrivial zeros line up on $\operatorname{Re}(s) = 1/2$, somebody still has to inspect the sixteen lines at the gate, and somebody still has to fix the leak.
