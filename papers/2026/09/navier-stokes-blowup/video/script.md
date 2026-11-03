# Narration script

Generated from the captions burned into the video (`make_captions.py`). Timestamps refer to `navier-stokes-blowup.mp4`. The words come from [`storyboard.md`](storyboard.md), the script, which also describes what is on screen.

## 0. Cold open

**[00:00:00]** This is moving water. Every arrow shows which way the water goes at that spot, and how fast.

**[00:00:08]** For almost two hundred years, one set of equations has described flows like this.

**[00:00:15]** And for almost a century, mathematicians have asked one question about them:

**[00:00:20]** can a smooth flow tear itself apart, with its speed shooting to infinity at a single point?

**[00:00:28]** In September 2026, OpenAI released a paper claiming the answer is yes, if you are allowed to push the fluid in just the right way.

**[00:00:39]** Let's see what that means, how it works, and how sure we can be.

## 1. The equations

**[00:00:52]** At every point and every moment, water has a velocity: a speed and a direction.

**[00:00:59]** The Navier–Stokes equations tell you how all those arrows change over time. They balance four effects.

**[00:01:09]** First, the fluid carries itself along. Fast water sweeps its own speed downstream.

**[00:01:16]** This is what makes eddies and swirls, and it is the only effect that can make the flow more extreme.

**[00:01:25]** Second, friction smooths things out. Neighbouring bits of fluid drag on each other and even out their differences.

**[00:01:34]** How strong that is depends on a number called the viscosity: high for honey, low for water.

**[00:01:43]** Third, pressure keeps the volume fixed.

**[00:01:47]** Water cannot be squeezed, so pressure pushes back wherever the flow would compress it.

**[00:01:53]** Squash a blob one way, and it must stretch the other way.

**[00:02:00]** And fourth, there may be an outside force: a stirring spoon, or gravity, pushing on the fluid.

**[00:02:11]** Written in symbols, these four effects make the Navier–Stokes equations. You do not need to read them.

**[00:02:18]** What matters is the tug of war: the fluid carrying itself along can sharpen the flow, and friction smooths it.

**[00:02:28]** So: a velocity at every point, and four effects that change it.

## 2. The question

**[00:02:41]** Start with a perfectly smooth flow: no jumps, no kinks, a finite speed everywhere.

**[00:02:49]** The equations tell you how it evolves.

**[00:02:53]** Does it stay smooth forever?

**[00:02:55]** Or can the self-carrying effect beat friction, squeezing the motion into a smaller and smaller region,

**[00:03:03]** until at some moment the speed at a point becomes infinite?

**[00:03:09]** That event is called a blowup. If it can happen, the equations stop predicting what comes next.

**[00:03:18]** People have worked on this since Jean Leray in 1934.

**[00:03:23]** We know breakdowns would have to be confined to a tiny set of points.

**[00:03:28]** We know blowups happen in modified versions of the equations, and in related equations,

**[00:03:34]** built by amplifying disturbances on smaller and smaller scales.

**[00:03:40]** But for the real three-dimensional equations, the question stayed open.

**[00:03:48]** In 2000 it became one of the seven Millennium Prize Problems, with a million dollars for a solution.

**[00:03:57]** The official problem offers four ways to win.

**[00:04:01]** Two say the flow stays smooth forever, two say it can break down, in two settings:

**[00:04:08]** all of space, or a box whose opposite walls are glued together, so the fluid wraps around.

**[00:04:16]** The smooth options must hold for every smooth starting flow, with no outside force at all.

**[00:04:24]** The breakdown options need just one example, and they allow a smooth outside force, as long as it fades away.

**[00:04:32]** The paper claims these two, C and D.

**[00:04:38]** So the question is whether a smooth flow can blow up, and the paper claims an example that does.

## 3. Why the force is not a cheat

**[00:04:53]** Allowing a force sounds like cheating. Here is the cheat. Draw any flow you like that blows up.

**[00:05:00]** Plug it into the equations, and call whatever is left over "the force". The equations now hold, by definition.

**[00:05:10]** But the rules forbid this. The force itself must be perfectly smooth, at every moment, including the moment of blowup.

**[00:05:19]** And the force you would need to hold up a blowup almost always blows up too.

**[00:05:26]** So the real challenge is to find a breakdown that a smooth, calm push can sustain.

**[00:05:32]** Each term in the equation may explode, but they must cancel so precisely that the leftover,

