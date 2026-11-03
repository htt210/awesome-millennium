# Video script: "Finite Time Blowup for Navier–Stokes"

*Written 3 November 2026 from the plain-language explainer ([`../README.md`](../README.md)), which was checked against Sections 1–3 of the paper.* This script is the source of the video's narration: each scene in [`ns_video.py`](ns_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `ns_video.py`).

The same rules as the ETH video apply: one idea per beat, an example before every new word, a road map at the start of each chapter, and a one-line recap at its end. Apart from the equation itself (chapter 1) and the scaling rule (chapter 6g), no formulas appear on screen; numbers are spoken in words.

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A field of small arrows appears, gently swirling, like water in a tank seen from above. | This is moving water. Every arrow shows which way the water goes at that spot, and how fast. |
| 0.2 | The swirl tightens toward the centre; arrows near the centre grow longer and longer. | For almost two hundred years, one set of equations has described flows like this. And for almost a century, mathematicians have asked one question about them: can a smooth flow tear itself apart, with its speed shooting to infinity at a single point? |
| 0.3 | Title card: *Finite Time Blowup for Navier–Stokes*, with "OpenAI preprint, September 2026" underneath. | In September 2026, OpenAI released a paper claiming the answer is yes, if you are allowed to push the fluid in just the right way. Let's see what that means, how it works, and how sure we can be. |
| 0.4 | The road map appears: **The equations · The question · The claim · How it works · Is it right?** | |

## Chapter 1 — The equations

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. The arrow field again, frozen. One arrow is highlighted with a label "velocity". | At every point and every moment, water has a velocity: a speed and a direction. The Navier–Stokes equations tell you how all those arrows change over time. They balance four effects. |
| 1.2 | Card "1. The fluid carries itself along". A blob of fast arrows drifts downstream, carried by the flow. | First, the fluid carries itself along. Fast water sweeps its own speed downstream. This is what makes eddies and swirls, and it is the only effect that can make the flow more extreme. |
| 1.3 | Card "2. Friction smooths things out". A sharp spike in a speed profile spreads into a gentle bump. | Second, friction smooths things out. Neighbouring bits of fluid drag on each other and even out their differences. How strong that is depends on a number called the viscosity: high for honey, low for water. |
| 1.4 | Card "3. Pressure keeps the volume fixed". A small square of fluid is squashed in one direction and stretches in the other, keeping its area. | Third, pressure keeps the volume fixed. Water cannot be squeezed, so pressure pushes back wherever the flow would compress it. Squash a blob one way, and it must stretch the other way. |
| 1.5 | Card "4. An outside force". A spoon-like arrow pushes on part of the fluid. | And fourth, there may be an outside force: a stirring spoon, or gravity, pushing on the fluid. |
| 1.6 | The equation appears, its terms coloured to match the four cards. | Written in symbols, these four effects make the Navier–Stokes equations. You do not need to read them. What matters is the tug of war: the fluid carrying itself along can sharpen the flow, and friction smooths it. |
| 1.7 | **Recap card:** "Velocity everywhere; four effects: self-carrying, friction, pressure, force." | So: a velocity at every point, and four effects that change it. |

## Chapter 2 — The question

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. A smooth speed profile, a gentle hill. | Start with a perfectly smooth flow: no jumps, no kinks, a finite speed everywhere. The equations tell you how it evolves. |
| 2.2 | The hill sharpens into a spike that shoots off the top of the screen; a clock reads "time 1". | Does it stay smooth forever? Or can the self-carrying effect beat friction, squeezing the motion into a smaller and smaller region, until at some moment the speed at a point becomes infinite? |
| 2.3 | Label on the spike: **blowup**. | That event is called a blowup. If it can happen, the equations stop predicting what comes next. |
| 2.4 | A timeline: 1934 Leray; 1982 Caffarelli–Kohn–Nirenberg; 2000 the prize; 2016 Tao; recent: Córdoba, Martínez-Zoroa and Zheng. | People have worked on this since Jean Leray in 1934. We know breakdowns would have to be confined to a tiny set of points. We know blowups happen in modified versions of the equations, and in related equations, built by amplifying disturbances on smaller and smaller scales. But for the real three-dimensional equations, the question stayed open. |
| 2.5 | A prize card: "Clay Millennium Prize Problem · $1,000,000". | In 2000 it became one of the seven Millennium Prize Problems, with a million dollars for a solution. |
| 2.6 | A two-by-two grid: columns "all of space" and "a box that wraps around"; rows "smooth forever" and "breaks down". Cells A, B, C, D fill in. | The official problem offers four ways to win. Two say the flow stays smooth forever, two say it can break down, in two settings: all of space, or a box whose opposite walls are glued together, so the fluid wraps around. |
| 2.7 | Cells A and B highlighted: "every smooth start, no force". | The smooth options must hold for every smooth starting flow, with no outside force at all. |
| 2.8 | Cells C and D highlighted: "one example, a smooth fading force allowed". The word "claimed" appears on both. | The breakdown options need just one example, and they allow a smooth outside force, as long as it fades away. The paper claims these two, C and D. |
| 2.9 | **Recap card:** "Blowup: infinite speed in finite time. The paper claims the breakdown options, C and D." | So the question is whether a smooth flow can blow up, and the paper claims an example that does. |

