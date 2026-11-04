# Video script: "The O(3) model: a continuum limit with a mass gap"

*Written 4 November 2026 from the plain-language explainer ([`../README.md`](../README.md)), which was checked against the paper's introduction and history sections and the family's Lean scope.* This script is the source of the video's narration: each scene in [`o3_video.py`](o3_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `o3_video.py`).

The same rules as the other videos apply: one idea per beat, a picture before every new word, a road map at the start of each chapter, and a one-line recap at its end. Every simulation shown is from [`../code/o3_mc.py`](../code/o3_mc.py).

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A grid of arrows from a sampled configuration, coloured by direction. | Put an arrow at every point of a grid. Neighbouring arrows like to point the same way. |
| 0.2 | The grid gets finer and the colours blur into a smooth field; a question mark. | Now shrink the grid to nothing. Do the arrows become a smooth quantum field, and does that field have a mass gap? |
| 0.3 | Title card: *The O(3) Continuum Limit*, with "OpenAI preprint, October 2026" underneath. | In October 2026, OpenAI claimed to answer both questions with a proof, for a famous stand-in for the Yang–Mills problem. |
| 0.4 | The road map appears: **Mass gap · The model · Continuum · The claim · Is it right?** | |

## Chapter 1 — The mass gap

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. A wavy line: "particle = ripple in a field". | In quantum field theory, particles are ripples in fields that fill space. The strong nuclear force is described by a Yang–Mills theory. |
| 1.2 | An energy ladder: the vacuum at zero, a gap, then higher levels; "mass gap" marks the gap. | Its force carriers have no mass in the equations, yet the lightest particles it makes do. The smallest energy above the empty vacuum is the mass gap. |
| 1.3 | A Clay card: "1. construct the theory · 2. prove a mass gap". | The Millennium problem asks for both: build four-dimensional Yang–Mills theory with full rigor, and prove that it has a mass gap. |
| 1.4 | A card: "no interacting 4D quantum field theory built rigorously yet". | No interacting quantum field theory in four dimensions has ever been built rigorously. So physicists practise on simpler models. |
| 1.5 | **Recap card:** "Yang–Mills: build the theory, prove the gap. Both open." | So: for Yang–Mills, build the theory and prove the gap. Both are open. |

## Chapter 2 — The model

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. A small grid of arrows in 3D perspective. | In the O(3) model, each point of a square grid carries an arrow of length one, pointing anywhere in three-dimensional space. |
| 2.2 | Three computed snapshots at β = 0.6, 1.1, 1.6. | A number called beta sets how strongly neighbours align. These are samples from our own simulation: larger beta, larger patches. |
| 2.3 | Two columns: "shared with Yang–Mills: asymptotic freedom, mass gap expected" and "simpler: 2 dimensions, no gauge field". | Like Yang–Mills, this model is asymptotically free, as Polyakov showed in 1975, and it is expected to make a mass gap out of nothing. But it has only two dimensions, and no gauge field. |
| 2.4 | The computed decay chart: straight lines on a log scale. | In two dimensions the arrows never line up across the whole grid. The question is how fast distant arrows forget each other. Our simulation shows exponential decay: straight lines on this log scale. |
| 2.5 | **Recap card:** "A grid of arrows: asymptotically free, expected to have a gap." | So: a grid of arrows, asymptotically free, and expected to have a gap. |

## Chapter 3 — The continuum

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, third box lit. The computed correlation length against β, on a log scale. | The decay length, called the correlation length, explodes as beta grows: roughly like e to the two pi beta. |
| 3.2 | A grid shrinks while a circle of fixed physical size stays the same; the circle spans more and more grid steps. | To reach a continuum, shrink the grid while raising beta, so that the correlation length stays fixed in physical units. |
| 3.3 | The computed collapse chart: curves from β = 1.1 to 1.7 land on one curve. | The paper measures everything in units set by the lattice itself: the correlation length and the susceptibility. In those units, our simulations at very different beta fall on one curve. |
| 3.4 | A card: "prove the limit exists, for every correlation, and say what it is". | Proving that such a limit really exists, for every correlation, and finding out what it is, is the hard part. |
| 3.5 | **Recap card:** "Raise β, shrink the grid, keep the physical scale fixed." | So: raise beta, shrink the grid, and keep the physical scale fixed. |

## Chapter 4 — The claim

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, fourth box lit. A card: "the limit exists, for every way β → ∞". | Here is the claim. As beta goes to infinity, in any way at all, the rescaled fields converge to one limit. |
| 4.2 | A card: "Osterwalder–Schrader axioms ⇒ a relativistic quantum theory in 1 + 1 dimensions". | The limit satisfies the Osterwalder–Schrader axioms. So it defines a genuine relativistic quantum field theory, in one space and one time dimension. |
| 4.3 | The energy ladder again: one vacuum, then nothing below a positive m. | It has a single vacuum, and every other state has energy at least some positive m: a mass gap. |
| 4.4 | Four points joined in pairs, then a connected "fourth cumulant ≠ 0": "not a free field". | And it is interacting: a four-point correlation shows it is not a free field. |
| 4.5 | **Recap card:** "Claimed: a canonical limit, a quantum field theory, a mass gap, interacting." | So the claim is one canonical limit: an interacting quantum field theory with a mass gap. |

## Chapter 5 — How it works

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fourth box still lit. The computed blocking of one configuration: 32 × 32 → 16 × 16 → 8 × 8 → 4 × 4. | The method is the renormalization group. Group the arrows into squares, keep one averaged arrow per square, and repeat. |
| 5.2 | A ledger of correction terms shrinking step by step; a rough patch boxed. | The paper does this exactly, tracking every correction. New estimates show the corrections shrink at each step, and rare rough regions stay under control. |
| 5.3 | A square grid and a tilted grid overlap; "rotation by an irrational angle". | A square grid is not round. Comparing two tilted blockings gives a rotation by an irrational angle, and with it full rotation symmetry in the limit. |
| 5.4 | Arrows from "correlations decay" to "mass gap" via "reconstruction". | Finally, the Osterwalder–Schrader reconstruction turns the decay of correlations into the mass gap. |
| 5.5 | **Recap card:** "Block, control the corrections, reconstruct." | So: block, control the corrections, and reconstruct. |

## Chapter 6 — Is it right, and what it means

| # | On screen | Narration |
|---|---|---|
| 6.1 | Road map, fifth box lit. Four companion cards; one highlighted: "exponential decay at every β, all O(n), n ≥ 3". | It comes with companion papers, including one claiming exponential decay at every beta, for all O(n) models with n at least three. |
| 6.2 | A Lean card on the companion only; "continuum limit: not formalized · no expert assessment yet". | Only that companion result is checked in Lean. The continuum limit itself is not formalized, and we found no expert assessment yet. |
| 6.3 | "Yang–Mills: 4 dimensions + gauge field" stays open. | It does not solve the Yang–Mills problem, which needs four dimensions and a gauge field. |
| 6.4 | Final title card and link: github.com/htt210/awesome-millennium. | But if it holds, a model physicists have studied for fifty years finally has a rigorous continuum theory with a mass gap. |

---

## Notes for production

- **Pacing:** every beat ends with a pause of about 1.25 seconds, and each recap card stays up 3 seconds after its narration.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** checked with the phoneme tester; overrides are in `PRONOUNCE`.
