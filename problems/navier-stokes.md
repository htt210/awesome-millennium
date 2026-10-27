# Navier–Stokes Existence and Smoothness

> **Question.** Do smooth solutions of the three-dimensional incompressible Navier–Stokes equations stay smooth forever — or can they break down?

**Status:** open according to the Clay Institute. On 2026-09-08 OpenAI [announced](https://openai.com/index/navier-stokes-solution/) a claimed proof of finite-time breakdown for the *forced* equations (alternatives (C) and (D) below); the Clay Institute [responded](https://www.claymath.org/news/navier-stokes-announcement/) that it will evaluate the claim and has not awarded the prize. See the queue below.

[Clay Mathematics Institute](https://www.claymath.org/millennium-problems/) · [official problem description (C. Fefferman), in *The Millennium Prize Problems*](https://www.claymath.org/library/monographs/MPPc.pdf)

## Statement

The equations for a velocity field $u(x,t) \in \mathbb{R}^3$ and pressure $p(x,t)$ with viscosity $\nu \gt 0$ and external force $f$ are

$$
\partial_t u + (u \cdot \nabla) u = \nu \Delta u - \nabla p + f, \qquad \nabla \cdot u = 0, \qquad u(x, 0) = u_0(x).
$$

The official problem asks for **any one** of four statements:

- **(A)** existence and smoothness for all time on $\mathbb{R}^3$ (with $f = 0$ and smooth, rapidly decaying, divergence-free $u_0$);
- **(B)** the same on the torus $\mathbb{R}^3 / \mathbb{Z}^3$;
- **(C)** breakdown on $\mathbb{R}^3$: some smooth data $u_0$ and smooth, rapidly decaying force $f$ admit no smooth, finite-energy solution for all time;
- **(D)** breakdown on $\mathbb{R}^3 / \mathbb{Z}^3$.

## Explained here

<!-- BEGIN:papers -->
_No explainers yet — see the queue below._
<!-- END:papers -->

## Queue

Papers we plan to explain next. Their claims have **not** been reviewed here yet.

<!-- BEGIN:backlog -->
- **[Finite Time Blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)** — OpenAI, 2026-09-08 · *resolves* · [announcement](https://openai.com/index/navier-stokes-solution/) · [Clay statement](https://www.claymath.org/news/navier-stokes-announcement/) · [dispute: Navier–Stokes lost in translation](https://arxiv.org/abs/2610.08144)  
  Claims, for every viscosity, a solution that starts from rest under a smooth external force and develops unbounded velocity in finite time with bounded energy — the breakdown alternatives (C) and (D). A Lean formalization was announced; whether it matches the written proof is disputed, and the Clay Institute has not ruled.
- **[Universal Computation with Eventually Stationary Navier–Stokes Forcing](https://github.com/openai/math/blob/main/preprints/Universal-Computation-with-Eventually-Stationary-Navier-Stokes-Forcing-September-27-2026/manuscript.pdf)** — OpenAI, 2026-09-27 · *adjacent*  
  Claims viscous incompressible flows, started from rest, that perform universal computation under smooth forcing: a marked particle reaches a target region exactly when a given Turing machine halts (openai/math family 376).
<!-- END:backlog -->
