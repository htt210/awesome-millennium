# Finite Time Blowup for Navier–Stokes

> **In one paragraph.** The Navier–Stokes equations describe how water and air move. The Millennium Prize question asks whether their solutions always stay smooth, or whether a flow can tear itself apart in a finite time, with its speed shooting to infinity at a point. On 8 September 2026 OpenAI released a paper claiming the second answer. For every viscosity, a fluid that starts at rest, pushed by a carefully designed smooth force, forms a vortex that narrows and spins ever faster until its speed has no limit at time 1, while its total energy stays finite. The official problem explicitly allows this kind of example (its options (C) and (D)), so if the proof is right, it settles the problem as written. It would not tell us whether flows left to themselves, with no force, can break down. OpenAI also published a computer-checked proof in Lean. A group of mathematicians has shown that the computer proof does not follow the written paper step by step, so the paper itself still needs human review.

| | |
|---|---|
| **Paper** | [Finite Time Blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf), OpenAI, 8 September 2026 (166 pages) |
| **The claim, plainly** | For every viscosity there is a smooth push, applied for a while to a fluid at rest, that makes the fluid's speed infinite at one point at time 1, with finite energy, so that the equations cannot be continued smoothly past that moment |
| **Millennium problem** | [Navier–Stokes existence and smoothness](../../../../problems/navier-stokes.md): claims options (C) and (D) |
| **Status** (2 November 2026) | Not peer reviewed. Lean formalization published by OpenAI; its relation to the written proof is [disputed](#8-the-dispute-the-computer-proof-is-not-the-paper). The Clay Institute says it is evaluating the claim |
| **More** | [Lean formalization](https://github.com/openai/NavierStokesAndEuler) · [figures](figures/) · [figure code](code/make_figures.py) |

## Contents

1. [The equations](#1-the-equations)
2. [The question: can a smooth flow break?](#2-the-question-can-a-smooth-flow-break)
3. [Four ways to win](#3-four-ways-to-win)
4. [Why the force is not a cheat](#4-why-the-force-is-not-a-cheat)
5. [The claim](#5-the-claim)
6. [How the construction works](#6-how-the-construction-works)
7. [Checking it by computer](#7-checking-it-by-computer)
8. [The dispute: the computer proof is not the paper](#8-the-dispute-the-computer-proof-is-not-the-paper)
9. [What it would mean, and what it would not](#9-what-it-would-mean-and-what-it-would-not)

## 1. The equations

Picture water in a tank. At every point and every moment it has a velocity: a speed and a direction. The Navier–Stokes equations say how that velocity changes, as the balance of four effects:

- **The fluid carries itself along.** Fast-moving water sweeps its own velocity downstream. This is the source of eddies, swirls and turbulence, and it is the only term that can make things more extreme.
- **Friction smooths things out.** Neighbouring bits of fluid drag on each other, evening out differences. How strongly is set by a number called the **viscosity**: high for honey, low for water.
- **Pressure keeps the volume fixed.** Water can't be squeezed, so pressure pushes back wherever the flow would compress or stretch it.
- **An outside force** may push on the fluid, like a stirring spoon or gravity.

In symbols, for a velocity $u$, pressure $p$, viscosity $\nu$ and force $f$:

```math
\partial_t u + (u \cdot \nabla)\, u = \nu\, \Delta u - \nabla p + f, \qquad \nabla \cdot u = 0 .
```

The first term on the right is friction, the second is pressure, and the second term on the left is the fluid carrying itself along. The tug of war between that self-carrying, which can sharpen a flow, and friction, which smooths it, is what the whole question is about.

## 2. The question: can a smooth flow break?

Start with a perfectly smooth flow: no jumps, no kinks, finite speed everywhere. The equations then say how it evolves. The question is whether it stays smooth forever. Or can the self-carrying effect win against friction, concentrating motion into a smaller and smaller region until, at some finite moment, the speed at a point becomes infinite? That event is called a **blowup**, or a **singularity**.

If a blowup can happen, the equations stop making sense at that point and moment: they no longer predict what comes next. People have studied the question since Jean Leray in 1934. Some partial answers are known:
- solutions can always be continued in a weak, "rough" sense (Leray);
- any breakdown must be confined to a vanishingly small set of points (Caffarelli, Kohn and Nirenberg, 1982);
- blowup has been proved for modified equations, for example Terence Tao's "averaged" Navier–Stokes in 2016;
- blowup has been proved for related equations, notably forced Euler equations without friction (Córdoba and Martínez-Zoroa) and Navier–Stokes with weakened friction (with Zheng). These built singularities by amplifying disturbances across smaller and smaller scales.

For the real equations in three dimensions, the question has stayed open. In 2000 the Clay Mathematics Institute made it one of its seven Millennium Prize Problems, worth one million dollars.

## 3. Four ways to win

The official problem statement, written by Charles Fefferman, offers four ways to win the prize. Two say "smooth forever", two say "can break down", in two different settings: all of space, or a box whose opposite walls are glued together so the fluid wraps around (mathematicians call this a torus).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figures/options-dark.png">
  <img src="figures/options-light.png" alt="A two-by-two grid. Columns: all of space, and a box that wraps around. Rows: smooth forever, options A and B, which must hold for every smooth start with no force; and breaks down, options C and D, which need one example and allow a smooth, fading force. C and D are highlighted as claimed." width="100%">
</picture>

The two halves are very different tasks:

- **(A) and (B)** must hold for *every* smooth starting flow, with *no* outside force.
- **(C) and (D)** need just *one* example of a breakdown, and they allow a smooth outside force, as long as it fades away fast enough in space and time.

The paper claims (C) and (D).

## 4. Why the force is not a cheat

At first sight, allowing a force seems to make breakdown easy. The paper says so itself: for any flow you like, you can *define* the force as whatever is left over when you plug the flow into the equations, and the equations then hold by construction.

The catch is that the rules require the force itself to be **perfectly smooth everywhere, at every moment, including the moment of blowup**, and to fade away. If you draw a blowup and solve for the force, the force almost always blows up too.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figures/force-dark.png">
  <img src="figures/force-light.png" alt="Two panels of schematic curves against time. Left, the cheat: fluid speed shoots up at time 1, and the force you would need shoots up even earlier. Right, the claim: fluid speed still shoots up at time 1, while the force is a smooth bump that rises and falls." width="100%">
</picture>

In the paper's words, "the challenge is to choose a flow that blows up while this residual remains smooth". The individual terms of the equation may each blow up. They must cancel so precisely that their sum, the force, stays smooth, along with all its derivatives, right through the singular moment.

## 5. The claim

Theorem 1.1 of the paper, in plain words, for **every** positive viscosity:

- the fluid **starts at rest**, and stays at rest for an initial stretch of time;
- an outside **force** acts only inside a bounded region of space, from some time after the start until time 2 at the latest, and is smooth everywhere;
- up to time 1 the flow is perfectly **smooth**, it stays inside a fixed bounded region, and its total **energy stays bounded**;
- as time approaches 1, the **speed** near the centre **grows without limit**;
- so **no smooth solution** with bounded energy, driven by the same force from the same rest state, can exist for all time.

Because everything happens in a bounded region, the same example fits inside the wrap-around box (Corollary 10.6). Together these are options (C) and (D).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figures/blowup-dark.png">
  <img src="figures/blowup-light.png" alt="Two panels against time. Left: top speed on a log scale, rising slowly and then shooting up as time approaches 1. Right: total kinetic energy, rising after the start and then staying bounded up to time 1." width="100%">
</picture>

How can the speed be infinite while the energy is finite? The fast motion happens in a region that shrinks as time runs out, and its volume shrinks faster than the square of the speed grows. In the paper's numbers, the energy in the core falls like $(1-t)^{1/2-3h}$, which tends to zero (Section 6 explains $h$).

## 6. How the construction works

The paper builds the flow in three regions: a collapsing **core**, a surrounding ring-shaped zone called the **annulus**, and a calm **exterior**. Then it repairs the leftover errors and shows that no other solution can avoid the blowup.

### Step 1: a collapsing vortex at the core

Use the vertical line through the centre as an axis. Near it, fluid **spirals inward**. As it moves in, it **spins faster**, like a figure skater pulling in their arms: a parcel of fluid that keeps its angular momentum must spin faster at a smaller radius. Incompressibility forbids the incoming fluid from piling up near the axis, so it escapes **up and down along the axis**, which lets the inflow and spin-up continue. Friction keeps competing throughout, carrying angular momentum back outward.

The core keeps the same shape while it shrinks: it is self-similar to leading order. Write $\tau = 1 - t$ for the time left. Then:

- its **width** shrinks like $\tau^{1/2}$;
- its **height** shrinks a little more slowly, like $\tau^{1/2-h}$, where $h$ is a fixed number between 0 and $1/100$. So the core becomes an ever more slender column;
- its **spin and axial speeds** grow like $\tau^{-1/2-h}$, without limit.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figures/collapse-dark.png">
  <img src="figures/collapse-light.png" alt="Left: concentric circles seen from above at times 0.5, 0.75, 0.9, 0.97 and 0.99, shrinking toward the centre, with arrows that grow longer as they shrink. Right: on a log scale against time, the width and height of the core fall toward zero, the height more slowly, while the swirl speed rises without limit." width="100%">
</picture>

### Step 2: the seam leaves an imbalance

Inside the core, the flow balances the equations to leading order. Far outside, the flow is a calm circular motion that slows with distance from the axis. Joining the two leaves an **imbalance in the annulus** between them. The background flow alone would need an outside force there that blows up as $t \to 1$, which is exactly the cheat the rules forbid.

### Step 3: pulses that carry the missing momentum

So the paper makes **the fluid's own motion** supply the missing push. It adds **pulses**: small, rapidly oscillating ripples confined to the annulus, each wrapping around a complete ring, and lasting only a short time.

- **Seeded, then amplified.** Each pulse is started by an *exponentially small* force. The shear of the background flow then makes it grow. In a spinning flow whose rotation falls off fast enough with radius, fluid nudged outward keeps a surplus of spin, and that surplus pushes it further out: a self-reinforcing instability.
- **Then damped.** The same shear tilts the pulse's ripples, making them finer and finer across the radius, until friction wins and the pulse dies out. Each pulse grows and then decays.
- **The payoff.** Although each ripple averages to zero, the *products* of its velocity components do not. A ripple moving outward with extra spin and inward with less spin carries angular momentum outward either way. This averaged **momentum flux** acts like an internal force on the background, and the pulses are tuned so that it cancels the imbalance from Step 2.
- **Two families.** The imbalance has two components (spin momentum and vertical momentum). The paper uses two families of pulses whose fluxes point in different directions, mixed with positive weights. This works because the background was shaped so that the needed flux lies inside the "cone" those two directions span.
- **Finer and finer.** As time runs out, the pulses are placed on ever smaller scales of space and time, keeping pace with the collapsing core.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figures/repair-dark.png">
  <img src="figures/repair-light.png" alt="Left: a shaded collapsing core surrounded by three wavy rings in the annulus, each with finer and smaller wiggles. Right: a bar chart on a log scale of the error left over after each correction round, falling extremely fast." width="100%">
</picture>

Using oscillations to produce a prescribed average stress is a classic idea from **convex integration**, the technique Buckmaster and Vicol used to build unexpected solutions of Navier–Stokes. The new twist here is *dynamical amplification*. The pulses are not simply placed; they are grown by the flow itself. In this respect the method is closer in spirit to the forced-Euler singularities of Córdoba and Martínez-Zoroa.

### Step 4: correct, and correct again

The pulses fix the leading imbalance but create new, smaller errors: their interactions with each other and with the background, and the effects of switching them on and off. The paper removes these in an **infinite cycle of corrections**. Each round:
- re-solves the pulse equations;
- adjusts the pulse strengths;
- corrects the average flow and the pressure;
- restores five bookkeeping integrals.

Each round makes the error vanish faster at the singular point. The paper tracks the rate with an exponent that starts at $1/5$ and gains $1/10$ every round. The corrections are summed with cutoffs that shrink stage by stage. In the end, the leftover error and **all its derivatives vanish faster than any power** as the singular point is approached.

### Step 5: the calm exterior, and the force

Outside the annulus, the flow is a purely circular motion that spreads exactly like heat. It solves the equations with no force at all. The whole construction is then cut off smoothly in space, so everything lives in a bounded region.

The **force is defined as the leftover**: whatever the final flow lacks to satisfy the equations exactly. Near the singular moment that leftover vanishes to every order, so the force extends smoothly through time 1. The paper continues it smoothly past time 1 and switches it off by time 2.

### Step 6: no other solution can escape

Building one flow that blows up is not quite enough. The rules ask that **no** smooth, finite-energy solution with the same force and starting state exists for all time. Lemma 10.5 of the paper shows that any such solution must **coincide** with the constructed one up to time 1. This is a uniqueness argument: two solutions that start together, with one of them well behaved, can never drift apart. So any rival solution inherits the blowup. This lemma is where the dispute's second example sits (Section 8).

### Step 7: every viscosity at once

Everything above is done at viscosity 1. Zooming space by the square root of the viscosity turns it into a solution at any viscosity $\nu$, with the same blowup time:

```math
u_\nu(x,t) = \sqrt{\nu}\; u\big(x/\sqrt{\nu},\, t\big), \qquad p_\nu(x,t) = \nu\, p\big(x/\sqrt{\nu},\, t\big), \qquad f_\nu(x,t) = \sqrt{\nu}\; f\big(x/\sqrt{\nu},\, t\big).
```

## 7. Checking it by computer

OpenAI published a formal proof in **Lean 4**, a language in which a computer checks every logical step.
- **Size:** about 429,000 lines in some 800 files.
- **Shortcuts:** none. It uses no unproved steps ("sorry") and no extra axioms beyond Lean's three standard ones.
- **The statement:** the final theorems are checked against Lean statements of options (C) and (D). These are adapted from the [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/Millenium/NavierStokes.lean) project, so they were not written by OpenAI. We compared them with Fefferman's official statement, condition by condition, and they match: smooth, divergence-free, rapidly decaying data and force; a solution smooth for all time with bounded energy.

If that check holds, the *theorem* is true, whatever the merits of the written paper. **We have not re-run the check ourselves.**

## 8. The dispute: the computer proof is not the paper

On 6 October 2026 A. Bastounis, F. Circelli and A. C. Hansen posted [*Navier–Stokes lost in translation*](https://arxiv.org/abs/2610.08144). Their point is narrow, and important.

**What they claim.** According to the authors, the Lean proof was produced by translating the paper into Lean with AI and accepting the translation once it compiled. A translation that compiles can quietly prove *different* steps from the paper. They give two concrete examples:
- **An inverse estimate** (the paper's Lemma 8.6, equation 8.19, in the mean-flow corrections). The paper claims a bound that costs four extra derivatives. The Lean version proves a weaker bound costing five, by summing a different series.
- **A pressure bound in the uniqueness argument** (equation 10.19, in the proof of Lemma 10.5). Both the bound and the way it is proved differ: different inequalities, a different route through Sobolev embedding, and an extra continuity step.

**What they do not claim.** They do not say the written proof is wrong, or that the theorem is false. Their conclusion is that a compiling Lean proof certifies the *theorem*, not the *paper*: the paper's own arguments still need ordinary peer review.

So the two questions come apart:

| Question | What would answer it |
|---|---|
| Is the theorem true? | The Lean check, if the formal statement is faithful and the check is independently re-run |
| Is the paper's proof correct, as written? | Human peer review of the paper |
| Has the prize been won? | The Clay Institute's rules: publication in a qualifying outlet, a waiting period, and acceptance by the community |

## 9. What it would mean, and what it would not

**If correct, it would:**

- settle the Millennium Prize problem in its official form, through the breakdown options (C) and (D): the forced Navier–Stokes equations can break down from smooth, harmless-looking data;
- show that bounded energy cannot rule out breakdown on its own, and that a smooth push suffices to drive a singularity.

**It would not:**

- **show that flows left to themselves blow up.** With no force, whether a smooth flow can break down on its own remains open. Many mathematicians regard that as the physical heart of the question, even though the prize's wording also accepts forced examples;
- **mean that real water or air blows up.** The equations are a model; at tiny scales real fluids are made of molecules, and the force here is specially engineered;
- **change weather forecasting or engineering.** It is an existence proof about an idealized model, not a new simulation method.

OpenAI released a companion paper the same day, [*Finite time blowup for the Euler equation*](https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf). It claims a blowup *without any force* for the friction-free Euler equations. That paper is not covered here.

## Words used on this page

| Here | In the paper |
|---|---|
| speed infinite at a point | blowup; $\lVert u(t) \rVert_{L^\infty}$ is unbounded as $t \to 1$ |
| smooth | infinitely differentiable, $C^\infty$ |
| wrap-around box | the torus $\mathbb{R}^3/\mathbb{Z}^3$ |
| friction strength | viscosity $\nu$ |
| time left | $\tau = 1 - t$ |
| collapsing vortex | the concentrating axisymmetric background, self-similar to leading order |
| annulus, exterior | the pulse annulus; the heat exterior |
| pulses | oscillatory wave packets, two families |
| momentum flux | stress; averaged quadratic products (covariances) of the pulse velocities |
| leftover, error | the momentum residual $R(u,p)$; the force is $f = R(u,p)$ |
| no other solution can escape | the uniqueness Lemma 10.5 |

Figures: [`code/make_figures.py`](code/make_figures.py). The scales of the core come from Section 2.1 and Theorem 3.1 of the paper; everything else drawn is schematic.
