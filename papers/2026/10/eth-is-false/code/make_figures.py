#!/usr/bin/env python3
"""Generate the figures of the explainer (light and dark variants) and the
CSV tables behind them.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png and ../figures/data/*.csv

Every number plotted here is computed from the paper's formulas or from the
toy implementation in toy_eth.py; nothing is hand-entered except the running
times of earlier algorithms, which are quoted from the paper's related-work
section.
"""

from __future__ import annotations

import csv
import itertools
import math
import random
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

import toy_eth as T  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "figures"
DATA = OUT / "data"

# Validated palette (dataviz reference instance): categorical slots 1-3 + chrome.
THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834", s3="#1baf7a",
                  mid="#f0efec", red="#e34948"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926", s3="#199e70",
                 mid="#383835", red="#e66767"),
}

# Best earlier 3-SAT bounds quoted in the paper (Section 1.1.1).
PPSZ_BEST = (1.307031578, "best earlier 3-SAT algorithm, randomized: $1.307^n$ (Jiang–Cai 2026)")
LAMBDA0 = 10_909_384_704  # toy_eth.galactic_threshold(); asserted below


def setup(theme: dict, size=(10, 5.4)):
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12, "mathtext.fontset": "dejavusans",
        "axes.edgecolor": theme["axis"], "axes.labelcolor": theme["ink2"],
        "xtick.color": theme["muted"], "ytick.color": theme["muted"],
        "text.color": theme["ink"], "axes.facecolor": theme["surface"],
        "figure.facecolor": theme["surface"], "savefig.facecolor": theme["surface"],
        "axes.grid": True, "grid.color": theme["grid"], "grid.linewidth": 0.8, "grid.linestyle": "-",
        "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2,
        "lines.solid_capstyle": "round", "lines.solid_joinstyle": "round",
    })
    return plt.figure(figsize=size, dpi=160)


def title(fig, text: str, sub: str, theme: dict):
    fig.text(0.012, 0.975, text, fontsize=16, fontweight="bold", color=theme["ink"], va="top")
    fig.text(0.012, 0.915, sub, fontsize=11, color=theme["ink2"], va="top")


def save(fig, name: str, mode: str):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}-{mode}.png")
    plt.close(fig)


