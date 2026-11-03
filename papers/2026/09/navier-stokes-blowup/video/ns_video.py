"""Narrated explainer for "Finite Time Blowup for Navier–Stokes" (OpenAI,
September 2026), written for 3b1b's manim (manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("5.3") and
the words come from beat 5.3 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl ns_video.py C5Core -w -l --config_file ../../../../../tools/video/custom_config.yml
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "video"))
from narrated import *  # noqa: E402,F403

CORE = ORANGE
ANNULUS = RED_C
EXTERIOR = BLUE_C
FLUID = BLUE_B
FAMILY1 = TEAL_C
FAMILY2 = PURPLE_B
H = 0.005  # illustrative exponent, 0 < h < 1/100 in the paper


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["The equations", "The question", "The claim", "How it works", "Is it right?"]
    PRONOUNCE = [(r"\bLeray\b", "Luh-ray"), (r"\bMartínez-Zoroa\b", "Marteenez Zoroa"),
                 (r"\bCircelli\b", "Cheer-chelly"), (r"\bBastounis\b", "Bas-toonis"), (r"\bCórdoba\b", "Cordoba"),
                 (r"\bNavier–Stokes\b", "Navier Stokes"), (r"\b1934\b", "nineteen thirty-four"),
                 (r"\b2026\b", "twenty twenty-six")]
    BUILD = HERE / "build"


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def swirl_field(center=ORIGIN, strength=1.0, tight=1.0, nx=13, ny=7, dx=0.95, color=FLUID):
    """A grid of arrows for a swirl around `center`: speed grows toward the
    centre as `tight` grows (capped so arrows stay short)."""
    arrows = VGroup()
    for i in range(nx):
        for j in range(ny):
            p = np.array([(i - (nx - 1) / 2) * dx, (j - (ny - 1) / 2) * dx, 0])
            d = p - center
            r = max(np.linalg.norm(d), 0.25)
            speed = strength * max(0.35, min(1.0, tight / (r + 0.3)))
            v = np.array([-d[1], d[0], 0]) / r * speed * 0.45
            if np.linalg.norm(v) < 0.05:
                continue
            arrows.add(Arrow(p - v / 2, p + v / 2, buff=0, fill_color=color, thickness=2.5,
                             max_tip_length_to_length_ratio=0.35))
    return arrows


def eq_terms():
    """The equation as separately coloured terms."""
    parts = [(R"\partial_t u", WHITE), ("+", WHITE), (R"(u\cdot\nabla)u", YELLOW), ("=", WHITE),
             (R"\nu\Delta u", BLUE_B), ("-", WHITE), (R"\nabla p", GREEN_B), ("+", WHITE), ("f", ORANGE)]
    row = VGroup(*[Tex(t, font_size=64).set_color(c) for t, c in parts]).arrange(RIGHT, buff=0.25)
    return row


def core_side(width=1.6, height=2.6, center=ORIGIN):
    """Side view of the core: an axis, the core's outline, inflow and axial outflow."""
    axis = DashedLine(center + 3.2 * DOWN, center + 3.2 * UP).set_stroke(GREY_B, 2)
    outline = Ellipse(width=width, height=height).set_stroke(CORE, 3).set_fill(CORE, 0.15).move_to(center)
    inflow = VGroup()
    for side in (-1, 1):
        for y in (-0.25, 0.25):
            a = center + np.array([side * (width / 2 + 0.9), y, 0])
            b = center + np.array([side * (width / 2 + 0.1), y, 0])
            inflow.add(Arrow(a, b, buff=0, fill_color=FLUID, thickness=3))
    outflow = VGroup(Arrow(center + 0.3 * UP, center + (height / 2 + 0.8) * UP, buff=0, fill_color=YELLOW, thickness=4),
                     Arrow(center + 0.3 * DOWN, center + (height / 2 + 0.8) * DOWN, buff=0, fill_color=YELLOW,
                           thickness=4))
    return VGroup(axis, outline, inflow, outflow)


def regions(r_core=0.9, r_in=1.3, r_out=2.0, r_ext=3.0, center=ORIGIN):
    """Top view: core, annulus, exterior."""
    ext = Circle(radius=r_ext).set_stroke(EXTERIOR, 2).set_fill(EXTERIOR, 0.08).move_to(center)
    ann = Annulus(inner_radius=r_in, outer_radius=r_out).set_fill(ANNULUS, 0.25).set_stroke(ANNULUS, 2)
    ann.move_to(center)
    core = Circle(radius=r_core).set_stroke(CORE, 3).set_fill(CORE, 0.3).move_to(center)
    labels = VGroup(txt("core", 24).move_to(center),
                    txt("annulus", 24).move_to(center + (r_in + r_out) / 2 * UP),
                    txt("exterior", 24).move_to(center + (r_out + r_ext) / 2 * UP + 0.05 * UP))
    g = VGroup(ext, ann, core, labels)
    g.ext, g.ann, g.core, g.labels = ext, ann, core, labels
    return g


def ripple_ring(radius=1.65, amp=0.06, freq=14, color=FAMILY1, center=ORIGIN):
    return ParametricCurve(lambda s: center + np.array([(radius + amp * math.sin(freq * s)) * math.cos(s),
                                                        (radius + amp * math.sin(freq * s)) * math.sin(s), 0]),
                           t_range=(0, TAU, TAU / 600)).set_stroke(color, 3)


def envelope(v):
    """Growth then viscous decay of a pulse (schematic), v in [0, 1]."""
    return math.exp(-((v - 0.5) / 0.17) ** 2)


def speed_chart(width=5.6, height=3.2, label="top speed"):
    return Chart((0.3, 1.0), (0, 10), width, height, xticks=(0.4, 0.6, 0.8, 1.0),
                 xfmt=lambda v: txt(f"{v:.1f}", 18, GREY_B), xlabel="time", ylabel=label, grid=False)


def on(t, start=0.38, width=0.2):
    if t <= start:
        return 0.0
    z = min(1.0, (t - start) / width)
    a = math.exp(-1 / z) if z > 0 else 0.0
    b = math.exp(-1 / (1 - z)) if z < 1 else 0.0
    return a / (a + b)


