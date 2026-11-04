"""Narrated explainer for "The Unique Games Theorem" (OpenAI, September 2026),
written for 3b1b's manim (manimgl 1.7.2).

The narration is in storyboard.md: every scene calls self.narrate("2.4") and
the words come from beat 2.4 there. The machinery (captions, voice, road map,
charts) is shared in tools/video/narrated.py. Render everything with
./render.sh, or one scene with
    manimgl ugc_video.py C2Game -w -l --config_file ../../../../../tools/video/custom_config.yml

Computed: the Goemans–Williamson curve, vertex covers of random graphs against
the exact optimum, and a small unique game with its best labeling. The test
gauges and the proof stages are schematics.
"""

from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4] / "tools" / "video"))
from narrated import *  # noqa: E402,F403

TEAM_A = BLUE_C
TEAM_B = ORANGE
OKC = GREEN_C
BAD = RED_C


class Video(Narrated):
    STORY = load_storyboard(HERE / "storyboard.md")
    ROADMAP = ["Hard problems", "Unique games", "The claim", "How it works", "Is it right?"]
    PRONOUNCE = [(r"\bSubhash\b", "Soo-bosh"), (r"\bHåstad\b", "Hoastad"), (r"\bHåstad's\b", "Hoastad's"),
                 (r"\b2002\b", "two thousand two"), (r"\b2018\b", "twenty eighteen"), (r"\b2026\b", "twenty twenty-six")]
    BUILD = HERE / "build"


# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------

def small_game(seed=4, n=6, k=4):
    rng = np.random.default_rng(seed)
    hidden = rng.integers(0, k, n)
    edges = [(i, (i + 1) % n) for i in range(n)] + [(0, 3), (1, 4), (2, 5)]
    cons = []
    for t, (u, v) in enumerate(edges):
        c = (hidden[v] - hidden[u]) % k
        if t in (2, 7):
            c = (c + 1 + rng.integers(0, k - 1)) % k
        cons.append((u, v, int(c)))
    best, best_lab = -1, None
    for lab in itertools.product(range(k), repeat=n):
        sat = sum((lab[v] - lab[u]) % k == c for u, v, c in cons)
        if sat > best:
            best, best_lab = sat, lab
    return n, k, cons, best, best_lab


def cover_ratios(trials=400, n=12, seed=11):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(trials):
        p = rng.uniform(0.12, 0.45)
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
        if not edges:
            continue
        opt = next(s for s in range(n + 1) for S in itertools.combinations(range(n), s)
                   if all(u in S or v in S for u, v in edges))
        used = set()
        for t in rng.permutation(len(edges)):
            u, v = edges[t]
            if u not in used and v not in used:
                used |= {u, v}
        out.append(len(used) / opt)
    return np.array(out)


def gw_ratio(theta):
    return (theta / math.pi) / ((1 - math.cos(theta)) / 2)


# ---------------------------------------------------------------------------
# pictures
# ---------------------------------------------------------------------------

def network(n=10, seed=2, radius=2.0, center=ORIGIN):
    rng = np.random.default_rng(seed)
    pts = [center + radius * np.array([math.cos(2 * math.pi * i / n + 0.2) * (0.75 + 0.25 * rng.random()),
                                       math.sin(2 * math.pi * i / n + 0.2) * (0.75 + 0.25 * rng.random()), 0])
           for i in range(n)]
    edges = sorted({tuple(sorted((i, j))) for i in range(n) for j in range(n) if i != j and rng.random() < 0.28})
    return pts, edges


def gauge(fill, width=6.0, color=GREEN_C, label=""):
    frame = RoundedRectangle(width=width, height=0.5, corner_radius=0.12).set_stroke(GREY_B, 2)
    bar = Rectangle(width=max(width * fill, 0.01), height=0.42).set_stroke(width=0).set_fill(color, 0.9)
    bar.move_to(frame.get_left() + np.array([width * fill / 2 + 0.04, 0, 0]))
    t = txt(label, 24, WHITE).next_to(frame, RIGHT, buff=0.3)
    return VGroup(frame, bar, t)


