# Narration script

Generated from the captions burned into the video (`make_captions.py`). Timestamps refer to `exact-bsd-low-selmer-corank.mp4`. The words come from [`storyboard.md`](storyboard.md), the script, which also describes what is on screen.

## 0. Cold open

**[00:00:00]** Here is an equation, and its curve. We want its rational solutions: points where both coordinates are fractions.

**[00:00:10]** Some curves have none. Some have a handful. Some have infinitely many.

**[00:00:15]** Is there a way to tell which, without searching forever?

**[00:00:21]** Two mathematicians guessed one in the nineteen sixties, from a computer experiment.

**[00:00:27]** It became a Millennium Prize problem.

**[00:00:30]** In October 2026, OpenAI claimed to prove its strongest form for a large class of curves.

## 1. Points on a curve

**[00:00:45]** Rational points on such a curve can be added. Here is how.

**[00:00:51]** Draw the line through two of them.

**[00:00:54]** It meets the curve at exactly one more point, and that point is rational too, because the algebra only uses adding and dividing.

**[00:01:05]** Reflect it across the curve's line of symmetry, and you get their sum.

**[00:01:10]** This rule turns the rational points into a group, like the whole numbers under addition.

**[00:01:17]** Adding a point to itself, again and again, can produce infinitely many points. Watch the fractions grow.

**[00:01:27]** In 1922, Mordell proved that all the rational points are built from a finite set of starting points.

**[00:01:35]** The number of independent starting points is the rank.

**[00:01:39]** On this curve every point is a multiple of one, so its rank is one.

**[00:01:47]** A rank zero curve has only finitely many rational points. Higher rank means more room.

**[00:01:54]** But nobody knows a procedure that always computes the rank.

**[00:02:00]** So: rational points can be added, and the rank counts the independent ones.

## 2. The experiment

**[00:02:14]** Instead of searching for rational points, Birch and Swinnerton-Dyer counted solutions modulo primes.

**[00:02:22]** Work with remainders after dividing by seven, and count the pairs that satisfy the equation.

**[00:02:30]** On average, the count is about the prime itself. But a curve with many rational points should have slightly more,

**[00:02:38]** because every rational point gives a solution modulo almost every prime.

**[00:02:46]** So they multiplied the ratios, count over p, for all primes up to some limit.

**[00:02:53]** For a curve of rank zero, the product stayed roughly level.

**[00:02:59]** For rank one it grew like the logarithm of the limit. For rank two, like its square.

**[00:03:05]** The rank was showing up as the power of the growth.

**[00:03:10]** We recomputed their experiment for primes up to a hundred thousand. The four curves separate cleanly, by rank.

**[00:03:21]** These counts are packaged into one function, the curve's L-function.

**[00:03:26]** Its behaviour at one point, s equals one, mirrors that growth.

**[00:03:34]** The conjecture says: the rank of the curve equals the number of times its L-function vanishes at s equals one.

**[00:03:42]** That number is called the analytic rank.

**[00:03:47]** So: count solutions modulo primes, and the L-function at one should reveal the rank.

## 3. The exact formula

**[00:04:01]** They went further, and predicted exactly how big the L-function is when it starts:

**[00:04:07]** an exact formula for its first nonzero Taylor coefficient.

**[00:04:13]** On the left: the L-function's first nonzero coefficient.

**[00:04:19]** On the right, a list of measurements of the same curve: its size as a real shape, and how spread out its rational points are.

**[00:04:30]** Local factors at the primes where the curve goes bad, and the points that return to the start when added to themselves.

**[00:04:40]** And one mysterious piece: the Tate–Shafarevich group, often called Sha.

**[00:04:46]** It counts near-misses: curves that have solutions modulo every prime power,

**[00:04:52]** and over the real numbers, but still no rational solution.

**[00:04:58]** Sha is conjectured to be finite. For most curves, nobody can prove even that.

**[00:05:07]** So the full prediction is an exact formula: one L-value, equal to a product of the curve's measurements.

## 4. What was known

**[00:05:22]** The rank prediction is known only when the analytic rank is zero or one.

**[00:05:28]** In the nineteen eighties, Gross and Zagier built special points,

**[00:05:34]** called Heegner points, whose size is given by the L-function's slope.

**[00:05:41]** Kolyvagin then showed that in analytic rank zero or one, the rank matches and Sha is finite.

**[00:05:48]** And since 2001, every such curve is known to be modular, so this applies to all of them.

**[00:05:58]** The exact formula was harder.

**[00:06:01]** Proving it means matching the two sides prime by prime: for every prime, the same number of factors on each side.

**[00:06:11]** Earlier work proved it at many primes for many curves.

