# Birch and Swinnerton-Dyer Conjecture

> **Question.** Is the number of independent rational points on an elliptic curve encoded in the behavior of its $L$-function at $s = 1$?

**Status:** open. [Clay Mathematics Institute](https://www.claymath.org/millennium-problems/) · [official problem description (A. Wiles), in *The Millennium Prize Problems*](https://www.claymath.org/library/monographs/MPPc.pdf)

## Statement

Let $E$ be an elliptic curve over $\mathbb{Q}$. By Mordell's theorem, $E(\mathbb{Q}) \cong \mathbb{Z}^{r} \oplus T$ for a finite group $T$ (the torsion points) and a finite **rank** $r$. The conjecture asserts that

```math
r = \operatorname{ord}_{s=1} L(E, s),
```

and the refined form predicts the leading Taylor coefficient of $L(E, s)$ at $s = 1$ in terms of the regulator, the real period, the Tamagawa numbers, the torsion subgroup, and the order of the Tate–Shafarevich group $\text{Ш}(E)$ (which is conjectured to be finite).

## The landscape

- When the analytic rank is $0$ or $1$, the rank equality and the finiteness of $\text{Ш}(E)$ are known (Gross–Zagier, Kolyvagin); the full leading-term formula is known only in special cases.
- **Selmer groups** control the rank from above; "converse theorems" go from Selmer rank back to analytic rank, and are the main route to the full formula in low rank.

## Explained here

<!-- BEGIN:papers -->
### Partial results

*Papers that prove a special case or a significant piece of the problem.*

| Date | Paper | Status |
|---|---|---|
| 2026-10-07 | **[Exact Birch–Swinnerton-Dyer Formula from Low Selmer Corank](../papers/2026/10/exact-bsd-low-selmer-corank/)**<br>OpenAI — Claims the complete Birch–Swinnerton-Dyer formula, with every prime factor exact, for every elliptic curve over $\mathbb{Q}$ whose Selmer group at some prime has corank $0$ or $1$, with no further hypotheses on the curve. | Preprint · Not formalized · Not yet examined |

- *Exact BSD formula in low rank*: Settles the conjecture, including the exact leading-term formula and finiteness of the Tate–Shafarevich group, for curves of rank $0$ or $1$ in the Selmer sense. Curves of rank $2$ or more are untouched.
<!-- END:papers -->

## Queue

Papers we plan to explain next. Their claims have **not** been reviewed here yet.

<!-- BEGIN:backlog -->
_Nothing queued._
<!-- END:backlog -->
