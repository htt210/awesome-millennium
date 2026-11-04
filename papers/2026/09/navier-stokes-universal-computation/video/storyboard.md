# Video script: "Navier–Stokes flows that compute"

*Written 4 November 2026 from the plain-language explainer ([`../README.md`](../README.md)), which was checked against the paper's introduction, Sections 3 to 5, and the family's Lean scope.* This script is the source of the video's narration: each scene in [`nscomp_video.py`](nscomp_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `nscomp_video.py`).

The same rules as the other videos apply: one idea per beat, a picture before every new word, a road map at the start of each chapter, and a one-line recap at its end. The machine runs and the encoded points are computed by [`../code/make_figures.py`](../code/make_figures.py).

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A box of fluid at rest; one marked drop; swirls start. | Take a box of water at rest, and push it with a smooth force. Follow one drop. |
| 0.2 | The drop wanders; a target strip glows; "enters ⇔ the program halts". | Can you predict whether the drop ever reaches a certain region? OpenAI claims a force for which the drop gets there exactly when a chosen computer program eventually stops. |
| 0.3 | Title card: *Fluids That Compute*, with "OpenAI preprint, September 2026" underneath. | So water, pushed the right way, can run any program. |
| 0.4 | The road map appears: **Fluids · Machines · The claim · How it works · Is it right?** | |

## Chapter 1 — Fluids

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. The Navier–Stokes equation, its terms labelled: momentum, pressure, friction, force. | The Navier–Stokes equations describe how a fluid like water moves: its momentum, its pressure, its internal friction, and any outside force. |
| 1.2 | A smooth vortex sharpens to a spike, with a question mark. | The Millennium problem asks whether smooth flows in three dimensions stay smooth forever, or can break down in finite time. |
| 1.3 | A card: "Tao, 2016: a fluid computer that builds a smaller, faster copy of itself". | In 2016, Terence Tao suggested a way to attack it: build a fluid that acts like a computer, programmed to copy itself smaller and faster, again and again. |
| 1.4 | **Recap card:** "Navier–Stokes: does smoothness last? Idea: fluids that compute." | So: does smoothness last? One idea is to make fluids compute. |

## Chapter 2 — Machines

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. A tape of cells and a head with a state. | A Turing machine is the simplest computer: a head on a long tape, reading and writing symbols, following a short table of rules. |
| 2.2 | The busy beaver runs six steps, computed, and halts with four ones. | Here is a real run. This machine writes four ones, and then stops. We say it halts. |
| 2.3 | A card: "Turing, 1936: no algorithm decides halting for every machine". | Turing proved that no algorithm can decide, for every machine, whether it will halt. |
| 2.4 | "a system that imitates every machine ⇒ undecidable questions about it". | So if a physical system can imitate every machine, some questions about its future cannot be decided either. |
| 2.5 | **Recap card:** "Machines can't always be predicted. Can fluids imitate them?" | So machines cannot always be predicted. The question is whether fluids can imitate them. |

## Chapter 3 — The claim

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, third box lit. A flat box with opposite faces glued; "fixed viscosity, starts at rest". | Here is the claim. Take a fluid in a box with opposite faces glued together, with a fixed viscosity, starting at rest. |
| 3.2 | A machine card flows into a "compiler" and out comes a formula for a force; a clock shows "constant after time 1". | For any machine and input, an algorithm writes down a smooth force that stops changing after one unit of time. It never runs the machine. |
| 3.3 | The flow stays smooth: "a smooth solution for all time". | With that force, the fluid moves smoothly forever. |
| 3.4 | The marked drop and the strip: "enters ⇔ halts". | And one marked drop enters a fixed strip if and only if the machine halts. |
| 3.5 | **Recap card:** "Claimed: a force that turns a flow from rest into any computer." | So the claim is a force that turns a fluid at rest into any computer. |

## Chapter 4 — How it works

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, fourth box lit. The tape splits into two halves that become the digits of X and Y; a point appears in a square. | The key idea is Cristopher Moore's. Write the tape left of the head as the digits of one number, and the rest as the digits of another. The whole tape becomes one point in a square. |
| 4.2 | The computed busy-beaver points hop between rectangles and land in the red halting band. | Each step moves the point. Here is the same run as before, computed exactly: it lands in the halting band at step six. |
| 4.3 | One rectangle squeezes four times thinner and stretches four times taller; "area 1/16 → 1/16". | Each rule acts on one rectangle by squeezing one way and stretching the other. Area is kept, which is exactly what a fluid that cannot be compressed does. |
| 4.4 | A record tape grows beside the machine: "keep what you would erase". | But a machine can erase, and a fluid's motion can always be undone. So the machine first keeps a record of everything it would erase, an idea of Charles Bennett. |
| 4.5 | Swirls carry rectangles to a parking area and then to their targets, without collisions. | Then smooth swirls carry every rectangle to its target, all rules at once, without collisions. |
| 4.6 | A third axis labelled "clock": moving up one unit runs one step. | A third direction acts as a clock: drifting up by one unit runs one step. After a gentle start, the flow stops changing. |
| 4.7 | "force = what the equation needs for this flow". | Finally, the force is read off from the equation: it is whatever makes this chosen flow obey Navier–Stokes. |
| 4.8 | **Recap card:** "Tape → point; rules → area-keeping maps; swirls + clock → force." | So: tape becomes point, rules become area-keeping maps, and swirls plus a clock give the force. |

## Chapter 5 — Is it right, and what it means

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fifth box lit. A Lean card: "companions formalized: a halting drop in all of space". | OpenAI checked closely related constructions in Lean, including a drop that detects halting in all of space. This exact theorem is outside that scope, and we found no expert assessment yet. |
| 5.2 | "smooth forever: no blowup" next to the Millennium question, still open. | It does not answer the Millennium problem: these flows stay smooth forever. |
| 5.3 | Tao's program: "compute" ticked, "copy itself into blowup" still open. | And it is only one ingredient of Tao's program. Making a fluid compute its own blowup is a much harder step. |
| 5.4 | Final title card and link: github.com/htt210/awesome-millennium. | But it shows, rigorously, that a pushed fluid can be as unpredictable as any computer. |

---

## Notes for production

- **Pacing:** every beat ends with a pause of about 1.25 seconds, and each recap card stays up 3 seconds after its narration.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** checked with the phoneme tester; overrides are in `PRONOUNCE`.
