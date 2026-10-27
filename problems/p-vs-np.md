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

- *ETH is false*: Refutes ETH, SETH, #ETH, Gap-ETH and NSETH. A subexponential running time can still be superpolynomial, so P vs NP stays open.
<!-- END:papers -->

## Queue

Papers we plan to explain next. Their claims have **not** been reviewed here yet.

<!-- BEGIN:backlog -->
- **[The Unique Games Theorem](https://github.com/openai/math/blob/main/preprints/The-Unique-Games-Theorem-September-23-2026/paper.pdf)** — OpenAI, 2026-09-23 · *adjacent*  
  Claims a proof of Khot's Unique Games Conjecture, with optimal NP-hardness of approximation for Max-Cut and Vertex Cover (openai/math family 102).
- **[Beyond the Square-Root Exponent for Depth-Three Boolean Circuits](https://github.com/openai/math/blob/main/preprints/Beyond-the-Square-Root-Exponent-for-Depth-Three-Boolean-Circuits-September-23-2026/main.pdf)** — OpenAI, 2026-09-23 · *adjacent*  
  Claims an explicit polynomial-time computable function that needs $2^{\omega(\sqrt{n})}$ gates in depth-three circuits, past a long-standing barrier for circuit lower bounds (openai/math family 112).
<!-- END:backlog -->
