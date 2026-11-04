"""Narrated explainer for "Exact Birch–Swinnerton-Dyer Formula from Low Selmer Corank"
(OpenAI, October 2026), written for 3b1b's manim (manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("2.4") and
the words come from beat 2.4 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl bsd_video.py C2Experiment -w -l --config_file ../../../../../tools/video/custom_config.yml

Computed from data: the curves and their rational points (exact fractions),
solutions modulo small primes, Birch and Swinnerton-Dyer's products over all
primes up to 100,000 for curves of rank 0 to 3, and sums of two cubes. The
L-function sketches, the "error gauge" and the stages of the proof are
schematics.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "video"))
from narrated import *  # noqa: E402,F403

CURVE = BLUE_C
POINT = ORANGE
SUM = GREEN_C
SHA = ORANGE
NEWC = YELLOW

# Curves y^2 + a3 y = x^3 + a2 x^2 + a4 x + a6 (Cremona labels), conductors and ranks.
CURVES = [("11a1", (-1, 1, -10, -20), 11, 0), ("37a1", (0, 1, -1, 0), 37, 1),
          ("389a1", (1, 1, -2, 0), 389, 2), ("5077a1", (0, 1, -7, 6), 5077, 3)]
CUBES = [(7, (-1, 2, 1)), (13, (2, 7, 3)), (17, (-1, 18, 7)), (31, (-65, 137, 42)), (43, (1, 7, 2)),
         (53, (-1819, 1872, 217)), (61, (-4, 5, 1)), (67, (1208, 5353, 1323)), (71, (-126, 197, 43)),
         (79, (-4, 13, 3)), (89, (36, 53, 13)), (97, (-5, 14, 3)), (103, (-349, 592, 117)), (107, (17, 90, 19))]


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["Points", "The conjecture", "The claim", "How it works", "Is it right?"]
    PRONOUNCE = [(r"\bShafarevich\b", "Shafa-ray-vich"), (r"\bKolyvagin\b", "Kolly-vah-gin"),
                 (r"\bZagier\b", "Zah-gyay"), (r"\bBurungale\b", "Boo-roon-gah-lay"),
                 (r"\b1922\b", "nineteen twenty-two"), (r"\b2026\b", "twenty twenty-six")]
    BUILD = HERE / "build"


# ---------------------------------------------------------------------------
# arithmetic
# ---------------------------------------------------------------------------

def primes_upto(n: int) -> np.ndarray:
    s = np.ones(n + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def add37(P, Q):
    """Chord-and-tangent addition on y^2 + y = x^3 - x with exact fractions; None is the point at infinity."""
    if P is None:
        return Q
    if Q is None:
        return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and y1 + y2 + 1 == 0:
        return None
    lam = (3 * x1 * x1 - 1) / (2 * y1 + 1) if x1 == x2 else (y2 - y1) / (x2 - x1)
    x3 = lam * lam - x1 - x2
    return (x3, -(lam * (x3 - x1) + y1) - 1)


def multiples(n=12):
    G, cur, out = (Fraction(0), Fraction(0)), None, []
    for _ in range(n):
        cur = add37(cur, G)
        out.append(cur)
    return out


def solutions_mod(p, coeffs=(0, 1, -1, 0)):
    a2, a3, a4, a6 = coeffs
    return [(x, y) for x in range(p) for y in range(p)
            if (y * y + a3 * y - (x ** 3 + a2 * x * x + a4 * x + a6)) % p == 0]


def bsd_products(coeffs, N, X=100_000):
    cache = HERE / "build" / f"bsd_{N}.npy"
    if cache.exists():
        return np.load(cache)
    a2, a3, a4, a6 = coeffs
    out, acc = [], 0.0
    for p in primes_upto(X):
        p = int(p)
        if p == 2 or N % p == 0:
            continue
        x = np.arange(p, dtype=np.int64)
        v = (4 * ((x * x % p) * x % p + a2 * (x * x % p) + a4 * x + a6) + a3 * a3) % p
        sq = np.zeros(p, dtype=bool)
        sq[(x * x) % p] = True
        acc += math.log((int(np.where(v == 0, 1, np.where(sq[v], 2, 0)).sum()) + 1) / p)
        out.append((math.log(math.log(p)), acc))
    arr = np.array(out)
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.save(cache, arr)
    return arr


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def tick(color=GREEN_C, s=1.0):
    return VMobject().set_points_as_corners([[-0.22 * s, 0, 0], [-0.06 * s, -0.18 * s, 0], [0.24 * s, 0.22 * s, 0]]
                                            ).set_stroke(color, 6)


def cross(color=RED_C, s=1.0):
    a = 0.18 * s
    return VGroup(Line([-a, -a, 0], [a, a, 0]), Line([-a, a, 0], [a, -a, 0])).set_stroke(color, 6)


def curve_branches(ax, coeffs, x0, x1, color=CURVE, width=4, n=1500):
    """The real points of y^2 + a3 y = x^3 + a2 x^2 + a4 x + a6, as upper and lower branches in chart coordinates."""
    a2, a3, a4, a6 = coeffs
    xs = np.linspace(x0, x1, n)
    disc = a3 * a3 + 4 * (xs ** 3 + a2 * xs * xs + a4 * xs + a6)
    pieces, cur = [], []
    for x, d in zip(xs, disc):
        if d >= 0:
            cur.append((x, d))
        elif cur:
            pieces.append(cur)
            cur = []
    if cur:
        pieces.append(cur)
    g = VGroup()
    for piece in pieces:
        top = [ax.c2p(x, (-a3 + math.sqrt(d)) / 2) for x, d in piece]
        bot = [ax.c2p(x, (-a3 - math.sqrt(d)) / 2) for x, d in piece]
        pts = bot[::-1] + top
        if piece[-1][0] < x1 - 1e-9:      # a closed oval
            pts = pts + [pts[0]]
        g.add(VMobject().set_points_as_corners(pts).set_stroke(color, width))
    return g


def plane(xr=(-1.6, 2.7), yr=(-3.3, 2.3), w=5.2, h=6.0):
    ax = Chart(xr, yr, w, h, grid=False)
    return ax


def frac_str(f):
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def paper_card(pages, label, width=2.6):
    return card([label, f"{pages} pages"], width=width, size=24)


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        eq = Tex(R"y^2 + y = x^3 - x", font_size=56).to_edge(UP, buff=0.8)
        ax = plane(w=4.0, h=4.4)
        ax.shift(0.1 * UP - ax.box.get_center())
        cv = curve_branches(ax, (0, 1, -1, 0), -1.6, 2.1)
        self.narrate("0.1")
        self.play(Write(eq))
        self.play(ShowCreation(cv), run_time=2.5)
        self.finish()

        self.narrate("0.2")
        pts = [p for p in multiples(9) if p is not None and abs(float(p[0])) < 2.6 and -3.2 < float(p[1]) < 2.2]
        dots = VGroup(*[Dot(ax.c2p(float(x), float(y)), radius=0.08, fill_color=POINT) for x, y in pts])
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.35), run_time=3)
        self.cue("Is there a way")
        q = txt("how many?", 34, YELLOW).next_to(ax.box, RIGHT, buff=0.6)
        self.play(FadeIn(q))
        self.finish()

        self.narrate("0.3")
        title = txt("The Birch–Swinnerton-Dyer formula", 52)
        sub = txt("OpenAI preprint, October 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(VGroup(eq, ax, cv, dots, q)), Write(title, run_time=2))
        self.play(FadeIn(sub))
        self.finish()
        self.clear_caption()

        self.narrate("0.4")
        big = self.roadmap(None, big=True).move_to(1.5 * DOWN)
        self.play(title.animate.shift(UP), sub.animate.shift(UP), FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — points
# ---------------------------------------------------------------------------

class C1Points(Video):
    def construct(self):
        self.chapter(0, "1. Points on a curve")
        ax = plane(w=4.0, h=4.6)
        ax.shift(3.3 * LEFT + 0.05 * UP - ax.box.get_center())
        cv = curve_branches(ax, (0, 1, -1, 0), -1.6, 2.1)
        eq = Tex(R"y^2 + y = x^3 - x", font_size=40).next_to(ax.box, UP, buff=0.05)
        P, Q, T, R = (-1, 0), (0, 0), (1, 0), (1, -1)
        dP, dQ = (Dot(ax.c2p(*P), radius=0.1, fill_color=POINT), Dot(ax.c2p(*Q), radius=0.1, fill_color=POINT))
        lP = txt("P", 30, POINT).next_to(dP, UL, buff=0.05)
        lQ = txt("Q", 30, POINT).next_to(dQ, UR, buff=0.05)

        self.narrate("1.1")
        self.play(ShowCreation(cv), FadeIn(eq), run_time=2)
        self.play(FadeIn(VGroup(dP, dQ, lP, lQ)))
        self.finish()

        self.narrate("1.2")
        line = Line(ax.c2p(-1.6, 0), ax.c2p(2.7, 0)).set_stroke(POINT, 3)
        dT = Dot(ax.c2p(*T), radius=0.1, fill_color=GREY_B)
        self.play(ShowCreation(line), run_time=1.5)
        self.cue("It meets the curve")
        self.play(FadeIn(dT, scale=2))
        self.finish()

        self.narrate("1.3")
        refl = DashedLine(ax.c2p(*T), ax.c2p(*R)).set_stroke(GREY_B, 2)
        dR = Dot(ax.c2p(*R), radius=0.11, fill_color=SUM)
        lR = txt("P + Q", 30, SUM).next_to(dR, RIGHT, buff=0.15)
        self.play(ShowCreation(refl))
        self.play(TransformFromCopy(dT, dR), FadeIn(lR))
        self.finish()

        self.narrate("1.4")
        self.play(FadeOut(VGroup(line, dT, refl, dR, lR, dP, lP, lQ)))
        rows = VGroup()
        for n, pt in enumerate(multiples(12), start=1):
            rows.add(VGroup(txt(f"{n} × (0, 0):", 24, CURVE), txt("x = " + frac_str(pt[0]), 24, WHITE))
                     .arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(3.0 * RIGHT + 0.1 * DOWN)
        xcol = max(r[0].get_right()[0] for r in rows) + 0.3
        for row in rows:
            row[1].move_to(np.array([xcol, row[1].get_y(), 0]), aligned_edge=LEFT)
        self.cue("Adding a point")
        self.play(LaggedStart(*[FadeIn(r, shift=0.1 * RIGHT) for r in rows], lag_ratio=0.25), run_time=5)
        self.finish()

        self.narrate("1.5")
        rank = txt("rank 1: every point is a multiple of one", 28, YELLOW).next_to(rows, UP, buff=0.3)
        self.play(FadeIn(rank))
        self.finish()
        self.clear_content()

        self.narrate("1.6")
        small = VGroup()
        for name, coeffs, xr, x1, yr, label in [
                ("11a1", (-1, 1, -10, -20), (4, 10), 8.9, (-25, 24), "rank 0: finitely many points"),
                ("37a1", (0, 1, -1, 0), (-1.6, 3), 2.45, (-4, 3), "rank 1"),
                ("389a1", (1, 1, -2, 0), (-2.6, 3), 2.55, (-5, 4), "rank 2")]:
            a = Chart(xr, yr, 3.4, 3.4, grid=False)
            c = curve_branches(a, coeffs, xr[0], x1, width=3)
            small.add(VGroup(a, c, txt(label, 24, GREY_A).next_to(a.box, DOWN, buff=0.2)))
        small.arrange(RIGHT, buff=0.7).move_to(0.4 * UP)
        self.play(LaggedStart(*[FadeIn(s) for s in small], lag_ratio=0.4), run_time=2.5)
        self.cue("But nobody knows")
        nb = txt("no known procedure always computes the rank", 28, YELLOW).next_to(small, DOWN, buff=0.4)
        self.play(FadeIn(nb))
        self.finish()

        self.recap("1.7", ["Rational points can be added.", "The rank counts the independent ones."])


# ---------------------------------------------------------------------------
# Chapter 2 — the experiment
# ---------------------------------------------------------------------------

def mod_grid(p, size=2.4):
    step = size / p
    g = VGroup()
    sols = set(solutions_mod(p))
    for x in range(p):
        for y in range(p):
            on = (x, y) in sols
            g.add(Dot(np.array([x * step, y * step, 0]), radius=0.06 if on else 0.025,
                      fill_color=POINT if on else GREY_D))
    frame = Square(size + step).set_stroke(GREY_D, 1).move_to(g)
    return VGroup(frame, g), len(sols) + 1


class C2Experiment(Video):
    def construct(self):
        self.chapter(1, "2. The experiment")
        self.narrate("2.1")
        g7, n7 = mod_grid(7, 3.6)
        g7.move_to(2.6 * LEFT + 0.3 * UP)
        lab = txt("solutions modulo 7", 28, GREY_A).next_to(g7, UP, buff=0.25)
        self.play(FadeIn(g7[0]), LaggedStart(*[FadeIn(d) for d in g7[1]], lag_ratio=0.01), FadeIn(lab), run_time=2)
        cnt = txt(f"{n7 - 1} solutions + 1 point at infinity = {n7}", 26, POINT).next_to(g7, RIGHT, buff=0.6)
        self.play(FadeIn(cnt))
        self.finish()
        self.clear_content()

        self.narrate("2.2")
        grids = VGroup()
        for p in (5, 7, 11, 13):
            g, n = mod_grid(p, 2.2)
            grids.add(VGroup(g, txt(f"p = {p}: count {n}", 24, GREY_A).next_to(g, DOWN, buff=0.2)))
        grids.arrange(RIGHT, buff=0.5).move_to(0.4 * UP)
        self.play(LaggedStart(*[FadeIn(g) for g in grids], lag_ratio=0.3), run_time=2.5)
        self.finish()
        self.clear_content()

        data = [(name, rank, bsd_products(coeffs, N)) for name, coeffs, N, rank in CURVES]
        ax = Chart((0.0, 2.5), (0, 8.5), 8.2, 4.2,
                   yticks=(0, math.log(10), math.log(100), math.log(1000)),
                   yfmt=lambda v: txt(f"{math.exp(v):,.0f}", 20, GREY_B),
                   xlabel="primes counted (log log scale)", ylabel="product of count / p", grid=False)
        ax.shift(0.5 * UP - ax.box.get_center())
        cols = [GREY_B, BLUE_C, GREEN_C, ORANGE]

        def plot(arr, c):
            pts = arr[:: max(1, len(arr) // 600)]
            return VMobject().set_points_as_corners([ax.c2p(x, y) for x, y in pts]).set_stroke(c, 3)

        lines = [plot(arr, c) for (_, _, arr), c in zip(data, cols)]
        labels = [txt(f"rank {rank}", 24, c).next_to(ax.c2p(*arr[-1]), RIGHT, buff=0.1)
                  for (_, rank, arr), c in zip(data, cols)]

        self.narrate("2.3")
        self.play(FadeIn(ax))
        self.play(ShowCreation(lines[0]), FadeIn(labels[0]), run_time=3)
        self.finish()

        self.narrate("2.4")
        for k, phrase in zip((1, 2, 3), ("For rank one", "For rank two", "The rank was showing")):
            self.cue(phrase)
            self.play(ShowCreation(lines[k]), FadeIn(labels[k]), run_time=2)
        self.finish()

        self.narrate("2.5")
        note = txt("computed for all primes up to 100,000", 24, GREY_A).next_to(ax.box, UP, buff=0.15)
        self.play(FadeIn(note))
        self.finish()
        self.clear_content()

        self.narrate("2.6")
        panels = VGroup()
        for r, c in zip((0, 1, 2), (GREY_B, BLUE_C, GREEN_C)):
            a = Chart((0.4, 1.6), (-0.6, 0.8), 3.4, 2.6, grid=False, xlabel="s")
            a.add(DashedLine(a.c2p(0.4, 0), a.c2p(1.6, 0)).set_stroke(GREY_D, 1.5),
                  DashedLine(a.c2p(1, -0.6), a.c2p(1, 0.8)).set_stroke(GREY_D, 1.5))
            shapes = {0: lambda s: 0.35 + 0.2 * (s - 1), 1: lambda s: 0.5 * (s - 1), 2: lambda s: 0.9 * (s - 1) ** 2}
            f = curve(a, shapes[r], 0.4, 1.6, color=c, width=4, ylim=(-0.6, 0.8))
            panels.add(VGroup(a, f, txt(f"rank {r}", 24, c).next_to(a.box, DOWN, buff=0.25)))
        panels.arrange(RIGHT, buff=0.6).move_to(0.4 * UP)
        name = txt("the L-function near s = 1", 28, YELLOW).next_to(panels, UP, buff=0.3)
        self.play(FadeIn(name), LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.4), run_time=3)
        self.finish()
        self.clear_content()

        self.narrate("2.7")
        st = card(["the rank of the curve equals the number of times", "its L-function vanishes at s = 1"],
                  title="The Birch and Swinnerton-Dyer conjecture", width=10.5, size=30).move_to(0.6 * UP)
        self.play(FadeIn(st))
        self.cue("That number is called")
        an = txt("that number: the analytic rank", 28, YELLOW).next_to(st, DOWN, buff=0.4)
        self.play(FadeIn(an))
        self.finish()

        self.recap("2.8", ["Count solutions modulo primes;", "the L-function at 1 should reveal the rank."])


# ---------------------------------------------------------------------------
# Chapter 3 — the formula
# ---------------------------------------------------------------------------

def formula():
    lhs = Tex(R"\frac{L^{(r)}(E,1)}{r!}", font_size=60)
    eq = Tex("=", font_size=60)
    num = VGroup(Tex(R"\Omega_E", font_size=56), Tex(R"\mathrm{Reg}_E", font_size=56),
                 Tex(R"|\text{Sha}|", font_size=56), Tex(R"\prod_\ell c_\ell", font_size=56)).arrange(RIGHT, buff=0.3)
    den = Tex(R"|E(\mathbb{Q})_{\mathrm{tors}}|^2", font_size=56)
    bar = Line(LEFT, RIGHT).set_width(num.get_width() + 0.3)
    rhs = VGroup(num, bar, den).arrange(DOWN, buff=0.18)
    f = VGroup(lhs, eq, rhs).arrange(RIGHT, buff=0.4)
    f.lhs, f.num, f.den = lhs, num, den
    return f


class C3Formula(Video):
    def construct(self):
        self.chapter(1, "3. The exact formula")
        f = formula().move_to(1.4 * UP)
        self.narrate("3.1")
        self.play(Write(f), run_time=3)
        self.finish()

        def label(mob, text, color, direction=DOWN):
            return txt(text, 24, color).next_to(mob, direction, buff=0.35)

        self.narrate("3.2")
        l1 = label(f.lhs, "first nonzero coefficient", BLUE_C)
        self.play(f.lhs.animate.set_color(BLUE_C), FadeIn(l1))
        self.finish()

        self.narrate("3.3")
        l2 = VGroup(txt("size of the curve", 22, GREEN_C), txt("spread of the points", 22, GREEN_C))
        l2[0].next_to(f.den, DOWN, buff=0.5).align_to(f.num[0], LEFT).shift(0.8 * LEFT)
        l2[1].next_to(l2[0], DOWN, buff=0.15).align_to(l2[0], LEFT)
        self.play(f.num[0].animate.set_color(GREEN_C), f.num[1].animate.set_color(GREEN_C), FadeIn(l2))
        self.finish()

        self.narrate("3.4")
        l3 = VGroup(txt("local factors at bad primes", 22, TEAL_C), txt("points of finite order", 22, PURPLE_B))
        l3.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(l2, RIGHT, buff=0.8).align_to(l2, UP)
        self.play(f.num[3].animate.set_color(TEAL_C), f.den.animate.set_color(PURPLE_B), FadeIn(l3))
        self.finish()

        self.narrate("3.5")
        l4 = txt("Sha: the Tate–Shafarevich group", 28, SHA).move_to(1.6 * DOWN)
        self.play(f.num[2].animate.set_color(SHA), FadeIn(l4))
        self.play(Indicate(f.num[2], color=SHA))
        self.finish()

        self.narrate("3.6")
        l5 = txt("conjectured finite; for most curves, not even that is known", 26, GREY_A).next_to(l4, DOWN, buff=0.25)
        self.play(FadeIn(l5))
        self.finish()

        self.recap("3.7", ["The formula: one L-value equals", "a product of the curve's measurements."])


# ---------------------------------------------------------------------------
# Chapter 4 — what was known
# ---------------------------------------------------------------------------

class C4Known(Video):
    def construct(self):
        self.chapter(1, "4. What was known")
        self.narrate("4.1")
        gz = card(["1986: Gross and Zagier", "Heegner points, sized by the L-function's slope"], width=9, size=28)
        gz.move_to(1.4 * UP)
        self.play(FadeIn(gz))
        self.finish()

        self.narrate("4.2")
        kol = card(["1989: Kolyvagin", "analytic rank 0 or 1: rank matches, Sha finite"], width=9, size=28)
        kol.next_to(gz, DOWN, buff=0.35)
        mod = card(["2001: every elliptic curve over Q is modular"], width=9, size=26).next_to(kol, DOWN, buff=0.35)
        self.play(FadeIn(kol))
        self.cue("And since 2001")
        self.play(FadeIn(mod))
        self.finish()
        self.clear_content()

        self.narrate("4.3")
        f = formula().scale(0.75).move_to(1.6 * UP)
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        row = VGroup(*[txt(str(p), 32, WHITE) for p in primes]).arrange(RIGHT, buff=0.7).move_to(0.3 * DOWN)
        pl = txt("the same number of factors of each prime, on both sides", 26, GREY_A).next_to(row, DOWN, buff=0.4)
        self.play(FadeIn(f))
        self.play(LaggedStart(*[FadeIn(t) for t in row], lag_ratio=0.1), FadeIn(pl))
        self.finish()

        self.narrate("4.4")
        marks = VGroup()
        for k, t in enumerate(row):
            if k in (0, 2, 3, 6):
                m = VGroup(tick(s=0.9), txt("if ...", 18, GREY_B)).arrange(DOWN, buff=0.05)
            else:
                m = txt("?", 36, YELLOW)
            marks.add(m.next_to(t, UP, buff=0.25))
        self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15), run_time=2)
        self.finish()

        self.recap("4.5", ["Rank 0 and 1: the rank was known;", "the exact formula, only in part."])


# ---------------------------------------------------------------------------
# Chapter 5 — the claim
# ---------------------------------------------------------------------------

class C5Claim(Video):
    def construct(self):
        self.chapter(2, "5. The claim")
        self.narrate("5.1")
        outer = RoundedRectangle(width=7.5, height=3.4, corner_radius=0.3).set_stroke(YELLOW, 3).move_to(0.6 * UP)
        ol = txt("the Selmer group", 30, YELLOW).next_to(outer, UP, buff=0.15)
        inner1 = RoundedRectangle(width=3.2, height=2.2, corner_radius=0.2).set_stroke(BLUE_C, 2)
        inner2 = RoundedRectangle(width=3.2, height=2.2, corner_radius=0.2).set_stroke(SHA, 2)
        inn = VGroup(inner1, inner2).arrange(RIGHT, buff=0.4).move_to(outer)
        il = VGroup(txt("rational points", 26, BLUE_C).move_to(inner1), txt("part of Sha", 26, SHA).move_to(inner2))
        self.play(ShowCreation(outer), FadeIn(ol))
        self.play(FadeIn(inn), FadeIn(il))
        self.finish()

        self.narrate("5.2")
        ub = txt("its size bounds the rank from above, and it can often be computed", 26, GREY_A)
        ub.next_to(outer, DOWN, buff=0.4)
        self.play(FadeIn(ub))
        self.finish()
        self.clear_content()

        self.narrate("5.3")
        thm = card(["If the Selmer bound at some prime is 0 or 1, then",
                    "the rank equals it, Sha is finite,", "and the exact formula holds, at every prime."],
                   title="The claim (Theorem 1.1)", width=10.5, size=30).move_to(0.8 * UP)
        self.play(FadeIn(thm))
        self.finish()

        self.narrate("5.4")
        stamp = txt("no extra conditions on the curve", 32, NEWC).next_to(thm, DOWN, buff=0.5)
        self.play(FadeIn(stamp, scale=1.3))
        self.finish()

        self.recap("5.5", ["Selmer bound 0 or 1:", "everything Birch and Swinnerton-Dyer predicted is true."])


# ---------------------------------------------------------------------------
# Chapter 6 — how it works
# ---------------------------------------------------------------------------

class C6How(Video):
    def construct(self):
        self.chapter(3, "6. How it works")
        self.narrate("6.1")
        inputs = VGroup(card(["converse", "companion, 82 pages"], width=3.0, size=24),
                        card(["the prime 2", "companion, 164 pages"], width=3.0, size=24),
                        card(["twist densities", "companion, 130 pages"], width=3.0, size=24),
                        card(["complex multiplication,", "rank 0 (Burungale–Flach)"], width=3.4, size=22))
        inputs.arrange(RIGHT, buff=0.25).move_to(1.4 * UP)
        self.play(LaggedStart(*[FadeIn(c, shift=0.1 * DOWN) for c in inputs], lag_ratio=0.3), run_time=2)
        self.finish()

        self.narrate("6.2")
        self.play(inputs[0][0].animate.set_stroke(YELLOW, 3))
        self.cue("The second gives")
        self.play(inputs[1][0].animate.set_stroke(YELLOW, 3))
        self.cue("The new step")
        new = txt("new here: every odd prime", 32, NEWC).move_to(0.2 * DOWN)
        self.play(FadeIn(new, scale=1.2))
        self.finish()
        self.clear_content()

        self.narrate("6.3")
        gl = txt("X = the number of factors of p by which the formula is off", 28, GREY_A).move_to(2.2 * UP)
        gauge = NumberLine((-3, 3, 1), width=8, include_numbers=False).set_stroke(GREY_B, 3).move_to(1.2 * UP)
        nums = VGroup(*[txt(str(v), 22, GREY_B).next_to(gauge.n2p(v), DOWN, buff=0.15) for v in range(-3, 4)])
        target = Circle(radius=0.22).set_stroke(GREEN_C, 4).move_to(gauge.n2p(0))
        self.play(FadeIn(gl), ShowCreation(gauge), FadeIn(nums))
        self.play(ShowCreation(target))
        self.finish()

        def box(tex, color, width=3.4):
            t = Tex(tex, font_size=40).set_color(color)
            r = RoundedRectangle(width=max(width, t.get_width() + 0.6), height=1.0, corner_radius=0.2)
            r.set_stroke(color, 3).set_fill(BLACK, 0.9)
            return VGroup(r, t.move_to(r))

        b1 = box(R"X(E) \geq 0", BLUE_C).move_to(4.2 * LEFT + 0.45 * DOWN)
        b2 = box(R"X(E^D) \geq 0", BLUE_C).move_to(4.2 * LEFT + 1.75 * DOWN)
        b3 = box(R"X(E) + X(E^D) = 0", GREEN_C).move_to(0.3 * RIGHT + 1.1 * DOWN)
        b4 = box(R"X(E) = 0", ORANGE).move_to(4.6 * RIGHT + 1.1 * DOWN)

        self.narrate("6.4")
        self.play(FadeIn(b1))
        self.finish()

        self.narrate("6.5")
        self.play(FadeIn(b2))
        self.finish()

        self.narrate("6.6")
        a1 = Arrow(b1.get_right(), b3.get_left(), buff=0.1, fill_color=GREY_B, thickness=3)
        a2 = Arrow(b2.get_right(), b3.get_left(), buff=0.1, fill_color=GREY_B, thickness=3)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(b3))
        self.finish()

        self.narrate("6.7")
        a3 = Arrow(b3.get_right(), b4.get_left(), buff=0.1, fill_color=GREY_B, thickness=3)
        dot = Dot(gauge.n2p(2.2), radius=0.14, fill_color=ORANGE)
        self.play(FadeIn(dot))
        self.play(dot.animate.move_to(gauge.n2p(0)), GrowArrow(a3), FadeIn(b4), run_time=2)
        self.finish()
        self.clear_content()

        self.narrate("6.8")
        k = card(["a new number system: an imaginary quadratic field", "where a Heegner point lives"],
                 width=10, size=28).move_to(1.8 * UP)
        an = card(["analytic series", "from L-values"], width=3.6, size=26)
        al = card(["algebraic series", "from Galois cohomology"], width=3.6, size=26)
        row = VGroup(an, al).arrange(RIGHT, buff=2.0).move_to(0.0 * UP)
        ratio = txt("their ratio is a unit", 30, NEWC).next_to(row, DOWN, buff=0.45)
        self.play(FadeIn(k))
        self.cue("The paper builds")
        self.play(FadeIn(an), FadeIn(al))
        self.cue("and shows their ratio")
        self.play(FadeIn(ratio))
        self.finish()
        self.clear_content()

        self.narrate("6.9")
        stages = ["integral", "no factor of p", "theta series", "a unit"]
        chain = VGroup(*[card([s], width=2.6, size=26) for s in stages]).arrange(RIGHT, buff=0.55).move_to(0.6 * UP)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, fill_color=GREY_B, thickness=3)
                          for a, b in zip(chain, chain[1:])])
        for i in range(4):
            anims = [FadeIn(chain[i], shift=0.1 * RIGHT)] + ([GrowArrow(arrows[i - 1])] if i else [])
            self.play(*anims, run_time=0.8)
        self.finish()
        self.clear_content()

        self.narrate("6.10")
        fr = Tex(R"\frac{\text{L-value side}}{\text{arithmetic side}}", font_size=60).move_to(1.0 * UP)
        one = Tex("= 1", font_size=72).set_color(NEWC).next_to(fr, RIGHT, buff=0.4)
        note = txt("a positive fraction with no prime factors", 28, GREY_A).next_to(fr, DOWN, buff=0.6)
        self.play(Write(fr))
        self.play(FadeIn(note))
        self.cue("So it equals one")
        self.play(FadeIn(one, scale=1.4))
        self.finish()

        self.recap("6.11", ["At each prime: at least zero, twice,", "adding up to zero. So exactly zero."])


# ---------------------------------------------------------------------------
# Chapter 7 — what follows
# ---------------------------------------------------------------------------

class C7Follow(Video):
    def construct(self):
        self.chapter(3, "7. What follows")
        rng = np.random.default_rng(3)
        self.narrate("7.1")
        n = 60
        ranks = rng.permutation([0] * 30 + [1] * 29 + [2])
        cells = VGroup(*[Square(0.42).set_stroke(width=0).set_fill(BLUE_D if r == 0 else (PURPLE_D if r == 1 else RED_D),
                                                                   1)
                         for r in ranks]).arrange_in_grid(4, 15, h_buff=0.08, v_buff=0.08).move_to(0.9 * UP)
        key = VGroup(txt("rank 0", 24, BLUE_C), txt("rank 1", 24, PURPLE_B), txt("rank 2 or more: rare", 24, RED_C))
        key.arrange(RIGHT, buff=0.6).next_to(cells, DOWN, buff=0.35)
        fl = txt("twists of one curve", 28, GREY_A).next_to(cells, UP, buff=0.25)
        self.play(FadeIn(fl), LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01), run_time=2)
        self.play(FadeIn(key))
        self.finish()

        self.narrate("7.2")
        self.play(*[c.animate.set_stroke(GREEN_C, 3) for c, r in zip(cells, ranks) if r < 2], run_time=1.5)
        al = txt("full formula for almost all twists", 28, GREEN_C).next_to(key, DOWN, buff=0.3)
        self.play(FadeIn(al))
        self.finish()
        self.clear_content()

        self.narrate("7.3")
        eq = Tex(R"x^3 + y^3 = \ell", font_size=56).move_to(2.3 * UP)
        rows = VGroup()
        for ell, (a, b, z) in CUBES[:8]:
            fa = Fraction(a, z)
            fb = Fraction(b, z)
            rows.add(VGroup(Tex(f"{ell} =", font_size=36).set_color(BLUE_C),
                            Tex(f"\\left({frac_str(fa)}\\right)^3 + \\left({frac_str(fb)}\\right)^3", font_size=36))
                     .arrange(RIGHT, buff=0.25))
        rows.arrange_in_grid(4, 2, h_buff=1.2, v_buff=0.3, aligned_edge=LEFT).next_to(eq, DOWN, buff=0.45)
        rule = txt("every prime leaving remainder 4, 7 or 8 on division by 9", 24, GREY_A).next_to(rows, DOWN,
                                                                                                   buff=0.35)
        self.play(Write(eq))
        self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2), run_time=3)
        self.play(FadeIn(rule))
        self.finish()

        self.narrate("7.4")
        target = rows[5]   # 53
        self.play(*[FadeOut(r) for r in rows if r is not target], FadeOut(rule))
        self.play(target.animate.scale(1.5).move_to(0.3 * UP).set_color(YELLOW))
        self.finish()

        self.recap("7.5", ["The full formula for almost all twists;", "and primes as sums of two cubes."])


# ---------------------------------------------------------------------------
# Chapter 8 — is it right?
# ---------------------------------------------------------------------------

class C8Check(Video):
    def construct(self):
        self.chapter(4, "8. Is it right?")
        self.narrate("8.1")
        papers = VGroup(paper_card(94, "this paper"), paper_card(82, "converse"), paper_card(164, "the prime 2"),
                        paper_card(130, "twist densities")).arrange(RIGHT, buff=0.3).move_to(0.9 * UP)
        papers[0][0].set_stroke(YELLOW, 3)
        allr = txt("all four have to be right", 28, YELLOW).next_to(papers, DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(p, shift=0.1 * DOWN) for p in papers], lag_ratio=0.3), run_time=2.5)
        self.play(FadeIn(allr))
        self.finish()
        self.clear_content()

        self.narrate("8.2")
        lean = card(["Lean: no computer-checked proof"], width=7.5, size=32).move_to(0.8 * UP)
        x = cross(s=1.6).next_to(lean, LEFT, buff=0.4)
        self.play(FadeIn(lean), ShowCreation(x))
        self.finish()
        self.play(FadeOut(VGroup(lean, x)))

        self.narrate("8.3")
        dates = VGroup(txt("3 October 2026: first posted", 30), txt("7 October: references updated only", 30, GREY_A))
        dates.arrange(DOWN, buff=0.35).move_to(0.8 * UP)
        self.play(FadeIn(dates[0]))
        self.cue("The seventh")
        self.play(FadeIn(dates[1]))
        self.finish()
        self.play(FadeOut(dates))

        self.narrate("8.4")
        st = txt("no public expert assessment found, as of 4 November 2026", 30, ORANGE).move_to(0.8 * UP)
        self.play(FadeIn(st))
        self.finish()

        self.recap("8.5", ["Four unreviewed papers, no formal proof,", "no expert verdict yet."])


# ---------------------------------------------------------------------------
# Chapter 9 — what it does not do
# ---------------------------------------------------------------------------

class C9Close(Video):
    def construct(self):
        self.chapter(4, "9. What it does not do")
        self.narrate("9.1")
        ax = Chart((-2.6, 3.0), (-5, 4), 4.4, 4.6, grid=False)
        ax.shift(3.3 * LEFT + 0.3 * DOWN - ax.box.get_center())
        cv = curve_branches(ax, (1, 1, -2, 0), -2.6, 2.55)
        eq = Tex(R"y^2 + y = x^3 + x^2 - 2x", font_size=36).next_to(ax.box, UP, buff=0.1)
        r2 = VGroup(txt("rank 2: untouched", 32, RED_C), txt("not even Sha is known to be finite", 26, GREY_A))
        r2.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(2.7 * RIGHT + 0.4 * UP)
        self.play(ShowCreation(cv), FadeIn(eq), run_time=2)
        self.play(FadeIn(r2))
        self.finish()
        self.clear_content()

        self.narrate("9.2")
        data = [(rank, bsd_products(coeffs, N)) for name, coeffs, N, rank in CURVES]
        a = Chart((0.0, 2.5), (0, 8.5), 8.2, 4.0, grid=False, xlabel="primes counted", ylabel="product of count / p")
        a.shift(0.5 * UP - a.box.get_center())
        cols = [GREY_B, BLUE_C, GREEN_C, ORANGE]
        lines = VGroup()
        for (rank, arr), c in zip(data, cols):
            pts = arr[:: max(1, len(arr) // 600)]
            lines.add(VMobject().set_points_as_corners([a.c2p(x, y) for x, y in pts]).set_stroke(c, 3))
        qs = VGroup(*[txt("?", 40, YELLOW).next_to(a.c2p(*data[k][1][-1]), RIGHT, buff=0.15) for k in (2, 3)])
        self.play(FadeIn(a), ShowCreation(lines), run_time=2)
        self.play(lines[0].animate.set_stroke(opacity=0.3), lines[1].animate.set_stroke(opacity=0.3), FadeIn(qs))
        self.finish()
        self.clear_content()

        self.narrate("9.3")
        self.play(FadeOut(self.roadmap_mob))
        title = txt("The Birch–Swinnerton-Dyer formula", 48)
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
        title = txt("The Birch–Swinnerton-Dyer formula", 56).to_edge(UP, buff=0.6)
        sub = txt("rational points and L-functions, explained for everyone", 30, GREY_A).next_to(title, DOWN, buff=0.25)
        ax = plane(w=4.0, h=4.4)
        ax.shift(3.6 * LEFT + 1.0 * DOWN - ax.box.get_center())
        cv = curve_branches(ax, (0, 1, -1, 0), -1.6, 2.1)
        pts = [p for p in multiples(9) if p is not None and abs(float(p[0])) < 2.6 and -3.2 < float(p[1]) < 2.2]
        dots = VGroup(*[Dot(ax.c2p(float(x), float(y)), radius=0.08, fill_color=POINT) for x, y in pts])
        f = formula().scale(0.7).move_to(2.6 * RIGHT + 1.0 * DOWN)
        self.add(title, sub, cv, dots, f)
