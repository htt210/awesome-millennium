"""3Blue1Brown-style explainer for "The Exponential Time Hypothesis is False"
(OpenAI, October 2026), written for 3b1b's manim (manimgl 1.7.2).

Render everything with ./render.sh, or one scene with
    manimgl eth_video.py S4Separation -w --hd --config_file custom_config.yml

Each scene burns its narration in as captions and logs their timings to
build/captions/<Scene>.json, which render.sh turns into captions.srt,
script.md and, with NARRATION_VOICES set, the voiced videos: every caption has
a `say` text written for the ear, and the scenes wait for the voices.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from manimlib import *

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from captions_util import plain, wrap_caption  # noqa: E402
from voice import voices_from_env  # noqa: E402
CAPTION_DIR = HERE / "build" / "captions"
VOICE_DIR = HERE / "build" / "voice"

SERIF = "CMU Serif"
X_COLOR = BLUE          # variables / assignments
CLAUSE_COLOR = YELLOW   # clauses
T_COLOR = TEAL          # deformation parameter
Y_COLOR = GREEN         # measurements
BAD = RED
GROUP_COLORS = [BLUE_D, PURPLE_B, TEAL_D]

# The example deformation polynomial from code/toy_eth.py (seed 4, n = 6,
# r = 2, Q = 3, R = 2): H(T) = 14 + T/3 - 38T^2/9 + 65T^3/18 - T^4/3 - T^5/6.
H_COEFFS = [14, 1 / 3, -38 / 9, 65 / 18, -1 / 3, -1 / 6]


def poly_eval(coeffs, x):
    return sum(c * x**k for k, c in enumerate(coeffs))


def taylor_at(coeffs, t, J):
    return [sum(c * math.comb(k, i) * t ** (k - i) for k, c in enumerate(coeffs) if k >= i)
            for i in range(J)]


class Narrated(Scene):
    """A scene with burned-in captions and logged caption timings. With narration
    voices, each caption stays up until the slowest voice has read its `say` text."""

    caption_size = 32
    min_read = 1.6
    chars_per_second = 14.0
    voice_lead = 0.25   # the voice starts this long after the caption starts fading in
    voice_gap = 0.45    # silence after the voice before the next caption

    def setup(self):
        super().setup()
        self.caption_mob = None
        self.caption_text = None
        self.caption_say = None
        self.caption_start = 0.0
        self.caption_log = []
        # NARRATION_VOICES (voice.py); unset, the video is silent and paced for reading
        self.voices = voices_from_env(VOICE_DIR)

    def caption(self, text: str, say: str | None = None, run_time: float = 0.5):
        if self.voices:
            self._finish_voice()
        old = self._close_caption()
        body = TexText(wrap_caption(text), font_size=self.caption_size, alignment=R"\centering")
        body.set_max_width(13.2)
        body.to_edge(DOWN, buff=0.32)
        box = BackgroundRectangle(body, fill_opacity=0.75, buff=0.14)
        mob = VGroup(box, body)
        mob.fix_in_frame()
        anims = [FadeIn(mob, run_time=run_time)]
        if old is not None:
            anims.append(FadeOut(old, run_time=run_time))
        self.play(*anims)
        self.caption_mob, self.caption_text, self.caption_start = mob, text, self.time - run_time
        self.caption_say = say or plain(text)

    def _need(self) -> float:
        """How long the current caption must stay up: until the slowest voice is done, or
        long enough to read it."""
        if self.voices:
            return self.voice_lead + max(v.duration(self.caption_say) for v in self.voices.values()) + self.voice_gap
        return self.min_read + len(plain(self.caption_text or "")) / self.chars_per_second

    def hold(self, extra: float = 0.0):
        """Wait until the current caption has been on screen long enough."""
        left = self._need() - (self.time - self.caption_start)
        self.wait(max(0.4, left) + extra)

    def _finish_voice(self):
        if self.caption_mob is not None:
            left = self._need() - (self.time - self.caption_start)
            if left > 0:
                self.wait(left)

    def _close_caption(self):
        old = self.caption_mob
        if old is not None:
            self.caption_log.append({"start": round(self.caption_start, 3), "end": round(self.time, 3),
                                     "text": self.caption_text, "say": self.caption_say})
        self.caption_mob = None
        return old

    def clear_caption(self):
        if self.voices:
            self._finish_voice()
        old = self._close_caption()
        if old is not None:
            self.play(FadeOut(old, run_time=0.4))

    def tear_down(self):
        self._close_caption()
        CAPTION_DIR.mkdir(parents=True, exist_ok=True)
        data = {"scene": type(self).__name__, "duration": round(self.time, 3), "voice_lead": self.voice_lead,
                "voices": sorted(self.voices), "captions": self.caption_log}
        (CAPTION_DIR / f"{type(self).__name__}.json").write_text(json.dumps(data, indent=1))
        super().tear_down()

    # small helpers -------------------------------------------------------
    def heading(self, text: str) -> Text:
        h = Text(text, font=SERIF, font_size=46)
        h.to_edge(UP, buff=0.35)
        return h


# ---------------------------------------------------------------------------
# Scene 1 — the hook
# ---------------------------------------------------------------------------

class S1Hook(Narrated):
    def construct(self):
        title = Text("The Exponential Time Hypothesis\nis False", font=SERIF, font_size=72,
                     t2c={"False": RED})
        sub = Text("an explainer of OpenAI's October 2026 preprint", font=SERIF, font_size=34)
        sub.set_color(GREY_A)
        sub.next_to(title, DOWN, buff=0.6)
        self.play(Write(title, run_time=2.2))
        self.play(FadeIn(sub, shift=0.3 * UP))
        self.caption(R"On 26 October 2026, OpenAI posted a preprint with a startling title.",
                     say="On October twenty-sixth, twenty twenty-six, OpenAI posted a preprint with a startling title.")
        self.hold()
        self.play(FadeOut(VGroup(title, sub)))

        # a 3-CNF formula
        formula = Tex(
            R"F=(x_1\lor\lnot x_2\lor x_3)\land(\lnot x_1\lor x_4\lor x_5)\land(x_2\lor\lnot x_3\lor\lnot x_5)"
            R"\land(\lnot x_2\lor\lnot x_4\lor x_5)",
            font_size=36,
        )
        formula.to_edge(UP, buff=1.1)
        self.caption(R"A 3-CNF formula is an AND of clauses; each clause is an OR of three literals.",
                     say="A three C N F formula is an and of clauses; each clause is an or of three literals.")
        self.play(Write(formula, run_time=2.5))
        self.hold()

        # an assignment, and clauses lighting up
        clauses = [(1, 0, 1), (0, 1, 1), (1, 0, 0), (0, 0, 1)]  # polarity per literal
        lits = [((1, 2, 3)), (1, 4, 5), (2, 3, 5), (2, 4, 5)]
        boxes = VGroup()
        for i in range(5):
            sq = Square(0.62).set_stroke(X_COLOR, 2)
            lab = Tex(f"x_{i + 1}", font_size=32).next_to(sq, UP, buff=0.12)
            boxes.add(VGroup(sq, lab))
        boxes.arrange(RIGHT, buff=0.35).next_to(formula, DOWN, buff=1.0)
        bits = VGroup(*(Integer(0, font_size=36).move_to(b[0]) for b in boxes))
        cl_marks = VGroup()
        for k in range(4):
            c = Circle(radius=0.28).set_stroke(GREY_B, 3)
            t = Tex(f"C_{k + 1}", font_size=30).move_to(c)
            cl_marks.add(VGroup(c, t))
        cl_marks.arrange(RIGHT, buff=0.5).next_to(boxes, DOWN, buff=0.8)
        self.caption(R"3-SAT asks: can we set the $n$ variables to 0 or 1 so that every clause is true?",
                     say="Three-sat asks: can we set the n variables to zero or one, so that every clause is true?")
        self.play(FadeIn(boxes, lag_ratio=0.1), FadeIn(bits), FadeIn(cl_marks, lag_ratio=0.1))

        def status(assign):
            out = []
            for (pol, ids) in zip(clauses, lits):
                out.append(any(assign[i - 1] == p for p, i in zip(pol, ids)))
            return out

        for assign in [(1, 1, 1, 1, 0), (1, 0, 1, 0, 1), (1, 0, 1, 1, 0)]:  # the last one satisfies F
            anims = []
            for b, v in zip(bits, assign):
                new = Integer(v, font_size=36).move_to(b)
                anims.append(Transform(b, new))
            ok = status(assign)
            for mark, good in zip(cl_marks, ok):
                anims.append(mark[0].animate.set_stroke(GREEN if good else BAD, 4))
            self.play(*anims, run_time=0.7)
            self.wait(0.5)
        assert all(status(assign))
        check = Tex(R"\checkmark", font_size=60, color=GREEN).next_to(cl_marks, RIGHT, buff=0.5)
        self.play(Write(check))
        self.hold()
        self.play(FadeOut(VGroup(formula, boxes, bits, cl_marks, check)))

        # brute force: 2^n squares
        self.caption(R"The obvious method tries all $2^n$ assignments. Every new variable doubles the work.",
                     say="The obvious method tries all two to the n assignments. Every new variable doubles the work.")
        grid = VGroup(*(Square(0.17).set_stroke(width=0).set_fill(GREY_D, 1) for _ in range(1024)))
        grid.arrange_in_grid(16, 64, buff=0.04).move_to(0.4 * UP)
        label = Tex(R"2^{10}=1024", font_size=44).next_to(grid, UP, buff=0.4)
        self.play(FadeIn(grid, lag_ratio=0.002, run_time=1.5), Write(label))
        self.play(LaggedStart(*(sq.animate.set_fill(X_COLOR, 1) for sq in grid), lag_ratio=0.002, run_time=3))
        self.hold()
        self.play(FadeOut(VGroup(grid, label)))

        # progress of bases
        self.caption(R"Decades of clever algorithms lowered the base, from $2^n$ to about $1.307^n$ \dots\ but every one of them is still exponential.",
                     say="Decades of clever algorithms lowered the base, from two to the n, to about one point three zero seven to the n. But every one of them is still exponential.")
        line = NumberLine((1, 2.05, 0.25), width=11, include_numbers=False)
        line.move_to(0.6 * UP)
        ends = VGroup(Tex("1", font_size=32).next_to(line.n2p(1), DOWN, buff=0.25),
                      Tex("2", font_size=32).next_to(line.n2p(2), DOWN, buff=0.25))
        self.play(ShowCreation(line), FadeIn(ends))
        brute = VGroup(Dot(line.n2p(2.0), radius=0.09, fill_color=YELLOW))
        brute.add(Tex(R"2^n", font_size=36).next_to(brute[0], UP, buff=0.3))
        brute.add(Text("brute force", font=SERIF, font_size=24, color=GREY_A).next_to(ends[1], DOWN, buff=0.15))
        self.play(FadeIn(brute, shift=0.2 * DOWN))
        cluster = VGroup(*(Dot(line.n2p(b), radius=0.08, fill_color=YELLOW) for b in (4 / 3, 1.307)))
        brace = Brace(cluster, UP, buff=0.25)
        btex = brace.get_tex(R"1.307^n \ \dots\ 1.334^n", font_size=34)
        who = Text("Schöning 1999 · PPSZ family 2014–2026", font=SERIF, font_size=24, color=GREY_A)
        who.next_to(cluster, DOWN, buff=0.75)
        self.play(FadeIn(cluster), GrowFromCenter(brace), FadeIn(btex), FadeIn(who))
        dots = VGroup(brute, cluster, brace, btex, who, ends)
        wall = Line(line.n2p(1.0) + 1.5 * UP, line.n2p(1.0) + 1.5 * DOWN, color=BAD, stroke_width=5)
        wall_label = Tex(R"\text{base } 1", font_size=32, color=BAD).next_to(wall, UP, buff=0.1)
        self.play(ShowCreation(wall), FadeIn(wall_label))
        self.hold()

        self.caption(R"The Exponential Time Hypothesis (Impagliazzo--Paturi, 2001) says this is unavoidable.",
                     say="The Exponential Time Hypothesis, posed by Impagliazzo and Pa-toori in two thousand one, says this is unavoidable.")
        eth = Tex(R"\text{ETH:}\quad \exists\, c>0:\ \text{3-SAT needs } 2^{cn} \text{ time}", font_size=46)
        eth.next_to(line, DOWN, buff=1.6)
        self.play(Write(eth))
        self.hold()
        self.play(FadeOut(VGroup(line, dots, wall, wall_label)), eth.animate.to_edge(UP, buff=0.9))

        thm = Tex(
            R"\#F \text{ in time } (n+m)^{O(1)}\, 2^{O\left(n\log\log n/\sqrt{\log n}\right)}",
            font_size=54, t2c={R"\#F": CLAUSE_COLOR},
        )
        thm.move_to(0.3 * UP)
        box = SurroundingRectangle(thm, buff=0.3, color=YELLOW)
        self.caption(R"The preprint claims a deterministic algorithm that \emph{counts} the solutions of any 3-CNF in subexponential time and polynomial space.",
                     say="The preprint claims a deterministic algorithm that counts the solutions of any three C N F in subexponential time, and polynomial space.")
        self.play(Write(thm), ShowCreation(box))
        cross = Cross(eth, stroke_width=6)
        self.play(ShowCreation(cross))
        self.hold()

        self.caption(R"That is not $\mathsf{P}=\mathsf{NP}$: a time like $2^{n/\sqrt{\log n}}$ still grows faster than every polynomial.",
                     say="That is not P equals NP: a time like two to the n over the square root of log n still grows faster than every polynomial.")
        cmp = Tex(R"n^{100} \ \ll\ 2^{n/\sqrt{\log n}} \ \ll\ 2^{0.01n}", font_size=48).next_to(box, DOWN, buff=0.9)
        self.play(FadeIn(cmp, shift=0.3 * UP))
        self.hold()
        self.clear_caption()
        self.play(FadeOut(VGroup(eth, cross, thm, box, cmp)))


# ---------------------------------------------------------------------------
# Scene 2 — counting as a polynomial
# ---------------------------------------------------------------------------

class S2Polynomial(Narrated):
    def construct(self):
        head = self.heading("Counting is a polynomial sum")
        self.play(Write(head))
        clause = Tex(R"x_a \lor \lnot x_b \lor x_c", font_size=56).shift(1.9 * UP + 3 * LEFT)
        arrow = Arrow(clause.get_right(), clause.get_right() + 1.6 * RIGHT, buff=0.2)
        phi = Tex(R"\Phi_e = 1-(1-X_a)\,X_b\,(1-X_c)", font_size=52,
                  t2c={R"\Phi_e": CLAUSE_COLOR}).next_to(arrow, RIGHT, buff=0.2)
        self.caption(R"Turn each clause into a polynomial $\Phi_e$: it is 1 when the clause is true and 0 when it is false.",
                     say="Turn each clause into a polynomial, Phi e: it is one when the clause is true, and zero when it is false.")
        self.play(Write(clause))
        self.play(GrowArrow(arrow), Write(phi))
        self.hold()

        # truth table
        rows = VGroup()
        header = VGroup(*(Tex(s, font_size=34) for s in ("x_a", "x_b", "x_c", R"\Phi_e")))
        rows.add(header)
        for a, b, c in [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]:
            val = 1 - (1 - a) * b * (1 - c)
            row = VGroup(*(Integer(v, font_size=34) for v in (a, b, c, val)))
            if val == 0:
                row.set_color(BAD)
            rows.add(row)
        for row in rows:
            for k, m in enumerate(row):
                m.move_to(np.array([-1.5 + 1.0 * k, 0, 0]))
        rows.arrange(DOWN, buff=0.16).next_to(clause, DOWN, buff=0.5).shift(0.4 * RIGHT)
        sep = Line(rows[0].get_corner(DL) + 0.1 * DOWN + 0.2 * LEFT, rows[0].get_corner(DR) + 0.1 * DOWN + 0.2 * RIGHT,
                   stroke_width=2, color=GREY_B)
        self.caption(R"The product $(1-X_a)X_b(1-X_c)$ equals 1 only on the single violating assignment $(0,1,0)$.",
                     say="The product, one minus X a, times X b, times one minus X c, equals one only on the single violating assignment: zero, one, zero.")
        self.play(FadeIn(rows, lag_ratio=0.08), ShowCreation(sep))
        self.play(FlashAround(rows[3], color=BAD))
        self.hold()
        self.play(FadeOut(VGroup(rows, sep)))

        count = Tex(R"\#F = \sum_{x\in\lbrace 0,1\rbrace^n} \prod_{e} \Phi_e(x)", font_size=64,
                    t2c={R"\Phi_e": CLAUSE_COLOR, R"\#F": CLAUSE_COLOR})
        count.move_to(0.4 * DOWN + 2.0 * LEFT)
        self.caption(R"Multiply over all clauses and add over all $2^n$ assignments: the result is the number of solutions, $\#F$.",
                     say="Multiply over all clauses, and add over all two to the n assignments: the result is the number of solutions, sharp F.")
        self.play(Write(count, run_time=2))
        self.hold()
        brace = Brace(count[R"\sum_{x\in\lbrace 0,1\rbrace^n}"], DOWN)
        btxt = brace.get_tex(R"2^n \text{ terms: still brute force}", font_size=36)
        self.play(GrowFromCenter(brace), FadeIn(btxt))
        self.hold(0.5)

        self.caption(R"The paper first treats formulas where every variable occurs in at most 3 clauses; then $\prod_e \Phi_e$ has degree at most $3n$.",
                     say="The paper first treats formulas where every variable occurs in at most three clauses; then the product of the Phi's has degree at most three n.")
        deg = Tex(R"\deg \prod_e \Phi_e \ \le\  3n", font_size=50).next_to(count, RIGHT, buff=1.0)
        self.play(FadeIn(deg, shift=0.3 * DOWN))
        self.hold()
        self.caption(R"(General $k$-CNF formulas are reduced to this case at the end.) The question is how to evaluate the sum faster.",
                     say="General k C N F formulas are reduced to this case at the end. The question is how to evaluate the sum faster.")
        self.hold()
        self.clear_caption()
        self.play(FadeOut(VGroup(head, clause, arrow, phi, count, brace, btxt, deg)))


# ---------------------------------------------------------------------------
# Scene 3 — the dream: independent groups
# ---------------------------------------------------------------------------

class S3Groups(Narrated):
    def construct(self):
        head = self.heading("The dream: independent groups")
        self.play(Write(head))
        r, per = 3, 4
        cols = VGroup()
        for g in range(r):
            dots = VGroup(*(Dot(radius=0.11, fill_color=GROUP_COLORS[g]) for _ in range(per)))
            dots.arrange(DOWN, buff=0.5)
            cols.add(dots)
        cols.arrange(RIGHT, buff=3.2).shift(0.75 * UP)
        frames = VGroup(*(SurroundingRectangle(c, buff=0.45).set_stroke(GROUP_COLORS[g], 2)
                          for g, c in enumerate(cols)))
        labels = VGroup(*(Tex(f"S_{g + 1}", font_size=36, color=GROUP_COLORS[g]).next_to(frames[g], UP, buff=0.15)
                          for g in range(r)))

        def clause_node(points, color=CLAUSE_COLOR):
            center = np.mean([p for p in points], axis=0) + 0.55 * RIGHT
            node = Square(0.18).set_fill(color, 1).set_stroke(width=0).move_to(center)
            edges = VGroup(*(Line(node.get_center(), p, stroke_width=2, color=color) for p in points))
            return VGroup(edges, node)

        inside = VGroup()
        for g in range(r):
            d = cols[g]
            inside.add(clause_node([d[0].get_center(), d[1].get_center(), d[2].get_center()]))
            inside.add(clause_node([d[1].get_center(), d[2].get_center(), d[3].get_center()]))
        self.caption(R"Suppose the $n$ variables split into $r$ groups, and no clause touches two groups.",
                     say="Suppose the n variables split into r groups, and no clause touches two groups.")
        self.play(FadeIn(cols, lag_ratio=0.1), ShowCreation(frames), FadeIn(labels))
        self.play(LaggedStartMap(FadeIn, inside, lag_ratio=0.15))
        self.hold()

        prod = Tex(R"\#F = N_1\cdot N_2\cdot N_3", font_size=48).next_to(frames, DOWN, buff=0.45)
        cost = Tex(R"\text{cost} \approx r\cdot 2^{2n/r}\ \text{ instead of }\ 2^n", font_size=40)
        cost.next_to(prod, DOWN, buff=0.25)
        self.caption(R"Then the count factors: count each group on its own and multiply. The cost is about $r\cdot 2^{2n/r}$ instead of $2^n$.",
                     say="Then the count factors: count each group on its own, and multiply. The cost is about r times two to the two n over r, instead of two to the n.")
        self.play(Write(prod))
        self.play(FadeIn(cost, shift=0.2 * UP))
        self.hold()
        self.play(FadeOut(VGroup(prod, cost)))

        cross = VGroup(
            clause_node([cols[0][3].get_center(), cols[1][0].get_center(), cols[1][2].get_center()], BAD),
            clause_node([cols[1][3].get_center(), cols[2][1].get_center(), cols[2][0].get_center()], BAD),
            clause_node([cols[0][0].get_center(), cols[2][3].get_center(), cols[1][1].get_center()], BAD),
        )
        self.caption(R"Real formulas are tangled: some clauses cross between groups, and the sum no longer factors.",
                     say="Real formulas are tangled: some clauses cross between groups, and the sum no longer factors.")
        self.play(LaggedStartMap(ShowCreation, cross, lag_ratio=0.3, run_time=2))
        self.hold()
        idea = Text("Idea: change the polynomial, not the formula.", font=SERIF, font_size=40, color=YELLOW)
        idea.next_to(frames, DOWN, buff=0.5)
        self.caption(R"The idea: deform the polynomial so that, at special parameter values, clauses talk across groups only through a few integer summaries.",
                     say="The idea: deform the polynomial so that, at special parameter values, clauses talk across groups only through a few integer summaries.")
        self.play(Write(idea))
        self.hold()
        self.clear_caption()
        self.play(FadeOut(VGroup(head, cols, frames, labels, inside, cross, idea)))


# ---------------------------------------------------------------------------
# Scene 4 — deformation and separation
# ---------------------------------------------------------------------------

class S4Separation(Narrated):
    def construct(self):
        head = self.heading("Deform, then separate")
        self.play(Write(head))
        repl = Tex(R"X_v \ \longmapsto\  \langle \vec P_{e,v}(T),\, \vec X\rangle=\sum_{i=1}^{n} p_{e,v,i}(T)\,X_i",
                   font_size=50, t2c={"T": T_COLOR})
        repl.shift(1.8 * UP)
        self.caption(R"Introduce a parameter $T$. In clause $e$, replace each input $X_v$ by a linear form whose coefficients are polynomials in $T$.",
                     say="Introduce a parameter, T. In clause e, replace each input X v by a linear form whose coefficients are polynomials in T.")
        self.play(Write(repl, run_time=2))
        self.hold()

        cond = Tex(R"\vec P_{e,v}(0)=\vec e_v, \qquad \deg \vec P_{e,v}\le R", font_size=44, t2c={"R": ORANGE})
        cond.next_to(repl, DOWN, buff=0.45)
        H = Tex(R"H(T)=\sum_{x\in\lbrace 0,1\rbrace^n}\prod_e \Phi_e\big(\langle \vec P_{e,v}(T),x\rangle\big)",
                font_size=48, t2c={"T": T_COLOR, R"\Phi_e": CLAUSE_COLOR})
        H.next_to(cond, DOWN, buff=0.55)
        facts = Tex(R"H(0)=\#F, \qquad \deg H \le 3nR", font_size=48, t2c={"R": ORANGE})
        facts.next_to(H, DOWN, buff=0.45)
        self.caption(R"At $T=0$ every form is $X_v$ again, so $H(0)=\#F$. With coefficient degree at most $R$, $H$ has degree at most $3nR$.",
                     say="At T equals zero, every form is X v again, so H of zero is the count, sharp F. With coefficient degree at most R, H has degree at most three n R.")
        self.play(FadeIn(cond, shift=0.2 * DOWN))
        self.play(Write(H))
        self.play(Write(facts))
        self.hold()
        self.play(FadeOut(VGroup(repl, cond, H)), facts.animate.scale(0.8).next_to(head, DOWN, buff=0.3))

        # groups at T = t, with measurement boxes
        r = 3
        groups = VGroup()
        for g in range(r):
            box = RoundedRectangle(width=3.0, height=1.9, corner_radius=0.2).set_stroke(GROUP_COLORS[g], 3)
            dots = VGroup(*(Dot(radius=0.08, fill_color=GROUP_COLORS[g]) for _ in range(6))).arrange_in_grid(2, 3, buff=0.45)
            dots.move_to(box).shift(0.3 * UP)
            meas = RoundedRectangle(width=1.4, height=0.5, corner_radius=0.1).set_stroke(Y_COLOR, 2)
            meas.next_to(box, DOWN, buff=0.2)
            ylab = Tex(f"y_{g + 1}=C_{g + 1}x_{g + 1}", font_size=26, color=Y_COLOR).move_to(meas)
            lab = Tex(f"S_{{t,{g + 1}}}", font_size=30, color=GROUP_COLORS[g]).next_to(box, UP, buff=0.1)
            groups.add(VGroup(box, dots, meas, ylab, lab))
        groups.arrange(RIGHT, buff=0.9)
        groups.shift((0.75 - groups[0][0].get_center()[1]) * UP)
        t_label = Tex(R"T=t\in\lbrace 1,\dots,Q\rbrace", font_size=40, color=T_COLOR)
        t_label.to_corner(UL, buff=0.4).shift(0.9 * DOWN)
        self.caption(R"The forms are built so that at $T=t\in\lbrace 1,\dots,Q\rbrace$ each clause reads its own group of variables, plus a few integer measurements $y=Cx$ of the other groups.",
                     say="The forms are built so that at each point t from one to Q, each clause reads its own group of variables, plus a few integer measurements, y equals C x, of the other groups.")
        self.play(FadeIn(groups, lag_ratio=0.15), Write(t_label))
        # a clause in group 2
        node = Square(0.22).set_fill(CLAUSE_COLOR, 1).set_stroke(width=0).move_to(groups[1][0].get_center() + 0.6 * DOWN)
        own = VGroup(*(Line(node.get_center(), groups[1][1][k].get_center(), stroke_width=2.5, color=CLAUSE_COLOR)
                       for k in (0, 2, 4)))
        reads = VGroup(
            Arrow(groups[0][2].get_right(), node.get_left(), buff=0.12, fill_color=Y_COLOR),
            Arrow(groups[2][2].get_left(), node.get_right(), buff=0.12, fill_color=Y_COLOR),
        )
        self.play(FadeIn(node), ShowCreation(own))
        self.play(LaggedStartMap(GrowArrow, reads, lag_ratio=0.3))
        self.hold()

        sep = Tex(R"H(t)=\sum_{\vec y}\ \prod_{g=1}^{r}\ \underbrace{\sum_{u:\ C_g u=y_g} A_{t,g}(u;\vec y)}_{B_{t,g}(\vec y)}",
                  font_size=44, t2c={R"\vec y": Y_COLOR, "y_g": Y_COLOR})
        sep.move_to(1.95 * DOWN)
        self.caption(R"Fix all the measurements $\vec y$, and the groups decouple again: each group is summed on its own, and the results multiply.",
                     say="Fix all the measurements y, and the groups decouple again: each group is summed on its own, and the results multiply.")
        self.play(Write(sep, run_time=2))
        self.hold()
        cost = Tex(R"\text{cost}\approx \underbrace{(2D+1)^{\#\text{measurements}}}_{\text{values of }\vec y}\cdot\underbrace{2^{2n/r}}_{\text{one group}}",
                   font_size=40)
        cost.move_to(sep)
        self.caption(R"Cost: (number of measurement values) $\times$ (assignments of one group). Subexponential, if there are few measurements and many groups.",
                     say="Cost: the number of measurement values, times the assignments of one group. Subexponential, if there are few measurements and many groups.")
        self.play(FadeOut(sep), FadeIn(cost))
        self.hold()
        self.caption(R"But this only works at $T=1,\dots,Q$. We still need $H(0)$.",
                     say="But this only works at T equals one through Q. We still need H of zero.")
        self.hold()
        self.clear_caption()
        self.play(FadeOut(VGroup(head, facts, groups, t_label, node, own, reads, cost)))


# ---------------------------------------------------------------------------
# Scene 5 — Hermite interpolation
# ---------------------------------------------------------------------------

class S5Hermite(Narrated):
    def construct(self):
        head = self.heading("From easy points back to T = 0")
        self.play(Write(head))
        axes = Axes(x_range=(-0.2, 3.45, 0.5), y_range=(-12, 22, 4), width=10.5, height=4.8,
                    axis_config=dict(stroke_color=GREY_B, include_tip=False))
        axes.shift(0.35 * DOWN + 0.4 * LEFT)
        axes.x_axis.add_numbers([1, 2, 3], font_size=30)
        t_lab = Tex("T", font_size=36, color=T_COLOR).next_to(axes.x_axis.get_right(), DOWN, buff=0.2)
        graph = axes.get_graph(lambda x: poly_eval(H_COEFFS, x), x_range=(-0.15, 3.35), color=BLUE)
        glab = Tex("H(T)", font_size=36, color=BLUE).next_to(axes.c2p(3.0, 12), RIGHT, buff=0.3)
        pts = VGroup(*(Dot(axes.c2p(t, poly_eval(H_COEFFS, t)), radius=0.09, fill_color=ORANGE) for t in (1, 2, 3)))
        q0 = Tex("?", font_size=60, color=GREEN).move_to(axes.c2p(0, 14) + 0.5 * UP)
        self.caption(R"We can now evaluate $H$ at $t=1,\dots,Q$ quickly. But the number we want is $H(0)=\#F$.",
                     say="We can now evaluate H at t equals one through Q quickly. But the number we want is H of zero, the count.")
        self.play(ShowCreation(axes), FadeIn(t_lab))
        self.play(LaggedStartMap(GrowFromCenter, pts, lag_ratio=0.3), Write(q0))
        self.hold()

        # many curves through the same points
        fam = VGroup()
        for c in (-1.6, -0.8, 0.8, 1.6):
            f = lambda x, c=c: poly_eval(H_COEFFS, x) + c * (x - 1) * (x - 2) * (x - 3)
            fam.add(axes.get_graph(f, x_range=(-0.15, 3.35), color=GREY_B, stroke_width=2))
        self.caption(R"$Q$ values cannot determine a polynomial of degree up to $3nR$: many curves pass through the same points, with different values at $0$.",
                     say="Q values cannot determine a polynomial of degree up to three n R: many curves pass through the same points, with different values at zero.")
        self.play(LaggedStartMap(ShowCreation, fam, lag_ratio=0.2, run_time=2.5))
        zero_dots = VGroup(*(Dot(g.get_start(), radius=0.06, fill_color=GREY_B) for g in fam))
        self.play(FadeIn(zero_dots))
        self.hold()

        # Taylor jets
        J = 4
        jets = VGroup()
        for t in (1, 2, 3):
            co = taylor_at(H_COEFFS, t, J)
            jets.add(axes.get_graph(lambda x, co=co, t=t: poly_eval(co, x - t), x_range=(t - 0.32, t + 0.32),
                                    color=ORANGE, stroke_width=12).set_stroke(opacity=0.5))
        self.caption(R"Instead, compute several Taylor coefficients of $H$ at each point: value, slope, curvature, \dots",
                     say="Instead, compute several Taylor coefficients of H at each point: value, slope, curvature, and so on.")
        self.play(LaggedStartMap(ShowCreation, jets, lag_ratio=0.3, run_time=2))
        self.hold()
        herm = Tex(R"Q\cdot J \ >\  \deg H \quad\Longrightarrow\quad H \text{ is determined}", font_size=42)
        herm.next_to(axes, UP, buff=0.1)
        self.caption(R"With $J$ coefficients at each of $Q$ points and $QJ>\deg H$, only one polynomial fits: Hermite interpolation recovers $H$, hence $H(0)$.",
                     say="With J coefficients at each of Q points, and Q times J bigger than the degree of H, only one polynomial fits: Ermeet interpolation recovers H, and hence H of zero.")
        self.play(FadeOut(fam), FadeOut(zero_dots), Write(herm))
        self.play(ShowCreation(graph, run_time=2.5), FadeIn(glab))
        ring = Circle(radius=0.16).set_stroke(GREEN, 5).move_to(axes.c2p(0, 14))
        ans = Tex(R"H(0)=\#F=14", font_size=40, color=GREEN).next_to(ring, DR, buff=0.2)
        self.play(FadeOut(q0), ShowCreation(ring), Write(ans))
        self.hold()

        cost = Tex(R"J\approx\frac{3nR}{Q}\quad\implies\quad \text{Taylor cost}\approx \sum_{j\le J}2^j\binom{n}{j}=2^{O\left(n\,\frac{R}{Q}\log\frac{Q}{R}\right)}",
                   font_size=40, t2c={"R": ORANGE, "Q": T_COLOR})
        cost.move_to(0.4 * UP)
        self.caption(R"Each Taylor coefficient costs extra sums (an inclusion--exclusion over $\le J$ variables). That is cheap only if $R\ll Q$: low degree, many points.",
                     say="Each Taylor coefficient costs extra sums: an inclusion-exclusion over at most J variables. That is cheap only if R is much smaller than Q: low degree, many points.")
        self.play(FadeOut(VGroup(axes, t_lab, graph, glab, pts, jets, herm, ring, ans)))
        self.play(Write(cost))
        self.hold(0.5)
        self.clear_caption()
        self.play(FadeOut(VGroup(head, cost)))


# ---------------------------------------------------------------------------
# Scene 6 — the matrix trick
# ---------------------------------------------------------------------------

class S6Matrix(Narrated):
    def construct(self):
        head = self.heading("Low degree, many points: the matrix trick")
        self.play(Write(head))

        kill = Tex(R"\text{term}\times\Big(1-\frac{T}{s}\Big)", font_size=50, t2c={"T": T_COLOR})
        kill.shift(1.4 * UP)
        k1 = Tex(R"T=0:\ \text{unchanged}", font_size=38).next_to(kill, DOWN, buff=0.5).shift(2.2 * LEFT)
        k2 = Tex(R"T=s:\ \text{deleted}", font_size=38, color=BAD).next_to(kill, DOWN, buff=0.5).shift(2.2 * RIGHT)
        self.caption(R"Multiplying a term by $(1-T/s)$ keeps it at $T=0$ and deletes it at $T=s$, at the price of one degree. Each term can afford at most $R-1$ such factors.",
                     say="Multiplying a term by one minus T over s keeps it at T equals zero, and deletes it at T equals s, at the price of one degree. Each term can afford at most R minus one such factors.")
        self.play(Write(kill))
        self.play(FadeIn(k1, shift=0.2 * UP), FadeIn(k2, shift=0.2 * UP))
        self.hold()
        self.play(FadeOut(VGroup(kill, k1, k2)))

        # labels: a word of Q pairs
        Q = 6
        word_a = [0, 2, 1, 1, 0, 2]
        word_d = [1, 2, 0, 2, 2, 1]

        def pair_cell(a, d, s):
            box = Rectangle(width=0.95, height=1.25).set_stroke(GREY_B, 2)
            top = Square(0.38).set_fill(GROUP_COLORS[a], 1).set_stroke(width=0).move_to(box.get_center() + 0.27 * UP)
            bot = Square(0.38).set_fill(GROUP_COLORS[d], 1).set_stroke(width=0).move_to(box.get_center() + 0.27 * DOWN)
            idx = Tex(f"s={s}", font_size=24, color=GREY_A).next_to(box, DOWN, buff=0.1)
            return VGroup(box, top, bot, idx)

        word = VGroup(*(pair_cell(a, d, s + 1) for s, (a, d) in enumerate(zip(word_a, word_d))))
        word.arrange(RIGHT, buff=0.12).shift(0.6 * UP)
        legend = VGroup(Text("variable's group", font=SERIF, font_size=24), Text("clause's group", font=SERIF, font_size=24))
        legend[0].next_to(word[0][1], LEFT, buff=0.5)
        legend[1].next_to(word[0][2], LEFT, buff=0.5)
        self.caption(R"Give each occurrence (clause $e$, variable $v$) a label: at every point $s$, the pair (group of $v$, group assigned to $e$). A word of $Q$ pairs.",
                     say="Give each occurrence, a clause e and a variable v, a label: at every point s, the pair: the group of v, and the group assigned to e. A word of Q pairs.")
        self.play(LaggedStartMap(FadeIn, word, lag_ratio=0.1), FadeIn(legend))
        mism = VGroup(*(SurroundingRectangle(word[s], buff=0.05, color=BAD) for s in range(Q) if word_a[s] != word_d[s]))
        self.play(LaggedStartMap(ShowCreation, mism, lag_ratio=0.15))
        self.hold()

        self.caption(R"The swap $\Pi_s$ exchanges the two entries of pair $s$. After swapping, the coordinate lives in the clause's own group at point $s$.",
                     say="The swap, Pi s, exchanges the two entries of pair s. After swapping, the coordinate lives in the clause's own group at point s.")
        swapped = VGroup(*(pair_cell(d, a, s + 1) for s, (a, d) in enumerate(zip(word_a, word_d))))
        swapped.move_to(word)
        self.play(FadeOut(mism))
        anims = []
        for s in range(Q):
            anims.append(Swap(word[s][1], word[s][2]))
        self.play(LaggedStart(*anims, lag_ratio=0.15, run_time=2.5))
        self.hold()
        self.play(FadeOut(VGroup(word, legend)))

        # M_0 = V_0 f(W_0)
        defs = Tex(R"V_0=\prod_{s=1}^{Q}\Pi_s,\qquad W_0=\tfrac12\sum_{s=1}^{Q}(I-\Pi_s),\qquad M_0=V_0\,f(W_0),\quad \deg f\le R-1",
                   font_size=40, t2c={"R": ORANGE})
        defs.next_to(head, DOWN, buff=0.45)
        split = Tex(R"\zeta_u=\underbrace{\big((I-M_0)\zeta\big)_u}_{\text{measured}}+\underbrace{\sum_w M_0[u,w]\,\zeta_w}_{\text{local after } \le R-1 \text{ fixes}}",
                    font_size=42, t2c={"R": ORANGE})
        split.next_to(defs, DOWN, buff=0.45)
        self.caption(R"Write every coordinate as a measured part plus a local part, using $M_0=V_0f(W_0)$ with $W_0=\frac12\sum_s(I-\Pi_s)$ and $\deg f\le R-1$.",
                     say="Write every coordinate as a measured part plus a local part, using M zero equals V zero times f of W zero, where W zero is one half the sum over s of I minus Pi s, and f has degree at most R minus one.")
        self.play(Write(defs, run_time=2))
        self.play(Write(split, run_time=2))
        self.hold()

        # eigenvalues and the binomial
        eig = Tex(R"M_0\psi=(-1)^j f(j)\,\psi\quad\text{on eigenvectors with } j \text{ antisymmetric factors}", font_size=36)
        eig.next_to(split, DOWN, buff=0.35)
        self.caption(R"The swaps share an eigenbasis. On an eigenvector with $j$ antisymmetric factors, $M_0$ acts by the number $(-1)^jf(j)$.",
                     say="The swaps share an eigenbasis. On an eigenvector with j antisymmetric factors, M zero acts by the number minus one to the j, times f of j.")
        self.play(FadeIn(eig, shift=0.2 * UP))
        self.hold()
        self.play(FadeOut(VGroup(defs, split)), eig.animate.next_to(head, DOWN, buff=0.35))

        Qb, p, R = 60, 0.4375, 12
        pmf = [math.comb(Qb, j) * p**j * (1 - p) ** (Qb - j) for j in range(Qb + 1)]
        lo, hi = 10, 43
        a0 = math.floor(Qb * p - (R - 1) / 2)
        bars = VGroup()
        width = 0.27
        for j in range(lo, hi):
            h = pmf[j] * 38
            bar = Rectangle(width=width * 0.8, height=max(h, 0.01)).set_stroke(width=0)
            bar.set_fill(BLUE if a0 <= j < a0 + R else ORANGE, 1)
            bar.move_to(np.array([(j - (lo + hi) / 2) * width, -2.3 + h / 2, 0]))
            bars.add(bar)
        base = Line(bars.get_corner(DL) + 0.1 * LEFT, bars.get_corner(DR) + 0.1 * RIGHT, color=GREY_B, stroke_width=2)
        jlab = Tex(R"j\sim\mathrm{Bin}(Q,p)", font_size=34).next_to(bars, RIGHT, buff=0.4).shift(1.0 * UP)
        self.caption(R"Across all basis vectors, $j$ is binomially distributed, with spread about $\sqrt Q$.",
                     say="Across all basis vectors, j is binomially distributed, with spread about the square root of Q.")
        self.play(ShowCreation(base), LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.03, run_time=2.5), Write(jlab))
        self.hold()
        band = SurroundingRectangle(VGroup(*bars[a0 - lo:a0 - lo + R]), buff=0.06, color=BLUE)
        blab = Tex(R"f(j)=(-1)^j \text{ on } R \text{ values} \Rightarrow M_0=I", font_size=32, color=BLUE)
        blab.next_to(band, UP, buff=0.15)
        tails = Tex(R"\text{tails: measured}", font_size=30, color=ORANGE).next_to(bars, LEFT, buff=0.2).shift(0.6 * UP)
        self.caption(R"Choose $f$ to interpolate $(-1)^j$ on $R$ values of $j$ around the peak. There $M_0$ acts as the identity; only the thin tails need measuring.",
                     say="Choose f to interpolate minus one to the j on R values of j around the peak. There, M zero acts as the identity; only the thin tails need measuring.")
        self.play(ShowCreation(band), FadeIn(blab))
        self.play(FadeIn(tails))
        self.hold()
        self.play(FadeOut(VGroup(bars, base, jlab, band, blab, tails)))

        why = Tex(R"\deg f\le R-1 \ \implies\  \text{each term undoes} \le R-1 \text{ swaps} \ \implies\  \text{fix with } \prod_{s}\Big(1-\frac{T}{s}\Big)",
                  font_size=36, t2c={"R": ORANGE, "T": T_COLOR})
        why.next_to(eig, DOWN, buff=0.9)
        self.caption(R"Because $\deg f\le R-1$, each term of $M_0$ disagrees with the clause's group at no more than $R-1$ points, so a degree-$(R-1)$ multiplier removes it there.",
                     say="Because f has degree at most R minus one, each term of M zero disagrees with the clause's group at no more than R minus one points, so a multiplier of degree R minus one removes it there.")
        self.play(Write(why))
        self.hold()
        par = Tex(R"R\approx\sqrt{\log n}\gg\sqrt{Q},\qquad Q\approx\frac{\log n}{\log\log n},\qquad r\approx\frac{\sqrt{\log n}}{(\log\log n)^2}",
                  font_size=36, t2c={"R": ORANGE, "Q": T_COLOR})
        par.next_to(why, DOWN, buff=0.7)
        self.caption(R"Taking $R\gg\sqrt Q$ makes the measured tails tiny, while $R\ll Q$ keeps the Taylor step cheap.",
                     say="Taking R much bigger than root Q makes the measured tails tiny, while R much smaller than Q keeps the Taylor step cheap.")
        self.play(FadeIn(par, shift=0.2 * UP))
        self.hold()
        self.clear_caption()
        self.play(FadeOut(VGroup(head, eig, why, par)))


# ---------------------------------------------------------------------------
# Scene 7 — the bill, and general k-SAT
# ---------------------------------------------------------------------------

class S7Costs(Narrated):
    def construct(self):
        head = self.heading("Paying the bill")
        self.play(Write(head))
        costs = Tex(
            R"\underbrace{\sum_{j\le q}2^j\binom{n}{j}}_{\text{Taylor data}}\ \cdot\ "
            R"\underbrace{(2D+1)^{2\tau n}}_{\text{measurements}}\ \cdot\ "
            R"\underbrace{2^{2n/r}}_{\text{one group}}",
            font_size=50,
        )
        costs.shift(1.2 * UP)
        self.caption(R"The total work is a product of three costs. With the chosen parameters each one is $2^{o(n)}$.",
                     say="The total work is a product of three costs. With the chosen parameters, each one is two to the little o of n.")
        self.play(Write(costs, run_time=2.5))
        self.hold()
        total = Tex(R"=\ 2^{O\left(n(\log\log n)^2/\sqrt{\log n}\right)}", font_size=56)
        total.next_to(costs, DOWN, buff=0.6)
        self.caption(R"Multiplied together: $2^{O(n(\log\log n)^2/\sqrt{\log n})}$ for bounded-occurrence formulas --- and only polynomial space, since nothing is tabulated.",
                     say="Multiplied together: two to the big O of n times log log n squared, over the square root of log n, for bounded-occurrence formulas. And only polynomial space, since nothing is tabulated.")
        self.play(Write(total))
        self.hold()
        self.play(FadeOut(VGroup(costs, total)))

        steps = [
            (R"any\\ $k$-CNF", WHITE),
            (R"sparsify:\\ sparse formulas", GREY_A),
            (R"parity tests:\\ $O(n)$ sparse equations", GREY_A),
            (R"Beigel--Tarui lift\\ modulo $2^{n+1}$", GREY_A),
            (R"interpolation\\ counter", YELLOW),
        ]
        boxes = VGroup()
        for text, color in steps:
            t = TexText(text, font_size=30, color=color)
            b = RoundedRectangle(width=2.45, height=1.35, corner_radius=0.15).set_stroke(color, 2)
            t.set_max_width(2.2).move_to(b)
            boxes.add(VGroup(b, t))
        boxes.arrange(RIGHT, buff=0.32).shift(0.6 * UP)
        arrows = VGroup(*(Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.06, thickness=3)
                          for i in range(len(boxes) - 1)))
        self.caption(R"General $k$-CNF formulas: split them into sparse formulas, compress the clauses into $O(n)$ sparse parity tests, and count the common solutions with the same machinery.",
                     say="General k C N F formulas: split them into sparse formulas, compress the clauses into big O of n sparse parity tests, and count the common solutions with the same machinery.")
        self.play(LaggedStartMap(FadeIn, boxes, lag_ratio=0.25), LaggedStartMap(GrowArrow, arrows, lag_ratio=0.25), run_time=3)
        self.hold()
        bt = Tex(R"p_\ell(y)=(1-y)^\ell\sum_{j<\ell}\binom{\ell+j-1}{j}y^j\ \equiv\ \begin{cases}1 & y \text{ even}\\ 0 & y\text{ odd}\end{cases}\pmod{2^\ell}",
                 font_size=38)
        bt.next_to(boxes, DOWN, buff=0.6)
        self.caption(R"A parity test passes when an integer sum is even. The Beigel--Tarui polynomial detects evenness modulo $2^\ell$, so the count is recovered exactly modulo $2^{n+1}$.",
                     say="A parity test passes when an integer sum is even. The Beigel-Tarui polynomial detects evenness modulo two to the ell, so the count is recovered exactly, modulo two to the n plus one.")
        self.play(Write(bt, run_time=2))
        self.hold()
        self.play(FadeOut(VGroup(boxes, arrows, bt)))

        thm = VGroup(
            Tex(R"\#F \text{ for every } k\text{-CNF, in time } (n+m)^{O_k(1)}\,2^{O_k\left(n\log\log n/\sqrt{\log n}\right)}",
                font_size=42),
            Tex(R"\text{and space } (n+m)^{O_k(1)}", font_size=42),
        ).arrange(DOWN, buff=0.35)
        thm.shift(0.4 * UP)
        box = SurroundingRectangle(thm, buff=0.25, color=YELLOW)
        note = Text("Theorem 1.1 — the sharper exponent comes from a tensor-contraction recursion (Appendix D)",
                    font=SERIF, font_size=24, color=GREY_A).next_to(box, DOWN, buff=0.35)
        self.caption(R"With a sharper recursive analysis, the paper's main theorem reaches exponent $O(n\log\log n/\sqrt{\log n})$ for every fixed $k$.",
                     say="With a sharper recursive analysis, the paper's main theorem reaches exponent big O of n log log n over the square root of log n, for every fixed k.")
        self.play(Write(thm), ShowCreation(box))
        self.play(FadeIn(note))
        self.hold()
        self.clear_caption()
        self.play(FadeOut(VGroup(head, thm, box, note)))


# ---------------------------------------------------------------------------
# Scene 8 — what it means
# ---------------------------------------------------------------------------

class S8Meaning(Narrated):
    def construct(self):
        head = self.heading("What falls, and what does not")
        self.play(Write(head))
        names = ["ETH", "SETH", "#ETH", "Gap-ETH", "NSETH"]
        hyps = VGroup(*(Text(nm, font=SERIF, font_size=40) for nm in names)).arrange(RIGHT, buff=0.8)
        hyps.shift(1.6 * UP)
        crosses = VGroup(*(Cross(h, stroke_width=5) for h in hyps))
        self.caption(R"If the proof holds, it refutes ETH and its relatives SETH, \#ETH, Gap-ETH and NSETH, which underpin a large body of conditional lower bounds.",
                     say="If the proof holds, it refutes E T H, and its relatives: SETH, sharp E T H, gap E T H, and N-SETH, which underpin a large body of conditional lower bounds.")
        self.play(LaggedStartMap(FadeIn, hyps, lag_ratio=0.15))
        self.play(LaggedStartMap(ShowCreation, crosses, lag_ratio=0.15))
        self.hold()

        cons = VGroup(
            Tex(R"\text{counting colorings, independent sets, perfect matchings in } 2^{o(v)}", font_size=34),
            Tex(R"\mathsf{E}^{\mathsf{NP}}\not\subseteq\mathsf{SIZE}(O(n));\ \text{ even } C_L(n)>c\,n\sqrt{\log n} \text{ for infinitely many } n", font_size=34),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(hyps, DOWN, buff=0.7)
        self.caption(R"The paper also derives subexponential exact counting for graph colorings and perfect matchings, and a new circuit lower bound for $\mathsf{E}^{\mathsf{NP}}$.",
                     say="The paper also derives subexponential exact counting for graph colorings and perfect matchings, and a new circuit lower bound for E to the NP.")
        self.play(LaggedStartMap(FadeIn, cons, lag_ratio=0.3, shift=0.2 * UP))
        self.hold()
        self.play(FadeOut(cons))

        notp = Tex(R"\mathsf{P}\ \overset{?}{=}\ \mathsf{NP}\quad\text{still open}", font_size=48).next_to(hyps, DOWN, buff=0.7)
        self.caption(R"It does not settle P vs NP: subexponential is still superpolynomial, and $2^{o(n)}$ bounds do not transfer through general reductions.",
                     say="It does not settle P versus NP: subexponential is still superpolynomial, and two to the little o of n bounds do not transfer through general reductions.")
        self.play(Write(notp))
        self.hold()
        galactic = Tex(R"\text{explicit construction engages at } \log_2 n\approx 1.1\times 10^{10}", font_size=40)
        galactic.next_to(notp, DOWN, buff=0.5)
        self.caption(R"It is also not a practical solver: with the explicit parameters of the paper's overview, the machinery only switches on when $\log_2 n$ is about $10^{10}$.",
                     say="It is also not a practical solver: with the explicit parameters of the paper's overview, the machinery only switches on when log base two of n is about ten to the tenth.")
        self.play(FadeIn(galactic, shift=0.2 * UP))
        self.hold()
        self.play(FadeOut(VGroup(hyps, crosses, notp, galactic)))

        status = VGroup(
            Text("Status (27 October 2026)", font=SERIF, font_size=36, color=YELLOW),
            Text("• preprint, not yet peer reviewed", font=SERIF, font_size=30),
            Text("• Lean 4 formalization of the main theorem reported by OpenAI", font=SERIF, font_size=30),
            Text("• under examination by a working group led by", font=SERIF, font_size=30),
            Text("   R. Impagliazzo, R. Paturi and R. Williams", font=SERIF, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(0.5 * UP)
        self.caption(R"Status: a preprint with a reported Lean formalization, now being examined by experts, including the hypothesis's originators.",
                     say="Status: a preprint with a reported Lean formalization, now being examined by experts, including the hypothesis's originators.")
        self.play(LaggedStartMap(FadeIn, status, lag_ratio=0.2))
        self.hold()
        self.clear_caption()
        self.play(FadeOut(VGroup(head, status)))

        end = VGroup(
            Text("Explainer, figures and code", font=SERIF, font_size=40),
            Text("github.com/htt210/awesome-millennium", font=SERIF, font_size=36, color=BLUE),
        ).arrange(DOWN, buff=0.4)
        self.play(FadeIn(end, lag_ratio=0.3))
        self.wait(3)
        self.play(FadeOut(end))


# ---------------------------------------------------------------------------
# Thumbnail / poster (render with -s to save a still)
# ---------------------------------------------------------------------------

class Thumbnail(Scene):
    def construct(self):
        title = Text("The Exponential Time Hypothesis is False", font=SERIF, font_size=60,
                     t2c={"False": RED})
        title.to_edge(UP, buff=0.6)
        eq = Tex(R"\#F \text{ in } 2^{O\left(n\log\log n/\sqrt{\log n}\right)}", font_size=72,
                 t2c={R"\#F": YELLOW})
        eq.next_to(title, DOWN, buff=0.6)
        axes = Axes(x_range=(-0.2, 3.45, 1), y_range=(-12, 22, 4), width=8, height=3.4,
                    axis_config=dict(stroke_color=GREY_B, include_tip=False, stroke_width=2))
        axes.next_to(eq, DOWN, buff=0.5)
        graph = axes.get_graph(lambda x: poly_eval(H_COEFFS, x), x_range=(-0.15, 3.35), color=BLUE)
        jets = VGroup()
        for t in (1, 2, 3):
            co = taylor_at(H_COEFFS, t, 4)
            jets.add(axes.get_graph(lambda x, co=co, t=t: poly_eval(co, x - t), x_range=(t - 0.3, t + 0.3),
                                    color=ORANGE, stroke_width=14).set_stroke(opacity=0.5))
        dots = VGroup(*(Dot(axes.c2p(t, poly_eval(H_COEFFS, t)), radius=0.08, fill_color=ORANGE) for t in (1, 2, 3)))
        ring = Circle(radius=0.15).set_stroke(GREEN, 5).move_to(axes.c2p(0, 14))
        sub = Text("an explainer · awesome-millennium", font=SERIF, font_size=30, color=GREY_A)
        sub.to_edge(DOWN, buff=0.4)
        self.add(title, eq, axes, jets, graph, dots, ring, sub)
