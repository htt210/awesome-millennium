# Video script: "The Quasi-Riemann Hypothesis"

*Written 4 November 2026 from the plain-language explainer ([`../README.md`](../README.md)), which was checked against the paper's Sections 1 and 2 and the outline of its 11/12 companion.* This script is the source of the video's narration: each scene in [`qrh_video.py`](qrh_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `qrh_video.py`).

The same rules as the other videos apply: one idea per beat, a picture before every new word, a road map at the start of each chapter, and a one-line recap at its end. Formulas on screen are kept to the zeta sum (chapter 2) and the theorem (chapter 4); numbers are spoken in words.

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A number line; the primes 2, 3, 5, 7, 11, 13, … light up one by one, irregularly spaced. | Two, three, five, seven, eleven, thirteen. The prime numbers. One at a time, they look random. |
| 0.2 | Zoom out: a staircase counting primes climbs alongside a smooth curve. | But count them, and they follow a smooth curve, with a small wobble. How big can that wobble get? The answer is hidden in the zeros of one function. |
| 0.3 | Title card: *The Quasi-Riemann Hypothesis*, with "OpenAI preprint, September 2026" underneath. | In September 2026, OpenAI released a paper claiming to keep those zeros away from the edge, for the first time. It is not the Riemann hypothesis. But if it holds, it is a major step toward it. |
| 0.4 | The road map appears: **Primes · Zeta · The claim · How it works · Is it right?** | |

## Chapter 1 — Primes

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. A grid of numbers from 1 to 60; the primes are highlighted. | A prime is a whole number bigger than one that only divides by one and itself. There is no simple rule for the next one. |
| 1.2 | A staircase that steps up by one at each prime, from 0 to 100. | Here is a staircase that climbs one step at every prime. Up to one hundred, there are twenty-five of them. |
| 1.3 | A smooth curve appears and follows the staircase closely. | And here is a smooth curve that follows the staircase closely. That the count of primes follows this curve forever is the prime number theorem, proved in 1896. |
| 1.4 | The gap between staircase and curve, up to a million, wiggling inside a dashed band. | The interesting part is the gap between the two. Up to a million there are seventy-eight thousand primes, and the curve is off by only about a hundred and thirty. |
| 1.5 | The band widens with a question mark. | How large can that gap ever get? Nobody knows exactly. But we know what decides it. |
| 1.6 | **Recap card:** "Primes follow a smooth curve. The question is the size of the wobble." | So: primes follow a smooth curve, and the question is the size of the wobble around it. |

## Chapter 2 — Zeta

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. The sum written out: zeta of s equals one plus one over two to the s, plus one over three to the s, and so on. | In 1859, Bernhard Riemann studied one function, called zeta. Add up one, plus one over two to the s, plus one over three to the s, and so on forever. |
| 2.2 | A plane: the input s is a point, with "position" left to right and "height" up. | The input s is a complex number. Think of it as a point on a map, with a position from left to right and a height. |
| 2.3 | Primes flow into the formula: "a product over the primes". | Euler had noticed that this sum over all whole numbers equals a product over the primes alone. So zeta knows about every prime at once. |
| 2.4 | Back to the gap chart: waves of different sizes are added, one per zero. | Riemann found an exact formula for the prime count: the smooth curve, plus one wave for each place where zeta equals zero. |
| 2.5 | Two waves side by side: a loud one for a zero far right, a quiet one for a zero at one half. | How loud each wave is depends on how far right its zero sits. A zero near position one makes a wave almost as big as the count itself. A zero at one half makes the smallest wave possible, about the square root of x. |
| 2.6 | The critical strip: a grey band between positions 0 and 1; the first zeros appear as dots on the line at one half. | All the interesting zeros live in a band between positions zero and one, called the critical strip. Here are the first thirteen. |
| 2.7 | A zero on the right is reflected to a zero on the left. | They come in mirror pairs: a zero at position beta comes with one at one minus beta. |
| 2.8 | **Recap card:** "Zeros of zeta set the wobble. Further right means a louder wave." | So the zeros of zeta set the wobble of the primes, and the further right a zero sits, the louder its wave. |

