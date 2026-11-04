#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png

Computed: `game` (a small unique game and its best labeling, by brute force),
`maxcut` (the Goemans–Williamson ratio, minimized numerically, and the best cut
of a small random graph against the guarantee) and `cover` (vertex covers of
random graphs: the factor-two matching algorithm against the exact optimum).
`gap` and `timeline` are labelled diagrams.
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

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


# ---------------------------------------------------------------------------
# 1. A small unique game
# ---------------------------------------------------------------------------

def small_game(seed=4, n=6, k=4, extra=3):
    """A unique game on n vertices with labels mod k and constraints a(v) = a(u) + c (mod k).
    Start from a hidden labeling, so most constraints agree with it, then corrupt a few."""
    rng = np.random.default_rng(seed)
    hidden = rng.integers(0, k, n)
    edges = [(i, (i + 1) % n) for i in range(n)] + [(0, 3), (1, 4), (2, 5)]
    cons = []
    for t, (u, v) in enumerate(edges):
        c = (hidden[v] - hidden[u]) % k
        if t in (2, 7):            # two corrupted constraints
            c = (c + 1 + rng.integers(0, k - 1)) % k
        cons.append((u, v, int(c)))
    best, best_lab = -1, None
    for lab in itertools.product(range(k), repeat=n):
        sat = sum((lab[v] - lab[u]) % k == c for u, v, c in cons)
        if sat > best:
            best, best_lab = sat, lab
    return n, k, cons, best, best_lab


def fig_game():
    n, k, cons, best, lab = small_game()
    pos = {i: (math.cos(2 * math.pi * i / n + 0.3), math.sin(2 * math.pi * i / n + 0.3)) for i in range(n)}
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.2))
        ax = fig.add_axes([0.02, 0.04, 0.50, 0.80])
        ax.set_aspect("equal")
        ax.axis("off")
        for u, v, c in cons:
            ok = (lab[v] - lab[u]) % k == c
            (x1, y1), (x2, y2) = pos[u], pos[v]
            ax.plot([x1, x2], [y1, y2], color=th["s3"] if ok else th["red"], lw=2.4 if ok else 2.0,
                    ls="-" if ok else (0, (3, 2)), zorder=1)
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"+{c}", fontsize=10.5, ha="center", va="center",
                    color=th["ink"], bbox=dict(boxstyle="round,pad=0.15", fc=th["surface"], ec="none"), zorder=2)
        for i, (x, y) in pos.items():
            ax.add_patch(plt.Circle((x, y), 0.13, fc=th["s1"], ec=th["s1"], zorder=3))
            ax.text(x, y, str(lab[i]), ha="center", va="center", color="white", fontsize=12, fontweight="bold",
                    zorder=4)
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.35)
        ax2 = fig.add_axes([0.55, 0.08, 0.44, 0.76])
        ax2.axis("off")
        txt = (f"Each dot gets a label from 0 to {k - 1}.\nEach line says: the label at one end\nplus the "
               f"number on the line, modulo {k},\nmust equal the label at the other end.\n\n"
               "Unique: once you pick one end's label,\nthe line forces exactly one label at\nthe other end.\n\n"
               f"The best labeling here (shown, found by\ntrying all {k ** n:,}) satisfies "
               f"{best} of {len(cons)} lines.\n"
               "Green: satisfied. Red dashed: broken.")
        ax2.text(0, 1, txt, va="top", fontsize=11.5, color=th["ink2"], transform=ax2.transAxes)
        title(fig, "A unique game", "Computed: a small example and its best labeling, found by brute force.", th)
        save(fig, "game", mode)


# ---------------------------------------------------------------------------
# 2. The gap
# ---------------------------------------------------------------------------

def fig_gap():
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.4))
        ax = fig.add_axes([0.05, 0.16, 0.90, 0.62])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.grid(False)
        ax.spines["left"].set_visible(False)
        eps, delta = 0.08, 0.10
        ax.axvspan(1 - eps, 1, color=th["s3"], alpha=0.35)
        ax.axvspan(0, delta, color=th["red"], alpha=0.30)
        ax.axvspan(delta, 1 - eps, color=th["mid"], alpha=1)
        ax.text(1 - eps / 2, 0.55, "satisfiable\nformula:\nvalue at least\n1 − ε", ha="center", va="center",
                fontsize=10.5, color=th["s3"], fontweight="bold")
        ax.text(delta / 2, 0.55, "unsatisfiable\nformula:\nvalue at most\nδ", ha="center", va="center",
                fontsize=10.5, color=th["red"], fontweight="bold")
        ax.text(0.5, 0.55, "telling these two cases apart is as hard as solving 3SAT,\nso no fast algorithm "
                "can do it unless P = NP", ha="center", va="center", fontsize=12, color=th["ink2"])
        ax.set_xlabel("value of the unique game: the largest fraction of constraints a labeling can satisfy")
        ax.set_xticks([0, delta, 1 - eps, 1])
        ax.set_xticklabels(["0", "δ", "1 − ε", "1"])
        title(fig, "What the theorem says",
              "Schematic of Theorem 1.1: a fast translation turns any 3SAT formula into a unique game whose value "
              "lands in one of the two coloured zones.", th)
        save(fig, "gap", mode)


# ---------------------------------------------------------------------------
# 3. Max-Cut and the Goemans–Williamson constant
# ---------------------------------------------------------------------------

