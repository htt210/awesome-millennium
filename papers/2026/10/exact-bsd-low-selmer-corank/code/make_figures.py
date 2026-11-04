#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png

Computed from data: `chord` (rational points on y^2 + y = x^3 - x, by exact
fractions), `bsd-plot` (Birch and Swinnerton-Dyer's experiment: products of
point counts over primes, for curves of rank 0 to 3) and `cubes` (rational
solutions of x^3 + y^3 = l, found by search). `formula` and `pinch` are labelled
diagrams; `timeline` is a list of dates.
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "figures"

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834", s3="#1baf7a", s4="#8a5cd1",
                  mid="#f0efec", red="#e34948"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926", s3="#199e70", s4="#9b74e0",
                 mid="#383835", red="#e66767"),
}

# Curves y^2 + a3 y = x^3 + a2 x^2 + a4 x + a6 (Cremona labels), with their conductors and ranks.
CURVES = [("11a1", (-1, 1, -10, -20), 11, 0), ("37a1", (0, 1, -1, 0), 37, 1),
          ("389a1", (1, 1, -2, 0), 389, 2), ("5077a1", (0, 1, -7, 6), 5077, 3)]


def setup(th: dict, size=(10, 5.0)):
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12, "mathtext.fontset": "dejavusans",
        "axes.edgecolor": th["axis"], "axes.labelcolor": th["ink2"],
        "xtick.color": th["muted"], "ytick.color": th["muted"],
        "text.color": th["ink"], "axes.facecolor": th["surface"],
        "figure.facecolor": th["surface"], "savefig.facecolor": th["surface"],
        "axes.grid": True, "grid.color": th["grid"], "grid.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2.4,
        "lines.solid_capstyle": "round", "legend.frameon": False,
    })
    return plt.figure(figsize=size, dpi=160)


def title(fig, text: str, sub: str, th: dict):
    fig.text(0.012, 0.975, text, fontsize=16, fontweight="bold", color=th["ink"], va="top")
    fig.text(0.012, 0.915, sub, fontsize=11, color=th["ink2"], va="top")


def save(fig, name: str, mode: str):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}-{mode}.png")
    plt.close(fig)


def primes_upto(n: int) -> np.ndarray:
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


# ---------------------------------------------------------------------------
# exact arithmetic on y^2 + y = x^3 - x (curve 37a1)
# ---------------------------------------------------------------------------

def add(P, Q):
    """Chord-and-tangent addition on y^2 + y = x^3 - x, with exact fractions; None is the point at infinity."""
    if P is None:
        return Q
    if Q is None:
        return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and y1 + y2 + 1 == 0:
        return None
    if x1 == x2:
        lam = (3 * x1 * x1 - 1) / (2 * y1 + 1)
    else:
        lam = (y2 - y1) / (x2 - x1)
    x3 = lam * lam - x1 - x2
    y3 = -(lam * (x3 - x1) + y1) - 1
    return (x3, y3)


