# Video script: "Beyond the Square-Root Exponent for Depth-Three Boolean Circuits"

*Written 4 November 2026 from the plain-language explainer ([`../README.md`](../README.md)), which was checked against the paper's introduction, its Sections 1 to 5, and its Lean scope.* This script is the source of the video's narration: each scene in [`circuits_video.py`](circuits_video.py) reads its beats from the tables below, by number. Each beat lists what is on screen and the exact narration. Captions show the same words; the narrator says a few of them differently (`PRONOUNCE` in `circuits_video.py`).

The same rules as the other videos apply: one idea per beat, a picture before every new word, a road map at the start of each chapter, and a one-line recap at its end.

---

## Chapter 0 — Cold open

| # | On screen | Narration |
|---|---|---|
| 0.1 | Black. A small circuit of gates; an input of zeros and ones flows up and the gates light. | Every computer program can be unrolled into a circuit: a network of tiny gates, each computing AND, OR, or NOT. |
| 0.2 | A gate counter climbs: "huge circuit ⇒ no fast program". | Prove that some problem needs an enormous circuit, and you prove it has no fast program. That is one road to P versus NP. |
| 0.3 | Title card: *Beyond the Square-Root Exponent*, with "OpenAI preprint, September 2026" underneath. | In 2026, OpenAI claimed a step along a small part of that road: circuits with only three layers. |
| 0.4 | The road map appears: **Circuits · The barrier · The claim · How it works · Is it right?** | |

## Chapter 1 — Circuits

| # | On screen | Narration |
|---|---|---|
| 1.1 | Road map, first box lit. An AND gate and an OR gate with input bits and outputs. | A gate takes bits, zeros and ones, and outputs one bit. AND outputs one only if all its inputs are one. OR outputs one if any input is one. |
| 1.2 | A circuit with a gate counter: "size = number of gates". | A circuit's size is its number of gates. Any fast program can be turned into a circuit that is not much bigger than its running time. |
| 1.3 | "needs huge circuits ⇒ no fast program"; for a problem in NP, "⇒ P ≠ NP". | So if a problem in NP needed huge circuits, it would have no fast program, and P would not equal NP. |
| 1.4 | A short bar: "best proven for general circuits: about 3 gates per input bit". | But proving that circuits must be large is very hard. For general circuits, the best bound known for any explicit problem is only about three gates per input bit. |
| 1.5 | **Recap card:** "Huge circuits would mean no fast program; proving it is hard." | So: huge circuits would mean no fast program, but proving that circuits are huge is hard. |

## Chapter 2 — Three layers

| # | On screen | Narration |
|---|---|---|
| 2.1 | Road map, first box still lit. The 4-bit circuit builds layer by layer: bottom ORs, middle ANDs, top OR. | So researchers study simpler circuits. Here: circuits with exactly three layers. OR gates at the bottom, AND gates in the middle, and one OR gate on top. |
| 2.2 | Gates with many inputs; a NOT on an input marked "free". | Gates may take any number of inputs, and a NOT on an input is free. Every function can be computed this way. The question is how many gates it takes. |
| 2.3 | The same circuit computes parity: an input 1011 lights the path; "11 gates, checked on all 16 inputs". | Take parity: is the number of ones odd? Here is a three-layer circuit for four bits, with eleven gates. We checked it on all sixteen inputs. |
| 2.4 | **Recap card:** "Three layers: OR, then AND, then OR. Count the gates." | So a three-layer circuit is OR, then AND, then OR, and we count its gates. |

## Chapter 3 — The barrier

| # | On screen | Narration |
|---|---|---|
| 3.1 | Road map, second box lit. The computed parity curve: log of gates divided by √n falls toward 1. | For n bits, split the inputs into about the square root of n blocks, and combine the parities of the blocks. That takes about two to the power square root of n gates. |
| 3.2 | A card: "1980s, Håstad: parity needs 2^Ω(√n) gates — random restrictions". | In the nineteen-eighties, Johan Håstad proved that parity really needs that many, up to the constant in the exponent, with a method called random restrictions. |
| 3.3 | Dotted lines at 2√n and 4√n; every proven bound stays below a line. | Later work sharpened the constants. But for every explicit function, the proven exponent stayed a constant times the square root of n. |
| 3.4 | A question card: "one explicit function needing more than 2^(A√n) gates, for every constant A?" | The open question: is there one explicit function that needs more than two to the power A root n gates, for every constant A? |
| 3.5 | **Recap card:** "For decades, the exponent stayed at a constant times √n." | So, for decades, the exponent stayed at a constant times the square root of n. |