def blowup_speed(t):
    return 1.2 * on(t) * (1 - t) ** -(0.5 + H) if t < 1 else 50


def force_bump(t, a=0.42, b=1.9):
    if t <= a or t >= b:
        return 0.0
    z = (t - a) / (b - a)
    return math.exp(1 - 1 / (1 - (2 * z - 1) ** 2))


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        tight = ValueTracker(0.6)
        field = always_redraw(lambda: swirl_field(tight=tight.get_value()).shift(0.3 * UP))
        self.narrate("0.1")
        self.play(FadeIn(field), run_time=2)
        self.finish()

        self.narrate("0.2")
        self.cue("can a smooth flow")
        self.play(tight.animate.set_value(3.0), run_time=5, rate_func=smooth)
        self.finish()

        self.narrate("0.3")
        title = txt("Finite Time Blowup for Navier–Stokes", 54)
        sub = txt("OpenAI preprint, September 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(field), Write(title, run_time=2))
        self.play(FadeIn(sub))
        self.finish()
        self.clear_caption()

        self.narrate("0.4")
        big = self.roadmap(None, big=True).move_to(1.5 * DOWN)
        self.play(title.animate.shift(UP), sub.animate.shift(UP), FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — the equations
# ---------------------------------------------------------------------------

class C1Equations(Video):
    def construct(self):
        self.chapter(0, "1. The equations")
        field = swirl_field(tight=0.8).shift(0.3 * UP)

        self.narrate("1.1")
        self.play(FadeIn(field))
        one = field[len(field) // 2 + 3]
        lab = txt("velocity", 26, YELLOW).next_to(one, UP, buff=0.15)
        self.play(one.animate.set_fill(YELLOW), FadeIn(lab))
        self.finish()
        self.play(FadeOut(VGroup(field, lab)))

        def effect_card(n, name, color):
            c = card([f"{n}. {name}"], width=8, size=30).to_edge(UP, buff=0.9)
            c[0].set_stroke(color, 3)
            c[1].set_color(color)
            return c

        # 1. carried along
        self.narrate("1.2")
        c1 = effect_card(1, "The fluid carries itself along", YELLOW)
        self.play(FadeIn(c1))
        blob = VGroup(*[Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, fill_color=YELLOW, thickness=4).move_to(
            np.array([x, y, 0])) for x in (-0.6, 0.6) for y in (-0.4, 0.4)]).move_to(4 * LEFT + 0.3 * DOWN)
        stream = VGroup(*[Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, fill_color=GREY_C, thickness=2).move_to(
            np.array([x, y, 0])) for x in np.arange(-6, 6.1, 1.2) for y in (-1.5, -0.3, 0.9)])
        self.play(FadeIn(stream), FadeIn(blob))
        self.cue("Fast water")
        self.play(blob.animate.shift(8 * RIGHT), run_time=4, rate_func=linear)
        self.finish()
        self.play(FadeOut(VGroup(stream, blob, c1)))

        # 2. friction
        self.narrate("1.3")
        c2 = effect_card(2, "Friction smooths things out", BLUE_B)
        ax = Chart((-3, 3), (0, 1.2), 7, 3.0, grid=False, xlabel="position across the flow", ylabel="speed")
        ax.shift(0.3 * DOWN - ax.box.get_center())
        width = ValueTracker(0.15)
        prof = always_redraw(lambda: curve(ax, lambda x: math.exp(-x * x / (2 * width.get_value() ** 2)) *
                                           (0.15 / width.get_value()) ** 0.5, -3, 3, n=300, color=BLUE_B,
                                           ylim=(-0.1, 1.25)))
        self.play(FadeIn(c2), FadeIn(ax), FadeIn(prof))
        self.cue("Neighbouring bits")
        self.play(width.animate.set_value(0.9), run_time=4)
        self.cue("high for honey")
        honey = txt("viscosity: honey high, water low", 26, GREY_A).next_to(ax.box, UP, buff=0.2)
        self.play(FadeIn(honey))
        self.finish()
        self.remove(prof)
        self.play(FadeOut(VGroup(c2, ax, honey)))

        # 3. pressure
        self.narrate("1.4")
        c3 = effect_card(3, "Pressure keeps the volume fixed", GREEN_B)
        sq = Square(2.0).set_fill(GREEN_E, 0.6).set_stroke(GREEN_B, 3).shift(0.3 * DOWN)
        area = txt("area stays the same", 26, GREY_A).next_to(sq, DOWN, buff=0.5)
        self.play(FadeIn(c3), FadeIn(sq))
        self.cue("Squash a blob")
        self.play(sq.animate.stretch(0.5, 1).stretch(2.0, 0), FadeIn(area), run_time=2)
        self.finish()
        self.play(FadeOut(VGroup(c3, sq, area)))

        # 4. force
        self.narrate("1.5")
        c4 = effect_card(4, "An outside force", ORANGE)
        field = swirl_field(tight=0.5, strength=0.6).scale(0.8).shift(0.2 * DOWN)
        push = Arrow(5.5 * LEFT + 0.3 * DOWN, 2.5 * LEFT + 0.3 * DOWN, buff=0, fill_color=ORANGE, thickness=8)
        self.play(FadeIn(c4), FadeIn(field))
        self.play(GrowArrow(push))
        self.finish()
        self.play(FadeOut(VGroup(c4, field, push)))

        # the equation
        self.narrate("1.6")
        eq = eq_terms().move_to(0.8 * UP)
        names = [("time change", 0, WHITE), ("carried along", 2, YELLOW), ("friction", 4, BLUE_B),
                 ("pressure", 6, GREEN_B), ("force", 8, ORANGE)]
        labels = VGroup(*[txt(n, 22, c).next_to(eq[i], DOWN, buff=0.45) for n, i, c in names])
        for lab_ in labels:
            lab_.set_y(eq.get_bottom()[1] - 0.6)
        self.play(Write(eq), run_time=2)
        self.play(FadeIn(labels, lag_ratio=0.2))
        self.cue("the tug of war")
        self.play(Indicate(eq[2], color=YELLOW, scale_factor=1.25), Indicate(eq[4], color=BLUE_B, scale_factor=1.25),
                  run_time=2)
        self.finish()

        self.recap("1.7", ["A velocity at every point.",
                           "Four effects: carried along, friction, pressure, and an outside force."])


# ---------------------------------------------------------------------------
# Chapter 2 — the question
# ---------------------------------------------------------------------------

def options_grid():
    cells = VGroup()
    texts = {"A": "every smooth start,\nno force", "B": "every smooth start,\nno force",
             "C": "one example,\na smooth fading force", "D": "one example,\na smooth fading force"}
    for k, letter in enumerate("ABCD"):
        col, row = k % 2, k // 2
        box = RoundedRectangle(width=4.6, height=1.7, corner_radius=0.15).set_stroke(GREY_B, 2).set_fill(GREY_E, 0.5)
        box.move_to(np.array([-1.1 + 4.9 * col, 0.85 - 2.0 * row, 0]))
        head = txt(f"({letter})", 32).move_to(box.get_corner(UL) + np.array([0.5, -0.35, 0]))
        body = txt(texts[letter], 24, GREY_A).move_to(box).shift(0.15 * DOWN + 0.25 * RIGHT)
        cells.add(VGroup(box, head, body))
    cols = VGroup(txt("all of space", 26, GREY_A).next_to(cells[0], UP, buff=0.2),
                  txt("a box that wraps around", 26, GREY_A).next_to(cells[1], UP, buff=0.2))
    rows = VGroup(txt("smooth\nforever", 26, GREY_A).next_to(cells[0], LEFT, buff=0.3),
                  txt("breaks\ndown", 26, GREY_A).next_to(cells[2], LEFT, buff=0.3))
    g = VGroup(cells, cols, rows)
    g.cells = cells
    return g


class C2Question(Video):
    def construct(self):
        self.chapter(1, "2. The question")
        ax = Chart((-3, 3), (0, 6), 7.5, 3.6, grid=False, xlabel="position", ylabel="speed")
        ax.shift(0.4 * UP - ax.box.get_center())
        sharp = ValueTracker(1.0)
        def bell(x):
            s = sharp.get_value()
            return 1.2 * s * math.exp(-x * x * s * s / 2)
        # two monotone halves, so the spike is cut cleanly where it leaves the chart
        prof = always_redraw(lambda: VGroup(*[curve(ax, bell, a, b, n=300, color=ORANGE, ylim=(-0.1, 6.0))
                                              for a, b in ((-3, 0), (0, 3))]))
        self.narrate("2.1")
        self.play(FadeIn(ax), FadeIn(prof))
        self.finish()

        self.narrate("2.2")
        clock = txt("time → 1", 28, GREY_A).next_to(ax.box, UR, buff=0.1).shift(0.4 * DOWN + 0.3 * LEFT)
        self.cue("Or can")
        self.play(FadeIn(clock))
        self.play(sharp.animate.set_value(9), run_time=5, rate_func=rush_into)
        self.finish()

        self.narrate("2.3")
        lab = txt("blowup", 40, RED_C).next_to(ax.c2p(0, 6), RIGHT, buff=0.4)
        self.play(FadeIn(lab, scale=1.4))
        self.finish()
        self.remove(prof)
        self.play(FadeOut(VGroup(ax, clock, lab)))

        self.narrate("2.4")
        line = Line(6 * LEFT, 6 * RIGHT).set_stroke(GREY_B, 2).shift(0.2 * UP)
        events = [(-5.2, "1934", "Leray:\nweak solutions"), (-2.6, "1982", "Caffarelli, Kohn,\nNirenberg"),
                  (0.0, "2000", "the prize"), (2.6, "2016", "Tao: a\nmodified equation"),
                  (5.2, "recent", "Córdoba, Martínez-Zoroa,\nZheng")]
        marks = VGroup()
        for x, year, what in events:
            d = Dot(np.array([x, 0.2, 0]), radius=0.09, fill_color=YELLOW)
            y = txt(year, 26, YELLOW).next_to(d, UP, buff=0.2)
            w = txt(what, 20, GREY_A).next_to(d, DOWN, buff=0.25)
            marks.add(VGroup(d, y, w))
        self.play(ShowCreation(line))
        for m, phrase in zip(marks, ["since Jean Leray", "confined to a tiny", "confined to a tiny",
                                     "We know blowups", "and in related equations"]):
            self.cue(phrase)
            self.play(FadeIn(m, shift=0.1 * UP), run_time=0.6)
        self.finish()
        self.play(FadeOut(VGroup(line, marks)))

        self.narrate("2.5")
        prize = card(["Clay Millennium Prize Problem", "$1,000,000"], width=8, size=34).move_to(0.4 * UP)
        self.play(FadeIn(prize))
        self.finish()
        self.play(FadeOut(prize))

        self.narrate("2.6")
        grid = options_grid().shift(0.15 * UP)
        self.play(FadeIn(grid.submobjects[1]), FadeIn(grid.submobjects[2]))
        self.play(LaggedStart(*[FadeIn(c) for c in grid.cells], lag_ratio=0.3, run_time=2))
        self.finish()

        self.narrate("2.7")
        self.play(*[c[0].animate.set_stroke(YELLOW, 4) for c in grid.cells[:2]])
        self.finish()

        self.narrate("2.8")
        self.play(*[c[0].animate.set_stroke(GREY_B, 2) for c in grid.cells[:2]],
                  *[c[0].animate.set_stroke(BLUE_C, 5).set_fill(BLUE_E, 0.6) for c in grid.cells[2:]])
        self.cue("The paper claims")
        claimed = VGroup(*[txt("claimed", 26, YELLOW).move_to(c[0].get_corner(UR) + np.array([-0.75, -0.3, 0]))
                           for c in grid.cells[2:]])
        self.play(FadeIn(claimed))
        self.finish()

        self.recap("2.9", ["Blowup: infinite speed in a finite time.",
                           "The paper claims the breakdown options, C and D."])


# ---------------------------------------------------------------------------
# Chapter 3 — why the force is not a cheat
# ---------------------------------------------------------------------------

class C3Force(Video):
    def construct(self):
        self.chapter(2, "3. Why the force is not a cheat")
        left = Chart((0.3, 2.0), (0, 10), 5.4, 3.3, grid=False, xlabel="time")
        left.shift(3.4 * LEFT + 0.2 * UP - left.box.get_center())
        one = DashedLine(left.c2p(1, 0), left.c2p(1, 10)).set_stroke(GREY_B, 1.5)
        speed = curve(left, blowup_speed, 0.3, 0.995, n=400, color=ORANGE, width=5, ylim=(-0.1, 10.2))
        sl = txt("fluid speed", 24, ORANGE).next_to(left.c2p(1.08, 8.6), RIGHT, buff=0)
        self.narrate("3.1")
        self.play(FadeIn(left), ShowCreation(one))
        self.play(ShowCreation(speed, run_time=2), FadeIn(sl))
        self.cue("call whatever is left")
        need = curve(left, lambda t: 0.9 * on(t) * (1 - t) ** -1.6 if t < 1 else 99, 0.3, 0.99, n=400,
                     color=RED_C, width=5, ylim=(-0.1, 10.2))
        nl = txt("force you would need", 24, RED_C).next_to(left.c2p(1.08, 7.2), RIGHT, buff=0)
        self.play(ShowCreation(need, run_time=2), FadeIn(nl))
        self.finish()

        self.narrate("3.2")
        self.cue("The force itself must be")
        cross = Cross(need, stroke_color=RED_C)
        self.play(ShowCreation(cross))
        self.finish()

        self.narrate("3.3")
        right = Chart((0.3, 2.0), (0, 10), 5.4, 3.3, grid=False, xlabel="time")
        right.shift(3.4 * RIGHT + 0.2 * UP - right.box.get_center())
        one2 = DashedLine(right.c2p(1, 0), right.c2p(1, 10)).set_stroke(GREY_B, 1.5)
        speed2 = curve(right, blowup_speed, 0.3, 0.995, n=400, color=ORANGE, width=5, ylim=(-0.1, 10.2))
        force = curve(right, lambda t: 3.0 * force_bump(t), 0.3, 2.0, n=300, color=BLUE_C, width=5)
        fl = txt("smooth force", 22, BLUE_C).next_to(right.c2p(1.3, 3.4), RIGHT, buff=0)
        self.play(FadeIn(right), ShowCreation(one2))
        self.play(ShowCreation(force, run_time=2), FadeIn(fl))
        self.cue("Each term")
        sl2 = txt("fluid speed", 24, ORANGE).next_to(right.c2p(1.08, 8.6), RIGHT, buff=0)
        self.play(ShowCreation(speed2, run_time=2), FadeIn(sl2))
        self.finish()

        self.recap("3.4", ["The force must stay smooth at the moment of blowup.",
                           "That is the whole difficulty."])


# ---------------------------------------------------------------------------
# Chapter 4 — the claim
# ---------------------------------------------------------------------------

class C4Claim(Video):
    def construct(self):
        self.chapter(2, "4. The claim")
        items = ["The fluid starts at rest.", "A smooth force, in a bounded region, for a bounded time.",
                 "Smooth up to time 1, with bounded energy.", "Speed grows without limit as time approaches 1.",
                 "No smooth solution can continue forever."]
        lines = VGroup(*[txt("•  " + s, 30) for s in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        lines.move_to(0.5 * UP)
        for k, beat in enumerate(["4.1", "4.2", "4.3", "4.4", "4.5"]):
            self.narrate(beat)
            self.play(FadeIn(lines[k], shift=0.15 * RIGHT))
            if k == 3:
                self.play(lines[k].animate.set_color(ORANGE))
            self.finish()
        self.play(FadeOut(lines))

        self.narrate("4.6")
        a = speed_chart(5.4, 3.0)
        a.shift(3.3 * LEFT + 0.3 * UP - a.box.get_center())
        b = Chart((0.3, 1.0), (0, 1.5), 5.4, 3.0, xticks=(0.4, 0.6, 0.8, 1.0),
                  xfmt=lambda v: txt(f"{v:.1f}", 18, GREY_B), xlabel="time", ylabel="total energy", grid=False)
        b.shift(3.3 * RIGHT + 0.3 * UP - b.box.get_center())
        sp = curve(a, blowup_speed, 0.3, 0.996, n=500, color=ORANGE, width=5, ylim=(-0.1, 10.2))
        en = curve(b, lambda t: on(t) * (1 - 0.15 * (1 - t) ** (0.5 - 2 * H)), 0.3, 1.0, n=300, color=BLUE_C,
                   width=5)
        self.play(FadeIn(a), FadeIn(b))
        self.play(ShowCreation(sp), ShowCreation(en), run_time=3)
        self.cue("Because the fast motion")
        shrink = Circle(radius=1.0).set_stroke(ORANGE, 3).move_to(a.c2p(0.95, 7.5))
        self.play(FadeIn(shrink))
        self.play(shrink.animate.scale(0.15), run_time=2.5)
        self.finish()

        self.recap("4.7", ["From rest, a smooth push, finite energy,", "and infinite speed at time 1."])


# ---------------------------------------------------------------------------
# Chapter 5 — the collapsing vortex
# ---------------------------------------------------------------------------

class C5Core(Video):
    def construct(self):
        self.chapter(3, "5. How it works: the collapsing vortex")
        reg = regions(r_ext=2.7).shift(0.1 * UP)
        self.narrate("5.1")
        self.cue("a collapsing core")
        self.play(FadeIn(reg.core), FadeIn(reg.labels[0]))
        self.cue("a ring-shaped zone")
        self.play(FadeIn(reg.ann), FadeIn(reg.labels[1]))
        self.cue("a calm exterior")
        self.play(FadeIn(reg.ext), FadeIn(reg.labels[2]))
        self.finish()
        self.play(FadeOut(reg))

        self.narrate("5.2")
        side = core_side(center=2.6 * LEFT + 0.2 * DOWN)
        axis, outline, inflow, outflow = side
        self.play(ShowCreation(axis), FadeIn(outline))
        self.cue("fluid spirals inward")
        self.play(LaggedStart(*[GrowArrow(a) for a in inflow], lag_ratio=0.2))
        self.finish()

        self.narrate("5.3")
        center = 3.4 * RIGHT + 0.2 * DOWN
        ring = Circle(radius=1.8).set_stroke(GREY_D, 1).move_to(center)
        top_lab = txt("seen from above", 22, GREY_A).next_to(ring, UP, buff=0.15)
        rad = ValueTracker(1.8)
        ang = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(center + rad.get_value() * np.array(
            [math.cos(ang.get_value()), math.sin(ang.get_value()), 0]), radius=0.12, fill_color=YELLOW))
        trail = always_redraw(lambda: Circle(radius=rad.get_value()).set_stroke(YELLOW, 1.5, opacity=0.5).move_to(
            center))
        self.play(FadeIn(ring), FadeIn(top_lab), FadeIn(dot), FadeIn(trail))
        # angular momentum: r * v = const, so the angle advances like 1 / r^2
        steps = 60
        for k in range(steps):
            r_now = 1.8 - 1.4 * (k + 1) / steps
            self.play(rad.animate.set_value(r_now), ang.animate.increment_value(0.12 * (1.8 / r_now) ** 2),
                      run_time=6 / steps, rate_func=linear)
        self.finish()

        self.narrate("5.4")
        self.play(LaggedStart(*[GrowArrow(a) for a in outflow], lag_ratio=0.3))
        self.finish()
        self.remove(dot, trail)
        self.play(FadeOut(VGroup(ring, top_lab, side)))

        self.narrate("5.5")
        tau = ValueTracker(0.5)

        def column():
            t = tau.get_value()
            w = 3.2 * (t / 0.5) ** 0.5
            h = 4.4 * (t / 0.5) ** (0.5 - 0.15)
            e = Ellipse(width=max(w, 0.05), height=max(h, 0.1)).set_stroke(CORE, 3).set_fill(CORE, 0.3)
            return e.move_to(2.5 * LEFT + 0.3 * DOWN)

        col = always_redraw(column)
        axis2 = DashedLine(2.5 * LEFT + 3.0 * DOWN, 2.5 * LEFT + 2.6 * UP).set_stroke(GREY_B, 2)
        wl = txt("width: like the square root of the time left", 24, GREY_A).move_to(2.6 * RIGHT + 1.7 * UP)
        hl = txt("height: a little more slowly", 24, GREY_A).next_to(wl, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(ShowCreation(axis2), FadeIn(col))
        self.cue("Its width")
        self.play(FadeIn(wl))
        self.cue("Its height")
        self.play(FadeIn(hl))
        self.play(tau.animate.set_value(0.01), run_time=5, rate_func=smooth)
        self.finish()

        self.narrate("5.6")
        meter = speed_chart(4.6, 2.3, "swirl speed")
        meter.shift(3.0 * RIGHT + 0.8 * DOWN - meter.box.get_center())
        sp = curve(meter, blowup_speed, 0.3, 0.996, n=500, color=ORANGE, width=5, ylim=(-0.1, 10.2))
        self.play(FadeIn(meter))
        self.play(ShowCreation(sp), run_time=4)
        self.finish()

        self.recap("5.7", ["The core: a slender spinning column", "that narrows and spins up, faster and faster."])


# ---------------------------------------------------------------------------
# Chapter 6 — the seam and the pulses
# ---------------------------------------------------------------------------

class C6Pulses(Video):
    def construct(self):
        self.chapter(3, "6. How it works: pulses and corrections")
        reg = regions(r_ext=2.7).shift(2.6 * LEFT + 0.1 * UP)
        c = reg.core.get_center()

        self.narrate("6a.1")
        self.play(FadeIn(reg))
        self.cue("But joining")
        imb = txt("imbalance", 28, RED_C).next_to(reg, RIGHT, buff=0.4).shift(1.2 * UP)
        self.play(reg.ann.animate.set_fill(ANNULUS, 0.6), FadeIn(imb))
        self.finish()

        self.narrate("6a.2")
        ch = Chart((0.3, 1.0), (0, 10), 4.6, 2.6, grid=False, xlabel="time", ylabel="force needed")
        ch.shift(3.6 * RIGHT + 1.0 * DOWN - ch.box.get_center())
        need = curve(ch, lambda t: 0.6 * on(t) * (1 - t) ** -1.3 if t < 1 else 99, 0.3, 0.995, n=400,
                     color=RED_C, width=5, ylim=(-0.1, 10.2))
        self.play(FadeIn(ch), ShowCreation(need, run_time=2))
        self.cue("That is exactly the cheat")
        self.play(ShowCreation(Cross(VGroup(ch, need), stroke_color=RED_C)))
        self.finish()
        self.clear_content(reg)

        # 6b — pulses
        self.narrate("6b.1")
        rip = ripple_ring(center=c)
        self.play(ShowCreation(rip), reg.labels[1].animate.set_opacity(0), run_time=2)
        self.finish()

        self.narrate("6b.2")
        env = Chart((0, 1), (0, 1.1), 4.6, 2.4, grid=False, xlabel="time within one pulse", ylabel="size")
        env.shift(3.6 * RIGHT + 1.3 * UP - env.box.get_center())
        grow = curve(env, envelope, 0, 0.5, n=100, color=FAMILY1, width=5)
        self.play(FadeIn(env))
        self.cue("Then the background")
        self.play(ShowCreation(grow), rip.animate.set_stroke(width=5), run_time=2)
        self.finish()

        self.narrate("6b.3")
        parcel = Dot(c + 1.45 * RIGHT, radius=0.13, fill_color=YELLOW)
        spin = Arc(radius=0.3, start_angle=0, angle=1.6 * PI).set_stroke(YELLOW, 3).add_tip()
        spin.move_to(parcel)
        self.play(FadeIn(parcel), ShowCreation(spin))
        self.cue("a bit of fluid nudged outward")
        self.play(parcel.animate.shift(0.25 * RIGHT), spin.animate.shift(0.25 * RIGHT))
        self.cue("flings it further out")
        fling = Arrow(parcel.get_center(), parcel.get_center() + 1.2 * RIGHT, buff=0.15, fill_color=YELLOW,
                      thickness=5)
        self.play(GrowArrow(fling), parcel.animate.shift(0.35 * RIGHT), spin.animate.shift(0.35 * RIGHT))
        self.finish()
        self.play(FadeOut(VGroup(parcel, spin, fling)))

        self.narrate("6b.4")
        stripes = VGroup(*[Line(UP * 0.9, DOWN * 0.9).set_stroke(FAMILY1, 3).shift(RIGHT * 0.25 * k)
                           for k in range(-4, 5)])
        frame = Rectangle(width=2.6, height=1.9).set_stroke(GREY_B, 1.5)
        patch = VGroup(frame, stripes).move_to(3.6 * RIGHT + 1.4 * DOWN)
        plab = txt("the ripple, close up", 20, GREY_A).next_to(patch, DOWN, buff=0.15)
        self.play(FadeIn(patch), FadeIn(plab))
        self.cue("tilts the ripples")
        self.play(stripes.animate.apply_matrix([[1, 0.9], [0, 1]], about_point=frame.get_center()).stretch(0.55, 0), run_time=2.5)
        self.cue("until friction wins")
        decay = curve(env, envelope, 0.5, 1.0, n=100, color=FAMILY1, width=5)
        self.play(ShowCreation(decay), stripes.animate.set_stroke(opacity=0.25), rip.animate.set_stroke(width=2),
                  run_time=2)
        self.finish()
        self.play(FadeOut(VGroup(patch, plab, env, grow, decay)))

        self.narrate("6b.5")
        p_out = Dot(c + 1.5 * RIGHT + 0.5 * UP, radius=0.13, fill_color=BLUE_C)
        p_in = Dot(c + 1.5 * RIGHT + 0.5 * DOWN, radius=0.13, fill_color=ORANGE)
        m_out = Arrow(p_out.get_center(), p_out.get_center() + 0.9 * RIGHT, buff=0.1, fill_color=BLUE_C, thickness=4)
        m_in = Arrow(p_in.get_center(), p_in.get_center() + 0.9 * LEFT, buff=0.1, fill_color=ORANGE, thickness=4)
        t_out = txt("moving out, extra spin", 22, BLUE_C).move_to(3.8 * RIGHT + 1.6 * UP)
        t_in = txt("moving in, less spin", 22, ORANGE).move_to(3.8 * RIGHT + 0.9 * UP)
        self.play(FadeIn(p_out), FadeIn(p_in))
        self.cue("Fluid moving outward")
        self.play(GrowArrow(m_out), FadeIn(t_out))
        self.cue("and fluid moving inward")
        self.play(GrowArrow(m_in), FadeIn(t_in))
        self.cue("Either way")
        flux = Arrow(3.0 * RIGHT + 0.3 * DOWN, 5.4 * RIGHT + 0.3 * DOWN, buff=0, fill_color=YELLOW, thickness=7)
        fl = txt("spin carried outward", 26, YELLOW).next_to(flux, DOWN, buff=0.2)
        self.play(GrowArrow(flux), FadeIn(fl))
        self.finish()

        self.narrate("6b.6")
        self.play(reg.ann.animate.set_fill(ANNULUS, 0.08), FadeOut(VGroup(p_out, p_in, m_out, m_in)), run_time=3)
        self.finish()
        self.play(FadeOut(VGroup(t_out, t_in, flux, fl)))

        self.narrate("6b.7")
        o = 3.4 * RIGHT + 1.2 * DOWN
        v1 = Arrow(o, o + np.array([2.2, 1.0, 0]), buff=0, fill_color=FAMILY1, thickness=5)
        v2 = Arrow(o, o + np.array([0.6, 2.4, 0]), buff=0, fill_color=FAMILY2, thickness=5)
        cone = Polygon(o, o + np.array([2.2, 1.0, 0]) * 1.2, o + np.array([0.6, 2.4, 0]) * 1.2)
        cone.set_fill(GREY_C, 0.25).set_stroke(width=0)
        target = Arrow(o, o + np.array([1.5, 1.9, 0]), buff=0, fill_color=YELLOW, thickness=6)
        l1 = txt("family 1", 22, FAMILY1).next_to(v1.get_end(), RIGHT, buff=0.1)
        l2 = txt("family 2", 22, FAMILY2).next_to(v2.get_end(), UP, buff=0.1)
        lt = txt("needed", 22, YELLOW).next_to(target.get_end(), UR, buff=0.05)
        self.cue("two families")
        self.play(GrowArrow(v1), GrowArrow(v2), FadeIn(l1), FadeIn(l2),
                  ShowCreation(ripple_ring(radius=1.75, amp=0.05, freq=22, color=FAMILY2, center=c)))
        self.cue("the target always lies")
        self.play(FadeIn(cone), GrowArrow(target), FadeIn(lt))
        self.finish()
        self.play(FadeOut(VGroup(v1, v2, cone, target, l1, l2, lt)))

        self.narrate("6b.8")
        fine = VGroup(*[ripple_ring(radius=r, amp=0.04 * r, freq=f, color=FAMILY1 if k % 2 == 0 else FAMILY2,
                                    center=c) for k, (r, f) in enumerate([(1.1, 26), (0.75, 34), (0.5, 44)])])
        self.play(LaggedStart(*[ShowCreation(f) for f in fine], lag_ratio=0.5), reg.core.animate.scale(0.4),
                  run_time=4)
        self.finish()


class C6Rest(Video):
    def construct(self):
        self.keep_roadmap(3, "6. How it works: corrections, force, uniqueness")
        sub = self.subtitle("Correct, and correct again")
        self.play(FadeIn(sub))

        self.narrate("6c.1")
        ch = Chart((-0.5, 7.5), (-24, 0.5), 7.0, 3.6, xticks=range(0, 8), yticks=(-20, -15, -10, -5, 0),
                   yfmt=lambda k: Tex(f"10^{{{k}}}", font_size=24, color=GREY_B), xlabel="correction round",
                   ylabel="error left over", grid=True)
        ch.shift(0.4 * UP - ch.box.get_center())
        bars = VGroup()
        for k in range(8):
            top = -(k * (k + 1)) / 2.5
            b = Rectangle(width=0.55, height=max(0.02, ch.c2p(0, top)[1] - ch.c2p(0, -24)[1]))
            b.set_fill(BLUE_C, 1).set_stroke(width=0).move_to(ch.c2p(k, -24), aligned_edge=DOWN)
            bars.add(b)
        self.play(FadeIn(ch))
        self.play(GrowFromEdge(bars[0], DOWN))
        self.finish()

        self.narrate("6c.2")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1:]], lag_ratio=0.5, run_time=5))
        self.finish()
        self.play(FadeOut(VGroup(ch, bars, sub)))

        # 6d — exterior and force
        sub = self.subtitle("The calm exterior, and the force")
        self.play(FadeIn(sub))
        self.narrate("6d.1")
        rings = VGroup()
        for r in (0.8, 1.4, 2.0, 2.6):
            circ = Circle(radius=r).set_stroke(EXTERIOR, 2, opacity=0.6)
            arr = Arrow(np.array([r, -0.3 / r, 0]), np.array([r, 0.3 / r + 0.2, 0]), buff=0, fill_color=EXTERIOR,
                        thickness=3)
            rings.add(VGroup(circ, arr))
        rings.shift(2.6 * LEFT + 0.3 * DOWN)
        self.play(LaggedStart(*[FadeIn(r) for r in rings], lag_ratio=0.3))
        self.play(Rotate(rings, 0.4, about_point=rings.get_center()), run_time=3)
        self.finish()

        self.narrate("6d.2")
        fch = Chart((0, 2.2), (0, 1.2), 5.4, 2.8, xticks=(0, 1, 2), grid=False, xlabel="time", ylabel="force")
        fch.shift(3.4 * RIGHT + 0.2 * DOWN - fch.box.get_center())
        one = DashedLine(fch.c2p(1, 0), fch.c2p(1, 1.2)).set_stroke(GREY_B, 1.5)
        fc = curve(fch, force_bump, 0, 2.2, n=400, color=BLUE_C, width=5)
        self.play(FadeIn(fch), ShowCreation(one))
        self.cue("the force passes smoothly")
        self.play(ShowCreation(fc), run_time=3)
        self.finish()
        self.play(FadeOut(VGroup(rings, fch, one, fc, sub)))

        # 6e — uniqueness
        sub = self.subtitle("No other solution can escape")
        self.play(FadeIn(sub))
        self.narrate("6e.1")
        uch = Chart((0, 1.0), (0, 10), 7.0, 3.4, xticks=(0, 0.5, 1.0), grid=False, xlabel="time",
                    ylabel="speed")
        uch.shift(0.3 * UP - uch.box.get_center())
        built = curve(uch, lambda t: 1.0 * on(t, 0.2, 0.2) * (1 - t) ** -0.505 if t < 1 else 99, 0, 0.996, n=500,
                      color=ORANGE, width=6, ylim=(-0.1, 10.2))
        rival = built.copy().set_stroke(BLUE_C, 3)
        lb = txt("the constructed flow", 22, ORANGE).next_to(uch.c2p(0.05, 8.5), RIGHT, buff=0)
        lr = txt("any rival solution", 22, BLUE_C).next_to(uch.c2p(0.05, 7.4), RIGHT, buff=0)
        self.play(FadeIn(uch))
        self.play(ShowCreation(built), FadeIn(lb), run_time=2)
        self.cue("would have to coincide")
        self.play(ShowCreation(rival), FadeIn(lr), run_time=3)
        self.finish()

        self.narrate("6e.2")
        sf = txt("smooth forever?", 30, BLUE_C).move_to(uch.c2p(0.55, 5.5))
        self.play(FadeIn(sf))
        self.play(ShowCreation(Cross(sf, stroke_color=RED_C)))
        self.finish()
        self.clear_content()

        # 6f — every viscosity, and the montage
        sub = self.subtitle("Every viscosity at once")
        self.play(FadeIn(sub))
        self.narrate("6f.1")
        col = Ellipse(width=1.2, height=2.6).set_stroke(CORE, 3).set_fill(CORE, 0.3).move_to(3 * LEFT)
        rule = Tex(R"u_\nu(x,t) = \sqrt{\nu} \cdot u(x / \sqrt{\nu}, t)", font_size=48).move_to(2.2 * RIGHT)
        zl = txt("zoom space by the square root of the viscosity", 24, GREY_A).next_to(rule, DOWN, buff=0.4)
        self.play(FadeIn(col))
        self.cue("Zooming space")
        self.play(col.animate.scale(1.8), FadeIn(rule), FadeIn(zl), run_time=2)
        self.finish()
        self.play(FadeOut(VGroup(col, rule, zl, sub)))

        self.narrate("6f.2")
        steps = ["core", "annulus", "pulses", "corrections", "force", "uniqueness"]
        boxes = VGroup(*[card([s], width=1.9, size=24) for s in steps]).arrange(RIGHT, buff=0.35).move_to(0.3 * UP)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, fill_color=GREY_B, thickness=3)
                          for a, b in zip(boxes, boxes[1:])])
        for i, phrase in enumerate(["A collapsing", "An imbalance", "cancelled by amplified", "Infinitely many",
                                    "A force equal", "And a uniqueness"]):
            self.cue(phrase)
            anims = [FadeIn(boxes[i], shift=0.1 * RIGHT)]
            if i:
                anims.append(GrowArrow(arrows[i - 1]))
            self.play(*anims, run_time=0.6)
        self.finish(2.0)