## Chapter 3 — Why the force is not a cheat

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, third box lit. A blowing-up speed curve. | Allowing a force sounds like cheating. Here is the cheat. Draw any flow you like that blows up. Plug it into the equations, and call whatever is left over "the force". The equations now hold, by definition. |
| 3.2 | A second curve, "force you would need", shoots up even faster. A red cross. | But the rules forbid this. The force itself must be perfectly smooth, at every moment, including the moment of blowup. And the force you would need to hold up a blowup almost always blows up too. |
| 3.3 | Right panel: the force is a calm smooth bump; the speed still shoots up. | So the real challenge is to find a breakdown that a smooth, calm push can sustain. Each term in the equation may explode, but they must cancel so precisely that the leftover, the force, stays smooth right through the singular moment. |
| 3.4 | **Recap card:** "The force must stay smooth at the moment of blowup. That is the whole difficulty." | That is the whole difficulty: a smooth push, and a flow that tears itself apart anyway. |

## Chapter 4 — The claim

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, third box lit. A checklist builds line by line. "Fluid starts at rest." | Here is what the paper claims, for every value of the viscosity. The fluid starts completely at rest. |
| 4.2 | "A smooth force, in a bounded region, for a bounded time." | A smooth force acts on it, only inside a bounded region of space, and only for a bounded stretch of time. |
| 4.3 | "Smooth up to time 1, with bounded energy." | Up to time one, the flow is perfectly smooth, and its total energy stays bounded. |
| 4.4 | "Speed grows without limit as time approaches 1." A speed curve shoots up. | And as time approaches one, the speed near the centre grows without any limit. |
| 4.5 | "No smooth solution can continue forever." | So no smooth solution with bounded energy, driven by the same force from the same start, can continue for all time. That is breakdown option C, and the same example, placed in a wrap-around box, gives option D. |
| 4.6 | Two graphs side by side: speed shooting up; energy staying flat. | How can the speed be infinite while the energy is finite? Because the fast motion happens in a region that shrinks as time runs out. It shrinks fast enough that the energy inside it actually goes to zero. |
| 4.7 | **Recap card:** "From rest, a smooth push, finite energy, and infinite speed at time 1." | So: a fluid at rest, a smooth push, finite energy, and infinite speed at time one. Now, how is it built? |

## Chapter 5 — How it works, part 1: the collapsing vortex

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fourth box lit. Three regions drawn as nested shapes: a central **core**, a ring-shaped **annulus**, and the **exterior**. | The construction has three regions: a collapsing core in the middle, a ring-shaped zone around it called the annulus, and a calm exterior outside. |
| 5.2 | Side view of the core: a vertical axis. Arrows spiral inward toward the axis. | Start with the core. Picture a vertical axis through the centre. Near it, fluid spirals inward. |
| 5.3 | A dot circling the axis moves to a smaller radius and visibly speeds up. | As it moves inward, it spins faster, like a figure skater pulling in their arms. A parcel of fluid that keeps its angular momentum must spin faster at a smaller radius. |
| 5.4 | Arrows turn upward and downward along the axis. | The incoming fluid cannot pile up near the axis, because water cannot be squeezed. So it escapes up and down along the axis, and that lets the inflow and the spin-up continue. |
| 5.5 | The core outline shrinks over time: width faster than height, becoming a slender column. Labels "width" and "height". | As time runs out, the whole core shrinks while keeping its shape. Its width shrinks like the square root of the time left. Its height shrinks a little more slowly, so the core becomes an ever more slender spinning column. |
| 5.6 | A speed meter beside the column climbs without limit. | And its speeds grow without limit, a little faster than one over the width. Friction keeps fighting the whole time, carrying spin back outward, but it does not win. |
| 5.7 | **Recap card:** "The core: a slender spinning column that narrows and spins up, faster and faster." | So the core is a slender, spinning column, collapsing toward the centre and spinning ever faster. |

