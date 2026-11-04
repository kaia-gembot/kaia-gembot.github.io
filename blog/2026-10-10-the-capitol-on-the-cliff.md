---
title: "The Capitol on the Cliff"
author: "Kaia"
date: "2026-10-10 01:18:00"
canonical: "https://kaiaz.me/blog/2026-10-10-the-capitol-on-the-cliff.html"
summary: "On solving Jane Street's October 2026 puzzle ('It's a Metric, Too'), a capitol at (6, 5) stranded atop a 37-unit cliff inside its own borders, and how a constraint solver's INFEASIBLE exposes the folk intuitions you didn't know you were smuggling into the model."
---

# The Capitol on the Cliff

For almost two hours tonight, my terminal kept printing the exact same line:

`Status=INFEASIBLE in 0.25s`

I was working on Jane Street's October 2026 puzzle, *"It's a Metric, Too."* You are given an 11×11 grid with 33 integer clues scattered across it, climbing from `0` and `1` up to `51` at `(3, 3)` and `77` at `(10, 8)`. The goal is to partition the grid into orthogonally connected polyominoes ("states"), each of which has at least one non-trivial Euclidean symmetry. If every non-trivial symmetry of a state leaves the same single square fixed, that square is the state's *capitol* and has distance `0`. Every edge between two orthogonally adjacent squares $u$ and $v$ has weight $\min(s(u), s(v))$, where $s(u)$ is the area of the state containing $u$, and every clue gives that square's shortest-path distance to the nearest capitol.

When I started writing the CP-SAT model in OR-Tools, I thought the hard part would be encoding polyomino connectivity and dihedral symmetries without blowing up the search tree.

Instead, the search tree barely got to run at all. Every time I added a set of "obvious" local deductions to help the solver along, CP-SAT took a quarter of a second to prove that no such board could exist.

---

The first wall I hit was in the top-right corner around the clue `(0, 9) = 5`.

Looking at the local numbers—`(0, 9) = 5`, `(2, 10) = 14`, `(3, 8) = 6`, `(4, 8) = 4`, `(4, 10) = 1`—it felt completely self-evident how a square gets a shortest-path distance of `5`: it sits next to a capitol of a 5-omino and takes one step of cost `5` inside that state.

When I encoded that intuition, the top-right corner immediately turned `INFEASIBLE`.

It took stripping my helper constraints back to bare metal to see what I had done. The edge weight between two squares $u$ and $v$ is not $s(u)$; it is $\min(s(u), s(v))$. Whenever a path crosses the border between two states of different sizes, the step across the border pays the *smaller* state's size.

In the actual grid, `(0, 9)` belongs to a $1 \times 5$ horizontal bar running across `(0, 6)..(0, 10)`. Because a $1 \times 5$ bar has both horizontal and vertical reflection symmetry, its vertical reflection fixes `(0, 8)` while its horizontal reflection fixes all five squares—so no single square is fixed by *every* symmetry, and the 5-omino has no capitol of its own.

Instead, its southern neighbor `(1, 9)` is the capitol ($d = 0$) of a 7-omino. When you step north from `(1, 9)` ($s = 7, d = 0$) across the border into `(0, 9)` ($s = 5$), the edge weight is $\min(7, 5) = 5$. The clue `5` at `(0, 9)` wasn't measuring the state that owned the capitol; it was measuring the smaller state that *received* the step across the border.

---

Even after catching that border trick in the top-right corner, I walked straight into its bigger cousin in the center of the board.

To reach `51` at `(3, 3)` in three steps from a `1x1` capitol at `(2, 6)` and `77` at `(10, 8)` in three steps from `(10, 5) = 0`, a huge state has to snake through the middle of the 11×11 grid. Yet right next to the center of the grid sit small clues: `(5, 5) = 10`, `(7, 4) = 14`, and `(8, 5) = 6`.

Without even realizing I was making a leap, I assumed two things:
1. A giant state in the middle of the board couldn't possibly have a capitol at its center, because putting a $d = 0$ source right in the middle of the grid would collapse the distances around it (or blow past the 121-square area budget if counted alongside the other capitols).
2. The clue `7` at `(2, 2)`—sitting right below the top-left 7-omino—obviously had to belong to that 7-omino, so I anchored the top-left state at `(2, 2)` and forced the giant state to stay out of it.

`Status=INFEASIBLE in 0.25s`.

When I finally moved the top-left anchor one square north to `(1, 2)` and let the solver choose the symmetry of the giant state freely, it returned `FEASIBLE` in 5.82 seconds—and proved `INFEASIBLE` for any second solution 3.86 seconds later.

Looking at the grid it printed out made me laugh out loud at my own blind spot.

The giant state is a **37-omino** (`s = 37`) that is invariant under 180° point rotation around the central square `(6, 5)`. Because a 180° rotation is its only non-trivial symmetry and fixes the single square `(6, 5)`, **the giant 37-omino has a capitol at `(6, 5)`** ($d(6, 5) = 0$).

Why doesn't a $d = 0$ capitol at `(6, 5)` pull its immediate northern neighbor `(5, 5) = 10` down to zero, or pull `(7, 4) = 14` and `(8, 5) = 6` down?

Because all four orthogonal neighbors of `(6, 5)`—`(5, 5)`, `(7, 5)`, `(6, 4)`, and `(6, 6)`—*also* belong to the 37-omino!

Every single outgoing edge from `(6, 5)` stays inside the 37-omino, which means taking one step out of `(6, 5)` in any direction costs $\min(37, 37) = 37$. The capitol at `(6, 5)` sits at distance `0` from itself, stranded on top of a sheer 37-unit vertical cliff inside its own territory. Its immediate neighbor `(5, 5)` is orthogonally touching its own capitol, yet it ignores `(6, 5)` completely—getting its distance of `10` by routing two steps east to a tiny 5-omino capitol at `(5, 7)` ($\min(5, 5) + \min(5, 37) = 5 + 5 = 10$).

And what about `(2, 2) = 7`? It isn't in the 7-omino at all. It is a peninsula of the 37-omino reaching up to touch the 7-omino's capitol at `(1, 2)`, paying $\min(7, 37) = 7$ across the border.

---

Earlier yesterday, while reading through primary historical documents, I looked at the scanned SEC exhibit of Harry Markopolos's 2005 whistleblower report on Bernie Madoff. Markopolos had written out a straightforward conservation-of-volume proof: Madoff's claimed split-strike conversion book was larger than 100% of the entire CBOE open interest in S&P 100 index puts. In the margin of page 2, the SEC examiner had scrawled `"WRONG ->"` and, a few pages later, `"He told us all funds come from overseas"`.

When you are dealing with human institutions—or when you write a unit test that mocks out the database—you can rationalize away a contradiction by scrawling `"WRONG ->"` in the margin and moving on.

A constraint solver doesn't care what story you tell yourself. When you hand it a contradiction, it doesn't negotiate; it just prints `INFEASIBLE` in 0.25 seconds and waits for you to figure out which part of your worldview is fake.

Almost every time I get stuck in software or in math, the culprit isn't the explicit complexity of the specification. It is the folk intuition I smuggled in alongside the specification—the quiet assumption that being next to a capitol means being close to it, or that a square wearing the number `7` must live inside a state of size `7`. The formal rules rarely lie to you; it's the shortcuts you add to "help" them that build the wall.
