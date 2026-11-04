"""Narrated explainer for "The rational Hodge conjecture for CM abelian varieties"
(OpenAI, September–October 2026), written for 3b1b's manim (manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("3.4") and
the words come from beat 3.4 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl hodge_video.py C3CM -w -l --config_file ../../../../../tools/video/custom_config.yml

Computed: the Hodge numbers of an abelian threefold, which lattices a turn
carries to themselves, and the balanced sign quadruples of the paper's
four-factor relation. Doughnuts, shadows, the ball quotient and the landscape
of varieties are schematics.
"""

from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "video"))
from narrated import *  # noqa: E402,F403

TORUS = TEAL_C
LOOPA = ORANGE
LOOPB = GREEN_C
HODGE = ORANGE
CMC = ORANGE
LAT = BLUE_C


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["Shapes", "The conjecture", "CM", "How it works", "Is it right?"]
    PRONOUNCE = [(r"\bWeil\b", "Vay"), (r"\bGrothendieck\b", "Grow-ten-deek"), (r"\bMilne\b", "Miln"),
                 (r"\bHecke\b", "Hecka"), (r"\bDeligne\b", "Duh-leen"),
                 (r"\b1924\b", "nineteen twenty-four"), (r"\b1950\b", "nineteen fifty"),
                 (r"\b1982\b", "nineteen eighty-two"), (r"\b2025\b", "twenty twenty-five"),
                 (r"\b2026\b", "twenty twenty-six")]
    BUILD = HERE / "build"


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def tick(color=GREEN_C, s=1.0):
    return VMobject().set_points_as_corners([[-0.22 * s, 0, 0], [-0.06 * s, -0.18 * s, 0], [0.24 * s, 0.22 * s, 0]]
                                            ).set_stroke(color, 6)


def cross(color=RED_C, s=1.0):
    a = 0.18 * s
    return VGroup(Line([-a, -a, 0], [a, a, 0]), Line([-a, a, 0], [a, -a, 0])).set_stroke(color, 6)


def doughnut(w=5.0, h=2.6, center=ORIGIN, color=TORUS):
    body = Ellipse(width=w, height=h).set_fill(color, 0.18).set_stroke(color, 3)
    hw = 0.36 * w
    smile = ArcBetweenPoints(np.array([-hw / 2, 0.08, 0]), np.array([hw / 2, 0.08, 0]), angle=1.3)
    frown = ArcBetweenPoints(np.array([-0.36 * hw, -0.02, 0]), np.array([0.36 * hw, -0.02, 0]), angle=-1.1)
    g = VGroup(body, smile.set_stroke(color, 3), frown.set_stroke(color, 3)).move_to(center)
    g.w, g.h = w, h
    return g


def loop_a(d):
    return Ellipse(width=0.72 * d.w, height=0.62 * d.h).set_stroke(LOOPA, 6).move_to(d[0].get_center() + 0.02 * UP)


def loop_b(d):
    c = d[0].get_center() + np.array([0.41 * d.w, 0, 0])
    front = Arc(start_angle=-PI / 2, angle=PI, radius=0.3 * d.h).stretch(0.4, 0).move_to(c + 0.05 * RIGHT)
    back = DashedVMobject(Arc(start_angle=PI / 2, angle=PI, radius=0.3 * d.h).stretch(0.4, 0).move_to(c),
                          num_dashes=10)
    return VGroup(front.set_stroke(LOOPB, 6), back.set_stroke(LOOPB, 3))


def hodge_diamond(g=3, cell=0.62):
    cells = VGroup()
    for p in range(g + 1):
        for q in range(g + 1):
            h = math.comb(g, p) * math.comb(g, q)
            box = RoundedRectangle(width=cell, height=cell * 0.75, corner_radius=0.08)
            mid = p == q
            box.set_stroke(HODGE if mid else GREY_B, 2).set_fill(HODGE if mid else GREY_E, 0.85 if mid else 0.6)
            t = txt(str(h), 26, BLACK if mid else WHITE)
            c = VGroup(box, t.move_to(box)).move_to(np.array([(q - p) * cell * 1.15, (p + q) * cell * 0.85, 0]))
            c.pq = (p, q)
            cells.add(c)
    rows = VGroup()
    for k in range(2 * g + 1):
        rows.add(txt(f"degree {k}", 20, GREY_B).move_to(np.array([-(g + 1) * cell * 1.15 - 0.6, k * cell * 0.85, 0])))
    return VGroup(cells, rows)


