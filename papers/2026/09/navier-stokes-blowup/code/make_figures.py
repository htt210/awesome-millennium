#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png

Two figures use the blowup law stated in the Lean formalization
(NavierStokes/LocalAngularGrowth.lean, BaseAngularGrowth.lean): along a ray at
distance sqrt(2 X tau) from the centre, tau = 1 - t, the swirl speed behaves
like e0 * tau^-(1/2 + h) with 0 < h < 1/100. The constants e0, X and h below
are illustrative choices inside that range. Every other figure is a labelled
schematic.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "figures"

# Validated palette (same as the ETH explainer): categorical slots 1-3 + chrome.
THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834", s3="#1baf7a",
                  mid="#f0efec", red="#e34948"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926", s3="#199e70",
                 mid="#383835", red="#e66767"),
}

H = 0.005          # illustrative exponent, 0 < h < 1/100 in the formalization
SPEED_EXP = 0.5 + H


def setup(theme: dict, size=(10, 5.0)):
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12, "mathtext.fontset": "dejavusans",
        "axes.edgecolor": theme["axis"], "axes.labelcolor": theme["ink2"],
        "xtick.color": theme["muted"], "ytick.color": theme["muted"],
        "text.color": theme["ink"], "axes.facecolor": theme["surface"],
        "figure.facecolor": theme["surface"], "savefig.facecolor": theme["surface"],
        "axes.grid": True, "grid.color": theme["grid"], "grid.linewidth": 0.8,
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


# ---------------------------------------------------------------------------
# 1. The four ways to win the prize
# ---------------------------------------------------------------------------

def fig_options():
    cells = [
        ("A", "all of space", "stays smooth forever", "every smooth start,\nno force"),
        ("B", "a box that wraps around", "stays smooth forever", "every smooth start,\nno force"),
        ("C", "all of space", "breaks down", "one example;\na smooth, fading force allowed"),
        ("D", "a box that wraps around", "breaks down", "one example;\na smooth, fading force allowed"),
    ]
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.6))
        ax = fig.add_axes([0.0, 0.0, 1.0, 0.84])
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5.6)
        ax.axis("off")
        ax.text(3.4, 5.25, "all of space", ha="center", fontsize=13, color=th["ink2"])
        ax.text(7.6, 5.25, "a box that wraps around", ha="center", fontsize=13, color=th["ink2"])
        ax.text(1.05, 3.75, "Smooth\nforever", ha="center", va="center", fontsize=13, color=th["ink2"])
        ax.text(1.05, 1.45, "Breaks\ndown", ha="center", va="center", fontsize=13, color=th["ink2"])
        for k, (letter, _, _, need) in enumerate(cells):
            col, row = k % 2, k // 2
            x0, y0 = 1.5 + 4.2 * col, 2.6 - 2.3 * row
            claimed = row == 1
            ax.add_patch(FancyBboxPatch((x0 + 0.05, y0 + 0.05), 3.8, 2.0, boxstyle="round,pad=0,rounding_size=0.12",
                                        fc=th["s1"] if claimed else th["mid"], ec="none", alpha=0.18 if claimed else 1))
            if claimed:
                ax.add_patch(FancyBboxPatch((x0 + 0.05, y0 + 0.05), 3.8, 2.0,
                                            boxstyle="round,pad=0,rounding_size=0.12", fc="none", ec=th["s1"], lw=2))
            ax.text(x0 + 0.35, y0 + 1.6, f"({letter})", fontsize=18, fontweight="bold", color=th["ink"])
            ax.text(x0 + 1.95, y0 + 0.85, need, ha="center", va="center", fontsize=12, color=th["ink"],
                    linespacing=1.3)
            if claimed:
                ax.text(x0 + 3.7, y0 + 1.68, "claimed", ha="right", fontsize=11, color=th["s1"], fontweight="bold")
        title(fig, "Four ways to win the Navier–Stokes prize",
              "Proving any one of them is enough. The paper claims (C) and (D): a breakdown example, "
              "driven by a smooth force.", th)
        save(fig, "options", mode)


# ---------------------------------------------------------------------------
# 2. Speed blows up, energy stays bounded
# ---------------------------------------------------------------------------