**[00:05:39]** the force, stays smooth right through the singular moment.

**[00:05:45]** That is the whole difficulty: a smooth push, and a flow that tears itself apart anyway.

## 4. The claim

**[00:05:59]** Here is what the paper claims, for every value of the viscosity. The fluid starts completely at rest.

**[00:06:08]** A smooth force acts on it, only inside a bounded region of space, and only for a bounded stretch of time.

**[00:06:18]** Up to time one, the flow is perfectly smooth, and its total energy stays bounded.

**[00:06:26]** And as time approaches one, the speed near the centre grows without any limit.

**[00:06:33]** So no smooth solution with bounded energy, driven by the same force from the same start, can continue for all time.

**[00:06:42]** That is breakdown option C, and the same example, placed in a wrap-around box, gives option D.

**[00:06:53]** How can the speed be infinite while the energy is finite?

**[00:06:57]** Because the fast motion happens in a region that shrinks as time runs out.

**[00:07:03]** It shrinks fast enough that the energy inside it actually goes to zero.

**[00:07:10]** So: a fluid at rest, a smooth push, finite energy, and infinite speed at time one. Now, how is it built?

## 5. How it works: the collapsing vortex

**[00:07:28]** The construction has three regions: a collapsing core in the middle,

**[00:07:33]** a ring-shaped zone around it called the annulus, and a calm exterior outside.

**[00:07:42]** Start with the core. Picture a vertical axis through the centre. Near it, fluid spirals inward.

**[00:07:51]** As it moves inward, it spins faster, like a figure skater pulling in their arms.

**[00:07:57]** A parcel of fluid that keeps its angular momentum must spin faster at a smaller radius.

**[00:08:05]** The incoming fluid cannot pile up near the axis, because water cannot be squeezed.

**[00:08:12]** So it escapes up and down along the axis, and that lets the inflow and the spin-up continue.

**[00:08:21]** As time runs out, the whole core shrinks while keeping its shape.

**[00:08:27]** Its width shrinks like the square root of the time left.

**[00:08:31]** Its height shrinks a little more slowly, so the core becomes an ever more slender spinning column.

**[00:08:39]** And its speeds grow without limit, a little faster than one over the width.

**[00:08:44]** Friction keeps fighting the whole time, carrying spin back outward, but it does not win.

**[00:08:53]** So the core is a slender, spinning column, collapsing toward the centre and spinning ever faster.

## 6. How it works: pulses and corrections

**[00:09:08]** Inside the core, the flow balances the equations. Outside, the exterior does too.

**[00:09:16]** But joining the two leaves an imbalance in the annulus between them.

**[00:09:22]** On its own, this background flow would need an outside force in the annulus that blows up.

**[00:09:28]** That is exactly the cheat the rules forbid. So the paper makes the fluid's own motion supply the missing push.

**[00:09:38]** It adds pulses: small, rapidly oscillating ripples inside the annulus.

**[00:09:45]** Each one wraps around a complete ring, and lasts only a short time.

**[00:09:52]** Each pulse is started by an exponentially small push. Then the background flow amplifies it.

**[00:10:00]** Here is how. In a spinning flow whose rotation falls off quickly with distance,

**[00:10:06]** a bit of fluid nudged outward keeps a surplus of spin, and that surplus flings it further out.

**[00:10:13]** The effect feeds itself, and the pulse grows.

**[00:10:20]** But the same shearing flow tilts the ripples and packs them closer and closer, until friction wins, and the pulse dies away.

**[00:10:29]** Each pulse grows, and then decays.

**[00:10:35]** Now the key point. A ripple averages to zero: as much fluid moves in as out. But look at what it carries.

**[00:10:44]** Fluid moving outward carries extra spin, and fluid moving inward carries a deficit. Either way, spin is carried outward.

**[00:10:55]** That steady, averaged flow of momentum acts like an internal force on the background.

**[00:11:01]** The pulses are tuned so that it cancels the imbalance in the annulus.

**[00:11:08]** The imbalance has two parts, one for spin and one for vertical motion.

**[00:11:14]** So the paper uses two families of pulses, pointing in different directions, mixed in positive amounts.

**[00:11:22]** The background is shaped so that the target always lies inside the cone between them.

**[00:11:30]** As time runs out, the pulses are placed on ever smaller scales, keeping pace with the collapsing core.

## 6. How it works: corrections, force, uniqueness

**[00:11:41]** The pulses fix the leading imbalance, but they create new, smaller errors:

