# Video script: "The Hodge conjecture for CM abelian varieties"

*Written 4 November 2026 from the plain-language explainer ([`../README.md`](../README.md)), which was checked against the paper's Sections 1, 3 and 7 and its Lean scope.* This script is the source of the video's narration: each scene in [`hodge_video.py`](hodge_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `hodge_video.py`).

The same rules as the other videos apply: one idea per beat, a picture before every new word, a road map at the start of each chapter, and a one-line recap at its end. Formulas on screen are kept to a minimum; numbers are spoken in words.

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A doughnut appears; a loop around its hole glows, then a loop around its tube. | Shapes have holes, and mathematicians keep a careful list of them. Each loop that cannot be shrunk is one entry on that list. |
| 0.2 | Inside the doughnut, a curve cut out by an equation appears and casts a glowing "shadow" onto the list. | Some entries come from smaller shapes drawn inside, shapes cut out by equations. Do all the entries that look like they should, really come from such shapes? |
| 0.3 | Title card: *The Hodge conjecture for CM abelian varieties*, with "OpenAI preprint, September 2026" underneath. | That is the Hodge conjecture, a Millennium Prize problem. In 2026, OpenAI claimed to prove it for one important family of shapes. |
| 0.4 | The road map appears: **Shapes · The conjecture · CM · How it works · Is it right?** | |

## Chapter 1 — Shapes, holes and shadows

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. The circle x² + y² = 1, then the label "a variety: a shape cut out by equations". | Algebraic geometry studies shapes cut out by polynomial equations. A circle is the simplest example. Such shapes are called varieties. |
| 1.2 | The equation y² = x³ − x; its complex solutions morph into a doughnut. | Allow the coordinates to be complex numbers, and even simple equations give rich shapes. The complex solutions of this cubic equation form a doughnut. |
| 1.3 | Loop a around the hole, loop b around the tube, each labelled "a class". | Topology records the holes of a shape. On a doughnut, a loop around the hole and a loop around the tube cannot be shrunk to a point. Each one gives a cohomology class. |
| 1.4 | A stack of boxes labelled "degree 0", "degree 1", "degree 2", … beside a higher-dimensional blob. | Higher-dimensional shapes have holes of every dimension, and so classes in every degree. |
| 1.5 | A curve drawn inside a surface; an arrow from it to a glowing class: "its shadow". | Now draw a smaller shape inside, itself cut out by equations. It is called an algebraic cycle, and it has a class too: its shadow. |
| 1.6 | **Recap card:** "Classes record holes. Shapes cut out by equations cast shadows." | So: classes record holes, and shapes cut out by equations cast shadows among them. |

## Chapter 2 — The conjecture

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, second box lit. A single class splits into coloured pieces labelled (p, q). | For complex shapes, every class splits into pieces labelled by two numbers, p and q. Roughly, they count two kinds of directions. |
| 2.2 | The Hodge diamond of an abelian threefold builds row by row; the middle column glows. | Here are the sizes of those pieces for a three-dimensional example, arranged in a diamond. Shadows of cycles always land in the balanced middle column, where p equals q, and they have rational coefficients. |
| 2.3 | A badge: "Hodge class = rational, and in the middle column". | A class that passes both tests is called a Hodge class. |
| 2.4 | Statement card: "**The Hodge conjecture.** Every Hodge class is a rational combination of shadows of algebraic cycles." | The Hodge conjecture says the converse: every Hodge class is the shadow of some rational combination of algebraic cycles. Hodge posed it in 1950. |
| 2.5 | The bottom row lights: "degree 2: true (Lefschetz, 1924)"; products of these climb higher. | In degree two it is known, by a theorem of Lefschetz from 1924. Multiplying those classes together reaches higher degrees too. |
| 2.6 | A lone class high in the diamond, not reached by any product, glows red: "exotic". | The hard part is any Hodge class that is not built that way: an exotic class. For those, someone has to find the cycle. |
| 2.7 | **Recap card:** "Every Hodge class should be a shadow. Exotic classes are the hard part." | So every Hodge class should be a shadow, and the exotic ones are the hard part. |

## Chapter 3 — Abelian varieties and complex multiplication

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, third box lit. A plane of complex numbers with a lattice of dots; a cell is shaded. | Take the complex plane and a lattice, a grid of points. |
| 3.2 | The cell's opposite edges are glued: first into a tube, then into a doughnut. | Glue each point to every point that differs from it by a lattice step. Opposite edges of the shaded cell meet, and the plane becomes a doughnut. |
| 3.3 | "dimension g: glue C^g along a lattice"; a sketch of a higher doughnut. | Do the same in more complex dimensions, and you get an abelian variety: a many-holed, higher-dimensional doughnut that can still be cut out by equations. |
| 3.4 | The square lattice turns a quarter turn and lands exactly on itself. | Most lattices have no special symmetry. But the square lattice is carried to itself by a quarter turn, which is multiplication by i. |
| 3.5 | A generic lattice turns and misses itself; a red cross. A hexagonal lattice turns a sixth turn and lands on itself; a tick. | When an abelian variety has the largest possible set of such symmetries, it is said to have complex multiplication, or to be CM. |
| 3.6 | A cloud of dots for all abelian varieties; a scattering of orange CM points everywhere among them. | CM varieties are rare, only countably many, yet spread densely among all the others. Their symmetries are governed by number fields, which makes them central in number theory. |
| 3.7 | Exotic classes appear on a CM example: "Weil classes, not built from divisors (dimension 4 and up)". | They are also where the hardest test cases of the Hodge conjecture live: exotic classes, called Weil classes, that are not built from products of simple ones. |
| 3.8 | **Recap card:** "CM abelian varieties: doughnuts with extra symmetry, and exotic Hodge classes." | So: CM abelian varieties are doughnuts with extra symmetry, and they carry exotic Hodge classes. |

