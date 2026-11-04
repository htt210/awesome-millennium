#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png

Computed: `lattices` (which lattices are carried to themselves by a rotation),
`diamond` (Hodge numbers h^{p,q} = C(g,p) C(g,q) of an abelian variety) and
`balance` (the sign patterns of the paper's four-factor relation, enumerated).
`shadow`, `proof` and `timeline` are labelled diagrams.
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "figures"

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834", s3="#1baf7a", s4="#8a5cd1",
                  mid="#f0efec", red="#e34948"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926", s3="#199e70", s4="#9b74e0",
                 mid="#383835", red="#e66767"),
}


def setup(th: dict, size=(10, 5.0)):
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12, "mathtext.fontset": "dejavusans",
        "axes.edgecolor": th["axis"], "axes.labelcolor": th["ink2"],
        "xtick.color": th["muted"], "ytick.color": th["muted"],
        "text.color": th["ink"], "axes.facecolor": th["surface"],
        "figure.facecolor": th["surface"], "savefig.facecolor": th["surface"],
        "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2.4,
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


# ---------------------------------------------------------------------------
# 1. Shapes, subshapes and their shadows
# ---------------------------------------------------------------------------

def fig_shadow():
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        ax = fig.add_axes([0.02, 0.04, 0.50, 0.80])
        ax.set_aspect("equal")
        ax.axis("off")
        u = np.linspace(0, 2 * np.pi, 400)
        # a doughnut seen from slightly above: outer outline, and the hole drawn as a smile and a frown
        ax.fill(2.6 * np.cos(u), 1.35 * np.sin(u), color=th["s1"], alpha=0.12)
        ax.plot(2.6 * np.cos(u), 1.35 * np.sin(u), color=th["s1"], lw=2.2)
        t = np.linspace(0.25 * np.pi, 0.75 * np.pi, 100)
        ax.plot(1.25 * np.cos(t) / np.cos(0.25 * np.pi) * 0.95, 0.55 * (np.sin(t) - np.sin(0.25 * np.pi)) * -1 + 0.1,
                color=th["s1"], lw=2.2)
        t2 = np.linspace(0.3 * np.pi, 0.7 * np.pi, 100)
        ax.plot(0.9 * np.cos(t2) / np.cos(0.3 * np.pi) * 0.95, 0.35 * (np.sin(t2) - np.sin(0.3 * np.pi)) + 0.02,
                color=th["s1"], lw=2.2)
        # loop a: around the hole; loop b: around the tube
        ax.plot(1.85 * np.cos(u), 0.85 * np.sin(u) - 0.05, color=th["s2"], lw=2.8)
        tb = np.linspace(-np.pi / 2, np.pi / 2, 100)
        ax.plot(2.2 + 0.18 * np.cos(tb), 0.42 * np.sin(tb) - 0.05, color=th["s3"], lw=2.8)
        ax.plot(2.2 - 0.18 * np.cos(tb), 0.42 * np.sin(tb) - 0.05, color=th["s3"], lw=1.6, ls=":")
        ax.text(-1.7, 0.95, "loop a", color=th["s2"], fontsize=12, fontweight="bold")
        ax.text(2.55, 0.55, "loop b", color=th["s3"], fontsize=12, fontweight="bold")
        ax.text(0, -1.75, "two loops that cannot be shrunk: their classes record the doughnut's holes",
                ha="center", fontsize=10.5, color=th["ink2"])
        ax.set_xlim(-3.4, 3.6)
        ax.set_ylim(-2.0, 1.8)
        ax2 = fig.add_axes([0.55, 0.06, 0.44, 0.78])
        ax2.axis("off")
        lines = [("Cohomology: a list of holes", th["ink"], 13.5, "bold"),
                 ("Every shape has \"classes\" that record its holes", th["ink2"], 11.5, "normal"),
                 ("of each dimension.", th["ink2"], 11.5, "normal"),
                 ("", th["ink2"], 6, "normal"),
                 ("Any subshape cut out by equations (an", th["ink2"], 11.5, "normal"),
                 ("algebraic cycle) has a class: its shadow.", th["ink2"], 11.5, "normal"),
                 ("", th["ink2"], 6, "normal"),
                 ("Shadows of algebraic cycles always pass a", th["ink2"], 11.5, "normal"),
                 ("symmetry test: they are Hodge classes.", th["s2"], 11.5, "bold"),
                 ("", th["ink2"], 6, "normal"),
                 ("The Hodge conjecture: every rational class", th["ink2"], 11.5, "normal"),
                 ("that passes the test is a shadow of some", th["ink2"], 11.5, "normal"),
                 ("combination of algebraic cycles.", th["ink2"], 11.5, "normal")]
        y = 0.97
        for text, c, size, weight in lines:
            ax2.text(0, y, text, color=c, fontsize=size, fontweight=weight, va="top", transform=ax2.transAxes)
            y -= 0.075 if size > 7 else 0.035
        title(fig, "Shapes, their holes, and shadows",
              "Schematic. Real examples live in many complex dimensions; the doughnut is the simplest picture of a "
              "shape with holes.", th)
        save(fig, "shadow", mode)


