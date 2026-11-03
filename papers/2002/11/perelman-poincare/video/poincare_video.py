"""Narrated explainer for Perelman's proof of the Poincaré conjecture (2002-2003),
written for 3b1b's manim (manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("3.4") and
the words come from beat 3.4 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl poincare_video.py C3Flow -w -l --config_file ../../../../../tools/video/custom_config.yml

Three-dimensional shapes are drawn as their two-dimensional cousins: a ball's
surface, a doughnut, the outline of a dumbbell.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "video"))
from narrated import *  # noqa: E402,F403

BALL = BLUE_C
TORUS = TEAL_C
LOOP = YELLOW
SHAPE = BLUE_B
CUT = RED_C


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["Shapes", "The question", "Ricci flow", "Perelman", "Checked"]
    PRONOUNCE = [(r"\bRicci\b", "Reechee"), (r"\bCao\b", "Tsao"), (r"\bZhu\b", "Joo"),
                 (r"\bHuai-Dong\b", "Why-Dong"), (r"\bXi-Ping\b", "Shee-Ping"),
                 (r"\b1904\b", "nineteen oh four"), (r"\b1961\b", "nineteen sixty-one"),
                 (r"\b1982\b", "nineteen eighty-two"), (r"\b2010\b", "twenty ten")]
    BUILD = HERE / "build"


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def ball(r=1.3, center=ORIGIN, color=BALL):
    """A ball's surface: a shaded disc with a front (solid) and back (dashed) equator."""
    disc = Circle(radius=r).set_fill(color, 0.22).set_stroke(color, 3)
    front = Arc(start_angle=PI, angle=PI, radius=r).stretch(0.28, 1, about_point=ORIGIN)
    back = DashedVMobject(Arc(start_angle=0, angle=PI, radius=r).stretch(0.28, 1, about_point=ORIGIN),
                          num_dashes=18)
    front.set_stroke(color, 1.5, opacity=0.7)
    back.set_stroke(color, 1.5, opacity=0.4)
    g = VGroup(disc, back, front).move_to(center)
    g.r, g.c = r, np.array(center, dtype=float)
    return g


def lat_loop(b, phi):
    """The loop at latitude phi on ball b (phi = pi/2 is the top pole)."""
    w = b.r * math.cos(phi)
    c = b.c + np.array([0, b.r * math.sin(phi), 0])
    if w < 0.03:
        return Dot(c, radius=0.07, fill_color=LOOP)
    return Ellipse(width=2 * w, height=0.56 * w).set_stroke(LOOP, 5).move_to(c)


def doughnut(w=4.0, h=2.2, center=ORIGIN, holes=(0.0,), color=TORUS):
    """A doughnut seen from slightly above: an outline and a hole drawn as a smile and a frown."""
    body = Ellipse(width=w, height=h).set_fill(color, 0.22).set_stroke(color, 3)
    marks = VGroup()
    hw = 0.36 * w / len(holes)
    for x in holes:
        smile = ArcBetweenPoints(np.array([x - hw, 0.08, 0]), np.array([x + hw, 0.08, 0]), angle=1.3)
        frown = ArcBetweenPoints(np.array([x - 0.72 * hw, -0.02, 0]), np.array([x + 0.72 * hw, -0.02, 0]),
                                 angle=-1.1)
        marks.add(smile.set_stroke(color, 3), frown.set_stroke(color, 3))
    g = VGroup(body, marks).move_to(center)
    g.w, g.h, g.c = w, h, np.array(center, dtype=float)
    return g


def ring_loop(d, t):
    """A loop around the doughnut's hole; t = 0 near the outer edge, t = 1 tight around the hole."""
    w = interpolate(0.86 * d.w, 0.42 * d.w, t)
    h = interpolate(0.78 * d.h, 0.34 * d.h, t)
    return Ellipse(width=w, height=h).set_stroke(LOOP, 5).move_to(d.c + 0.02 * UP)


def mug(center=ORIGIN, color=TORUS):
    body = RoundedRectangle(width=1.6, height=1.9, corner_radius=0.25).set_fill(color, 0.22).set_stroke(color, 3)
    handle = Arc(start_angle=-PI / 2, angle=PI, radius=0.5).set_stroke(color, 14)
    handle.next_to(body, RIGHT, buff=-0.05)
    return VGroup(handle, body).move_to(center)


def tick(color=GREEN_C, s=1.0):
    return VMobject().set_points_as_corners([[-0.22 * s, 0, 0], [-0.06 * s, -0.18 * s, 0], [0.24 * s, 0.22 * s, 0]]
                                            ).set_stroke(color, 6)


def cross(color=RED_C, s=1.0):
    a = 0.18 * s
    return VGroup(Line([-a, -a, 0], [a, a, 0]), Line([-a, a, 0], [a, -a, 0])).set_stroke(color, 6)


def profile_shape(rfun, x0, x1, scale=1.0, center=ORIGIN, color=SHAPE, n=240):
    """The outline of a surface of revolution with radius profile rfun(x), x in [x0, x1]."""
    xs = np.linspace(x0, x1, n)
    rs = np.array([max(rfun(x), 0.0) for x in xs])
    top = [np.array([x * scale, r * scale, 0]) for x, r in zip(xs, rs)]
    bot = [np.array([x * scale, -r * scale, 0]) for x, r in zip(xs[::-1], rs[::-1])]
    m = VMobject().set_points_as_corners(top + bot + [top[0]])
    return m.set_fill(color, 0.22).set_stroke(color, 3).shift(center)


def dumbbell(x, neck, c=1.5, R=0.95):
    """Radius profile of a smooth dumbbell: a bridge from `neck` at the middle to R at |x| = c, then bulbs."""
    a = abs(x)
    if a >= c:
        return math.sqrt(max(R * R - (a - c) ** 2, 0.0))
    return neck + (R - neck) * math.sin(math.pi * a / (2 * c)) ** 2


def capped_piece(side, neck, cut=0.45, c=1.5, R=0.95, scale=1.6, color=SHAPE):
    """One half of the dumbbell after surgery: cut at |x| = cut, closed with a round cap."""
    xs = np.linspace(cut, c + R, 160)
    rs = [dumbbell(x, neck, c, R) for x in xs]
    rr = dumbbell(cut, neck, c, R)
    th = np.linspace(PI / 2, -PI / 2, 40)
    cap = [np.array([side * (cut - 0.9 * rr * math.cos(t)), rr * math.sin(t), 0]) for t in th]
    # cap from top to bottom, then along the bottom outward, then back along the top
    pts = cap + [np.array([side * x, -r, 0]) for x, r in zip(xs, rs)] + \
        [np.array([side * x, r, 0]) for x, r in zip(xs[::-1], rs[::-1])] + [cap[0]]
    m = VMobject().set_points_as_corners([p * scale for p in pts])
    return m.set_fill(color, 0.22).set_stroke(color, 3)


