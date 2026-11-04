#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png

Computed: `components` (how many independent numbers the full curvature, the Ricci
curvature and the scalar curvature carry at a point, by dimension) and `sphere`
(a round four-sphere under Ricci flow, from the exact solution). `bubble`, `rates`
(power laws compared with Wang's restriction), `tree` and `timeline` are labelled
diagrams or schematics, marked as such on the figures.
"""

from __future__ import annotations

import numpy as np
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch  # noqa: E402

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
        "lines.solid_capstyle": "round", "legend.frameon": False, "axes.axisbelow": True,
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

def counts(n: int):
    rm = n * n * (n * n - 1) // 12          # independent components of the Riemann tensor
    ric = n * (n + 1) // 2                   # of the (symmetric) Ricci tensor
    return rm, min(ric, rm), 1


def fig_components():
    ns = np.arange(2, 9)
    rm, ric, r = zip(*(counts(int(n)) for n in ns))
    assert counts(4) == (20, 10, 1) and counts(3) == (6, 6, 1) and counts(2) == (1, 1, 1)
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.2))
        ax = fig.add_axes([0.09, 0.13, 0.86, 0.64])
        w = 0.27
        ax.bar(ns - w, rm, w, color=th["s1"], label="full curvature (Riemann tensor)")
        ax.bar(ns, ric, w, color=th["s3"], label="Ricci curvature")
        ax.bar(ns + w, r, w, color=th["s2"], label="scalar curvature")
        for x, a in zip(ns, rm):
            ax.text(x - w, a * 1.12, str(a), ha="center", fontsize=9.5, color=th["ink2"])
        ax.set_yscale("log")
        ax.set_ylim(0.7, 1000)
        ax.set_xticks(ns)
        ax.set_xlabel("dimension n")
        ax.set_ylabel("independent numbers at each point")
        ax.legend(loc="upper left", fontsize=10)
        ax.annotate("dimension 4: scalar curvature\nis 1 number out of 20", xy=(4.27, 1.05), xytext=(5.0, 2.6),
                    fontsize=10.5, color=th["s2"], arrowprops=dict(arrowstyle="-|>", color=th["s2"], lw=1.4))
        title(fig, "Scalar curvature sees very little of the curvature",
              "Computed: n²(n²−1)/12 numbers for the full curvature, n(n+1)/2 for Ricci, 1 for scalar. "
              "From dimension 4 on they differ.", th)
        save(fig, "components", mode)


def fig_sphere():
    # A round 4-sphere of radius r0 under Ricci flow: r(t)^2 = r0^2 - 6 t  (Ric = 3/r^2 g in dimension 4).
    r0 = 1.0
    T = r0 ** 2 / 6
    t = np.linspace(0, T * 0.985, 400)
    r2 = r0 ** 2 - 6 * t
    R = 12 / r2                       # scalar curvature n(n-1)/r^2
    Rm = 1 / r2                       # every sectional curvature equals 1/r^2
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.0))
        ax = fig.add_axes([0.09, 0.13, 0.58, 0.64])
        ax.semilogy(t / T, R, color=th["s2"], label="scalar curvature R = 12 / r²")
        ax.semilogy(t / T, Rm, color=th["s1"], label="each sectional curvature = 1 / r²")
        ax.set_xlabel("time, as a fraction of the extinction time T = r₀² / 6")
        ax.set_ylabel("curvature")
        ax.legend(loc="upper left", fontsize=10)
        ax2 = fig.add_axes([0.71, 0.15, 0.27, 0.6])
        ax2.axis("off")
        ax2.set_xlim(-1.2, 1.2)
        ax2.set_ylim(-1.2, 1.2)
        ax2.set_aspect("equal")
        for k, f in enumerate((0.0, 0.5, 0.8, 0.95)):
            rr = np.sqrt(1 - f)
            ax2.add_patch(Circle((0, 0), rr, fc="none", ec=th["s1"], lw=2, alpha=1 - 0.2 * k))
        ax2.text(0, -1.18, "radius shrinks to 0", ha="center", fontsize=10, color=th["ink2"])
        title(fig, "A shrinking sphere: scalar and full curvature blow up together",
              "Computed from the exact solution r(t)² = r₀² − 6t for a round 4-sphere. Here bounded R would mean "
              "bounded curvature.", th)
        save(fig, "sphere", mode)


def fig_bubble():
    """Schematic: a Ricci-flat bubble of size a. Its scalar curvature is 0, its full curvature ~ 1/a^2."""
    a = np.array([1.0, 0.5, 0.25])
    r = np.linspace(0, 3, 400)
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.0))
        ax = fig.add_axes([0.09, 0.13, 0.86, 0.64])
        for k, ak in enumerate(a):
            prof = (1 / ak ** 2) / (1 + (r / ak) ** 2) ** 3          # a bump of height 1/a^2 and width a
            ax.plot(r, prof, color=[th["s1"], th["s4"], th["s2"]][k], label=f"full curvature, bubble size a = {ak}")
        ax.plot(r, 0 * r, color=th["s3"], lw=3, label="scalar curvature: 0 for every a")
        ax.set_xlabel("distance from the bubble's centre")
        ax.set_ylabel("curvature (schematic)")
        ax.set_ylim(-1, 17)
        ax.legend(loc="upper right", fontsize=10)
        title(fig, "The danger: a shrinking Ricci-flat bubble",
              "Schematic. A Ricci-flat piece has zero scalar curvature, yet its full curvature grows like 1/a² as "
              "its size a shrinks.", th)
        save(fig, "bubble", mode)


def fig_rates():
    s = np.logspace(-4, 0, 300)            # s = T - t
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.2))
        ax = fig.add_axes([0.09, 0.13, 0.6, 0.64])
        ax.loglog(s, 1 / s, color=th["s1"], label="(T − t)⁻¹: Type I rate")
        ax.loglog(s, 1 / s ** 2, color=th["muted"], ls="--", label="(T − t)⁻²: Wang's threshold")
        for lam, c in [(3, th["s4"]), (5, th["s2"])]:
            ax.loglog(s, 1 / s ** lam, color=c, label=f"(T − t)^−{lam}: faster Type II")
        ax.axhline(1, color=th["s3"], lw=3, label="bounded scalar curvature")
        ax.invert_xaxis()
        ax.set_ylim(0.3, 1e12)
        ax.set_xlabel("time left before the singularity, T − t")
        ax.set_ylabel("largest full curvature")
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=10)
        title(fig, "With bounded scalar curvature, blowup must be fast",
              "Illustrative power laws. Wang (2012): bounded R forces |Rm| ≥ c (T − t)⁻² at some late times; "
              "the counterexample's λ can be any of an unbounded set.", th)
        save(fig, "rates", mode)


def fig_tree():
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.2))
        ax = fig.add_axes([0.02, 0.02, 0.96, 0.8])
        ax.axis("off")
        ax.set_xlim(-5, 5)
        ax.set_ylim(-2.6, 2.6)
        ax.set_aspect("equal")
        ax.add_patch(Circle((0, 0), 2.4, fc="none", ec=th["s3"], lw=2, ls="--"))
        ax.text(2.0, 2.0, "collar at b = N·a", color=th["s3"], fontsize=11)
        ax.add_patch(Circle((0, 0), 1.2, fc=th["mid"], ec=th["s1"], lw=2.5))
        ax.text(0, 1.35, "outermost Ricci-flat piece, size a", ha="center", color=th["s1"], fontsize=11)
        for (x, y, rr) in [(-0.45, -0.2, 0.33), (0.5, 0.15, 0.22), (0.35, -0.55, 0.12)]:
            ax.add_patch(Circle((x, y), rr, fc=th["surface"], ec=th["s4"], lw=2))
        ax.add_patch(Circle((-0.5, -0.25), 0.1, fc=th["surface"], ec=th["s2"], lw=1.6))
        ax.text(-3.2, -1.6, "smaller pieces inside\n(any number of levels)", color=th["s4"], fontsize=10.5,
                ha="center")
        ax.annotate("", xy=(-0.55, -0.35), xytext=(-2.6, -1.25),
                    arrowprops=dict(arrowstyle="-|>", color=th["s4"], lw=1.4))
        ax.text(3.6, -1.7, "outside: nearly flat,\nreplaced by a flat end", color=th["ink2"], fontsize=10.5,
                ha="center")
        title(fig, "Zooming into a would-be singularity: a tree of Ricci-flat pieces",
              "A labelled diagram after Figure 1 of the four-dimensional paper. The proof shows the outermost "
              "size a cannot shrink.", th)
        save(fig, "tree", mode)


def fig_timeline():
    events = [(1982, "Hamilton\nintroduces\nRicci flow"), (2003, "Perelman:\nPoincaré via\nRicci flow"),
              (2005, "Šešum: bounded\nRicci curvature\nis enough"), (2012, "Wang: bounded R\nforces fast\nblowup"),
              (2017, "Bamler–Zhang:\nestimates under\nbounded R"), (2019, "Stolarski: fast\nconical\nsingularities"),
              (2026, "OpenAI: yes in\n4D, no in high\ndimension (claimed)")]
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
        title(fig, "Does scalar curvature detect Ricci-flow singularities?", "Evenly spaced steps, not to scale.",
              th)
        save(fig, "timeline", mode)


def main():
    fig_components()
    fig_sphere()
    fig_bubble()
    fig_rates()
    fig_tree()
    fig_timeline()


if __name__ == "__main__":
    main()