def write_csv(name: str, header: list[str], rows: list[list]):
    DATA.mkdir(parents=True, exist_ok=True)
    with (DATA / f"{name}.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


# ---------------------------------------------------------------------------
# 1-2. The explicit running-time bound of the technique overview
# ---------------------------------------------------------------------------

def binary_entropy(a: float) -> float:
    return 0.0 if a in (0.0, 1.0) else -a * math.log2(a) - (1 - a) * math.log2(1 - a)


def cost_terms(lam: int) -> tuple[float, float, float]:
    """Exponent per variable of the three costs in (2.11), with the explicit
    parameters (2.19), for n = 2^lam.

    Taylor data: sum_{j<=q} 2^j C(n,j) with q/n -> a = 3R/Q grows like
    2^{n (a + H(a))} for a < 2/3 and like 3^n otherwise.  Measurement tuples:
    (2D+1)^{2 tau n}.  One group: 2^{2n/r}.  Polynomial factors are ignored."""
    p = T.overview_parameters(lam)
    r, Q, R = p["r"], p["Q"], p["R"]
    a = 3 * R / Q
    taylor = a + binary_entropy(a) if a < 2 / 3 else math.log2(3)
    tau = 1 / (r * lam)
    log2_D = 2 * Q * math.log2(r)
    measurements = 2 * tau * (log2_D + 1)  # log2(2D+1) = log2 D + 1 + o(1)
    groups = 2 / r
    return taylor, measurements, groups


def crossing(target: float) -> float:
    lo, hi = float(LAMBDA0), 1e40
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if sum(cost_terms(int(mid))) < target:
            hi = mid
        else:
            lo = mid
    return hi


def sci(x: float) -> str:
    e = int(math.floor(math.log10(x)))
    return rf"{x / 10**e:.1f}\times 10^{{{e}}}"


def fig_exponent():
    xs = [10 ** (9 + i / 200) for i in range(0, 7 * 200 + 1)]
    bound = [1.0 if x < LAMBDA0 else sum(cost_terms(int(x))) for x in xs]
    ppsz = math.log2(PPSZ_BEST[0])
    x_brute, x_ppsz = crossing(1.0), crossing(ppsz)
    write_csv("exponent", ["log2_n", "taylor", "measurements", "groups", "total"],
              [[f"{x:.6g}", *(f"{c:.6g}" for c in cost_terms(int(x))), f"{sum(cost_terms(int(x))):.6g}"]
               for x in xs[::50] if x >= LAMBDA0])
    for mode, th in THEMES.items():
        fig = setup(th)
        ax = fig.add_axes([0.08, 0.13, 0.66, 0.70])
        ax.set_xscale("log")
        ax.axhline(1.0, color=th["muted"], lw=2)
        ax.axhline(ppsz, color=th["s2"], lw=2)
        ax.plot(xs, bound, color=th["s1"], lw=2.4)
        ax.axvline(LAMBDA0, color=th["axis"], lw=1)
        for x, y in ((x_brute, 1.0), (x_ppsz, ppsz)):
            ax.plot([x], [y], "o", ms=9, color=th["s1"], mec=th["surface"], mew=2, zorder=5)
        ax.annotate(rf"engages at $\log_2 n \approx {sci(LAMBDA0)}$" + "\n(smaller $n$: exhaustive search)",
                    (LAMBDA0, 1.53), xytext=(2.0e11, 1.40), fontsize=10.5, color=th["ink2"],
                    arrowprops=dict(arrowstyle="-", color=th["axis"], lw=1))
        ax.annotate(rf"beats $2^n$ once $\log_2 n \gtrsim {sci(x_brute)}$", (x_brute, 1.0),
                    xytext=(x_brute * 2.2, 1.12), fontsize=10.5, color=th["ink2"],
                    arrowprops=dict(arrowstyle="-", color=th["axis"], lw=1))
        ax.annotate(rf"beats $1.307^n$ once $\log_2 n \gtrsim {sci(x_ppsz)}$", (x_ppsz, ppsz),
                    xytext=(x_ppsz * 2.2, 0.62), fontsize=10.5, color=th["ink2"],
                    arrowprops=dict(arrowstyle="-", color=th["axis"], lw=1))
        ax.set_xlim(1e9, 1e16)
        ax.set_ylim(0, 1.65)
        ax.set_xlabel(r"$\log_2 n$   ($n$ = number of variables)")
        ax.set_ylabel(r"exponent per variable, $\log_2(\mathrm{time})/n$")
        # direct labels at the right edge; legend-equivalent since every line is labeled
        lab = dict(fontsize=10.5, va="center", color=th["ink"], clip_on=False)
        ax.text(1.35e16, sum(cost_terms(int(1e16))) + 0.03, "this paper's proved bound\n(Sec. 2, explicit parameters)", **lab)
        ax.text(1.35e16, 1.0, "exhaustive search, $2^n$", **lab)
        ax.text(1.35e16, ppsz + 0.02, "best earlier 3-SAT algorithm\n$1.307^n$ (randomized)", **lab)
        for y, c in ((sum(cost_terms(int(1e16))) + 0.03, th["s1"]), (1.0, th["muted"]), (ppsz + 0.02, th["s2"])):
            ax.plot([1.04e16], [y], "s", ms=7, color=c, clip_on=False)
        title(fig, "When does the explicit construction beat brute force?",
              "Bounded-occurrence 3-CNF; the paper's cost formula (2.11) with its explicit parameters (2.19); polynomial factors ignored",
              th)
        save(fig, "exponent", mode)
    return x_brute, x_ppsz


def fig_costs():
    xs = [10 ** (math.log10(LAMBDA0) + i / 100) for i in range(0, 600)]
    terms = [cost_terms(int(x)) for x in xs]
    names = ["Taylor data", "measurement tuples", "one group"]
    for mode, th in THEMES.items():
        fig = setup(th)
        ax = fig.add_axes([0.09, 0.13, 0.66, 0.70])
        ax.set_xscale("log")
        ax.set_yscale("log")
        colors = [th["s1"], th["s2"], th["s3"]]
        for k, (name, c) in enumerate(zip(names, colors)):
            ys = [t[k] for t in terms]
            ax.plot(xs, ys, color=c)
            ax.plot([1.04 * xs[-1]], [ys[-1]], "s", ms=7, color=c, clip_on=False)
            ax.text(1.35 * xs[-1], ys[-1], name, fontsize=11, va="center", color=th["ink"], clip_on=False)
        ax.set_xlim(LAMBDA0, xs[-1])
        ax.set_ylim(1e-9, 3)
        ax.set_xlabel(r"$\log_2 n$")
        ax.set_ylabel("exponent per variable")
        title(fig, "The three costs, per variable",
              r"Taylor data $\Sigma_{j\leq q}\,2^j\binom{n}{j}$  ·  measurements $(2D+1)^{2\tau n}$  ·  one group $2^{2n/r}$ — all three tend to 0",
              th)
        save(fig, "costs", mode)


# ---------------------------------------------------------------------------
# 3. The spectrum trick: interpolate (-1)^j on an interval near Qp
# ---------------------------------------------------------------------------

def fig_spectrum():
    Q, r, R = 400, 8, 50
    p = (r - 1) / (2 * r)
    a0 = math.floor(Q * p - (R - 1) / 2)
    interval = range(a0, a0 + R)
    pmf = [math.comb(Q, j) * p**j * (1 - p) ** (Q - j) for j in range(Q + 1)]
    measured = sum(pmf[j] for j in range(Q + 1) if j not in interval)
    write_csv("spectrum", ["j", "fraction_of_directions", "in_interval"],
              [[j, f"{pmf[j]:.6g}", j in interval] for j in range(Q + 1) if pmf[j] > 1e-9])
    # small interpolation example
    I = list(range(4, 10))

    def f(x: float) -> float:
        tot = 0.0
        for i in I:
            term = (-1.0) ** i
            for k in I:
                if k != i:
                    term *= (x - k) / (i - k)
            tot += term
        return tot

    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.0))
        ax = fig.add_axes([0.06, 0.14, 0.52, 0.66])
        ax.set_axisbelow(True)
        lo, hi = 130, 222
        for j in range(lo, hi):
            c = th["s1"] if j in interval else th["s2"]
            ax.bar(j, pmf[j] * 100, width=0.62, color=c, linewidth=0)
        ax.set_xlim(lo, hi)
        ax.set_ylim(0, max(pmf) * 100 * 1.25)
        ax.set_xlabel(r"$j$ = number of antisymmetric factors of a basis vector")
        ax.set_ylabel("% of basis vectors")
        ax.text(a0 + R / 2, max(pmf) * 100 * 1.13, rf"interval $\mathcal{{I}}$ of $R={R}$ values: $M_0$ fixes these",
                ha="center", fontsize=10.5, color=th["ink2"])
        ax.text(132, max(pmf) * 100 * 0.70, f"orange tails are measured:\n{measured * 100:.1f}% of directions",
                fontsize=10.5, color=th["ink2"])
        ax.set_title(rf"(a)  $j\sim\mathrm{{Bin}}(Q,p)$,  $Q={Q}$, $r={r}$, $p=\frac{{r-1}}{{2r}}$",
                     fontsize=12, color=th["ink"], loc="left")
        ax2 = fig.add_axes([0.66, 0.14, 0.32, 0.66])
        xs = [2.6 + i * 0.01 for i in range(int((10.4 - 2.6) / 0.01) + 1)]
        ax2.plot(xs, [f(x) for x in xs], color=th["s1"])
        ax2.plot(I, [(-1) ** i for i in I], "o", ms=9, color=th["s2"], mec=th["surface"], mew=2, zorder=5)
        ax2.axhline(0, color=th["axis"], lw=1)
        ax2.set_ylim(-7, 7)
        ax2.set_xlim(2.6, 10.4)
        ax2.set_xlabel(r"$j$")
        ax2.set_title(r"(b)  $\deg f\leq R-1$ and $f(j)=(-1)^j$ on $\mathcal{I}$", fontsize=12,
                      color=th["ink"], loc="left")
        ax2.text(6.5, 5.4, r"$f$ (here $R=6$)", fontsize=10.5, color=th["ink2"], ha="center")
        title(fig, "Why only a few directions need measuring",
              r"$M_0=V_0f(W_0)$ acts on each joint eigenvector by $(-1)^jf(j)$: equal to 1 on $\mathcal{I}$, so $I-M_0$ only sees the tails",
              th)
        save(fig, "spectrum", mode)
    return measured