**[00:11:47]** from interacting with each other, with the background, and from being switched on and off.

**[00:11:55]** So the paper corrects them, in an infinite cycle of rounds.

**[00:11:59]** Each round makes the remaining error vanish faster at the singular point.

**[00:12:05]** In the end, the leftover error, and every one of its derivatives,

**[00:12:10]** vanishes faster than any power as you approach the singular point.

**[00:12:18]** Outside, the flow is a simple circular motion that spreads exactly like heat. It needs no force at all.

**[00:12:27]** And the whole construction is cut off smoothly, so everything happens in a bounded region.

**[00:12:35]** The force is then defined as the leftover: whatever the final flow still lacks.

**[00:12:41]** Because that leftover vanishes so completely near the singular moment,

**[00:12:46]** the force passes smoothly through time one, and it switches off by time two.

**[00:12:55]** One more step. The rules ask that no smooth solution with the same force and start exists for all time.

**[00:13:03]** The paper shows that any such solution would have to coincide with the constructed one, all the way up to time one.

**[00:13:12]** Two solutions that start together, with one of them well behaved, can never drift apart.

**[00:13:20]** So any rival inherits the blowup, and cannot stay smooth forever.

**[00:13:29]** Everything so far is done for one particular viscosity.

**[00:13:33]** Zooming space by the square root of the viscosity turns it into a solution for any viscosity, with the same blowup time.

**[00:13:44]** Let's put it together. A collapsing, spinning core. An imbalance in the ring around it, cancelled by amplified pulses.

**[00:13:53]** Infinitely many rounds of corrections. A force equal to the smooth leftover.

**[00:13:59]** And a uniqueness argument that leaves no escape.

## 7. Is it right?

**[00:14:08]** So, is it right?

**[00:14:10]** OpenAI also published a proof written in Lean, a language in which a computer checks every logical step.

**[00:14:18]** It is about four hundred and twenty-nine thousand lines long, with no gaps and no extra assumptions.

**[00:14:28]** Its final theorems are checked against a statement of the prize problem that OpenAI did not write,

**[00:14:35]** adapted from a project called Formal Conjectures. If that check holds, the theorem is true.

**[00:14:42]** We have not re-run it ourselves.

**[00:14:47]** But in October, three mathematicians, Bastounis, Circelli and Hansen, pointed out a problem.

**[00:14:55]** According to them, the Lean proof was produced by translating the paper with AI,

**[00:15:01]** and accepting the translation as soon as it compiled.

**[00:15:06]** They found places where the Lean proof quietly proves different steps from the paper:

**[00:15:12]** a weaker bound in one place, and a different argument for a pressure estimate in the uniqueness step.

**[00:15:20]** They do not claim the paper is wrong. Their point is that a computer proof certifies the theorem, not the paper.

**[00:15:28]** The paper's own arguments still need ordinary human review.

**[00:15:35]** So there are three separate questions. Is the theorem true? That is for the Lean check.

**[00:15:42]** Is the paper's proof correct as written? That is for peer review. And has the prize been won?

**[00:15:49]** That is for the Clay Institute, which says it is evaluating the claim.

**[00:15:56]** A computer-checked theorem, and a written proof that still needs review.

## 8. What it would mean

**[00:16:08]** If it is right, it settles the Millennium problem as officially written:

**[00:16:13]** the forced Navier–Stokes equations can break down from smooth, harmless-looking starting data.

**[00:16:21]** But it does not show that flows left to themselves blow up.

**[00:16:25]** Without any force, that question is still open, and many mathematicians see it as the physical heart of the problem.

**[00:16:35]** It also does not mean real water blows up.

**[00:16:39]** The equations are a model, real fluids are made of molecules, and this force is specially engineered.

**[00:16:47]** And it changes nothing about weather forecasting or engineering.

**[00:16:53]** A breakdown, driven by a perfectly smooth push. The unforced question remains.

## 9. Closing

**[00:17:04]** Let's recap. A fluid at rest. A calm, smooth push. A spinning column that narrows and spins up without limit.

**[00:17:14]** A ring of amplified ripples carrying exactly the momentum it needs.

**[00:17:19]** And a force that stays smooth while the flow tears itself apart.

**[00:17:25]** If the proof holds up, the answer to the prize question, as it was written, is yes: smooth flows can break.

**[00:17:34]** Whether they can break all on their own is still a mystery.

Total running time: 17 min 43 s.
