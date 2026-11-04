"""Narrated explainer for OpenAI's two Ricci-flow papers of 24 September 2026
("Bounded scalar curvature and smooth extension of four-dimensional Ricci flow"
and "A closed Ricci flow with bounded scalar curvature and finite-time curvature
blowup"), written for 3b1b's manim (manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("2.3") and
the words come from beat 2.3 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl ricci_video.py C2Curvature -w -l --config_file ../../../../../tools/video/custom_config.yml

Computed: the shrinking-sphere curvature (exact solution) and the number of
curvature components by dimension. The smoothing shapes, pinching neck, bubble
profiles, power-law rates, tree and warped shape are schematics.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "video"))
from narrated import *  # noqa: E402,F403


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["Ricci flow", "Curvature", "The question", "The claims", "Is it right?"]
    PRONOUNCE = [(r"\bRicci\b", "Reechee"), (r"\bŠešum\b", "Shesum"), (r"\b1982\b", "nineteen eighty-two"),
                 (r"\b2005\b", "two thousand five"), (r"\b2026\b", "twenty twenty-six")]
    BUILD = HERE / "build"


def counts(n: int):
    return n * n * (n * n - 1) // 12, min(n * (n + 1) // 2, n * n * (n * n - 1) // 12), 1


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def blob(t, center=ORIGIN, size=2.0):
    """A bumpy closed curve that smooths (t: 0 -> 1) and shrinks."""
    eps = 0.28 * (1 - t) ** 2
    r0 = size * math.sqrt(max(1 - 0.85 * t, 0.02))
    return ParametricCurve(lambda s: center + r0 * (1 + eps * math.cos(5 * s) + 0.5 * eps * math.sin(3 * s))
                           * np.array([math.cos(s), math.sin(s), 0]), t_range=(0, TAU, 0.02)).set_stroke(BLUE_C, 4)


def dumbbell(s, center=ORIGIN, width=8.0):
    """Upper and lower profiles of a dumbbell whose neck radius is 1 - s."""
    def f(x):
        return 1.2 * (1 - (x / (width / 2)) ** 8) ** 0.5 - (0.95 * s) * math.exp(-x * x / 0.6)
    xs = np.linspace(-width / 2 + 0.001, width / 2 - 0.001, 300)
    up = [center + np.array([x, max(f(x), 0.03), 0]) for x in xs]
    dn = [center + np.array([x, -max(f(x), 0.03), 0]) for x in xs[::-1]]
    return VMobject().set_points_smoothly(up + dn + [up[0]]).set_stroke(BLUE_C, 4).set_fill(BLUE_E, 0.3)


def dial(value=0.2, label="scalar curvature", color=GREEN_C, center=ORIGIN):
    arc = Arc(radius=1.0, start_angle=PI, angle=-PI).set_stroke(GREY_B, 4).move_arc_center_to(center)
    ang = PI * (1 - value)
    needle = Line(center, center + 0.85 * np.array([math.cos(ang), math.sin(ang), 0])).set_stroke(color, 6)
    lab = txt(label, 24, color).next_to(arc, DOWN, buff=0.25)
    return VGroup(arc, needle, lab)


def bubble_profile(ax, a, color):
    return curve(ax, lambda r: (1 / a ** 2) / (1 + (r / a) ** 2) ** 3, 0, 3, n=300, color=color, width=4,
                 ylim=(-1, 17))


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        self.narrate("0.1")
        tr = ValueTracker(0)
        shape = always_redraw(lambda: blob(tr.get_value(), center=0.4 * UP))
        self.add(shape)
        self.play(tr.animate.set_value(0.9), run_time=4, rate_func=linear)
        shape.clear_updaters()
        self.cue("This is Ricci flow")
        lab = txt("Ricci flow", 34, YELLOW).move_to(2.6 * UP)
        self.play(FadeIn(lab))
        self.finish()
        self.play(FadeOut(VGroup(shape, lab)))

        self.narrate("0.2")
        s = ValueTracker(0)
        db = always_redraw(lambda: dumbbell(s.get_value(), center=0.4 * UP))
        self.add(db)
        self.play(s.animate.set_value(1.0), run_time=3)
        db.clear_updaters()
        warn = txt("curvature → ∞", 32, RED_C).move_to(2.3 * UP)
        star = RegularPolygon(n=8).set_height(0.6).set_fill(RED_C, 1).set_stroke(width=0).move_to(0.4 * UP)
        self.play(FadeIn(warn), FadeIn(star, scale=0.3))
        self.finish()

        self.narrate("0.3")
        d = dial(0.25, center=1.7 * DOWN + 4.0 * RIGHT)
        self.play(db.animate.shift(1.5 * LEFT), star.animate.shift(1.5 * LEFT), warn.animate.shift(1.5 * LEFT),
                  FadeIn(d))
        self.play(Rotate(d[1], 0.12, about_point=d[1].get_start()), rate_func=there_and_back, run_time=1.2)
        self.cue("no in four")
        ans = VGroup(txt("4 dimensions: no", 28, GREEN_C), txt("high dimensions: yes", 28, ORANGE))
        ans.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(4.0 * RIGHT + 1.0 * UP)
        self.play(FadeIn(ans, lag_ratio=0.4))
        self.finish()

        self.narrate("0.4")
        title = txt("Scalar Curvature and Ricci Flow", 52)
        sub = txt("OpenAI preprints, September 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        VGroup(title, sub).shift(UP)
        big = self.roadmap(None, big=True).move_to(1.6 * DOWN)
        self.play(FadeOut(VGroup(db, star, warn, d, ans)), Write(title, run_time=1.5), FadeIn(sub))
        self.play(FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — Ricci flow
# ---------------------------------------------------------------------------

class C1Flow(Video):
    def construct(self):
        self.chapter(0, "1. Ricci flow")
        self.narrate("1.1")
        eq = Tex(R"\partial_t g = -2\mathrm{Ric}(g)", font_size=72).move_to(1.0 * UP)
        lg = txt("g: how lengths are measured", 26, GREY_A).next_to(eq, DOWN, buff=0.5)
        lr = txt("Ric: the Ricci curvature", 26, GREY_A).next_to(lg, DOWN, buff=0.2)
        self.play(Write(eq))
        self.cue("changes how lengths")
        self.play(FadeIn(lg))
        self.cue("driven by")
        self.play(FadeIn(lr))
        self.finish()
        self.clear_content()

        self.narrate("1.2")
        circ = Circle(radius=1.4).set_stroke(BLUE_C, 4).move_to(3.8 * LEFT + 0.4 * UP)
        ax = Chart((0, 1), (0, 3), 6.0, 3.2, xticks=(0, 0.5, 1), yticks=(0, 1, 2, 3),
                   xfmt=lambda v: txt(f"{v:g} T" if v else "0", 18, GREY_B),
                   yfmt=lambda v: txt(f"10^{int(v)}" if v > 1 else ("1" if v == 0 else "10"), 18, GREY_B),
                   xlabel="time", ylabel="curvature", grid=False)
        ax.shift(2.4 * RIGHT + 0.45 * UP - ax.box.get_center())
        R = curve(ax, lambda f: math.log10(12 / (1 - f)), 0, 0.985, n=300, color=ORANGE, width=4, ylim=(0, 3))
        K = curve(ax, lambda f: math.log10(1 / (1 - f)), 0, 0.985, n=300, color=BLUE_C, width=4, ylim=(0, 3))
        lab = VGroup(txt("scalar 12/r²", 20, ORANGE), txt("sectional 1/r²", 20, BLUE_C)).arrange(DOWN, buff=0.1)
        lab.next_to(ax.c2p(0.05, 2.6), RIGHT, buff=0.05)
        self.play(ShowCreation(circ), FadeIn(ax), FadeIn(lab))
        self.play(circ.animate.scale(0.05), ShowCreation(R), ShowCreation(K), run_time=3.5)
        self.finish()
        self.clear_content()

        self.narrate("1.3")
        db = dumbbell(0.97, center=0.6 * UP)
        sing = txt("singularity", 28, RED_C).next_to(db, UP, buff=0.2)
        cut = VGroup(DashedLine(0.6 * UP + 0.55 * LEFT + 0.9 * DOWN, 0.6 * UP + 0.55 * LEFT + 0.9 * UP),
                     DashedLine(0.6 * UP + 0.55 * RIGHT + 0.9 * DOWN, 0.6 * UP + 0.55 * RIGHT + 0.9 * UP))
        cut.set_stroke(YELLOW, 3)
        p3 = txt("three dimensions: cut and continue (Perelman)", 28, YELLOW).next_to(db, DOWN, buff=0.5)
        self.play(FadeIn(db), FadeIn(sing))
        self.cue("Perelman understood")
        self.play(ShowCreation(cut), FadeIn(p3))
        self.finish()

        self.recap("1.4", ["Ricci flow smooths shapes,", "but it can break down."])


# ---------------------------------------------------------------------------
# Chapter 2 — curvature
# ---------------------------------------------------------------------------

class C2Curvature(Video):
    def construct(self):
        self.chapter(1, "2. Curvature")
        self.narrate("2.1")
        many = VGroup(*[Arrow(ORIGIN, 0.8 * np.array([math.cos(a), math.sin(a), 0]), buff=0).set_stroke(BLUE_C, 3)
                        for a in np.linspace(0, TAU, 12, endpoint=False)]).move_to(4.2 * LEFT + 0.5 * UP)
        l1 = txt("full curvature", 24, BLUE_C).next_to(many, DOWN, buff=0.25)
        few = VGroup(*[Arrow(ORIGIN, 0.8 * np.array([math.cos(a), math.sin(a), 0]), buff=0).set_stroke(TEAL_C, 3)
                       for a in np.linspace(0, TAU, 4, endpoint=False)]).move_to(0.5 * UP)
        l2 = txt("Ricci: averaged", 24, TEAL_C).next_to(few, DOWN, buff=0.25)
        one = Dot(4.2 * RIGHT + 0.5 * UP, radius=0.25, fill_color=ORANGE)
        l3 = txt("scalar: one number", 24, ORANGE).next_to(one, DOWN, buff=0.45)
        a1 = Arrow(many.get_right(), few.get_left(), buff=0.3).set_stroke(GREY_B, 3)
        a2 = Arrow(few.get_right(), one.get_left(), buff=0.3).set_stroke(GREY_B, 3)
        self.play(FadeIn(many), FadeIn(l1))
        self.cue("Averaging gives")
        self.play(GrowArrow(a1), FadeIn(few), FadeIn(l2))
        self.cue("averaging again")
        self.play(GrowArrow(a2), FadeIn(one, scale=2), FadeIn(l3))
        self.finish()
        self.clear_content()

        self.narrate("2.2")
        ns = list(range(2, 9))
        ax = Chart((1.4, 8.6), (0, 3), 9.0, 3.4, xticks=tuple(ns), yticks=(0, 1, 2, 3),
                   xfmt=lambda v: txt(str(int(v)), 20, GREY_B),
                   yfmt=lambda v: txt(["1", "10", "100", "1000"][int(v)], 18, GREY_B),
                   xlabel="dimension", ylabel="numbers per point", grid=False)
        ax.shift(0.4 * UP - ax.box.get_center())
        bars = VGroup()
        for n in ns:
            for k, (val, col) in enumerate(zip(counts(n), (BLUE_C, TEAL_C, ORANGE))):
                h = math.log10(val) + 0.08
                lo, hi = ax.c2p(n - 0.36 + 0.24 * k, 0), ax.c2p(n - 0.14 + 0.24 * k, h)
                bars.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1]).set_stroke(width=0)
                         .set_fill(col, 0.9).move_to((lo + hi) / 2))
        keys = VGroup(txt("full", 20, BLUE_C), txt("Ricci", 20, TEAL_C), txt("scalar", 20, ORANGE))
        keys.arrange(RIGHT, buff=0.4).next_to(ax.box, UP, buff=0.15)
        self.play(FadeIn(ax), FadeIn(keys))
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), run_time=2)
        k4 = 3 * ns.index(4)
        hl = SurroundingRectangle(VGroup(*bars[k4:k4 + 3]), buff=0.08).set_stroke(YELLOW, 3)
        n4 = txt("dimension 4: 20, 10, 1", 26, YELLOW).next_to(hl, UP, buff=0.6)
        self.play(ShowCreation(hl), FadeIn(n4))
        self.finish()
        self.clear_content()

        self.narrate("2.3")
        shape = VMobject().set_points_smoothly([np.array([math.cos(a) * (1.6 + 0.5 * math.cos(2 * a)),
                                                          math.sin(a) * (1.0 + 0.3 * math.sin(3 * a)), 0])
                                                for a in np.linspace(0, TAU, 60)]).set_stroke(PURPLE_B, 4)
        shape.move_to(0.5 * UP)
        tags = VGroup(txt("Ricci curvature = 0", 26, TEAL_C), txt("scalar curvature = 0", 26, ORANGE),
                      txt("yet curved", 30, YELLOW)).arrange(DOWN, buff=0.2).next_to(shape, RIGHT, buff=0.8)
        self.play(ShowCreation(shape))
        self.play(FadeIn(tags, lag_ratio=0.4))
        self.finish()

        self.recap("2.4", ["Scalar curvature: one number.", "It can miss a lot."])


# ---------------------------------------------------------------------------
# Chapter 3 — the question
# ---------------------------------------------------------------------------

class C3Question(Video):
    def construct(self):
        self.chapter(2, "3. The question")
        self.narrate("3.1")
        rows = VGroup(
            VGroup(txt("full curvature bounded", 28), txt("⇒ continues (Hamilton)", 28, GREEN_C)),
            VGroup(txt("Ricci curvature bounded", 28), txt("⇒ continues (Šešum, 2005)", 28, GREEN_C)),
            VGroup(txt("scalar curvature bounded", 28), txt("⇒ ?", 36, YELLOW)))
        for r in rows:
            r.arrange(RIGHT, buff=0.4)
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(0.5 * UP)
        self.play(FadeIn(rows[0]))
        self.cue("In 2005")
        self.play(FadeIn(rows[1]))
        self.cue("The question is")
        self.play(FadeIn(rows[2]))
        self.finish()
        self.clear_content()

        self.narrate("3.2")
        ax = Chart((0, 3), (-1, 17), 8.0, 3.4, grid=False, xlabel="distance from the centre",
                   ylabel="curvature")
        ax.shift(0.45 * UP - ax.box.get_center())
        zero = Line(ax.c2p(0, 0), ax.c2p(3, 0)).set_stroke(GREEN_C, 5)
        zl = txt("scalar curvature: 0", 22, GREEN_C).next_to(ax.c2p(3, 0), UL, buff=0.1)
        sch = txt("schematic", 20, GREY_B).next_to(ax.box, UR, buff=0.05).shift(0.3 * DOWN)
        self.play(FadeIn(ax), ShowCreation(zero), FadeIn(zl), FadeIn(sch))
        prev = None
        for a, col in [(1.0, BLUE_C), (0.5, PURPLE_B), (0.25, ORANGE)]:
            p = bubble_profile(ax, a, col)
            lab = txt(f"size {a}", 20, col).next_to(ax.c2p(a * 0.4, min(1 / a ** 2, 16)), RIGHT, buff=0.15)
            self.play(ShowCreation(p), FadeIn(lab), run_time=1.2)
        self.finish()
        self.clear_content()

        self.narrate("3.3")
        ax2 = Chart((0, 4), (0, 12), 7.0, 3.4, xticks=(0, 1, 2, 3, 4), yticks=(0, 4, 8, 12),
                    xfmt=lambda v: txt(f"10^-{int(v)}" if v else "1", 18, GREY_B),
                    yfmt=lambda v: txt(f"10^{int(v)}" if v else "1", 18, GREY_B),
                    xlabel="time left before the tear", ylabel="full curvature", grid=False)
        ax2.shift(1.0 * LEFT + 0.45 * UP - ax2.box.get_center())
        lines = VGroup()
        labs = VGroup()
        for lam, col, name in [(1, BLUE_C, "usual rate"), (2, GREY_B, "threshold"), (3, PURPLE_B, "faster"),
                               (5, ORANGE, "faster still")]:
            ln = Line(ax2.c2p(0, 0), ax2.c2p(min(4, 12 / lam), min(12, 4 * lam))).set_stroke(col, 4)
            if lam == 2:
                ln = DashedLine(ln.get_start(), ln.get_end()).set_stroke(col, 3)
            lines.add(ln)
            labs.add(txt(name, 20, col))
        labs.arrange(DOWN, buff=0.12, aligned_edge=LEFT).next_to(ax2.box, RIGHT, buff=0.4)
        bound = Line(ax2.c2p(0, 0.1), ax2.c2p(4, 0.1)).set_stroke(GREEN_C, 5)
        self.play(FadeIn(ax2), ShowCreation(bound))
        self.play(LaggedStart(*[ShowCreation(l) for l in lines], lag_ratio=0.3), FadeIn(labs), run_time=2)
        self.finish()

        self.recap("3.4", ["Is bounded scalar curvature", "enough to keep going?"])


# ---------------------------------------------------------------------------
# Chapter 4 — the claims
# ---------------------------------------------------------------------------

class C4Claims(Video):
    def construct(self):
        self.chapter(3, "4. The claims")
        self.narrate("4.1")
        c = card(["dimension 4:", "bounded scalar curvature ⇒ the flow continues smoothly"], width=10, size=30,
                 color=GREEN_C).move_to(0.6 * UP)
        self.play(FadeIn(c))
        self.finish()
        self.play(FadeOut(c))

        self.narrate("4.2")
        collar = DashedVMobject(Circle(radius=2.3)).set_stroke(TEAL_C, 3).move_to(0.4 * UP)
        root = Circle(radius=1.2).set_stroke(BLUE_C, 4).set_fill(GREY_E, 0.6).move_to(0.4 * UP)
        kids = VGroup(*[Circle(radius=r).set_stroke(PURPLE_B, 3).move_to(0.4 * UP + np.array([x, y, 0]))
                        for x, y, r in [(-0.45, -0.2, 0.33), (0.5, 0.15, 0.22), (0.35, -0.55, 0.12)]])
        tiny = Circle(radius=0.1).set_stroke(ORANGE, 2).move_to(0.4 * UP + np.array([-0.5, -0.25, 0]))
        rl = txt("outermost piece, size a", 22, BLUE_C).next_to(root, UP, buff=0.12)
        cl = txt("collar", 22, TEAL_C).next_to(collar, RIGHT, buff=0.15)
        self.play(FadeIn(root), FadeIn(rl))
        self.cue("nested inside")
        self.play(LaggedStart(*[ShowCreation(k) for k in kids], lag_ratio=0.3), ShowCreation(tiny))
        self.play(ShowCreation(collar), FadeIn(cl))
        self.finish()

        self.narrate("4.3")
        eq = Tex(R"cK^2 \le o(1)(K+1)^2", font_size=48).move_to(4.0 * RIGHT + 1.6 * UP)
        k0 = Tex(R"\Rightarrow\ K \to 0", font_size=48, color=YELLOW).next_to(eq, DOWN, buff=0.35)
        fr = txt("size a cannot keep shrinking", 26, GREEN_C).next_to(k0, DOWN, buff=0.4)
        grp = VGroup(collar, root, kids, tiny, rl, cl)
        self.play(grp.animate.scale(0.8).shift(3.0 * LEFT))
        self.play(Write(eq))
        self.play(FadeIn(k0))
        self.cue("So the tear")
        self.play(FadeIn(fr))
        self.finish()
        self.clear_content()

        self.narrate("4.4")
        c2 = card(["dimension 13 and up: a flow on S² × S^(q+1)",
                   "with bounded scalar curvature that still blows up"], width=10.5, size=28, color=ORANGE)
        c2.move_to(0.6 * UP)
        self.play(FadeIn(c2))
        self.finish()
        self.play(FadeOut(c2))

        self.narrate("4.5")
        ax = Chart((0, 1), (0, 1.3), 8.0, 3.0, grid=False, xlabel="position along the line")
        ax.shift(0.45 * UP - ax.box.get_center())
        tr = ValueTracker(0.0)
        r1 = always_redraw(lambda: curve(ax, lambda x: 0.5 + 0.35 * math.sin(math.pi * x) * (1 - 0.6 * tr.get_value()),
                                          0, 1, color=BLUE_C, width=4))
        r2 = always_redraw(lambda: curve(ax, lambda x: max(0.02, 1.1 * math.sin(math.pi * x) ** 0.6
                                                           * (x ** (tr.get_value() * 0.8))), 0, 1,
                                          color=ORANGE, width=4))
        keys = VGroup(txt("radius of S²", 20, BLUE_C), txt("radius of the big sphere", 20, ORANGE))
        keys.arrange(RIGHT, buff=0.6).next_to(ax.box, UP, buff=0.15)
        cone = txt("a cone forms here (schematic)", 22, YELLOW).next_to(ax.c2p(0, 0.15), RIGHT, buff=0.3)
        self.add(ax, r1, r2, keys)
        self.play(tr.animate.set_value(1.0), run_time=3)
        r1.clear_updaters()
        r2.clear_updaters()
        self.play(FadeIn(cone))
        self.finish()

        self.recap("4.6", ["Claimed: yes in four dimensions,", "no in high dimensions."])


# ---------------------------------------------------------------------------
# Chapter 5 — is it right?
# ---------------------------------------------------------------------------

class C5Close(Video):
    def construct(self):
        self.chapter(4, "5. Is it right?")
        self.narrate("5.1")
        items = VGroup(txt("no computer-checked proof", 30, ORANGE), txt("no expert assessment found yet", 30, ORANGE),
                       txt("the 4D proof uses a companion paper", 30, GREY_A)).arrange(DOWN, buff=0.35)
        items.move_to(0.6 * UP)
        self.play(FadeIn(items[0]))
        self.cue("and we found")
        self.play(FadeIn(items[1]))
        self.cue("The four-dimensional")
        self.play(FadeIn(items[2]))
        self.finish()
        self.clear_content()

        self.narrate("5.2")
        a = txt("✓  Poincaré conjecture: proved by Perelman", 32, GREEN_C).move_to(1.2 * UP)
        b = txt("these papers: its tool, in four dimensions and up", 30, GREY_A).next_to(a, DOWN, buff=0.5)
        self.play(FadeIn(a))
        self.play(FadeIn(b))
        self.finish()
        self.clear_content()

        self.narrate("5.3")
        self.play(FadeOut(self.roadmap_mob))
        title = txt("Scalar Curvature and Ricci Flow", 50)
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
        title = txt("Can a Shape Tear Quietly?", 60).to_edge(UP, buff=0.6)
        sub = txt("Ricci flow and scalar curvature, explained for everyone", 30, GREY_A).next_to(title, DOWN, buff=0.25)
        db = dumbbell(0.97, center=1.2 * DOWN + 2.2 * LEFT, width=7.0)
        d = dial(0.25, center=1.6 * DOWN + 4.6 * RIGHT)
        self.add(title, sub, db, d)