# ---------------------------------------------------------------------------
# 4. The matrix M_0 and the measured part I - M_0 for r = 2, Q = 3, R = 2
# ---------------------------------------------------------------------------

def fig_m0():
    params = T.Params(2, 3, 2)
    labels = list(T.all_labels(params))
    index = {u: i for i, u in enumerate(labels)}
    D = len(labels)
    M = [[0.0] * D for _ in range(D)]
    for u in labels:
        for w, (c, _) in T.m0_row(params, u).items():
            M[index[u]][index[w]] = float(c)
    IM = [[(1.0 if i == j else 0.0) - M[i][j] for j in range(D)] for i in range(D)]
    nnz = sum(1 for row in M for v in row if v)
    write_csv("m0", ["row", "col", "M0", "I_minus_M0"],
              [[i, j, M[i][j], IM[i][j]] for i in range(D) for j in range(D) if M[i][j] or IM[i][j]])
    stats = T.check_matrix(params)
    for mode, th in THEMES.items():
        cmap = LinearSegmentedColormap.from_list("div", [th["s1"], th["mid"], th["red"]])
        fig = setup(th, size=(11, 5.6))
        vmax = max(abs(v) for row in M + IM for v in row)
        for k, (mat, name) in enumerate(((M, r"(a)  $M_0$"), (IM, r"(b)  $I-M_0$  (rank 10)"))):
            ax = fig.add_axes([0.04 + k * 0.47, 0.06, 0.40, 0.74])
            ax.imshow(mat, cmap=cmap, vmin=-vmax, vmax=vmax, interpolation="nearest")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(False)
            for side in ax.spines.values():
                side.set_visible(True)
                side.set_color(th["axis"])
            ax.set_title(name, fontsize=12, color=th["ink"], loc="left")
        cax = fig.add_axes([0.92, 0.18, 0.012, 0.5])
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(-vmax, vmax))
        cb = fig.colorbar(sm, cax=cax)
        cb.outline.set_visible(False)
        cb.ax.tick_params(colors=th["muted"], labelsize=9)
        title(fig, r"The auxiliary matrix for $r=2$, $Q=3$, $R=2$ ($D=r^{2Q}=64$)",
              f"(a) {nnz} nonzeros: each row only reaches indices obtained by swapping pairs.  "
              f"(b) the correction is a combination of {stats['measured']} measurements",
              th)
        save(fig, "m0", mode)
    return nnz, stats


