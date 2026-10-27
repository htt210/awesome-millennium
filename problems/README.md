# The Millennium Prize Problems

In 2000 the [Clay Mathematics Institute](https://www.claymath.org/millennium-problems/) named seven problems and offered US$1 million for the solution of each. One has been solved.

| Problem | Area | Page |
|---|---|---|
| P vs NP | Theoretical computer science | [p-vs-np.md](p-vs-np.md) |
| Riemann Hypothesis | Analytic number theory | [riemann-hypothesis.md](riemann-hypothesis.md) |
| Yang–Mills Existence and Mass Gap | Mathematical physics | [yang-mills.md](yang-mills.md) |
| Navier–Stokes Existence and Smoothness | Partial differential equations | [navier-stokes.md](navier-stokes.md) |
| Hodge Conjecture | Algebraic geometry | [hodge-conjecture.md](hodge-conjecture.md) |
| Birch and Swinnerton-Dyer Conjecture | Arithmetic geometry | [birch-swinnerton-dyer.md](birch-swinnerton-dyer.md) |
| Poincaré Conjecture (solved) | Geometric topology | [poincare-conjecture.md](poincare-conjecture.md) |

Each page states the problem, sketches its landscape, and lists — automatically, from the papers' metadata — every explainer in this repository that bears on it:

- **resolves** — the paper claims to settle the problem as the Clay Institute states it;
- **partial** — it proves a special case or a significant piece of it;
- **adjacent** — it settles a closely related question in the problem's landscape (for example, refuting the Exponential Time Hypothesis is adjacent to P vs NP: it does not decide it).

The problem registry the catalog tool validates against is [`problems.yaml`](problems.yaml). Under the Clay rules a solution must appear in a qualifying outlet and have general acceptance two years after publication; this repository only records claims and their verification status.