def cigar(length=5.0, r=0.42, center=ORIGIN, color=SHAPE):
    """A long thin tube with a rounded tip on the left, open (dashed) on the right."""
    xs = np.linspace(0, length, 200)
    rs = r * np.sqrt(1 - np.exp(-2.2 * xs / r))
    top = VMobject().set_points_as_corners([np.array([x, y, 0]) for x, y in zip(xs, rs)])
    bot = VMobject().set_points_as_corners([np.array([x, -y, 0]) for x, y in zip(xs, rs)])
    tail = VGroup(DashedLine([length, r, 0], [length + 0.9, r, 0]), DashedLine([length, -r, 0], [length + 0.9, -r, 0]))
    g = VGroup(top, bot, tail).set_stroke(color, 3)
    tail.set_stroke(color, 2, opacity=0.6)
    return g.move_to(center)


def neck_model(capped=False, color=SHAPE):
    a, b, r = -0.9, 0.9, 0.35
    g = VGroup(Line([a, r, 0], [b, r, 0]), Line([a, -r, 0], [b, -r, 0]),
               Ellipse(width=0.25, height=2 * r).move_to([b, 0, 0]))
    if capped:
        g.add(Arc(start_angle=PI / 2, angle=PI, radius=r).stretch(1.4, 0).move_to([a - 0.24, 0, 0]))
    else:
        g.add(DashedVMobject(Ellipse(width=0.25, height=2 * r).move_to([a, 0, 0]), num_dashes=10))
    return g.set_stroke(color, 3)


def curve_shortening(n=300, frames=90):
    """Discrete curve-shortening flow of the explainer's wiggly curve, sampled at
    evenly spaced areas (area falls at a constant rate, so evenly in time)."""
    cache = HERE / "build" / "curve_flow.npy"
    if cache.exists():
        return list(np.load(cache))
    s = np.linspace(0, 2 * math.pi, n, endpoint=False)
    r = 1.0 + 0.32 * np.sin(5 * s) + 0.12 * np.cos(9 * s + 0.6)
    x = np.stack([r * np.cos(s), r * np.sin(s)], axis=1)

    def area(y):
        return 0.5 * abs(np.sum(y[:, 0] * np.roll(y[:, 1], -1) - np.roll(y[:, 0], -1) * y[:, 1]))

    a0 = area(x)
    targets = list(np.linspace(1.0, 0.02, frames) * a0)
    snaps = [x.copy()]
    targets.pop(0)
    k = 0
    while targets:
        e = np.roll(x, -1, axis=0) - x
        h = np.linalg.norm(e, axis=1).mean()
        dt = 0.2 * h * h
        x = x + dt * (np.roll(x, -1, axis=0) - 2 * x + np.roll(x, 1, axis=0)) / (h * h)
        k += 1
        if k % 40 == 0:
            seg = np.linalg.norm(np.roll(x, -1, axis=0) - x, axis=1)
            cum = np.concatenate([[0], np.cumsum(seg)])
            tgt = np.linspace(0, cum[-1], n, endpoint=False)
            xx = np.concatenate([x, x[:1]])
            x = np.stack([np.interp(tgt, cum, xx[:, 0]), np.interp(tgt, cum, xx[:, 1])], axis=1)
        if area(x) <= targets[0]:
            snaps.append(x.copy())
            targets.pop(0)
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.save(cache, np.array(snaps))
    return snaps


def snap_curve(snaps, k, center, scale=1.4, rescale=False, color=SHAPE):
    i = min(int(k), len(snaps) - 2)
    f = k - i
    y = (1 - f) * snaps[i] + f * snaps[i + 1]
    if rescale:
        a0 = _area(snaps[0])
        y = (y - y.mean(axis=0)) * math.sqrt(a0 / _area(y))
    pts = [np.array([p[0] * scale, p[1] * scale, 0]) + center for p in y]
    return VMobject().set_points_as_corners(pts + [pts[0]]).set_stroke(color, 4)


def _area(y):
    return 0.5 * abs(np.sum(y[:, 0] * np.roll(y[:, 1], -1) - np.roll(y[:, 0], -1) * y[:, 1]))


def blob(t, center=ORIGIN, color=SHAPE):
    """A gently lumpy, positively curved blob that rounds out and shrinks as t goes 0 -> 1."""
    k = math.sqrt(max(1 - t, 0.0))
    return ParametricCurve(lambda s: center + k * (1.5 + 0.18 * (1 - t) * math.cos(2 * s) +
                                                    0.08 * (1 - t) * math.sin(3 * s)) *
                           np.array([math.cos(s), math.sin(s), 0]),
                           t_range=(0, TAU, TAU / 200)).set_stroke(color, 4).set_fill(color, 0.2)


def wiggly(scale=1.4, center=ORIGIN, color=SHAPE):
    return ParametricCurve(lambda s: center + scale * (1 + 0.32 * math.sin(5 * s) + 0.12 * math.cos(9 * s + 0.6)) *
                           np.array([math.cos(s), math.sin(s), 0]),
                           t_range=(0, TAU, TAU / 300)).set_stroke(color, 4)


def paper_cards(size=24):
    papers = [("1. The entropy formula", "November 2002"), ("2. Ricci flow with surgery", "March 2003"),
              ("3. Finite extinction time", "July 2003")]
    return VGroup(*[card([f"{a}  ·  {b}"], width=8.0, size=size) for a, b in papers]).arrange(DOWN, buff=0.25)