**[00:06:15]** But each result needed extra conditions on the curve or the prime.

**[00:06:20]** No proof covered every prime for every curve of rank zero or one.

**[00:06:27]** So in rank zero and one, the rank was known, but the exact formula only in part.

## 5. The claim

**[00:06:42]** To state the claim we need one more object, the Selmer group.

**[00:06:47]** It collects everything that looks like a rational point when you check the curve modulo powers of a prime.

**[00:06:55]** It contains the true rational points, so its size gives an upper bound on the rank.

**[00:07:01]** And unlike the rank, it can often be computed.

**[00:07:07]** Here is the claim. If this upper bound is zero or one, at even a single prime,

**[00:07:13]** then the rank equals it, Sha is finite, and the exact formula holds, at every prime.

**[00:07:23]** No extra conditions on the curve are needed.

**[00:07:28]** So for a curve whose Selmer bound is zero or one, everything Birch and Swinnerton-Dyer predicted would be true.

## 6. How it works

**[00:07:44]** The paper is clear about what is new.

**[00:07:47]** It takes four inputs: three companion papers from OpenAI, and one published theorem.

**[00:07:55]** The first companion gives the rank and the finiteness of Sha. The second gives the formula at the prime two.

**[00:08:03]** The new step is every other prime.

**[00:08:09]** For each odd prime p, write X for the number of factors of p by which the formula is off. The goal is to show X is zero.

**[00:08:20]** First, a one-sided inequality: X is at least zero, for each curve.

**[00:08:26]** The L-value never has fewer factors of p than predicted.

**[00:08:32]** Next, a sister curve: a twist of the original, chosen to have the opposite analytic rank.

**[00:08:39]** The same inequality applies to it.

**[00:08:43]** Then the hard part: a pair identity. The two errors add up to exactly zero.

**[00:08:51]** Two numbers that are each at least zero, and add up to zero, must both be zero. So the formula is exact at p.

**[00:09:02]** The pair identity combines the curve and its twist over a new number system, where a Heegner point lives.

**[00:09:09]** The paper builds two power series, one from L-values and one from Galois cohomology,

**[00:09:16]** and shows their ratio is a unit: neither has a factor the other lacks.

**[00:09:24]** That takes four stages: the ratio is integral, it has no factor of p,

**[00:09:30]** theta series rule out other common factors, and extra variables push away whatever is left.

**[00:09:40]** Put together with the prime two, the ratio of the two sides is a positive fraction with no prime factors at all.

**[00:09:49]** So it equals one, and the formula holds exactly.

**[00:09:55]** So, at each prime: at least zero, twice, adding up to zero. Exactly zero.

## 7. What follows

**[00:10:10]** A companion paper claims that, for any elliptic curve,

**[00:10:15]** half of its twists have analytic rank zero and half have rank one, with the rest negligible.

**[00:10:22]** Combined with this paper, the full Birch and Swinnerton-Dyer formula would hold for almost all twists of every curve.

**[00:10:33]** Another companion applies the result to the curves x cubed plus y cubed equals a prime.

**[00:10:40]** It concludes that every prime leaving remainder four, seven or eight on division by nine is a sum of two rational cubes.

**[00:10:51]** Some need surprisingly large fractions.

**[00:10:55]** Fifty-three is minus eighteen nineteen over two seventeen, cubed, plus eighteen seventy-two over two seventeen, cubed.

**[00:11:06]** So: the full formula for almost all twists, and a classical question about cubes, if it all holds up.

## 8. Is it right?

**[00:11:23]** The theorem stands on this ninety-four page paper, plus three companions of eighty-two,

**[00:11:29]** a hundred and sixty-four, and a hundred and thirty pages. All of them have to be right.

**[00:11:39]** Unlike OpenAI's Navier–Stokes and quasi-Riemann papers, there is no computer-checked proof in Lean.

**[00:11:48]** It was first posted on the third of October 2026. The seventh of October revision only updates references.

**[00:12:00]** As of the fourth of November, we found no public assessment by an expert, and no paper responding to it.

**[00:12:09]** So: four unreviewed papers, no formal proof, and no expert verdict yet.

## 9. What it does not do

**[00:12:24]** It does not solve the Millennium problem. That asks for every elliptic curve.

**[00:12:30]** Curves of rank two or more, like this one, are untouched. For them, nobody can prove even that Sha is finite.

**[00:12:41]** The pattern Birch and Swinnerton-Dyer saw in their experiment is still unproved for most of these curves.

**[00:12:51]** But for curves with at most one independent point, their prediction may now be complete, down to every last prime.

Total running time: 13 min 5 s.