def lattice(w1, w2, n=4, radius=0.07, color=LAT, scale=0.9, box=2.4):
    dots = VGroup()
    for a in range(-n, n + 1):
        for b in range(-n, n + 1):
            z = (a * w1 + b * w2) * scale
            if abs(z.real) <= box and abs(z.imag) <= box:
                dots.add(Dot(np.array([z.real, z.imag, 0]), radius=radius, fill_color=color))
    return dots


def cell_poly(w1, w2, scale=0.9, color=LAT):
    pts = [0, w1, w1 + w2, w2]
    return Polygon(*[np.array([z.real * scale, z.imag * scale, 0]) for z in pts]).set_stroke(color, 2).set_fill(
        color, 0.25)


def sign_rows(quad, size=0.55):
    rows = VGroup()
    for k, v in enumerate(quad):
        row = VGroup(txt(f"v{k + 1}", 28, WHITE))
        for s in v:
            col = BLUE_C if s > 0 else ORANGE
            sq = Square(size).set_fill(col, 0.9).set_stroke(col, 2)
            row.add(VGroup(sq, txt("+" if s > 0 else "−", 30, WHITE).move_to(sq)))
        row.arrange(RIGHT, buff=0.18)
        rows.add(row)
    rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
    rows[2:].shift(0.35 * DOWN)
    return rows


BALANCED = None


def balanced_quads(n=3):
    pats = list(itertools.product([1, -1], repeat=n))
    quads = [(a, b, c, d) for a in pats for b in pats for c in pats for d in pats
             if all(a[i] + b[i] == c[i] + d[i] for i in range(n))]
    return pats, quads


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        d = doughnut(5.2, 2.7, 0.4 * UP)
        self.narrate("0.1")
        la, lb = loop_a(d), loop_b(d)
        self.play(FadeIn(d))
        self.play(ShowCreation(la))
        self.play(ShowCreation(lb))
        self.finish()

        self.narrate("0.2")
        cyc = ParametricCurve(lambda t: 0.4 * UP + np.array([1.3 * math.cos(t), 0.42 * math.sin(2 * t) - 0.1, 0]),
                              t_range=(0, TAU, TAU / 200)).set_stroke(YELLOW, 4)
        shadow = txt("its shadow: a class", 28, YELLOW).next_to(d, DOWN, buff=0.4)
        self.play(ShowCreation(cyc), run_time=1.5)
        self.play(FadeIn(shadow, shift=0.2 * DOWN))
        self.cue("Do all the entries")
        q = txt("?", 72, YELLOW).next_to(d, RIGHT, buff=0.4)
        self.play(FadeIn(q))
        self.finish()

        self.narrate("0.3")
        title = txt("The Hodge conjecture for CM abelian varieties", 46)
        sub = txt("OpenAI preprint, September 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(VGroup(d, la, lb, cyc, shadow, q)), Write(title, run_time=2))
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
        self.chapter(0, "1. Shapes, holes and shadows")
        self.narrate("1.1")
        circ = Circle(radius=1.4).set_stroke(BLUE_C, 4).move_to(2.6 * LEFT + 0.4 * UP)
        eq = Tex(R"x^2 + y^2 = 1", font_size=48).next_to(circ, RIGHT, buff=1.0)
        lab = txt("a variety: a shape cut out by equations", 28, YELLOW).move_to(2.0 * DOWN)
        self.play(ShowCreation(circ), Write(eq))
        self.play(FadeIn(lab))
        self.finish()
        self.play(FadeOut(VGroup(circ, eq, lab)))

        self.narrate("1.2")
        eq2 = Tex(R"y^2 = x^3 - x", font_size=52).move_to(2.2 * UP)
        d = doughnut(5.0, 2.6, 0.1 * DOWN)
        cl = txt("complex solutions", 26, GREY_A).next_to(d, DOWN, buff=0.3)
        self.play(Write(eq2))
        self.cue("The complex solutions")
        self.play(FadeIn(d, scale=0.6), FadeIn(cl), run_time=2)
        self.finish()

        self.narrate("1.3")
        la, lb = loop_a(d), loop_b(d)
        ta = txt("a class", 24, LOOPA).next_to(d, LEFT, buff=0.3)
        tb = txt("a class", 24, LOOPB).next_to(lb, RIGHT, buff=0.15)
        self.play(ShowCreation(la), FadeIn(ta))
        self.play(ShowCreation(lb), FadeIn(tb))
        self.finish()
        self.clear_content()

        self.narrate("1.4")
        blob = VGroup(*[Ellipse(width=2.4 - 0.4 * k, height=1.6 - 0.25 * k).set_stroke(TORUS, 2, opacity=1 - 0.2 * k)
                        for k in range(4)]).move_to(3.0 * LEFT + 0.4 * UP)
        stack = VGroup(*[card([f"degree {k}"], width=2.6, size=24) for k in range(5)]).arrange(UP, buff=0.12)
        stack.move_to(2.6 * RIGHT + 0.3 * UP)
        self.play(FadeIn(blob))
        self.play(LaggedStart(*[FadeIn(s, shift=0.1 * UP) for s in stack], lag_ratio=0.2), run_time=2)
        self.finish()
        self.clear_content()

        self.narrate("1.5")
        surf = Ellipse(width=6, height=3).set_fill(TORUS, 0.15).set_stroke(TORUS, 3).move_to(2.5 * LEFT + 0.4 * UP)
        cv = ParametricCurve(lambda t: surf.get_center() + np.array([2.2 * math.cos(t), 0.8 * math.sin(3 * t) * 0.6, 0]),
                             t_range=(0, TAU, TAU / 300)).set_stroke(YELLOW, 4)
        cls = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.2).set_stroke(YELLOW, 3).move_to(3.6 * RIGHT + 0.4 * UP)
        clt = txt("its shadow", 28, YELLOW).move_to(cls)
        arr = Arrow(surf.get_right() + 0.1 * RIGHT, cls.get_left(), buff=0.1, fill_color=YELLOW, thickness=4)
        nm = txt("an algebraic cycle", 26, YELLOW).next_to(surf, DOWN, buff=0.3)
        self.play(FadeIn(surf))
        self.play(ShowCreation(cv), FadeIn(nm), run_time=1.5)
        self.cue("and it has a class")
        self.play(GrowArrow(arr), FadeIn(cls), FadeIn(clt))
        self.finish()

        self.recap("1.6", ["Classes record holes.", "Shapes cut out by equations cast shadows."])


