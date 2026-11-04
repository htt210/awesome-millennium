# Video script: "The Unique Games Theorem"

*Written 4 November 2026 from the plain-language explainer ([`../README.md`](../README.md)), which was checked against the paper's introduction and its Lean scope.* This script is the source of the video's narration: each scene in [`ugc_video.py`](ugc_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `ugc_video.py`).

The same rules as the other videos apply: one idea per beat, a picture before every new word, a road map at the start of each chapter, and a one-line recap at its end.

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A network of nodes; the nodes split into two coloured teams, and the links between teams light up. | Split a network into two teams, cutting as many links as you can. Finding the very best split is hopelessly slow for big networks. |
| 0.2 | A gauge fills to 87.9%: "a fast algorithm guarantees this much". | But a clever fast algorithm, found in 1995, always gets at least eighty-eight percent of the best. For thirty years, nobody could do better, and nobody could prove it was impossible. |
| 0.3 | Title card: *The Unique Games Theorem*, with "OpenAI preprint, September 2026" underneath. | In 2026, OpenAI claimed to prove a conjecture that would settle this, and dozens of similar questions, at once. |
| 0.4 | The road map appears: **Hard problems · Unique games · The claim · How it works · Is it right?** | |

## Chapter 1 — Hard problems

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. Two boxes: "easy to check" and "easy to solve?" with P and NP. | Some problems are easy to check but seem hard to solve. Whether every problem that is easy to check is also easy to solve is the P versus NP question, a Millennium Prize problem. |
| 1.2 | Switches and rules, as in a 3SAT puzzle; the label "3SAT: NP-hard". | Among the hardest of these is 3SAT: deciding whether a list of rules about on-off switches can all be satisfied. Most experts believe no fast algorithm exists. |
| 1.3 | Two problems drawn: Max-Cut (a network split in two) and Vertex Cover (a few nodes covering every link). | When exact answers are out of reach, we settle for good-enough ones. Max-Cut asks to cut as many links as possible. Vertex Cover asks for as few nodes as possible touching every link. |
| 1.4 | The Goemans–Williamson curve dips to its minimum, 0.878. | For Max-Cut, the 1995 algorithm of Goemans and Williamson places the nodes on a sphere and cuts with a random plane. Its guarantee is the lowest point of this curve: about eighty-seven point nine percent. |
| 1.5 | A histogram of cover sizes: never above twice the best. | For Vertex Cover, a two-line algorithm is never worse than twice the best. We tried it on four hundred small random networks: it never went past two. |
| 1.6 | **Recap card:** "Hard problems; good-enough answers; thresholds nobody could beat or explain." | So: hard problems, good-enough answers, and thresholds nobody could beat or explain. |

## Chapter 2 — Unique games

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. A small network; each node gets a number from 0 to 3. | A unique game is a puzzle on a network. Each node gets a label, say a number from zero to three. |
| 2.2 | Each link shows "+c": the label at one end, plus c modulo 4, should equal the other. | Each link carries a rule: the label at one end, plus some number, wrapping around after three, must equal the label at the other end. |
| 2.3 | One end is fixed; the rule forces exactly one label at the other end. | The rule is unique: once you choose one end, it forces exactly one label at the other. |
| 2.4 | The best labeling: 7 of 9 links green, 2 red. "value = 7/9". | The value of the game is the largest fraction of rules a single labeling can satisfy. For this one, found by trying all four thousand labelings, it is seven out of nine. |
| 2.5 | Propagation: one choice spreads around a fully satisfiable game. | If every rule can be satisfied, it is easy: choose one label and let the rules spread. The question is what happens when only almost all of them can be. |
| 2.6 | **Recap card:** "A unique game: labels, and rules that force one answer." | So a unique game is labels on a network, and rules that each force one answer. |