# ---------------------------------------------------------------------------
# 5. Hermite recovery of H(0) from Taylor data at t = 1, 2, 3
# ---------------------------------------------------------------------------

def exact_H(con) -> list[Fraction]:
    def padd(a, b):
        n = max(len(a), len(b))
        return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]

    def pmul(a, b):
        out = [Fraction(0)] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] += x * y
        return out

    total = [Fraction(0)]
    for x in itertools.product((0, 1), repeat=con.n):
        prod = [Fraction(1)]
        for e, lits in enumerate(con.clauses):
            if not lits:
                continue
            fac = [Fraction(1)]
            for v, pos in lits:
                form = [Fraction(0)]
                for var, poly in con.occ[(e, v)].coeffs.items():
                    if x[var]:
                        form = padd(form, poly)
                fac = pmul(fac, padd([Fraction(1)], [-c for c in form]) if pos else form)
            prod = pmul(prod, padd([Fraction(1)], [-c for c in fac]))
        total = padd(total, prod)
    while len(total) > 1 and total[-1] == 0:
        total.pop()
    return total


def fig_hermite():
    rng = random.Random(4)
    n = 6
    clauses = T.random_bounded_cnf(n, rng)
    params = T.Params(2, 3, 2)
    con = T.build(n, clauses, params, rng)
    H = exact_H(con)
    truth = T.brute_force_count(n, clauses)
    assert H[0] == truth
    J = con.degree_bound // params.Q + 1

    def ev(poly, x):
        return float(sum(float(c) * x**k for k, c in enumerate(poly)))

    def jet(t):  # Taylor polynomial of degree J-1 at t, as coefficients in z
        return [sum(c * math.comb(k, i) * Fraction(t) ** (k - i) for k, c in enumerate(H) if k >= i)
                for i in range(J)]

    xs = [-0.15 + i * 0.005 for i in range(int(3.5 / 0.005) + 1)]
    write_csv("hermite", ["T", "H(T)"], [[f"{x:.3f}", f"{ev(H, x):.6g}"] for x in xs[::10]])
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.4))
        ax = fig.add_axes([0.08, 0.13, 0.70, 0.70])
        for t in range(1, params.Q + 1):
            coeffs = jet(t)
            zs = [-0.32 + i * 0.01 for i in range(65)]
            ax.plot([t + z for z in zs], [ev(coeffs, z) for z in zs], color=th["s2"], lw=9, alpha=0.35,
                    solid_capstyle="round", zorder=2)
        ax.plot(xs, [ev(H, x) for x in xs], color=th["s1"], zorder=3)
        for t in range(1, params.Q + 1):
            ax.plot([t], [ev(H, t)], "o", ms=9, color=th["s2"], mec=th["surface"], mew=2, zorder=5)
        ax.plot([0], [truth], "o", ms=12, mfc=th["surface"], mec=th["s3"], mew=3, zorder=6)
        ax.annotate(r"$H(0)$ = #$F$ = " + f"{truth}\nnever evaluated directly", (0, truth),
                    xytext=(0.25, truth - 7.5), fontsize=11, color=th["ink2"],
                    arrowprops=dict(arrowstyle="-", color=th["axis"], lw=1))
        ax.set_xlim(-0.2, 3.45)
        ys = [ev(H, x) for x in xs]
        ax.set_ylim(min(ys) - 6, max(ys) + 6)
        ax.set_xlabel(r"deformation parameter $T$")
        ax.set_ylabel(r"$H(T)$")
        lab = dict(fontsize=11, va="center", color=th["ink"], clip_on=False)
        top = max(ys) + 2
        ax.plot([3.55], [top], "s", ms=7, color=th["s1"], clip_on=False)
        ax.text(3.64, top, r"$H(T)$, degree " + str(len(H) - 1), **lab)
        ax.plot([3.55], [top - 7], "s", ms=7, color=th["s2"], alpha=0.6, clip_on=False)
        ax.text(3.64, top - 7, f"computed: {J} Taylor\ncoefficients at\n$t=1,2,3$", **lab)
        title(fig, "Recovering the count from easier points",
              rf"A real $H(T)$ from the toy code ($n={n}$, $Q=3$): {params.Q}×{J} Taylor coefficients > degree bound "
              rf"{con.degree_bound}, so they pin down $H$",
              th)
        save(fig, "hermite", mode)
    return truth, len(H) - 1, J, con.degree_bound


def main():
    assert T.galactic_threshold() == LAMBDA0
    x_brute, x_ppsz = fig_exponent()
    fig_costs()
    measured = fig_spectrum()
    nnz, stats = fig_m0()
    truth, deg, J, dbound = fig_hermite()
    print(f"exponent: beats 2^n at log2 n ~ {x_brute:.3e}, beats 1.307^n at log2 n ~ {x_ppsz:.3e}")
    print(f"spectrum: measured fraction {measured:.4f}")
    print(f"m0: nnz={nnz}, measured={stats['measured']}, g={stats['eigenvalues']}")
    print(f"hermite: #F={truth}, deg H={deg}, J={J}, degree bound={dbound}")
    print(f"wrote figures to {OUT}")


if __name__ == "__main__":
    main()
