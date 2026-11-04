# Riemann Hypothesis

> **Question.** Do all nontrivial zeros of the Riemann zeta function lie on the line $\operatorname{Re}(s) = \tfrac12$?

**Status:** open. [Clay Mathematics Institute description](https://www.claymath.org/millennium/riemann-hypothesis/)

## Statement

The Riemann zeta function is $\zeta(s) = \sum_{n \ge 1} n^{-s}$ for $\operatorname{Re}(s) \gt 1$, extended to a meromorphic function on $\mathbb{C}$ with a single pole at $s = 1$. Its *trivial* zeros are $s = -2, -4, -6, \dots$; all other zeros lie in the critical strip $0 \lt \operatorname{Re}(s) \lt 1$. The Riemann Hypothesis asserts that every nontrivial zero $\rho$ satisfies

$$
\operatorname{Re}(\rho) = \tfrac12 .
$$

Equivalently, the prime-counting function obeys $\pi(x) = \operatorname{Li}(x) + O\left(\sqrt{x}\log x\right)$.

## The landscape

- **Zero-free regions.** Classical results (de la Vallée Poussin, Vinogradov–Korobov) exclude zeros only in regions that shrink toward $\operatorname{Re}(s) = 1$. A *zero-free half-plane* $\operatorname{Re}(s) \gt \sigma_0$ for some fixed $\sigma_0 \lt 1$ — the "quasi-Riemann hypothesis" — would already be a historic advance. OpenAI claimed one with $\sigma_0 = 7/8$ in September 2026; it is under examination (see below).
- **Generalized RH** extends the question to Dirichlet $L$-functions and beyond; Landau–Siegel zeros are the main obstruction in that setting.

## Explained here

<!-- BEGIN:papers -->
### Partial results

*Papers that prove a special case or a significant piece of the problem.*

| Date | Paper | Status |
|---|---|---|
| 2026-09-30 | **[The Quasi-Riemann Hypothesis: a zero-free half-plane Re(s) > 7/8](../papers/2026/09/quasi-riemann-hypothesis/)**<br>OpenAI — Claims that the Riemann zeta function and every Dirichlet $L$-function have no zeros with real part above $7/8$, a fixed margin from the edge that holds at every height and for every character, which mathematicians call the quasi-Riemann hypothesis. | Preprint · Formalized (Lean 4) · Under examination |

- *Quasi-Riemann hypothesis*: Keeps every zero of zeta between real parts $1/8$ and $7/8$; the Riemann hypothesis asks for exactly $1/2$ and stays open. If right, it also removes Landau–Siegel zeros and settles Vinogradov's conjecture on the least quadratic nonresidue.
<!-- END:papers -->

## Queue

Papers we plan to explain next. Their claims have **not** been reviewed here yet.

<!-- BEGIN:backlog -->
_Nothing queued._
<!-- END:backlog -->