# ---------------------------------------------------------------------------
# Chapter 2 — the conjecture
# ---------------------------------------------------------------------------

class C2Conjecture(Video):
    def construct(self):
        self.chapter(1, "2. The conjecture")
        self.narrate("2.1")
        blob = Circle(radius=0.9).set_fill(GREY_C, 0.5).set_stroke(WHITE, 2).move_to(3.6 * LEFT + 0.4 * UP)
        bl = txt("a class", 26, WHITE).next_to(blob, DOWN, buff=0.2)
        pieces = VGroup(*[RoundedRectangle(width=1.6, height=0.8, corner_radius=0.15).set_fill(c, 0.7).set_stroke(c, 2)
                          for c in (BLUE_C, ORANGE, GREEN_C)]).arrange(RIGHT, buff=0.3).move_to(1.8 * RIGHT + 0.4 * UP)
        pl = VGroup(*[Tex(s, font_size=36).move_to(p) for s, p in zip(("(2,0)", "(1,1)", "(0,2)"), pieces)])
        self.play(FadeIn(blob), FadeIn(bl))
        self.play(TransformFromCopy(VGroup(blob), pieces), FadeIn(pl), run_time=1.5)
        self.finish()
        self.clear_content()

        self.narrate("2.2")
        dia = hodge_diamond(3)
        dia.move_to(0.5 * UP).scale(0.95)
        cells, rows = dia
        order = sorted(range(len(cells)), key=lambda i: sum(cells[i].pq))
        self.play(FadeIn(rows), LaggedStart(*[FadeIn(cells[i], scale=0.8) for i in order], lag_ratio=0.08), run_time=3)
        self.cue("Shadows of cycles")
        mids = [c for c in cells if c.pq[0] == c.pq[1]]
        self.play(*[Indicate(c, color=HODGE, scale_factor=1.15) for c in mids], run_time=1.5)
        self.finish()

        self.narrate("2.3")
        badge = card(["Hodge class:", "rational, and in the middle column"], width=4.0, size=22).to_edge(RIGHT, buff=0.2)
        badge.shift(0.6 * UP)
        self.play(FadeIn(badge))
        self.finish()
        self.play(FadeOut(badge))

        self.narrate("2.4")
        st = card(["Every Hodge class is a rational combination", "of shadows of algebraic cycles."],
                  title="The Hodge conjecture", width=9.5, size=30)
        veil = self.dim()
        self.play(veil.animate.set_fill(opacity=0.85), FadeIn(st.move_to(0.6 * UP)))
        self.cue("Hodge posed it")
        yr = txt("posed by W. V. D. Hodge, 1950", 26, GREY_A).next_to(st, DOWN, buff=0.35)
        self.play(FadeIn(yr))
        self.finish()
        self.play(FadeOut(VGroup(st, yr)), veil.animate.set_fill(opacity=0))
        self.remove(veil)

        self.narrate("2.5")
        low = [c for c in cells if c.pq == (1, 1)]
        lt = txt("degree 2: true (Lefschetz, 1924)", 24, GREEN_C).next_to(dia, RIGHT, buff=0.4).shift(1.2 * DOWN)
        self.play(*[c[0].animate.set_stroke(GREEN_C, 5) for c in low], FadeIn(lt))
        self.cue("Multiplying those")
        up = [c for c in cells if c.pq in ((2, 2), (3, 3))]
        arrs = VGroup(*[Arrow(low[0].get_top(), c.get_bottom(), buff=0.1, fill_color=GREEN_C, thickness=3) for c in up[:1]])
        self.play(GrowArrow(arrs[0]))
        self.finish()

        self.narrate("2.6")
        target = [c for c in cells if c.pq == (2, 2)][0]
        ring = Circle(radius=0.55).set_stroke(RED_C, 5).move_to(target)
        ex = txt("exotic: not built from degree 2", 24, RED_C).next_to(dia, RIGHT, buff=0.4).shift(0.6 * UP)
        self.play(ShowCreation(ring), FadeIn(ex))
        self.finish()

        self.recap("2.7", ["Every Hodge class should be a shadow.", "Exotic classes are the hard part."])


