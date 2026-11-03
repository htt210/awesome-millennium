#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png

`curve-flow` is computed: it runs curve-shortening flow, the one-dimensional
cousin of Ricci flow, on a wiggly closed curve (each point moves toward its
centre of curvature at a speed equal to the curvature). Every other figure is
a labelled schematic.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "figures"

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834", s3="#1baf7a",
                  mid="#f0efec", red="#e34948"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926", s3="#199e70",
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
        "lines.solid_capstyle": "round",
    })
    return plt.figure(figsize=size, dpi=160)


def title(fig, text: str, sub: str, th: dict):
    fig.text(0.012, 0.975, text, fontsize=16, fontweight="bold", color=th["ink"], va="top")
    fig.text(0.012, 0.915, sub, fontsize=11, color=th["ink2"], va="top")


def save(fig, name: str, mode: str):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}-{mode}.png")
    plt.close(fig)


def blank(ax):
    ax.set_aspect("equal")
    ax.axis("off")


# ---------------------------------------------------------------------------
# 1. The lasso test: sphere versus doughnut
# ---------------------------------------------------------------------------

def fig_loops():
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.2))
        ax = fig.add_axes([0.02, 0.06, 0.46, 0.76])
        blank(ax)
        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.35, 1.25)
        ax.add_patch(Circle((0, 0), 1.0, fc=th["mid"], ec=th["ink2"], lw=1.6))
        ax.add_patch(Ellipse((0, 0), 2.0, 0.5, fill=False, ec=th["axis"], lw=1.0, ls=(0, (3, 3))))
        for k, s in enumerate([0.9, 0.62, 0.36, 0.14]):
            cy = 0.62 - 0.0 * k
            ax.add_patch(Ellipse((0.05, cy), 1.0 * s, 0.32 * s, fill=False, ec=th["s1"],
                                 lw=2.4, alpha=1 - 0.18 * k))
        ax.plot([0.05], [0.62], "o", ms=6, color=th["s1"])
        ax.text(0, -1.25, "sphere: every loop shrinks to a point", ha="center", fontsize=12, color=th["ink"])

        ax2 = fig.add_axes([0.52, 0.06, 0.46, 0.76])
        blank(ax2)
        ax2.set_xlim(-1.6, 1.6)
        ax2.set_ylim(-1.35, 1.25)
        ax2.add_patch(Ellipse((0, 0), 2.9, 1.5, fc=th["mid"], ec=th["ink2"], lw=1.6))
        t = np.linspace(0, math.pi, 100)
        ax2.plot(0.62 * np.cos(t), -0.05 - 0.16 * np.sin(t), color=th["ink2"], lw=1.6)
        ax2.plot(0.45 * np.cos(t), -0.09 + 0.09 * np.sin(t), color=th["ink2"], lw=1.6)
        # a loop around the tube, through the hole
        ax2.add_patch(Ellipse((-0.98, 0.0), 0.34, 0.72, fill=False, ec=th["s2"], lw=2.6))
        ax2.text(-0.98, 0.52, "stuck", ha="center", fontsize=11, color=th["s2"], fontweight="bold")
        ax2.text(0, -1.25, "doughnut: a loop through the hole cannot", ha="center", fontsize=12, color=th["ink"])
        title(fig, "The lasso test",
              "Throw a loop of string on a surface and pull it tight. On a sphere it always slips off to a point; "
              "on a doughnut it can get caught.", th)
        save(fig, "loops", mode)


# ---------------------------------------------------------------------------
# 2. Gluing: circle, sphere, three-sphere
# ---------------------------------------------------------------------------

