# Narration script

Generated from the captions burned into the video (`make_captions.py`). Timestamps refer to `o3-sigma-model-continuum-limit.mp4`. The words come from [`storyboard.md`](storyboard.md), the script, which also describes what is on screen.

## 0. Cold open

**[00:00:00]** Put an arrow at every point of a grid. Neighbouring arrows like to point the same way.

**[00:00:07]** Now shrink the grid to nothing. Do the arrows become a smooth quantum field, and does that field have a mass gap?

**[00:00:17]** In October 2026, OpenAI claimed to answer both questions with a proof, for a famous stand-in for the Yang–Mills problem.

## 1. The mass gap

**[00:00:34]** In quantum field theory, particles are ripples in fields that fill space.

**[00:00:40]** The strong nuclear force is described by a Yang–Mills theory.

**[00:00:47]** Its force carriers have no mass in the equations, yet the lightest particles it makes do.

**[00:00:54]** The smallest energy above the empty vacuum is the mass gap.

**[00:01:00]** The Millennium problem asks for both: build four-dimensional Yang–Mills theory with full rigor, and prove that it has a mass gap.

**[00:01:12]** No interacting quantum field theory in four dimensions has ever been built rigorously.

**[00:01:18]** So physicists practise on simpler models.

**[00:01:24]** So: for Yang–Mills, build the theory and prove the gap. Both are open.

## 2. The model

**[00:01:38]** In the O(3) model, each point of a square grid carries an arrow of length one, pointing anywhere in three-dimensional space.

**[00:01:49]** A number called beta sets how strongly neighbours align.

**[00:01:53]** These are samples from our own simulation: larger beta, larger patches.

**[00:02:01]** Like Yang–Mills, this model is asymptotically free, as Polyakov showed in 1975,

**[00:02:10]** and it is expected to make a mass gap out of nothing. But it has only two dimensions, and no gauge field.

**[00:02:20]** In two dimensions the arrows never line up across the whole grid.

**[00:02:25]** The question is how fast distant arrows forget each other.

**[00:02:30]** Our simulation shows exponential decay: straight lines on this log scale.

**[00:02:38]** So: a grid of arrows, asymptotically free, and expected to have a gap.

## 3. The continuum

**[00:02:52]** The decay length, called the correlation length, explodes as beta grows: roughly like e to the two pi beta.

**[00:03:02]** To reach a continuum, shrink the grid while raising beta, so that the correlation length stays fixed in physical units.

**[00:03:13]** The paper measures everything in units set by the lattice itself: the correlation length and the susceptibility.

**[00:03:21]** In those units, our simulations at very different beta fall on one curve.

**[00:03:30]** Proving that such a limit really exists, for every correlation, and finding out what it is, is the hard part.

**[00:03:40]** So: raise beta, shrink the grid, and keep the physical scale fixed.

## 4. The claim

**[00:03:54]** Here is the claim. As beta goes to infinity, in any way at all, the rescaled fields converge to one limit.

**[00:04:05]** The limit satisfies the Osterwalder–Schrader axioms.

**[00:04:09]** So it defines a genuine relativistic quantum field theory, in one space and one time dimension.

**[00:04:20]** It has a single vacuum, and every other state has energy at least some positive m: a mass gap.

**[00:04:30]** And it is interacting: a four-point correlation shows it is not a free field.

**[00:04:37]** So the claim is one canonical limit: an interacting quantum field theory with a mass gap.

## 5. How it works

**[00:04:51]** The method is the renormalization group. Group the arrows into squares, keep one averaged arrow per square, and repeat.

**[00:05:03]** The paper does this exactly, tracking every correction.

**[00:05:08]** New estimates show the corrections shrink at each step, and rare rough regions stay under control.

**[00:05:17]** A square grid is not round.

**[00:05:20]** Comparing two tilted blockings gives a rotation by an irrational angle, and with it full rotation symmetry in the limit.

**[00:05:31]** Finally, the Osterwalder–Schrader reconstruction turns the decay of correlations into the mass gap.

**[00:05:40]** So: block, control the corrections, and reconstruct.

## 6. Is it right?

**[00:05:52]** It comes with companion papers, including one claiming exponential decay at every beta, for all O(n) models with n at least three.

**[00:06:04]** Only that companion result is checked in Lean.

**[00:06:08]** The continuum limit itself is not formalized, and we found no expert assessment yet.

**[00:06:17]** It does not solve the Yang–Mills problem, which needs four dimensions and a gauge field.

**[00:06:27]** But if it holds, a model physicists have studied for fifty years finally has a rigorous continuum theory with a mass gap.

Total running time: 6 min 40 s.