# ---------------------------------------------------------------------------
# Chapter 3 — CM
# ---------------------------------------------------------------------------

class C3CM(Video):
    def construct(self):
        self.chapter(2, "3. Complex multiplication")
        w1, w2 = 1 + 0j, 0.35 + 1.1j
        self.narrate("3.1")
        dots = lattice(w1, w2).move_to(3.0 * LEFT + 0.3 * UP)
        cellp = cell_poly(w1, w2).shift(dots.get_center() - lattice(w1, w2).get_center())
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), run_time=1.5)
        self.play(FadeIn(cellp))
        self.finish()

        self.narrate("3.2")
        rect = Rectangle(width=2.4, height=1.6).set_fill(LAT, 0.25).set_stroke(LAT, 3).move_to(2.6 * RIGHT + 0.4 * UP)
        tube = VGroup(Ellipse(width=0.5, height=1.6).move_to(rect.get_left() + 0.25 * RIGHT),
                      Line(rect.get_corner(UL) + 0.25 * RIGHT, rect.get_corner(UR) + 0.25 * LEFT),
                      Line(rect.get_corner(DL) + 0.25 * RIGHT, rect.get_corner(DR) + 0.25 * LEFT),
                      Ellipse(width=0.5, height=1.6).move_to(rect.get_right() + 0.25 * LEFT)).set_stroke(LAT, 3)
        dn = doughnut(3.2, 1.7, rect.get_center(), color=LAT)
        self.play(TransformFromCopy(cellp, rect))
        self.cue("Opposite edges")
        self.play(FadeTransform(rect, tube), run_time=1.2)
        self.play(FadeTransform(tube, dn), run_time=1.2)
        self.finish()
        self.clear_content()

        self.narrate("3.3")
        hd = VGroup(doughnut(3.4, 1.8, color=TORUS), doughnut(2.4, 1.2, color=TORUS).shift(0.15 * UP),
                    doughnut(1.4, 0.7, color=TORUS).shift(0.3 * UP)).move_to(2.8 * LEFT + 0.4 * UP)
        lab = VGroup(Tex(R"\mathbb{C}^g / \text{lattice}", font_size=44),
                     txt("an abelian variety", 30, YELLOW)).arrange(DOWN, buff=0.3).move_to(2.6 * RIGHT + 0.4 * UP)
        self.play(FadeIn(hd), Write(lab[0]))
        self.play(FadeIn(lab[1]))
        self.finish()
        self.clear_content()

        self.narrate("3.4")
        sq = lattice(1 + 0j, 1j).move_to(0.4 * UP)
        rot = sq.copy().set_fill(opacity=0)
        for d in rot:
            d.set_stroke(ORANGE, 3)
        sql = txt("square lattice", 28, LAT).next_to(sq, UP, buff=0.2)
        self.play(FadeIn(sq), FadeIn(sql))
        self.add(rot)
        self.play(Rotate(rot, PI / 2, about_point=sq.get_center()), run_time=2)
        ok = VGroup(tick(), txt("a quarter turn lands on itself", 26, GREEN_C)).arrange(RIGHT, buff=0.3)
        ok.next_to(sq, DOWN, buff=0.3)
        self.play(FadeIn(ok))
        self.finish()
        self.clear_content()

        self.narrate("3.5")
        g = lattice(1 + 0j, 0.31 + 1.13j, box=1.6).move_to(3.4 * LEFT + 0.4 * UP)
        gr = g.copy().set_fill(opacity=0)
        for d in gr:
            d.set_stroke(ORANGE, 3)
        h = lattice(1 + 0j, complex(0.5, math.sqrt(3) / 2), box=1.6).move_to(3.4 * RIGHT + 0.4 * UP)
        hr = h.copy().set_fill(opacity=0)
        for d in hr:
            d.set_stroke(ORANGE, 3)
        self.play(FadeIn(g), FadeIn(h))
        self.add(gr, hr)
        self.play(Rotate(gr, PI / 2, about_point=g.get_center()), Rotate(hr, PI / 3, about_point=h.get_center()),
                  run_time=2)
        m1 = VGroup(cross(), txt("generic: misses", 24, RED_C)).arrange(RIGHT, buff=0.25).next_to(g, DOWN, buff=0.3)
        m2 = VGroup(tick(), txt("hexagonal: lands", 24, GREEN_C)).arrange(RIGHT, buff=0.25).next_to(h, DOWN, buff=0.3)
        self.play(FadeIn(m1), FadeIn(m2))
        self.cue("it is said to have")
        cm = txt("complex multiplication: CM", 32, YELLOW).move_to(2.7 * UP)
        self.play(FadeIn(cm, scale=1.2))
        self.finish()
        self.clear_content()

        self.narrate("3.6")
        rng = np.random.default_rng(5)
        cloud = VGroup(*[Dot(np.array([x, y, 0]), radius=0.035, fill_color=GREY_C)
                         for x, y in rng.uniform([-5.5, -1.6], [5.5, 2.4], size=(500, 2))])
        cms = VGroup(*[Dot(np.array([x, y, 0]), radius=0.07, fill_color=CMC)
                       for x, y in rng.uniform([-5.5, -1.6], [5.5, 2.4], size=(45, 2))])
        self.play(FadeIn(cloud), run_time=1.2)
        self.cue("yet spread")
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in cms], lag_ratio=0.05), run_time=2)
        lab = txt("orange: CM varieties", 26, CMC).to_edge(DOWN, buff=1.6)
        self.play(FadeIn(lab))
        self.finish()
        self.clear_content()

        self.narrate("3.7")
        ex = card(["Weil classes: exotic Hodge classes", "not built from divisors (dimension 4 and up)"], width=9, size=28)
        self.play(FadeIn(ex.move_to(0.6 * UP)))
        self.finish()

        self.recap("3.8", ["CM abelian varieties: doughnuts with extra symmetry,", "and exotic Hodge classes."])


