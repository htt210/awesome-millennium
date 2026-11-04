"""Narrated explainer for "The Quasi-Riemann Hypothesis" (OpenAI, September 2026),
written for 3b1b's manim (manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("2.4") and
the words come from beat 2.4 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl qrh_video.py C2Zeta -w -l --config_file ../../../../../tools/video/custom_config.yml

Computed from data: the prime staircase and its error, Riemann's explicit
formula built from the first zeros of zeta, the Moebius running total, the
Eisenstein primes and the least quadratic nonresidues. The bar charts of the
"crowd" and the folding rows are schematics.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "video"))
from narrated import *  # noqa: E402,F403

PRIME = YELLOW
SMOOTH = ORANGE
ZERO = BLUE_C
OLD = GREEN_C
NEW = ORANGE
ROGUE = RED_C

# Imaginary parts of the first nontrivial zeros of zeta (all on Re s = 1/2).
ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073,
         48.005151, 49.773832, 52.970321, 56.446248, 59.347044]

# Euler's idoneal numbers (65 known).
IDONEAL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 18, 21, 22, 24, 25, 28, 30, 33, 37, 40, 42, 45, 48,
           57, 58, 60, 70, 72, 78, 85, 88, 93, 102, 105, 112, 120, 130, 133, 165, 168, 177, 190, 210, 232, 240,
           253, 273, 280, 312, 330, 345, 357, 385, 408, 462, 520, 760, 840, 1320, 1365, 1848]


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["Primes", "Zeta", "The claim", "How it works", "Is it right?"]
    PRONOUNCE = [(r"\bDirichlet\b", "Deerishlay"), (r"\bSiegel\b", "Seagull"), (r"\bidoneal\b", "eye-doh-nee-al"),
                 (r"\b1859\b", "eighteen fifty-nine"), (r"\b1896\b", "eighteen ninety-six"),
                 (r"\b2026\b", "twenty twenty-six")]
    BUILD = HERE / "build"


# ---------------------------------------------------------------------------
# number theory data
# ---------------------------------------------------------------------------

def sieve(n: int) -> np.ndarray:
    is_p = np.ones(n + 1, dtype=bool)
    is_p[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = False
    return is_p


def mobius(n: int) -> np.ndarray:
    mu = np.ones(n + 1, dtype=np.int8)
    mu[0] = 0
    for p in np.nonzero(sieve(n))[0]:
        mu[p::p] *= -1
        mu[p * p::p * p] = 0
    return mu


def li(x: float) -> float:
    """Offset logarithmic integral from 2 to x (Simpson's rule)."""
    if x <= 2:
        return 0.0
    n = 2000
    t = np.linspace(2, x, n + 1)
    f = 1 / np.log(t)
    h = (x - 2) / n
    return float(h / 3 * (f[0] + f[-1] + 4 * f[1:-1:2].sum() + 2 * f[2:-1:2].sum()))


IS_P = sieve(1_000_000)
PI = np.cumsum(IS_P)


def psi_step(x: float) -> float:
    """Chebyshev's weighted prime count: log p for every prime power p^k up to x."""
    total = 0.0
    for p in range(2, int(x) + 1):
        if IS_P[p]:
            q = p
            while q <= x:
                total += math.log(p)
                q *= p
    return total


def psi_explicit(x: float, k: int) -> float:
    """Riemann–von Mangoldt explicit formula truncated to the first k pairs of zeros."""
    v = x - math.log(2 * math.pi) - 0.5 * math.log(1 - x ** -2)
    for g in ZEROS[:k]:
        rho = complex(0.5, g)
        v -= 2 * (x ** rho / rho).real
    return v


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def tick(color=GREEN_C, s=1.0):
    return VMobject().set_points_as_corners([[-0.22 * s, 0, 0], [-0.06 * s, -0.18 * s, 0], [0.24 * s, 0.22 * s, 0]]
                                            ).set_stroke(color, 6)


def cross(color=RED_C, s=1.0):
    a = 0.18 * s
    return VGroup(Line([-a, -a, 0], [a, a, 0]), Line([-a, a, 0], [a, -a, 0])).set_stroke(color, 6)


class Strip(VGroup):
    """The critical strip: real part 0..1 left to right, height 0..T upwards."""

    def __init__(self, width=4.2, height=4.6, T=62, center=ORIGIN, zeros=True):
        super().__init__()
        self.W, self.H, self.T = width, height, T
        band = Rectangle(width=width, height=height).set_stroke(width=0).set_fill(GREY_E, 1).move_to(center)
        self.band = band
        edges = VGroup(Line(self.p(0, 0), self.p(0, T)), Line(self.p(1, 0), self.p(1, T))).set_stroke(GREY_B, 2)
        base = Line(self.p(-0.08, 0), self.p(1.08, 0)).set_stroke(GREY_B, 2)
        half = DashedLine(self.p(0.5, 0), self.p(0.5, T), dash_length=0.12).set_stroke(ZERO, 2)
        labels = VGroup(*[txt(s, 24, GREY_A).next_to(self.p(x, 0), DOWN, buff=0.15)
                          for x, s in ((0, "0"), (0.5, "1/2"), (1, "1"))])
        self.band, self.half, self.labels = band, half, labels
        self.add(band, edges, base, half, labels)
        self.dots = VGroup(*[Dot(self.p(0.5, g), radius=0.07, fill_color=ZERO) for g in ZEROS])
        if zeros:
            self.add(self.dots)

    def p(self, x, t):
        # measured from the band's current corner, so it stays right after the strip is moved
        return self.band.get_corner(DL) + np.array([x * self.W, t / self.T * self.H, 0])

    def zone(self, x0, x1, color, opacity=0.55):
        r = Rectangle(width=(x1 - x0) * self.W, height=self.H).set_stroke(width=0).set_fill(color, opacity)
        return r.move_to(self.p((x0 + x1) / 2, self.T / 2))

    def classical(self, color=OLD, opacity=0.55):
        ts = np.linspace(0, self.T, 120)
        w = 0.3 / np.log(ts + 4)
        right = [self.p(1 - wi, t) for wi, t in zip(w, ts)] + [self.p(1, self.T), self.p(1, 0)]
        left = [self.p(wi, t) for wi, t in zip(w, ts)] + [self.p(0, self.T), self.p(0, 0)]
        return VGroup(*[Polygon(*pts).set_stroke(width=0).set_fill(color, opacity) for pts in (right, left)])

    def vline(self, x, color, label=None, size=22):
        g = VGroup(DashedLine(self.p(x, 0), self.p(x, self.T), dash_length=0.1).set_stroke(color, 3))
        if label:
            g.add(txt(label, size, color).next_to(self.p(x, 0), DOWN, buff=0.15))
        return g


def staircase(ax, xs_int, counts, color=PRIME, width=4):
    pts = []
    for i in range(len(xs_int) - 1):
        pts.append(ax.c2p(xs_int[i], counts[i]))
        pts.append(ax.c2p(xs_int[i + 1], counts[i]))
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


def number_tile(n, color=GREY_A, size=28):
    return txt(str(n), size, color)


def eisenstein_grid(R=3.0, scale=0.34):
    is_p = sieve(400)
    dots = VGroup()
    rr = R / scale
    for a in range(-14, 15):
        for b in range(-14, 15):
            x, y = a - b / 2, b * math.sqrt(3) / 2
            if x * x + y * y > rr * rr or (a == 0 and b == 0):
                continue
            n = a * a - a * b + b * b
            q = math.isqrt(n)
            prime = bool(is_p[n]) or (q * q == n and bool(is_p[q]) and q % 3 == 2)
            unit = n == 1
            color = BLUE_C if unit else (ORANGE if prime else GREY_C)
            r = 0.075 if (prime or unit) else 0.04
            dots.add(Dot(np.array([x * scale, y * scale, 0]), radius=r, fill_color=color))
    dots.add(Dot(ORIGIN, radius=0.05, fill_color=WHITE))
    return dots


def least_nonresidue(p: int) -> int:
    n = 2
    while pow(n, (p - 1) // 2, p) == 1:
        n += 1
    return n


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        line = NumberLine((0, 40, 1), width=12, include_numbers=False).set_stroke(GREY_B, 2).shift(0.6 * UP)
        primes = [p for p in range(2, 41) if IS_P[p]]
        dots = VGroup(*[Dot(line.n2p(p), radius=0.1, fill_color=PRIME) for p in primes])
        nums = VGroup(*[txt(str(p), 24, PRIME).next_to(line.n2p(p), DOWN, buff=0.25) for p in primes])
        self.narrate("0.1")
        self.play(ShowCreation(line))
        for d, n, phrase in zip(dots[:6], nums[:6], ["Two", "three", "five", "seven", "eleven", "thirteen"]):
            self.cue(phrase)
            self.play(FadeIn(d, scale=1.6), FadeIn(n), run_time=0.4)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(d, scale=1.6), FadeIn(n)) for d, n in zip(dots[6:], nums[6:])],
                              lag_ratio=0.25), run_time=2)
        self.finish()

        self.narrate("0.2")
        self.play(FadeOut(VGroup(line, dots, nums)))
        ax = Chart((0, 100), (0, 30), 8.5, 3.8, grid=False, xlabel="x", ylabel="primes up to x")
        ax.shift(0.4 * UP - ax.box.get_center())
        xs = list(range(0, 101))
        st = staircase(ax, xs, [int(PI[x]) if x >= 2 else 0 for x in xs])
        sm = curve(ax, li, 2, 100, n=120, color=SMOOTH, width=5)
        self.play(FadeIn(ax), ShowCreation(st), run_time=2.5)
        self.cue("they follow a smooth curve")
        self.play(ShowCreation(sm), run_time=2)
        self.finish()

        self.narrate("0.3")
        title = txt("The Quasi-Riemann Hypothesis", 54)
        sub = txt("OpenAI preprint, September 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(VGroup(ax, st, sm)), Write(title, run_time=2))
        self.play(FadeIn(sub))
        self.finish()
        self.clear_caption()

        self.narrate("0.4")
        big = self.roadmap(None, big=True).move_to(1.5 * DOWN)
        self.play(title.animate.shift(UP), sub.animate.shift(UP), FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — primes
# ---------------------------------------------------------------------------

class C1Primes(Video):
    def construct(self):
        self.chapter(0, "1. Primes")
        self.narrate("1.1")
        tiles = VGroup(*[number_tile(n) for n in range(1, 61)]).arrange_in_grid(6, 10, buff=(0.55, 0.3))
        tiles.move_to(0.4 * UP)
        self.play(LaggedStart(*[FadeIn(t) for t in tiles], lag_ratio=0.02), run_time=2)
        self.play(*[tiles[n - 1].animate.set_color(PRIME).scale(1.15) for n in range(2, 61) if IS_P[n]],
                  *[tiles[n - 1].animate.set_color(GREY_D) for n in range(1, 61) if not IS_P[n]], run_time=1.5)
        self.finish()
        self.play(FadeOut(tiles))

        self.narrate("1.2")
        ax = Chart((0, 100), (0, 30), 8.5, 3.6, xticks=(0, 25, 50, 75, 100), yticks=(0, 10, 20, 30),
                   xfmt=lambda v: txt(str(int(v)), 20, GREY_B), yfmt=lambda v: txt(str(int(v)), 20, GREY_B),
                   xlabel="x", ylabel="primes up to x", grid=False)
        ax.shift(0.5 * UP - ax.box.get_center())
        xs = list(range(0, 101))
        st = staircase(ax, xs, [int(PI[x]) if x >= 2 else 0 for x in xs])
        self.play(FadeIn(ax))
        self.play(ShowCreation(st), run_time=3, rate_func=linear)
        n25 = txt("25 primes", 26, PRIME).next_to(ax.c2p(100, 25), UL, buff=0.15)
        self.play(FadeIn(n25))
        self.finish()

        self.narrate("1.3")
        sm = curve(ax, li, 2, 100, n=120, color=SMOOTH, width=5)
        sl = txt("smooth curve", 26, SMOOTH).next_to(ax.c2p(60, 20), UL, buff=0.1)
        self.play(ShowCreation(sm), FadeIn(sl), run_time=2)
        self.finish()
        self.play(FadeOut(VGroup(ax, st, sm, sl, n25)))

        self.narrate("1.4")
        ax2 = Chart((2, 6), (-600, 600), 8.5, 3.6, xticks=(2, 3, 4, 5, 6), yticks=(-400, 0, 400),
                    xfmt=lambda v: Tex(f"10^{{{int(v)}}}", font_size=26).set_color(GREY_B),
                    yfmt=lambda v: txt(str(int(v)), 20, GREY_B),
                    xlabel="x (log scale)", ylabel="curve minus count", grid=False)
        ax2.shift(0.5 * UP - ax2.box.get_center())
        lxs = np.linspace(2, 6, 500)
        err = [li(10 ** v) - PI[int(10 ** v)] for v in lxs]
        pts = [ax2.c2p(v, e) for v, e in zip(lxs, err)]
        wob = VMobject().set_points_as_corners(pts).set_stroke(PRIME, 3)
        env = lambda v: math.sqrt(10 ** v) * math.log(10 ** v) / (8 * math.pi)  # noqa: E731
        band = VGroup(curve(ax2, env, 2, 6, color=GREEN_C, width=3),
                      curve(ax2, lambda v: -env(v), 2, 6, color=GREEN_C, width=3))
        band = VGroup(*[DashedVMobject(b, num_dashes=40) for b in band])
        self.play(FadeIn(ax2))
        self.play(ShowCreation(wob), run_time=3)
        self.cue("Up to a million")
        lab = txt("about 130 off, out of 78,498", 24, PRIME).next_to(ax2.c2p(6, 130), UL, buff=0.2)
        self.play(FadeIn(lab))
        self.finish()

        self.narrate("1.5")
        q = txt("?", 72, GREEN_C).next_to(ax2.c2p(6, 500), LEFT, buff=0.3)
        self.play(ShowCreation(band), run_time=2)
        self.play(FadeIn(q, scale=1.4))
        self.finish()

        self.recap("1.6", ["Primes follow a smooth curve.", "The question is the size of the wobble."])


# ---------------------------------------------------------------------------
# Chapter 2 — zeta
# ---------------------------------------------------------------------------

class C2Zeta(Video):
    def construct(self):
        self.chapter(1, "2. Zeta")
        self.narrate("2.1")
        zeta = Tex(R"\zeta(s) = 1 + \frac{1}{2^s} + \frac{1}{3^s} + \frac{1}{4^s} + \cdots", font_size=64)
        zeta.move_to(1.2 * UP)
        self.play(Write(zeta), run_time=3)
        self.finish()

        self.narrate("2.2")
        o = 2.0 * LEFT + 2.0 * DOWN
        xa = Arrow(o, o + 4.5 * RIGHT, buff=0, fill_color=GREY_B, thickness=3)
        ya = Arrow(o, o + 2.6 * UP, buff=0, fill_color=GREY_B, thickness=3)
        xl = txt("position", 24, GREY_A).next_to(xa, DOWN, buff=0.15)
        yl = txt("height", 24, GREY_A).next_to(ya, LEFT, buff=0.15)
        s = Dot(o + 2.8 * RIGHT + 1.6 * UP, radius=0.11, fill_color=YELLOW)
        sl = Tex("s", font_size=48).set_color(YELLOW).next_to(s, UR, buff=0.1)
        self.play(GrowArrow(xa), GrowArrow(ya), FadeIn(xl), FadeIn(yl))
        self.play(FadeIn(s, scale=1.5), FadeIn(sl))
        self.finish()
        self.play(FadeOut(VGroup(xa, ya, xl, yl, s, sl)))

        self.narrate("2.3")
        prod = Tex(R"= \frac{1}{1-2^{-s}} \cdot \frac{1}{1-3^{-s}} \cdot \frac{1}{1-5^{-s}} \cdot \frac{1}{1-7^{-s}} \cdots",
                   font_size=56).next_to(zeta, DOWN, buff=0.7)
        pl = txt("a product over the primes", 28, PRIME).next_to(prod, DOWN, buff=0.5)
        self.play(Write(prod), run_time=2.5)
        self.play(FadeIn(pl))
        self.finish()
        self.play(FadeOut(VGroup(zeta, prod, pl)))

        self.narrate("2.4")
        ax = Chart((2, 50), (0, 55), 8.5, 3.6, xticks=(10, 20, 30, 40, 50), yticks=(0, 25, 50),
                   xfmt=lambda v: txt(str(int(v)), 20, GREY_B), yfmt=lambda v: txt(str(int(v)), 20, GREY_B),
                   xlabel="x", ylabel="weighted prime count", grid=False)
        ax.shift(0.5 * UP - ax.box.get_center())
        xs = np.linspace(2, 50, 961)
        st_pts = []
        prev = None
        for x in xs:
            y = psi_step(x)
            if prev is not None and y != prev:
                st_pts.append(ax.c2p(x, prev))
            st_pts.append(ax.c2p(x, y))
            prev = y
        stair = VMobject().set_points_as_corners(st_pts).set_stroke(PRIME, 3)
        k = ValueTracker(0)
        approx = always_redraw(lambda: VMobject().set_points_as_corners(
            [ax.c2p(x, max(-2, min(57, psi_explicit(x, int(k.get_value()))))) for x in np.linspace(2.05, 50, 700)]
        ).set_stroke(SMOOTH, 4))
        klab = always_redraw(lambda: txt(f"smooth curve + {int(k.get_value())} waves", 26, SMOOTH)
                             .next_to(ax.box, UP, buff=0.1).align_to(ax.box, LEFT))
        self.play(FadeIn(ax), ShowCreation(stair), run_time=2)
        self.play(FadeIn(approx), FadeIn(klab))
        self.cue("plus one wave")
        self.play(k.animate.set_value(13.99), run_time=6, rate_func=linear)
        self.finish()
        self.remove(approx, klab)
        self.play(FadeOut(VGroup(ax, stair)))

        self.narrate("2.5")
        a1 = Chart((1, 60), (-60, 60), 5.4, 3.0, grid=False, xlabel="x")
        a1.shift(3.3 * LEFT + 0.5 * UP - a1.box.get_center())
        a2 = Chart((1, 60), (-60, 60), 5.4, 3.0, grid=False, xlabel="x")
        a2.shift(3.3 * RIGHT + 0.5 * UP - a2.box.get_center())
        loud = curve(a1, lambda x: x ** 0.95 * math.sin(3 * math.log(x) * 4), 1, 60, n=400, color=ROGUE, width=4)
        quiet = curve(a2, lambda x: x ** 0.5 * math.sin(3 * math.log(x) * 4), 1, 60, n=400, color=ZERO, width=4)
        t1 = txt("zero near position 1: loud", 26, ROGUE).next_to(a1.box, UP, buff=0.15)
        t2 = txt("zero at 1/2: quiet", 26, ZERO).next_to(a2.box, UP, buff=0.15)
        self.play(FadeIn(a1), FadeIn(t1), ShowCreation(loud), run_time=2)
        self.cue("A zero at one half")
        self.play(FadeIn(a2), FadeIn(t2), ShowCreation(quiet), run_time=2)
        self.finish()
        self.play(FadeOut(VGroup(a1, a2, loud, quiet, t1, t2)))

        self.narrate("2.6")
        strip = Strip(zeros=False).move_to(0.35 * UP)
        name = txt("the critical strip", 28, GREY_A).next_to(strip.band, RIGHT, buff=0.5)
        self.play(FadeIn(strip), FadeIn(name))
        self.cue("Here are the first")
        self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in strip.dots], lag_ratio=0.15), run_time=2.5)
        self.add(strip.dots)
        self.finish()

        self.narrate("2.7")
        z = Circle(radius=0.09).set_stroke(ROGUE, 3).move_to(strip.p(0.8, 40))
        m = Circle(radius=0.09).set_stroke(ROGUE, 3).move_to(strip.p(0.2, 40))
        zl = txt("if a zero were here", 22, ROGUE).next_to(z, UP, buff=0.2)
        arr = CurvedArrow(z.get_left() + 0.05 * LEFT, m.get_right() + 0.05 * RIGHT, angle=0.8).set_stroke(ROGUE, 3)
        self.play(FadeIn(z), FadeIn(zl))
        self.cue("comes with one")
        self.play(ShowCreation(arr), FadeIn(m))
        self.finish()

        self.recap("2.8", ["Zeros of zeta set the wobble.", "Further right means a louder wave."])


