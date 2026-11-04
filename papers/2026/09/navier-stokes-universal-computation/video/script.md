# Narration script

Generated from the captions burned into the video (`make_captions.py`). Timestamps refer to `navier-stokes-universal-computation.mp4`. The words come from [`storyboard.md`](storyboard.md), the script, which also describes what is on screen.

## 0. Cold open

**[00:00:00]** Take a box of water at rest, and push it with a smooth force. Follow one drop.

**[00:00:07]** Can you predict whether the drop ever reaches a certain region?

**[00:00:11]** OpenAI claims a force for which the drop gets there exactly when a chosen computer program eventually stops.

**[00:00:21]** So water, pushed the right way, can run any program.

## 1. Fluids

**[00:00:33]** The Navier–Stokes equations describe how a fluid like water moves:

**[00:00:38]** its momentum, its pressure, its internal friction, and any outside force.

**[00:00:47]** The Millennium problem asks whether smooth flows in three dimensions stay smooth forever, or can break down in finite time.

**[00:00:59]** In 2016, Terence Tao suggested a way to attack it: build a fluid that acts like a computer,

**[00:01:07]** programmed to copy itself smaller and faster, again and again.

**[00:01:14]** So: does smoothness last? One idea is to make fluids compute.

## 2. Machines

**[00:01:27]** A Turing machine is the simplest computer: a head on a long tape, reading and writing symbols, following a short table of rules.

**[00:01:40]** Here is a real run. This machine writes four ones, and then stops. We say it halts.

**[00:01:49]** Turing proved that no algorithm can decide, for every machine, whether it will halt.

**[00:01:58]** So if a physical system can imitate every machine, some questions about its future cannot be decided either.

**[00:02:08]** So machines cannot always be predicted. The question is whether fluids can imitate them.

## 3. The claim

**[00:02:22]** Here is the claim. Take a fluid in a box with opposite faces glued together, with a fixed viscosity, starting at rest.

**[00:02:33]** For any machine and input, an algorithm writes down a smooth force that stops changing after one unit of time.

**[00:02:42]** It never runs the machine.

**[00:02:47]** With that force, the fluid moves smoothly forever.

**[00:02:53]** And one marked drop enters a fixed strip if and only if the machine halts.

**[00:03:01]** So the claim is a force that turns a fluid at rest into any computer.

## 4. How it works

**[00:03:14]** The key idea is Cristopher Moore's.

**[00:03:17]** Write the tape left of the head as the digits of one number, and the rest as the digits of another.

**[00:03:24]** The whole tape becomes one point in a square.

**[00:03:30]** Each step moves the point. Here is the same run as before, computed exactly: it lands in the halting band at step six.

**[00:03:42]** Each rule acts on one rectangle by squeezing one way and stretching the other.

**[00:03:48]** Area is kept, which is exactly what a fluid that cannot be compressed does.

**[00:03:56]** But a machine can erase, and a fluid's motion can always be undone.

**[00:04:01]** So the machine first keeps a record of everything it would erase, an idea of Charles Bennett.

**[00:04:10]** Then smooth swirls carry every rectangle to its target, all rules at once, without collisions.

**[00:04:19]** A third direction acts as a clock: drifting up by one unit runs one step. After a gentle start, the flow stops changing.

**[00:04:31]** Finally, the force is read off from the equation: it is whatever makes this chosen flow obey Navier–Stokes.

**[00:04:41]** So: tape becomes point, rules become area-keeping maps, and swirls plus a clock give the force.

## 5. Is it right?

**[00:04:57]** OpenAI checked closely related constructions in Lean, including a drop that detects halting in all of space.

**[00:05:05]** This exact theorem is outside that scope, and we found no expert assessment yet.

**[00:05:14]** It does not answer the Millennium problem: these flows stay smooth forever.

**[00:05:22]** And it is only one ingredient of Tao's program. Making a fluid compute its own blowup is a much harder step.

**[00:05:32]** But it shows, rigorously, that a pushed fluid can be as unpredictable as any computer.

Total running time: 5 min 44 s.