## Chapter 3 — The question

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, second box still lit. The strip with all dots on the dashed line at one half; label "Riemann hypothesis". | The Riemann hypothesis says every zero in the strip sits exactly on the line at one half. Computers have checked more than ten trillion of them, and every one is on the line. |
| 3.2 | A prize card: "Millennium Prize Problem". | It is one of the seven Millennium Prize Problems, and still unproved. |
| 3.3 | The edge at position 1 lights up green: "no zeros here (1896)". | What has been proved is far weaker. In 1896 it was shown that there are no zeros on the right edge itself. That was enough for the prime number theorem. |
| 3.4 | A green zero-free zone hugs the edge but narrows as the height grows. | Later work pushed the zeros a little way in from the edge, but only by a margin that shrinks as you go higher up. Far enough up, the zeros might creep right up to the edge. |
| 3.5 | A vertical dashed line short of the edge, the whole region to its right shaded: "quasi-Riemann hypothesis". | So mathematicians asked a much more modest question. Is there some fixed line, anywhere short of the edge, with no zeros to its right, at any height at all? This is the quasi-Riemann hypothesis. Nobody could prove it with any number. |
| 3.6 | Cousins of zeta appear: "primes that leave remainder 1 when divided by 4", and so on. | The same questions apply to a family of cousins of zeta, called Dirichlet L-functions. Each one counts primes in a pattern, like the primes that leave remainder one when divided by four. |
| 3.7 | On the real line, a single red dot very close to 1: "a rogue zero?" | For these, there was one more worry: a single rogue zero, sitting on the real line extremely close to one. It is called a Landau–Siegel zero, and nobody could rule it out. |
| 3.8 | **Recap card:** "The quasi-Riemann hypothesis: some fixed line with no zeros to its right." | So the question was: is there some fixed line, short of the edge, with no zeros to its right? |

## Chapter 4 — The claim

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, third box lit. The theorem card: "No zeros with real part above 7/8, for zeta and every Dirichlet L-function." | Here is the claim. Zeta, and every one of its Dirichlet cousins, has no zeros with position greater than seven eighths. |
| 4.2 | The band from 7/8 to 1 turns orange, at every height. | No exceptions: at every height, for every pattern of primes. |
| 4.3 | Its mirror band from 0 to 1/8 turns orange too. | By the mirror symmetry, there are none to the left of one eighth either. Every zero is trapped in the middle three quarters of the strip. |
| 4.4 | A red cross over the rogue zero from chapter 3. | And the rogue zero near one is gone with them. |
| 4.5 | Two steps: "Part I: 11/12" then "Part II: 7/8"; a second card "companion paper, 5 October: 11/12". | The paper proves this in two stages: first a line at eleven twelfths, then sharpened to seven eighths. A shorter companion paper, written with human help, gives a second proof of the eleven twelfths line. |
| 4.6 | **Recap card:** "Claimed: no zeros past 7/8, for zeta and all its cousins." | So the claim is: no zeros past seven eighths, for zeta and all its cousins. Now, how is it proved? |

## Chapter 5 — How it works, part 1: sums that cancel

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fourth box lit. Numbers 1 to 30 each get a score: plus one, minus one or zero. | Give every whole number a score from its prime factors. An even number of different primes scores plus one, an odd number scores minus one, and a repeated prime factor scores zero. |
| 5.2 | The running total of the scores up to 100,000 wanders inside the square-root curves. | These scores behave like coin flips. Add them up, and the running total stays small. |
| 5.3 | A zero at position beta appears; the total is pushed up to size x to the beta. | This total is tied exactly to the zeros. A zero at position beta would push it up to about x to the beta. |
| 5.4 | Arrows both ways: "the total stays below x to the theta" and "no zeros right of theta". | And the other way round: if you can prove the total never grows faster than x to some power theta, there are no zeros to the right of theta. |
| 5.5 | The proof's plan as two boxes: "assume a rightmost zero beyond 7/8" leads to "the same sum must be large and small". | So the proof assumes there is a rightmost zero beyond the line, builds one sum in two ways, and shows it would have to be both large and small. |
| 5.6 | **Recap card:** "No zeros past a line means sums that provably cancel." | So: no zeros past a line is the same as sums that provably cancel. |

## Chapter 6 — How it works, part 2: a crowd and a symmetry

| # | On screen | Narration |
|---|---|---|
| 6.1 | Road map, fourth box still lit. One bar labelled "our sum", with a question mark. | Bounding one such sum directly is hopeless. That is the whole difficulty. |
| 6.2 | The bar is joined by a crowd of bars: a family of related sums. | So the proof hides it in a crowd. It builds a large family of related sums, by twisting the original with extra symbols, cousins of asking whether a number is a perfect square. |
| 6.3 | A dashed line across the crowd: "proved average". | Two facts do the work. First, the family as a whole cancels well on average. |
| 6.4 | Several bars turn orange: copies of our sum. | Second, our sum appears in the family many times over, as nearly identical copies, one for each of many primes. |
| 6.5 | The orange bars grow tall; the average line rises above the dashed bound and turns red. | If our sum were large, its copies alone would push the average over the bound. |
| 6.6 | The orange bars shrink; the average drops back below. | So it must be small. |
| 6.7 | A long row of terms folds into a short row: "a hidden symmetry". | To bound the average, the proof rewrites it and finds special sums with a hidden symmetry. They are the coefficients of the cubic theta function, studied by Kubota and Patterson since the nineteen seventies. |
| 6.8 | The short row folds again, and again. | That symmetry trades a long, hard sum for a shorter one. Repeating the trade shrinks the problem, step by step. |
| 6.9 | A hexagonal grid of dots: the Eisenstein integers, primes in orange. | All of this happens in a different number system: the Eisenstein integers, built from a cube root of one, laid out on a grid of triangles. |
| 6.10 | A Dirichlet L-function slides out of an Eisenstein L-function, as one of two factors. | Each Dirichlet L-function is a factor of an L-function of this number system. So a zero-free line proved for the whole Eisenstein family carries back to zeta and its cousins. |
| 6.11 | A gauge slides from 11/12 to 7/8. | The first stage reaches eleven twelfths. The second changes the setup, with sums of unequal lengths and carefully chosen primes, and squeezes the line to seven eighths. |
| 6.12 | **Recap card:** "Hide the sum in a crowd; bound the crowd with a symmetry; carry it back to zeta." | So: hide the sum in a crowd, bound the crowd with a hidden symmetry, and carry the result back to zeta. |

