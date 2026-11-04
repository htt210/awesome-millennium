"""Narrated explainer for "Beyond the Square-Root Exponent for Depth-Three Boolean
Circuits" (OpenAI, September 2026), written for 3b1b's manim (manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("2.3") and
the words come from beat 2.3 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl circuits_video.py C2Layers -w -l --config_file ../../../../../tools/video/custom_config.yml

Computed, with the same code as the explainer's figures (../code/make_figures.py):
the 4-bit parity circuit (checked on all inputs), the parity size curve, the
random restriction of a wide CNF, and the paper's language at n = 20480. The
claimed growth curve, the covering picture and the exponent axis are schematics.
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

ONC = GREEN_C      # a gate that outputs 1
OFFC = GREY_D      # a gate that outputs 0
ORC = BLUE_C
ANDC = TEAL_C
TOPC = ORANGE


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["Circuits", "The barrier", "The claim", "How it works", "Is it right?"]
    PRONOUNCE = [(r"\bHåstad\b", "Hoastad"), (r"\b2026\b", "twenty twenty-six")]
    BUILD = HERE / "build"


# ---------------------------------------------------------------------------
# data (shared with the figures)
# ---------------------------------------------------------------------------

CLAUSES, MIDDLE = mf.check_parity()          # 4-bit parity circuit, verified on all 16 inputs
NAMES = ["x₁", "x₂", "x₃", "x₄"]


def parity_curve():
    ns = np.unique(np.round(np.geomspace(16, 40000, 90)).astype(int))
    return [(math.log10(n), math.log2(mf.best_parity_size(int(n))[0]) / math.sqrt(n)) for n in ns]


def restriction_hist(trials=6, seed=3):
    rng = np.random.default_rng(seed)
    hist = np.zeros(21)
    left = []
    for _ in range(trials):
        w = mf.restriction_trial(rng)
        left.append(len(w))
        hist += np.bincount(w, minlength=21)
    return hist / trials, float(np.mean(left))


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def gate(label: str, color, width=1.15, height=0.5, size=22):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.1).set_stroke(color, 2.5)
    box.set_fill(BLACK, 1)
    return VGroup(box, txt(label, size, color).move_to(box))


class ParityCircuit(VGroup):
    """The 4-bit parity circuit: inputs, 8 bottom ORs, 2 middle ANDs, 1 top OR."""

    def __init__(self, width=11.0, y_in=-2.0, y_bot=-0.75, y_mid=0.55, y_top=1.75, literals=True):
        super().__init__()
        xs_in = np.linspace(-width * 0.33, width * 0.33, 4)
        xs_bot = np.linspace(-width / 2 + 0.6, width / 2 - 0.6, len(CLAUSES))
        xs_mid = [-width * 0.2, width * 0.2]
        self.inputs = VGroup(*[txt(n, 30).move_to([x, y_in, 0]) for n, x in zip(NAMES, xs_in)])
        self.bottom = VGroup(*[gate("OR", ORC).move_to([x, y_bot, 0]) for x in xs_bot])
        self.middle = VGroup(*[gate("AND", ANDC, width=1.3).move_to([x, y_mid, 0]) for x in xs_mid])
        self.top = gate("OR", TOPC, width=1.3).move_to([0, y_top, 0])
        self.w_in = VGroup()
        for i, c in enumerate(CLAUSES):
            for v, _ in c:
                self.w_in.add(Line(self.inputs[v].get_top() + 0.05 * UP, self.bottom[i].get_bottom())
                              .set_stroke(GREY_D, 1.5))
        self.w_mid = VGroup()
        for k, g in enumerate(MIDDLE):
            for c in g:
                self.w_mid.add(Line(self.bottom[c].get_top(), self.middle[k].get_bottom()).set_stroke(GREY_C, 2))
        self.w_top = VGroup(*[Line(m.get_top(), self.top.get_bottom()).set_stroke(GREY_B, 2.5) for m in self.middle])
        self.lits = VGroup()
        if literals:
            for i, c in enumerate(CLAUSES):
                s = "∨".join(("" if sign else "¬") + NAMES[v] for v, sign in c)
                self.lits.add(txt(s, 15, GREY_B).next_to(self.bottom[i], DOWN, buff=0.08))
        self.add(self.w_in, self.w_mid, self.w_top, self.inputs, self.bottom, self.middle, self.top, self.lits)

    def values(self, x):
        bot = [any(x[v] == s for v, s in c) for c in CLAUSES]
        mid = [all(bot[c] for c in g) for g in MIDDLE]
        return bot, mid, any(mid)

    def light(self, scene, x, run_time=0.6):
        """Animate the evaluation on input x, layer by layer; returns the input digits."""
        bot, mid, top = self.values(x)
        digits = VGroup(*[txt(str(b), 28, YELLOW).next_to(self.inputs[i], DOWN, buff=0.12)
                          for i, b in enumerate(x)])
        scene.play(FadeIn(digits, shift=0.2 * UP), run_time=run_time)
        scene.play(*[g[0].animate.set_fill(ONC if b else OFFC, 0.85) for g, b in zip(self.bottom, bot)],
                   run_time=run_time)
        scene.play(*[g[0].animate.set_fill(ONC if b else OFFC, 0.85) for g, b in zip(self.middle, mid)],
                   run_time=run_time)
        scene.play(self.top[0].animate.set_fill(ONC if top else OFFC, 0.85), run_time=run_time)
        return digits

    def reset(self):
        return [g[0].animate.set_fill(BLACK, 1) for g in [*self.bottom, *self.middle, self.top]]


def single_gate(kind: str, bits, color, center):
    g = gate(kind, color, width=1.6, height=0.7, size=30).move_to(center)
    ins = VGroup()
    for k, b in enumerate(bits):
        x = center[0] + (k - 1) * 0.6
        start = np.array([x, center[1] - 1.5, 0])
        ln = Line(start, g.get_bottom() + (k - 1) * 0.4 * RIGHT).set_stroke(GREY_B, 2)
        ins.add(VGroup(ln, txt(str(b), 30, YELLOW).next_to(start, DOWN, buff=0.1)))
    out_v = int(all(bits)) if kind == "AND" else int(any(bits))
    out = Line(g.get_top(), g.get_top() + 0.9 * UP).set_stroke(GREY_B, 2)
    ov = txt(str(out_v), 34, ONC if out_v else RED_C).next_to(out, UP, buff=0.1)
    return g, ins, VGroup(out, ov)


def parity_chart(height=3.6, width=8.6):
    ax = Chart((1.2, 4.7), (0, 5.3), width, height, xticks=(2, 3, 4), yticks=(0, 1, 2, 3, 4, 5),
               xfmt=lambda v: txt(f"10^{int(v)}" if v != 2 else "100", 20, GREY_B).set_color(GREY_B),
               yfmt=lambda v: txt(str(int(v)), 20, GREY_B),
               xlabel="number of inputs n", ylabel="log₂(gates) ÷ √n", grid=False)
    pts = parity_curve()
    cv = VMobject().set_points_smoothly([ax.c2p(x, y) for x, y in pts]).set_stroke(BLUE_C, 4)
    one = DashedLine(ax.c2p(1.2, 1), ax.c2p(4.7, 1)).set_stroke(GREY_B, 2)
    return ax, cv, one


def bar_chart_blocks(n=20480, width=12.0, y=0.6):
    d, r, t = mf.params(n)
    blocks = [("data", d, BLUE_C), ("hash bits", d + r - 1, PURPLE_B), ("P", r, ORANGE),
              ("coefficients", t * r, TEAL_C)]
    used = sum(b for _, b, _ in blocks)
    blocks.append(("ignored", n - used, GREY_D))
    grp, labels = VGroup(), VGroup()
    x0 = -width / 2
    for k, (lab, w, col) in enumerate(blocks):
        ww = width * w / n
        rect = Rectangle(width=ww, height=0.7).set_stroke(BLACK, 2).set_fill(col, 0.9)
        rect.move_to([x0 + ww / 2, y, 0])
        grp.add(rect)
        t_ = txt(f"{lab}\n{w:,}", 20, WHITE)
        if lab == "P":
            t_.next_to(rect, DOWN, buff=0.15)
        else:
            t_.next_to(rect, UP, buff=0.15)
        labels.add(t_)
        x0 += ww
    head = txt(f"one input of n = {n:,} bits", 26, GREY_A).next_to(VGroup(grp, labels), UP, buff=0.3)
    return VGroup(grp, labels, head), (d, r, t)


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        circ = ParityCircuit(width=10.5, literals=False).shift(0.3 * UP)
        self.narrate("0.1")
        self.play(FadeIn(circ.inputs), ShowCreation(circ.w_in), FadeIn(circ.bottom), run_time=1.4)
        self.play(ShowCreation(circ.w_mid), FadeIn(circ.middle), ShowCreation(circ.w_top), FadeIn(circ.top))
        self.cue("each computing")
        digits = circ.light(self, [1, 0, 1, 1], run_time=0.5)
        self.finish()

        self.narrate("0.2")
        count = txt("11 gates", 40, YELLOW).move_to(2.0 * UP)
        self.play(FadeOut(VGroup(circ, digits)), FadeIn(count))
        for s in ("11,000 gates", "11,000,000 gates", "11,000,000,000 gates"):
            self.play(Transform(count, txt(s, 40, YELLOW).move_to(2.0 * UP)), run_time=0.5)
        imp = txt("huge circuit  ⇒  no fast program", 40, WHITE).move_to(0.4 * UP)
        self.play(FadeIn(imp, shift=0.2 * UP))
        self.cue("That is one road")
        pnp = txt("one road to P vs NP", 32, GREY_A).next_to(imp, DOWN, buff=0.4)
        self.play(FadeIn(pnp))
        self.finish()

        self.narrate("0.3")
        title = txt("Beyond the Square-Root Exponent", 54)
        sub = txt("OpenAI preprint, September 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(VGroup(count, imp, pnp)), Write(title, run_time=2))
        self.play(FadeIn(sub))
        self.cue("circuits with only three")
        three = txt("for circuits with three layers", 32, YELLOW).next_to(sub, DOWN, buff=0.4)
        self.play(FadeIn(three))
        self.finish()
        self.clear_caption()

        self.narrate("0.4")
        big = self.roadmap(None, big=True).move_to(1.6 * DOWN)
        self.play(VGroup(title, sub, three).animate.shift(UP), FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, three, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — circuits
# ---------------------------------------------------------------------------

class C1Circuits(Video):
    def construct(self):
        self.chapter(0, "1. Circuits")
        self.narrate("1.1")
        g1, i1, o1 = single_gate("AND", [1, 1, 0], ANDC, np.array([-3.2, 0.4, 0]))
        g2, i2, o2 = single_gate("OR", [0, 1, 0], ORC, np.array([3.2, 0.4, 0]))
        self.play(FadeIn(g1), FadeIn(i1))
        self.play(ShowCreation(o1[0]), FadeIn(o1[1], shift=0.2 * UP))
        self.cue("OR outputs")
        self.play(FadeIn(g2), FadeIn(i2))
        self.play(ShowCreation(o2[0]), FadeIn(o2[1], shift=0.2 * UP))
        self.finish()
        self.clear_content()

        self.narrate("1.2")
        circ = ParityCircuit(width=9.0, literals=False).scale(0.8).shift(0.2 * UP + 1.4 * LEFT)
        size = VGroup(txt("size =", 30, YELLOW), txt("number of gates", 30, YELLOW), txt("= 11", 30, YELLOW))
        size.arrange(DOWN, buff=0.2).move_to(5.0 * RIGHT + 0.5 * UP)
        self.play(FadeIn(circ))
        self.play(LaggedStart(*[Indicate(g, scale_factor=1.15) for g in [*circ.bottom, *circ.middle, circ.top]],
                              lag_ratio=0.08), FadeIn(size))
        self.cue("Any fast program")
        prog = card(["fast program  →  circuit,", "not much bigger than its running time"], width=7.5, size=26)
        prog.move_to(2.0 * DOWN)
        self.play(FadeIn(prog))
        self.finish()
        self.clear_content()

        self.narrate("1.3")
        a = txt("a problem needs huge circuits", 34).move_to(1.6 * UP)
        b = txt("⇒  it has no fast program", 34).next_to(a, DOWN, buff=0.4)
        c = txt("if it is in NP  ⇒  P ≠ NP", 36, YELLOW).next_to(b, DOWN, buff=0.6)
        self.play(FadeIn(a))
        self.play(FadeIn(b))
        self.cue("and P would")
        self.play(FadeIn(c, scale=1.1))
        self.finish()
        self.clear_content()

        self.narrate("1.4")
        base = Line(5.5 * LEFT, 5.5 * RIGHT).shift(0.2 * DOWN).set_stroke(GREY_B, 2)
        proven = Rectangle(width=1.0, height=0.5).set_stroke(width=0).set_fill(BLUE_C, 0.9)
        proven.move_to(base.get_left() + 0.5 * RIGHT + 0.25 * UP + 0.0 * DOWN)
        pl = txt("proven: about 3 gates per input bit", 26, BLUE_C).next_to(proven, UP, buff=0.25)
        pl.align_to(proven, LEFT)
        need = Arrow(base.get_left() + 1.2 * DOWN, base.get_right() + 1.2 * DOWN + 0.6 * RIGHT, buff=0)
        need.set_stroke(ORANGE, 5).set_fill(ORANGE)
        nl = txt("needed for P ≠ NP: more than any power of n", 26, ORANGE).next_to(need, DOWN, buff=0.2)
        self.play(ShowCreation(base), GrowFromEdge(proven, LEFT), FadeIn(pl))
        self.cue("the best bound")
        self.play(GrowArrow(need), FadeIn(nl))
        self.finish()

        self.recap("1.5", ["Huge circuits would mean no fast program;", "proving it is hard."])


# ---------------------------------------------------------------------------
# Chapter 2 — three layers
# ---------------------------------------------------------------------------

class C2Layers(Video):
    def construct(self):
        self.chapter(0, "2. Three layers")
        circ = ParityCircuit(width=10.0).shift(0.5 * LEFT + 0.25 * UP)
        tags = VGroup(txt("bottom: OR", 24, ORC).next_to(circ.bottom[-1], RIGHT, buff=0.3),
                      txt("middle: AND", 24, ANDC).next_to(circ.middle[-1], RIGHT, buff=1.6),
                      txt("top: one OR", 24, TOPC).next_to(circ.top, RIGHT, buff=2.4))
        self.narrate("2.1")
        self.play(FadeIn(circ.inputs))
        self.cue("OR gates at the bottom")
        self.play(ShowCreation(circ.w_in), FadeIn(circ.bottom), FadeIn(circ.lits), FadeIn(tags[0]), run_time=1.2)
        self.cue("AND gates in the middle")
        self.play(ShowCreation(circ.w_mid), FadeIn(circ.middle), FadeIn(tags[1]))
        self.cue("and one OR gate")
        self.play(ShowCreation(circ.w_top), FadeIn(circ.top), FadeIn(tags[2]))
        self.finish()

        self.narrate("2.2")
        many = SurroundingRectangle(VGroup(circ.middle[0], *[circ.bottom[c] for c in MIDDLE[0]]), buff=0.15)
        many.set_stroke(YELLOW, 2)
        ml = txt("any number of inputs", 24, YELLOW).next_to(many, UP, buff=0.1).shift(1.5 * LEFT)
        neg = next(i for i, c in enumerate(CLAUSES) if any(not s for _, s in c))
        nl = SurroundingRectangle(circ.lits[neg], buff=0.06).set_stroke(YELLOW, 2)
        free = txt("NOT on an input: free", 24, YELLOW).next_to(circ.inputs, DOWN, buff=0.25)
        self.play(ShowCreation(many), FadeIn(ml))
        self.cue("a NOT on an input")
        self.play(ShowCreation(nl), FadeIn(free))
        self.cue("The question is")
        q = txt("how many gates?", 34, YELLOW).move_to(2.6 * UP + 4.0 * RIGHT)
        self.play(FadeOut(VGroup(many, ml, nl, free)), FadeIn(q))
        self.finish()

        self.narrate("2.3")
        par = txt("parity: is the number of 1s odd?", 28, YELLOW).move_to(2.6 * UP + 3.4 * RIGHT)
        self.play(FadeOut(q), FadeIn(par))
        x = [1, 0, 1, 1]
        digits = circ.light(self, x, run_time=0.5)
        res = txt("three 1s: odd  →  output 1", 24, ONC).next_to(circ.top, LEFT, buff=0.4)
        self.play(FadeIn(res))
        self.cue("with eleven gates")
        checked = all(mf.evaluate(CLAUSES, MIDDLE, [(a >> i) & 1 for i in range(4)]) == bin(a).count("1") % 2
                      for a in range(16))
        note = txt(f"11 gates · {'checked' if checked else 'FAILED'} on all 16 inputs", 26, YELLOW)
        note.move_to(par)
        self.play(FadeOut(par), FadeIn(note))
        self.finish()

        self.recap("2.4", ["Three layers: OR, then AND, then OR.", "Count the gates."])


# ---------------------------------------------------------------------------
# Chapter 3 — the barrier
# ---------------------------------------------------------------------------

class C3Barrier(Video):
    def construct(self):
        self.chapter(1, "3. The barrier")
        ax, cv, one = parity_chart()
        grp = VGroup(ax, cv, one)
        grp.shift(0.45 * UP - ax.box.get_center())
        lab = txt("parity, best block split (computed)", 22, BLUE_C).next_to(ax.c2p(3.0, 1.6), UP, buff=0.05)
        onel = txt("exponent = √n", 20, GREY_B).next_to(ax.c2p(4.7, 1), UL, buff=0.08)
        self.narrate("3.1")
        self.play(FadeIn(ax))
        self.play(ShowCreation(cv), FadeIn(lab), run_time=2)
        self.cue("That takes about")
        self.play(ShowCreation(one), FadeIn(onel))
        self.finish()
        self.play(FadeOut(VGroup(grp, lab, onel)))

        self.narrate("3.2")
        h = card(["1980s, Johan Håstad:", "parity needs about 2^(c·√n) gates", "method: random restrictions"],
                 width=9, size=30).move_to(0.5 * UP)
        self.play(FadeIn(h))
        self.finish()
        self.play(FadeOut(h))

        self.narrate("3.3")
        lines = VGroup()
        for a in (2, 4):
            ln = DashedLine(ax.c2p(1.2, a), ax.c2p(4.7, a)).set_stroke(ORANGE, 2)
            lines.add(VGroup(ln, txt(f"exponent = {a}√n", 20, ORANGE).next_to(ax.c2p(1.25, a), UR, buff=0.06)))
        self.play(FadeIn(VGroup(grp, lab, onel)))
        self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.4))
        self.cue("stayed a constant")
        band = Rectangle(width=ax.box.get_width(), height=ax.c2p(0, 1.6)[1] - ax.c2p(0, 0)[1])
        band.set_stroke(width=0).set_fill(BLUE_E, 0.35).move_to(ax.box.get_bottom(), aligned_edge=DOWN)
        self.play(FadeIn(band))
        self.finish()
        self.play(FadeOut(VGroup(grp, lab, onel, lines, band)))

        self.narrate("3.4")
        q = card(["one explicit function needing more than", "2^(A·√n) gates, for every constant A?"],
                 width=10, size=32, title="The open question").move_to(0.5 * UP)
        self.play(FadeIn(q))
        self.finish()

        self.recap("3.5", ["For decades, the exponent stayed", "at a constant times √n."])


# ---------------------------------------------------------------------------
# Chapter 4 — the claim
# ---------------------------------------------------------------------------

class C4Claim(Video):
    def construct(self):
        self.chapter(2, "4. The claim")
        self.narrate("4.1")
        c = card(["one fixed problem,", "solved by a fast program"], width=8, size=34).move_to(0.6 * UP)
        self.play(FadeIn(c))
        self.finish()
        self.play(FadeOut(c))

        self.narrate("4.2")
        ax, cv, one = parity_chart()
        grp = VGroup(ax, cv, one)
        grp.shift(0.45 * UP - ax.box.get_center())
        lines = VGroup(*[DashedLine(ax.c2p(1.2, a), ax.c2p(4.7, a)).set_stroke(ORANGE, 2) for a in (2, 4)])
        claim = curve(ax, lambda x: 1.1 + 0.55 * (x - 1.2) ** 2.2, 1.2, 4.7, color=YELLOW, width=5, ylim=(0, 5.25))
        cl = txt("claimed (schematic): above every line, eventually", 22, YELLOW).next_to(ax.c2p(1.3, 4.6), RIGHT,
                                                                                         buff=0.05)
        self.play(FadeIn(grp), FadeIn(lines))
        self.play(ShowCreation(claim), FadeIn(cl), run_time=2.5)
        self.finish()
        self.play(FadeOut(VGroup(grp, lines, claim, cl)))

        self.narrate("4.3")
        bar, (d, r, t) = bar_chart_blocks()
        bar.move_to(0.6 * UP)
        self.play(FadeIn(bar[2]), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar[0]], lag_ratio=0.3),
                  FadeIn(bar[1], lag_ratio=0.3), run_time=2)
        self.cue("The program hashes")
        steps = txt("hash the data  →  evaluate the polynomial  →  read one bit", 26, YELLOW)
        steps.next_to(bar, DOWN, buff=0.6)
        self.play(FadeIn(steps))
        self.finish()
        self.play(FadeOut(VGroup(bar, steps)))

        self.narrate("4.4")
        (_, _, _), rates = mf.language_rates()
        hx = Chart((0.3, len(rates) + 0.7), (0, 1), 9.0, 3.2, xticks=tuple(range(1, len(rates) + 1)),
                   yticks=(0, 0.5, 1), xfmt=lambda v: txt(str(int(v)), 18, GREY_B),
                   yfmt=lambda v: txt(f"{v:.1f}", 18, GREY_B), xlabel="random slice", ylabel="fraction accepted",
                   grid=False)
        hx.shift(0.5 * UP - hx.box.get_center())
        bars = VGroup()
        for k, v in enumerate(rates, start=1):
            lo, hi = hx.c2p(k - 0.3, 0), hx.c2p(k + 0.3, v)
            bars.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1]).set_stroke(width=0)
                     .set_fill(BLUE_C, 0.9).move_to((lo + hi) / 2))
        half = DashedLine(hx.c2p(0.3, 0.5), hx.c2p(len(rates) + 0.7, 0.5)).set_stroke(GREY_A, 2)
        info = txt(f"n = 20,480 · d = {d:,} · r = {r} · t = {t}", 22, GREY_A).next_to(hx.box, UP, buff=0.25)
        self.play(FadeIn(hx), FadeIn(info))
        self.cue("Fixing the extra")
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), run_time=2)
        self.play(ShowCreation(half))
        self.finish()

        self.narrate("4.5")
        pick = bars[5]
        glow = SurroundingRectangle(pick, buff=0.08).set_stroke(YELLOW, 4)
        hard = txt("some slice is hard; the program never has to find it", 26, YELLOW)
        hard.next_to(hx.box, UP, buff=0.25)
        self.play(FadeOut(info), FadeIn(hard), ShowCreation(glow),
                  *[b.animate.set_fill(opacity=0.3) for b in bars if b is not pick])
        self.finish()

        self.recap("4.6", ["Claimed: one fast-to-compute function", "beats every constant A."])


# ---------------------------------------------------------------------------
# Chapter 5 — how it works
# ---------------------------------------------------------------------------

class C5How(Video):
    def construct(self):
        self.chapter(3, "5. How it works")
        self.narrate("5.1")
        top = gate("OR", TOPC, width=1.4).move_to(1.9 * UP)
        mids = VGroup(*[gate("AND", ANDC, width=1.4) for _ in range(4)]).arrange(RIGHT, buff=1.4).move_to(0.2 * UP)
        wires = VGroup(*[Line(m.get_top(), top.get_bottom()).set_stroke(GREY_B, 2) for m in mids])
        notes = VGroup(*[txt("accepts only\nyes-inputs", 20, GREY_A).next_to(m, DOWN, buff=0.25) for m in mids])
        self.play(FadeIn(top), FadeIn(mids), ShowCreation(wires))
        self.cue("so every middle")
        self.play(LaggedStart(*[FadeIn(n_) for n_ in notes], lag_ratio=0.2))
        self.finish()
        self.clear_content()

        self.narrate("5.2")
        sq = Square(side_length=4.0).set_stroke(GREY_B, 2).move_to(0.4 * UP)
        yes = Rectangle(width=4.0, height=1.0).set_stroke(width=0).set_fill(GREEN_E, 0.7)
        yes.move_to(sq.get_bottom(), aligned_edge=DOWN)
        sl = txt("all inputs", 22, GREY_A).next_to(sq, UP, buff=0.15)
        yl = txt("yes-inputs: at least ¼", 22, GREEN_C).next_to(sq, RIGHT, buff=0.3).align_to(yes, DOWN)
        self.play(ShowCreation(sq), FadeIn(sl))
        self.play(FadeIn(yes), FadeIn(yl))
        rng = np.random.default_rng(5)
        patches = VGroup()
        for _ in range(40):
            s = Square(side_length=0.16).set_stroke(YELLOW, 1).set_fill(YELLOW, 0.6)
            p = yes.get_corner(DL) + np.array([rng.uniform(0.1, 3.9), rng.uniform(0.1, 0.9), 0])
            patches.add(s.move_to(p))
        pl = txt("each middle gate: a tiny patch", 22, YELLOW).next_to(sq, LEFT, buff=0.3)
        self.cue("it takes very many")
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in patches], lag_ratio=0.05), FadeIn(pl), run_time=2.5)
        self.finish()
        self.clear_content()

        self.narrate("5.3")
        hist, left = restriction_hist()
        before = Chart((15, 25), (0, 1.1e6), 3.0, 3.0, xticks=(20,), yticks=(0, 1e6),
                       xfmt=lambda v: txt(str(int(v)), 18, GREY_B),
                       yfmt=lambda v: txt("0" if v == 0 else "1,000,000", 18, GREY_B), xlabel="clause width",
                       grid=False)
        before.move_to(3.8 * LEFT + 0.4 * UP)
        lo, hi = before.c2p(19.3, 0), before.c2p(20.7, 1e6)
        bbar = Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1]).set_stroke(width=0).set_fill(GREY_B, 0.9)
        bbar.move_to((lo + hi) / 2)
        bt = txt("before: 1,000,000 clauses", 22, GREY_A).next_to(before.box, UP, buff=0.2)
        after = Chart((-0.5, 20.5), (0, 2.5), 6.0, 3.0, xticks=(0, 5, 10, 15, 20), yticks=(0, 1, 2),
                      xfmt=lambda v: txt(str(int(v)), 18, GREY_B), yfmt=lambda v: txt(str(int(v)), 18, GREY_B),
                      xlabel="clause width", grid=False)
        after.move_to(2.9 * RIGHT + 0.4 * UP)
        abars = VGroup()
        for w, c in enumerate(hist):
            if c <= 0:
                continue
            lo, hi = after.c2p(w - 0.35, 0), after.c2p(w + 0.35, c)
            abars.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1]).set_stroke(width=0)
                      .set_fill(BLUE_C, 0.9).move_to((lo + hi) / 2))
        at = txt(f"after: about {left:.0f} clauses left (computed)", 22, BLUE_C).next_to(after.box, UP, buff=0.2)
        arrow = Arrow(before.box.get_right() + 0.2 * RIGHT, after.box.get_left() + 0.5 * LEFT, buff=0.1)
        arrow.set_stroke(YELLOW, 4).set_fill(YELLOW)
        rl = txt("restrict", 22, YELLOW).next_to(arrow, UP, buff=0.1)
        self.play(FadeIn(before), GrowFromEdge(bbar, DOWN), FadeIn(bt))
        self.cue("Most clauses vanish")
        self.play(GrowArrow(arrow), FadeIn(rl))
        self.play(FadeIn(after), LaggedStart(*[GrowFromEdge(b, DOWN) for b in abars], lag_ratio=0.1), FadeIn(at))
        self.finish()
        self.clear_content()

        self.narrate("5.4")
        wide = card(["wide formula"], width=3.4, size=30).move_to(4.3 * LEFT + 0.6 * UP)
        eq = txt("=", 44).next_to(wide, RIGHT, buff=0.35)
        terms = VGroup()
        for k, (w, s) in enumerate([("0.9", "+"), ("0.6", "−"), ("0.3", "+")]):
            terms.add(VGroup(txt(f"{s} {w} ×", 28, YELLOW), card(["narrow"], width=1.9, size=26)).arrange(RIGHT, buff=0.15))
        terms.add(txt("+ …", 30, YELLOW))
        terms.arrange(RIGHT, buff=0.25).next_to(eq, RIGHT, buff=0.35)
        note = txt("total weight ≤ 2 on average, however many clauses", 28, YELLOW).move_to(1.3 * DOWN)
        lemma = txt("the new restriction lemma", 26, GREY_A).move_to(2.2 * UP)
        self.play(FadeIn(lemma), FadeIn(wide), FadeIn(eq))
        self.play(LaggedStart(*[FadeIn(t_) for t_ in terms], lag_ratio=0.25))
        self.cue("with total weight")
        self.play(FadeIn(note))
        self.finish()
        self.clear_content()

        self.narrate("5.5")
        narrow = card(["one narrow formula"], width=4.0, size=28).move_to(4.0 * LEFT + 0.6 * UP)
        pieces = VGroup(*[card([f"piece {k}"], width=1.7, size=22) for k in range(1, 5)])
        pieces.arrange(DOWN, buff=0.15).move_to(0.2 * RIGHT + 0.6 * UP)
        arrows = VGroup(*[Arrow(narrow.get_right(), p.get_left(), buff=0.1).set_stroke(GREY_B, 2) for p in pieces])
        check = card(["checked all at once", "against a random slice"], width=4.2, size=24).move_to(4.4 * RIGHT + 0.6 * UP)
        a2 = Arrow(pieces.get_right(), check.get_left(), buff=0.15).set_stroke(YELLOW, 4).set_fill(YELLOW)
        sp = txt("sparsification", 24, GREY_A).next_to(arrows, UP, buff=0.4)
        self.play(FadeIn(narrow))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(pieces, lag_ratio=0.2),
                  FadeIn(sp))
        self.cue("There are few enough")
        self.play(GrowArrow(a2), FadeIn(check))
        self.finish()

        self.recap("5.6", ["Restrict, simplify,", "then count the gates."])


# ---------------------------------------------------------------------------
# Chapter 6 — is it right?
# ---------------------------------------------------------------------------

class C6Close(Video):
    def construct(self):
        self.chapter(4, "6. Is it right?")
        self.narrate("6.1")
        lean = card(["Lean 4: the main theorem, formalized"], width=9, size=30).move_to(1.0 * UP)
        nr = txt("not re-run by us", 24, GREY_A).next_to(lean, DOWN, buff=0.3)
        self.play(FadeIn(lean))
        self.cue("We have not")
        self.play(FadeIn(nr))
        self.finish()
        self.play(FadeOut(VGroup(lean, nr)))

        self.narrate("6.2")
        fu = card(["October 2026: a follow-up report", "extends it to every fixed depth"], width=9, size=28)
        fu.move_to(1.0 * UP)
        src = txt("(from search results)", 22, GREY_A).next_to(fu, DOWN, buff=0.25)
        nv = txt("no expert assessment found yet", 26, ORANGE).next_to(src, DOWN, buff=0.3)
        self.play(FadeIn(fu), FadeIn(src))
        self.cue("We found no")
        self.play(FadeIn(nv))
        self.finish()
        self.play(FadeOut(VGroup(fu, src, nv)))

        self.narrate("6.3")
        pnp = txt("P vs NP ?", 72, YELLOW).move_to(1.0 * UP)
        op = txt("still open · three layers are a weak model", 28, GREY_A).next_to(pnp, DOWN, buff=0.4)
        self.play(FadeIn(pnp, scale=1.2))
        self.play(FadeIn(op))
        self.finish()
        self.play(FadeOut(VGroup(pnp, op)))

        self.narrate("6.4")
        axis = Arrow(5.8 * LEFT, 5.8 * RIGHT, buff=0).shift(0.3 * DOWN).set_stroke(GREY_B, 3).set_fill(GREY_B)
        al = txt("exponent of the gate count (schematic)", 22, GREY_A).next_to(axis, DOWN, buff=0.3)
        marks = VGroup()
        for x, lab, col in [(-4.6, "c·√n\n1980s", BLUE_C), (-2.8, "beyond every A·√n\nclaimed, 2026", YELLOW),
                            (4.4, "n ÷ log log n\nValiant's target", ORANGE)]:
            tick = Line(UP * 0.2, DOWN * 0.2).set_stroke(col, 4).move_to(axis.get_center() + x * RIGHT)
            marks.add(VGroup(tick, txt(lab, 22, col).next_to(tick, UP, buff=0.2)))
        self.play(GrowArrow(axis), FadeIn(al))
        self.play(FadeIn(marks[0]), FadeIn(marks[1]))
        self.cue("Leslie Valiant")
        self.play(FadeIn(marks[2]))
        self.finish()
        self.play(FadeOut(VGroup(axis, al, marks)))

        self.narrate("6.5")
        self.play(FadeOut(self.roadmap_mob))
        title = txt("Beyond the Square-Root Exponent", 50)
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
        title = txt("Beyond the Square-Root Exponent", 56).to_edge(UP, buff=0.6)
        sub = txt("a new lower bound for three-layer circuits, explained for everyone", 28, GREY_A)
        sub.next_to(title, DOWN, buff=0.25)
        circ = ParityCircuit(width=10.0, literals=False).scale(0.75).shift(1.2 * DOWN)
        self.add(title, sub, circ)
