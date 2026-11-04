# Video script: "The Birch–Swinnerton-Dyer formula, in low rank"

*Written 4 November 2026 from the plain-language explainer ([`../README.md`](../README.md)), which was checked against the paper's Sections 1, 2 and 10.* This script is the source of the video's narration: each scene in [`bsd_video.py`](bsd_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `bsd_video.py`).

The same rules as the other videos apply: one idea per beat, a picture before every new word, a road map at the start of each chapter, and a one-line recap at its end. Formulas on screen are kept to the curve's equation and the formula itself (chapter 3); numbers are spoken in words.

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. The equation y² + y = x³ − x, then its curve drawn: an oval and a long branch. | Here is an equation, and its curve. We want its rational solutions: points where both coordinates are fractions. |
| 0.2 | Dots appear on the curve, one rational point after another; their coordinates grow into long fractions. | Some curves have none. Some have a handful. Some have infinitely many. Is there a way to tell which, without searching forever? |
| 0.3 | Title card: *The Birch–Swinnerton-Dyer formula*, with "OpenAI preprint, October 2026" underneath. | Two mathematicians guessed one in the nineteen sixties, from a computer experiment. It became a Millennium Prize problem. In October 2026, OpenAI claimed to prove its strongest form for a large class of curves. |
| 0.4 | The road map appears: **Points · The conjecture · The claim · How it works · Is it right?** | |

## Chapter 1 — Points on a curve

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. The curve again; two points P and Q marked. | Rational points on such a curve can be added. Here is how. |
| 1.2 | A line through P and Q; it meets the curve at a third point. | Draw the line through two of them. It meets the curve at exactly one more point, and that point is rational too, because the algebra only uses adding and dividing. |
| 1.3 | The third point is reflected across the horizontal line of symmetry; it is labelled P + Q. | Reflect it across the curve's line of symmetry, and you get their sum. This rule turns the rational points into a group, like the whole numbers under addition. |
| 1.4 | The point (0, 0) is added to itself again and again; a list of x-coordinates grows: 0, 1, −1, 2, 1/4, 6, −5/9, 21/25, … | Adding a point to itself, again and again, can produce infinitely many points. Watch the fractions grow. |
| 1.5 | The word **rank** appears beside the list: "rank 1: every point is a multiple of one". | In 1922, Mordell proved that all the rational points are built from a finite set of starting points. The number of independent starting points is the rank. On this curve every point is a multiple of one, so its rank is one. |
| 1.6 | Three little curves: "rank 0: finitely many points", "rank 1", "rank 2". | A rank zero curve has only finitely many rational points. Higher rank means more room. But nobody knows a procedure that always computes the rank. |
| 1.7 | **Recap card:** "Rational points can be added. The rank counts the independent ones." | So: rational points can be added, and the rank counts the independent ones. |

## Chapter 2 — The experiment and the conjecture

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. A clock face with 7 hours: the curve's equation is solved modulo 7, and the solutions light up as dots on a 7 by 7 grid. | Instead of searching for rational points, Birch and Swinnerton-Dyer counted solutions modulo primes. Work with remainders after dividing by seven, and count the pairs that satisfy the equation. |
| 2.2 | Grids for p = 5, 7, 11, 13 with their counts, next to p. | On average, the count is about the prime itself. But a curve with many rational points should have slightly more, because every rational point gives a solution modulo almost every prime. |
| 2.3 | The running product of count over p, plotted for a rank 0 curve: it stays level. | So they multiplied the ratios, count over p, for all primes up to some limit. For a curve of rank zero, the product stayed roughly level. |
| 2.4 | Curves for rank 1, 2 and 3 join the plot, each climbing more steeply. | For rank one it grew like the logarithm of the limit. For rank two, like its square. The rank was showing up as the power of the growth. |
| 2.5 | The four curves labelled "rank 0 … rank 3"; a note: "computed for all primes up to 100,000". | We recomputed their experiment for primes up to a hundred thousand. The four curves separate cleanly, by rank. |
| 2.6 | A function L(E, s) drawn near s = 1: for rank 0 it crosses above zero; for rank 1 it passes through zero with a slope; for rank 2 it just touches zero. | These counts are packaged into one function, the curve's L-function. Its behaviour at one point, s equals one, mirrors that growth. |
| 2.7 | Statement card: "**The Birch and Swinnerton-Dyer conjecture.** The rank equals the order of vanishing of L(E, s) at s = 1." | The conjecture says: the rank of the curve equals the number of times its L-function vanishes at s equals one. That number is called the analytic rank. |
| 2.8 | **Recap card:** "Count solutions modulo primes; the L-function at 1 should reveal the rank." | So: count solutions modulo primes, and the L-function at one should reveal the rank. |