def game_mob(n, k, cons, lab, show=True, radius=1.9, center=ORIGIN):
    pos = {i: center + radius * np.array([math.cos(2 * math.pi * i / n + 0.3), math.sin(2 * math.pi * i / n + 0.3), 0])
           for i in range(n)}
    lines, labels, nodes = VGroup(), VGroup(), VGroup()
    for u, v, c in cons:
        ok = (lab[v] - lab[u]) % k == c
        col = OKC if (ok or not show) else BAD
        ln = Line(pos[u], pos[v]).set_stroke(col if show else GREY_B, 3)
        if show and not ok:
            ln = DashedLine(pos[u], pos[v]).set_stroke(BAD, 3)
        lines.add(ln)
        lab_mob = txt(f"+{c}", 22, WHITE)
        mid = (pos[u] + pos[v]) / 2
        bg = BackgroundRectangle(lab_mob, fill_opacity=0.9, buff=0.04)
        labels.add(VGroup(bg, lab_mob).move_to(mid))
    for i in range(n):
        circ = Circle(radius=0.26).set_fill(BLUE_D, 1).set_stroke(BLUE_C, 2).move_to(pos[i])
        nodes.add(VGroup(circ, txt(str(lab[i]) if show else "?", 26, WHITE).move_to(pos[i])))
    return VGroup(lines, labels, nodes)


# ---------------------------------------------------------------------------
# Chapter 0
# ---------------------------------------------------------------------------