def fig_chord():
    P, Q = (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(0))
    R = add(P, Q)            # (1, -1)
    third = (R[0], -1 - R[1])  # the third intersection, before reflecting
    G = (Fraction(0), Fraction(0))
    mult, cur = [], None
    for n in range(1, 13):
        cur = add(cur, G)
        mult.append((n, cur))
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.4))
        ax = fig.add_axes([0.05, 0.10, 0.44, 0.70])
        roots = np.roots([4, 0, -4, 1]).real   # where the curve has a vertical tangent: 1 + 4(x^3 - x) = 0
        xs = np.sort(np.concatenate([np.linspace(-1.33, 2.6, 4000), roots, roots + 1e-9]))
        rhs = xs ** 3 - xs
        disc = 1 + 4 * rhs
        disc = np.where(np.abs(disc) < 1e-7, 0.0, disc)
        ok = disc >= 0
        yp = (-1 + np.sqrt(np.where(ok, disc, np.nan))) / 2
        ym = (-1 - np.sqrt(np.where(ok, disc, np.nan))) / 2
        ax.plot(xs, yp, color=th["s1"])
        ax.plot(xs, ym, color=th["s1"])
        ax.axhline(0, color=th["s2"], lw=1.6, ls=(0, (4, 2)))
        ax.plot([float(third[0])] * 2, [float(third[1]), float(R[1])], color=th["muted"], lw=1.4, ls=":")
        for pt, lab, c in [(P, "P", th["s2"]), (Q, "Q", th["s2"]), (third, "", th["muted"]),
                           (R, "P + Q", th["s3"])]:
            ax.plot(float(pt[0]), float(pt[1]), "o", ms=9, color=c, zorder=3)
            if lab:
                ax.text(float(pt[0]) + 0.08, float(pt[1]) - (0.35 if lab == "P + Q" else -0.15), lab,
                        color=c, fontsize=13, fontweight="bold")
        ax.set_xlim(-1.5, 2.7)
        ax.set_ylim(-3.2, 2.2)
        ax.set_aspect("equal")
        ax.set_title(r"$y^2 + y = x^3 - x$", fontsize=13, color=th["ink"], loc="left")
        ax2 = fig.add_axes([0.53, 0.10, 0.46, 0.70])
        ax2.axis("off")
        ax2.text(0, 1.0, "Adding the point (0, 0) to itself, again and again:", fontsize=12, color=th["ink"],
                 va="top", transform=ax2.transAxes)
        y = 0.88
        for n, pt in mult:
            s = "point at infinity" if pt is None else f"x = {pt[0]}"
            if len(s) > 40:
                s = s[:37] + "..."
            ax2.text(0.02, y, f"{n} × (0, 0):", fontsize=11.5, color=th["s1"], va="top", transform=ax2.transAxes)
            ax2.text(0.26, y, s, fontsize=11.5, color=th["ink2"], va="top", family="DejaVu Sans Mono",
                     transform=ax2.transAxes)
            y -= 0.066
        ax2.text(0, y - 0.03, "Every rational point is a whole-number multiple of this one:\nthe curve has rank 1. "
                 "The fractions grow very fast.", fontsize=11, color=th["ink2"], va="top", transform=ax2.transAxes)
        title(fig, "Adding points on an elliptic curve",
              "Computed with exact fractions. The line through P and Q meets the curve once more; reflecting that "
              "point gives P + Q.", th)
        save(fig, "chord", mode)


# ---------------------------------------------------------------------------
# Birch and Swinnerton-Dyer's experiment
# ---------------------------------------------------------------------------

def bsd_products(coeffs, N, X=100_000):
    a2, a3, a4, a6 = coeffs
    xs, ys = [], []
    acc = 0.0
    for p in primes_upto(X):
        p = int(p)
        if p == 2 or N % p == 0:
            continue
        x = np.arange(p, dtype=np.int64)
        v = (4 * ((x * x % p) * x % p + a2 * (x * x % p) + a4 * x + a6) + a3 * a3) % p
        sq = np.zeros(p, dtype=bool)
        sq[(x * x) % p] = True
        count = int(np.where(v == 0, 1, np.where(sq[v], 2, 0)).sum()) + 1
        acc += math.log(count / p)
        xs.append(p)
        ys.append(math.exp(acc))
    return np.array(xs), np.array(ys)


def fig_bsd_plot():
    data = [(name, rank, *bsd_products(coeffs, N)) for name, coeffs, N, rank in CURVES]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.2))
        ax = fig.add_axes([0.07, 0.12, 0.60, 0.68])
        cols = [th["muted"], th["s1"], th["s3"], th["s2"]]
        for (name, rank, xs, ys), c in zip(data, cols):
            ax.plot(np.log(xs), ys, color=c, lw=2)
            ax.text(np.log(xs[-1]) * 1.01, ys[-1], f"rank {rank}", color=c, fontsize=11, va="center",
                    fontweight="bold")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("log X (log scale), where X is the largest prime counted")
        ax.set_ylabel("product of (points mod p) / p")
        ax.set_xlim(1.0, 13.5)
        ax2 = fig.add_axes([0.72, 0.12, 0.27, 0.68])
        ax2.axis("off")
        txt = ("For each prime p, count the\nsolutions of the curve's equation\nmodulo p, and multiply the ratios\n"
               "(count / p) together.\n\nCurves with more rational points\nhave more solutions mod p, and\n"
               "the product grows like a power\nof log X: the power is the rank.\n\n"
               "Curves: 11a1, 37a1, 389a1,\n5077a1 (Cremona's labels).")
        ax2.text(0, 1, txt, va="top", fontsize=11, color=th["ink2"], transform=ax2.transAxes)
        title(fig, "The experiment behind the conjecture",
              "Computed for all primes up to 100,000, recreating the computer runs of Birch and Swinnerton-Dyer "
              "in the early 1960s.", th)
        save(fig, "bsd-plot", mode)


# ---------------------------------------------------------------------------
# The formula, labelled
# ---------------------------------------------------------------------------