# ---------------------------------------------------------------------------
# Chapter 3 — the question
# ---------------------------------------------------------------------------

class C3Question(Video):
    def construct(self):
        self.chapter(1, "3. The question")
        strip = Strip().move_to(2.6 * LEFT + 0.35 * UP)
        self.narrate("3.1")
        self.play(FadeIn(strip))
        rh = txt("Riemann hypothesis:\nevery zero on this line", 26, ZERO).next_to(strip.band, RIGHT, buff=0.6)
        rh.shift(1.2 * UP)
        self.play(FadeIn(rh), Indicate(strip.half, color=ZERO))
        self.cue("Computers have checked")
        chk = txt("more than ten trillion checked", 24, GREY_A).next_to(rh, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(FadeIn(chk))
        self.finish()

        self.narrate("3.2")
        prize = card(["Millennium Prize Problem", "unsolved"], width=4.6, size=26).next_to(chk, DOWN, buff=0.5)
        prize.align_to(rh, LEFT)
        self.play(FadeIn(prize))
        self.finish()
        self.play(FadeOut(VGroup(rh, chk, prize)))

        self.narrate("3.3")
        edge = Line(strip.p(1, 0), strip.p(1, strip.T)).set_stroke(OLD, 8)
        el = txt("no zeros on the edge (1896)", 26, OLD).next_to(strip.band, RIGHT, buff=0.6).shift(1.2 * UP)
        self.play(ShowCreation(edge), FadeIn(el))
        self.finish()

        self.narrate("3.4")
        zone = strip.classical()
        zl = txt("a zero-free margin that\nshrinks with height", 26, OLD).next_to(el, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(FadeIn(zone), FadeIn(zl), run_time=2)
        self.add(strip.dots)
        self.finish()
        self.play(FadeOut(VGroup(el, zl)))

        self.narrate("3.5")
        x0 = 0.95
        fixed = strip.zone(x0, 1, NEW, 0.45)
        fl = strip.vline(x0, NEW)
        ql = txt("some fixed line?\nno zeros to its right,\nat any height", 26, NEW)
        ql.next_to(strip.band, RIGHT, buff=0.6).shift(1.0 * UP)
        name = txt("the quasi-Riemann hypothesis", 28, YELLOW).next_to(ql, DOWN, buff=0.45, aligned_edge=LEFT)
        self.play(FadeIn(fixed), ShowCreation(fl), FadeIn(ql))
        self.cue("This is the quasi-Riemann")
        self.play(FadeIn(name))
        self.finish()
        self.play(FadeOut(VGroup(ql, name, fixed, fl)))
        self.clear_content()

        self.narrate("3.6")
        cous = VGroup(card(["primes that leave remainder 1 when divided by 4", "5, 13, 17, 29, 37, 41, ..."],
                           width=9, size=26),
                      card(["primes that leave remainder 3 when divided by 4", "3, 7, 11, 19, 23, 31, ..."],
                           width=9, size=26)).arrange(DOWN, buff=0.35).move_to(0.6 * UP)
        dl = txt("each counted by a Dirichlet L-function", 26, YELLOW).next_to(cous, DOWN, buff=0.4)
        self.play(FadeIn(cous[0]))
        self.play(FadeIn(cous[1]))
        self.play(FadeIn(dl))
        self.finish()
        self.play(FadeOut(VGroup(cous, dl)))

        self.narrate("3.7")
        real = NumberLine((0, 1, 0.5), width=10, include_numbers=False).set_stroke(GREY_B, 3).shift(0.4 * UP)
        rl = VGroup(*[txt(s, 26, GREY_A).next_to(real.n2p(v), DOWN, buff=0.25) for v, s in ((0, "0"), (0.5, "1/2"),
                                                                                             (1, "1"))])
        rogue = Dot(real.n2p(0.97), radius=0.13, fill_color=ROGUE)
        rq = txt("a rogue zero?", 30, ROGUE).next_to(rogue, UP, buff=0.4)
        self.play(ShowCreation(real), FadeIn(rl))
        self.play(FadeIn(rogue, scale=2), FadeIn(rq))
        self.cue("It is called")
        ls = txt("a Landau–Siegel zero", 28, ROGUE).next_to(rl, DOWN, buff=0.5)
        self.play(FadeIn(ls))
        self.finish()

        self.recap("3.8", ["The quasi-Riemann hypothesis:", "some fixed line with no zeros to its right."])


# ---------------------------------------------------------------------------
# Chapter 4 — the claim
# ---------------------------------------------------------------------------

class C4Claim(Video):
    def construct(self):
        self.chapter(2, "4. The claim")
        self.narrate("4.1")
        thm = card(["No zeros with real part above 7/8,", "for zeta and every Dirichlet L-function."],
                   title="The claim", width=10, size=32).move_to(0.6 * UP)
        self.play(FadeIn(thm))
        self.finish()
        self.play(thm.animate.scale(0.62).to_edge(UP, buff=0.75).to_edge(RIGHT, buff=0.4))

        self.narrate("4.2")
        strip = Strip().move_to(2.8 * LEFT + 0.2 * DOWN)
        self.play(FadeIn(strip))
        right = strip.zone(7 / 8, 1, NEW, 0.6)
        rl = strip.vline(7 / 8, NEW, "7/8")
        self.play(GrowFromEdge(right, DOWN), ShowCreation(rl), run_time=2)
        self.add(strip.dots)
        note = txt("at every height,\nfor every pattern of primes", 26, NEW).move_to(3.3 * RIGHT + 0.4 * DOWN)
        self.play(FadeIn(note))
        self.finish()

        self.narrate("4.3")
        left = strip.zone(0, 1 / 8, NEW, 0.6)
        ll = strip.vline(1 / 8, NEW, "1/8")
        self.play(GrowFromEdge(left, DOWN), ShowCreation(ll), run_time=2)
        mid = txt("every zero: between 1/8 and 7/8", 26, YELLOW).next_to(note, DOWN, buff=0.5)
        self.play(FadeIn(mid))
        self.finish()

        self.narrate("4.4")
        rogue = Dot(strip.p(0.97, 1.0), radius=0.11, fill_color=ROGUE)
        self.play(FadeIn(rogue, scale=2))
        self.play(ShowCreation(cross(s=1.0).move_to(rogue)))
        gone = txt("rogue zero: ruled out", 26, ROGUE).next_to(mid, DOWN, buff=0.5)
        self.play(FadeIn(gone))
        self.finish()
        self.clear_content()

        self.narrate("4.5")
        steps = VGroup(card(["Part I", "a line at 11/12"], width=4.0, size=30),
                       card(["Part II", "sharpened to 7/8"], width=4.0, size=30)).arrange(RIGHT, buff=1.2)
        steps.move_to(0.9 * UP)
        arrow = Arrow(steps[0].get_right(), steps[1].get_left(), buff=0.15, fill_color=GREY_B, thickness=4)
        comp = card(["companion paper, 5 October 2026", "a second proof of 11/12, written with human help"],
                    width=9, size=26).next_to(steps, DOWN, buff=0.6)
        self.play(FadeIn(steps[0]))
        self.play(GrowArrow(arrow), FadeIn(steps[1]))
        self.cue("A shorter companion")
        self.play(FadeIn(comp))
        self.finish()

        self.recap("4.6", ["Claimed: no zeros past 7/8,", "for zeta and all its cousins."])


# ---------------------------------------------------------------------------
# Chapter 5 — sums that cancel
# ---------------------------------------------------------------------------

class C5Cancel(Video):
    def construct(self):
        self.chapter(3, "5. How it works: sums that cancel")
        mu = mobius(100_000)
        self.narrate("5.1")
        tiles = VGroup()
        for n in range(1, 31):
            m = int(mu[n])
            sc = {1: ("+1", GREEN_C), -1: ("−1", RED_C), 0: ("0", GREY_C)}[m]
            tiles.add(VGroup(txt(str(n), 26, WHITE), txt(sc[0], 24, sc[1])).arrange(DOWN, buff=0.12))
        tiles.arrange_in_grid(3, 10, buff=(0.45, 0.45)).move_to(0.5 * UP)
        self.play(LaggedStart(*[FadeIn(t[0]) for t in tiles], lag_ratio=0.03))
        self.cue("An even number")
        self.play(LaggedStart(*[FadeIn(t[1]) for t in tiles], lag_ratio=0.05), run_time=3)
        self.finish()
        self.play(FadeOut(tiles))

        self.narrate("5.2")
        ax = Chart((0, 100_000), (-400, 400), 8.5, 3.6, xticks=(0, 50_000, 100_000), yticks=(-300, 0, 300),
                   xfmt=lambda v: txt(f"{int(v):,}", 20, GREY_B), yfmt=lambda v: txt(str(int(v)), 20, GREY_B),
                   xlabel="x", ylabel="running total", grid=False)
        ax.shift(0.5 * UP - ax.box.get_center())
        M = np.cumsum(mu.astype(np.int64))
        idx = np.linspace(1, 100_000, 1500).astype(int)
        walk = VMobject().set_points_as_corners([ax.c2p(int(i), int(M[i])) for i in idx]).set_stroke(ZERO, 2.5)
        root = VGroup(curve(ax, lambda x: math.sqrt(x), 0, 100_000, color=GREEN_C, width=3),
                      curve(ax, lambda x: -math.sqrt(x), 0, 100_000, color=GREEN_C, width=3))
        root = VGroup(*[DashedVMobject(r, num_dashes=40) for r in root])
        rl = Tex(R"\pm\sqrt{x}", font_size=34).set_color(GREEN_C).next_to(ax.c2p(100_000, 316), RIGHT, buff=0.1)
        self.play(FadeIn(ax))
        self.play(ShowCreation(walk), run_time=3, rate_func=linear)
        self.play(ShowCreation(root), FadeIn(rl))
        self.finish()

        self.narrate("5.3")
        push = curve(ax, lambda x: x ** 0.53, 1, 100_000, color=ROGUE, width=4, ylim=(-1, 400))
        pl = Tex(R"x^{\beta}", font_size=40).set_color(ROGUE).next_to(ax.c2p(100_000, 400), LEFT, buff=0.2)
        self.play(ShowCreation(push), FadeIn(pl), run_time=2)
        self.finish()
        self.play(FadeOut(VGroup(ax, walk, root, rl, push, pl)))

        self.narrate("5.4")
        a = card(["the total never grows", "faster than x to a power θ"], width=5.0, size=28)
        b = card(["no zeros to the", "right of θ"], width=5.0, size=28)
        row = VGroup(a, b).arrange(RIGHT, buff=1.6).move_to(0.6 * UP)
        arr = Arrow(a.get_right(), b.get_left(), buff=0.15, fill_color=YELLOW, thickness=4)
        self.play(FadeIn(a))
        self.play(GrowArrow(arr), FadeIn(b))
        self.finish()
        self.play(FadeOut(VGroup(a, b, arr)))

        self.narrate("5.5")
        p1 = card(["assume a rightmost zero", "beyond the line"], width=5.0, size=28)
        p2 = card(["one sum, built two ways:", "large and small at once"], width=5.0, size=28)
        row = VGroup(p1, p2).arrange(RIGHT, buff=1.6).move_to(0.6 * UP)
        arr = Arrow(p1.get_right(), p2.get_left(), buff=0.15, fill_color=GREY_B, thickness=4)
        bang = txt("impossible, so no such zero", 30, YELLOW).next_to(row, DOWN, buff=0.6)
        self.play(FadeIn(p1))
        self.cue("builds one sum")
        self.play(GrowArrow(arr), FadeIn(p2))
        self.cue("both large and small")
        self.play(FadeIn(bang))
        self.finish()

        self.recap("5.6", ["No zeros past a line means", "sums that provably cancel."])


# ---------------------------------------------------------------------------
# Chapter 6 — a crowd and a symmetry
# ---------------------------------------------------------------------------

class C6Crowd(Video):
    def construct(self):
        self.chapter(3, "6. How it works: a crowd and a symmetry")
        rng = np.random.default_rng(7)
        n = 40
        base = rng.exponential(0.5, n)
        copies = sorted(rng.choice(np.arange(1, n), 7, replace=False))
        ours = 0
        floor = 1.6 * DOWN
        bw = 0.22

        def bars(h_ours, colored):
            g = VGroup()
            for i in range(n):
                h = h_ours if (i == ours or (colored and i in copies)) else base[i]
                col = ORANGE if (i == ours or (colored and i in copies)) else BLUE_C
                r = Rectangle(width=bw, height=max(h, 0.02)).set_stroke(width=0).set_fill(col, 1)
                r.move_to(floor + np.array([(i - n / 2) * 0.28, max(h, 0.02) / 2, 0]))
                g.add(r)
            return g

        self.narrate("6.1")
        one = bars(0.6, False)[ours]
        q = txt("our sum: how big?", 26, ORANGE).next_to(one, UP, buff=0.3)
        self.play(GrowFromEdge(one, DOWN), FadeIn(q))
        self.finish()

        self.narrate("6.2")
        crowd = bars(0.6, False)
        self.play(FadeOut(q), LaggedStart(*[GrowFromEdge(b, DOWN) for b in crowd[1:]], lag_ratio=0.04), run_time=2.5)
        self.remove(one)
        self.add(crowd)
        fam = txt("a family of related sums", 28, BLUE_C).to_edge(UP, buff=0.9)
        self.play(FadeIn(fam))
        self.finish()

        self.narrate("6.3")
        budget = 0.9
        bl = DashedLine(floor + np.array([-6, budget, 0]), floor + np.array([5.5, budget, 0])).set_stroke(GREEN_C, 3)
        bt = txt("proved bound on the average", 24, GREEN_C).next_to(bl, UP, buff=0.1).align_to(bl, RIGHT)
        self.play(ShowCreation(bl), FadeIn(bt))
        self.finish()

        self.narrate("6.4")
        colored = bars(0.6, True)
        self.play(Transform(crowd, colored))
        cl = txt("copies of our sum", 26, ORANGE).next_to(fam, DOWN, buff=0.25)
        self.play(FadeIn(cl))
        self.finish()

        def avg_line(h_ours, col):
            vals = [h_ours if (i == ours or i in copies) else base[i] for i in range(n)]
            a = float(np.mean(vals))
            return Line(floor + np.array([-6, a, 0]), floor + np.array([5.5, a, 0])).set_stroke(col, 4)

        self.narrate("6.5")
        tall = bars(3.6, True)
        av = avg_line(0.6, GREY_B)
        self.play(ShowCreation(av))
        self.play(Transform(crowd, tall), Transform(av, avg_line(3.6, RED_C)), run_time=2)
        over = txt("average too big", 26, RED_C).next_to(av, UP, buff=0.1).align_to(av, LEFT)
        self.play(FadeIn(over))
        self.finish()

        self.narrate("6.6")
        self.play(Transform(crowd, bars(0.3, True)), Transform(av, avg_line(0.3, GREY_B)), FadeOut(over), run_time=2)
        small = txt("so our sum is small", 28, YELLOW).next_to(cl, DOWN, buff=0.25)
        self.play(FadeIn(small))
        self.finish()
        self.clear_content()

        self.narrate("6.7")
        row = VGroup(*[Square(0.42).set_stroke(BLUE_B, 2).set_fill(BLUE_E, 0.6) for _ in range(16)]).arrange(RIGHT, buff=0.1)
        row.move_to(0.9 * UP)
        rl = txt("a long, hard sum", 26, BLUE_B).next_to(row, UP, buff=0.3)
        self.play(LaggedStart(*[FadeIn(s) for s in row], lag_ratio=0.05), FadeIn(rl))
        self.cue("cubic theta function")
        sym = txt("cubic theta function: a hidden symmetry", 28, YELLOW).next_to(row, DOWN, buff=0.5)
        self.play(FadeIn(sym))
        self.finish()

        self.narrate("6.8")
        rows = [row]
        for m in (8, 4, 2):
            r = VGroup(*[Square(0.42).set_stroke(YELLOW, 2).set_fill(BLUE_E, 0.6) for _ in range(m)]).arrange(RIGHT,
                                                                                                         buff=0.1)
            r.next_to(rows[-1], DOWN, buff=0.35)
            if m == 8:
                r.next_to(sym, DOWN, buff=0.35)
            rows.append(r)
            self.play(TransformFromCopy(rows[-2], r), run_time=1.2)
        self.finish()
        self.clear_content()

        self.narrate("6.9")
        grid = eisenstein_grid().move_to(2.8 * LEFT + 0.3 * UP)
        gl = VGroup(txt("the Eisenstein integers", 30, YELLOW), txt("a + b·ω,  ω a cube root of 1", 26, GREY_A),
                    txt("orange: Eisenstein primes", 24, ORANGE), txt("blue: the six units", 24, BLUE_C))
        gl.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(3.4 * RIGHT + 0.4 * UP)
        self.play(LaggedStart(*[FadeIn(d) for d in grid], lag_ratio=0.004), run_time=2.5)
        self.play(FadeIn(gl))
        self.finish()
        self.clear_content()

        self.narrate("6.10")
        big = card(["an L-function of the Eisenstein integers"], width=8.5, size=30).move_to(1.3 * UP)
        def texcard(tex):
            t = Tex(tex, font_size=44)
            box = RoundedRectangle(width=3.4, height=1.0, corner_radius=0.2).set_stroke(GREY_B, 2)
            return VGroup(box, t.move_to(box))
        f1 = texcard(R"L(s,\chi)")
        f2 = texcard(R"L(s,\chi\chi_{-3})")
        parts = VGroup(f1, f2).arrange(RIGHT, buff=0.8).next_to(big, DOWN, buff=0.9)
        times = Tex(R"\times", font_size=48).move_to(parts)
        eq = Tex("=", font_size=48).next_to(big, DOWN, buff=0.25)
        dl = txt("ordinary Dirichlet L-functions: zeta and its cousins", 26, YELLOW).next_to(parts, DOWN, buff=0.4)
        self.play(FadeIn(big))
        self.play(FadeIn(eq), TransformFromCopy(big, f1), TransformFromCopy(big, f2), FadeIn(times), run_time=2)
        self.cue("So a zero-free line")
        self.play(FadeIn(dl))
        self.finish()
        self.clear_content()

        self.narrate("6.11")
        gauge = NumberLine((0.8, 1.0, 0.05), width=10, include_numbers=False).set_stroke(GREY_B, 3).shift(0.5 * UP)
        gls = VGroup(*[txt(s, 26, GREY_A).next_to(gauge.n2p(v), DOWN, buff=0.25)
                       for v, s in ((0.8, "0.8"), (0.85, "0.85"), (0.9, "0.9"), (0.95, "0.95"), (1.0, "1"))])
        pos = ValueTracker(11 / 12)
        mark = always_redraw(lambda: VGroup(Triangle().scale(0.16).rotate(PI).set_fill(NEW, 1).set_stroke(width=0)
                                            .next_to(gauge.n2p(pos.get_value()), UP, buff=0.05)))
        f12 = txt("11/12", 28, GREY_A).next_to(gauge.n2p(11 / 12), UP, buff=0.55)
        self.play(ShowCreation(gauge), FadeIn(gls))
        self.play(FadeIn(mark), FadeIn(f12))
        self.cue("The second changes")
        f78 = txt("7/8", 32, NEW).next_to(gauge.n2p(7 / 8), UP, buff=0.55)
        self.play(pos.animate.set_value(7 / 8), run_time=2.5)
        self.play(FadeIn(f78))
        self.finish()
        self.remove(mark)

        self.recap("6.12", ["Hide the sum in a crowd; bound the crowd with a symmetry;", "carry it back to zeta."])


# ---------------------------------------------------------------------------
# Chapter 7 — what would follow
# ---------------------------------------------------------------------------

class C7Follow(Video):
    def construct(self):
        self.chapter(3, "7. What would follow")
        self.narrate("7.1")
        first = VGroup(tick(), txt("no Landau–Siegel zeros", 32)).arrange(RIGHT, buff=0.4).move_to(0.6 * UP)
        self.play(FadeIn(first, shift=0.1 * RIGHT))
        self.finish()
        self.play(FadeOut(first))

        self.narrate("7.2")
        ps = [p for p in range(3, 200_000) if IS_P[p]]
        least = [least_nonresidue(p) for p in ps]
        ax = Chart((0.4, 5.4), (0, 40), 8.5, 3.4, xticks=(1, 2, 3, 4, 5), yticks=(0, 20, 40),
                   xfmt=lambda v: Tex(f"10^{{{int(v)}}}", font_size=26).set_color(GREY_B),
                   yfmt=lambda v: txt(str(int(v)), 20, GREY_B),
                   xlabel="prime p (log scale)", ylabel="smallest non-square", grid=False)
        ax.shift(0.5 * UP - ax.box.get_center())
        dots = VGroup(*[Dot(ax.c2p(math.log10(p), q), radius=0.025, fill_color=BLUE_C).set_opacity(0.6)
                        for p, q in list(zip(ps, least))[::40]])
        rec, best = [], 0
        for p, q in zip(ps, least):
            if q > best:
                best = q
                rec.append((p, q))
        rline = VMobject().set_points_as_corners([ax.c2p(math.log10(p), q) for p, q in rec]).set_stroke(ORANGE, 3)
        rl = txt(f"records: never above {best}", 24, ORANGE).next_to(ax.c2p(5.4, best), UL, buff=0.15)
        self.play(FadeIn(ax))
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=2)
        self.play(ShowCreation(rline), FadeIn(rl))
        self.cue("That settles")
        vg = txt("Vinogradov's conjecture", 28, YELLOW).next_to(ax.box, UP, buff=0.15).align_to(ax.box, LEFT)
        self.play(FadeIn(vg))
        self.finish()
        self.clear_content()

        self.narrate("7.3")
        sq = card(["square roots modulo a prime", "fast, with no random guessing"], width=7.5, size=30).move_to(0.6 * UP)
        self.play(FadeIn(sq))
        self.finish()
        self.play(FadeOut(sq))

        self.narrate("7.4")
        ax = Chart((0, 300), (0, 32), 8.5, 3.4, xticks=(0, 100, 200, 300), yticks=(0, 15, 30),
                   xfmt=lambda v: txt(str(int(v)), 20, GREY_B), yfmt=lambda v: txt(str(int(v)), 20, GREY_B),
                   xlabel="x", ylabel="primes up to x", grid=False)
        ax.shift(0.5 * UP - ax.box.get_center())
        xs = list(range(0, 301))
        c1 = np.cumsum([1 if (x >= 2 and IS_P[x] and x % 4 == 1) else 0 for x in xs])
        c3 = np.cumsum([1 if (x >= 2 and IS_P[x] and x % 4 == 3) else 0 for x in xs])
        s1 = staircase(ax, xs, list(c1), color=GREEN_C, width=3)
        s3 = staircase(ax, xs, list(c3), color=PURPLE_B, width=3)
        sm = curve(ax, lambda x: li(x) / 2, 2, 300, n=120, color=SMOOTH, width=4)
        lab = VGroup(txt("remainder 1 mod 4", 22, GREEN_C), txt("remainder 3 mod 4", 22, PURPLE_B),
                     txt("half the smooth curve", 22, SMOOTH)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lab.next_to(ax.c2p(5, 31), DR, buff=0.05)
        self.play(FadeIn(ax), ShowCreation(s1), ShowCreation(s3), run_time=2.5)
        self.play(ShowCreation(sm), FadeIn(lab))
        self.finish()
        self.clear_content()

        self.narrate("7.5")
        nums = VGroup(*[txt(str(v), 22, YELLOW) for v in IDONEAL]).arrange_in_grid(5, 13, buff=(0.28, 0.25))
        nums.move_to(0.7 * UP)
        il = txt("Euler's 65 idoneal numbers: the list is complete", 28, GREEN_C).next_to(nums, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(t) for t in nums], lag_ratio=0.02), run_time=2.5)
        self.play(FadeIn(il))
        self.finish()

        self.recap("7.6", ["One zero-free line,", "and several old results follow."])