class C0Open(Video):
    def construct(self):
        self.chapter_title = "0. Cold open"
        pts, edges = network(center=0.4 * UP)
        team = [i % 2 == 0 or i in (3,) for i in range(len(pts))]
        lines = VGroup(*[Line(pts[i], pts[j]).set_stroke(GREY_B, 2) for i, j in edges])
        dots = VGroup(*[Dot(p, radius=0.16, fill_color=GREY_B) for p in pts])
        self.narrate("0.1")
        self.play(ShowCreation(lines), FadeIn(dots), run_time=1.5)
        self.cue("cutting as many")
        self.play(*[d.animate.set_fill(TEAM_A if team[i] else TEAM_B) for i, d in enumerate(dots)],
                  *[l.animate.set_stroke(YELLOW, 4) for l, (i, j) in zip(lines, edges) if team[i] != team[j]])
        self.finish()

        self.narrate("0.2")
        g = gauge(0.879, label="87.9% of the best, guaranteed").move_to(2.4 * DOWN)
        g[1].stretch(0.01, 0, about_edge=LEFT)
        self.play(FadeIn(g[0]), FadeIn(g[2]))
        self.play(g[1].animate.stretch(87.9, 0, about_edge=LEFT), run_time=2)
        self.finish()

        self.narrate("0.3")
        title = txt("The Unique Games Theorem", 56)
        sub = txt("OpenAI preprint, September 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(VGroup(lines, dots, g)), Write(title, run_time=2))
        self.play(FadeIn(sub))
        self.finish()
        self.clear_caption()

        self.narrate("0.4")
        big = self.roadmap(None, big=True).move_to(1.5 * DOWN)
        self.play(title.animate.shift(UP), sub.animate.shift(UP), FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — hard problems
# ---------------------------------------------------------------------------

class C1Hard(Video):
    def construct(self):
        self.chapter(0, "1. Hard problems")
        self.narrate("1.1")
        np_box = card(["NP", "easy to check"], width=4.2, size=30).move_to(2.6 * LEFT + 0.6 * UP)
        p_box = card(["P", "easy to solve"], width=4.2, size=30).move_to(2.6 * RIGHT + 0.6 * UP)
        q = txt("are they the same?", 30, YELLOW).move_to(1.3 * DOWN)
        self.play(FadeIn(np_box), FadeIn(p_box))
        self.play(FadeIn(q))
        self.finish()
        self.clear_content()

        self.narrate("1.2")
        rules = VGroup(*[card([r], width=4.6, size=26) for r in ("A on, or B off, or C on", "B on, or C off, or D on",
                                                                  "A off, or C on, or D off")]).arrange(DOWN, buff=0.2)
        rules.move_to(2.4 * LEFT + 0.5 * UP)
        tag = txt("3SAT: among the hardest", 30, YELLOW).move_to(3.0 * RIGHT + 0.5 * UP)
        self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.3))
        self.play(FadeIn(tag))
        self.finish()
        self.clear_content()

        self.narrate("1.3")
        pts, edges = network(n=8, seed=5, radius=1.6, center=3.3 * LEFT + 0.4 * UP)
        team = [i % 2 == 0 for i in range(len(pts))]
        mc = VGroup(*[Line(pts[i], pts[j]).set_stroke(YELLOW if team[i] != team[j] else GREY_D, 3) for i, j in edges],
                    *[Dot(p, radius=0.14, fill_color=TEAM_A if team[k] else TEAM_B) for k, p in enumerate(pts)])
        pts2, edges2 = network(n=8, seed=9, radius=1.6, center=3.3 * RIGHT + 0.4 * UP)
        cov = {0, 3, 5}
        vc = VGroup(*[Line(pts2[i], pts2[j]).set_stroke(GREY_B, 3) for i, j in edges2],
                    *[Dot(p, radius=0.16 if k in cov else 0.12, fill_color=YELLOW if k in cov else GREY_C)
                      for k, p in enumerate(pts2)])
        l1 = txt("Max-Cut", 30, WHITE).next_to(mc, DOWN, buff=0.3)
        l2 = txt("Vertex Cover", 30, WHITE).next_to(vc, DOWN, buff=0.3)
        self.play(FadeIn(mc), FadeIn(l1))
        self.cue("Vertex Cover asks")
        self.play(FadeIn(vc), FadeIn(l2))
        self.finish()
        self.clear_content()

        self.narrate("1.4")
        ax = Chart((0, 180), (0.8, 1.6), 8.0, 3.6, xticks=(0, 45, 90, 135, 180), yticks=(0.8, 1.0, 1.2, 1.4, 1.6),
                   xfmt=lambda v: txt(f"{int(v)}°", 20, GREY_B), yfmt=lambda v: txt(f"{v:.1f}", 20, GREY_B),
                   xlabel="angle between two vectors", ylabel="rounding ratio", grid=False)
        ax.shift(0.5 * UP - ax.box.get_center())
        cv = curve(ax, lambda d: gw_ratio(math.radians(d)), 1, 180, n=400, color=BLUE_C, width=4, ylim=(0.79, 1.61))
        ths = np.linspace(0.01, math.pi, 200001)
        r = (ths / math.pi) / ((1 - np.cos(ths)) / 2)
        i = int(np.argmin(r))
        md, mv = math.degrees(ths[i]), float(r[i])
        dot = Dot(ax.c2p(md, mv), radius=0.1, fill_color=ORANGE)
        lab = txt(f"minimum ≈ {mv:.4f}: about 87.9%", 26, ORANGE).next_to(dot, UP, buff=0.4).shift(1.2 * LEFT)
        self.play(FadeIn(ax), ShowCreation(cv), run_time=2.5)
        self.cue("Its guarantee")
        self.play(FadeIn(dot, scale=2), FadeIn(lab))
        self.finish()
        self.clear_content()

        self.narrate("1.5")
        ratios = cover_ratios()
        bins = np.arange(0.975, 2.08, 0.05)
        counts, _ = np.histogram(ratios, bins=bins)
        hx = Chart((0.95, 2.1), (0, 100), 8.0, 3.4, xticks=(1.0, 1.5, 2.0), yticks=(0, 50, 100),
                   xfmt=lambda v: txt(f"{v:.1f}", 20, GREY_B), yfmt=lambda v: txt(str(int(v)), 20, GREY_B),
                   xlabel="cover found ÷ smallest cover", ylabel="graphs", grid=False)
        hx.shift(0.5 * UP - hx.box.get_center())
        bars = VGroup()
        for c, a, b in zip(counts, bins[:-1], bins[1:]):
            if c == 0:
                continue
            lo, hi = hx.c2p(a + 0.004, 0), hx.c2p(b - 0.004, c)
            bars.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1]).set_stroke(width=0).set_fill(BLUE_C, 0.9)
                     .move_to((lo + hi) / 2))
        two = DashedLine(hx.c2p(2.03, 0), hx.c2p(2.03, 100)).set_stroke(ORANGE, 3)
        tl = txt("factor 2", 24, ORANGE).next_to(two, UP, buff=0.1)
        self.play(FadeIn(hx), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), run_time=2)
        self.play(ShowCreation(two), FadeIn(tl))
        self.finish()

        self.recap("1.6", ["Hard problems; good-enough answers;", "thresholds nobody could beat or explain."])


