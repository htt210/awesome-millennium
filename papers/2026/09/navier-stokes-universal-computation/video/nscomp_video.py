"""Narrated explainer for "Universal Computation with Eventually Stationary
Navier–Stokes Forcing" (OpenAI, September 2026), written for 3b1b's manim
(manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("2.3") and
the words come from beat 2.3 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl nscomp_video.py C2Machines -w -l --config_file ../../../../../tools/video/custom_config.yml

Computed, with the same code as the explainer's figures (../code/make_figures.py):
the busy-beaver run, its encoded points (checked step by step against the affine
rectangle maps), and the area of a rule's rectangle before and after. The fluid
box, the swirls, the drop's path and the clock are schematics.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "video"))
sys.path.insert(0, str(HERE.parent / "code"))
from narrated import *  # noqa: E402,F403
import make_figures as mf  # noqa: E402

CONFS, PTS, CONFS2, PTS2 = mf.check()      # busy beaver (halts at step 6) and a machine that never halts


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["Fluids", "Machines", "The claim", "How it works", "Is it right?"]
    PRONOUNCE = [(r"\b1936\b", "nineteen thirty-six"), (r"\b2016\b", "twenty sixteen"),
                 (r"\b2026\b", "twenty twenty-six")]
    BUILD = HERE / "build"


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def fluid_box(size=4.6, center=ORIGIN, strip=True):
    box = Square(side_length=size).set_stroke(BLUE_B, 3).set_fill(BLUE_E, 0.25).move_to(center)
    grp = VGroup(box)
    if strip:
        band = Rectangle(width=size, height=size * (1 / 8 - 1 / 32)).set_stroke(width=0).set_fill(RED_C, 0.35)
        band.move_to(box.get_bottom() + size * (1 / 32 + (1 / 8 - 1 / 32) / 2) * UP)
        grp.add(band)
    return grp


def swirls(box, n=5, seed=2):
    rng = np.random.default_rng(seed)
    out = VGroup()
    s = box.get_width()
    for _ in range(n):
        c = box.get_center() + np.array([rng.uniform(-0.3, 0.3) * s, rng.uniform(-0.15, 0.35) * s, 0])
        r = rng.uniform(0.08, 0.16) * s
        arc = Arc(radius=r, start_angle=rng.uniform(0, TAU), angle=1.6 * PI).move_arc_center_to(c)
        out.add(arc.set_stroke(BLUE_A, 2.5).add_tip(length=0.15, width=0.15, fill_color=BLUE_A))
    return out


def drop_path(box, halts=True, seed=4, n=14):
    rng = np.random.default_rng(seed)
    s = box.get_width()
    c = box.get_center()
    pts = [c + np.array([-0.25 * s, -0.25 * s + 0.5 * s * 0.5, 0])]
    for k in range(n):
        y = rng.uniform(0.25, 0.85) if (k < n - 1 or not halts) else 0.08
        pts.append(c + np.array([rng.uniform(-0.4, 0.4) * s, (y - 0.5) * s, 0]))
    return VMobject().set_points_smoothly(pts).set_stroke(YELLOW, 3)


def tape_row(conf, lo=-3, hi=3, cell=0.62, center=ORIGIN):
    state, tape, head = conf
    cells = VGroup()
    for i in range(lo, hi + 1):
        v = tape.get(i, 0)
        sq = Square(side_length=cell * 0.92).set_stroke(GREY_B, 1.5).set_fill(BLUE_D if v else BLACK, 1)
        cells.add(VGroup(sq, txt(str(v), 24, WHITE).move_to(sq)))
    cells.arrange(RIGHT, buff=cell * 0.08).move_to(center)
    hbox = SurroundingRectangle(cells[head - lo], buff=0.05).set_stroke(RED_C if state == "H" else ORANGE, 4)
    lab = txt("HALT" if state == "H" else f"state {state}", 24, RED_C if state == "H" else ORANGE)
    lab.next_to(cells, RIGHT, buff=0.35)
    return VGroup(cells, hbox, lab)


def square_map(size=4.4, center=ORIGIN):
    """The encoding square [1/4, 1] x [1/4, 3/4] with the rule rectangles; returns (group, to_point)."""
    w, h = size, size * (0.5 / 0.75)
    frame = Rectangle(width=w, height=h).set_stroke(GREY_B, 2).move_to(center)
    dl = frame.get_corner(DL)

    def to_point(x, y):
        return dl + np.array([(float(x) - 0.25) / 0.75 * w, (float(y) - 0.25) / 0.5 * h, 0])
    rects = VGroup()
    for q, lab in [(1, "A"), (2, "B"), (3, "H")]:
        for a, sl in [(1, "0"), (2, "1")]:
            p0, p1 = to_point(q / 4, a / 4), to_point((q + 1) / 4, (a + 1) / 4)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1]).move_to((p0 + p1) / 2)
            r.set_stroke(GREY_C, 1.5).set_fill(RED_E if q == 3 else GREY_E, 0.6 if q == 3 else 0.5)
            t = txt(f"{lab}, reads {sl}", 16, GREY_A).next_to(r.get_corner(DL), UR, buff=0.06)
            rects.add(VGroup(r, t))
    xl = txt("X: state, then tape to the left", 20, GREY_A).next_to(frame, DOWN, buff=0.15)
    yl = txt("Y: tape from the head on", 20, GREY_A).rotate(PI / 2).next_to(frame, LEFT, buff=0.15)
    return VGroup(rects, frame, xl, yl), to_point


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        box = fluid_box(center=0.4 * UP)
        drop = Dot(box[0].get_center() + np.array([-0.25, 0.0, 0]) * box[0].get_width(), radius=0.12,
                   fill_color=YELLOW)
        self.narrate("0.1")
        self.play(FadeIn(box[0]), FadeIn(drop))
        sw = swirls(box[0])
        self.cue("push it")
        self.play(LaggedStart(*[ShowCreation(s) for s in sw], lag_ratio=0.2), run_time=1.5)
        self.finish()

        self.narrate("0.2")
        path = drop_path(box[0], halts=True)
        path.shift(drop.get_center() - path.get_start())
        self.play(FadeIn(box[1]))
        self.play(ShowCreation(path), MoveAlongPath(drop, path), run_time=3)
        self.cue("exactly when")
        rule = txt("enters the red strip  ⇔  the program halts", 30, YELLOW).next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(rule))
        self.finish()

        self.narrate("0.3")
        title = txt("Fluids That Compute", 58)
        sub = txt("OpenAI preprint, September 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(VGroup(box, drop, sw, path, rule)), Write(title, run_time=2))
        self.play(FadeIn(sub))
        self.finish()
        self.clear_caption()

        self.narrate("0.4")
        big = self.roadmap(None, big=True).move_to(1.6 * DOWN)
        self.play(VGroup(title, sub).animate.shift(UP), FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — fluids
# ---------------------------------------------------------------------------

class C1Fluids(Video):
    def construct(self):
        self.chapter(0, "1. Fluids")
        self.narrate("1.1")
        eq = Tex(R"\partial_t u + (u\cdot\nabla)u", "=", R"-\nabla p", "+", R"\nu\Delta u", "+", "f",
                 font_size=64).move_to(0.9 * UP)
        labs = [("momentum", 0, BLUE_C), ("pressure", 2, TEAL_C), ("friction", 4, PURPLE_B), ("force", 6, ORANGE)]
        tags = VGroup()
        for name, i, col in labs:
            eq[i].set_color(col)
            tags.add(txt(name, 24, col).next_to(eq[i], DOWN, buff=0.35))
        self.play(Write(eq), run_time=2)
        self.cue("its momentum")
        self.play(LaggedStart(*[FadeIn(t, shift=0.1 * UP) for t in tags], lag_ratio=0.5), run_time=3)
        self.finish()
        self.clear_content()

        self.narrate("1.2")
        ax = Chart((-3, 3), (0, 4), 7.0, 3.2, grid=False)
        ax.shift(0.45 * UP - ax.box.get_center())
        tr = ValueTracker(1.0)
        graph = always_redraw(lambda: curve(ax, lambda x: min(3.9, 1.0 / (tr.get_value() + 0.6 * x * x)) *
                                            tr.get_value() ** 0.5 * 1.2, -3, 3, n=300, color=BLUE_C, width=4))
        q = txt("?", 80, YELLOW).move_to(ax.c2p(2.2, 3.0))
        self.add(ax, graph)
        self.play(tr.animate.set_value(0.3), run_time=2.5)
        self.play(FadeIn(q, scale=1.3))
        self.finish()
        graph.clear_updaters()
        self.clear_content()

        self.narrate("1.3")
        c = card(["Tao, 2016: a fluid computer", "that builds a smaller, faster copy of itself"], width=9.5, size=30)
        c.move_to(1.0 * UP)
        boxes = VGroup(*[Square(side_length=1.6 * 0.55 ** k).set_stroke(BLUE_B, 3) for k in range(5)])
        boxes.arrange(RIGHT, buff=0.4, aligned_edge=DOWN).next_to(c, DOWN, buff=0.5)
        self.play(FadeIn(c))
        self.cue("programmed to copy")
        self.play(LaggedStart(*[FadeIn(b, scale=0.7) for b in boxes], lag_ratio=0.3), run_time=2)
        self.finish()

        self.recap("1.4", ["Navier–Stokes: does smoothness last?", "One idea: fluids that compute."])


# ---------------------------------------------------------------------------
# Chapter 2 — machines
# ---------------------------------------------------------------------------

class C2Machines(Video):
    def construct(self):
        self.chapter(1, "2. Machines")
        self.narrate("2.1")
        row = tape_row(CONFS[0], center=0.8 * UP)
        rules = VGroup(*[txt(f"{s}, reads {a}  →  write {w}, move {'right' if m > 0 else 'left'}, "
                             f"{'HALT' if n == 'H' else 'go to ' + n}", 22, GREY_A)
                         for (s, a), (n, w, m) in mf.BUSY_BEAVER.items()]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        rules.next_to(row, DOWN, buff=0.6)
        self.play(FadeIn(row))
        self.cue("following a short")
        self.play(FadeIn(rules, lag_ratio=0.2))
        self.finish()
        self.clear_content()

        self.narrate("2.2")
        rows = VGroup(*[tape_row(c, cell=0.5) for c in CONFS]).arrange(DOWN, buff=0.12).move_to(0.35 * UP)
        rows.set_height(5.0).move_to(0.35 * UP)
        self.play(FadeIn(rows[0]))
        for r in rows[1:]:
            self.play(FadeIn(r, shift=0.15 * DOWN), run_time=0.55)
        self.cue("We say it halts")
        self.play(Indicate(rows[-1][2], color=RED_C))
        self.finish()
        self.clear_content()

        self.narrate("2.3")
        t = card(["Turing, 1936:", "no algorithm decides halting for every machine"], width=9.5, size=30).move_to(0.6 * UP)
        self.play(FadeIn(t))
        self.finish()
        self.play(FadeOut(t))

        self.narrate("2.4")
        a = txt("a system that imitates every machine", 32).move_to(1.2 * UP)
        b = txt("⇒  undecidable questions about its future", 32, YELLOW).next_to(a, DOWN, buff=0.45)
        self.play(FadeIn(a))
        self.play(FadeIn(b))
        self.finish()

        self.recap("2.5", ["Machines can't always be predicted.", "Can fluids imitate them?"])


# ---------------------------------------------------------------------------
# Chapter 3 — the claim
# ---------------------------------------------------------------------------

class C3Claim(Video):
    def construct(self):
        self.chapter(2, "3. The claim")
        self.narrate("3.1")
        box = fluid_box(size=3.8, center=3.4 * LEFT + 0.3 * UP)
        glue = VGroup(*[Arrow(box[0].get_left() + 0.3 * LEFT + y * UP, box[0].get_left() + 0.05 * LEFT + y * UP,
                              buff=0).set_stroke(GREY_B, 2) for y in (-1, 0, 1)])
        glue2 = glue.copy().rotate(PI, about_point=box[0].get_center())
        facts = VGroup(txt("opposite faces glued", 26), txt("fixed viscosity", 26), txt("starts at rest", 26))
        facts.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(2.6 * RIGHT + 0.3 * UP)
        self.play(FadeIn(box[0]), FadeIn(glue), FadeIn(glue2))
        self.play(FadeIn(facts, lag_ratio=0.3))
        self.finish()
        self.clear_content()

        self.narrate("3.2")
        m = card(["machine + input"], width=3.4, size=28).move_to(4.4 * LEFT + 0.6 * UP)
        comp = card(["compiler"], width=2.6, size=28, color=YELLOW).move_to(0.6 * UP)
        f = card(["formula for a force f"], width=3.8, size=28).move_to(4.3 * RIGHT + 0.6 * UP)
        a1 = Arrow(m.get_right(), comp.get_left(), buff=0.1).set_stroke(GREY_B, 3)
        a2 = Arrow(comp.get_right(), f.get_left(), buff=0.1).set_stroke(GREY_B, 3)
        clock = txt("smooth · constant after time 1 · never runs the machine", 24, GREY_A).next_to(comp, DOWN, buff=0.8)
        self.play(FadeIn(m))
        self.play(GrowArrow(a1), FadeIn(comp), GrowArrow(a2), FadeIn(f))
        self.cue("It never runs")
        self.play(FadeIn(clock))
        self.finish()
        self.clear_content()

        self.narrate("3.3")
        box = fluid_box(size=4.0, center=0.3 * UP, strip=False)
        sw = swirls(box[0], n=6, seed=7)
        sm = txt("a smooth solution for all time", 28, BLUE_B).next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(box))
        self.play(LaggedStart(*[ShowCreation(s) for s in sw], lag_ratio=0.15), FadeIn(sm))
        self.finish()
        self.clear_content()

        self.narrate("3.4")
        box = fluid_box(size=4.0, center=0.3 * UP)
        drop = Dot(box[0].get_center() + np.array([-1.0, 0.0, 0]), radius=0.12, fill_color=YELLOW)
        path = drop_path(box[0], halts=True, seed=9)
        path.shift(drop.get_center() - path.get_start())
        rule = txt("enters the strip  ⇔  the machine halts", 30, YELLOW).next_to(box, DOWN, buff=0.3)
        self.play(FadeIn(box), FadeIn(drop))
        self.play(ShowCreation(path), MoveAlongPath(drop, path), run_time=2.5)
        self.play(FadeIn(rule))
        self.finish()

        self.recap("3.5", ["Claimed: a force that turns a fluid at rest", "into any computer."])


# ---------------------------------------------------------------------------
# Chapter 4 — how it works
# ---------------------------------------------------------------------------

class C4How(Video):
    def construct(self):
        self.chapter(3, "4. How it works")
        self.narrate("4.1")
        row = tape_row(CONFS[3], center=1.7 * UP)
        left = SurroundingRectangle(row[0][:3], buff=0.06).set_stroke(TEAL_C, 3)
        right = SurroundingRectangle(row[0][3:], buff=0.06).set_stroke(PURPLE_B, 3)
        xl = txt("X = 0.(state)(cells to the left)…", 24, TEAL_C).next_to(row, DOWN, buff=0.35).shift(2.4 * LEFT)
        yl = txt("Y = 0.(cell under head)(cells to the right)…", 24, PURPLE_B).next_to(xl, RIGHT, buff=0.6)
        sq, to_point = square_map(size=3.6, center=1.25 * DOWN)
        dot = Dot(to_point(*PTS[3]), radius=0.1, fill_color=YELLOW)
        self.play(FadeIn(row))
        self.cue("Write the tape")
        self.play(ShowCreation(left), FadeIn(xl))
        self.cue("and the rest")
        self.play(ShowCreation(right), FadeIn(yl))
        self.cue("The whole tape")
        self.play(FadeIn(sq), FadeIn(dot, scale=2))
        self.finish()
        self.clear_content()

        self.narrate("4.2")
        sq, to_point = square_map(size=6.0, center=0.4 * UP)
        dots = VGroup(*[Dot(to_point(*p), radius=0.09, fill_color=ORANGE) for p in PTS])
        nums = VGroup(*[txt(str(k), 20, WHITE).next_to(d, UR, buff=0.04) for k, d in enumerate(dots)])
        self.play(FadeIn(sq))
        self.play(FadeIn(dots[0]), FadeIn(nums[0]))
        for k in range(1, len(dots)):
            seg = Line(dots[k - 1].get_center(), dots[k].get_center()).set_stroke(ORANGE, 2, opacity=0.6)
            self.play(ShowCreation(seg), FadeIn(dots[k], scale=1.5), FadeIn(nums[k]), run_time=0.6)
        self.cue("it lands")
        self.play(Indicate(dots[-1], color=RED_C, scale_factor=2))
        self.finish()
        self.clear_content()

        self.narrate("4.3")
        sq = Square(side_length=1.6).set_stroke(BLUE_C, 3).set_fill(BLUE_C, 0.6).move_to(3.0 * LEFT + 0.4 * UP)
        tall = Rectangle(width=0.4, height=6.4 * 0.62).set_stroke(ORANGE, 3).set_fill(ORANGE, 0.6)
        tall.move_to(2.4 * RIGHT + 0.4 * UP)
        a = txt("area 1/16", 26, BLUE_C).next_to(sq, DOWN, buff=0.3)
        b = txt("area 1/16", 26, ORANGE).next_to(tall, RIGHT, buff=0.3)
        arr = Arrow(sq.get_right(), tall.get_left(), buff=0.3).set_stroke(GREY_B, 3)
        self.play(FadeIn(sq), FadeIn(a))
        self.play(GrowArrow(arr), TransformFromCopy(sq, tall), run_time=1.5)
        self.play(FadeIn(b))
        self.cue("Area is kept")
        inc = txt("incompressible fluids keep area", 28, YELLOW).move_to(2.3 * DOWN)
        self.play(FadeIn(inc))
        self.finish()
        self.clear_content()

        self.narrate("4.4")
        mach = card(["machine step"], width=3.0, size=26).move_to(3.8 * LEFT + 1.0 * UP)
        er = txt("erases the old symbol", 24, RED_C).next_to(mach, DOWN, buff=0.3)
        rec = card(["record of what was erased"], width=4.6, size=26, color=YELLOW).move_to(3.0 * RIGHT + 1.0 * UP)
        hist = VGroup(*[Square(side_length=0.42).set_stroke(YELLOW, 2) for _ in range(7)]).arrange(RIGHT, buff=0.06)
        hist.next_to(rec, DOWN, buff=0.4)
        bn = txt("Bennett, 1973: keep a history, and every step can be undone", 24, GREY_A).move_to(1.8 * DOWN)
        self.play(FadeIn(mach), FadeIn(er))
        self.cue("So the machine first")
        self.play(FadeIn(rec), LaggedStart(*[FadeIn(h) for h in hist], lag_ratio=0.15), FadeIn(bn))
        self.finish()
        self.clear_content()

        self.narrate("4.5")
        rng = np.random.default_rng(3)
        srcs = VGroup(*[Rectangle(width=0.7, height=0.5).set_stroke(BLUE_C, 2).set_fill(BLUE_C, 0.5)
                        .move_to([-5 + 0.9 * k, 1.6 - 0.6 * (k % 3), 0]) for k in range(5)])
        park = Rectangle(width=2.6, height=1.0).set_stroke(GREY_B, 2).move_to(0.6 * DOWN)
        pl = txt("parking area", 20, GREY_A).next_to(park, DOWN, buff=0.1)
        tgts = VGroup(*[Rectangle(width=0.35, height=1.0).set_stroke(ORANGE, 2).set_fill(ORANGE, 0.5)
                        .move_to([2.6 + 0.6 * k, 1.4 - 0.4 * (k % 2), 0]) for k in range(5)])
        self.play(FadeIn(srcs), ShowCreation(park), FadeIn(pl))
        self.play(*[s.animate.move_to(park.get_center() + (k - 2) * 0.45 * RIGHT).scale(0.6)
                    for k, s in enumerate(srcs)], run_time=1.4)
        self.play(*[Transform(s, t) for s, t in zip(srcs, tgts)], run_time=1.6)
        self.finish()
        self.clear_content()

        self.narrate("4.6")
        axis = Arrow(2.2 * DOWN, 2.4 * UP, buff=0).set_stroke(GREY_B, 3).set_fill(GREY_B).shift(3.5 * LEFT)
        al = txt("clock: the third direction", 24, GREY_A).next_to(axis, RIGHT, buff=0.2).shift(1.8 * UP)
        ticks = VGroup(*[VGroup(Line(0.15 * LEFT, 0.15 * RIGHT).set_stroke(GREY_B, 2),
                                txt(f"step {k}", 20, GREY_A)).arrange(RIGHT, buff=0.15)
                         .move_to(axis.get_start() + (0.6 + 1.2 * k) * UP + 0.45 * RIGHT) for k in range(4)])
        d = Dot(axis.get_start() + 0.6 * UP, radius=0.12, fill_color=YELLOW)
        steady = txt("after a gentle start, the flow stops changing", 26, YELLOW).move_to(2.0 * RIGHT + 0.3 * UP)
        self.play(GrowArrow(axis), FadeIn(al), FadeIn(ticks))
        self.play(FadeIn(d))
        self.play(d.animate.shift(3.6 * UP), run_time=2.5, rate_func=linear)
        self.cue("After a gentle")
        self.play(FadeIn(steady))
        self.finish()
        self.clear_content()

        self.narrate("4.7")
        eq = Tex(R"f", "=", R"\partial_t u + (u\cdot\nabla)u + \nabla p - \nu\Delta u", font_size=60).move_to(0.9 * UP)
        eq[0].set_color(ORANGE)
        note = txt("choose the flow u first; the force is whatever the equation needs", 26, GREY_A)
        note.next_to(eq, DOWN, buff=0.5)
        self.play(Write(eq), run_time=2)
        self.play(FadeIn(note))
        self.finish()

        self.recap("4.8", ["Tape → point; rules → area-keeping maps;", "swirls + clock → force."])


# ---------------------------------------------------------------------------
# Chapter 5 — is it right?
# ---------------------------------------------------------------------------

class C5Close(Video):
    def construct(self):
        self.chapter(4, "5. Is it right?")
        self.narrate("5.1")
        lean = card(["Lean 4: companion constructions,", "including a halting drop in all of space"], width=9.5, size=28)
        lean.move_to(1.2 * UP)
        out = txt("this theorem: outside that scope", 26, ORANGE).next_to(lean, DOWN, buff=0.4)
        ne = txt("no expert assessment found yet", 26, ORANGE).next_to(out, DOWN, buff=0.25)
        self.play(FadeIn(lean))
        self.cue("This exact theorem")
        self.play(FadeIn(out))
        self.cue("and we found")
        self.play(FadeIn(ne))
        self.finish()
        self.clear_content()

        self.narrate("5.2")
        q = txt("Navier–Stokes blowup ?", 56, YELLOW).move_to(1.0 * UP)
        sm = txt("these flows stay smooth forever", 28, GREY_A).next_to(q, DOWN, buff=0.4)
        self.play(FadeIn(q, scale=1.2))
        self.play(FadeIn(sm))
        self.finish()
        self.clear_content()

        self.narrate("5.3")
        a = txt("✓  make a fluid compute", 34, GREEN_C).move_to(1.2 * UP + 1.0 * LEFT)
        b = txt("?  make it compute its own blowup", 34, ORANGE).next_to(a, DOWN, buff=0.5, aligned_edge=LEFT)
        tl = txt("Tao's program", 26, GREY_A).next_to(a, UP, buff=0.5, aligned_edge=LEFT)
        self.play(FadeIn(tl), FadeIn(a))
        self.cue("Making a fluid")
        self.play(FadeIn(b))
        self.finish()
        self.clear_content()

        self.narrate("5.4")
        self.play(FadeOut(self.roadmap_mob))
        title = txt("Fluids That Compute", 52)
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
        title = txt("Fluids That Compute", 60).to_edge(UP, buff=0.6)
        sub = txt("a Navier–Stokes flow that runs any program, explained for everyone", 28, GREY_A)
        sub.next_to(title, DOWN, buff=0.25)
        box = fluid_box(size=4.2, center=3.3 * LEFT + 1.1 * DOWN)
        sq, to_point = square_map(size=4.4, center=3.0 * RIGHT + 1.0 * DOWN)
        dots = VGroup(*[Dot(to_point(*p), radius=0.08, fill_color=ORANGE) for p in PTS])
        self.add(title, sub, box, swirls(box[0]), sq, dots)