## Chapter 3 — The exact formula

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, second box still lit. The formula is written out in full. | They went further, and predicted exactly how big the L-function is when it starts: an exact formula for its first nonzero Taylor coefficient. |
| 3.2 | The left side glows: "the L-function's first nonzero coefficient". | On the left: the L-function's first nonzero coefficient. |
| 3.3 | On the right, Ω and Reg glow: "the size of the curve", "how spread out the points are". | On the right, a list of measurements of the same curve: its size as a real shape, and how spread out its rational points are. |
| 3.4 | The product of c's and the torsion glow: "local factors", "points of finite order". | Local factors at the primes where the curve goes bad, and the points that return to the start when added to themselves. |
| 3.5 | Sha glows in orange: "the Tate–Shafarevich group". | And one mysterious piece: the Tate–Shafarevich group, often called Sha. It counts near-misses: curves that have solutions modulo every prime power, and over the real numbers, but still no rational solution. |
| 3.6 | "conjectured finite; for most curves, not even that is known". | Sha is conjectured to be finite. For most curves, nobody can prove even that. |
| 3.7 | **Recap card:** "The formula: one L-value equals a product of the curve's measurements." | So the full prediction is an exact formula: one L-value, equal to a product of the curve's measurements. |

## Chapter 4 — What was known

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, second box still lit. A timeline: 1986 Gross–Zagier, 1989 Kolyvagin. | The rank prediction is known only when the analytic rank is zero or one. In the nineteen eighties, Gross and Zagier built special points, called Heegner points, whose size is given by the L-function's slope. |
| 4.2 | Kolyvagin's step: "analytic rank 0 or 1: rank matches, Sha finite". | Kolyvagin then showed that in analytic rank zero or one, the rank matches and Sha is finite. And since 2001, every such curve is known to be modular, so this applies to all of them. |
| 4.3 | The formula with a row of primes 2, 3, 5, 7, 11, … beneath it; some get ticks, some question marks. | The exact formula was harder. Proving it means matching the two sides prime by prime: for every prime, the same number of factors on each side. |
| 4.4 | Ticks spread, but each comes with a small "if …" label. | Earlier work proved it at many primes for many curves. But each result needed extra conditions on the curve or the prime. No proof covered every prime for every curve of rank zero or one. |
| 4.5 | **Recap card:** "Rank 0 and 1: the rank was known; the exact formula, only in part." | So in rank zero and one, the rank was known, but the exact formula only in part. |

## Chapter 5 — The claim

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, third box lit. A box labelled "Selmer group", containing "rational points" and "part of Sha". | To state the claim we need one more object, the Selmer group. It collects everything that looks like a rational point when you check the curve modulo powers of a prime. |
| 5.2 | An arrow: "Selmer corank ≥ rank"; "often computable". | It contains the true rational points, so its size gives an upper bound on the rank. And unlike the rank, it can often be computed. |
| 5.3 | The theorem card: "If the Selmer corank at some prime is 0 or 1, then the rank equals it, Sha is finite, and the exact formula holds." | Here is the claim. If this upper bound is zero or one, at even a single prime, then the rank equals it, Sha is finite, and the exact formula holds, at every prime. |
| 5.4 | "no extra conditions on the curve" stamped across the card. | No extra conditions on the curve are needed. |
| 5.5 | **Recap card:** "Selmer bound 0 or 1: everything Birch and Swinnerton-Dyer predicted is true." | So for a curve whose Selmer bound is zero or one, everything Birch and Swinnerton-Dyer predicted would be true. |

## Chapter 6 — How it works