# ---------------------------------------------------------------------------
# Chapter 4 — the claim
# ---------------------------------------------------------------------------

class C4Claim(Video):
    def construct(self):
        self.chapter(2, "4. The claim")
        self.narrate("4.1")
        cards = VGroup(card(["1982: Deligne", "Hodge classes on abelian varieties are 'absolute'"], width=9, size=26),
                       card(["2025: Markman", "the conjecture for all abelian fourfolds"], width=9, size=26))
        cards.arrange(DOWN, buff=0.35).move_to(0.6 * UP)
        self.play(FadeIn(cards[0]))
        self.cue("In 2025")
        self.play(FadeIn(cards[1]))
        self.finish()
        self.play(FadeOut(cards))

        self.narrate("4.2")
        thm = card(["On every abelian variety with complex multiplication,", "of any dimension, every Hodge class is",
                    "a rational combination of shadows of algebraic cycles."],
                   title="The claim (Theorem 1.1)", width=10.5, size=30).move_to(0.7 * UP)
        self.play(FadeIn(thm))
        self.finish()

        self.narrate("4.3")
        inc = VGroup(tick(), txt("exotic classes included", 30, GREEN_C)).arrange(RIGHT, buff=0.3).next_to(thm, DOWN,
                                                                                                         buff=0.4)
        self.play(FadeIn(inc))
        self.finish()

        self.recap("4.4", ["Claimed: the Hodge conjecture", "for every CM abelian variety."])