# ---------------------------------------------------------------------------
# 2. Lattices and complex multiplication
# ---------------------------------------------------------------------------

def lattice_points(w1, w2, n=4):
    pts = []
    for a in range(-n, n + 1):
        for b in range(-n, n + 1):
            pts.append(a * w1 + b * w2)
    return np.array(pts)


def is_preserved(w1, w2, mult):
    """Does multiplying by the complex number `mult` carry the lattice Z w1 + Z w2 into itself?"""
    M = np.array([[w1.real, w2.real], [w1.imag, w2.imag]])
    for w in (w1 * mult, w2 * mult):
        c = np.linalg.solve(M, [w.real, w.imag])
        if np.max(np.abs(c - np.round(c))) > 1e-9:
            return False
    return True


def fig_lattices():
    cases = [("square lattice", 1 + 0j, 1j, 1j, "multiplying by i (a quarter turn)\nmaps it to itself: CM"),
             ("hexagonal lattice", 1 + 0j, complex(0.5, math.sqrt(3) / 2), complex(0.5, math.sqrt(3) / 2),
              "a sixth turn maps it to itself: CM"),
             ("a generic lattice", 1 + 0j, complex(0.31, 1.13), 1j,
              "no turn except a half turn\nmaps it to itself: not CM")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.9))
        for k, (name, w1, w2, mult, note) in enumerate(cases):
            ax = fig.add_axes([0.02 + 0.33 * k, 0.12, 0.30, 0.66])
            ax.set_aspect("equal")
            ax.axis("off")
            pts = lattice_points(w1, w2)
            keep = (np.abs(pts.real) < 2.2) & (np.abs(pts.imag) < 2.2)
            ax.plot(pts.real[keep], pts.imag[keep], "o", color=th["s1"], ms=5)
            rot = pts * mult
            keep2 = (np.abs(rot.real) < 2.2) & (np.abs(rot.imag) < 2.2)
            ax.plot(rot.real[keep2], rot.imag[keep2], "o", mfc="none", mec=th["s2"], ms=10, mew=1.6)
            ax.add_patch(Polygon([(0, 0), (w1.real, w1.imag), ((w1 + w2).real, (w1 + w2).imag),
                                  (w2.real, w2.imag)], closed=True, fc=th["s1"], alpha=0.15, ec=th["s1"], lw=1.6))
            ok = is_preserved(w1, w2, mult)
            ax.text(0, 2.5, name, ha="center", fontsize=12.5, color=th["ink"], fontweight="bold")
            ax.text(0, -2.75, note, ha="center", va="top", fontsize=10.5, color=th["s3"] if ok else th["red"])
            ax.set_xlim(-2.3, 2.3)
            ax.set_ylim(-3.6, 2.8)
        title(fig, "Complex multiplication, in the simplest case",
              "Computed. Blue dots: a lattice of complex numbers; orange rings: the same lattice turned. Gluing "
              "the shaded cell's opposite sides\ngives a doughnut-shaped curve; when the turn maps the lattice to "
              "itself, the curve has complex multiplication.", th)
        save(fig, "lattices", mode)


# ---------------------------------------------------------------------------
# 3. The Hodge diamond of an abelian variety
# ---------------------------------------------------------------------------