# ---------------------------------------------------------------------------
# Chapter 2 — unique games
# ---------------------------------------------------------------------------

class C2Game(Video):
    def construct(self):
        self.chapter(1, "2. Unique games")
        n, k, cons, best, lab = small_game()
        center = 2.4 * LEFT + 0.3 * UP
        blank = game_mob(n, k, cons, lab, show=False, center=center)
        self.narrate("2.1")
        self.play(FadeIn(blank[2]))
        self.play(ShowCreation(blank[0]), run_time=1.5)
        self.finish()

        self.narrate("2.2")
        rule = VGroup(txt("rule on each link:", 26, GREY_A),
                      Tex(R"a(v) = a(u) + c \pmod 4", font_size=40)).arrange(DOWN, buff=0.25).move_to(3.4 * RIGHT + 0.8 * UP)
        self.play(FadeIn(blank[1]), FadeIn(rule))
        self.finish()

        self.narrate("2.3")
        u, v, c = cons[0]
        uniq = txt("choose one end: the rule forces the other", 26, YELLOW).next_to(rule, DOWN, buff=0.5)
        self.play(Indicate(blank[2][u], color=YELLOW), Indicate(blank[2][v], color=YELLOW), FadeIn(uniq))
        self.finish()
        self.play(FadeOut(uniq))

        self.narrate("2.4")
        solved = game_mob(n, k, cons, lab, show=True, center=center)
        self.play(FadeTransform(blank, solved), run_time=1.5)
        val = txt(f"value = {best}/{len(cons)}", 32, OKC).next_to(rule, DOWN, buff=0.5)
        note = txt(f"best of all {k ** n:,} labelings", 24, GREY_A).next_to(val, DOWN, buff=0.2)
        self.play(FadeIn(val), FadeIn(note))
        self.finish()
        self.clear_content()

        self.narrate("2.5")
        full = [(u, v, (lab[v] - lab[u]) % k) for u, v, _ in cons]
        g = game_mob(n, k, full, lab, show=False, center=0.4 * UP)
        self.play(FadeIn(g))
        order = [0, 1, 2, 3, 4, 5]
        for i in order:
            self.play(Transform(g[2][i][1], txt(str(lab[i]), 26, WHITE).move_to(g[2][i][1])),
                      g[2][i][0].animate.set_fill(GREEN_D, 1), run_time=0.35)
        self.cue("The question is")
        q = txt("but if only almost all rules can be satisfied?", 28, YELLOW).to_edge(DOWN, buff=1.7)
        self.play(FadeIn(q))
        self.finish()

        self.recap("2.6", ["A unique game: labels on a network,", "and rules that each force one answer."])


# ---------------------------------------------------------------------------
# Chapter 3 — the conjecture
# ---------------------------------------------------------------------------