## Chapter 4 — The claim

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, third box still lit. A timeline: 1982 Deligne, 2025 Markman. | Earlier work set the stage. In 1982 Deligne proved that Hodge classes on abelian varieties have a strong arithmetic property shared by shadows of cycles. In 2025, Eyal Markman proved the conjecture for all abelian varieties of dimension four. |
| 4.2 | Theorem card: "On every CM abelian variety, of any dimension, every Hodge class is a rational combination of shadows of algebraic cycles." | Here is the claim. On every abelian variety with complex multiplication, of any dimension, every Hodge class is the shadow of a rational combination of algebraic cycles. |
| 4.3 | The exotic class from chapter 2 turns green: "exotic classes included". | That includes all the exotic ones. |
| 4.4 | **Recap card:** "Claimed: the Hodge conjecture for every CM abelian variety." | So the claim is the Hodge conjecture for every CM abelian variety. |

## Chapter 5 — How it works

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fourth box lit. Four rows of plus and minus signs: v1, v2, v3, v4. | The proof has five stages. First, a reduction. Each basic CM piece is described by a list of signs, one for each pair of directions. |
| 5.2 | The column sums of rows 1 and 2 match those of rows 3 and 4: "balanced". | The paper shows that every Hodge class on a CM variety can be assembled from one kind of building block: a class on four pieces whose signs balance, the first two adding up to the last two. |
| 5.3 | A counter: "3 pairs of directions: 8 types, 216 balanced quadruples". | So it is enough to show that every balanced block is a shadow. |
| 5.4 | A surface S with four arrows to four boxes B1 to B4; an integral sign with a nonzero result. | Second, a surface does the work. If some surface maps to the four pieces, and a certain integral over it is not zero, then the image of that surface is an algebraic cycle whose shadow is the block. |
| 5.5 | A ball, with a tiling pattern folding into a compact surface; wavy theta functions drawn on it. | Third, the surface is built from theta functions on a quotient of the complex ball, a classical object in number theory. The paper shows the integral is not zero. |
| 5.6 | Hecke and Frobenius labels around the four boxes; each box gets a tick. | Fourth, arithmetic. Using Hecke operators and the Frobenius map modulo primes, it shows the theta forms come from exactly the right CM pieces. |
| 5.7 | The pieces are glued into one surface, and coefficients drop from complex to rational. | Fifth, everything is assembled on one surface and brought back to rational coefficients. |
| 5.8 | **Recap card:** "Balanced blocks; a surface with a nonzero integral; theta functions; arithmetic." | So: balanced blocks, a surface with a nonzero integral, built from theta functions, and checked by arithmetic. |

## Chapter 6 — What follows

| # | On screen | Narration |
|---|---|---|
| 6.1 | Road map, fourth box still lit. An arrow from the theorem to "the Tate conjecture for abelian varieties over finite fields (Milne)". | If it holds, older theorems of James Milne give more. The Tate conjecture, the cousin of the Hodge conjecture over finite fields, would follow for every abelian variety. |
| 6.2 | A second arrow: "the Hodge standard conjecture, abelian varieties, every characteristic". | So would one of Grothendieck's standard conjectures for abelian varieties, in every characteristic. |
| 6.3 | Further arrows to companion papers: "powers of certain sixfolds", "Jacobians of abelian covers". | And several companion papers use this result to prove the Hodge conjecture for further families. |
| 6.4 | **Recap card:** "One family settled, and the Tate conjecture for abelian varieties over finite fields." | One family settled, and with it the Tate conjecture for abelian varieties over finite fields. |

## Chapter 7 — Is it right?

| # | On screen | Narration |
|---|---|---|
| 7.1 | Road map, fifth box lit. A card: "Lean 4, added 26 October 2026: every rational Hodge class on a CM abelian variety is algebraic". | On the twenty-sixth of October, OpenAI added a computer-checked proof of the main theorem in Lean. We have not re-run it, and it does not cover the consequences for the Tate conjecture. |
| 7.2 | Three crossed-out papers: "withdrawn 6 and 7 October: a sign error". | Three other Hodge papers from the same release were withdrawn in October, after a sign error in one of them. |
| 7.3 | A magnifying glass over this paper's references: "none of them cited". | We checked the source: this paper does not cite any of them, and its one revision only updates a citation. |
| 7.4 | "no public expert assessment found, as of 4 November 2026". | As of the fourth of November, we found no public assessment of the written proof by an expert. |
| 7.5 | **Recap card:** "Lean-checked main theorem; written proof not yet assessed." | So: a computer-checked main theorem, and a written proof that experts have yet to assess. |

## Chapter 8 — What it does not do

| # | On screen | Narration |
|---|---|---|
| 8.1 | A vast landscape of shapes; a small orange region labelled "CM abelian varieties". | It does not solve the Millennium problem. The conjecture is about every smooth projective variety, and CM abelian varieties are one special family among them. |
| 8.2 | Other regions glow with question marks: "general abelian varieties", "K3 surfaces", "most varieties". | General abelian varieties, K3 surfaces, and most other shapes are not covered. The proof's tools, theta functions, Hecke operators and Frobenius, are special to this family. |
| 8.3 | Final title card and link: github.com/htt210/awesome-millennium. | But for the shapes with the most symmetry, and some of the strangest Hodge classes, every class may now be a shadow. |

---

## Notes for production

- **Pacing:** every beat ends with a pause of about 1.25 seconds, and each recap card stays up 3 seconds after its narration. Animations play while the narrator describes them.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** checked with the phoneme tester; overrides are in `PRONOUNCE`.