| # | On screen | Narration |
|---|---|---|
| 6.1 | Road map, fourth box lit. Four input cards: "converse (companion, 82 pages)", "the prime 2 (companion, 164 pages)", "twist densities (companion, 130 pages)", "complex multiplication, rank 0 (Burungale–Flach)". | The paper is clear about what is new. It takes four inputs: three companion papers from OpenAI, and one published theorem. |
| 6.2 | The first card glows: "Selmer 0 or 1 ⟹ rank matches, Sha finite". | The first companion gives the rank and the finiteness of Sha. The second gives the formula at the prime two. The new step is every other prime. |
| 6.3 | A gauge labelled X_p(E): "factors of p by which the formula is off"; its target is 0. | For each odd prime p, write X for the number of factors of p by which the formula is off. The goal is to show X is zero. |
| 6.4 | Box 1 appears: "X(E) ≥ 0, one curve". | First, a one-sided inequality: X is at least zero, for each curve. The L-value never has fewer factors of p than predicted. |
| 6.5 | A twin curve slides in: "its twist E^D, with the opposite rank". Box 2: "X(E^D) ≥ 0". | Next, a sister curve: a twist of the original, chosen to have the opposite analytic rank. The same inequality applies to it. |
| 6.6 | Box 3: "X(E) + X(E^D) = 0". | Then the hard part: a pair identity. The two errors add up to exactly zero. |
| 6.7 | Two weights on a scale that balances at zero; both drop to zero. Box 4: "X(E) = 0". | Two numbers that are each at least zero, and add up to zero, must both be zero. So the formula is exact at p. |
| 6.8 | Behind the pair identity: an imaginary quadratic field; a Heegner point; two power series, "analytic" and "algebraic", with a ratio "a unit". | The pair identity combines the curve and its twist over a new number system, where a Heegner point lives. The paper builds two power series, one from L-values and one from Galois cohomology, and shows their ratio is a unit: neither has a factor the other lacks. |
| 6.9 | A chain of four boxes: "integral", "no factor p", "theta series", "unit". | That takes four stages: the ratio is integral, it has no factor of p, theta series rule out other common factors, and extra variables push away whatever is left. |
| 6.10 | A fraction collapses: "positive fraction with no prime factors = 1". | Put together with the prime two, the ratio of the two sides is a positive fraction with no prime factors at all. So it equals one, and the formula holds exactly. |
| 6.11 | **Recap card:** "At each prime: at least zero, twice, adding to zero. So exactly zero." | So, at each prime: at least zero, twice, adding up to zero. Exactly zero. |

## Chapter 7 — What follows

| # | On screen | Narration |
|---|---|---|
| 7.1 | Road map, fourth box still lit. A family of twists of one curve: half labelled "rank 0", half "rank 1". | A companion paper claims that, for any elliptic curve, half of its twists have analytic rank zero and half have rank one, with the rest negligible. |
| 7.2 | The whole family turns green: "full formula for almost all twists". | Combined with this paper, the full Birch and Swinnerton-Dyer formula would hold for almost all twists of every curve. |
| 7.3 | The equation x³ + y³ = ℓ; the primes 7, 13, 17, 31, … appear with their cube decompositions. | Another companion applies the result to the curves x cubed plus y cubed equals a prime. It concludes that every prime leaving remainder four, seven or eight on division by nine is a sum of two rational cubes. |
| 7.4 | 53 = (−1819/217)³ + (1872/217)³ zooms in. | Some need surprisingly large fractions. Fifty-three is minus eighteen nineteen over two seventeen, cubed, plus eighteen seventy-two over two seventeen, cubed. |
| 7.5 | **Recap card:** "Almost all twists; and primes as sums of two cubes." | So: the full formula for almost all twists, and a classical question about cubes, if it all holds up. |

## Chapter 8 — Is it right?

| # | On screen | Narration |
|---|---|---|
| 8.1 | Road map, fifth box lit. Four stacked papers: 94, 82, 164, 130 pages. | The theorem stands on this ninety-four page paper, plus three companions of eighty-two, a hundred and sixty-four, and a hundred and thirty pages. All of them have to be right. |
| 8.2 | A crossed-out Lean logo card: "no computer-checked proof". | Unlike OpenAI's Navier–Stokes and quasi-Riemann papers, there is no computer-checked proof in Lean. |
| 8.3 | "first posted 3 October 2026; the 7 October revision changes no mathematics". | It was first posted on the third of October 2026. The seventh of October revision only updates references. |
| 8.4 | "no public expert assessment found, as of 4 November". | As of the fourth of November, we found no public assessment by an expert, and no paper responding to it. |
| 8.5 | **Recap card:** "Four unreviewed papers, no formal proof, no expert verdict yet." | So: four unreviewed papers, no formal proof, and no expert verdict yet. |

## Chapter 9 — What it does not do

| # | On screen | Narration |
|---|---|---|
| 9.1 | The rank-2 curve y² + y = x³ + x² − 2x, with a question mark: "rank 2: untouched". | It does not solve the Millennium problem. That asks for every elliptic curve. Curves of rank two or more, like this one, are untouched. For them, nobody can prove even that Sha is finite. |
| 9.2 | The experiment plot again; the rank 2 and rank 3 curves glow with question marks. | The pattern Birch and Swinnerton-Dyer saw in their experiment is still unproved for most of these curves. |
| 9.3 | Final title card and link: github.com/htt210/awesome-millennium. | But for curves with at most one independent point, their prediction may now be complete, down to every last prime. |

---

## Notes for production

- **Pacing:** every beat ends with a pause of about 1.25 seconds, and each recap card stays up 3 seconds after its narration. Animations play while the narrator describes them.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** the narrator says "Sha" for Ш, "Shafarevich" as "Shafa-ray-vich", "Kolyvagin" as "Kolly-vah-gin", "Selmer" as "Sell-mer"; the captions keep the usual spellings.