def gap_line(width=10.0, eps=0.08, delta=0.1):
    line = NumberLine((0, 1, 0.5), width=width, include_numbers=False).set_stroke(GREY_B, 3)
    hi = Rectangle(width=width * eps, height=0.6).set_stroke(width=0).set_fill(GREEN_D, 0.8)
    hi.move_to(line.n2p(1 - eps / 2))
    lo = Rectangle(width=width * delta, height=0.6).set_stroke(width=0).set_fill(RED_D, 0.8)
    lo.move_to(line.n2p(delta / 2))
    labels = VGroup(txt("0", 24, GREY_B).next_to(line.n2p(0), DOWN, buff=0.35),
                    txt("1", 24, GREY_B).next_to(line.n2p(1), DOWN, buff=0.35),
                    txt("almost all satisfiable", 24, GREEN_C).next_to(hi, UP, buff=0.15),
                    txt("almost none", 24, RED_C).next_to(lo, UP, buff=0.15))
    g = VGroup(line, hi, lo, labels)
    g.line = line
    return g


class C3Conjecture(Video):
    def construct(self):
        self.chapter(1, "3. The conjecture")
        self.narrate("3.1")
        g = gap_line().move_to(1.4 * UP)
        q = txt("telling these apart: as hard as 3SAT?", 30, YELLOW).next_to(g, DOWN, buff=0.6)
        who = txt("Subhash Khot, 2002", 26, GREY_A).next_to(q, DOWN, buff=0.25)
        self.play(FadeIn(g))
        self.play(FadeIn(q), FadeIn(who))
        self.finish()
        self.clear_content()

        self.narrate("3.2")
        src = card(["Unique Games", "Conjecture"], width=3.6, size=28).move_to(4.0 * LEFT + 0.4 * UP)
        outs = VGroup(card(["Max-Cut: 87.9% is optimal"], width=6.0, size=26),
                      card(["Vertex Cover: 2 is optimal"], width=6.0, size=26),
                      card(["every constraint problem:", "one family of algorithms is best"], width=6.0, size=24))
        outs.arrange(DOWN, buff=0.3).move_to(2.4 * RIGHT + 0.4 * UP)
        arrs = VGroup(*[Arrow(src.get_right(), o.get_left(), buff=0.1, fill_color=GREY_B, thickness=3) for o in outs])
        self.play(FadeIn(src))
        self.play(GrowArrow(arrs[0]), FadeIn(outs[0]))
        self.cue("and the factor two")
        self.play(GrowArrow(arrs[1]), FadeIn(outs[1]))
        self.finish()

        self.narrate("3.3")
        self.play(GrowArrow(arrs[2]), FadeIn(outs[2]))
        self.finish()
        self.clear_content()

        self.narrate("3.4")
        g = gap_line().move_to(1.0 * UP)
        half = DashedLine(g.line.n2p(0.5) + 0.6 * DOWN, g.line.n2p(0.5) + 0.6 * UP).set_stroke(YELLOW, 3)
        hl = txt("2018: about half satisfiable", 26, YELLOW).next_to(half, UP, buff=0.15)
        who = txt("Khot, Minzer and Safra: the 2-to-2 theorem", 26, GREY_A).next_to(g, DOWN, buff=0.6)
        self.play(FadeIn(g))
        self.play(ShowCreation(half), FadeIn(hl), FadeIn(who))
        self.cue("not almost fully")
        self.play(Indicate(g[1], color=GREEN_C, scale_factor=1.15))
        self.finish()

        self.recap("3.5", ["Khot's conjecture would explain the thresholds.", "It stayed open."])


# ---------------------------------------------------------------------------
# Chapter 4 — the claim
# ---------------------------------------------------------------------------