## Chapter 7 — What would follow

| # | On screen | Narration |
|---|---|---|
| 7.1 | Road map, fourth box still lit. A list begins: "No Landau–Siegel zeros". | If it holds up, several old problems fall at once. The rogue zeros near one are gone for good. |
| 7.2 | The non-square chart: for each prime, the smallest number that is not a perfect square modulo that prime. | For every prime, the smallest number that is not a perfect square, after dividing by that prime, is tiny: at most a fixed power of the logarithm of the prime. That settles an old conjecture of Vinogradov. |
| 7.3 | A padlock-style card: "square roots mod p, fast, no guessing". | It means square roots modulo a prime can be found quickly, without random guessing. |
| 7.4 | Staircases for primes in different patterns, all hugging their curves. | Primes in every pattern follow their smooth curves, with a guaranteed bound on the error. |
| 7.5 | A list of 65 numbers: "Euler's idoneal numbers: complete". | And the companion paper notes it confirms that Euler's list of sixty-five special numbers, called idoneal numbers, is complete. |
| 7.6 | **Recap card:** "One zero-free line unlocks several old results." | One zero-free line, and several old results follow. |

## Chapter 8 — Is it right?

| # | On screen | Narration |
|---|---|---|
| 8.1 | Road map, fifth box lit. A card: "Lean 4: if the real part of s is more than 7/8, zeta of s is not zero." | OpenAI also published a computer-checked version in Lean. The statement for zeta is one line: if the real part of s is more than seven eighths, zeta of s is not zero. |
| 8.2 | "not re-run by us"; a note: "certifies the theorem, not the written proof". | We have not re-run it ourselves. And a computer check certifies the theorem, not the hundred and ninety-nine page written argument. |
| 8.3 | A card: "Quanta, 19 October 2026: number theorists working through it". | People are now reading it. Quanta Magazine reported in October that number theorists are working through the proof, and that Peter Sarnak turned a course he teaches into a study of it. |
| 8.4 | Three cards: Banks, Kerr, Green, each "Landau–Siegel argument, reworked". | Others have already rewritten the related argument about rogue zeros: William Banks with explicit numbers, Bryce Kerr with a simpler proof, and Ben Green with his own account. |
| 8.5 | "No error reported, as of 4 November. Not yet peer reviewed." | No error has been reported so far. No journal has reviewed it yet. |
| 8.6 | **Recap card:** "Computer-checked statement; human reading under way." | So: a computer-checked statement, and a human reading that is still under way. |

## Chapter 9 — What it does not do

| # | On screen | Narration |
|---|---|---|
| 9.1 | The strip: the band 1/8 to 7/8 still wide; the line at 1/2 dashed and labelled "Riemann hypothesis: still open". | It does not prove the Riemann hypothesis. That needs every zero on the line at one half. This keeps them between one eighth and seven eighths. |
| 9.2 | Two curves: x to the seven eighths, and the much smaller square root of x. | The wobble it guarantees is about x to the seven eighths, still far from the square root of x the Riemann hypothesis predicts. |
| 9.3 | A question mark over the gap between 7/8 and 1/2. | And experts doubt this method can be pushed all the way to one half. |
| 9.4 | Final title card and link: github.com/htt210/awesome-millennium. | The primes still keep their deepest secret. But if this proof holds, their zeros have finally been pushed away from the edge. |

---

## Notes for production

- **Pacing:** every beat ends with a pause of about 1.25 seconds, and each recap card stays up 3 seconds after its narration. Animations play while the narrator describes them.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** the narrator says "Ree-mahn", "Deer-ish-lay", "Lan-dow", "See-gul", "Koo-bo-ta"; the captions keep the usual spellings.
