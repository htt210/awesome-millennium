# Narration script

Generated from the captions burned into the video (`make_captions.py`). Timestamps refer to `quasi-riemann-hypothesis.mp4`. The words come from [`storyboard.md`](storyboard.md), the script, which also describes what is on screen.

## 0. Cold open

**[00:00:00]** Two, three, five, seven, eleven, thirteen. The prime numbers. One at a time, they look random.

**[00:00:10]** But count them, and they follow a smooth curve, with a small wobble. How big can that wobble get?

**[00:00:17]** The answer is hidden in the zeros of one function.

**[00:00:23]** In September 2026, OpenAI released a paper claiming to keep those zeros away from the edge, for the first time.

**[00:00:32]** It is not the Riemann hypothesis. But if it holds, it is a major step toward it.

## 1. Primes

**[00:00:46]** A prime is a whole number bigger than one that only divides by one and itself. There is no simple rule for the next one.

**[00:00:58]** Here is a staircase that climbs one step at every prime. Up to one hundred, there are twenty-five of them.

**[00:01:07]** And here is a smooth curve that follows the staircase closely.

**[00:01:11]** That the count of primes follows this curve forever is the prime number theorem, proved in 1896.

**[00:01:21]** The interesting part is the gap between the two.

**[00:01:25]** Up to a million there are seventy-eight thousand primes, and the curve is off by only about a hundred and thirty.

**[00:01:34]** How large can that gap ever get? Nobody knows exactly. But we know what decides it.

**[00:01:42]** So: primes follow a smooth curve, and the question is the size of the wobble around it.

## 2. Zeta

**[00:01:56]** In 1859, Bernhard Riemann studied one function, called zeta.

**[00:02:03]** Add up one, plus one over two to the s, plus one over three to the s, and so on forever.

**[00:02:11]** The input s is a complex number. Think of it as a point on a map, with a position from left to right and a height.

**[00:02:22]** Euler had noticed that this sum over all whole numbers equals a product over the primes alone.

**[00:02:29]** So zeta knows about every prime at once.

**[00:02:35]** Riemann found an exact formula for the prime count: the smooth curve, plus one wave for each place where zeta equals zero.

**[00:02:48]** How loud each wave is depends on how far right its zero sits.

**[00:02:53]** A zero near position one makes a wave almost as big as the count itself.

**[00:02:58]** A zero at one half makes the smallest wave possible, about the square root of x.

**[00:03:07]** All the interesting zeros live in a band between positions zero and one, called the critical strip.

**[00:03:14]** Here are the first thirteen.

**[00:03:18]** They come in mirror pairs: a zero at position beta comes with one at one minus beta.

**[00:03:27]** So the zeros of zeta set the wobble of the primes, and the further right a zero sits, the louder its wave.

## 3. The question

**[00:03:42]** The Riemann hypothesis says every zero in the strip sits exactly on the line at one half.

**[00:03:49]** Computers have checked more than ten trillion of them, and every one is on the line.

**[00:03:56]** It is one of the seven Millennium Prize Problems, and still unproved.

**[00:04:04]** What has been proved is far weaker. In 1896 it was shown that there are no zeros on the right edge itself.

**[00:04:12]** That was enough for the prime number theorem.

**[00:04:17]** Later work pushed the zeros a little way in from the edge, but only by a margin that shrinks as you go higher up.

**[00:04:25]** Far enough up, the zeros might creep right up to the edge.

**[00:04:32]** So mathematicians asked a much more modest question.

**[00:04:37]** Is there some fixed line, anywhere short of the edge, with no zeros to its right, at any height at all?

**[00:04:44]** This is the quasi-Riemann hypothesis. Nobody could prove it with any number.

**[00:04:54]** The same questions apply to a family of cousins of zeta, called Dirichlet L-functions.

**[00:05:00]** Each one counts primes in a pattern, like the primes that leave remainder one when divided by four.

**[00:05:09]** For these, there was one more worry: a single rogue zero, sitting on the real line extremely close to one.

**[00:05:18]** It is called a Landau–Siegel zero, and nobody could rule it out.

**[00:05:25]** So the question was: is there some fixed line, short of the edge, with no zeros to its right?

## 4. The claim

**[00:05:39]** Here is the claim. Zeta, and every one of its Dirichlet cousins, has no zeros with position greater than seven eighths.

**[00:05:51]** No exceptions: at every height, for every pattern of primes.

**[00:05:58]** By the mirror symmetry, there are none to the left of one eighth either.

**[00:06:02]** Every zero is trapped in the middle three quarters of the strip.

**[00:06:08]** And the rogue zero near one is gone with them.

**[00:06:14]** The paper proves this in two stages: first a line at eleven twelfths, then sharpened to seven eighths.

**[00:06:22]** A shorter companion paper, written with human help, gives a second proof of the eleven twelfths line.

