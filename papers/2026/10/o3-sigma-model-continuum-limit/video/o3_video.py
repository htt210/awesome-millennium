"""Narrated explainer for "The canonical massive continuum limit of the
two-dimensional O(3) model" (OpenAI, October 2026), written for 3b1b's manim
(manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("2.3") and
the words come from beat 2.3 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl o3_video.py C2Model -w -l --config_file ../../../../../tools/video/custom_config.yml

Computed: every spin configuration, correlation curve, length and block average
comes from the Monte Carlo in ../code/o3_mc.py (its saved mc_results.json). The
energy ladders, the shrinking grid, the tilted grids and the four-point picture
are schematics.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "video"))
from narrated import *  # noqa: E402,F403

RES = json.loads((HERE.parent / "code" / "mc_results.json").read_text())
BY_BETA = {r["beta"]: r for r in RES}
CURVE_COLS = [BLUE_A, BLUE_B, BLUE_C, BLUE_D, PURPLE_B, ORANGE, RED_C]


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["Mass gap", "The model", "Continuum", "The claim", "Is it right?"]
    PRONOUNCE = [(r"\bO\(3\)", "O three"), (r"\bO\(n\)", "O n"), (r"\bPolyakov\b", "Polyahkov"),
                 (r"\b1975\b", "nineteen seventy-five"), (r"\b2026\b", "twenty twenty-six")]
    BUILD = HERE / "build"


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def hexcol(v):
    r, g, b = (np.clip((np.asarray(v) + 1) / 2, 0, 1) * 255).astype(int)
    return f"#{r:02x}{g:02x}{b:02x}"


def spin_squares(q, size=3.6, center=ORIGIN):
    q = np.asarray(q)
    n = q.shape[0]
    cell = size / n
    grp = VGroup()
    for i in range(n):
        for j in range(n):
            sq = Square(side_length=cell).set_stroke(width=0).set_fill(hexcol(q[i, j]), 1)
            sq.move_to(center + np.array([(j - (n - 1) / 2) * cell, ((n - 1) / 2 - i) * cell, 0]))
            grp.add(sq)
    return grp


def spin_arrows(q, size=5.0, center=ORIGIN):
    """Arrows for a small window: the in-plane part of each unit vector, coloured by the full vector."""
    q = np.asarray(q)
    n = q.shape[0]
    cell = size / n
    grp = VGroup()
    for i in range(n):
        for j in range(n):
            c = center + np.array([(j - (n - 1) / 2) * cell, ((n - 1) / 2 - i) * cell, 0])
            v = np.array([q[i, j][0], q[i, j][1], 0]) * 0.45 * cell
            if np.linalg.norm(v) < 0.04 * cell:
                grp.add(Dot(c, radius=0.05 * cell, fill_color=hexcol(q[i, j])))
            else:
                grp.add(Line(c - v, c + v).set_stroke(hexcol(q[i, j]), 3).add_tip(length=0.14 * cell, width=0.14 * cell, fill_color=hexcol(q[i, j])))
    return grp


def block(q, k):
    q = np.asarray(q)
    L = q.shape[0] // k
    b = q[:L * k, :L * k].reshape(L, k, L, k, 3).sum(axis=(1, 3))
    return b / np.linalg.norm(b, axis=-1, keepdims=True)


def ladder(center=ORIGIN, gap=1.0, label=True):
    base = Line(1.4 * LEFT, 1.4 * RIGHT).set_stroke(YELLOW, 4).move_to(center)
    vac = txt("vacuum", 24, YELLOW).next_to(base, LEFT, buff=0.3)
    levels = VGroup(*[Line(1.4 * LEFT, 1.4 * RIGHT).set_stroke(BLUE_C, 3).move_to(center + (gap + 0.25 * k) * UP)
                      for k in range(6)])
    brace = Brace(Line(center, center + gap * UP), RIGHT, buff=1.6).set_color(ORANGE)
    bl = txt("mass gap m > 0", 24, ORANGE).next_to(brace, RIGHT, buff=0.15)
    axis = Arrow(center + 1.9 * LEFT + 0.2 * DOWN, center + 1.9 * LEFT + (gap + 1.8) * UP, buff=0)
    axis.set_stroke(GREY_B, 2).set_fill(GREY_B)
    al = txt("energy", 22, GREY_B).next_to(axis, UP, buff=0.1)
    return VGroup(axis, al, base, vac, levels, brace, bl)


def log_chart(x_range, y_range, width, height, xticks, yticks, xlabel, ylabel, xfmt=None):
    return Chart(x_range, y_range, width, height, xticks=xticks, yticks=yticks,
                 xfmt=xfmt or (lambda v: txt(f"{v:g}", 18, GREY_B)),
                 yfmt=lambda v: txt(f"10^{int(v)}" if v not in (0, 1) else ("1" if v == 0 else "10"), 18, GREY_B),
                 xlabel=xlabel, ylabel=ylabel, grid=False)


def poly(ax, xs, ys, color, width=3):
    pts = [ax.c2p(x, y) for x, y in zip(xs, ys)]
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        q = np.array(BY_BETA[1.6]["snapshot"])
        self.narrate("0.1")
        arrows = spin_arrows(q[:12, :12], size=5.2, center=0.4 * UP)
        self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.004), run_time=2)
        self.finish()

        self.narrate("0.2")
        fine = spin_squares(q, size=5.2, center=0.4 * UP)
        self.play(FadeOut(arrows), FadeIn(fine), run_time=1.5)
        self.cue("Do the arrows")
        qm = txt("?", 120, YELLOW).next_to(fine, RIGHT, buff=0.8)
        self.play(FadeIn(qm, scale=1.3))
        self.cue("mass gap")
        gapq = txt("a mass gap?", 34, ORANGE).next_to(fine, LEFT, buff=0.6)
        self.play(FadeIn(gapq))
        self.finish()

        self.narrate("0.3")
        title = txt("The O(3) Continuum Limit", 56)
        sub = txt("OpenAI preprint, October 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(VGroup(fine, qm, gapq)), Write(title, run_time=2))
        self.play(FadeIn(sub))
        self.cue("famous stand-in")
        st = txt("a stand-in for the Yang–Mills problem", 30, YELLOW).next_to(sub, DOWN, buff=0.4)
        self.play(FadeIn(st))
        self.finish()
        self.clear_caption()

        self.narrate("0.4")
        big = self.roadmap(None, big=True).move_to(1.6 * DOWN)
        self.play(VGroup(title, sub, st).animate.shift(UP), FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, st, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — the mass gap
# ---------------------------------------------------------------------------

class C1Gap(Video):
    def construct(self):
        self.chapter(0, "1. The mass gap")
        self.narrate("1.1")
        field = FunctionGraph(lambda x: 0.6 * math.exp(-x * x) * math.cos(5 * x), x_range=(-6, 6, 0.02))
        field.set_stroke(BLUE_C, 4).shift(0.8 * UP)
        flat = Line(6 * LEFT, 6 * RIGHT).set_stroke(GREY_D, 2).shift(0.8 * UP)
        fl = txt("a field fills space; a particle is a ripple in it", 28, GREY_A).next_to(flat, DOWN, buff=0.9)
        self.play(ShowCreation(flat), FadeIn(fl))
        self.play(Transform(flat.copy(), field), run_time=1.5)
        self.cue("The strong nuclear")
        ym = txt("strong force: a Yang–Mills theory", 30, YELLOW).next_to(fl, DOWN, buff=0.35)
        self.play(FadeIn(ym))
        self.finish()
        self.clear_content()

        self.narrate("1.2")
        lad = ladder(center=1.3 * DOWN + 1.0 * LEFT, gap=1.4)
        self.play(FadeIn(lad[:4]))
        self.play(LaggedStart(*[ShowCreation(l) for l in lad[4]], lag_ratio=0.15))
        self.cue("The smallest energy")
        self.play(GrowFromCenter(lad[5]), FadeIn(lad[6]))
        self.finish()
        self.clear_content()

        self.narrate("1.3")
        clay = card(["1.  construct 4D Yang–Mills theory rigorously", "2.  prove that it has a mass gap"],
                    width=10, size=30, title="The Millennium problem").move_to(0.6 * UP)
        self.play(FadeIn(clay))
        self.finish()
        self.play(FadeOut(clay))

        self.narrate("1.4")
        c = card(["no interacting quantum field theory in four dimensions", "has been built rigorously yet"],
                 width=10.5, size=30).move_to(1.0 * UP)
        toy = txt("so: practise on simpler models", 32, YELLOW).next_to(c, DOWN, buff=0.5)
        self.play(FadeIn(c))
        self.cue("So physicists")
        self.play(FadeIn(toy))
        self.finish()

        self.recap("1.5", ["Yang–Mills: build the theory, prove the gap.", "Both are open."])


# ---------------------------------------------------------------------------
# Chapter 2 — the model
# ---------------------------------------------------------------------------

class C2Model(Video):
    def construct(self):
        self.chapter(1, "2. The model")
        q = np.array(BY_BETA[1.1]["snapshot"])
        self.narrate("2.1")
        arrows = spin_arrows(q[:9, :9], size=4.6, center=0.4 * UP + 2.0 * LEFT)
        note = VGroup(txt("one arrow per grid point", 26), txt("length one", 26, GREY_A),
                      txt("pointing anywhere in 3D", 26, GREY_A)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        note.next_to(arrows, RIGHT, buff=0.8)
        self.play(LaggedStart(*[FadeIn(a) for a in arrows], lag_ratio=0.01), run_time=1.5)
        self.play(FadeIn(note, lag_ratio=0.3))
        self.finish()
        self.clear_content()

        self.narrate("2.2")
        panels = VGroup()
        for k, b in enumerate((0.6, 1.1, 1.6)):
            grid = spin_squares(BY_BETA[b]["snapshot"], size=3.3, center=np.array([(k - 1) * 4.2, 0.5, 0]))
            lab = txt(f"β = {b}", 28, YELLOW).next_to(grid, UP, buff=0.2)
            panels.add(VGroup(grid, lab))
        src = txt("our Monte Carlo samples", 22, GREY_A).next_to(panels, DOWN, buff=0.3)
        self.play(FadeIn(panels[0]))
        self.cue("These are samples")
        self.play(FadeIn(panels[1]), FadeIn(panels[2]), FadeIn(src))
        self.finish()
        self.clear_content()

        self.narrate("2.3")
        same = card(["asymptotically free (Polyakov, 1975)", "a mass gap expected"], width=5.6, size=26,
                    title="like Yang–Mills").move_to(3.1 * LEFT + 0.5 * UP)
        diff = card(["two dimensions, not four", "no gauge field"], width=5.6, size=26, title="but simpler",
                    title_color=ORANGE).move_to(3.1 * RIGHT + 0.5 * UP)
        self.play(FadeIn(same))
        self.cue("But it has only")
        self.play(FadeIn(diff))
        self.finish()
        self.clear_content()

        self.narrate("2.4")
        ax = log_chart((0, 60), (-3.5, 0), 8.0, 3.6, (0, 20, 40, 60), (-3, -2, -1, 0),
                       "distance (grid steps)", "correlation")
        ax.shift(0.45 * UP - ax.box.get_center())
        curves = VGroup()
        for r, col in zip(RES, CURVE_COLS):
            C = np.array(r["C_axis"])
            rr = np.arange(len(C))
            bad = np.nonzero(C < 5e-4)[0]
            keep = (rr < (bad[0] if len(bad) else len(C))) & (rr <= 60)
            curves.add(poly(ax, rr[keep], np.log10(C[keep]), col))
        labs = VGroup(*[txt(f"β = {r['beta']}", 18, col) for r, col in zip(RES, CURVE_COLS)])
        labs.arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(ax.box, RIGHT, buff=0.3)
        self.play(FadeIn(ax))
        self.cue("Our simulation")
        self.play(LaggedStart(*[ShowCreation(c) for c in curves], lag_ratio=0.2), FadeIn(labs), run_time=2.5)
        self.finish()

        self.recap("2.5", ["A grid of arrows: asymptotically free,", "and expected to have a gap."])


# ---------------------------------------------------------------------------
# Chapter 3 — the continuum
# ---------------------------------------------------------------------------

class C3Continuum(Video):
    def construct(self):
        self.chapter(2, "3. The continuum")
        self.narrate("3.1")
        b = np.array([r["beta"] for r in RES])
        xi = np.array([r["xi2"] for r in RES])
        ax = log_chart((0.5, 1.8), (-1, 2), 8.0, 3.6, (0.6, 0.9, 1.2, 1.5, 1.8), (-1, 0, 1, 2),
                       "coupling β", "correlation length")
        ax.shift(0.45 * UP - ax.box.get_center())
        sel = b >= 1.3
        const = float(np.exp(np.mean(np.log(xi[sel] / (np.exp(2 * math.pi * b[sel]) / b[sel])))))
        shape = curve(ax, lambda x: math.log10(const * math.exp(2 * math.pi * x) / x), 0.9, 1.8, color=GREY_B,
                      width=2, ylim=(-1, 2))
        shape = DashedVMobject(shape)
        dots = VGroup(*[Dot(ax.c2p(x, math.log10(y)), radius=0.08, fill_color=BLUE_C) for x, y in zip(b, xi)])
        vals = VGroup(*[txt(f"{y:.1f}", 18, GREY_A).next_to(d, UL, buff=0.05) for d, y in zip(dots, xi)])
        sl = txt("e^(2πβ)/β shape, constant fitted", 20, GREY_B).next_to(ax.c2p(1.0, 1.7), RIGHT, buff=0.05)
        self.play(FadeIn(ax))
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.2), FadeIn(vals))
        self.cue("roughly like")
        self.play(ShowCreation(shape), FadeIn(sl))
        self.finish()
        self.clear_content()

        self.narrate("3.2")
        circle = Circle(radius=1.6).set_stroke(ORANGE, 4).move_to(0.4 * UP)
        cl = txt("one correlation length", 24, ORANGE).next_to(circle, UP, buff=0.15)
        grids = []
        for steps in (4, 8, 16):
            a = 3.2 / steps
            g = VGroup()
            n = int(4.4 / a)
            for k in range(-n, n + 1):
                g.add(Line([k * a, -4.4, 0], [k * a, 4.4, 0]).set_stroke(GREY_D, 1.5))
                g.add(Line([-4.4, k * a, 0], [4.4, k * a, 0]).set_stroke(GREY_D, 1.5))
            g.move_to(circle.get_center())
            grids.append((g, txt(f"{steps // 2} grid steps across the radius", 24, GREY_A).move_to(2.3 * DOWN)))
        g0, l0 = grids[0]
        self.play(FadeIn(g0), ShowCreation(circle), FadeIn(cl), FadeIn(l0))
        for g, l in grids[1:]:
            self.play(FadeOut(g0), FadeIn(g), FadeOut(l0), FadeIn(l), run_time=1.2)
            g0, l0 = g, l
        self.bring_to_front(circle)
        self.finish()
        self.clear_content()

        self.narrate("3.3")
        sel = [r for r in RES if r["beta"] >= 1.1]
        series = []
        for r in sel:
            C = np.array(r["C_axis"])
            rr = np.arange(len(C))
            x = rr / r["xi2"]
            y = r["xi2"] ** 2 * C / r["chi"]
            keep = x <= 2.5
            series.append((x[keep], np.log10(y[keep])))
        lo = math.floor(min(s[1].min() for s in series))
        hi = math.ceil(max(s[1].max() for s in series))
        ax2 = log_chart((0, 2.5), (lo, hi), 8.0, 3.6, (0, 1, 2), tuple(range(lo, hi + 1)),
                        "distance ÷ correlation length", "rescaled correlation")
        ax2.shift(0.45 * UP - ax2.box.get_center())
        curves = VGroup(*[poly(ax2, x, y, col, 3) for (x, y), col in zip(series, CURVE_COLS[2:])])
        labs = VGroup(*[txt(f"β = {r['beta']}: ξ = {r['xi2']:.1f}", 18, col) for r, col in zip(sel, CURVE_COLS[2:])])
        labs.arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(ax2.box, RIGHT, buff=0.3)
        self.play(FadeIn(ax2))
        self.cue("In those units")
        self.play(LaggedStart(*[ShowCreation(c) for c in curves], lag_ratio=0.3), FadeIn(labs), run_time=2.5)
        self.finish()
        self.clear_content()

        self.narrate("3.4")
        c = card(["prove the limit exists, for every correlation,", "and say what it is"], width=9.5, size=32)
        c.move_to(0.6 * UP)
        self.play(FadeIn(c))
        self.finish()

        self.recap("3.5", ["Raise β, shrink the grid,", "keep the physical scale fixed."])


# ---------------------------------------------------------------------------
# Chapter 4 — the claim
# ---------------------------------------------------------------------------

class C4Claim(Video):
    def construct(self):
        self.chapter(3, "4. The claim")
        self.narrate("4.1")
        c = card(["the rescaled fields converge to one limit,", "for every way β → ∞"], width=9.5, size=32)
        c.move_to(0.6 * UP)
        self.play(FadeIn(c))
        self.finish()
        self.play(FadeOut(c))

        self.narrate("4.2")
        os_ = card(["Osterwalder–Schrader axioms"], width=6.5, size=32).move_to(1.5 * UP)
        arr = Arrow(os_.get_bottom(), os_.get_bottom() + 1.0 * DOWN, buff=0.1).set_stroke(YELLOW, 4).set_fill(YELLOW)
        qft = card(["a relativistic quantum field theory", "in 1 space + 1 time dimension"], width=8.5, size=30)
        qft.next_to(arr, DOWN, buff=0.1)
        self.play(FadeIn(os_))
        self.cue("So it defines")
        self.play(GrowArrow(arr), FadeIn(qft))
        self.finish()
        self.clear_content()

        self.narrate("4.3")
        lad = ladder(center=1.3 * DOWN + 1.0 * LEFT, gap=1.4)
        one = txt("one vacuum", 24, YELLOW).next_to(lad[2], DOWN, buff=0.2)
        self.play(FadeIn(lad[:4]), FadeIn(one))
        self.cue("every other state")
        self.play(LaggedStart(*[ShowCreation(l) for l in lad[4]], lag_ratio=0.1))
        self.play(GrowFromCenter(lad[5]), FadeIn(lad[6]))
        self.finish()
        self.clear_content()

        self.narrate("4.4")
        pts = [np.array(p) for p in ([-4.6, 1.3, 0], [-2.6, 1.3, 0], [-4.6, -0.5, 0], [-2.6, -0.5, 0])]
        free = VGroup(*[Dot(p, radius=0.12, fill_color=BLUE_C) for p in pts],
                      Line(pts[0], pts[2]).set_stroke(BLUE_C, 3), Line(pts[1], pts[3]).set_stroke(BLUE_C, 3))
        fl = txt("free field: only pairs", 24, BLUE_C).next_to(free, DOWN, buff=0.4)
        pts2 = [p + 7.2 * RIGHT for p in pts]
        ctr = sum(pts2) / 4
        inter = VGroup(*[Dot(p, radius=0.12, fill_color=ORANGE) for p in pts2],
                       *[Line(p, ctr).set_stroke(ORANGE, 3) for p in pts2], Dot(ctr, radius=0.16, fill_color=ORANGE))
        il = txt("connected four-point ≠ 0", 24, ORANGE).next_to(inter, DOWN, buff=0.4)
        self.play(FadeIn(free), FadeIn(fl))
        self.cue("a four-point")
        self.play(FadeIn(inter), FadeIn(il))
        self.finish()

        self.recap("4.5", ["Claimed: one canonical limit, an interacting", "quantum field theory with a mass gap."])


# ---------------------------------------------------------------------------
# Chapter 5 — how it works
# ---------------------------------------------------------------------------

class C5How(Video):
    def construct(self):
        self.chapter(3, "5. How it works")
        q = np.array(BY_BETA[1.6]["snapshot"])
        self.narrate("5.1")
        levels = [q, block(q, 2), block(q, 4), block(q, 8)]
        panels = VGroup(*[spin_squares(l, size=2.6) for l in levels]).arrange(RIGHT, buff=0.75).move_to(0.5 * UP)
        arrows = VGroup(*[Arrow(panels[k].get_right(), panels[k + 1].get_left(), buff=0.08).set_stroke(GREY_B, 3)
                          for k in range(3)])
        labs = VGroup(*[txt(s, 20, GREY_A).next_to(p, DOWN, buff=0.2)
                        for s, p in zip(["32 × 32", "16 × 16", "8 × 8", "4 × 4"], panels)])
        self.play(FadeIn(panels[0]), FadeIn(labs[0]))
        self.cue("keep one averaged")
        for k in range(3):
            self.play(GrowArrow(arrows[k]), FadeIn(panels[k + 1]), FadeIn(labs[k + 1]), run_time=0.9)
        self.finish()
        self.clear_content()

        self.narrate("5.2")
        rows = VGroup()
        for k, w in enumerate((5.0, 2.6, 1.4, 0.75, 0.4)):
            bar = Rectangle(width=w, height=0.36).set_stroke(width=0).set_fill(TEAL_C, 0.85)
            lab = txt(f"step {k + 1}", 20, GREY_A)
            rows.add(VGroup(lab, bar).arrange(RIGHT, buff=0.3, aligned_edge=ORIGIN))
        rows.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(2.2 * LEFT + 0.5 * UP)
        rl = txt("corrections left over, step by step", 22, TEAL_C).next_to(rows, UP, buff=0.3)
        rough = card(["rare rough regions:", "kept under control"], width=4.2, size=24).move_to(4.0 * RIGHT + 0.5 * UP)
        self.play(FadeIn(rl), LaggedStart(*[FadeIn(r, shift=0.2 * RIGHT) for r in rows], lag_ratio=0.25), run_time=2)
        self.cue("and rare rough")
        self.play(FadeIn(rough))
        self.finish()
        self.clear_content()

        self.narrate("5.3")
        def grid(angle, color):
            g = VGroup()
            for k in range(-6, 7):
                g.add(Line([k * 0.5, -3, 0], [k * 0.5, 3, 0]).set_stroke(color, 1.6))
                g.add(Line([-3, k * 0.5, 0], [3, k * 0.5, 0]).set_stroke(color, 1.6))
            return g.rotate(angle).move_to(0.5 * UP)
        g1 = grid(0, GREY_C)
        g2 = grid(math.atan(0.5), BLUE_C)
        mask = Circle(radius=2.2).move_to(0.5 * UP).set_stroke(GREY_B, 2)
        tl = txt("tilted blocking: a rotation by an irrational angle", 24, BLUE_C).next_to(mask, DOWN, buff=0.3)
        g1.set_opacity(0.8)
        self.play(FadeIn(g1), ShowCreation(mask))
        self.play(FadeIn(g2), FadeIn(tl))
        self.play(Rotate(g2, 2 * math.pi / 12, about_point=0.5 * UP), run_time=1.5)
        self.finish()
        self.clear_content()

        self.narrate("5.4")
        a = card(["correlations decay"], width=4.0, size=28).move_to(4.2 * LEFT + 0.5 * UP)
        b = card(["reconstruction"], width=3.6, size=28).move_to(0.5 * UP)
        c = card(["mass gap"], width=3.0, size=30, color=ORANGE).move_to(4.4 * RIGHT + 0.5 * UP)
        a1 = Arrow(a.get_right(), b.get_left(), buff=0.1).set_stroke(YELLOW, 4).set_fill(YELLOW)
        a2 = Arrow(b.get_right(), c.get_left(), buff=0.1).set_stroke(YELLOW, 4).set_fill(YELLOW)
        self.play(FadeIn(a))
        self.play(GrowArrow(a1), FadeIn(b))
        self.play(GrowArrow(a2), FadeIn(c))
        self.finish()

        self.recap("5.5", ["Block, control the corrections,", "reconstruct."])


# ---------------------------------------------------------------------------
# Chapter 6 — is it right?
# ---------------------------------------------------------------------------

class C6Close(Video):
    def construct(self):
        self.chapter(4, "6. Is it right?")
        self.narrate("6.1")
        names = ["O(4): sharp mass bounds", "O(n), n ≥ 3: exponential decay at every β",
                 "O(3): an isolated particle", "O(4): exact mass asymptotics"]
        cards = VGroup(*[card([n_], width=7.6, size=24) for n_ in names]).arrange(DOWN, buff=0.15).move_to(0.5 * UP)
        hl = SurroundingRectangle(cards[1], buff=0.05).set_stroke(YELLOW, 4)
        self.play(LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.2))
        self.cue("including one")
        self.play(ShowCreation(hl))
        self.finish()
        self.clear_content()

        self.narrate("6.2")
        lean = card(["Lean 4: the exponential-decay companion only"], width=9, size=28).move_to(1.2 * UP)
        nf = txt("continuum limit: not formalized", 28, ORANGE).next_to(lean, DOWN, buff=0.4)
        ne = txt("no expert assessment found yet", 28, ORANGE).next_to(nf, DOWN, buff=0.25)
        self.play(FadeIn(lean))
        self.cue("The continuum limit")
        self.play(FadeIn(nf))
        self.cue("and we found")
        self.play(FadeIn(ne))
        self.finish()
        self.clear_content()

        self.narrate("6.3")
        ym = txt("Yang–Mills mass gap ?", 60, YELLOW).move_to(1.0 * UP)
        op = txt("still open: four dimensions and a gauge field", 28, GREY_A).next_to(ym, DOWN, buff=0.4)
        self.play(FadeIn(ym, scale=1.2))
        self.play(FadeIn(op))
        self.finish()
        self.play(FadeOut(VGroup(ym, op)))

        self.narrate("6.4")
        self.play(FadeOut(self.roadmap_mob))
        title = txt("The O(3) Continuum Limit", 50)
        link = VGroup(txt("Explainer, figures and code:", 26, GREY_A),
                      txt("github.com/htt210/awesome-millennium", 28, YELLOW)).arrange(DOWN, buff=0.15)
        link.next_to(title, DOWN, buff=0.6)
        self.play(Write(title))
        self.play(FadeIn(link))
        self.finish(3.0)
        self.clear_caption()
        self.wait(1)


class Thumbnail(Scene):
    def construct(self):
        title = txt("The O(3) Continuum Limit", 58).to_edge(UP, buff=0.6)
        sub = txt("a grid of arrows becomes a quantum field with a mass gap", 30, GREY_A).next_to(title, DOWN, buff=0.25)
        q = np.array(BY_BETA[1.6]["snapshot"])
        g = spin_squares(q, size=4.2, center=3.2 * LEFT + 1.2 * DOWN)
        lad = ladder(center=2.6 * DOWN + 3.0 * RIGHT, gap=1.4)
        self.add(title, sub, g, lad)