class C4Claim(Video):
    def construct(self):
        self.chapter(2, "4. The claim")
        self.narrate("4.1")
        sat = card(["3SAT puzzle"], width=3.0, size=28).move_to(4.6 * LEFT + 0.8 * UP)
        box = card(["fast translation"], width=3.4, size=28).move_to(0.6 * LEFT + 0.8 * UP)
        game = card(["unique game"], width=3.0, size=28).move_to(3.6 * RIGHT + 0.8 * UP)
        a1 = Arrow(sat.get_right(), box.get_left(), buff=0.1, fill_color=GREY_B, thickness=3)
        a2 = Arrow(box.get_right(), game.get_left(), buff=0.1, fill_color=GREY_B, thickness=3)
        self.play(FadeIn(sat))
        self.play(GrowArrow(a1), FadeIn(box))
        self.play(GrowArrow(a2), FadeIn(game))
        self.finish()

        self.narrate("4.2")
        y = VGroup(txt("solvable puzzle", 26, GREEN_C), txt("→  almost all rules satisfiable", 26, GREEN_C)).arrange(
            RIGHT, buff=0.3)
        nn = VGroup(txt("unsolvable puzzle", 26, RED_C), txt("→  almost none", 26, RED_C)).arrange(RIGHT, buff=0.3)
        both = VGroup(y, nn).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(1.0 * DOWN)
        self.play(FadeIn(y))
        self.cue("If it cannot")
        self.play(FadeIn(nn))
        self.finish()

        self.narrate("4.3")
        concl = txt("telling them apart fast would solve 3SAT", 28, YELLOW).next_to(both, DOWN, buff=0.4)
        self.play(FadeIn(concl))
        self.finish()

        self.recap("4.4", ["Claimed: Khot's Unique Games Conjecture", "is true."])


# ---------------------------------------------------------------------------
# Chapter 5 — how it works
# ---------------------------------------------------------------------------

class C5How(Video):
    def construct(self):
        self.chapter(3, "5. How it works")
        self.narrate("5.1")
        start = card(["start: Håstad's equations modulo 2", "x + y + z = 1,  x + w + v = 0,  ..."], width=9, size=28)
        self.play(FadeIn(start.move_to(0.6 * UP)))
        self.finish()
        self.play(FadeOut(start))

        self.narrate("5.2")
        rng = np.random.default_rng(1)
        grid = VGroup(*[Square(0.34).set_fill(WHITE if b else BLACK, 1).set_stroke(GREY_B, 1)
                        for b in rng.integers(0, 2, 36)]).arrange_in_grid(6, 6, buff=0).move_to(3.6 * LEFT + 0.4 * UP)
        arrow = Arrow(grid.get_right(), grid.get_right() + 1.6 * RIGHT, buff=0.1, fill_color=GREY_B, thickness=3)
        table = card(["table:", "grid → answer"], width=3.0, size=26).next_to(arrow, RIGHT, buff=0.1)
        nudge = txt("nudge the grid, compare answers", 26, YELLOW).next_to(VGroup(grid, table), DOWN, buff=0.5)
        self.play(FadeIn(grid), GrowArrow(arrow), FadeIn(table))
        self.cue("A test nudges")
        flips = [grid[i] for i in (3, 9, 15, 33)]
        self.play(*[f.animate.set_fill(ORANGE, 1) for f in flips], FadeIn(nudge))
        self.finish()
        self.clear_content()

        self.narrate("5.3")
        g1 = gauge(0.5, width=6.0, color=ORANGE, label="honest answers pass: about 50%").move_to(0.8 * UP + 1.0 * LEFT)
        ob = txt("the one-half obstacle", 30, ORANGE).next_to(g1, DOWN, buff=0.5)
        self.play(FadeIn(g1))
        self.play(FadeIn(ob))
        self.finish()

        self.narrate("5.4")
        g2 = gauge(0.97, width=6.0, color=GREEN_C, label="with the disguise: almost always").next_to(ob, DOWN, buff=0.5)
        g2.align_to(g1, LEFT)
        dis = txt("a nonlinear disguise", 28, GREEN_C).next_to(g1, UP, buff=0.4)
        self.play(FadeIn(dis))
        self.play(FadeIn(g2[0]), FadeIn(g2[2]), GrowFromEdge(g2[1], LEFT), run_time=1.5)
        self.finish()
        self.clear_content()

        self.narrate("5.5")
        cheat = card(["a cheating table", "using simple linear information"], width=6, size=28).move_to(1.0 * UP)
        caught = txt("caught at least 1 time in 8", 30, RED_C).next_to(cheat, DOWN, buff=0.5)
        self.play(FadeIn(cheat))
        self.play(FadeIn(caught, scale=1.2))
        self.finish()
        self.clear_content()

        self.narrate("5.6")
        lab = card(["a labeling satisfying", "a small fraction of rules"], width=4.6, size=26).move_to(3.4 * LEFT + 0.6 * UP)
        ans = card(["a good answer to", "Håstad's equations"], width=4.6, size=26).move_to(3.4 * RIGHT + 0.6 * UP)
        arr = Arrow(lab.get_right(), ans.get_left(), buff=0.1, fill_color=YELLOW, thickness=4)
        exp = txt("expansion theorem (2018)", 24, YELLOW).next_to(arr, UP, buff=0.15)
        self.play(FadeIn(lab))
        self.play(GrowArrow(arr), FadeIn(exp), FadeIn(ans))
        self.finish()

        self.recap("5.7", ["A nonlinear disguise beats the one-half obstacle;", "expansion does the rest."])