def mark_rows(items, size=32):
    rows = VGroup()
    for good, text in items:
        sym = tick() if good else cross()
        rows.add(VGroup(sym, txt(text, size)).arrange(RIGHT, buff=0.4))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5)


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        b = ball(1.6, 3.2 * LEFT + 0.3 * UP)
        phi = ValueTracker(-0.25)
        loop = always_redraw(lambda: lat_loop(b, phi.get_value()))
        self.narrate("0.1")
        self.play(FadeIn(b), ShowCreation(loop))
        self.cue("pull it tight")
        self.play(phi.animate.set_value(PI / 2), run_time=3)
        self.finish()

        self.narrate("0.2")
        d = doughnut(4.2, 2.3, 3.0 * RIGHT + 0.3 * UP)
        t = ValueTracker(0.0)
        dl = always_redraw(lambda: ring_loop(d, t.get_value()))
        self.play(FadeIn(d), ShowCreation(dl))
        self.play(t.animate.set_value(1.0), run_time=2.5)
        stuck = txt("stuck", 30, RED_C).next_to(d, DOWN, buff=0.3)
        self.play(FadeIn(stuck), t.animate.set_value(0.92), rate_func=there_and_back, run_time=1)
        self.finish()

        self.narrate("0.3")
        title = txt("Perelman's proof of the Poincaré conjecture", 50)
        sub = txt("Ricci flow, 2002–2003", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.remove(loop, dl)
        self.play(FadeOut(VGroup(b, d, stuck, lat_loop(b, PI / 2), ring_loop(d, 1.0))), Write(title, run_time=2))
        self.play(FadeIn(sub))
        self.finish()
        self.clear_caption()

        self.narrate("0.4")
        big = self.roadmap(None, big=True).move_to(1.5 * DOWN)
        self.play(title.animate.shift(UP), sub.animate.shift(UP), FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — shapes
# ---------------------------------------------------------------------------

class C1Shapes(Video):
    def construct(self):
        self.chapter(0, "1. Shapes")
        self.narrate("1.1")
        w = wiggly(1.3, 0.2 * UP)
        self.play(ShowCreation(w), run_time=1.5)
        self.cue("stretch and bend")
        self.play(Transform(w, Circle(radius=1.5).set_stroke(SHAPE, 4).move_to(0.2 * UP)), run_time=2.5)
        self.cue("never tear")
        no = txt("no tearing, no gluing", 28, GREY_A).next_to(w, DOWN, buff=0.5)
        self.play(FadeIn(no))
        self.finish()
        self.play(FadeOut(VGroup(w, no)))

        self.narrate("1.2")
        m = mug(3.0 * LEFT + 0.4 * UP)
        d = doughnut(3.4, 1.9, 3.0 * RIGHT + 0.4 * UP)
        eq = Tex("=", font_size=72).move_to(0.4 * UP)
        labels = VGroup(*[txt("one hole", 26, GREY_A).next_to(x, DOWN, buff=0.4) for x in (m, d)])
        self.play(FadeIn(m), FadeIn(d))
        self.cue("Each has exactly")
        self.play(FadeIn(eq), FadeIn(labels))
        self.finish()
        self.play(FadeOut(VGroup(m, eq, labels)))

        self.narrate("1.3")
        b = ball(1.3, 3.0 * LEFT + 0.4 * UP)
        ne = Tex(R"\neq", font_size=72).move_to(0.4 * UP)
        self.play(FadeIn(b), FadeIn(ne))
        self.finish()
        self.play(FadeOut(VGroup(b, ne, d)))

        self.narrate("1.4")
        ground = Arc(start_angle=PI / 2 - 0.55, angle=1.1, radius=7).move_to(1.0 * DOWN)
        ground.set_stroke(BALL, 4)
        top = ground.point_from_proportion(0.5)
        head = Circle(radius=0.14).set_stroke(WHITE, 3).move_to(top + 0.95 * UP)
        body = VGroup(Line(top + 0.8 * UP, top + 0.35 * UP), Line(top + 0.35 * UP, top + 0.15 * LEFT),
                      Line(top + 0.35 * UP, top + 0.15 * RIGHT), Line(top + 0.65 * UP, top + 0.6 * UP + 0.3 * LEFT),
                      Line(top + 0.65 * UP, top + 0.6 * UP + 0.3 * RIGHT)).set_stroke(WHITE, 3)
        view = DashedVMobject(Circle(radius=1.6).move_to(top + 0.4 * UP), num_dashes=40).set_stroke(GREY_B, 2)
        sees = txt("all you can see", 24, GREY_A).next_to(view, RIGHT, buff=0.3)
        self.play(ShowCreation(ground), FadeIn(VGroup(head, body)))
        self.play(ShowCreation(view), FadeIn(sees))
        self.finish()
        self.play(FadeOut(VGroup(ground, head, body, view, sees)))

        self.narrate("1.5")
        b = ball(1.5, 3.0 * LEFT + 0.4 * UP)
        phi = ValueTracker(-0.3)
        bl = always_redraw(lambda: lat_loop(b, phi.get_value()))
        self.play(FadeIn(b), ShowCreation(bl))
        self.cue("every loop shrinks")
        self.play(phi.animate.set_value(PI / 2), run_time=2.5)
        self.finish()

        self.narrate("1.6")
        d = doughnut(4.0, 2.2, 3.0 * RIGHT + 0.4 * UP)
        t = ValueTracker(0.0)
        dl = always_redraw(lambda: ring_loop(d, t.get_value()))
        self.play(FadeIn(d), ShowCreation(dl))
        self.play(t.animate.set_value(1.0), run_time=2.5)
        stuck = txt("stuck", 30, RED_C).next_to(d, DOWN, buff=0.35)
        self.play(FadeIn(stuck))
        self.finish()

        self.narrate("1.7")
        sc = txt("simply connected", 32, YELLOW).next_to(b, DOWN, buff=0.35)
        self.play(FadeIn(sc, shift=0.1 * UP))
        self.finish()
        self.remove(bl, dl)
        self.play(FadeOut(VGroup(b, d, sc, stuck, lat_loop(b, PI / 2), ring_loop(d, 1.0))))

        self.narrate("1.8")
        shapes = VGroup(ball(1.0), doughnut(2.6, 1.5), doughnut(3.6, 1.6, holes=(-0.85, 0.85)))
        shapes.arrange(RIGHT, buff=1.0).move_to(0.6 * UP)
        marks = VGroup(tick(s=1.4), cross(s=1.2), cross(s=1.2))
        for mk, sh in zip(marks, shapes):
            mk.next_to(sh, DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(s) for s in shapes], lag_ratio=0.3))
        self.cue("Every closed surface")
        self.play(LaggedStart(*[ShowCreation(mk) for mk in marks], lag_ratio=0.3))
        self.finish()

        self.recap("1.9", ["Shapes up to stretching.", "The lasso test: can every loop shrink?"])


# ---------------------------------------------------------------------------
# Chapter 2 — the question
# ---------------------------------------------------------------------------