def fig_gluing():
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.6))
        rows = [("two segments,\nends glued", "a circle"), ("two discs,\nedges glued", "a sphere"),
                ("two solid balls,\nsurfaces glued", "the three-sphere")]
        for k, (src, dst) in enumerate(rows):
            ax = fig.add_axes([0.02 + 0.33 * k, 0.05, 0.30, 0.74])
            blank(ax)
            ax.set_xlim(-1.6, 1.6)
            ax.set_ylim(-1.3, 1.3)
            if k == 0:
                ax.plot([-1.2, -0.3], [0.5, 0.5], color=th["s1"], lw=4)
                ax.plot([0.3, 1.2], [0.5, 0.5], color=th["s2"], lw=4)
            else:
                fill = 0.35 if k == 2 else 0.18
                ax.add_patch(Circle((-0.75, 0.5), 0.45, fc=th["s1"], alpha=fill, ec=th["s1"], lw=2.5))
                ax.add_patch(Circle((0.75, 0.5), 0.45, fc=th["s2"], alpha=fill, ec=th["s2"], lw=2.5))
            ax.text(0, 1.15, src, ha="center", va="center", fontsize=11.5, color=th["ink2"])
            ax.add_patch(FancyArrowPatch((0, -0.05), (0, -0.55), arrowstyle="-|>", mutation_scale=16,
                                         color=th["muted"], lw=1.6))
            ax.text(0, -0.95, dst, ha="center", fontsize=14, fontweight="bold", color=th["ink"])
            if k == 2:
                ax.text(0, -1.25, "lives in four dimensions: it cannot be drawn,\nbut you could live inside one",
                        ha="center", va="center", fontsize=10, color=th["ink2"])
        title(fig, "What the three-sphere is",
              "Each line glues two copies of a filled shape along their boundaries. The third step is the "
              "three-dimensional sphere of Poincaré's question.", th)
        save(fig, "gluing", mode)


# ---------------------------------------------------------------------------
# 3. Curve-shortening flow (computed)
# ---------------------------------------------------------------------------

def curve_shortening(n=400, steps=60000, every=None):
    """Discrete curve-shortening flow: x' = curvature vector, with periodic
    resampling to equal arc length. Returns snapshots at chosen fractions of the
    time until the curve shrinks to a small size."""
    s = np.linspace(0, 2 * math.pi, n, endpoint=False)
    r = 1.0 + 0.32 * np.sin(5 * s) + 0.12 * np.cos(9 * s + 0.6)
    x = np.stack([r * np.cos(s), r * np.sin(s)], axis=1)
    snaps = [x.copy()]
    area0 = None
    t = 0.0
    for k in range(steps):
        e = np.roll(x, -1, axis=0) - x
        h = np.linalg.norm(e, axis=1).mean()
        dt = 0.2 * h * h
        lap = (np.roll(x, -1, axis=0) - 2 * x + np.roll(x, 1, axis=0)) / (h * h)
        x = x + dt * lap
        t += dt
        if k % 50 == 0:   # resample to equal arc length
            seg = np.linalg.norm(np.roll(x, -1, axis=0) - x, axis=1)
            cum = np.concatenate([[0], np.cumsum(seg)])
            target = np.linspace(0, cum[-1], n, endpoint=False)
            xx = np.concatenate([x, x[:1]])
            x = np.stack([np.interp(target, cum, xx[:, 0]), np.interp(target, cum, xx[:, 1])], axis=1)
        area = 0.5 * abs(np.sum(x[:, 0] * np.roll(x[:, 1], -1) - np.roll(x[:, 0], -1) * x[:, 1]))
        if area0 is None:
            area0 = area
        if any(abs(area - f * area0) < 0.004 * area0 for f in (0.8, 0.55, 0.3, 0.1)) and \
                (len(snaps) == 0 or abs(area - _area(snaps[-1])) > 0.05 * area0):
            snaps.append(x.copy())
        if area < 0.05 * area0:
            break
    return snaps


def _area(x):
    return 0.5 * abs(np.sum(x[:, 0] * np.roll(x[:, 1], -1) - np.roll(x[:, 0], -1) * x[:, 1]))