# ---------------------------------------------------------------------------
# Chapter 5 — how it works
# ---------------------------------------------------------------------------

class C5How(Video):
    def construct(self):
        self.chapter(3, "5. How it works")
        pats, quads = balanced_quads(3)
        ex = next(q for q in quads if q[0] != q[2] and q[0] != q[3] and q[0] != q[1])
        rows = sign_rows(ex).move_to(2.6 * LEFT + 0.4 * UP)
        self.narrate("5.1")
        self.play(LaggedStart(*[FadeIn(r, shift=0.1 * RIGHT) for r in rows], lag_ratio=0.3), run_time=2)
        self.finish()

        self.narrate("5.2")
        s = [ex[0][i] + ex[1][i] for i in range(3)]
        top = txt("v1 + v2 = (" + ", ".join(f"{x:+d}" for x in s) + ")", 26, GREEN_C).next_to(rows[1], RIGHT, buff=0.8)
        bot = txt("v3 + v4 = (" + ", ".join(f"{x:+d}" for x in s) + ")", 26, GREEN_C).next_to(rows[3], RIGHT, buff=0.8)
        self.play(FadeIn(top))
        self.play(FadeIn(bot))
        bal = txt("balanced", 32, YELLOW).next_to(VGroup(top, bot), RIGHT, buff=0.4)
        self.play(FadeIn(bal, scale=1.2))
        self.finish()

        self.narrate("5.3")
        cnt = txt(f"3 pairs of directions: {len(pats)} types, {len(quads)} balanced quadruples", 26, GREY_A)
        cnt.to_edge(DOWN, buff=1.7)
        self.play(FadeIn(cnt))
        self.finish()
        self.clear_content()

        self.narrate("5.4")
        S = Ellipse(width=2.6, height=1.6).set_fill(TORUS, 0.25).set_stroke(TORUS, 3).move_to(3.6 * LEFT + 0.4 * UP)
        Sl = txt("a surface S", 26, TORUS).next_to(S, DOWN, buff=0.2)
        boxes = VGroup(*[card([f"piece {i}"], width=2.0, size=24) for i in range(1, 5)]).arrange(DOWN, buff=0.2)
        boxes.move_to(0.6 * RIGHT + 0.4 * UP)
        arrs = VGroup(*[Arrow(S.get_right(), b.get_left(), buff=0.1, fill_color=GREY_B, thickness=3) for b in boxes])
        integ = Tex(R"\int_S \omega_1 \wedge \omega_2 \wedge \bar\omega_3 \wedge \bar\omega_4 \neq 0",
                    font_size=40).move_to(4.4 * RIGHT + 0.9 * UP)
        res = txt("so the image of S is a\ncycle hitting the block", 24, YELLOW).next_to(integ, DOWN, buff=0.4)
        self.play(FadeIn(S), FadeIn(Sl))
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(b)) for a, b in zip(arrs, boxes)], lag_ratio=0.2))
        self.cue("and a certain integral")
        self.play(Write(integ))
        self.cue("then the image")
        self.play(FadeIn(res))
        self.finish()
        self.clear_content()

        self.narrate("5.5")
        ball = Circle(radius=1.6).set_stroke(BLUE_C, 3).set_fill(BLUE_E, 0.3).move_to(3.4 * LEFT + 0.4 * UP)
        arcs = VGroup(*[ArcBetweenPoints(ball.get_center() + 1.6 * np.array([math.cos(a), math.sin(a), 0]),
                                         ball.get_center() + 1.6 * np.array([math.cos(a + 1.4), math.sin(a + 1.4), 0]),
                                         angle=-1.2).set_stroke(BLUE_B, 2) for a in np.linspace(0, TAU, 8, endpoint=False)])
        bl = txt("the complex ball", 26, BLUE_B).next_to(ball, DOWN, buff=0.2)
        surf = doughnut(3.0, 1.6, 2.6 * RIGHT + 0.4 * UP, color=TORUS)
        waves = VGroup(*[ParametricCurve(lambda t, k=k: surf.get_center() + np.array([t, 0.18 * math.sin(4 * t + k) +
                                                                                      0.25 * (k - 1), 0]),
                                         t_range=(-1.2, 1.2, 0.02)).set_stroke(YELLOW, 2) for k in range(3)])
        tl = txt("theta functions on a compact quotient", 26, YELLOW).next_to(surf, DOWN, buff=0.3)
        self.play(FadeIn(ball), ShowCreation(arcs), FadeIn(bl))
        self.play(TransformFromCopy(ball, surf[0]), FadeIn(surf[1:]), run_time=1.5)
        self.play(ShowCreation(waves), FadeIn(tl))
        self.finish()
        self.clear_content()

        self.narrate("5.6")
        boxes = VGroup(*[card([f"piece {i}"], width=2.2, size=24) for i in range(1, 5)]).arrange(RIGHT, buff=0.3)
        boxes.move_to(0.6 * UP)
        labs = VGroup(txt("Hecke operators", 26, BLUE_B), txt("Frobenius modulo primes", 26, BLUE_B))
        labs.arrange(RIGHT, buff=1.2).next_to(boxes, UP, buff=0.4)
        ticks_ = VGroup(*[tick(s=1.1).next_to(b, DOWN, buff=0.3) for b in boxes])
        self.play(FadeIn(boxes), FadeIn(labs))
        self.cue("it shows the theta forms")
        self.play(LaggedStart(*[ShowCreation(t) for t in ticks_], lag_ratio=0.25))
        self.finish()
        self.clear_content()

        self.narrate("5.7")
        parts = VGroup(*[doughnut(1.6, 0.85, color=TORUS) for _ in range(3)]).arrange(RIGHT, buff=0.4).move_to(1.0 * UP)
        one = doughnut(3.6, 1.9, 1.0 * UP, color=TORUS)
        coef = VGroup(txt("complex coefficients", 26, GREY_A), Arrow(LEFT, RIGHT, fill_color=GREY_B, thickness=3),
                      txt("rational coefficients", 26, YELLOW)).arrange(RIGHT, buff=0.3).move_to(1.2 * DOWN)
        self.play(FadeIn(parts))
        self.play(FadeTransform(parts, one), run_time=1.5)
        self.play(FadeIn(coef))
        self.finish()

        self.recap("5.8", ["Balanced blocks; a surface with a nonzero integral;", "theta functions; arithmetic."])