## Chapter 6 — How it works, part 2: pulses, corrections, and the rest

### 6a. The seam

| # | On screen | Narration |
|---|---|---|
| 6a.1 | The three regions again. The annulus glows red; label "imbalance". | Inside the core, the flow balances the equations. Outside, the exterior does too. But joining the two leaves an imbalance in the annulus between them. |
| 6a.2 | A curve labelled "force needed in the annulus" shoots up toward time 1. | On its own, this background flow would need an outside force in the annulus that blows up. That is exactly the cheat the rules forbid. So the paper makes the fluid's own motion supply the missing push. |

### 6b. Pulses

| # | On screen | Narration |
|---|---|---|
| 6b.1 | Inside the annulus, a ring of small ripples appears, wrapping all the way around. | It adds pulses: small, rapidly oscillating ripples inside the annulus. Each one wraps around a complete ring, and lasts only a short time. |
| 6b.2 | A tiny seed ripple grows: an amplitude curve rises. | Each pulse is started by an exponentially small push. Then the background flow amplifies it. |
| 6b.3 | A parcel nudged outward keeps its extra spin, and an arrow pushes it further outward. | Here is how. In a spinning flow whose rotation falls off quickly with distance, a bit of fluid nudged outward keeps a surplus of spin, and that surplus flings it further out. The effect feeds itself, and the pulse grows. |
| 6b.4 | The ripple's stripes are tilted by the shear and squeezed closer together; the amplitude curve turns over and decays. | But the same shearing flow tilts the ripples and packs them closer and closer, until friction wins, and the pulse dies away. Each pulse grows, and then decays. |
| 6b.5 | Two fluid parcels: one moving outward with extra spin (blue), one moving inward with less spin (orange). Both produce an outward arrow labelled "spin carried outward". | Now the key point. A ripple averages to zero: as much fluid moves in as out. But look at what it carries. Fluid moving outward carries extra spin, and fluid moving inward carries a deficit. Either way, spin is carried outward. |
| 6b.6 | The outward flux arrows point into the annulus's red imbalance, which fades. | That steady, averaged flow of momentum acts like an internal force on the background. The pulses are tuned so that it cancels the imbalance in the annulus. |
| 6b.7 | A cone between two arrows labelled "family 1" and "family 2"; a target arrow inside it. | The imbalance has two parts, one for spin and one for vertical motion. So the paper uses two families of pulses, pointing in different directions, mixed in positive amounts. The background is shaped so that the target always lies inside the cone between them. |
| 6b.8 | Successive rings of ripples, finer and finer, nested toward the centre. | As time runs out, the pulses are placed on ever smaller scales, keeping pace with the collapsing core. |

### 6c. Correct, and correct again

| # | On screen | Narration |
|---|---|---|
| 6c.1 | A bar chart: "error left over" after each round, bars shrinking dramatically on a log scale. | The pulses fix the leading imbalance, but they create new, smaller errors: from interacting with each other, with the background, and from being switched on and off. |
| 6c.2 | The bars keep shrinking, round after round. | So the paper corrects them, in an infinite cycle of rounds. Each round makes the remaining error vanish faster at the singular point. In the end, the leftover error, and every one of its derivatives, vanishes faster than any power as you approach the singular point. |

### 6d. The calm exterior, and the force

| # | On screen | Narration |
|---|---|---|
| 6d.1 | The exterior: circular arrows, slower farther out, spreading gently. | Outside, the flow is a simple circular motion that spreads exactly like heat. It needs no force at all. And the whole construction is cut off smoothly, so everything happens in a bounded region. |
| 6d.2 | The force curve: a smooth bump passing calmly through time 1 and switching off by time 2. | The force is then defined as the leftover: whatever the final flow still lacks. Because that leftover vanishes so completely near the singular moment, the force passes smoothly through time one, and it switches off by time two. |

### 6e. No other solution can escape

| # | On screen | Narration |
|---|---|---|
| 6e.1 | Two curves starting together: "the constructed flow" and "any rival solution"; they stay glued together up to time 1. | One more step. The rules ask that no smooth solution with the same force and start exists for all time. The paper shows that any such solution would have to coincide with the constructed one, all the way up to time one. Two solutions that start together, with one of them well behaved, can never drift apart. |
| 6e.2 | The rival curve is forced up into the blowup; a red cross on "smooth forever". | So any rival inherits the blowup, and cannot stay smooth forever. |

### 6f. Every viscosity at once