def fig_blowup():
    ts = [0.4 + 0.5995 * i / 2000 for i in range(2001)]
    start = 0.375                       # the fluid is at rest up to t = 3/8
    def ramp(t):                        # smooth switch-on after rest (schematic)
        if t <= start:
            return 0.0
        z = (t - start) / 0.2
        return 1.0 if z >= 1 else math.exp(1 - 1 / (1 - (1 - z) ** 2)) if z > 0 else 0.0
    speed = [ramp(t) * (1 - t) ** -SPEED_EXP for t in ts]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        a1 = fig.add_axes([0.07, 0.14, 0.40, 0.66])
        a1.set_axisbelow(True)
        a1.set_yscale("log")
        a1.plot(ts, [max(s, 1e-3) for s in speed], color=th["s2"])
        a1.axvline(1.0, color=th["muted"], lw=1.2, ls=(0, (4, 3)))
        a1.text(0.985, 2.2, "time 1", ha="right", fontsize=10.5, color=th["ink2"])
        a1.set_xlim(0.35, 1.0)
        a1.set_ylim(0.5, 60)
        a1.set_xlabel("time")
        a1.set_ylabel("top speed (log scale)")
        a1.set_title("(a) speed: no limit as time approaches 1", loc="left", fontsize=12, color=th["ink"])
        a2 = fig.add_axes([0.57, 0.14, 0.40, 0.66])
        a2.set_axisbelow(True)
        energy = [ramp(t) * (1.0 - 0.15 * (1 - t) ** (0.5 - 2 * H)) for t in ts]
        a2.plot(ts, energy, color=th["s1"])
        a2.axvline(1.0, color=th["muted"], lw=1.2, ls=(0, (4, 3)))
        a2.set_xlim(0.35, 1.0)
        a2.set_ylim(0, 1.4)
        a2.set_xlabel("time")
        a2.set_ylabel("total kinetic energy")
        a2.set_title("(b) energy: stays bounded", loc="left", fontsize=12, color=th["ink"])
        title(fig, "Blowup with finite energy",
              "Shapes only. The speed law, about (1 − t) to the power −(1/2 + h) with h below 1/100, "
              "is the one stated in the formalization.", th)
        save(fig, "blowup", mode)


# ---------------------------------------------------------------------------
# 3. Why the force is not a cheat
# ---------------------------------------------------------------------------

def on(t: float, start: float = 0.375, width: float = 0.25) -> float:
    """Smooth switch from 0 (at rest until t = 3/8) to 1."""
    if t <= start:
        return 0.0
    z = min(1.0, (t - start) / width)
    a = math.exp(-1 / z) if z > 0 else 0.0
    b = math.exp(-1 / (1 - z)) if z < 1 else 0.0
    return a / (a + b)


def fig_force():
    ts = [0.0 + 1.35 * i / 1500 for i in range(1501)]
    def bump(t, a, b):
        if t <= a or t >= b:
            return 0.0
        z = (t - a) / (b - a)
        return math.exp(1 - 1 / (1 - (2 * z - 1) ** 2))
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.9))
        for k in range(2):
            ax = fig.add_axes([0.06 + 0.5 * k, 0.14, 0.41, 0.62])
            ax.set_axisbelow(True)
            ax.set_xlim(0, 1.35)
            ax.set_ylim(0, 4.2)
            ax.axvline(1.0, color=th["muted"], lw=1.2, ls=(0, (4, 3)))
            ax.text(1.02, 3.95, "time 1", fontsize=10.5, color=th["ink2"])
            ax.set_xlabel("time")
            ax.set_yticks([])
            before = [t for t in ts if t < 0.995]
            ax.plot(before, [min(4.5, 0.25 * on(t) * (1 - t) ** -SPEED_EXP) for t in before],
                    color=th["s2"], label="fluid speed")
            if k == 0:
                ax.plot(before, [min(4.5, 0.18 * on(t) * (1 - t) ** -1.6) for t in before],
                        color=th["red"], ls=(0, (5, 3)), label="force you would need")
                ax.set_title("(a) the cheat: pick a blowup, solve for the force.\n"
                             "The force blows up too — not allowed.", loc="left", fontsize=12, color=th["ink"])
            else:
                ax.plot(ts, [1.1 * bump(t, 0.38, 1.25) for t in ts], color=th["s1"], label="force")
                ax.set_title("(b) the claim: the force stays a smooth push\n"
                             "(timing illustrative); the speed still blows up.", loc="left", fontsize=12,
                             color=th["ink"])
            ax.legend(loc="upper left", frameon=False, fontsize=11)
        title(fig, "Why the force is not a cheat",
              "Shapes only. With a force you can make almost anything happen, unless the force must stay "
              "smooth at the moment of blowup.", th)
        save(fig, "force", mode)


# ---------------------------------------------------------------------------
# 4. The collapsing swirl
# ---------------------------------------------------------------------------