def fig_diamond(g=3):
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.4))
        ax = fig.add_axes([0.02, 0.03, 0.62, 0.82])
        ax.axis("off")
        ax.set_aspect("equal")
        for p in range(g + 1):
            for q in range(g + 1):
                h = math.comb(g, p) * math.comb(g, q)
                x, y = (q - p) * 0.9, (p + q) * 0.75
                mid = p == q
                ax.add_patch(FancyBboxPatch((x - 0.36, y - 0.27), 0.72, 0.54,
                                            boxstyle="round,pad=0.02,rounding_size=0.1",
                                            fc=th["s2"] if mid else th["mid"], ec=th["s2"] if mid else th["axis"],
                                            alpha=0.85 if mid else 1, lw=1.4))
                ax.text(x, y, str(h), ha="center", va="center", fontsize=14,
                        color="white" if mid else th["ink"], fontweight="bold" if mid else "normal")
        for k in range(2 * g + 1):
            ax.text(-(g + 1) * 0.9 - 0.3, k * 0.75, f"degree {k}", ha="right", va="center", fontsize=10,
                    color=th["muted"])
        ax.set_xlim(-(g + 1) * 0.9 - 1.6, (g + 1) * 0.9 + 0.4)
        ax.set_ylim(-0.6, 2 * g * 0.75 + 0.6)
        ax2 = fig.add_axes([0.66, 0.06, 0.33, 0.78])
        ax2.axis("off")
        txt = (f"An abelian variety of dimension {g}\nsplits its classes into pieces\nlabelled (p, q). The numbers "
               f"are\nthe sizes of the pieces:\nh(p, q) = C({g}, p) × C({g}, q).\n\n"
               "Hodge classes can only live in\nthe orange middle column, where\np = q, and only on its rational "
               "\npoints.\n\nThe conjecture says each of them\nis the shadow of an algebraic\ncycle.")
        ax2.text(0, 1, txt, va="top", fontsize=11, color=th["ink2"], transform=ax2.transAxes)
        title(fig, f"Where Hodge classes live: the Hodge diamond of an abelian {g}-fold",
              "Computed from the binomial formula for abelian varieties.", th)
        save(fig, "diamond", mode)


# ---------------------------------------------------------------------------
# 4. The four-factor relation, enumerated
# ---------------------------------------------------------------------------

def fig_balance(n=3):
    """Sign patterns v on a group of 2n embeddings, odd under complex conjugation, are determined by n signs.
    Count quadruples (v1, v2, v3, v4) with v1 + v2 = v3 + v4."""
    patterns = list(itertools.product([1, -1], repeat=n))
    quads = [(a, b, c, d) for a in patterns for b in patterns for c in patterns for d in patterns
             if all(a[i] + b[i] == c[i] + d[i] for i in range(n))]
    ex = next(q for q in quads if q[0] != q[2] and q[0] != q[3] and q[0] != q[1])
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.9))
        ax = fig.add_axes([0.03, 0.06, 0.55, 0.76])
        ax.axis("off")
        ax.set_xlim(-0.5, n + 2.5)
        ax.set_ylim(-0.8, 5.0)
        names = ["v1", "v2", "v3", "v4"]
        for row, (nm, v) in enumerate(zip(names, ex)):
            y = 4 - row - (0.5 if row >= 2 else 0)
            ax.text(-0.3, y, nm, ha="right", va="center", fontsize=13, color=th["ink"], fontweight="bold")
            for i, s in enumerate(v):
                c = th["s1"] if s > 0 else th["s2"]
                ax.add_patch(FancyBboxPatch((i + 0.1, y - 0.35), 0.8, 0.7, boxstyle="round,pad=0.02",
                                            fc=c, ec=c, alpha=0.85))
                ax.text(i + 0.5, y, "+" if s > 0 else "−", ha="center", va="center", fontsize=18, color="white",
                        fontweight="bold")
        sums_top = [ex[0][i] + ex[1][i] for i in range(n)]
        ax.text(n + 0.4, 3.5, "v1 + v2 =", va="center", fontsize=11, color=th["ink2"])
        ax.text(n + 0.4, 3.1, "(" + ", ".join(f"{s:+d}" for s in sums_top) + ")", va="center", fontsize=12,
                color=th["s3"], fontweight="bold")
        ax.text(n + 0.4, 1.0, "v3 + v4 =", va="center", fontsize=11, color=th["ink2"])
        ax.text(n + 0.4, 0.6, "(" + ", ".join(f"{s:+d}" for s in sums_top) + ")", va="center", fontsize=12,
                color=th["s3"], fontweight="bold")
        ax.plot([-0.1, n + 0.1], [2.0, 2.0], color=th["axis"], lw=1.5, ls=(0, (4, 2)))
        ax2 = fig.add_axes([0.62, 0.08, 0.37, 0.76])
        ax2.axis("off")
        txt = ("Each row is the \"type\" of a basic CM\npiece: a choice of + (holomorphic) or\n− (antiholomorphic) for "
               f"each of {n} pairs\nof directions.\n\nThe paper's key relation asks for four\npieces whose signs balance:\n"
               "v1 + v2 = v3 + v4.\n\n"
               f"With {n} pairs there are {len(patterns)} types and\n{len(quads)} balanced quadruples "
               f"(out of {len(patterns) ** 4}).\nThe paper shows every balanced\nquadruple gives an algebraic cycle.")
        ax2.text(0, 1, txt, va="top", fontsize=11, color=th["ink2"], transform=ax2.transAxes)
        title(fig, "The balance relation at the heart of the proof",
              "Computed: one balanced quadruple, and a count of all of them, for a CM field with three pairs of "
              "embeddings.", th)
        save(fig, "balance", mode)


