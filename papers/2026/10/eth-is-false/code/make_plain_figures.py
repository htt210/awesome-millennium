#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    python make_plain_figures.py      # writes ../figures/plain-*.png

Same palette and helpers as make_figures.py (which draws the figures of the
technical walkthrough). The numbers come from the paper's formulas, from
toy_eth.py, or from the related-work section of the paper.
"""

from __future__ import annotations

import math
from fractions import Fraction

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

import make_figures as MF
import toy_eth as T
from make_figures import THEMES, save, setup, title

LOG10_2 = math.log10(2)


def legend_entry(ax, x, y, color, text, th, marker="s", transform=None):
    kw = dict(transform=transform or ax.transAxes, clip_on=False)
    ax.plot([x], [y], marker, ms=7, color=color, **kw)
    ax.text(x + 0.018, y, text, fontsize=11, va="center", color=th["ink"], **kw)


# ---------------------------------------------------------------------------
# 1. The puzzle: switches and rules
# ---------------------------------------------------------------------------

SWITCHES = ["A", "B", "C", "D"]
# each rule: (switch, wanted state); a rule is happy when at least one wish holds
RULES = [[("A", 1), ("B", 0), ("C", 1)],
         [("B", 1), ("C", 0), ("D", 1)],
         [("A", 0), ("C", 1), ("D", 0)]]
SETTING = {"A": 1, "B": 1, "C": 1, "D": 0}


def fig_puzzle():
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 4.6))
        ax = fig.add_axes([0.0, 0.0, 1.0, 0.82])
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 4.6)
        ax.axis("off")
        sx = {s: 1.6 + 2.2 * i for i, s in enumerate(SWITCHES)}
        for s in SWITCHES:          # a toggle switch drawn as a pill with a knob
            on = SETTING[s]
            x = sx[s]
            ax.add_patch(FancyBboxPatch((x - 0.55, 3.35), 1.1, 0.5, boxstyle="round,pad=0,rounding_size=0.25",
                                        fc=th["s1"] if on else th["mid"], ec="none"))
            ax.add_patch(Circle((x + (0.3 if on else -0.3), 3.6), 0.2, fc=th["surface"], ec="none", zorder=3))
            ax.text(x, 4.15, s, ha="center", fontsize=15, fontweight="bold", color=th["ink"])
            ax.text(x, 3.08, "on" if on else "off", ha="center", fontsize=11, color=th["ink2"])
        for k, rule in enumerate(RULES):
            x = 1.75 + 3.25 * k
            ok = [SETTING[s] == want for s, want in rule]
            for (s, want), good in zip(rule, ok):
                ax.plot([sx[s], x], [2.85, 2.05], color=th["s3"] if good else th["axis"], lw=2.4 if good else 1.2,
                        zorder=1)
            ax.add_patch(FancyBboxPatch((x - 1.45, 0.35), 2.9, 1.7, boxstyle="round,pad=0,rounding_size=0.15",
                                        fc=th["surface"], ec=th["axis"], lw=1.2, zorder=2))
            ax.text(x, 1.78, f"Rule {k + 1}", ha="center", fontsize=12, fontweight="bold", color=th["ink"], zorder=3)
            wishes = "\nor ".join(f"{s} {'on' if want else 'off'}" for s, want in rule)
            ax.text(x, 1.08, wishes, ha="center", va="center", fontsize=11, color=th["ink2"], zorder=3,
                    linespacing=1.25)
            ax.text(x + 1.2, 1.78, "✓" if any(ok) else "✗", ha="center", fontsize=15, zorder=3,
                    color=th["s3"] if any(ok) else th["red"], fontweight="bold")
        title(fig, "The puzzle: flip switches so that every rule is happy",
              "Each rule names three switches and is happy if at least one of them is the way it wants. "
              "Green lines: wishes that come true.", th)
        save(fig, "plain-puzzle", mode)


# ---------------------------------------------------------------------------
# 2. Trying every setting doubles with every switch
# ---------------------------------------------------------------------------

def fig_doubling():
    ns = list(range(10, 101))
    secs = [2.0 ** n / 1e9 for n in ns]
    marks = [("1 second", 1.0), ("1 year", 3.156e7), ("age of the universe", 13.8e9 * 3.156e7)]
    for mode, th in THEMES.items():
        fig = setup(th)
        ax = fig.add_axes([0.10, 0.13, 0.64, 0.70])
        ax.set_yscale("log")
        ax.set_axisbelow(True)
        for label, s in marks:
            ax.axhline(s, color=th["axis"], lw=1)
            n_cross = math.log2(s * 1e9)
            ax.plot([n_cross], [s], "o", ms=9, color=th["s1"], mec=th["surface"], mew=2, zorder=5)
            ax.text(101.5, s, f"{label}\n(at {n_cross:.0f} switches)", fontsize=10.5, va="center",
                    color=th["ink2"], clip_on=False)
        ax.plot(ns, secs, color=th["s1"], lw=2.4)
        ax.set_xlim(10, 100)
        ax.set_ylim(1e-6, 1e22)
        ax.set_xlabel("number of switches")
        ax.set_ylabel("time to try every setting (seconds)")
        title(fig, "Trying every setting: each new switch doubles the work",
              "A computer checking a billion settings per second. 2 switches have 4 settings, 3 have 8, "
              "100 have about $10^{30}$.", th)
        save(fig, "plain-doubling", mode)


# ---------------------------------------------------------------------------
# 3. Fifty years of shortcuts: the growth factor per switch
# ---------------------------------------------------------------------------

HISTORY = [  # (year, factor per extra switch, who); 3-SAT, as cited by the paper or classical
    (1985, 1.619, "Monien–Speckenmeyer"),
    (1999, 4 / 3, "Schöning"),
    (2014, 1.308, "PPSZ, Hertli"),
    (2026, 1.307031578, "Jiang–Cai"),
]


def fig_history():
    for mode, th in THEMES.items():
        fig = setup(th)
        ax = fig.add_axes([0.08, 0.13, 0.88, 0.70])
        ax.set_axisbelow(True)
        xs, ys = [1970], [2.0]
        for year, base, _ in HISTORY:
            xs += [year, year]
            ys += [ys[-1], base]
        xs.append(2026.9)
        ys.append(ys[-1])
        ax.plot(xs, ys, color=th["s1"], lw=2.4, drawstyle="default")
        ax.plot([1970], [2.0], "o", ms=9, color=th["s1"], mec=th["surface"], mew=2, zorder=5)
        ax.text(1971, 2.04, "try everything: ×2", fontsize=10.5, color=th["ink2"])
        for year, base, who in HISTORY:
            ax.plot([year], [base], "o", ms=9, color=th["s1"], mec=th["surface"], mew=2, zorder=5)
        places = [(1986, 1.655, "left"), (1998.3, 1.37, "right"), (2013.3, 1.37, "right"), (2026.5, 1.235, "right")]
        for (year, base, who), (x, y, ha) in zip(HISTORY, places):
            ax.text(x, y, f"{who} {year}: ×{base:.3f}", fontsize=10.5, color=th["ink2"], ha=ha)
        ax.axhline(1.0, color=th["ink2"], lw=1.5, ls=(0, (4, 3)))
        ax.text(1971, 1.06, "×1 would mean the work stops multiplying. ETH says some floor above ×1 can never be "
                "crossed.", fontsize=10.5, va="center", color=th["ink"])
        ax.set_xlim(1968, 2028)
        ax.set_ylim(0.98, 2.15)
        ax.set_xlabel("year")
        ax.set_ylabel("work multiplied by each extra switch")
        title(fig, "Fifty years of shortcuts, still exponential",
              "Best known guarantees for the three-switch-rule puzzle (3-SAT). Every one still multiplies the work "
              "by a fixed factor per switch.", th)
        save(fig, "plain-history", mode)


# ---------------------------------------------------------------------------
# 4. Three shapes of growth
# ---------------------------------------------------------------------------

def fig_shapes():
    """Work per switch, steps ** (1/n): flat for exponential growth, sinking toward 1 otherwise."""
    ns = [10 ** (2 + i / 100) for i in range(0, 1001)]
    curves = [
        ("exponential, like $2^{n}$:\nalways ×2", lambda n: 2.0, "s2"),
        ("subexponential, like $2^{n/\\sqrt{\\log_2 n}}$:\nsinks toward ×1, slowly", lambda n: 2 ** (1 / math.sqrt(math.log2(n))), "s1"),
        ("polynomial, like $n^{3}$:\nsinks toward ×1, fast", lambda n: n ** (3 / n), "s3"),
    ]
    for mode, th in THEMES.items():
        fig = setup(th)
        ax = fig.add_axes([0.09, 0.13, 0.60, 0.70])
        ax.set_xscale("log")
        ax.set_axisbelow(True)
        for label, f, c in curves:
            ys = [f(n) for n in ns]
            ax.plot(ns, ys, color=th[c], lw=2.4)
            ax.plot([ns[-1] * 1.8], [ys[-1]], "s", ms=7, color=th[c], clip_on=False)
            nudge = {"s1": 0.07, "s3": -0.05}.get(c, 0.0)
            ax.text(ns[-1] * 3.2, ys[-1] + nudge, label, fontsize=11, va="center", color=th["ink"], clip_on=False)
        ax.set_xlim(ns[0], ns[-1])
        ax.set_ylim(1.0, 2.15)
        ax.set_xlabel("number of switches, $n$ (each gridline is 100 times more)")
        ax.set_ylabel("average work multiplied per switch")
        title(fig, "Three ways to grow, measured per switch",
              "Shapes only, every constant set to 1. ETH says the puzzle is stuck on a flat line; "
              "the new method's line keeps sinking.", th)
        save(fig, "plain-shapes", mode)


# ---------------------------------------------------------------------------
# 5. Splitting into independent teams
# ---------------------------------------------------------------------------

def fig_teams():
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 4.8))
        ax = fig.add_axes([0.0, 0.02, 0.52, 0.80])
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")
        import random
        rng = random.Random(7)
        teams = [(2.5, 3.0, th["s1"]), (7.5, 3.0, th["s2"])]
        pts = []
        for cx, cy, c in teams:
            ax.add_patch(Circle((cx, cy), 2.2, fc=th["mid"], ec="none"))
            team = [(cx + 1.5 * math.cos(a), cy + 1.5 * math.sin(a)) for a in
                    [2 * math.pi * k / 7 + 0.3 for k in range(7)]]
            for _ in range(8):
                a, b = rng.sample(team, 2)
                ax.plot([a[0], b[0]], [a[1], b[1]], color=th["axis"], lw=1.2, zorder=1)
            for x, y in team:
                ax.add_patch(Circle((x, y), 0.23, fc=c, ec=th["surface"], lw=2, zorder=3))
            pts.append(team)
        ax.text(2.5, 0.25, "team 1", ha="center", fontsize=12, color=th["ink"])
        ax.text(7.5, 0.25, "team 2", ha="center", fontsize=12, color=th["ink"])
        ax.text(5.0, 5.55, "no rule connects the two teams", ha="center", fontsize=11, color=th["ink2"])

        ax2 = fig.add_axes([0.62, 0.16, 0.34, 0.62])
        ax2.set_axisbelow(True)
        ax2.set_yscale("log")
        vals = [2.0 ** 40, 2 * 2.0 ** 20]
        ax2.bar([0, 1], vals, width=0.55, color=[th["s2"], th["s1"]], linewidth=0)
        ax2.set_xticks([0, 1], ["all 40 switches\nat once", "two teams of 20,\nseparately"])
        ax2.set_ylim(1, 1e14)
        ax2.text(0, vals[0] * 2.2, "1.1 trillion", ha="center", fontsize=11, color=th["ink"])
        ax2.text(1, vals[1] * 2.2, "2.1 million", ha="center", fontsize=11, color=th["ink"])
        ax2.set_ylabel("settings to try (log scale)")
        ax2.grid(axis="x", visible=False)
        title(fig, "The dream: independent teams",
              "If no rule mixes the teams, count each team's good settings on its own and multiply: "
              "the work collapses.", th)
        save(fig, "plain-teams", mode)


# ---------------------------------------------------------------------------
# 6. The dial: at special settings, teams only exchange a few totals
# ---------------------------------------------------------------------------

def fig_dial():
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.6))
        for k, (label, sub) in enumerate([("dial at 0: the real puzzle", "rules reach across teams"),
                                          ("dial at 1, 2, 3, ...: blended puzzles",
                                           "across teams, rules only see a few totals")]):
            ax = fig.add_axes([0.02 + 0.5 * k, 0.04, 0.46, 0.74])
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 6)
            ax.axis("off")
            team_pts = []
            for cx, c in ((2.4, th["s1"]), (7.6, th["s2"])):
                ax.add_patch(Circle((cx, 3.0), 1.9, fc=th["mid"], ec="none"))
                team = [(cx + 1.25 * math.cos(a), 3.0 + 1.25 * math.sin(a))
                        for a in [2 * math.pi * j / 6 + 0.5 for j in range(6)]]
                for x, y in team:
                    ax.add_patch(Circle((x, y), 0.21, fc=c, ec=th["surface"], lw=2, zorder=3))
                team_pts.append(team)
            left, right = team_pts
            crossing = [(left[0], right[3]), (left[5], right[2]), (left[1], right[4]), (left[0], right[2])]
            if k == 0:
                for a, b in crossing:
                    ax.plot([a[0], b[0]], [a[1], b[1]], color=th["red"], lw=1.6, zorder=2)
            else:
                ax.add_patch(FancyBboxPatch((4.35, 2.45), 1.3, 1.1, boxstyle="round,pad=0,rounding_size=0.12",
                                            fc=th["surface"], ec=th["s3"], lw=2, zorder=4))
                ax.text(5.0, 3.0, "a few\ntotals", ha="center", va="center", fontsize=10.5, color=th["ink"],
                        zorder=5)
                for p in (left[0], left[5]):
                    ax.plot([p[0], 4.35], [p[1], 3.0], color=th["s3"], lw=1.6, zorder=2)
                for p in (right[3], right[2]):
                    ax.plot([5.65, p[0]], [3.0, p[1]], color=th["s3"], lw=1.6, zorder=2)
            ax.text(5.0, 5.55, label, ha="center", fontsize=12.5, fontweight="bold", color=th["ink"])
            ax.text(5.0, 0.35, sub, ha="center", fontsize=11, color=th["ink2"])
        title(fig, "The trick: a dial that blends the puzzle",
              "At the special dial settings, fix the few totals, and the teams can again be counted separately.",
              th)
        save(fig, "plain-dial", mode)


# ---------------------------------------------------------------------------
# 7. Back to dial 0: a curve is pinned down by values plus slopes
# ---------------------------------------------------------------------------

def fig_curve():
    import random
    rng = random.Random(4)
    n = 6
    clauses = T.random_bounded_cnf(n, rng)
    params = T.Params(2, 3, 2)
    con = T.build(n, clauses, params, rng)
    H = [float(c) for c in MF.exact_H(con)]
    truth = T.brute_force_count(n, clauses)
    assert abs(H[0] - truth) < 1e-9

    def h(x, c=0.0):
        return sum(a * x**k for k, a in enumerate(H)) + c * (x - 1) * (x - 2) * (x - 3)

    def slope(x):
        return sum(k * a * x ** (k - 1) for k, a in enumerate(H) if k)

    xs = [-0.2 + i * 0.005 for i in range(int(3.6 / 0.005) + 1)]
    alts = [-2.0, -1.0, 1.0, 2.0]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.9))
        for k in range(2):
            ax = fig.add_axes([0.06 + 0.49 * k, 0.13, 0.42, 0.62])
            ax.set_axisbelow(True)
            if k == 0:
                for c in alts:
                    ax.plot(xs, [h(x, c) for x in xs], color=th["muted"], lw=1.4)
                    ax.plot([0], [h(0, c)], "o", ms=7, color=th["muted"], mec=th["surface"], mew=1.5, zorder=4)
            ax.plot(xs, [h(x) for x in xs], color=th["s1"], lw=2.4, zorder=3)
            for t in (1, 2, 3):
                ax.plot([t], [h(t)], "o", ms=10, color=th["s2"], mec=th["surface"], mew=2, zorder=5)
                if k == 1:
                    d = 0.32
                    ax.plot([t - d, t + d], [h(t) - d * slope(t), h(t) + d * slope(t)], color=th["s2"], lw=7,
                            alpha=0.45, solid_capstyle="round", zorder=4)
            ax.plot([0], [truth], "o", ms=12, mfc=th["surface"], mec=th["s3"], mew=3, zorder=6)
            ax.set_xlim(-0.25, 3.5)
            ax.set_ylim(-5, 42)
            ax.set_xlabel("dial setting")
            if k == 0:
                ax.set_ylabel("blended answer")
                ax.set_title("(a) values at 1, 2, 3 only: many curves fit,\nand they disagree at 0",
                             loc="left", fontsize=12, color=th["ink"])
            else:
                ax.set_title(f"(b) add the slopes at 1, 2, 3: only one curve fits,\nand it gives the count, {truth}",
                             loc="left", fontsize=12, color=th["ink"])
        title(fig, "Getting back to the real puzzle",
              "A real example from our toy code (6 switches). The answer at dial 0 is the true count; "
              "the method only computes things at 1, 2, 3.", th)
        save(fig, "plain-curve", mode)
    return truth


# ---------------------------------------------------------------------------
# 8. The catch: astronomically large puzzles
# ---------------------------------------------------------------------------

def fig_catch():
    lams = [10 ** (math.log10(MF.LAMBDA0) + i / 200) for i in range(0, 5 * 200 + 1)]
    factor = [2 ** sum(MF.cost_terms(int(x))) for x in lams]
    digits = [x * LOG10_2 for x in lams]
    x_brute, x_ppsz = MF.crossing(1.0) * LOG10_2, MF.crossing(math.log2(MF.PPSZ_BEST[0])) * LOG10_2
    for mode, th in THEMES.items():
        fig = setup(th)
        ax = fig.add_axes([0.09, 0.13, 0.62, 0.70])
        ax.set_xscale("log")
        ax.set_axisbelow(True)
        ax.axhline(2.0, color=th["s2"], lw=2)
        ax.axhline(MF.PPSZ_BEST[0], color=th["s3"], lw=2)
        ax.plot(digits, factor, color=th["s1"], lw=2.4)
        for x, y, txt in ((x_brute, 2.0, "beats trying everything:\nn has about 18 billion digits"),
                          (x_ppsz, MF.PPSZ_BEST[0], "beats the best old method:\nn has about 340 billion digits")):
            ax.plot([x], [y], "o", ms=9, color=th["s1"], mec=th["surface"], mew=2, zorder=5)
            ax.annotate(txt, (x, y), xytext=(x * 2.5, y + 0.45), fontsize=10.5, color=th["ink2"],
                        arrowprops=dict(arrowstyle="-", color=th["axis"], lw=1))
        right = digits[-1]
        for y, c, txt in ((factor[-1], th["s1"], "the new method\n(paper's explicit numbers)"),
                          (2.0, th["s2"], "try everything: ×2"),
                          (MF.PPSZ_BEST[0], th["s3"], "best old method: ×1.307")):
            ax.plot([right * 1.08], [y], "s", ms=7, color=c, clip_on=False)
            ax.text(right * 1.25, y, txt, fontsize=11, va="center", color=th["ink"], clip_on=False)
        ax.set_xlim(digits[0], right)
        ax.set_ylim(1.0, 3.0)
        ax.set_xlabel("size of the puzzle: number of DIGITS in the number of switches $n$")
        ax.set_ylabel("average work multiplied per switch")
        title(fig, "The catch: it only wins on unimaginably large puzzles",
              "For comparison, the number of atoms in the observable universe has about 80 digits.", th)
        save(fig, "plain-catch", mode)
    return x_brute, x_ppsz


def main():
    fig_puzzle()
    fig_doubling()
    fig_history()
    fig_shapes()
    fig_teams()
    fig_dial()
    truth = fig_curve()
    x_brute, x_ppsz = fig_catch()
    print(f"curve: count {truth}; catch: {x_brute:.3g} and {x_ppsz:.3g} digits")


if __name__ == "__main__":
    main()