def fig_curve_flow():
    snaps = curve_shortening()
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.0))
        colors = [th["muted"], th["s1"], th["s3"], th["s2"], th["red"]]
        ax = fig.add_axes([0.02, 0.05, 0.45, 0.80])
        blank(ax)
        for k, x in enumerate(snaps[:5]):
            xx = np.concatenate([x, x[:1]])
            ax.plot(xx[:, 0], xx[:, 1], color=colors[k % 5], lw=2.2)
        ax.text(0, -1.55, "the same curve at five moments, all drawn to one scale", ha="center", fontsize=11,
                color=th["ink2"])
        ax2 = fig.add_axes([0.52, 0.05, 0.46, 0.80])
        blank(ax2)
        for k, x in enumerate(snaps[:5]):
            c = x.mean(axis=0)
            scale = math.sqrt(_area(snaps[0]) / _area(x))
            y = (x - c) * scale
            ax2.plot(*np.concatenate([y, y[:1]]).T, color=colors[k % 5], lw=2.2,
                     transform=ax2.transData)
        ax2.text(0, -1.55, "rescaled to the same area: the shape becomes a perfect circle", ha="center",
                 fontsize=11, color=th["ink2"])
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.7, 1.5)
        ax2.set_xlim(-1.6, 1.6)
        ax2.set_ylim(-1.7, 1.5)
        title(fig, "Smoothing a shape by its own curvature",
              "Computed: curve-shortening flow, the one-dimensional cousin of Ricci flow. Each point moves toward\n"
              "the inside of its bend, faster where the curve bends more sharply.", th)
        save(fig, "curve-flow", mode)
    return len(snaps)


# ---------------------------------------------------------------------------
# 4. Neckpinch and surgery
# ---------------------------------------------------------------------------

def dumbbell(x, neck, c=1.5, R=0.95):
    """Radius profile of a smooth dumbbell surface of revolution: a bridge that
    widens from `neck` at the middle to radius R at |x| = c, then two round bulbs."""
    a = np.abs(x)
    bulb = np.sqrt(np.clip(R * R - (a - c) ** 2, 0, None))
    bridge = neck + (R - neck) * np.sin(np.pi * np.minimum(a, c) / (2 * c)) ** 2
    return np.where(a < c, bridge, bulb)


def fig_neckpinch():
    x = np.linspace(-2.6, 2.6, 900)
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.2))
        ax = fig.add_axes([0.02, 0.08, 0.46, 0.72])
        blank(ax)
        colors = [th["muted"], th["s1"], th["s2"]]
        for neck, c in zip([0.45, 0.22, 0.02], colors):
            r = dumbbell(x, neck)
            ax.plot(x, r, color=c, lw=2.2)
            ax.plot(x, -r, color=c, lw=2.2)
        ax.annotate("neck pinches", (0, 0.03), xytext=(0.0, 1.25), ha="center", fontsize=11, color=th["ink2"],
                    arrowprops=dict(arrowstyle="-", color=th["axis"]))
        ax.text(0, -1.35, "Ricci flow: a thin neck shrinks to a point in finite time", ha="center", fontsize=11,
                color=th["ink2"])
        ax.set_xlim(-2.8, 2.8)
        ax.set_ylim(-1.5, 1.5)
        ax2 = fig.add_axes([0.52, 0.08, 0.46, 0.72])
        blank(ax2)
        r = dumbbell(x, 0.22)
        keep = np.abs(x) > 0.55
        for side in (-1, 1):
            m = keep & (np.sign(x) == side)
            ax2.plot(x[m] + side * 0.25, r[m], color=th["s1"], lw=2.2)
            ax2.plot(x[m] + side * 0.25, -r[m], color=th["s1"], lw=2.2)
            edge = side * (0.55 + 0.25)
            rr = dumbbell(np.array([0.55]), 0.22)[0]
            th_ = np.linspace(-math.pi / 2, math.pi / 2, 60)
            ax2.plot(edge - side * rr * 0.9 * np.cos(th_), rr * np.sin(th_), color=th["s3"], lw=3)
        ax2.text(0, 0.0, "cut,\ncap", ha="center", va="center", fontsize=11, color=th["s3"], fontweight="bold")
        ax2.text(0, -1.35, "surgery: cut the neck just before it pinches, glue in caps, keep flowing",
                 ha="center", fontsize=11, color=th["ink2"])
        ax2.set_xlim(-2.8, 2.8)
        ax2.set_ylim(-1.5, 1.5)
        title(fig, "Necks, and surgery",
              "Schematic. Hamilton's plan, and the step Perelman made work: when a neck is about to pinch, "
              "cut it out and cap both ends.", th)
        save(fig, "neckpinch", mode)