def fig_formula():
    pieces = [(r"$L^{(r)}(E,1)\,/\,r!$", "the first nonzero Taylor coefficient of the\nL-function at s = 1 (r = the rank)", "s1"),
              (r"$\Omega_E$", "the real period: the size of the curve\nas a real shape", "s3"),
              (r"$\mathrm{Reg}_E$", "the regulator: how spread out the\nrational points are", "s3"),
              (r"$|\mathrm{Sha}|$", "the Tate–Shafarevich group: a hidden\nobstruction, not known to be finite", "s2"),
              (r"$\Pi\, c_\ell$", "local factors at the primes where the\ncurve goes bad", "s3"),
              (r"$|E(\mathbb{Q})_{\mathrm{tors}}|^2$", "torsion: the points that return to\nthe start when added to themselves", "s4")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.2))
        ax = fig.add_axes([0, 0, 1, 0.86])
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        formula = (r"$\frac{L^{(r)}(E,1)}{r!} \;=\; \frac{\Omega_E \cdot \mathrm{Reg}_E \cdot |\mathrm{Sha}|"
                   r" \cdot \prod_\ell c_\ell}{|E(\mathbb{Q})_{\mathrm{tors}}|^2}$")
        ax.text(0.5, 0.80, formula, fontsize=26, ha="center", va="center", color=th["ink"])
        for k, (tex, label, c) in enumerate(pieces):
            col, row = k % 3, k // 3
            x, y = 0.04 + 0.32 * col, 0.50 - 0.27 * row
            ax.add_patch(FancyBboxPatch((x, y - 0.20), 0.29, 0.22, boxstyle="round,pad=0.005,rounding_size=0.015",
                                        fc=th["mid"], ec=th[c], lw=1.6))
            ax.text(x + 0.015, y - 0.015, tex, fontsize=15, color=th[c], va="top")
            ax.text(x + 0.015, y - 0.095, label, fontsize=9.5, color=th["ink2"], va="top")
        title(fig, "The Birch–Swinnerton-Dyer formula",
              "The leading-term formula, as stated in Theorem 1.1 of the paper. Each piece is a different "
              "measurement of the same curve.", th)
        save(fig, "formula", mode)


# ---------------------------------------------------------------------------
# The squeeze
# ---------------------------------------------------------------------------

def fig_pinch():
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        ax = fig.add_axes([0.02, 0.05, 0.96, 0.78])
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        boxes = [(0.03, 0.55, "one curve, E", r"$X_p(E) \geq 0$", "single-curve inequality\n(Section 5)", "s1"),
                 (0.03, 0.10, "its twist, E^D", r"$X_p(E^D) \geq 0$", "same inequality,\napplied to the twist", "s1"),
                 (0.37, 0.32, "the pair", r"$X_p(E) + X_p(E^D) = 0$", "pair identity over an\nimaginary quadratic "
                                                                       "field\n(Sections 6 to 10)", "s3"),
                 (0.71, 0.32, "so", r"$X_p(E) = 0$", "for every odd prime p", "s2")]
        for x, y, head, formula, note, c in boxes:
            ax.add_patch(FancyBboxPatch((x, y), 0.26, 0.33, boxstyle="round,pad=0.01,rounding_size=0.02",
                                        fc=th["mid"], ec=th[c], lw=2))
            ax.text(x + 0.13, y + 0.28, head, ha="center", va="center", fontsize=11, color=th["ink2"])
            ax.text(x + 0.13, y + 0.17, formula, ha="center", va="center", fontsize=16, color=th[c])
            ax.text(x + 0.13, y + 0.06, note, ha="center", va="center", fontsize=9.5, color=th["ink2"])
        for (x0, y0), (x1, y1) in [((0.29, 0.72), (0.37, 0.55)), ((0.29, 0.27), (0.37, 0.42)),
                                   ((0.63, 0.485), (0.71, 0.485))]:
            ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=16,
                                         color=th["muted"], lw=1.6))
        title(fig, "The squeeze",
              r"Schematic. $X_p$ measures, at the prime p, how far the formula is from exact. Two numbers that "
              "are each at least zero\nand add up to zero must both be zero.", th)
        save(fig, "pinch", mode)


# ---------------------------------------------------------------------------
# Sums of two cubes
# ---------------------------------------------------------------------------

def icbrt(n: int):
    s = 1 if n >= 0 else -1
    n = abs(n)
    r = round(n ** (1 / 3))
    for c in (r - 1, r, r + 1):
        if c >= 0 and c ** 3 == n:
            return s * c
    return None


