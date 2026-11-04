#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png
    python make_figures.py --check    # self-test only

Computed: `machine` (a run of the two-state "busy beaver" Turing machine),
`encoding` (the same run, and a run of a machine that never halts, as points
moving in a square, under a simplified version of Moore's encoding of a tape as
two numbers), and `area` (one rule of that encoding as a map of rectangles that
keeps area). The encoding is exact: rational arithmetic, and every step is checked
against the affine map of its rectangle. `recipe` and `timeline` are labelled
diagrams.

Our encoding is simpler than the paper's (which uses gapped digits and a
reversible, history-keeping version of the machine); it shows the idea, not the
paper's construction.
"""

from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

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
        "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2.0,
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
# Turing machines
# ---------------------------------------------------------------------------
# rules: (state, symbol) -> (new state, written symbol, move in {-1, 0, +1}); "H" halts.

BUSY_BEAVER = {("A", 0): ("B", 1, +1), ("A", 1): ("B", 1, -1),
               ("B", 0): ("A", 1, -1), ("B", 1): ("H", 1, +1)}
# a machine with no halting rule: it bounces between two walls of 1s it keeps pushing outwards
FOREVER = {("A", 0): ("B", 1, -1), ("A", 1): ("A", 1, +1),
           ("B", 0): ("A", 1, +1), ("B", 1): ("B", 1, -1)}


def run(rules, steps, state="A"):
    tape, head = {}, 0
    out = [(state, dict(tape), head)]
    for _ in range(steps):
        if state == "H":
            break
        state, w, mv = rules[(state, tape.get(head, 0))]
        tape[head] = w
        head += mv
        out.append((state, dict(tape), head))
    return out


# ---------------------------------------------------------------------------
# A tape as a point of the unit square (in the spirit of Moore's generalized shifts)
# ---------------------------------------------------------------------------
# Base B = 4. Digits: blank -> 1, symbol 1 -> 2; states A -> 1, B -> 2, H -> 3.
#   X = 0.(state)(cell left of head)(next cell left)...   in base B
#   Y = 0.(cell under head)(next cell right)...           in base B
# The blank tape is 0.111... = 1/(B - 1), so every point is rational.

B = 4
SDIG = {"A": 1, "B": 2, "H": 3}
DIG = {0: 1, 1: 2}


def encode(state, tape, head, span=60):
    x = Fr(SDIG[state], B)
    for k in range(1, span):
        x += Fr(DIG[tape.get(head - k, 0)], B ** (k + 1))
    x += Fr(1, B ** (span + 1)) / (B - 1) * B        # blank tail beyond the span
    y = Fr(0)
    for k in range(span):
        y += Fr(DIG[tape.get(head + k, 0)], B ** (k + 1))
    y += Fr(1, B ** span) / (B - 1)
    return x, y


def affine_step(x, y, rules):
    """One machine step as an affine map of the point, using only its leading digits."""
    q = int(x * B)
    a = int(y * B)
    state = {v: k for k, v in SDIG.items()}[q]
    sym = {v: k for k, v in DIG.items()}[a]
    nq, w, mv = rules[(state, sym)]
    if mv == +1:      # written symbol joins the left part; the right part shifts: x shrinks by B, y grows by B
        x2 = Fr(SDIG[nq], B) + Fr(DIG[w], B * B) + (x - Fr(q, B)) / B
        y2 = B * y - a
    elif mv == -1:    # the next left cell becomes the head cell: x grows by B, y shrinks by B
        c = int((x - Fr(q, B)) * B * B)
        x2 = Fr(SDIG[nq], B) + B * (x - Fr(q, B) - Fr(c, B * B))
        y2 = Fr(c, B) + Fr(DIG[w], B * B) + (y - Fr(a, B)) / B
    else:
        x2, y2 = x - Fr(q, B) + Fr(SDIG[nq], B), y - Fr(a, B) + Fr(DIG[w], B)
    return x2, y2


def orbit(rules, steps):
    """Encoded points of a run; every step checked against the affine rectangle map."""
    pts = []
    confs = run(rules, steps)
    for k, (s, t, h) in enumerate(confs):
        p = encode(s, t, h)
        if k > 0:
            assert affine_step(*pts[-1], rules) == p
        pts.append(p)
    return confs, pts


def check():
    confs, pts = orbit(BUSY_BEAVER, 50)
    assert confs[-1][0] == "H" and len(confs) == 7 and sum(confs[-1][1].values()) == 4
    confs2, pts2 = orbit(FOREVER, 120)
    assert all(s != "H" for s, _, _ in confs2) and len(confs2) == 121
    return confs, pts, confs2, pts2


# ---------------------------------------------------------------------------
# figures
# ---------------------------------------------------------------------------

def fig_machine(confs):
    lo, hi = -3, 3
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.4))
        ax = fig.add_axes([0.08, 0.03, 0.9, 0.78])
        ax.axis("off")
        ax.set_xlim(lo - 1.6, hi + 2.0)
        ax.set_ylim(-len(confs) + 0.2, 1.0)
        for i in range(lo, hi + 1):
            ax.text(i, 0.55, str(i), ha="center", va="center", fontsize=9, color=th["muted"])
        for k, (s, tape, head) in enumerate(confs):
            yk = -k
            ax.text(lo - 1.4, yk, f"step {k}", ha="left", va="center", fontsize=10.5, color=th["ink2"])
            for i in range(lo, hi + 1):
                v = tape.get(i, 0)
                ax.add_patch(Rectangle((i - 0.45, yk - 0.38), 0.9, 0.76, fc=th["s1"] if v else th["mid"],
                                       ec=th["axis"], lw=1))
                ax.text(i, yk, str(v), ha="center", va="center", fontsize=11,
                        color="white" if v else th["ink2"])
            ax.add_patch(Rectangle((head - 0.5, yk - 0.44), 1.0, 0.88, fc="none",
                                   ec=th["red"] if s == "H" else th["s2"], lw=2.6))
            ax.text(hi + 0.7, yk, "HALT" if s == "H" else f"state {s}", ha="left", va="center", fontsize=11,
                    color=th["red"] if s == "H" else th["s2"], fontweight="bold" if s == "H" else "normal")
        title(fig, "A Turing machine: a head that reads, writes and moves",
              "Computed: the two-state 'busy beaver' run. The orange box is the head. It halts after 6 steps "
              "with four 1s.", th)
        save(fig, "machine", mode)


def draw_square(ax, th, pts, colour, halting=True, numbers=True):
    for q, lab in [(1, "A"), (2, "B"), (3, "H")]:
        for a, slab in [(1, "0"), (2, "1")]:
            fc = th["red"] if q == 3 else th["mid"]
            ax.add_patch(Rectangle((q / B, a / B), 1 / B, 1 / B, fc=fc, alpha=0.25 if q == 3 else 1,
                                   ec=th["axis"], lw=1))
            ax.text(q / B + 0.012, a / B + 0.012, f"{lab}, reads {slab}", fontsize=8.5, color=th["ink2"],
                    va="bottom")
    xs = [float(p[0]) for p in pts]
    ys = [float(p[1]) for p in pts]
    ax.plot(xs, ys, "-", color=colour, lw=1, alpha=0.6)
    ax.plot(xs, ys, "o", color=colour, ms=5)
    if numbers:
        for k, (x, y) in enumerate(zip(xs, ys)):
            ax.annotate(str(k), (x, y), textcoords="offset points", xytext=(5, 4), fontsize=9, color=th["ink"])
    ax.set_xlim(0.25, 1)
    ax.set_ylim(0.25, 0.75)
    ax.set_aspect("equal")
    ax.set_xticks([0.25, 0.5, 0.75, 1])
    ax.set_yticks([0.25, 0.5, 0.75])
    ax.set_xlabel("X: state, then the tape to the left")
    ax.set_ylabel("Y: tape from the head on")


def fig_encoding(pts, pts2):
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.6))
        ax1 = fig.add_axes([0.07, 0.11, 0.4, 0.68])
        draw_square(ax1, th, pts, th["s2"])
        ax1.set_title("busy beaver: reaches the red halting band at step 6", fontsize=10.5, color=th["ink"])
        ax2 = fig.add_axes([0.57, 0.11, 0.4, 0.68])
        draw_square(ax2, th, pts2, th["s1"], numbers=False)
        ax2.set_title(f"a machine that never halts: {len(pts2) - 1} steps, never there", fontsize=10.5,
                      color=th["ink"])
        title(fig, "The whole tape as one point of a square",
              "Computed exactly. Each step moves the point by a stretch-and-squeeze map of its rectangle. "
              "Halting = entering the red band.", th)
        save(fig, "encoding", mode)


def fig_area():
    # the rule (A, 0) -> (B, 1, right): x' = 2/4 + 2/16 + (x - 1/4)/4,  y' = 4 y - 1
    src = ((Fr(1, 4), Fr(1, 4)), (Fr(1, 2), Fr(1, 2)))           # [1/4, 1/2] x [1/4, 1/2]
    corners = [(src[0][0], src[0][1]), (src[1][0], src[1][1])]
    img = []
    for x, y in corners:
        img.append((Fr(2, 4) + Fr(2, 16) + (x - Fr(1, 4)) / 4, 4 * y - 1))
    (x0, y0), (x1, y1) = img
    a_src = (src[1][0] - src[0][0]) * (src[1][1] - src[0][1])
    a_img = (x1 - x0) * (y1 - y0)
    assert a_src == a_img
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.2))
        ax = fig.add_axes([0.25, 0.1, 0.5, 0.7])
        ax.add_patch(Rectangle((0, 0), 1, 1, fc="none", ec=th["axis"], lw=1))
        ax.add_patch(Rectangle((float(src[0][0]), float(src[0][1])), 0.25, 0.25, fc=th["s1"], alpha=0.75,
                               ec=th["s1"]))
        ax.add_patch(Rectangle((float(x0), float(y0)), float(x1 - x0), float(y1 - y0), fc=th["s2"], alpha=0.75,
                               ec=th["s2"]))
        ax.annotate("", xy=(float(x0) - 0.005, 0.5), xytext=(0.5, 0.42),
                    arrowprops=dict(arrowstyle="-|>", color=th["ink2"], lw=1.6, connectionstyle="arc3,rad=-0.3"))
        ax.text(0.375, 0.2, f"before\narea {a_src}", ha="center", va="top", fontsize=11, color=th["s1"])
        ax.text(float(x1) + 0.02, 0.8, f"after\narea {a_img}", ha="left", va="center", fontsize=11, color=th["s2"])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
        title(fig, "One rule = one stretch-and-squeeze that keeps area",
              "Computed: the rule 'state A reads 0: write 1, move right, go to B' squeezes X by 4 and stretches Y "
              "by 4.", th)
        save(fig, "area", mode)


def fig_recipe():
    steps = [("1. Make it reversible", "Keep a record of\nwhat each step erases\n(Bennett's idea).", "s1"),
             ("2. Rectangles", "Each rule becomes a\nstretch-and-squeeze\nmap of a rectangle.", "s4"),
             ("3. A stirring flow", "Smooth swirls in a plane\ncarry every rectangle\nto its image.", "s3"),
             ("4. Clock and force", "A third direction is\nthe clock. Then read off\nthe force that drives it.", "s2")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.2))
        ax = fig.add_axes([0.02, 0.04, 0.96, 0.78])
        ax.axis("off")
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 1)
        for i, (head, body, c) in enumerate(steps):
            ax.add_patch(FancyBboxPatch((i + 0.06, 0.1), 0.82, 0.8, boxstyle="round,pad=0.02",
                                        fc=th["mid"], ec=th[c], lw=2))
            ax.text(i + 0.47, 0.76, head, ha="center", va="center", fontsize=11.5, fontweight="bold", color=th[c])
            ax.text(i + 0.47, 0.42, body, ha="center", va="center", fontsize=10.5, color=th["ink"])
            if i < 3:
                ax.annotate("", xy=(i + 1.05, 0.5), xytext=(i + 0.9, 0.5),
                            arrowprops=dict(arrowstyle="-|>", color=th["axis"], lw=1.8))
        title(fig, "From a machine to a force", "A labelled diagram of Sections 3 to 5 of the paper.", th)
        save(fig, "recipe", mode)


def fig_timeline():
    events = [(1961, "Landauer:\nerasing costs;\nkeep records"), (1973, "Bennett:\nreversible\ncomputation"),
              (1990, "Moore: a tape\nas a point;\ngeneralized shifts"), (2016, "Tao: a 'fluid\ncomputer' as a\nroute to blowup"),
              (2021, "Cardona et al.:\nTuring-complete\nEuler flows"), (2026, "Dyhr et al.:\nstationary\nNavier–Stokes"),
              (2026, "OpenAI: forced\nflow from rest\n(claimed)")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.6))
        ax = fig.add_axes([0.03, 0.04, 0.94, 0.80])
        ax.axis("off")
        ax.set_xlim(-0.6, len(events) - 0.4)
        ax.set_ylim(-1.8, 1.6)
        ax.plot([-0.4, len(events) - 0.6], [0, 0], color=th["axis"], lw=2)
        for k, (year, text) in enumerate(events):
            up = k % 2 == 0
            last = k == len(events) - 1
            ax.plot([k], [0], "o", ms=9, color=th["s2"] if last else th["s1"], zorder=3)
            ax.plot([k, k], [0, 0.3 if up else -0.3], color=th["axis"], lw=1)
            ax.text(k, 0.4 if up else -0.4, f"{year}\n{text}", ha="center", va="bottom" if up else "top",
                    fontsize=10, color=th["ink"])
        title(fig, "Computing with fluids", "Evenly spaced steps, not to scale.", th)
        save(fig, "timeline", mode)


def main(argv):
    confs, pts, confs2, pts2 = check()
    if "--check" in argv:
        print("ok: busy beaver halts after", len(confs) - 1, "steps; the other machine ran", len(confs2) - 1)
        return
    fig_machine(confs)
    fig_encoding(pts, pts2)
    fig_area()
    fig_recipe()
    fig_timeline()


if __name__ == "__main__":
    main(sys.argv[1:])