class C2Question(Video):
    def construct(self):
        self.chapter(1, "2. The question")
        self.narrate("2.1")
        L = 3.6
        screen = Square(L).set_stroke(GREY_B, 2).move_to(0.3 * UP)
        o = screen.get_center()
        tt = ValueTracker(0.0)

        def pos():
            t = tt.get_value()
            x = (0.9 * t + 0.4 * L) % L - L / 2
            y = (0.37 * t + 0.5 * L) % L - L / 2
            return o + np.array([x, y, 0])
        dot = always_redraw(lambda: Dot(pos(), radius=0.12, fill_color=YELLOW))
        arrow = always_redraw(lambda: Arrow(pos(), pos() + 0.55 * normalize(np.array([0.9, 0.37, 0])), buff=0.12,
                                            fill_color=YELLOW, thickness=3))
        self.play(ShowCreation(screen), FadeIn(dot))
        self.add(arrow)
        self.play(tt.animate.set_value(3.0), run_time=3, rate_func=linear)
        self.finish()

        self.narrate("2.2")
        self.play(tt.animate.set_value(14.0), run_time=10, rate_func=linear)
        self.finish()
        self.remove(dot, arrow)
        self.play(FadeOut(screen))

        self.narrate("2.3")
        s1 = Line(LEFT, RIGHT).set_stroke(SHAPE, 5).move_to(3.6 * LEFT + 1.0 * UP)
        s2 = Line(LEFT, RIGHT).set_stroke(SHAPE, 5).move_to(3.6 * LEFT + 0.2 * DOWN)
        self.play(ShowCreation(s1), ShowCreation(s2))
        c = 3.6 * LEFT + 0.4 * UP
        self.play(Transform(s1, Arc(start_angle=0, angle=PI, radius=0.95).set_stroke(SHAPE, 5).move_to(c + 0.475 * UP)),
                  Transform(s2, Arc(start_angle=PI, angle=PI, radius=0.95).set_stroke(SHAPE, 5).move_to(c + 0.475 * DOWN)),
                  run_time=2)
        l1 = txt("a circle", 30).next_to(c, DOWN, buff=1.4)
        self.play(FadeIn(l1))
        self.finish()

        self.narrate("2.4")
        d1 = Circle(radius=0.7).set_fill(BALL, 0.3).set_stroke(BALL, 3).move_to(1.0 * LEFT + 0.4 * UP)
        d2 = Circle(radius=0.7).set_fill(BALL, 0.3).set_stroke(BALL, 3).move_to(1.0 * RIGHT + 0.4 * UP)
        self.play(FadeIn(d1), FadeIn(d2))
        target = ball(0.95, 0.4 * UP)
        self.play(d1.animate.move_to(0.4 * UP), d2.animate.move_to(0.4 * UP), run_time=1.5)
        self.play(FadeOut(VGroup(d1, d2)), FadeIn(target))
        l2 = txt("a sphere", 30).next_to(target, DOWN, buff=0.45)
        self.play(FadeIn(l2))
        self.finish()

        self.narrate("2.5")
        cL, cR = 2.7 * RIGHT + 0.4 * UP, 5.1 * RIGHT + 0.4 * UP
        bL = Circle(radius=1.0).set_fill(BLUE_D, 0.45).set_stroke(BALL, 3).move_to(cL)
        bR = Circle(radius=1.0).set_fill(PURPLE_D, 0.45).set_stroke(PURPLE_B, 3).move_to(cR)
        mark1 = Dot(cL + RIGHT, radius=0.08, fill_color=YELLOW)
        mark2 = Dot(cR + LEFT, radius=0.08, fill_color=YELLOW)
        glue = DashedLine(cL + RIGHT, cR + LEFT).set_stroke(YELLOW, 2)
        self.play(FadeIn(bL), FadeIn(bR))
        self.play(FadeIn(mark1), FadeIn(mark2), ShowCreation(glue))
        l3 = txt("the three-sphere", 30, YELLOW).next_to(VGroup(bL, bR), DOWN, buff=0.45)
        self.play(FadeIn(l3))
        self.cue("Leave one ball")
        walker = Dot(cL + 0.5 * LEFT, radius=0.11, fill_color=WHITE)
        self.play(FadeIn(walker))
        self.play(walker.animate.move_to(cL + RIGHT), run_time=1.5, rate_func=linear)
        walker.move_to(cR + LEFT)
        self.play(walker.animate.move_to(cR + 0.4 * LEFT), run_time=1.2, rate_func=linear)
        self.finish()

        self.narrate("2.6")
        lp = Ellipse(width=1.0, height=0.6).set_stroke(LOOP, 4).move_to(cL + 0.1 * DOWN)
        self.play(FadeOut(walker), ShowCreation(lp))
        self.cue("every loop in it")
        self.play(lp.animate.scale(0.02), run_time=2)
        self.finish()
        self.play(FadeOut(lp))
        self.clear_content()

        self.narrate("2.7")
        stmt = card(["Every closed three-dimensional space in which", "every loop can shrink is a three-sphere."],
                    title="The Poincaré conjecture", width=10, size=32).move_to(0.4 * UP)
        self.play(FadeIn(stmt))
        self.finish()
        self.play(FadeOut(stmt))

        self.narrate("2.8")
        line = Line(5.5 * LEFT, 5.5 * RIGHT).set_stroke(GREY_B, 2).shift(0.4 * UP)
        events = [(-4.4, "1904", "Poincaré asks"), (-1.5, "1961", "Smale:\ndimensions 5 and up"),
                  (1.4, "1982", "Freedman:\ndimension 4"), (4.3, "2000", "Millennium Prize")]
        marks = VGroup()
        for x, year, what in events:
            dt = Dot(np.array([x, 0.4, 0]), radius=0.09, fill_color=YELLOW)
            yr = txt(year, 26, YELLOW).next_to(dt, UP, buff=0.2)
            wt = txt(what, 22, GREY_A).next_to(dt, DOWN, buff=0.25)
            marks.add(VGroup(dt, yr, wt))
        self.play(ShowCreation(line), FadeIn(marks[0]))
        self.cue("Stephen Smale")
        self.play(FadeIn(marks[1], shift=0.1 * UP))
        self.cue("Michael Freedman")
        self.play(FadeIn(marks[2], shift=0.1 * UP))
        self.finish()

        self.narrate("2.9")
        three = txt("dimension 3: open", 26, RED_C).next_to(marks[0], DOWN, buff=0.3)
        self.play(FadeIn(three))
        self.cue("In 2000")
        self.play(FadeIn(marks[3], shift=0.1 * UP))
        self.finish()

        self.recap("2.10", ["Does every loop shrinking", "force a three-sphere?"])


# ---------------------------------------------------------------------------
# Chapter 3 — Ricci flow
# ---------------------------------------------------------------------------