# Two primes whose smallest solutions lie outside the quick search below; found by a longer search and checked here.
KNOWN = {53: (-1819, 1872, 217), 67: (1208, 5353, 1323)}


def cube_solutions(limit=120, zmax=400):
    rows = []
    for ell in range(2, limit):
        if any(ell % q == 0 for q in range(2, int(ell ** 0.5) + 1)) or ell % 9 not in (4, 7, 8):
            continue
        if ell in KNOWN:
            x, y, z = KNOWN[ell]
            assert x ** 3 + y ** 3 == ell * z ** 3
            rows.append((ell, KNOWN[ell]))
            continue
        found = None
        for z in range(1, zmax):
            lz = ell * z ** 3
            for x in range(-6 * z, 6 * z + 1):
                y = icbrt(lz - x ** 3)
                if y is not None and math.gcd(math.gcd(abs(x), abs(y)), z) == 1:
                    found = (x, y, z)
                    break
            if found:
                break
        rows.append((ell, found))
    return rows


def frac(a, z):
    return f"{a}" if z == 1 else f"{a}/{z}"


def fig_cubes():
    rows = cube_solutions()
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.4))
        ax = fig.add_axes([0.03, 0.04, 0.94, 0.78])
        ax.axis("off")
        n = len(rows)
        half = (n + 1) // 2
        for k, (ell, sol) in enumerate(rows):
            col, row = divmod(k, half)
            x, y = 0.02 + 0.5 * col, 0.95 - row * 0.115
            ax.text(x, y, f"{ell} =", fontsize=13, color=th["s1"], fontweight="bold", va="top",
                    transform=ax.transAxes)
            if sol:
                a, b, z = sol
                s = f"({frac(a, z)})³ + ({frac(b, z)})³"
                ax.text(x + 0.07, y, s, fontsize=13, color=th["ink"], va="top", family="DejaVu Sans Mono",
                        transform=ax.transAxes)
            else:
                ax.text(x + 0.07, y, "solutions exist (by the theorem), but none\nwith denominator below 400",
                        fontsize=10.5, color=th["s2"], va="top", transform=ax.transAxes)
        title(fig, "A companion consequence: primes that are sums of two cubes",
              "Computed by search. A companion paper proves every prime that leaves remainder 4, 7 or 8 on "
              "division by 9 is a sum of two\nrational cubes. Here are the primes below 120 of that kind; some "
              "need large denominators.", th)
        save(fig, "cubes", mode)


# ---------------------------------------------------------------------------
# Timeline
# ---------------------------------------------------------------------------

def fig_timeline():
    events = [(1922, "Mordell: finitely\nmany generators"), (1965, "Birch and\nSwinnerton-Dyer:\nthe conjecture"),
              (1986, "Gross–Zagier:\nheights of\nHeegner points"), (1989, "Kolyvagin:\nrank 0 and 1\nbehave"),
              (2001, "modularity of\nevery elliptic\ncurve over Q"), (2004, "Kato; later\nSkinner–Urban:\nformula "
                                                                             "pieces"),
              (2015, "Bhargava–Shankar:\naverage rank\nis bounded"), (2026, "OpenAI: exact\nformula, low\n"
                                                                          "Selmer corank\n(claimed)")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        ax = fig.add_axes([0.03, 0.04, 0.94, 0.80])
        ax.axis("off")
        ax.set_xlim(-0.6, len(events) - 0.4)
        ax.set_ylim(-1.8, 1.6)
        ax.plot([-0.4, len(events) - 0.6], [0, 0], color=th["axis"], lw=2)
        for k, (year, text) in enumerate(events):
            up = k % 2 == 0
            ax.plot([k], [0], "o", ms=9, color=th["s2"] if year == 2026 else th["s1"], zorder=3)
            ax.plot([k, k], [0, 0.3 if up else -0.3], color=th["axis"], lw=1)
            ax.text(k, 0.4 if up else -0.4, f"{year}\n{text}", ha="center", va="bottom" if up else "top",
                    fontsize=10, color=th["ink"])
        title(fig, "A century of rational points", "Evenly spaced steps, not to scale.", th)
        save(fig, "timeline", mode)


def main():
    import sys
    if "--skip-slow" not in sys.argv:
        fig_bsd_plot()
    fig_chord()
    fig_formula()
    fig_pinch()
    fig_cubes()
    fig_timeline()


if __name__ == "__main__":
    main()
