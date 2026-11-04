# P vs NP

> **Question.** Can every problem whose solutions can be *checked* quickly also be *solved* quickly?

**Status:** open. [Clay Mathematics Institute description](https://www.claymath.org/millennium/p-vs-np/) · [official problem statement (S. Cook)](https://www.claymath.org/wp-content/uploads/2022/06/pvsnp.pdf)

## Statement

$\mathsf{P}$ is the class of decision problems solvable by a deterministic Turing machine in time $n^{O(1)}$ on inputs of length $n$. $\mathsf{NP}$ is the class of problems whose "yes" instances have certificates of polynomial length that can be verified in polynomial time. The problem asks whether

$$
\mathsf{P} = \mathsf{NP}.
$$

Cook and Levin showed that satisfiability of Boolean formulas (SAT), and already $3$-SAT, is $\mathsf{NP}$-complete: a polynomial-time algorithm for $3$-SAT would give one for every problem in $\mathsf{NP}$. Most researchers expect $\mathsf{P} \ne \mathsf{NP}$.

## The landscape: from P vs NP to fine-grained hypotheses

$\mathsf{P} \ne \mathsf{NP}$ only says $3$-SAT has no polynomial-time algorithm. *Fine-grained* hypotheses make sharper predictions about **how much** exponential time is needed, and a large body of conditional lower bounds rests on them. Write $n$ for the number of variables and $m$ for the number of clauses.

| Hypothesis | Prediction |
|---|---|
| ETH (Impagliazzo–Paturi 2001) | $3$-SAT needs $2^{\Omega(n)}$ time |
| SETH | for every $\varepsilon \gt 0$ some $k$-SAT needs $2^{(1-\varepsilon)n}$ time |
| #ETH | counting $3$-SAT solutions needs $2^{\Omega(n)}$ time |
| Gap-ETH | even distinguishing satisfiable from far-from-satisfiable $3$-CNFs needs $2^{\Omega(n)}$ time |

They are nested: $\text{SETH} \Rightarrow \text{ETH} \Rightarrow \mathsf{P} \ne \mathsf{NP}$. Refuting ETH therefore removes the strongest *quantitative* reasons to believe $3$-SAT is exponentially hard, **but it does not resolve P vs NP**: a running time such as $2^{n/\sqrt{\log n}}$ is subexponential yet still grows faster than every polynomial.

## Explained here

<!-- BEGIN:papers -->
### Adjacent results

*Papers that settle a closely related question in the problem's landscape without deciding it.*

| Date | Paper | Status |
|---|---|---|
| 2026-10-25 | **[The Exponential Time Hypothesis is False](../papers/2026/10/eth-is-false/)**<br>OpenAI — A deterministic algorithm counts the satisfying assignments of any $k$-CNF in subexponential time and polynomial space; the case $k = 3$ refutes ETH. | Preprint · Formalized (Lean 4) · Under examination |
| 2026-09-23 | **[The Unique Games Theorem](../papers/2026/09/unique-games-theorem/)**<br>OpenAI — Claims a proof of Khot's Unique Games Conjecture, which would make the best known approximation algorithms for Max-Cut, Vertex Cover and many other problems provably optimal unless P = NP. | Preprint · Formalized (Lean 4) · Under examination |
| 2026-09-23 | **[Beyond the Square-Root Exponent for Depth-Three Boolean Circuits](../papers/2026/09/depth-three-circuits-beyond-square-root/)**<br>OpenAI — Claims one explicit polynomial-time function whose three-layer OR–AND–OR circuits need $2^{\omega(\sqrt n)}$ gates, past the square-root exponent that explicit depth-three lower bounds had not beaten since the 1980s. | Preprint · Formalized (Lean 4) · Not yet examined |

- *ETH is false*: Refutes ETH, SETH, #ETH, Gap-ETH and NSETH. A subexponential running time can still be superpolynomial, so P vs NP stays open.
- *Unique Games Theorem*: Does not decide whether P equals NP. It shows that many approximation problems are exactly as hard as NP problems, so their best known algorithms cannot be improved unless P = NP.
- *Depth-three circuits beyond the square root*: A circuit lower bound for a weak model, three-layer circuits, for a function that is easy for ordinary programs. It does not decide P vs NP and is far from the bounds that would affect general circuits.
<!-- END:papers -->

## Queue

Papers we plan to explain next. Their claims have **not** been reviewed here yet.

<!-- BEGIN:backlog -->
_Nothing queued._
<!-- END:backlog -->