class C3Flow(Video):
    def construct(self):
        self.chapter(2, "3. Ricci flow")
        self.narrate("3.1")
        lumpy = ParametricCurve(lambda s: 0.3 * UP + (1.5 + 0.28 * math.sin(3 * s) + 0.15 * math.cos(7 * s)) *
                                np.array([math.cos(s), math.sin(s), 0]),
                                t_range=(0, TAU, TAU / 300)).set_stroke(SHAPE, 4).set_fill(SHAPE, 0.15)
        self.play(ShowCreation(lumpy), run_time=2)
        self.finish()
        self.play(FadeOut(lumpy))

        self.narrate("3.2")
        ax = Chart((-math.pi, math.pi), (0, 2.2), 7.5, 3.2, grid=False, xlabel="position", ylabel="temperature")
        ax.shift(0.4 * UP - ax.box.get_center())
        heat = ValueTracker(0.0)
        coeffs = [(3, 0.35), (5, 0.25), (8, 0.18), (13, 0.12), (2, 0.2)]

        def temp(x):
            t = heat.get_value()
            return 1.0 + sum(a * math.exp(-k * k * t) * math.cos(k * x + k) for k, a in coeffs)
        prof = always_redraw(lambda: curve(ax, temp, -math.pi, math.pi, n=400, color=ORANGE))
        self.play(FadeIn(ax), FadeIn(prof))
        self.cue("the way heat flows")
        self.play(heat.animate.set_value(0.6), run_time=4)
        self.finish()
        self.remove(prof)
        self.play(FadeOut(VGroup(ax, curve(ax, temp, -math.pi, math.pi, n=400, color=ORANGE))))

        self.narrate("3.3")
        parts = VGroup(Tex(R"\partial_t g", font_size=80), Tex("=", font_size=80),
                       Tex(R"-2 \operatorname{Ric}(g)", font_size=80)).arrange(RIGHT, buff=0.35).move_to(0.9 * UP)
        parts[0].set_color(BLUE_B)
        parts[2].set_color(ORANGE)
        labs = VGroup(txt("how the shape changes", 26, BLUE_B).next_to(parts[0], DOWN, buff=0.5),
                      txt("its curvature", 26, ORANGE).next_to(parts[2], DOWN, buff=0.5))
        self.play(Write(parts))
        self.play(FadeIn(labs))
        self.cue("Where the space curves like a sphere")
        sph = VGroup(ball(0.6), txt("shrinks", 24, GREY_A)).arrange(DOWN, buff=0.2).move_to(2.6 * LEFT + 1.4 * DOWN)
        sad = VGroup(ParametricCurve(lambda s: np.array([s, 0.25 * s * s, 0]), t_range=(-0.8, 0.8, 0.02)),
                     ParametricCurve(lambda s: np.array([s, -0.25 * s * s - 0.35, 0]), t_range=(-0.8, 0.8, 0.02)))
        sad.set_stroke(TORUS, 3)
        sadg = VGroup(sad, txt("expands", 24, GREY_A)).arrange(DOWN, buff=0.2).move_to(2.6 * RIGHT + 1.4 * DOWN)
        self.play(FadeIn(sph))
        self.cue("where it curves like a saddle")
        self.play(FadeIn(sadg))
        self.finish()
        self.play(FadeOut(VGroup(parts, labs, sph, sadg)))

        self.narrate("3.4")
        snaps = curve_shortening()
        k = ValueTracker(0.0)
        cl, cr = 3.2 * LEFT + 0.3 * UP, 3.2 * RIGHT + 0.3 * UP
        left = always_redraw(lambda: snap_curve(snaps, k.get_value(), cl))
        self.play(ShowCreation(left), run_time=1.5)
        self.cue("Every point moves")
        self.play(k.animate.set_value(14), run_time=7, rate_func=linear)
        self.finish()

        self.narrate("3.5")
        right = always_redraw(lambda: snap_curve(snaps, k.get_value(), cr, scale=1.0, rescale=True, color=YELLOW))
        rl = txt("rescaled to the same size", 24, GREY_A).move_to(cr + 2.2 * DOWN)
        self.play(FadeIn(right), FadeIn(rl))
        self.play(k.animate.set_value(len(snaps) - 1.001), run_time=6, rate_func=linear)
        self.finish()
        self.remove(left, right)
        self.play(FadeOut(VGroup(rl, snap_curve(snaps, len(snaps) - 1.001, cl),
                                 snap_curve(snaps, len(snaps) - 1.001, cr, scale=1.0, rescale=True, color=YELLOW))))

        self.narrate("3.6")
        bt = ValueTracker(0.0)
        bb = always_redraw(lambda: blob(bt.get_value(), 0.4 * UP))
        pl = txt("curved positively everywhere", 26, GREY_A).move_to(2.2 * DOWN)
        self.play(FadeIn(bb), FadeIn(pl))
        self.cue("They become rounder")
        self.play(bt.animate.set_value(0.995), run_time=5)
        self.finish()
        self.remove(bb)
        self.play(FadeOut(pl))

        self.recap("3.7", ["Ricci flow: let the shape smooth itself", "by its own curvature."])


# ---------------------------------------------------------------------------
# Chapter 4 — necks
# ---------------------------------------------------------------------------