# ---------------------------------------------------------------------------
# Chapter 6 — is it right, and what it means
# ---------------------------------------------------------------------------

class C6Close(Video):
    def construct(self):
        self.chapter(4, "6. Is it right?")
        self.narrate("6.1")
        lean = card(["Lean 4: the main reduction, and direct proofs", "for Max-Cut, Vertex Cover, and two more"],
                    width=10, size=28).move_to(1.0 * UP)
        nr = txt("not re-run by us", 24, GREY_A).next_to(lean, DOWN, buff=0.3)
        self.play(FadeIn(lean))
        self.cue("We have not")
        self.play(FadeIn(nr))
        self.finish()
        self.play(FadeOut(VGroup(lean, nr)))

        self.narrate("6.2")
        ex = card(["reported studying it, October 2026:", "Moshkovitz, Khot, Håstad, Minzer and others"],
                  width=10, size=28).move_to(1.0 * UP)
        nv = txt("no settled verdict yet", 26, ORANGE).next_to(ex, DOWN, buff=0.35)
        self.play(FadeIn(ex))
        self.play(FadeIn(nv))
        self.finish()
        self.play(FadeOut(VGroup(ex, nv)))

        self.narrate("6.3")
        locks = VGroup(card(["Max-Cut: 87.9%"], width=4.2, size=30), card(["Vertex Cover: 2"], width=4.2, size=30))
        locks.arrange(RIGHT, buff=0.8).move_to(1.0 * UP)
        un = txt("final thresholds, unless P = NP", 30, YELLOW).next_to(locks, DOWN, buff=0.5)
        self.play(FadeIn(locks))
        self.play(FadeIn(un))
        self.finish()
        self.play(FadeOut(VGroup(locks, un)))

        self.narrate("6.4")
        pnp = txt("P vs NP ?", 72, YELLOW).move_to(0.8 * UP)
        op = txt("still open", 30, GREY_A).next_to(pnp, DOWN, buff=0.4)
        self.play(FadeIn(pnp, scale=1.2), FadeIn(op))
        self.finish()
        self.play(FadeOut(VGroup(pnp, op)))

        self.narrate("6.5")
        self.play(FadeOut(self.roadmap_mob))
        title = txt("The Unique Games Theorem", 50)
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
        title = txt("The Unique Games Theorem", 58).to_edge(UP, buff=0.6)
        sub = txt("the limits of good-enough answers, explained for everyone", 30, GREY_A).next_to(title, DOWN, buff=0.25)
        n, k, cons, best, lab = small_game()
        g = game_mob(n, k, cons, lab, show=True, center=3.4 * LEFT + 1.0 * DOWN, radius=1.6)
        ga = gauge(0.879, width=5.0, label="87.9%").move_to(3.0 * RIGHT + 1.0 * DOWN)
        self.add(title, sub, g, ga)