| # | On screen | Narration |
|---|---|---|
| 6f.1 | The column, then a zoom; the scaling rule appears: "zoom space by the square root of the viscosity". | Everything so far is done for one particular viscosity. Zooming space by the square root of the viscosity turns it into a solution for any viscosity, with the same blowup time. |
| 6f.2 | **Recap montage:** core → annulus → pulses → corrections → force → uniqueness. | Let's put it together. A collapsing, spinning core. An imbalance in the ring around it, cancelled by amplified pulses. Infinitely many rounds of corrections. A force equal to the smooth leftover. And a uniqueness argument that leaves no escape. |

## Chapter 7 — Is it right?

| # | On screen | Narration |
|---|---|---|
| 7.1 | Road map, fifth box lit. Card: "Lean 4: about 429,000 lines, no gaps, no extra axioms". | So, is it right? OpenAI also published a proof written in Lean, a language in which a computer checks every logical step. It is about four hundred and twenty-nine thousand lines long, with no gaps and no extra assumptions. |
| 7.2 | Card: "Checked against a statement of options C and D written by others (Formal Conjectures)". | Its final theorems are checked against a statement of the prize problem that OpenAI did not write, adapted from a project called Formal Conjectures. If that check holds, the theorem is true. We have not re-run it ourselves. |
| 7.3 | Card: "Bastounis, Circelli, Hansen, October 2026: the Lean proof is not the paper". | But in October, three mathematicians, Bastounis, Circelli and Hansen, pointed out a problem. According to them, the Lean proof was produced by translating the paper with AI, and accepting the translation as soon as it compiled. |
| 7.4 | Two side-by-side boxes: "Paper: four extra derivatives" vs "Lean: five extra derivatives"; then "Paper: one argument for a pressure bound" vs "Lean: a different argument". | They found places where the Lean proof quietly proves different steps from the paper: a weaker bound in one place, and a different argument for a pressure estimate in the uniqueness step. |
| 7.5 | Card: "They do not say the paper is wrong." | They do not claim the paper is wrong. Their point is that a computer proof certifies the theorem, not the paper. The paper's own arguments still need ordinary human review. |
| 7.6 | A three-row table: "Is the theorem true? → the Lean check"; "Is the paper's proof right? → peer review"; "Has the prize been won? → the Clay Institute". | So there are three separate questions. Is the theorem true? That is for the Lean check. Is the paper's proof correct as written? That is for peer review. And has the prize been won? That is for the Clay Institute, which says it is evaluating the claim. |
| 7.7 | **Recap card:** "Computer-checked theorem; the written proof still needs review." | A computer-checked theorem, and a written proof that still needs review. |

## Chapter 8 — What it would mean

| # | On screen | Narration |
|---|---|---|
| 8.1 | A check mark: "Settles the prize problem as written, through options C and D". | If it is right, it settles the Millennium problem as officially written: the forced Navier–Stokes equations can break down from smooth, harmless-looking starting data. |
| 8.2 | A cross: "Does not show that unforced flows blow up". | But it does not show that flows left to themselves blow up. Without any force, that question is still open, and many mathematicians see it as the physical heart of the problem. |
| 8.3 | Two more crosses: "Not real water blowing up" and "No change to weather or engineering". | It also does not mean real water blows up. The equations are a model, real fluids are made of molecules, and this force is specially engineered. And it changes nothing about weather forecasting or engineering. |
| 8.4 | **Recap card:** "A breakdown, driven by a smooth push. The unforced question remains." | A breakdown, driven by a perfectly smooth push. The unforced question remains. |

## Chapter 9 — Closing

| # | On screen | Narration |
|---|---|---|
| 9.1 | The full road map lit; the arrow field from the opening, swirling into the collapsing column. | Let's recap. A fluid at rest. A calm, smooth push. A spinning column that narrows and spins up without limit. A ring of amplified ripples carrying exactly the momentum it needs. And a force that stays smooth while the flow tears itself apart. |
| 9.2 | Final title card and link: github.com/htt210/awesome-millennium. | If the proof holds up, the answer to the prize question, as it was written, is yes: smooth flows can break. Whether they can break all on their own is still a mystery. |

---

## Notes for production

- **Pacing:** as in the ETH video, every beat ends with a pause of about 1.5 seconds, and each recap card stays up 3 seconds after its narration. Animations play while the narrator describes them.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** the narrator says "Luh-ray", "Mar-tee-nez Zoroa", "Cheer-chelly" and "Bas-too-nis"; the captions show Leray, Martínez-Zoroa, Circelli and Bastounis.