## Chapter 3 — The conjecture

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, second box still lit. A number line from 0 to 1 with zones near 1 − ε and near δ. | In 2002, Subhash Khot conjectured that telling apart games that are almost fully satisfiable from games that are almost completely unsatisfiable is as hard as 3SAT. |
| 3.2 | Arrows from the conjecture to "Max-Cut: 87.9% is optimal" and "Vertex Cover: 2 is optimal". | Researchers then discovered how much it would explain. It would make the eighty-seven point nine percent optimal for Max-Cut, and the factor two optimal for Vertex Cover. |
| 3.3 | A third arrow: "every constraint satisfaction problem: one family of algorithms is best". | And it would make one family of algorithms the best possible for a whole universe of similar problems. |
| 3.4 | A timeline: 2018, Khot, Minzer and Safra: "the 2-to-2 theorem: half satisfiable". | Progress was slow. In 2018, Khot, Minzer and Safra proved a closely related theorem. But it only handled games about half satisfiable, not almost fully satisfiable. |
| 3.5 | **Recap card:** "Khot's conjecture would explain the thresholds. It stayed open." | So Khot's conjecture would explain the thresholds, and for twenty-four years it stayed open. |

## Chapter 4 — The claim

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, third box lit. A 3SAT puzzle flows through a box "fast translation" into a unique game. | Here is the claim. There is a fast way to translate any 3SAT puzzle into a unique game. |
| 4.2 | Two outcomes: "solvable puzzle → almost all rules satisfiable" (green), "unsolvable → almost none" (red). | If the puzzle can be solved, almost all of the game's rules can be satisfied. If it cannot, almost none can. |
| 4.3 | "telling them apart fast would solve 3SAT, so P = NP". | So a fast way to tell the two cases apart would solve 3SAT. That is exactly Khot's conjecture. |
| 4.4 | **Recap card:** "Claimed: Khot's Unique Games Conjecture is true." | So the claim is that Khot's Unique Games Conjecture is true. |

## Chapter 5 — How it works

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fourth box lit. A card: "start: Håstad's equations modulo 2". | The proof starts from a known hard problem: Håstad's systems of equations modulo two, where telling almost-satisfiable from half-satisfiable is already known to be hard. |
| 5.2 | Each answer becomes a table indexed by grids of zeros and ones; a test nudges the grid and compares. | Each answer is written out as a large table, indexed by grids of zeros and ones. A test nudges the grid slightly and checks whether the table's answer changed. |
| 5.3 | A gauge: an honest table passes only about half the time; "the one-half obstacle". | The trouble: with the natural encoding, even an honest answer passes only about half the time. That is why the 2018 theorem stopped at one half. |
| 5.4 | A nonlinear map hides the nudge: the honest pass rate climbs close to 100%. | The new idea is a nonlinear disguise. The answers are encoded through a special map that barely notices the nudge, so honest answers pass almost always. |
| 5.5 | A cheater using simple linear information gets caught: "detected at least 1 time in 8". | Yet any table that cheats with simple linear information notices the nudge often, and gets caught. |
| 5.6 | An arrow back from "a good labeling" to "a good answer to Håstad's equations", labelled "expansion theorem (2018)". | Finally, if any labeling satisfies even a small fraction of the rules, the proof decodes it into a good answer for the original equations, using the 2018 expansion theorem. |
| 5.7 | **Recap card:** "A nonlinear disguise beats the one-half obstacle; expansion does the rest." | So: a nonlinear disguise beats the one-half obstacle, and the expansion theorem does the rest. |

## Chapter 6 — Is it right, and what it means

| # | On screen | Narration |
|---|---|---|
| 6.1 | Road map, fifth box lit. A Lean card: "the main reduction and four direct hardness results, formalized". | OpenAI published computer-checked versions in Lean of the main reduction, and of direct proofs for Max-Cut, Vertex Cover, and two other problems. We have not re-run them. |
| 6.2 | A card: "experts reported studying it: Moshkovitz, Khot, Håstad, Minzer". | According to press and blog reports, experts including Dana Moshkovitz, Subhash Khot himself, Johan Håstad and Dor Minzer were studying the proof in October, without a settled verdict yet. |
| 6.3 | Thresholds lock into place: 87.9% for Max-Cut, 2 for Vertex Cover, "unless P = NP". | If it holds, the old thresholds become final: no fast algorithm can beat them, unless P equals NP. |
| 6.4 | A large "P vs NP?" stays open. | It does not decide P versus NP. Every consequence carries that same condition. |
| 6.5 | Final title card and link: github.com/htt210/awesome-millennium. | But it would turn decades of educated guesses about good-enough answers into theorems. |

---

## Notes for production

- **Pacing:** every beat ends with a pause of about 1.25 seconds, and each recap card stays up 3 seconds after its narration.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** checked with the phoneme tester; overrides are in `PRONOUNCE`.