# ---------------------------------------------------------------------------
# 5. The structure of the proof
# ---------------------------------------------------------------------------

def fig_proof():
    steps = [("1. Reduce", "every CM Hodge class is\nbuilt from four-factor\nbalanced pieces\n(Section 2)", "s1"),
             ("2. A surface", "a nonzero period on a\nsurface mapping to the\nfour pieces gives a cycle\n(Section 3)",
              "s3"),
             ("3. Theta forms", "build that surface and its\nnonzero period from theta\nfunctions on a ball "
                                "quotient\n(Section 4)", "s4"),
             ("4. Arithmetic", "show the forms come from\nthe right CM pieces, using\nFrobenius and Hecke\n"
                               "(Sections 5a to 5c)", "s2"),
             ("5. Assemble", "put it on one surface,\ncompose the pieces,\ndescend to Q\n(Section 6)",
              "s1")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.5))
        ax = fig.add_axes([0.01, 0.05, 0.98, 0.78])
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        w = 0.18
        for k, (head, body, c) in enumerate(steps):
            x = 0.01 + k * 0.198
            ax.add_patch(FancyBboxPatch((x, 0.12), w, 0.76, boxstyle="round,pad=0.005,rounding_size=0.02",
                                        fc=th["mid"], ec=th[c], lw=2))
            ax.text(x + w / 2, 0.80, head, ha="center", va="top", fontsize=12.5, color=th[c], fontweight="bold")
            ax.text(x + w / 2, 0.62, body, ha="center", va="top", fontsize=9.2, color=th["ink2"])
            if k < len(steps) - 1:
                ax.add_patch(FancyArrowPatch((x + w + 0.002, 0.5), (x + 0.198 - 0.002, 0.5), arrowstyle="-|>",
                                             mutation_scale=14, color=th["muted"], lw=1.4))
        title(fig, "How the proof is organised", "Schematic of the paper's five stages, with its section numbers.",
              th)
        save(fig, "proof", mode)


# ---------------------------------------------------------------------------
# 6. Timeline
# ---------------------------------------------------------------------------

def fig_timeline():
    events = [(1924, "Lefschetz:\ncodimension one\nis true"), (1950, "Hodge poses\nthe question"),
              (1961, "Atiyah–Hirzebruch:\nthe integer version\nis false"), (1982, "Deligne: Hodge classes\non abelian "
                                                                                "varieties are\n'absolute'"),
              (2000, "Clay prize"), (2025, "Markman: all\nabelian fourfolds"),
              (2026, "OpenAI: all CM\nabelian varieties\n(claimed)")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.6))
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
        title(fig, "Three quarters of a century of the Hodge conjecture", "Evenly spaced steps, not to scale.", th)
        save(fig, "timeline", mode)


def main():
    fig_shadow()
    fig_lattices()
    fig_diamond()
    fig_balance()
    fig_proof()
    fig_timeline()


if __name__ == "__main__":
    main()
