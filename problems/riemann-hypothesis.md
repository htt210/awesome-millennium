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

- **Zero-free regions.** Classical results (de la Vallée Poussin, Vinogradov–Korobov) exclude zeros only in regions that shrink toward $\operatorname{Re}(s) = 1$. A *zero-free half-plane* $\operatorname{Re}(s) \gt \sigma_0$ for some fixed $\sigma_0 \lt 1$ — the "quasi-Riemann hypothesis" — would already be a historic advance.
- **Generalized RH** extends the question to Dirichlet $L$-functions and beyond; Landau–Siegel zeros are the main obstruction in that setting.

## Explained here

<!-- BEGIN:papers -->
_No explainers yet — see the queue below._
<!-- END:papers -->

## Queue

Papers we plan to explain next. Their claims have **not** been reviewed here yet.

<!-- BEGIN:backlog -->
- **[The Quasi-Riemann Hypothesis: a zero-free half-plane](https://github.com/openai/math/blob/main/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/paper.pdf)** — OpenAI, 2026-09-30 · *partial*  
  Claims that every Dirichlet $L$-function, including $\zeta(s)$, has no zeros with $\operatorname{Re}(s) \gt 7/8$ (openai/math family 003; a companion gives a different proof for $\operatorname{Re}(s) \gt 11/12$).
<!-- END:backlog -->
