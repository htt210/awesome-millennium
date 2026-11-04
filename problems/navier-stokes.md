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
### Claimed resolutions

*Papers that claim to settle the problem as stated by the Clay Institute.*

| Date | Paper | Status |
|---|---|---|
| 2026-09-08 | **[Finite Time Blowup for Navier–Stokes](../papers/2026/09/navier-stokes-blowup/)**<br>OpenAI — For every viscosity, a smooth force that is switched on for a while drives a fluid starting at rest to unbounded speed at time 1 with bounded energy, which would settle the Clay problem through its breakdown alternatives (C) and (D). | Preprint · Formalized (Lean 4) · Under examination |

- *Navier–Stokes blowup*: Claims breakdown alternatives (C) and (D) of the official problem, which allow a smooth, decaying force. Whether flows with no force can break down stays open. The Clay Institute has not ruled.

### Adjacent results

*Papers that settle a closely related question in the problem's landscape without deciding it.*

| Date | Paper | Status |
|---|---|---|
| 2026-09-27 | **[Universal Computation with Eventually Stationary Navier–Stokes Forcing](../papers/2026/09/navier-stokes-universal-computation/)**<br>OpenAI — For any Turing machine and input, an explicit smooth force, constant after time 1, makes a viscous fluid starting at rest carry one particle into a fixed region exactly when the machine halts. | Preprint · Not formalized · Not yet examined |

- *Navier–Stokes flows that compute*: The flows stay smooth for all time, so it says nothing about blowup. It makes precise the "fluid computer" idea that Tao proposed as one route toward blowup, for forced flows on the flat torus.
<!-- END:papers -->

## Queue

Papers we plan to explain next. Their claims have **not** been reviewed here yet.

<!-- BEGIN:backlog -->
_Nothing queued._
<!-- END:backlog -->