# ---------------------------------------------------------------------------
# 5. Extinction
# ---------------------------------------------------------------------------

def fig_extinction():
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 4.8))
        ax = fig.add_axes([0.08, 0.15, 0.86, 0.66])
        ax.set_axisbelow(True)
        segs = [(0.0, 0.32, 1.0), (0.32, 0.58, 0.78), (0.58, 0.81, 0.52), (0.81, 1.0, 0.27)]
        for k, (a, b, v0) in enumerate(segs):
            ts = np.linspace(a, b, 100)
            vs = v0 * (1 - 0.55 * (ts - a) / (b - a)) if k < 3 else v0 * np.sqrt(np.clip(1 - (ts - a) / (b - a),
                                                                                           0, None))
            ax.plot(ts, vs, color=th["s1"])
            if k < 3:
                ax.plot([b, b], [vs[-1], segs[k + 1][2]], color=th["s2"], lw=1.6, ls=(0, (3, 2)))
                ax.text(b + 0.005, (vs[-1] + segs[k + 1][2]) / 2, "surgery", fontsize=10, color=th["s2"],
                        va="center")
        ax.plot([1.0], [0.0], "o", ms=9, color=th["s3"])
        ax.text(0.985, 0.08, "extinct", ha="right", fontsize=11, color=th["s3"], fontweight="bold")
        ax.set_xlim(0, 1.08)
        ax.set_ylim(0, 1.1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel("time")
        ax.set_ylabel("total volume")
        title(fig, "Finite extinction",
              "Schematic. For a shape in which every loop shrinks, the flow with surgery dies out completely\n"
              "in finite time (Perelman's third paper).", th)
        save(fig, "extinction", mode)


# ---------------------------------------------------------------------------
# 6. Timeline
# ---------------------------------------------------------------------------

def fig_timeline():
    events = [(1904, "Poincaré asks\nthe question"), (1961, "Smale: solved in\ndimension 5 and up"),
              (1982, "Freedman: dimension 4.\nHamilton: Ricci flow.\nThurston: geometrization"),
              (2000, "Clay prize"), (2002, "Perelman's three\npapers (2002–03)"),
              (2006, "checked by several teams;\nFields Medal declined"), (2010, "Clay prize awarded,\ndeclined")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.6))
        ax = fig.add_axes([0.03, 0.06, 0.94, 0.76])
        ax.axis("off")
        ax.set_xlim(-0.6, len(events) - 0.4)
        ax.set_ylim(-1.5, 1.5)
        ax.plot([-0.4, len(events) - 0.6], [0, 0], color=th["axis"], lw=2)
        for k, (year, text) in enumerate(events):
            up = k % 2 == 0
            ax.plot([k], [0], "o", ms=9, color=th["s1"] if year < 2002 else th["s2"], zorder=3)
            ax.plot([k, k], [0, 0.35 if up else -0.35], color=th["axis"], lw=1)
            ax.text(k, 0.45 if up else -0.45, f"{int(year)}\n{text}",
                    ha="center", va="bottom" if up else "top", fontsize=10.5, color=th["ink"])
        title(fig, "A century in seven steps",
              "Evenly spaced steps, not to scale. Perelman never published in a journal; experts spent about\n"
              "three years checking his papers.", th)
        save(fig, "timeline", mode)


def main():
    fig_loops()
    fig_gluing()
    n = fig_curve_flow()
    fig_neckpinch()
    fig_extinction()
    fig_timeline()
    print(f"wrote figures to {OUT} ({n} curve snapshots)")


if __name__ == "__main__":
    main()