**[00:06:32]** So the claim is: no zeros past seven eighths, for zeta and all its cousins. Now, how is it proved?

## 5. How it works: sums that cancel

**[00:06:48]** Give every whole number a score from its prime factors.

**[00:06:52]** An even number of different primes scores plus one, an odd number scores minus one, and a repeated prime factor scores zero.

**[00:07:04]** These scores behave like coin flips. Add them up, and the running total stays small.

**[00:07:11]** This total is tied exactly to the zeros. A zero at position beta would push it up to about x to the beta.

**[00:07:22]** And the other way round: if you can prove the total never grows faster than x to some power theta,

**[00:07:28]** there are no zeros to the right of theta.

**[00:07:34]** So the proof assumes there is a rightmost zero beyond the line,

**[00:07:39]** builds one sum in two ways, and shows it would have to be both large and small.

**[00:07:47]** So: no zeros past a line is the same as sums that provably cancel.

## 6. How it works: a crowd and a symmetry

**[00:08:00]** Bounding one such sum directly is hopeless. That is the whole difficulty.

**[00:08:07]** So the proof hides it in a crowd. It builds a large family of related sums, by twisting the original with extra symbols,

**[00:08:16]** cousins of asking whether a number is a perfect square.

**[00:08:22]** Two facts do the work. First, the family as a whole cancels well on average.

**[00:08:30]** Second, our sum appears in the family many times over, as nearly identical copies, one for each of many primes.

**[00:08:40]** If our sum were large, its copies alone would push the average over the bound.

**[00:08:47]** So it must be small.

**[00:08:51]** To bound the average, the proof rewrites it and finds special sums with a hidden symmetry.

**[00:08:58]** They are the coefficients of the cubic theta function, studied by Kubota and Patterson since the nineteen seventies.

**[00:09:08]** That symmetry trades a long, hard sum for a shorter one. Repeating the trade shrinks the problem, step by step.

**[00:09:18]** All of this happens in a different number system: the Eisenstein integers,

**[00:09:24]** built from a cube root of one, laid out on a grid of triangles.

**[00:09:31]** Each Dirichlet L-function is a factor of an L-function of this number system.

**[00:09:37]** So a zero-free line proved for the whole Eisenstein family carries back to zeta and its cousins.

**[00:09:47]** The first stage reaches eleven twelfths.

**[00:09:50]** The second changes the setup, with sums of unequal lengths and carefully chosen primes, and squeezes the line to seven eighths.

**[00:10:01]** So: hide the sum in a crowd, bound the crowd with a hidden symmetry, and carry the result back to zeta.

## 7. What would follow

**[00:10:17]** If it holds up, several old problems fall at once. The rogue zeros near one are gone for good.

**[00:10:27]** For every prime, the smallest number that is not a perfect square,

**[00:10:32]** after dividing by that prime, is tiny: at most a fixed power of the logarithm of the prime.

**[00:10:39]** That settles an old conjecture of Vinogradov.

**[00:10:45]** It means square roots modulo a prime can be found quickly, without random guessing.

**[00:10:54]** Primes in every pattern follow their smooth curves, with a guaranteed bound on the error.

**[00:11:02]** And the companion paper notes it confirms that Euler's list of sixty-five special numbers, called idoneal numbers, is complete.

**[00:11:14]** One zero-free line, and several old results follow.

## 8. Is it right?

**[00:11:26]** OpenAI also published a computer-checked version in Lean.

**[00:11:30]** The statement for zeta is one line: if the real part of s is more than seven eighths, zeta of s is not zero.

**[00:11:40]** We have not re-run it ourselves.

**[00:11:43]** And a computer check certifies the theorem, not the hundred and ninety-nine page written argument.

**[00:11:52]** People are now reading it. Quanta Magazine reported in October that number theorists are working through the proof,

**[00:12:00]** and that Peter Sarnak turned a course he teaches into a study of it.

**[00:12:07]** Others have already rewritten the related argument about rogue zeros:

**[00:12:12]** William Banks with explicit numbers, Bryce Kerr with a simpler proof, and Ben Green with his own account.

**[00:12:22]** No error has been reported so far. No journal has reviewed it yet.

**[00:12:29]** So: a computer-checked statement, and a human reading that is still under way.

## 9. What it does not do

**[00:12:43]** It does not prove the Riemann hypothesis. That needs every zero on the line at one half.

**[00:12:49]** This keeps them between one eighth and seven eighths.

**[00:12:56]** The wobble it guarantees is about x to the seven eighths, still far from the square root of x the Riemann hypothesis predicts.

**[00:13:08]** And experts doubt this method can be pushed all the way to one half.

**[00:13:14]** The primes still keep their deepest secret.

**[00:13:18]** But if this proof holds, their zeros have finally been pushed away from the edge.

Total running time: 13 min 28 s.
