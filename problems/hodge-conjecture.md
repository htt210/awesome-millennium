# Hodge Conjecture

> **Question.** On a smooth complex projective variety, is every Hodge class a rational combination of classes of algebraic subvarieties?

**Status:** open. [Clay Mathematics Institute](https://www.claymath.org/millennium-problems/) · [official problem description (P. Deligne), in *The Millennium Prize Problems*](https://www.claymath.org/library/monographs/MPPc.pdf)

## Statement

Let $X$ be a nonsingular complex projective variety. Its rational cohomology carries the Hodge decomposition $H^{k}(X, \mathbb{C}) = \bigoplus_{p+q=k} H^{p,q}(X)$. The **Hodge classes** of degree $2p$ are

$$
\mathrm{Hdg}^{p}(X) = H^{2p}(X, \mathbb{Q}) \cap H^{p,p}(X).
$$

The Hodge conjecture asserts that every class in $\mathrm{Hdg}^{p}(X)$ is a rational linear combination of cohomology classes of algebraic subvarieties of $X$ of codimension $p$.

## The landscape

- Known for $p = 1$ (the Lefschetz $(1,1)$ theorem) and hence in a few low-dimensional cases.
- **Abelian varieties** — in particular those with complex multiplication (CM) — and products of K3 surfaces are the classical test cases; Weil classes on abelian varieties are a well-known source of difficulty.

## Explained here

<!-- BEGIN:papers -->
### Partial results

*Papers that prove a special case or a significant piece of the problem.*

| Date | Paper | Status |
|---|---|---|
| 2026-10-06 | **[The rational Hodge conjecture for CM abelian varieties](../papers/2026/10/hodge-cm-abelian-varieties/)**<br>OpenAI — Claims the Hodge conjecture for every complex abelian variety with complex multiplication, in every dimension and codimension, and through theorems of Milne the Tate conjecture for abelian varieties over finite fields. | Preprint · Formalized (Lean 4) · Not yet examined |

- *Hodge conjecture for CM abelian varieties*: Proves the conjecture for one important family of shapes, CM abelian varieties and their products, where exotic Hodge classes not built from divisors do occur. The conjecture for general varieties stays open.
<!-- END:papers -->

## Queue

Papers we plan to explain next. Their claims have **not** been reviewed here yet.

<!-- BEGIN:backlog -->
_Nothing queued._
<!-- END:backlog -->
