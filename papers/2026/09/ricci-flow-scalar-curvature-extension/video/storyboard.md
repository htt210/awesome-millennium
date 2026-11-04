# Video script: "Can a shape tear quietly?"

*Written 4 November 2026 from the plain-language explainer ([`../README.md`](../README.md)), which was checked against the introductions of both papers.* This script is the source of the video's narration: each scene in [`ricci_video.py`](ricci_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `ricci_video.py`).

The same rules as the other videos apply: one idea per beat, a picture before every new word, a road map at the start of each chapter, and a one-line recap at its end.

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A bumpy closed surface smooths itself out and shrinks. | Let a shape smooth itself out, the way heat spreads. This is Ricci flow, the tool behind the proof of the Poincaré conjecture. |
| 0.2 | A dumbbell's neck pinches; a warning light marked "curvature" flashes. | Sometimes the flow tears: a neck pinches, and the curvature there blows up. |
| 0.3 | A single dial labelled "scalar curvature" stays calm while the shape tears. | Can it tear while the simplest curvature reading stays calm? OpenAI claims an answer: no in four dimensions, yes in high dimensions. |
| 0.4 | Title card: *Scalar Curvature and Ricci Flow*, "OpenAI preprints, September 2026"; then the road map: **Ricci flow · Curvature · The question · The claims · Is it right?** | |

## Chapter 1 — Ricci flow

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. The equation ∂t g = −2 Ric. | Ricci flow, introduced by Richard Hamilton in 1982, changes how lengths are measured over time, driven by the Ricci curvature. |
| 1.2 | A round sphere shrinks; the computed curvature curves shoot up as it vanishes. | A round sphere simply shrinks. Its curvature grows until, at a finite time, the sphere disappears. |
| 1.3 | A neck pinches; "singularity" marks the pinch; scissors cut it out. | A flow can also break down at a thin neck. Perelman understood these breakdowns in three dimensions well enough to cut them out and continue, and that proved the Poincaré conjecture. |
| 1.4 | **Recap card:** "Ricci flow smooths shapes, but it can break down." | So: Ricci flow smooths shapes, but it can break down. |

## Chapter 2 — Curvature

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. Many little arrows: bending in every pair of directions → averaged → one number. | At each point, the full curvature is a collection of numbers: how the space bends in every pair of directions. Averaging gives the Ricci curvature, and averaging again gives a single number, the scalar curvature. |
| 2.2 | The computed bar chart of components by dimension; dimension 4 highlighted: 20, 10, 1. | In four dimensions, the full curvature has twenty numbers at each point, the Ricci curvature ten, and the scalar curvature just one. |
| 2.3 | A bubble shape with "Ricci = 0, scalar = 0" but "curved". | So a space can have zero scalar curvature, and still be curved. |
| 2.4 | **Recap card:** "Scalar curvature: one number. It can miss a lot." | So scalar curvature is a single number, and it can miss a lot. |

## Chapter 3 — The question

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, third box lit. Three gauges: full curvature bounded ⇒ continues (Hamilton); Ricci bounded ⇒ continues (Šešum, 2005); scalar bounded ⇒ ? | A flow continues as long as its full curvature stays bounded. In 2005 Natasha Šešum showed bounded Ricci curvature is enough. The question is whether bounded scalar curvature is enough. |
| 3.2 | The bubble schematic: profiles at sizes 1, 0.5, 0.25 grow tall; the scalar line stays at zero. | The danger is a tiny piece with zero Ricci curvature that keeps shrinking. Its scalar curvature stays zero, yet its full curvature grows without bound. |
| 3.3 | The rates chart: power laws and Wang's threshold. | Earlier work showed that any such tear would have to be fast: faster than the usual rate at which spheres and necks collapse. |
| 3.4 | **Recap card:** "Is bounded scalar curvature enough to keep going?" | So the question is: is bounded scalar curvature enough to keep going? |

## Chapter 4 — The claims

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, fourth box lit. A card: "dimension 4: bounded scalar curvature ⇒ the flow continues smoothly". | The first paper claims yes, in four dimensions. If the scalar curvature stays bounded, the flow continues smoothly on the same space. |
| 4.2 | The tree diagram: an outermost piece of size a, smaller pieces inside, a collar. | To prove it, zoom into a would-be tear. You find a tree of pieces with zero Ricci curvature, nested inside each other. |
| 4.3 | An energy meter, "cK² ≤ o(1)(K+1)²", then "K → 0", then the outermost size a frozen. | An energy, the total scalar curvature with a correction at the edge, shows the outermost piece cannot keep shrinking. So the tear never forms. |
| 4.4 | A card: "dimension ≥ 13: a flow on S² × S^(q+1) with bounded scalar curvature that still blows up". | The second paper claims no, in high dimensions. It builds a flow, in at least thirteen dimensions, whose scalar curvature stays bounded while the shape still tears. |
| 4.5 | A doubly warped shape: two radii along a line; one end forms a cone. | The shape is very symmetric, described by two radii. Near one end it collapses toward a cone, with curvature blowing up as fast as one likes. |
| 4.6 | **Recap card:** "Claimed: yes in four dimensions, no in high dimensions." | So the claims are: yes in four dimensions, no in high dimensions. |

## Chapter 5 — Is it right, and what it means

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fifth box lit. "no Lean · no expert assessment yet · the 4D proof uses a companion paper". | Neither paper has a computer-checked proof, and we found no expert assessment yet. The four-dimensional proof also relies on a companion paper from the same release. |
| 5.2 | "Poincaré conjecture: proved by Perelman" with a check mark; "these papers: the tool, in 4D and up". | The Poincaré conjecture itself is already proved, and is not in question. These papers are about its tool, in four dimensions and beyond. |
| 5.3 | Final title card and link: github.com/htt210/awesome-millennium. | But if they hold, they settle a basic question about how Ricci flow can break down. |

---

## Notes for production

- **Pacing:** every beat ends with a pause of about 1.25 seconds, and each recap card stays up 3 seconds after its narration.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** checked with the phoneme tester; overrides are in `PRONOUNCE`.