def gw_constant():
    th = np.linspace(1e-6, math.pi, 2_000_001)
    r = (th / math.pi) / ((1 - np.cos(th)) / 2)
    i = int(np.argmin(r))
    return float(r[i]), float(th[i]), th, r


def fig_maxcut():
    alpha, th_star, thetas, ratio = gw_constant()
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        ax = fig.add_axes([0.07, 0.14, 0.52, 0.64])
        ax.plot(np.degrees(thetas), ratio, color=th["s1"])
        ax.axhline(alpha, color=th["s2"], lw=1.6, ls=(0, (4, 2)))
        ax.plot([math.degrees(th_star)], [alpha], "o", color=th["s2"], ms=8)
        ax.text(math.degrees(th_star) - 4, alpha + 0.05, f"minimum ≈ {alpha:.5f}, at {math.degrees(th_star):.1f}°",
                ha="right", va="bottom", fontsize=10.5, color=th["s2"])
        ax.set_xlim(0, 180)
        ax.set_ylim(0.8, 1.6)
        ax.set_xlabel("angle between two vectors (degrees)")
        ax.set_ylabel("rounding ratio")
        ax2 = fig.add_axes([0.63, 0.12, 0.36, 0.70])
        ax2.axis("off")
        txt = ("Max-Cut: split a network's nodes into\ntwo teams to cut as many links as\npossible.\n\n"
               "Goemans and Williamson (1995) place\nthe nodes as vectors on a sphere and\ncut with a random "
               "plane. Their cut is\nalways at least this minimum ratio,\nabout 87.9%, of the best.\n\n"
               "The theorem, with Khot, Kindler,\nMossel and O'Donnell (2005), says no\nfast algorithm can "
               "promise more,\nunless P = NP.")
        ax2.text(0, 1, txt, va="top", fontsize=11, color=th["ink2"], transform=ax2.transAxes)
        title(fig, "The 87.9% barrier for Max-Cut",
              "Computed: the Goemans–Williamson ratio (θ/π) ÷ ((1 − cos θ)/2), minimized over the angle θ.", th)
        save(fig, "maxcut", mode)


# ---------------------------------------------------------------------------
# 4. Vertex Cover: factor two
# ---------------------------------------------------------------------------

def min_cover(n, edges):
    for size in range(n + 1):
        for S in itertools.combinations(range(n), size):
            s = set(S)
            if all(u in s or v in s for u, v in edges):
                return size
    return n


def matching_cover(edges, order):
    used = set()
    for t in order:
        u, v = edges[t]
        if u not in used and v not in used:
            used |= {u, v}
    return len(used)


def fig_cover(trials=400, n=12, seed=11):
    rng = np.random.default_rng(seed)
    ratios = []
    for _ in range(trials):
        p = rng.uniform(0.12, 0.45)
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
        if not edges:
            continue
        opt = min_cover(n, edges)
        mc = matching_cover(edges, rng.permutation(len(edges)))
        ratios.append(mc / opt)
    ratios = np.array(ratios)
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        ax = fig.add_axes([0.07, 0.14, 0.52, 0.64])
        ax.hist(ratios, bins=np.arange(0.975, 2.08, 0.05), color=th["s1"], alpha=0.85)
        ax.axvline(2.03, color=th["s2"], lw=2, ls=(0, (4, 2)))
        ax.text(1.98, ax.get_ylim()[1] * 0.92, "factor 2:\nthe proved\nguarantee", ha="right", va="top",
                fontsize=10.5, color=th["s2"])
        ax.set_xlabel("size of the cover found ÷ size of the smallest cover")
        ax.set_ylabel(f"number of graphs (out of {len(ratios)})")
        ax2 = fig.add_axes([0.63, 0.12, 0.36, 0.70])
        ax2.axis("off")
        txt = ("Vertex Cover: pick as few nodes as\npossible so that every link touches\none of them.\n\n"
               "A two-line algorithm (take both ends\nof a maximal set of separate links)\nis never worse than "
               "twice the best.\nOn these small random graphs it is\noften much better.\n\n"
               "The theorem, with Khot and Regev\n(2008), says no fast algorithm can\npromise any factor "
               "below 2,\nunless P = NP.")
        ax2.text(0, 1, txt, va="top", fontsize=11, color=th["ink2"], transform=ax2.transAxes)
        title(fig, "The factor-two barrier for Vertex Cover",
              f"Computed on {len(ratios)} random graphs with {n} nodes: the simple algorithm against the exact "
              "optimum, found by search.", th)
        save(fig, "cover", mode)


# ---------------------------------------------------------------------------
# 5. Timeline
# ---------------------------------------------------------------------------

def fig_timeline():
    events = [(1992, "PCP theorem:\nproofs checkable\nby spot checks"), (1995, "Goemans–Williamson:\n87.9% for\nMax-Cut"),
              (2002, "Khot states the\nUnique Games\nConjecture"), (2005, "KKMO: it would\nmake 87.9%\noptimal"),
              (2008, "Raghavendra:\nit would settle\nevery CSP"), (2018, "Khot–Minzer–Safra:\nthe 2-to-2\ntheorem"),
              (2026, "OpenAI: the\nconjecture\n(claimed)")]
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
        title(fig, "Three decades of hardness of approximation", "Evenly spaced steps, not to scale.", th)
        save(fig, "timeline", mode)


def main():
    fig_game()
    fig_gap()
    fig_maxcut()
    fig_cover()
    fig_timeline()


if __name__ == "__main__":
    main()