# ---------------------------------------------------------------------------
# Chapter 7 — is it right?
# ---------------------------------------------------------------------------

class C7Check(Video):
    def construct(self):
        self.chapter(4, "7. Is it right?")
        self.narrate("7.1")
        c1 = card(["Lean 4", "about 429,000 lines", "no gaps · no extra axioms"], width=9, size=30).move_to(1.6 * UP)
        self.play(FadeIn(c1))
        self.finish()

        self.narrate("7.2")
        c2 = card(["checked against a statement of options C and D", "written by others (Formal Conjectures)"],
                  width=9, size=26).move_to(0.6 * DOWN)
        self.play(FadeIn(c2))
        self.cue("We have not re-run")
        note = txt("not re-run by us", 24, GREY_A).next_to(c2, DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.finish()
        self.play(FadeOut(VGroup(c1, c2, note)))

        self.narrate("7.3")
        c3 = card(["Bastounis, Circelli, Hansen · October 2026", "the Lean proof is not the paper"], width=9,
                  size=28).move_to(1.7 * UP)
        self.play(FadeIn(c3))
        self.finish()

        self.narrate("7.4")
        rows = VGroup()
        for paper, lean in [("Paper: four extra derivatives", "Lean: five extra derivatives"),
                            ("Paper: one argument for a pressure bound", "Lean: a different argument")]:
            a = card([paper], width=5.6, size=22)
            b = card([lean], width=5.6, size=22)
            rows.add(VGroup(a, b).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, buff=0.35).move_to(0.6 * DOWN)
        self.cue("a weaker bound")
        self.play(FadeIn(rows[0]))
        self.cue("a different argument")
        self.play(FadeIn(rows[1]))
        self.finish()

        self.narrate("7.5")
        c5 = txt("They do not say the paper is wrong.", 32, YELLOW).move_to(2.6 * DOWN)
        self.play(FadeOut(rows), FadeIn(c5.move_to(0.5 * DOWN)))
        self.finish()
        self.play(FadeOut(VGroup(c3, c5)))

        self.narrate("7.6")
        qa = [("Is the theorem true?", "the Lean check"), ("Is the paper's proof right?", "peer review"),
              ("Has the prize been won?", "the Clay Institute")]
        table = VGroup()
        for k, (q, a) in enumerate(qa):
            # questions right-aligned and answers left-aligned on one column, so the arrows line up
            y = (0.4 + 0.75 * (1 - k)) * UP
            qt = txt(q, 30).move_to(y, aligned_edge=RIGHT).shift(0.4 * LEFT)
            at = txt("→  " + a, 30, YELLOW).move_to(y, aligned_edge=LEFT).shift(0.4 * RIGHT)
            table.add(VGroup(qt, at))
        for row, phrase in zip(table, ["Is the theorem true", "Is the paper's proof", "And has the prize"]):
            self.cue(phrase)
            self.play(FadeIn(row, shift=0.1 * RIGHT))
        self.finish()

        self.recap("7.7", ["A computer-checked theorem;", "the written proof still needs review."])


# ---------------------------------------------------------------------------
# Chapter 8 — what it would mean
# ---------------------------------------------------------------------------

class C8Meaning(Video):
    def construct(self):
        self.chapter(4, "8. What it would mean")
        items = [("8.1", "✓", "Settles the prize problem as written (options C and D)", GREEN_C),
                 ("8.2", "✗", "Does not show that unforced flows blow up", RED_C),
                 ("8.3", "✗", "Not real water blowing up; no change to weather or engineering", RED_C)]
        rows = VGroup()
        for beat, mark, text, color in items:
            if mark == "✓":
                sym = VMobject().set_points_as_corners([[-0.22, 0.0, 0], [-0.06, -0.18, 0], [0.24, 0.22, 0]])
            else:
                sym = VGroup(Line([-0.18, -0.18, 0], [0.18, 0.18, 0]), Line([-0.18, 0.18, 0], [0.18, -0.18, 0]))
            sym.set_stroke(color, 6)
            row = VGroup(sym, txt(text, 32)).arrange(RIGHT, buff=0.4)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(0.4 * UP)
        for (beat, *_), row in zip(items, rows):
            self.narrate(beat)
            self.play(FadeIn(row, shift=0.1 * RIGHT))
            self.finish()
        self.recap("8.4", ["A breakdown, driven by a smooth push.", "The unforced question remains."])


# ---------------------------------------------------------------------------
# Chapter 9 — closing
# ---------------------------------------------------------------------------

class C9Close(Video):
    def construct(self):
        self.chapter_title = "9. Closing"
        self.narrate("9.1")
        big = self.roadmap(-1, big=True).move_to(2.6 * UP)
        self.play(FadeIn(big, lag_ratio=0.2))
        tight = ValueTracker(0.6)
        field = always_redraw(lambda: swirl_field(tight=tight.get_value()).scale(0.8).shift(0.25 * DOWN))
        self.play(FadeIn(field))
        self.cue("A spinning column")
        self.play(tight.animate.set_value(3.0), run_time=5)
        self.finish()

        self.narrate("9.2")
        self.remove(field)
        self.play(FadeOut(big))
        title = txt("Finite Time Blowup for Navier–Stokes", 48)
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
        title = txt("Finite Time Blowup for Navier–Stokes", 54).to_edge(UP, buff=0.6)
        sub = txt("explained for everyone", 30, GREY_A).next_to(title, DOWN, buff=0.25)
        field = swirl_field(tight=2.6).scale(0.75).shift(3.0 * LEFT + 1.1 * DOWN)
        reg = regions().scale(0.8).shift(3.6 * RIGHT + 1.0 * DOWN)
        rip = ripple_ring(radius=1.32, amp=0.05, freq=18, center=reg.core.get_center())
        self.add(title, sub, field, reg, rip)