class C4Necks(Video):
    def construct(self):
        self.chapter(2, "4. Necks that pinch")
        self.narrate("4.1")
        neck = ValueTracker(0.45)
        bulb = ValueTracker(0.95)
        center = 0.3 * UP
        dumb = always_redraw(lambda: profile_shape(lambda x: dumbbell(x, neck.get_value(), R=bulb.get_value()),
                                                   -1.5 - bulb.get_value(), 1.5 + bulb.get_value(), scale=1.6,
                                                   center=center))
        self.play(FadeIn(dumb))
        self.finish()

        self.narrate("4.2")
        self.cue("It pinches off")
        self.play(neck.animate.set_value(0.0), bulb.animate.set_value(0.86), run_time=4, rate_func=rush_into)
        self.finish()

        self.narrate("4.3")
        flash = Dot(center, radius=0.16, fill_color=RED_C)
        sing = txt("singularity", 32, RED_C).next_to(flash, UP, buff=0.9)
        arr = Arrow(sing.get_bottom(), center + 0.12 * UP, buff=0.1, fill_color=RED_C, thickness=3)
        self.play(GrowFromCenter(flash), Flash(center, color=RED_C, flash_radius=0.6))
        self.cue("This is called")
        self.play(FadeIn(sing), GrowArrow(arr))
        self.finish()
        self.play(FadeOut(VGroup(flash, sing, arr)))

        self.narrate("4.4")
        self.play(neck.animate.set_value(0.22), bulb.animate.set_value(0.9), run_time=1.5)
        self.cue("cut it")
        cuts = VGroup(*[DashedLine(center + np.array([s * 0.45 * 1.6, 1.0, 0]), center + np.array([s * 0.45 * 1.6, -1.0, 0]))
                        for s in (-1, 1)]).set_stroke(CUT, 3)
        self.play(ShowCreation(cuts))
        pieces = VGroup(capped_piece(-1, 0.22, R=0.9).shift(center), capped_piece(1, 0.22, R=0.9).shift(center))
        self.remove(dumb)
        self.add(pieces)
        self.play(FadeOut(cuts), pieces[0].animate.shift(0.5 * LEFT), pieces[1].animate.shift(0.5 * RIGHT))
        self.cue("cap each end")
        self.play(Indicate(pieces, color=YELLOW, scale_factor=1.03))
        self.cue("and keep flowing")
        rounds = VGroup(*[Circle(radius=1.15).set_fill(SHAPE, 0.22).set_stroke(SHAPE, 3).move_to(p.get_center())
                          for p in pieces])
        self.play(FadeTransform(pieces, rounds), run_time=2)
        self.finish()
        self.play(FadeOut(rounds))

        self.narrate("4.5")
        items = ["1. only singularities you can cut", "2. cuts stay under control", "3. a clear ending"]
        lines = VGroup(*[txt(s, 32) for s in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(0.4 * UP)
        for line, phrase in zip(lines, ["Every singularity", "The cuts must not", "And the flow must end"]):
            self.cue(phrase)
            self.play(FadeIn(line, shift=0.1 * RIGHT))
        self.finish()
        self.play(FadeOut(lines))

        self.narrate("4.6")
        cg = cigar(center=0.4 * UP)
        q = txt("?", 72, RED_C).next_to(cg, UP, buff=0.3)
        self.play(ShowCreation(cg), run_time=2)
        self.cue("Hamilton could not")
        self.play(FadeIn(q))
        self.finish()
        self.play(FadeOut(VGroup(cg, q)))

        self.recap("4.7", ["Necks pinch; surgery cuts them.", "Three things were missing."])


# ---------------------------------------------------------------------------
# Chapter 5 — Perelman
# ---------------------------------------------------------------------------

class C5Perelman(Video):
    def construct(self):
        self.chapter(3, "5. What Perelman added")
        self.narrate("5.1")
        papers = paper_cards(28).move_to(0.4 * UP)
        for k, phrase in enumerate(["In November 2002", "posted the first", "Together"]):
            self.cue(phrase)
            self.play(FadeIn(papers[k], shift=0.1 * UP))
        self.finish()
        self.play(FadeOut(papers))

        self.narrate("5.2")
        ax = Chart((0, 1), (0, 1), 6.5, 3.0, grid=False, xlabel="time", ylabel="entropy")
        ax.shift(0.4 * UP - ax.box.get_center())
        ent = curve(ax, lambda t: 0.15 + 0.75 * (1 - math.exp(-3 * t)) + 0.05 * math.sin(6 * t) * t, 0, 1,
                    color=YELLOW, width=5)
        up = txt("only goes up", 26, YELLOW).move_to(ax.c2p(0.7, 0.4))
        self.play(FadeIn(ax))
        self.play(ShowCreation(ent), run_time=2.5)
        self.play(FadeIn(up))
        self.finish()
        self.play(FadeOut(VGroup(ax, ent, up)))

        self.narrate("5.3")
        good = Circle(radius=0.9).set_fill(SHAPE, 0.25).set_stroke(SHAPE, 3).move_to(2.6 * LEFT + 0.6 * UP)
        bad = Ellipse(width=2.6, height=0.28).set_fill(SHAPE, 0.25).set_stroke(SHAPE, 3).move_to(2.6 * RIGHT + 0.6 * UP)
        tg = tick(s=1.4).next_to(good, DOWN, buff=0.4)
        cb = cross(s=1.2).next_to(bad, DOWN, buff=0.9)
        nlc = txt("no local collapsing", 32, YELLOW).move_to(2.0 * DOWN)
        self.play(FadeIn(good), FadeIn(bad))
        self.play(ShowCreation(tg), ShowCreation(cb))
        self.cue("A small ball always")
        self.play(FadeIn(nlc))
        self.finish()
        self.play(FadeOut(VGroup(good, bad, tg, cb, nlc)))

        self.narrate("5.4")
        cg = cigar(center=0.6 * LEFT + 0.6 * UP)
        tip = cg[0].get_left()
        zoom = Square(0.9).set_stroke(GREY_B, 2).move_to(tip + 0.35 * RIGHT)
        inset = VGroup(Line(LEFT, RIGHT), Line(LEFT, RIGHT).shift(0.12 * DOWN)).set_stroke(SHAPE, 3)
        frame = Rectangle(width=2.6, height=1.4).set_stroke(GREY_B, 2)
        inset_g = VGroup(frame, inset.move_to(frame)).move_to(3.4 * LEFT + 1.6 * DOWN)
        link = DashedLine(zoom.get_bottom(), frame.get_top()).set_stroke(GREY_B, 1.5)
        lab = txt("collapsed", 24, GREY_A).next_to(frame, RIGHT, buff=0.3)
        self.play(ShowCreation(cg), run_time=1.5)
        self.cue("Zoom in")
        self.play(ShowCreation(zoom), ShowCreation(link), FadeIn(inset_g), FadeIn(lab))
        self.cue("which the flow can never")
        self.play(ShowCreation(Cross(cg, stroke_color=RED_C)))
        self.finish()
        self.clear_content()

        self.narrate("5.5")
        models = VGroup(neck_model(), neck_model(capped=True),
                        Circle(radius=0.55).set_stroke(SHAPE, 3)).arrange(RIGHT, buff=1.4).move_to(0.6 * UP)
        names = VGroup(*[txt(s, 24, GREY_A).next_to(m, DOWN, buff=0.4) for s, m in
                         zip(["a thin neck", "a capped neck", "a small round piece"], models)])
        for k, phrase in enumerate(["a thin round neck", "a neck closed off", "or a small"]):
            self.cue(phrase)
            self.play(FadeIn(models[k]), FadeIn(names[k]))
        self.finish()

        self.narrate("5.6")
        cuts = VGroup(*[DashedLine(m.get_top() + 0.3 * UP, m.get_bottom() + 0.3 * DOWN).set_stroke(CUT, 3)
                        for m in models[:2]])
        whole = txt("set aside whole", 22, CUT).next_to(models[2], UP, buff=0.3)
        self.play(LaggedStart(*[ShowCreation(c) for c in cuts], FadeIn(whole), lag_ratio=0.4))
        self.finish()
        self.clear_content()

        self.narrate("5.7")
        axis = Arrow(5.5 * LEFT, 5.5 * RIGHT, buff=0, fill_color=GREY_B, thickness=2).shift(0.4 * UP)
        tl = txt("time", 24, GREY_A).next_to(axis, DOWN, buff=0.2).align_to(axis, RIGHT)
        ticks_ = VGroup(*[Line(UP * 0.3, DOWN * 0.3).set_stroke(CUT, 4).move_to(np.array([x, 0.4, 0]))
                          for x in (-3.8, -2.2, -1.1, 0.6, 1.9, 3.3)])
        sl = txt("surgeries", 24, CUT).next_to(ticks_, UP, buff=0.3)
        brace = Brace(VGroup(*ticks_[:4]), DOWN, buff=0.4)
        bl = txt("finitely many before any moment", 24, YELLOW).next_to(brace, DOWN, buff=0.15)
        self.play(GrowArrow(axis), FadeIn(tl))
        self.play(LaggedStart(*[ShowCreation(t) for t in ticks_], lag_ratio=0.25), FadeIn(sl))
        self.cue("only finitely many")
        self.play(GrowFromCenter(brace), FadeIn(bl))
        self.finish()
        self.clear_content()

        self.narrate("5.8")
        ax = Chart((0, 1.05), (0, 1.1), 7.5, 3.2, grid=False, xlabel="time", ylabel="total volume")
        ax.shift(0.4 * UP - ax.box.get_center())
        segs = [(0.0, 0.32, 1.0), (0.32, 0.58, 0.78), (0.58, 0.81, 0.52), (0.81, 1.0, 0.27)]
        parts = VGroup()
        for i, (a, b, v0) in enumerate(segs):
            if i < 3:
                parts.add(curve(ax, lambda t, a=a, b=b, v0=v0: v0 * (1 - 0.55 * (t - a) / (b - a)), a, b,
                                color=BLUE_C, width=5))
                parts.add(DashedLine(ax.c2p(b, v0 * 0.45), ax.c2p(b, segs[i + 1][2])).set_stroke(CUT, 3))
            else:
                parts.add(curve(ax, lambda t, a=a, b=b, v0=v0: v0 * math.sqrt(max(1 - (t - a) / (b - a), 0)), a,
                                b - 1e-4, color=BLUE_C, width=5))
        ext = VGroup(Dot(ax.c2p(1.0, 0), radius=0.1, fill_color=YELLOW),
                     txt("extinct", 26, YELLOW).next_to(ax.c2p(1.0, 0), RIGHT, buff=0.25))
        self.play(FadeIn(ax))
        self.play(ShowCreation(parts, lag_ratio=1.0), run_time=5, rate_func=linear)
        self.play(FadeIn(ext))
        self.finish()
        self.clear_content()

        self.narrate("5.9")
        ax = Chart((0, 1.2), (0, 1.1), 7.0, 3.2, grid=False, xlabel="time", ylabel="width")
        ax.shift(0.4 * UP - ax.box.get_center())
        bound = curve(ax, lambda t: 1.0 - t, 0, 1.0, color=GREY_B, width=3)
        wid = curve(ax, lambda t: max(0.0, (1.0 - t) * (0.82 - 0.1 * math.sin(7 * t))), 0, 1.0, color=YELLOW, width=5)
        bl = txt("falls at a steady rate", 24, GREY_A).move_to(ax.c2p(0.62, 0.72))
        z = VGroup(Dot(ax.c2p(1.0, 0), radius=0.1, fill_color=RED_C),
                   txt("zero", 26, RED_C).next_to(ax.c2p(1.0, 0), UP, buff=0.35))
        self.play(FadeIn(ax))
        self.cue("using the smallest disc")
        self.play(ShowCreation(wid), run_time=2.5)
        self.cue("shrinks at a steady rate")
        self.play(ShowCreation(bound), FadeIn(bl))
        self.cue("must reach zero")
        self.play(FadeIn(z))
        self.finish()

        self.recap("5.10", ["An entropy that only rises; no collapsing;",
                            "a short list of models; controlled surgery; extinction."])


# ---------------------------------------------------------------------------
# Chapter 6 — putting it together
# ---------------------------------------------------------------------------

def three_bulbs(neck):
    def r(x):
        bulbs = [math.sqrt(max(1.0 - (x - c) ** 2, 0.0)) for c in (-2.4, 0.0, 2.4)]
        between = neck if -2.4 <= x <= 2.4 else 0.0
        return max(max(bulbs), between)
    return r


class C6Together(Video):
    def construct(self):
        self.chapter(3, "6. Putting it together")
        self.narrate("6.1")
        neck = ValueTracker(0.45)
        center = 0.4 * UP
        shape = always_redraw(lambda: profile_shape(three_bulbs(neck.get_value()), -3.4, 3.4, scale=1.3,
                                                    center=center))
        self.play(FadeIn(shape))
        self.cue("Run the flow")
        self.play(neck.animate.set_value(0.12), run_time=2.5)
        self.cue("cut each neck")
        cx = [-2.4, 0.0, 2.4]
        cuts = VGroup(*[DashedLine(center + np.array([x * 1.3, 0.8, 0]), center + np.array([x * 1.3, -0.8, 0]))
                        for x in (-1.2, 1.2)]).set_stroke(CUT, 3)
        self.play(ShowCreation(cuts))
        balls = VGroup(*[Circle(radius=1.1).set_fill(SHAPE, 0.22).set_stroke(SHAPE, 3).move_to(center + x * 1.3 * RIGHT)
                         for x in cx])
        self.remove(shape)
        self.play(FadeOut(cuts), FadeIn(balls), run_time=0.8)
        self.play(*[b.animate.shift(0.3 * d * RIGHT) for b, d in zip(balls, (-1, 0, 1))])
        self.cue("After finitely many")
        self.play(*[b.animate.scale(0.01) for b in balls], run_time=2.5, rate_func=rush_into)
        self.remove(balls)
        self.finish()

        self.narrate("6.2")
        spots = [center + (x * 1.3 + 0.3 * d) * RIGHT for x, d in zip(cx, (-1, 0, 1))]
        balls = VGroup(*[ball(1.0, p) for p in spots])
        labels = VGroup(*[txt("a round sphere", 22, GREY_A).next_to(b, DOWN, buff=0.3) for b in balls])
        self.play(LaggedStart(*[GrowFromCenter(b) for b in balls], lag_ratio=0.3), run_time=2)
        self.play(FadeIn(labels))
        self.cue("or one of a few")
        rel = VGroup(doughnut(1.6, 0.9), doughnut(1.6, 0.9)).arrange(DOWN, buff=0.6).move_to(5.6 * RIGHT + 0.4 * UP)
        self.play(balls.animate.shift(1.0 * LEFT), labels.animate.shift(1.0 * LEFT), FadeIn(rel))
        self.finish()

        self.narrate("6.3")
        loops = VGroup(*[ring_loop(r, 1.0) for r in rel])
        self.play(ShowCreation(loops))
        xs = VGroup(*[Cross(VGroup(r, l), stroke_color=RED_C) for r, l in zip(rel, loops)])
        self.cue("our shape has none")
        self.play(ShowCreation(xs))
        self.play(FadeOut(VGroup(rel, loops, xs)), labels.animate.set_color(YELLOW))
        self.finish()

        self.narrate("6.4")
        self.play(FadeOut(labels))
        self.play(balls[0].animate.move_to(center + 1.7 * LEFT), balls[2].animate.move_to(center + 1.7 * RIGHT),
                  balls[1].animate.move_to(center), run_time=1.5)
        one = ball(1.6, center)
        self.play(FadeTransform(balls, one), run_time=2)
        lab = txt("a three-sphere", 30, YELLOW).next_to(one, DOWN, buff=0.4)
        self.play(FadeIn(lab))
        self.finish()

        self.recap("6.5", ["Flow, cut, burn away,", "and read the answer backwards."])


# ---------------------------------------------------------------------------
# Chapter 7 — checked
# ---------------------------------------------------------------------------

class C7Checked(Video):
    def construct(self):
        self.chapter(4, "7. Checked")
        self.narrate("7.1")
        papers = paper_cards(28).move_to(0.9 * UP)
        nj = txt("never sent to a journal", 28, GREY_A).next_to(papers, DOWN, buff=0.5)
        self.play(FadeIn(papers))
        self.play(FadeIn(nj))
        self.finish()
        self.play(FadeOut(VGroup(papers, nj)))

        self.narrate("7.2")
        teams = [("Kleiner and Lott", "detailed notes"), ("Morgan and Tian", "a book-length proof"),
                 ("Cao and Zhu", "a complete account")]
        cards = VGroup(*[card([a, b], width=3.9, size=26) for a, b in teams]).arrange(RIGHT, buff=0.3).move_to(0.8 * UP)
        tks = VGroup(*[tick(s=1.3).next_to(c, DOWN, buff=0.35) for c in cards])
        for c, phrase in zip(cards, ["Bruce Kleiner", "John Morgan", "Huai-Dong Cao"]):
            self.cue(phrase)
            self.play(FadeIn(c, shift=0.1 * UP))
        self.cue("By 2006")
        self.play(LaggedStart(*[ShowCreation(t) for t in tks], lag_ratio=0.3))
        self.finish()
        self.play(FadeOut(VGroup(cards, tks)))

        self.narrate("7.3")
        medal = VGroup(Polygon([-0.35, 0.9, 0], [0.0, 0.25, 0], [0.35, 0.9, 0]).set_fill(BLUE_D, 1).set_stroke(width=0),
                       Circle(radius=0.6).set_fill(GOLD_D, 1).set_stroke(GOLD_B, 3).move_to(0.25 * DOWN))
        medal.move_to(3.4 * LEFT + 0.6 * UP)
        fm = VGroup(txt("Fields Medal, 2006", 34), txt("declined", 32, RED_C)).arrange(DOWN, buff=0.3)
        fm.next_to(medal, RIGHT, buff=0.8)
        self.play(FadeIn(medal), FadeIn(fm[0]))
        self.cue("He became the first")
        self.play(FadeIn(fm[1]))
        self.finish()
        self.play(FadeOut(VGroup(medal, fm)))

        self.narrate("7.4")
        mp = card(["Millennium Prize, 2010", "one million dollars"], width=7, size=34).move_to(0.9 * UP)
        dec = txt("declined", 32, RED_C).next_to(mp, DOWN, buff=0.4)
        self.play(FadeIn(mp))
        self.cue("He declined that too")
        self.play(FadeIn(dec))
        self.finish()
        self.play(FadeOut(VGroup(mp, dec)))

        self.recap("7.5", ["Checked by several teams.", "Two prizes, both declined."])


# ---------------------------------------------------------------------------
# Chapter 8 — meaning
# ---------------------------------------------------------------------------

class C8Meaning(Video):
    def construct(self):
        self.chapter(4, "8. What it means")
        items = [("8.1", True, "The Poincaré conjecture is true"),
                 ("8.2", True, "Geometrization: every closed 3D space is built from eight kinds of pieces"),
                 ("8.3", False, "The smooth four-dimensional version is still open"),
                 ("8.4", False, "No complete computer-checked proof yet")]
        rows = mark_rows([(g, t) for _, g, t in items], size=30).move_to(0.4 * UP)
        for (beat, *_), row in zip(items, rows):
            self.narrate(beat)
            self.play(FadeIn(row, shift=0.1 * RIGHT))
            self.finish()
        self.recap("8.5", ["The only Millennium problem", "the Clay Institute has declared solved."])


# ---------------------------------------------------------------------------
# Chapter 9 — closing
# ---------------------------------------------------------------------------

class C9Close(Video):
    def construct(self):
        self.chapter_title = "9. Closing"
        self.narrate("9.1")
        big = self.roadmap(-1, big=True).move_to(3.0 * UP)
        self.play(FadeIn(big, lag_ratio=0.2))
        b = ball(1.3, 3.2 * LEFT + 0.2 * DOWN)
        phi = ValueTracker(-0.25)
        loop = always_redraw(lambda: lat_loop(b, phi.get_value()))
        self.play(FadeIn(b), ShowCreation(loop))
        self.play(phi.animate.set_value(PI / 2), run_time=2.5)
        self.cue("A shape that smooths")
        snaps = curve_shortening()
        k = ValueTracker(0.0)
        cc = 3.0 * RIGHT + 0.2 * DOWN
        cv = always_redraw(lambda: snap_curve(snaps, k.get_value(), cc, scale=1.2))
        self.play(ShowCreation(cv))
        self.play(k.animate.set_value(len(snaps) - 1.001), run_time=6, rate_func=linear)
        self.finish()

        self.narrate("9.2")
        self.remove(loop, cv)
        self.play(FadeOut(VGroup(big, b, lat_loop(b, PI / 2), snap_curve(snaps, len(snaps) - 1.001, cc, scale=1.2))))
        title = txt("Perelman's proof of the Poincaré conjecture", 46)
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
        title = txt("The Poincaré conjecture", 60).to_edge(UP, buff=0.6)
        sub = txt("Perelman's proof, explained for everyone", 30, GREY_A).next_to(title, DOWN, buff=0.25)
        b = ball(1.4, 4.2 * LEFT + 0.9 * DOWN)
        loop = lat_loop(b, 0.75)
        dumb = profile_shape(lambda x: dumbbell(x, 0.18), -2.45, 2.45, scale=1.05, center=0.2 * RIGHT + 0.9 * DOWN)
        snaps = curve_shortening()
        curves = VGroup(*[snap_curve(snaps, i, 4.4 * RIGHT + 0.9 * DOWN, scale=1.0,
                                     color=interpolate_color(BLUE_B, YELLOW, i / (len(snaps) - 1)))
                          for i in (0, 25, 50, 75)])
        self.add(title, sub, b, loop, dumb, curves)