# ---------------------------------------------------------------------------
# Chapter 8 — is it right?
# ---------------------------------------------------------------------------

class C8Check(Video):
    def construct(self):
        self.chapter(4, "8. Is it right?")
        self.narrate("8.1")
        lean = card(["Lean 4", "if the real part of s is more than 7/8,", "then zeta of s is not zero"],
                    width=9, size=30).move_to(1.4 * UP)
        self.play(FadeIn(lean))
        self.finish()

        self.narrate("8.2")
        note = VGroup(txt("not re-run by us", 26, GREY_A),
                      txt("it certifies the theorem, not the 199-page written proof", 26, YELLOW))
        note.arrange(DOWN, buff=0.25).next_to(lean, DOWN, buff=0.5)
        self.play(FadeIn(note[0]))
        self.cue("And a computer check")
        self.play(FadeIn(note[1]))
        self.finish()
        self.play(FadeOut(VGroup(lean, note)))

        self.narrate("8.3")
        q = card(["Quanta Magazine, 19 October 2026", "number theorists are working through the proof",
                  "Peter Sarnak is teaching a course on it"], width=9.5, size=28).move_to(0.7 * UP)
        self.play(FadeIn(q))
        self.finish()
        self.play(FadeOut(q))

        self.narrate("8.4")
        people = [("William Banks", "explicit numbers"), ("Bryce Kerr", "a simpler proof"), ("Ben Green", "his own account")]
        cards = VGroup(*[card([a, b], width=3.9, size=26) for a, b in people]).arrange(RIGHT, buff=0.3).move_to(0.9 * UP)
        sub = txt("the related argument about rogue zeros, reworked", 26, GREY_A).next_to(cards, DOWN, buff=0.45)
        for c, phrase in zip(cards, ["William Banks", "Bryce Kerr", "Ben Green"]):
            self.cue(phrase)
            self.play(FadeIn(c, shift=0.1 * UP))
        self.play(FadeIn(sub))
        self.finish()
        self.play(FadeOut(VGroup(cards, sub)))

        self.narrate("8.5")
        st = VGroup(txt("no error reported, as of 4 November 2026", 32, GREEN_C),
                    txt("not yet peer reviewed", 32, GREY_A)).arrange(DOWN, buff=0.4).move_to(0.6 * UP)
        self.play(FadeIn(st[0]))
        self.play(FadeIn(st[1]))
        self.finish()

        self.recap("8.6", ["A computer-checked statement;", "a human reading still under way."])