## Chapter 4 — The claim

| # | On screen | Narration |
|---|---|---|
| 4.1 | Road map, third box lit. A card: "one language, decided by a fast program". | OpenAI's paper claims yes. It gives one fixed problem, solved by a fast program. |
| 4.2 | The parity chart again; an arrow climbs past every dotted line. | For every constant A, once the input is long enough, three-layer circuits for it need more than two to the power A root n gates. |
| 4.3 | The input bar at n = 20,480: data, hash bits, polynomial, coefficients, ignored. | The input is cut into blocks: data bits, bits for a hash, a polynomial, and some coefficients. The program hashes the data, evaluates the polynomial, and reads off one bit. |
| 4.4 | Twelve bars near one half: "fraction accepted, per slice". | We implemented it exactly as defined. Fixing the extra bits gives a slice of the problem. Each random slice we tried accepts about half its inputs. |
| 4.5 | One slice glows: "some slice is hard; the program never has to find it". | The proof shows that some slice is hard for circuits. The program never has to find it. |
| 4.6 | **Recap card:** "Claimed: one fast-to-compute function beats every constant A." | So the claim is one function, fast to compute, that beats every constant A. |

## Chapter 5 — How it works

| # | On screen | Narration |
|---|---|---|
| 5.1 | Road map, fourth box lit. The top OR with its middle ANDs; each AND accepts only yes-inputs. | Start at the top. The top gate is an OR, so every middle gate may only accept inputs that the slice accepts. |
| 5.2 | Small patches try to cover a region of yes-inputs, a quarter of the square. | If each middle gate accepts only a tiny fraction of inputs, it takes very many of them to cover the quarter of inputs that the slice accepts. |
| 5.3 | The computed restriction histogram: a million clauses of width 20 become about 7 narrow ones. | To show that, the proof uses random restrictions: leave a few variables free, and fix the rest at random. Most clauses vanish, and the survivors are narrow. |
| 5.4 | "wide formula = weighted mix of narrow formulas, total weight ≤ 2, any number of clauses". | The new restriction lemma makes this exact. A wide formula becomes a weighted mix of narrow ones, with total weight at most two, however many clauses it had. |
| 5.5 | A narrow formula splits into few sparse pieces; all checked at once against a random slice. | Then a sparsification method cuts each narrow formula into a few simple pieces. There are few enough to check them all at once, against a randomly chosen slice. |
| 5.6 | **Recap card:** "Restrict, simplify, then count the gates." | So: restrict, simplify, and then count the gates. |

## Chapter 6 — Is it right, and what it means

| # | On screen | Narration |
|---|---|---|
| 6.1 | Road map, fifth box lit. A Lean card: "the main theorem, formalized in Lean 4". | OpenAI published a computer-checked proof of the main theorem, in Lean. We have not re-run it. |
| 6.2 | A card: "October 2026: a follow-up extends it to every fixed depth (search results)". | According to search results, an October report already builds on it, for circuits of every fixed depth. We found no expert assessment yet. |
| 6.3 | A large "P vs NP?" stays open; "three layers: a weak model". | It does not decide P versus NP. Three-layer circuits are a weak model, and the function is easy for ordinary programs. |
| 6.4 | A far-off marker on the exponent axis: "Valiant's target: about n ÷ log log n". | It is also far from a famous target set by Leslie Valiant, where three-layer bounds would say something about general circuits. |
| 6.5 | Final title card and link: github.com/htt210/awesome-millennium. | But after nearly forty years, it moves the square-root barrier for three-layer circuits. |

---

## Notes for production

- **Pacing:** every beat ends with a pause of about 1.25 seconds, and each recap card stays up 3 seconds after its narration.
- **Narrator:** both BookVoice US voices, male and female, with the same pictures and timing.
- **Pronunciation:** checked with the phoneme tester; overrides are in `PRONOUNCE`.