def fig_collapse():
    times = [0.5, 0.75, 0.9, 0.97, 0.99]
    X = 0.4
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.4))
        ax = fig.add_axes([0.03, 0.04, 0.44, 0.80])
        ax.set_aspect("equal")
        ax.set_xlim(-1.05, 1.05)
        ax.set_ylim(-1.05, 1.05)
        ax.axis("off")
        colors = [th["muted"], th["s3"], th["s1"], th["s2"], th["red"]]
        for t, c in zip(times, colors):
            r = math.sqrt(2 * X * (1 - t)) / math.sqrt(2 * X * 0.5) * 0.9
            ax.add_patch(Circle((0, 0), r, fill=False, ec=c, lw=2.4))
            ang = math.radians(35)
            p = (r * math.cos(ang), r * math.sin(ang))
            d = (-math.sin(ang), math.cos(ang))
            L = 0.04 + 0.022 * (1 - t) ** -SPEED_EXP
            ax.add_patch(FancyArrowPatch(p, (p[0] + L * d[0], p[1] + L * d[1]), arrowstyle="-|>",
                                         mutation_scale=14, color=c, lw=2))
            if t <= 0.9:
                ax.text(r * math.cos(math.radians(-25)) + 0.04, r * math.sin(math.radians(-25)), f"t = {t}",
                        fontsize=10.5, color=c, va="center")
        ax.plot([0], [0], "o", ms=6, color=th["ink"])
        ax.text(-1.04, 0.9, "innermost rings:\nt = 0.97 and 0.99", fontsize=10.5, color=th["ink2"])
        ax.text(0, -1.03, "seen from above: the ring of swirling fluid shrinks\nand spins faster (arrow length ~ speed)",
                ha="center", fontsize=11, color=th["ink2"])
        a2 = fig.add_axes([0.58, 0.16, 0.38, 0.62])
        a2.set_axisbelow(True)
        ts = [0.5 + 0.4999 * i / 1000 for i in range(1001)]
        a2.plot(ts, [math.sqrt(1 - t) / math.sqrt(0.5) for t in ts], color=th["s1"], label="size of the ring")
        a2.plot(ts, [(1 - t) ** -SPEED_EXP * 0.5 ** SPEED_EXP for t in ts], color=th["s2"], label="swirl speed")
        a2.set_yscale("log")
        a2.set_xlim(0.5, 1.0)
        a2.set_ylim(0.01, 100)
        a2.set_xlabel("time")
        a2.set_ylabel("relative to t = 0.5 (log scale)")
        a2.legend(loc="upper left", frameon=False, fontsize=11)
        title(fig, "The collapsing swirl at the core",
              "Size shrinks like the square root of the time left; speed grows a bit faster than one over that.\n"
              "Rates from the formalization; constants illustrative.", th)
        save(fig, "collapse", mode)


# ---------------------------------------------------------------------------
# 5. Repair rounds
# ---------------------------------------------------------------------------

def fig_repair():
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.0))
        ax = fig.add_axes([0.02, 0.04, 0.42, 0.80])
        ax.set_aspect("equal")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.axis("off")
        ax.add_patch(Circle((0, 0), 0.45, fc=th["s2"], ec="none", alpha=0.25))
        ax.text(0, 0, "collapsing\ncore", ha="center", va="center", fontsize=11, color=th["ink"])
        for k, (freq, amp, c) in enumerate([(8, 0.05, th["s1"]), (20, 0.03, th["s3"]), (44, 0.018, th["s2"])]):
            r0 = 0.6 + 0.14 * k
            angs = [2 * math.pi * i / 1200 for i in range(1201)]
            xs = [(r0 + amp * math.sin(freq * a)) * math.cos(a) for a in angs]
            ys = [(r0 + amp * math.sin(freq * a)) * math.sin(a) for a in angs]
            ax.plot(xs, ys, color=c, lw=1.8)
        ax.text(0, -1.06, "repair waves in the ring around the core:\neach round finer and weaker",
                ha="center", fontsize=11, color=th["ink2"])
        a2 = fig.add_axes([0.56, 0.16, 0.40, 0.62])
        a2.set_axisbelow(True)
        rounds = list(range(0, 8))
        err = [10 ** (-(k * (k + 1)) / 2.5) for k in rounds]
        a2.bar(rounds, err, width=0.6, color=th["s1"], linewidth=0)
        a2.set_yscale("log")
        a2.set_ylim(1e-24, 3)
        a2.set_xlabel("repair round")
        a2.set_ylabel("error left over (log scale)")
        a2.grid(axis="x", visible=False)
        title(fig, "Repairing the leftover error, round after round",
              "Schematic. The collapsing pattern is not an exact solution: fine waves cancel what is left,\n"
              "so that what the flow still lacks is smooth, and the force supplies exactly that.", th)
        save(fig, "repair", mode)


def main():
    fig_options()
    fig_blowup()
    fig_force()
    fig_collapse()
    fig_repair()
    print(f"wrote figures to {OUT}")


if __name__ == "__main__":
    main()
