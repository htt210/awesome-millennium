# Narration script

Generated from the captions burned into the video (`make_captions.py`). Timestamps refer to `hodge-cm-abelian-varieties.mp4`. The words come from [`storyboard.md`](storyboard.md), the script, which also describes what is on screen.

## 0. Cold open

**[00:00:00]** Shapes have holes, and mathematicians keep a careful list of them.

**[00:00:05]** Each loop that cannot be shrunk is one entry on that list.

**[00:00:11]** Some entries come from smaller shapes drawn inside, shapes cut out by equations.

**[00:00:17]** Do all the entries that look like they should, really come from such shapes?

**[00:00:24]** That is the Hodge conjecture, a Millennium Prize problem.

**[00:00:28]** In 2026, OpenAI claimed to prove it for one important family of shapes.

## 1. Shapes, holes and shadows

**[00:00:43]** Algebraic geometry studies shapes cut out by polynomial equations. A circle is the simplest example.

**[00:00:51]** Such shapes are called varieties.

**[00:00:56]** Allow the coordinates to be complex numbers, and even simple equations give rich shapes.

**[00:01:03]** The complex solutions of this cubic equation form a doughnut.

**[00:01:09]** Topology records the holes of a shape.

**[00:01:12]** On a doughnut, a loop around the hole and a loop around the tube cannot be shrunk to a point.

**[00:01:19]** Each one gives a cohomology class.

**[00:01:25]** Higher-dimensional shapes have holes of every dimension, and so classes in every degree.

**[00:01:34]** Now draw a smaller shape inside, itself cut out by equations.

**[00:01:39]** It is called an algebraic cycle, and it has a class too: its shadow.

**[00:01:47]** So: classes record holes, and shapes cut out by equations cast shadows among them.

## 2. The conjecture

**[00:02:01]** For complex shapes, every class splits into pieces labelled by two numbers, p and q.

**[00:02:09]** Roughly, they count two kinds of directions.

**[00:02:15]** Here are the sizes of those pieces for a three-dimensional example, arranged in a diamond.

**[00:02:21]** Shadows of cycles always land in the balanced middle column, where p equals q, and they have rational coefficients.

**[00:02:31]** A class that passes both tests is called a Hodge class.

**[00:02:38]** The Hodge conjecture says the converse: every Hodge class is the shadow of some rational combination of algebraic cycles.

**[00:02:48]** Hodge posed it in 1950.

**[00:02:53]** In degree two it is known, by a theorem of Lefschetz from 1924.

**[00:02:59]** Multiplying those classes together reaches higher degrees too.

**[00:03:05]** The hard part is any Hodge class that is not built that way: an exotic class. For those, someone has to find the cycle.

**[00:03:17]** So every Hodge class should be a shadow, and the exotic ones are the hard part.

## 3. Complex multiplication

**[00:03:30]** Take the complex plane and a lattice, a grid of points.

**[00:03:36]** Glue each point to every point that differs from it by a lattice step.

**[00:03:41]** Opposite edges of the shaded cell meet, and the plane becomes a doughnut.

**[00:03:48]** Do the same in more complex dimensions, and you get an abelian variety:

**[00:03:54]** a many-holed, higher-dimensional doughnut that can still be cut out by equations.

**[00:04:02]** Most lattices have no special symmetry.

**[00:04:06]** But the square lattice is carried to itself by a quarter turn, which is multiplication by i.

**[00:04:14]** When an abelian variety has the largest possible set of such symmetries, it is said to have complex multiplication, or to be CM.

**[00:04:26]** CM varieties are rare, only countably many, yet spread densely among all the others.

**[00:04:33]** Their symmetries are governed by number fields, which makes them central in number theory.

**[00:04:42]** They are also where the hardest test cases of the Hodge conjecture live:

**[00:04:47]** exotic classes, called Weil classes, that are not built from products of simple ones.

**[00:04:55]** So: CM abelian varieties are doughnuts with extra symmetry, and they carry exotic Hodge classes.

## 4. The claim

**[00:05:10]** Earlier work set the stage.

**[00:05:13]** In 1982 Deligne proved that Hodge classes on abelian varieties have a strong arithmetic property shared by shadows of cycles.

**[00:05:23]** In 2025, Eyal Markman proved the conjecture for all abelian varieties of dimension four.

**[00:05:33]** Here is the claim. On every abelian variety with complex multiplication, of any dimension,

**[00:05:40]** every Hodge class is the shadow of a rational combination of algebraic cycles.

**[00:05:48]** That includes all the exotic ones.

**[00:05:53]** So the claim is the Hodge conjecture for every CM abelian variety.

## 5. How it works

**[00:06:05]** The proof has five stages. First, a reduction.

**[00:06:10]** Each basic CM piece is described by a list of signs, one for each pair of directions.

**[00:06:18]** The paper shows that every Hodge class on a CM variety can be assembled from one kind of building block:

**[00:06:25]** a class on four pieces whose signs balance, the first two adding up to the last two.

**[00:06:33]** So it is enough to show that every balanced block is a shadow.

**[00:06:40]** Second, a surface does the work. If some surface maps to the four pieces, and a certain integral over it is not zero,

**[00:06:49]** then the image of that surface is an algebraic cycle whose shadow is the block.

**[00:06:57]** Third, the surface is built from theta functions on a quotient of the complex ball, a classical object in number theory.

**[00:07:06]** The paper shows the integral is not zero.

**[00:07:11]** Fourth, arithmetic.

**[00:07:15]** Using Hecke operators and the Frobenius map modulo primes, it shows the theta forms come from exactly the right CM pieces.

**[00:07:27]** Fifth, everything is assembled on one surface and brought back to rational coefficients.

**[00:07:36]** So: balanced blocks, a surface with a nonzero integral, built from theta functions, and checked by arithmetic.

## 6. What follows

**[00:07:52]** If it holds, older theorems of James Milne give more.

**[00:07:57]** The Tate conjecture, the cousin of the Hodge conjecture over finite fields, would follow for every abelian variety.

**[00:08:07]** So would one of Grothendieck's standard conjectures for abelian varieties, in every characteristic.

**[00:08:15]** And several companion papers use this result to prove the Hodge conjecture for further families.

**[00:08:24]** One family settled, and with it the Tate conjecture for abelian varieties over finite fields.

## 7. Is it right?

**[00:08:38]** On the twenty-sixth of October, OpenAI added a computer-checked proof of the main theorem in Lean.

**[00:08:46]** We have not re-run it, and it does not cover the consequences for the Tate conjecture.

**[00:08:54]** Three other Hodge papers from the same release were withdrawn in October, after a sign error in one of them.

**[00:09:03]** We checked the source: this paper does not cite any of them, and its one revision only updates a citation.

**[00:09:13]** As of the fourth of November, we found no public assessment of the written proof by an expert.

**[00:09:22]** So: a computer-checked main theorem, and a written proof that experts have yet to assess.

## 8. What it does not do

**[00:09:36]** It does not solve the Millennium problem.

**[00:09:39]** The conjecture is about every smooth projective variety, and CM abelian varieties are one special family among them.

**[00:09:49]** General abelian varieties, K3 surfaces, and most other shapes are not covered.

**[00:09:55]** The proof's tools, theta functions, Hecke operators and Frobenius, are special to this family.

**[00:10:05]** But for the shapes with the most symmetry, and some of the strangest Hodge classes, every class may now be a shadow.

Total running time: 10 min 18 s.