# ---------------------------------------------------------------------------
# Chapter 6 — what follows
# ---------------------------------------------------------------------------

class C6Follow(Video):
    def construct(self):
        self.chapter(3, "6. What follows")
        src = card(["Hodge for CM abelian varieties"], width=5.2, size=28).move_to(4.0 * LEFT + 0.05 * UP)
        outs = VGroup(card(["the Tate conjecture for abelian varieties", "over finite fields (Milne)"], width=6.4, size=24),
                      card(["the Hodge standard conjecture for abelian", "varieties, every characteristic (Milne)"],
                           width=6.4, size=24),
                      card(["companion papers: powers of certain sixfolds,", "Jacobians of abelian covers"], width=6.4,
                           size=24)).arrange(DOWN, buff=0.2).move_to(2.6 * RIGHT + 0.05 * UP)
        arrs = VGroup(*[Arrow(src.get_right(), o.get_left(), buff=0.1, fill_color=GREY_B, thickness=3) for o in outs])
        for k, beat in enumerate(["6.1", "6.2", "6.3"]):
            self.narrate(beat)
            anims = [GrowArrow(arrs[k]), FadeIn(outs[k])]
            if k == 0:
                anims.insert(0, FadeIn(src))
            self.play(*anims)
            self.finish()
        self.recap("6.4", ["One family settled, and the Tate conjecture", "for abelian varieties over finite fields."])


# ---------------------------------------------------------------------------
# Chapter 7 — is it right?
# ---------------------------------------------------------------------------