# ---------------------------------------------------------------------------
# Chapter 9 — what it does not do, and closing
# ---------------------------------------------------------------------------

class C9Close(Video):
    def construct(self):
        self.chapter(4, "9. What it does not do")
        self.narrate("9.1")
        strip = Strip().move_to(2.8 * LEFT + 0.2 * DOWN)
        bands = VGroup(strip.zone(7 / 8, 1, NEW, 0.6), strip.zone(0, 1 / 8, NEW, 0.6))
        self.play(FadeIn(strip), FadeIn(bands))
        self.add(strip.dots)
        rh = txt("Riemann hypothesis:\nevery zero on the line at 1/2\n(still open)", 26, ZERO)
        rh.move_to(3.3 * RIGHT + 0.8 * UP)
        this = txt("this paper: between 1/8 and 7/8", 26, NEW).next_to(rh, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(Indicate(strip.half, color=ZERO), FadeIn(rh))
        self.cue("This keeps them")
        self.play(FadeIn(this))
        self.finish()
        self.clear_content()

        self.narrate("9.2")
        ax = Chart((1, 10_000), (0, 3200), 8.5, 3.4, xticks=(5000, 10_000), yticks=(0, 1500, 3000),
                   xfmt=lambda v: txt(f"{int(v):,}", 20, GREY_B), yfmt=lambda v: txt(f"{int(v):,}", 20, GREY_B),
                   xlabel="x", ylabel="size of the wobble", grid=False)
        ax.shift(0.5 * UP - ax.box.get_center())
        a = curve(ax, lambda x: x ** 0.875, 1, 10_000, color=NEW, width=4)
        b = curve(ax, lambda x: x ** 0.5, 1, 10_000, color=ZERO, width=4)
        al = Tex(R"x^{7/8}", font_size=40).set_color(NEW).next_to(ax.c2p(10_000, 10_000 ** 0.875), LEFT, buff=0.3)
        bl = Tex(R"\sqrt{x}", font_size=40).set_color(ZERO).next_to(ax.c2p(10_000, 100), UP, buff=0.3)
        self.play(FadeIn(ax), ShowCreation(a), FadeIn(al), run_time=2)
        self.cue("still far from")
        self.play(ShowCreation(b), FadeIn(bl))
        self.finish()
        self.clear_content()

        self.narrate("9.3")
        gap = NumberLine((0.5, 0.875, 0.125), width=9, include_numbers=False).set_stroke(GREY_B, 3).shift(0.5 * UP)
        ends = VGroup(txt("1/2", 30, ZERO).next_to(gap.n2p(0.5), DOWN, buff=0.3),
                      txt("7/8", 30, NEW).next_to(gap.n2p(0.875), DOWN, buff=0.3))
        qm = txt("?", 80, YELLOW).next_to(gap, UP, buff=0.3)
        self.play(ShowCreation(gap), FadeIn(ends))
        self.play(FadeIn(qm, scale=1.5))
        self.finish()
        self.clear_content()

        self.narrate("9.4")
        self.play(FadeOut(self.roadmap_mob))
        title = txt("The Quasi-Riemann Hypothesis", 50)
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
        title = txt("The Quasi-Riemann Hypothesis", 58).to_edge(UP, buff=0.6)
        sub = txt("no zeros past 7/8, explained for everyone", 30, GREY_A).next_to(title, DOWN, buff=0.25)
        strip = Strip(width=3.6, height=4.0).move_to(3.6 * LEFT + 0.9 * DOWN)
        bands = VGroup(strip.zone(7 / 8, 1, NEW, 0.6), strip.zone(0, 1 / 8, NEW, 0.6))
        ax = Chart((0, 100), (0, 30), 6.0, 3.2, grid=False)
        ax.shift(2.6 * RIGHT + 0.9 * DOWN - ax.box.get_center())
        xs = list(range(0, 101))
        st = staircase(ax, xs, [int(PI[x]) if x >= 2 else 0 for x in xs])
        sm = curve(ax, li, 2, 100, n=120, color=SMOOTH, width=5)
        self.add(title, sub, strip, bands, strip.dots, ax, st, sm)