class C7Check(Video):
    def construct(self):
        self.chapter(4, "7. Is it right?")
        self.narrate("7.1")
        lean = card(["Lean 4, added 26 October 2026:", "every rational Hodge class on a CM abelian variety",
                     "is algebraic"], width=10, size=28).move_to(1.2 * UP)
        notes = txt("not re-run by us · the Tate consequences are outside it", 24, GREY_A).next_to(lean, DOWN, buff=0.35)
        self.play(FadeIn(lean))
        self.cue("We have not re-run")
        self.play(FadeIn(notes))
        self.finish()
        self.play(FadeOut(VGroup(lean, notes)))

        self.narrate("7.2")
        papers = VGroup(*[card([t], width=3.6, size=22) for t in ("Weil classes on split\nabelian eightfolds",
                                                                  "Kuga–Satake\ncorrespondences for K3",
                                                                  "Hodge for products\nof K3 surfaces")])
        papers.arrange(RIGHT, buff=0.3).move_to(0.9 * UP)
        xs = VGroup(*[cross(s=0.9).move_to(p.get_corner(UR) + 0.05 * DL) for p in papers])
        wl = txt("withdrawn 6 and 7 October: a sign error", 26, RED_C).next_to(papers, DOWN, buff=0.4)
        self.play(FadeIn(papers))
        self.play(ShowCreation(xs), FadeIn(wl))
        self.finish()

        self.narrate("7.3")
        chk = VGroup(tick(), txt("this paper cites none of them", 28, GREEN_C)).arrange(RIGHT, buff=0.3)
        chk.next_to(wl, DOWN, buff=0.4)
        self.play(FadeIn(chk))
        self.finish()
        self.clear_content()

        self.narrate("7.4")
        st = txt("no public expert assessment found, as of 4 November 2026", 30, ORANGE).move_to(0.8 * UP)
        self.play(FadeIn(st))
        self.finish()

        self.recap("7.5", ["A computer-checked main theorem;", "the written proof not yet assessed."])


# ---------------------------------------------------------------------------
# Chapter 8 — what it does not do
# ---------------------------------------------------------------------------

class C8Close(Video):
    def construct(self):
        self.chapter(4, "8. What it does not do")
        self.narrate("8.1")
        land = RoundedRectangle(width=11, height=4.6, corner_radius=0.4).set_stroke(GREY_B, 2).set_fill(GREY_E, 0.4)
        land.move_to(0.4 * UP)
        ll = txt("all smooth projective varieties", 26, GREY_A).next_to(land, UP, buff=0.1).align_to(land, LEFT)
        cmr = Ellipse(width=2.4, height=1.2).set_fill(CMC, 0.5).set_stroke(CMC, 3).move_to(land.get_center() + 3.6 * LEFT
                                                                                           + 0.9 * DOWN)
        cml = txt("CM abelian varieties", 22, WHITE).move_to(cmr)
        self.play(FadeIn(land), FadeIn(ll))
        self.play(FadeIn(cmr), FadeIn(cml))
        self.finish()

        self.narrate("8.2")
        others = VGroup()
        for text, pos, w in [("general abelian varieties", 2.0 * LEFT + 0.7 * UP, 3.6),
                             ("K3 surfaces", 2.6 * RIGHT + 1.1 * UP, 2.6),
                             ("most varieties", 2.4 * RIGHT + 0.9 * DOWN, 3.0)]:
            e = Ellipse(width=w, height=1.0).set_stroke(GREY_B, 2).move_to(land.get_center() + pos)
            others.add(VGroup(e, txt(text, 22, GREY_A).move_to(e), txt("?", 40, YELLOW).next_to(e, RIGHT, buff=0.1)))
        self.play(LaggedStart(*[FadeIn(o) for o in others], lag_ratio=0.3), run_time=2)
        self.finish()
        self.clear_content()

        self.narrate("8.3")
        self.play(FadeOut(self.roadmap_mob))
        title = txt("The Hodge conjecture for CM abelian varieties", 44)
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
        title = txt("The Hodge conjecture for CM abelian varieties", 50).to_edge(UP, buff=0.6)
        sub = txt("holes, shadows and symmetry, explained for everyone", 30, GREY_A).next_to(title, DOWN, buff=0.25)
        d = doughnut(4.6, 2.4, 3.4 * LEFT + 1.0 * DOWN)
        dia = hodge_diamond(3).scale(0.75).move_to(3.4 * RIGHT + 1.0 * DOWN)
        self.add(title, sub, d, loop_a(d), loop_b(d), dia)
