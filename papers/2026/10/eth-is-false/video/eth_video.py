"""3Blue1Brown-style explainer for "The Exponential Time Hypothesis is False"
(OpenAI, October 2026), written for 3b1b's manim (manimgl 1.7.2).

The narration is not in this file: every scene calls self.narrate("1.4") and
the words come from beat 1.4 of storyboard.md, the script that was reviewed
before animating. The words appear as captions and, with NARRATION_VOICES set,
are spoken by voice.py; the scene waits for the voice. Each scene logs what it
said and when to build/captions/<Scene>.json, which make_captions.py and
make_voiceover.py turn into captions.srt, script.md and the soundtracks.

Render everything with ./render.sh, or one scene with
    manimgl eth_video.py C1Puzzle -w --hd --config_file custom_config.yml
"""

from __future__ import annotations

import itertools
import json
import math
import re
import sys
from pathlib import Path

from manimlib import *
import random  # noqa: E402,F811  (after the star import, which may shadow it)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from voice import voices_from_env  # noqa: E402

CAPTION_DIR = HERE / "build" / "captions"
VOICE_DIR = HERE / "build" / "voice"
SERIF = "CMU Serif"

ON_COLOR = BLUE_C
OFF_COLOR = GREY_D
HAPPY = GREEN_C
SAD = RED_C
POINT = ORANGE
EXP_COLOR = ORANGE
SUB_COLOR = BLUE_C
POLY_COLOR = GREEN_C

# The deformed counting polynomial of a real 6-switch puzzle (code/toy_eth.py,
# seed 4, r = 2, Q = 3, R = 2): H(T) = 14 + T/3 - 38T^2/9 + 65T^3/18 - T^4/3 - T^5/6.
H_COEFFS = [14, 1 / 3, -38 / 9, 65 / 18, -1 / 3, -1 / 6]

# Written form on screen -> spoken form for the narrator.
PRONOUNCE = [(r"\bETH\b", "E T H"), (r"\b3-SAT\b", "three-sat"), (r"\bSAT\b", "sat"),
             (r"\bPaturi\b", "Pa-toori"), (r"\b1985\b", "nineteen eighty-five"),
             (r"\b1999\b", "nineteen ninety-nine"), (r"\b2014\b", "twenty fourteen"),
             (r"\b2026\b", "twenty twenty-six")]

ROADMAP = ["The puzzle", "Why it's hard", "The bet", "The new idea", "What it means"]

LEAD = 0.25          # the voice starts this long after its caption appears
CHUNK_GAP = 0.3      # silence between two captions of one beat
BEAT_PAUSE = 1.25    # silence after a beat (plus the next beat's lead: about 1.5 s)
RECAP_PAUSE = 3.0


# ---------------------------------------------------------------------------
# the script
# ---------------------------------------------------------------------------

def load_storyboard(path: Path = HERE / "storyboard.md") -> dict[str, str]:
    """Beat id -> narration, from the tables of storyboard.md."""
    beats = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(\d+[a-f]?\.\d+)\s*\|(.*)\|(.*)\|\s*$", line)
        if m:
            beats[m.group(1)] = m.group(3).strip()
    return beats


STORY = load_storyboard()


def spoken(text: str) -> str:
    for pattern, said in PRONOUNCE:
        text = re.sub(pattern, said, text)
    return text


def split_long(sentence: str, limit: int = 130) -> list[str]:
    if len(sentence) <= limit:
        return [sentence]
    cuts = [m.end() for m in re.finditer(r"[,:;] ", sentence)]
    if not cuts:
        return [sentence]
    mid = len(sentence) / 2
    cut = min(cuts, key=lambda c: abs(c - mid))
    return split_long(sentence[:cut].strip(), limit) + split_long(sentence[cut:].strip(), limit)


def caption_chunks(text: str, limit: int = 120) -> list[str]:
    """Sentences, long ones split at a clause boundary, short ones merged: each
    chunk fits in two caption lines."""
    pieces = []
    for sentence in re.split(r"(?<=[.?!])\s+", text.strip()):
        pieces += split_long(sentence)
    chunks = []
    for p in pieces:
        if chunks and len(chunks[-1]) + 1 + len(p) <= limit:
            chunks[-1] += " " + p
        else:
            chunks.append(p)
    return chunks


def wrap(text: str, width: int) -> str:
    """Line breaks with lines of similar length (no one-word last line)."""
    n = max(1, math.ceil(len(text) / width))
    target = len(text) / n
    lines, cur = [], ""
    for word in text.split():
        if cur and len(lines) < n - 1 and len(cur) + 1 + len(word) / 2 > target:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return "\n".join(lines + [cur])


# ---------------------------------------------------------------------------
# small pictures
# ---------------------------------------------------------------------------

def txt(s: str, size: float = 30, color=WHITE, **kw) -> Text:
    return Text(s, font=SERIF, font_size=size, color=color, **kw)


class Switch(VGroup):
    """A toggle switch with a letter above it and on/off below it."""

    def __init__(self, label: str, on: bool | None = False, scale: float = 1.0):
        super().__init__()
        self.pill = RoundedRectangle(width=1.1, height=0.52, corner_radius=0.26)
        self.pill.set_stroke(width=0)
        self.knob = Circle(radius=0.19).set_fill(WHITE, 1).set_stroke(width=0)
        self.state_text = VGroup()
        self.add(self.pill, self.knob, self.state_text)
        if label:
            self.name = txt(label, 34).next_to(self.pill, UP, buff=0.22)
            self.add(self.name)
        self.on = None
        self._apply(on)
        self.scale(scale)

    def _target(self, on):
        if on is None:
            return GREY_E, self.pill.get_center(), "?"
        return (ON_COLOR if on else OFF_COLOR), self.pill.get_center() + (0.28 if on else -0.28) * RIGHT * (
            self.pill.get_width() / 1.1), ("on" if on else "off")

    def _words(self):
        if not self.state_text.submobjects:
            k = self.pill.get_width() / 1.1
            for word in ("on", "off", "?"):
                self.state_text.add(txt(word, 24, GREY_A).scale(k).next_to(self.pill, DOWN, buff=0.15))
        return self.state_text.submobjects

    @staticmethod
    def _index(on):
        return 2 if on is None else (0 if on else 1)

    def _apply(self, on):
        color, pos, _ = self._target(on)
        self.pill.set_fill(color, 1)
        self.knob.move_to(pos)
        self.knob.set_opacity(0 if on is None else 1)
        for i, w in enumerate(self._words()):
            w.set_opacity(1 if i == self._index(on) else 0)
        self.on = on

    def flip(self, on, run_time=0.4):
        color, pos, _ = self._target(on)
        self.on = on
        return AnimationGroup(
            self.pill.animate.set_fill(color, 1),
            self.knob.animate.move_to(pos).set_opacity(0 if on is None else 1),
            *[w.animate.set_opacity(1 if i == self._index(on) else 0) for i, w in enumerate(self._words())],
            run_time=run_time)


class RuleCard(VGroup):
    """'Rule k' and its three wishes, stacked; colored by the switches' states."""

    def __init__(self, k: int | None, wishes: list[tuple[str, int]], width=2.9):
        super().__init__()
        self.wishes = wishes
        lines = [txt(f"{'or ' if i else ''}{s} {'on' if w else 'off'}", 28) for i, (s, w) in enumerate(wishes)]
        self.lines = VGroup(*lines).arrange(DOWN, buff=0.14)
        self.title = txt(f"Rule {k}" if k else "Rule", 30, YELLOW)
        body = VGroup(self.title, self.lines).arrange(DOWN, buff=0.25)
        self.box = RoundedRectangle(width=width, height=body.get_height() + 0.5, corner_radius=0.15)
        self.box.set_stroke(GREY_B, 2).set_fill(BLACK, 0)
        self.box.move_to(body)
        self.mark = VGroup()
        self.add(self.box, body, self.mark)

    def status(self, state: dict) -> list[bool | None]:
        out = []
        for s, w in self.wishes:
            v = state.get(s)
            out.append(None if v is None else v == w)
        return out

    def color_by(self, state: dict, run_time=0.4):
        st = self.status(state)
        anims = []
        for line, ok in zip(self.lines, st):
            anims.append(line.animate.set_color(HAPPY if ok else (WHITE if ok is None else GREY_C)))
        happy = any(ok for ok in st)
        decided = happy or all(ok is not None for ok in st)
        color = HAPPY if happy else (SAD if decided else GREY_B)
        anims.append(self.box.animate.set_stroke(color, 3 if decided else 2))
        mark = txt("✓" if happy else ("✗" if decided else ""), 34, color)
        mark.next_to(self.box.get_corner(UR), DL, buff=0.12)
        anims.append(Transform(self.mark, VGroup(mark) if decided else VGroup()))
        return AnimationGroup(*anims, run_time=run_time)


def card(lines: list[str], width=11.0, size=34, color=WHITE, title: str | None = None, title_color=YELLOW):
    body = VGroup()
    if title:
        body.add(txt(title, size + 4, title_color))
    for line in lines:
        body.add(txt(wrap(line, int(width * 5.2)), size, color))
    body.arrange(DOWN, buff=0.3)
    box = RoundedRectangle(width=max(width, body.get_width() + 0.8), height=body.get_height() + 0.7,
                           corner_radius=0.2).set_stroke(GREY_B, 2).set_fill(BLACK, 0.9)
    box.move_to(body)
    return VGroup(box, body)


def gauge(value: float) -> VGroup:
    label = txt("factor per switch", 20, GREY_A)
    times = txt("×", 34, YELLOW)
    num = DecimalNumber(value, num_decimal_places=2, font_size=40, color=YELLOW)
    row = VGroup(times, num).arrange(RIGHT, buff=0.08)
    body = VGroup(label, row).arrange(DOWN, buff=0.08)
    box = RoundedRectangle(width=body.get_width() + 0.4, height=body.get_height() + 0.3, corner_radius=0.12)
    box.set_stroke(YELLOW, 1.5).set_fill(BLACK, 0.9).move_to(body)
    g = VGroup(box, body)
    g.num = num
    g.to_corner(UR, buff=0.25)
    g.fix_in_frame()
    return g


def dial(value: float = 0.0, radius=0.75) -> VGroup:
    face = Circle(radius=radius).set_stroke(GREY_B, 3).set_fill(BLACK, 1)
    ticks = VGroup()
    for v in range(4):
        a = dial_angle(v)
        p = face.get_center() + radius * np.array([math.cos(a), math.sin(a), 0])
        ticks.add(Line(p * 0.82 + face.get_center() * 0.18, p).set_stroke(GREY_B, 3))
        ticks.add(txt(str(v), 22, GREY_A).move_to(face.get_center() + 1.3 * radius * np.array(
            [math.cos(a), math.sin(a), 0])))
    needle = Line(ORIGIN, 0.8 * radius * RIGHT).set_stroke(YELLOW, 5)
    needle.rotate(dial_angle(value), about_point=ORIGIN)
    hub = Dot(radius=0.06, fill_color=YELLOW)
    g = VGroup(face, ticks, needle, hub)
    g.needle, g.value = needle, value
    title = txt("dial", 24, GREY_A).next_to(face, DOWN, buff=0.15)
    g.add(title)
    return g


def dial_angle(v: float) -> float:
    return math.radians(150 - 40 * v)


def turn_dial(d: VGroup, value: float, run_time=1.0):
    center = d[0].get_center()
    delta = dial_angle(value) - dial_angle(d.value)
    d.value = value
    return Rotate(d.needle, delta, about_point=center, run_time=run_time)


def team_blob(center, n=7, radius=1.35, color=ON_COLOR, seed=0, links=6, dot_r=0.16):
    rng = random.Random(seed)
    bg = Circle(radius=radius + 0.45).set_fill(GREY_E, 0.6).set_stroke(width=0).move_to(center)
    pts = [center + radius * 0.8 * np.array([math.cos(2 * math.pi * k / n + 0.4), math.sin(2 * math.pi * k / n + 0.4), 0])
           for k in range(n)]
    lines = VGroup()
    for _ in range(links):
        a, b = rng.sample(range(n), 2)
        lines.add(Line(pts[a], pts[b]).set_stroke(GREY_B, 2))
    dots = VGroup(*[Dot(p, radius=dot_r, fill_color=color) for p in pts])
    g = VGroup(bg, lines, dots)
    g.pts, g.dots = pts, dots
    return g


def mini_row(bits, size=0.24):
    return VGroup(*[Square(size).set_fill(ON_COLOR if b else OFF_COLOR, 1).set_stroke(BLACK, 1) for b in bits]).arrange(
        RIGHT, buff=0.04)


class Chart(VGroup):
    """Axes along the bottom and left edges of a width x height box, whatever the
    data ranges (manim's Axes put the axes through (0, 0))."""

    def __init__(self, x_range, y_range, width, height, xticks=(), yticks=(), xfmt=None, yfmt=None,
                 xlabel=None, ylabel=None, grid=True):
        super().__init__()
        self.x0, self.x1 = x_range
        self.y0, self.y1 = y_range
        self.box = Rectangle(width=width, height=height).set_stroke(width=0).set_fill(opacity=0)
        self.add(self.box)
        dl, dr, ul = self.box.get_corner(DL), self.box.get_corner(DR), self.box.get_corner(UL)
        if grid:
            for v in yticks:
                self.add(Line(self.c2p(self.x0, v), self.c2p(self.x1, v)).set_stroke(GREY_E, 1))
        self.add(Line(dl, dr).set_stroke(GREY_B, 2), Line(dl, ul).set_stroke(GREY_B, 2))
        xfmt = xfmt or (lambda v: txt(str(v), 20, GREY_B))
        yfmt = yfmt or (lambda v: txt(str(v), 20, GREY_B))
        self.xl = VGroup(*[xfmt(v).next_to(self.c2p(v, self.y0), DOWN, buff=0.15) for v in xticks])
        self.yl = VGroup(*[yfmt(v).next_to(self.c2p(self.x0, v), LEFT, buff=0.15) for v in yticks])
        self.add(self.xl, self.yl)
        if xlabel:
            self.add(txt(xlabel, 22, GREY_A).next_to(self.xl if xticks else Line(dl, dr), DOWN, buff=0.12))
        if ylabel:
            self.add(txt(ylabel, 20, GREY_A).rotate(PI / 2).next_to(self.yl if yticks else Line(dl, ul), LEFT,
                                                                     buff=0.2))

    def c2p(self, x, y):
        dl = self.box.get_corner(DL)
        return dl + np.array([(x - self.x0) / (self.x1 - self.x0) * self.box.get_width(),
                              (y - self.y0) / (self.y1 - self.y0) * self.box.get_height(), 0])


def times_label(v):
    return txt(f"×{v:.1f}", 20, GREY_B)


def power_label(k):
    return Tex(f"10^{{{k}}}", font_size=26, color=GREY_B)


def curve(ax, f, x0, x1, n=200, color=BLUE, width=4, ylim=None):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = f(x)
        if ylim and not (ylim[0] <= y <= ylim[1]):
            continue
        pts.append(ax.c2p(x, y))
    m = VMobject().set_points_smoothly(pts) if len(pts) > 2 else VMobject()
    return m.set_stroke(color, width)


def poly(coeffs, x):
    return sum(c * x ** k for k, c in enumerate(coeffs))


# ---------------------------------------------------------------------------
# the narrated scene
# ---------------------------------------------------------------------------

class Narrated(Scene):
    """Captions and voice for the beats of storyboard.md, plus the road map."""

    def setup(self):
        super().setup()
        self.voices = voices_from_env(VOICE_DIR)
        self.log = []
        self.beat_end = 0.0
        self.chunks = []           # (shown_at, voice_at, duration, text, mobject)
        self.caption_box = VGroup().fix_in_frame()
        self.current_caption = None
        self.caption_box.add_updater(lambda m: self._update_caption())
        self.add(self.caption_box)
        self.roadmap_mob = None
        self.gauge_mob = None

    # -- narration ----------------------------------------------------------
    def _duration(self, said: str) -> float:
        if self.voices:
            return max(v.duration(said) for v in self.voices.values())
        return 0.6 + len(said) / 15.0

    def _caption_mob(self, text: str) -> VGroup:
        body = txt(wrap(text, 66), 38)
        body.set_max_width(13.4)
        body.to_edge(DOWN, buff=0.3)
        box = BackgroundRectangle(body, fill_opacity=0.8, buff=0.14)
        return VGroup(box, body).fix_in_frame()

    def _update_caption(self):
        active = None
        for c in self.chunks:
            if c["shown"] <= self.time + 1e-6:
                active = c
        if active is not self.current_caption:
            self._close_caption()
            if active is not None:
                self.caption_box.set_submobjects([active["mob"]])
                active["shown_real"] = self.time
                self.current_caption = active

    def _close_caption(self):
        if self.current_caption is not None:
            c = self.current_caption
            self.log.append({"start": round(c["shown_real"], 3), "end": round(self.time, 3), "text": c["text"],
                             "say": c["say"], "voice_at": round(c["voice_at"], 3)})
            self.current_caption = None
            self.caption_box.set_submobjects([])

    def narrate(self, beat: str):
        """Start beat `beat`: its captions and voice run while the following
        animations play. Call finish() to wait for the end."""
        if self.time < self.beat_end:
            self.wait(self.beat_end - self.time)
        text = STORY[beat]
        self.chunks = [c for c in self.chunks if c is self.current_caption]
        t = self.time
        for i, chunk in enumerate(caption_chunks(text) if text else []):
            said = spoken(chunk)
            dur = self._duration(said)
            shown = t if i == 0 else t - LEAD
            self.chunks.append({"shown": shown, "voice_at": t + LEAD if i == 0 else t, "dur": dur, "text": chunk,
                                "say": said, "mob": self._caption_mob(chunk)})
            t = (t + LEAD if i == 0 else t) + dur + CHUNK_GAP
        self.beat_end = t - CHUNK_GAP if text else t
        self.beat_chunks = [c for c in self.chunks if c is not self.current_caption]

    def cue(self, phrase: str, offset: float = 0.0):
        """Wait until the narrator is about to say `phrase` (estimated from its
        position in the caption)."""
        for c in self.beat_chunks:
            i = c["text"].find(phrase)
            if i >= 0:
                t = c["voice_at"] + c["dur"] * (i / max(1, len(c["text"]))) + offset
                if t > self.time:
                    self.wait(t - self.time)
                return
        raise ValueError(f"cue {phrase!r} not in the current beat")

    def finish(self, pause: float = BEAT_PAUSE):
        left = self.beat_end + pause - self.time
        if left > 0:
            self.wait(left)

    def say(self, beat: str, pause: float = BEAT_PAUSE):
        self.narrate(beat)
        self.finish(pause)

    def clear_caption(self):
        self.chunks = []
        self._close_caption()

    def recap(self, beat: str, lines: list[str]):
        c = card(lines, title="Recap", size=32)
        c.move_to(0.3 * UP)
        self.play(FadeOut(self.content(), run_time=0.6), FadeIn(c, run_time=0.6))
        self.narrate(beat)
        self.finish(RECAP_PAUSE)
        self.clear_caption()
        self.play(FadeOut(c))

    def content(self) -> Group:
        """Everything on screen except captions, road map and gauge."""
        keep = {self.caption_box, self.roadmap_mob, self.gauge_mob}
        return Group(*[m for m in self.mobjects if m not in keep])

    # -- signposts -------------------------------------------------------------
    def roadmap(self, active: int | None, big=False) -> VGroup:
        boxes = VGroup()
        for i, name in enumerate(ROADMAP):
            lit = active is not None and (i == active or active == -1)
            label = txt(name, 22, "#111111" if lit else GREY_B)
            box = RoundedRectangle(width=2.05, height=0.5, corner_radius=0.1)
            box.set_fill(YELLOW if lit else BLACK, 1).set_stroke(YELLOW if lit else GREY_D, 1.5)
            label.move_to(box)
            boxes.add(VGroup(box, label))
        boxes.arrange(RIGHT, buff=0.12)
        if big:
            boxes.scale(1.3)
        else:
            boxes.scale(0.75).to_corner(UL, buff=0.22)
        return boxes.fix_in_frame()

    def chapter(self, active: int, title: str):
        heading = txt(title, 56).move_to(0.6 * UP)
        big = self.roadmap(active, big=True).move_to(0.9 * DOWN)
        self.play(FadeIn(heading, shift=0.3 * UP), FadeIn(big, lag_ratio=0.1))
        self.wait(1.2)
        small = self.roadmap(active)
        if self.roadmap_mob is not None:
            self.remove(self.roadmap_mob)
        self.play(FadeOut(heading), ReplacementTransform(big, small))
        self.roadmap_mob = small

    def subtitle(self, text: str) -> Text:
        t = txt(text, 30, YELLOW).to_edge(UP, buff=0.85)
        return t

    def show_gauge(self, value: float):
        self.gauge_mob = gauge(value)
        self.play(FadeIn(self.gauge_mob, shift=0.2 * DOWN))

    def set_gauge(self, value: float, run_time=1.5):
        return ChangeDecimalToValue(self.gauge_mob.num, value, run_time=run_time)

    def tear_down(self):
        self._close_caption()
        CAPTION_DIR.mkdir(parents=True, exist_ok=True)
        data = {"scene": type(self).__name__, "duration": round(self.time, 3), "voices": sorted(self.voices),
                "captions": self.log}
        (CAPTION_DIR / f"{type(self).__name__}.json").write_text(json.dumps(data, indent=1))
        super().tear_down()


# ---------------------------------------------------------------------------
# shared data
# ---------------------------------------------------------------------------

PUZZLE_SWITCHES = "ABCD"
PUZZLE_RULES = [[("A", 1), ("B", 0), ("C", 1)], [("B", 1), ("C", 0), ("D", 1)], [("A", 0), ("C", 1), ("D", 0)]]


def good_settings():
    out = []
    for bits in itertools.product([0, 1], repeat=4):
        st = dict(zip(PUZZLE_SWITCHES, bits))
        if all(any(st[s] == w for s, w in rule) for rule in PUZZLE_RULES):
            out.append(bits)
    return out


HISTORY = [(1970, 2.0), (1985, 1.619), (1999, 4 / 3), (2014, 1.308), (2026, 1.307)]


def history_chart():
    ax = Chart((1965, 2030), (1.0, 2.1), 10.0, 4.0, xticks=range(1970, 2030, 10),
               yticks=(1.0, 1.2, 1.4, 1.6, 1.8, 2.0), yfmt=times_label,
               ylabel="work multiplied by each extra switch")
    ax.shift(0.45 * UP + 0.4 * RIGHT - ax.box.get_center())
    return ax, ax


def step_segments(ax):
    segs, dots = [], []
    pts = HISTORY + [(2029, HISTORY[-1][1])]
    for (y0, v0), (y1, v1) in zip(pts, pts[1:]):
        flat = Line(ax.c2p(y0, v0), ax.c2p(y1, v0)).set_stroke(BLUE_C, 5)
        drop = Line(ax.c2p(y1, v0), ax.c2p(y1, v1)).set_stroke(BLUE_C, 5)
        segs.append(VGroup(flat, drop) if y1 != 2029 else VGroup(flat))
        dots.append(Dot(ax.c2p(y0, v0), radius=0.08, fill_color=BLUE_C))
    return segs, dots


def shapes_chart():
    ax = Chart((2, 12), (1.0, 2.1), 9.0, 3.9, xticks=range(2, 13, 2), yticks=(1.0, 1.2, 1.4, 1.6, 1.8, 2.0),
               xfmt=power_label, yfmt=times_label, xlabel="number of switches", ylabel="average work per switch")
    ax.shift(0.5 * UP + 1.0 * LEFT - ax.box.get_center())
    exp = curve(ax, lambda x: 2.0, 2, 12, color=EXP_COLOR)
    sub = curve(ax, lambda x: 2 ** (1 / math.sqrt(x * math.log2(10))), 2, 12, color=SUB_COLOR)
    pol = curve(ax, lambda x: 10 ** (3 * x / 10 ** x), 2, 12, n=600, color=POLY_COLOR)
    return ax, ax, exp, sub, pol


# ---------------------------------------------------------------------------
# Chapter 0 — cold open
# ---------------------------------------------------------------------------

class C0Open(Narrated):
    def construct(self):
        s = Switch("", False, scale=1.6)
        self.narrate("0.1")
        self.play(FadeIn(s))
        self.cue("It can be on")
        self.play(s.flip(True))
        self.cue("or off", -0.1)
        self.play(s.flip(False))
        self.finish()

        self.narrate("0.2")
        row = VGroup(*[Switch("", False, scale=0.9) for _ in range(10)]).arrange(RIGHT, buff=0.25).move_to(0.5 * UP)
        self.play(ReplacementTransform(s, row[4]), FadeIn(VGroup(*row[:4], *row[5:]), lag_ratio=0.1))
        rng = random.Random(1)
        budget, rts, rt = self.beat_end - 1.0 - self.time, [], 0.5
        while sum(rts) + rt < budget:          # flicker faster and faster
            rts.append(rt)
            rt = max(0.12, rt * 0.8)
        for rt in rts:
            self.play(*[sw.flip(rng.random() < 0.5, run_time=rt) for sw in row])
        self.finish(0.3)

        self.narrate("0.3")
        ax = Chart((0, 10), (0, 10), 8, 4.2, grid=False, xlabel="size of the puzzle", ylabel="work")
        ax.shift(0.4 * UP - ax.box.get_center())
        labels = VGroup()
        wall = curve(ax, lambda x: 0.02 * 2 ** x, 0, 9.0, color=RED_C, width=6, ylim=(0, 10.5))
        self.play(FadeOut(row), FadeIn(ax), FadeIn(labels))
        self.play(ShowCreation(wall, run_time=2.0))
        self.finish()

        self.narrate("0.4")
        title = txt("The Exponential Time Hypothesis is False", 52)
        sub = txt("OpenAI preprint, October 2026", 30, GREY_A).next_to(title, DOWN, buff=0.4)
        self.play(FadeOut(VGroup(ax, labels, wall)), Write(title, run_time=2))
        self.play(FadeIn(sub))
        self.finish()
        self.clear_caption()

        self.narrate("0.5")
        big = self.roadmap(None, big=True).move_to(1.5 * DOWN)
        self.play(title.animate.shift(UP), sub.animate.shift(UP), FadeIn(big, lag_ratio=0.2, run_time=2))
        self.finish(2.0)
        self.play(FadeOut(VGroup(title, sub, big)))


# ---------------------------------------------------------------------------
# Chapter 1 — the puzzle
# ---------------------------------------------------------------------------

class C1Puzzle(Narrated):
    def construct(self):
        self.chapter(0, "1. The puzzle")
        sw = {k: Switch(k, False) for k in PUZZLE_SWITCHES}
        row = VGroup(*sw.values()).arrange(RIGHT, buff=1.6).move_to(1.7 * UP)
        state = {k: 0 for k in PUZZLE_SWITCHES}

        self.narrate("1.1")
        self.play(LaggedStart(*[FadeIn(s, shift=0.2 * DOWN) for s in row], lag_ratio=0.25, run_time=2))
        self.finish()

        self.narrate("1.2")
        r1 = RuleCard(1, PUZZLE_RULES[0]).move_to(1.3 * DOWN)
        self.play(FadeIn(r1, shift=0.2 * UP))
        self.cue("This one says")
        links = VGroup(*[Line(r1.box.get_top(), sw[s].state_text.get_bottom() + 0.1 * DOWN).set_stroke(GREY_B, 2)
                         for s, _ in PUZZLE_RULES[0]])
        self.play(LaggedStart(*[ShowCreation(l) for l in links], lag_ratio=0.3))
        for line in r1.lines:
            self.play(Indicate(line, color=YELLOW, scale_factor=1.1), run_time=0.7)
        self.finish()

        self.narrate("1.3")
        ors = VGroup(*[line[:2] for line in r1.lines[1:]])
        self.play(Indicate(ors, color=YELLOW, scale_factor=1.4), run_time=1.5)
        self.cue("at least one")
        self.play(Indicate(ors, color=YELLOW, scale_factor=1.4), run_time=1.2)
        self.finish()

        self.narrate("1.4")
        self.cue("Right now")
        self.play(r1.lines[0].animate.set_color(GREY_C), r1.lines[2].animate.set_color(GREY_C))
        self.cue("But B is off")
        self.play(Indicate(sw["B"], color=HAPPY), r1.lines[1].animate.set_color(HAPPY))
        self.cue("so the rule is happy")
        self.play(r1.color_by(state))
        self.finish()

        self.narrate("1.5")
        state["B"] = 1
        self.play(sw["B"].flip(True))
        self.play(r1.color_by(state))
        self.finish()

        self.narrate("1.6")
        r2 = RuleCard(2, PUZZLE_RULES[1])
        r3 = RuleCard(3, PUZZLE_RULES[2])
        rules = VGroup(r1.copy(), r2, r3).arrange(RIGHT, buff=0.6).move_to(1.4 * DOWN)
        state["B"] = 0
        self.play(FadeOut(links), sw["B"].flip(False))
        self.play(r1.animate.move_to(rules[0]), FadeIn(r2, shift=0.2 * UP), FadeIn(r3, shift=0.2 * UP))
        self.remove(rules[0])
        rules = VGroup(r1, r2, r3)
        neutral = {k: None for k in PUZZLE_SWITCHES}
        self.play(*[r.color_by(neutral) for r in rules])
        self.finish()

        self.narrate("1.7")
        q = txt("Can you set the switches so that every rule is happy?", 30, YELLOW).to_edge(UP, buff=0.85)
        self.play(Write(q))
        self.finish()

        self.narrate("1.8")
        state = {k: None for k in PUZZLE_SWITCHES}
        self.play(*[s.flip(None) for s in sw.values()])
        steps = [("A", 1, "A on makes"), ("B", 1, "B on makes"), ("C", 1, "C on makes"), ("D", 0, "And D can")]
        for key, val, phrase in steps:
            self.cue(phrase)
            state[key] = val
            self.play(sw[key].flip(bool(val)), *[r.color_by(state) for r in rules])
        self.cue("Every rule is happy")
        self.play(*[Indicate(r, color=HAPPY, scale_factor=1.05) for r in rules])
        self.finish()

        self.narrate("1.9")
        name = card(["This puzzle is called 3-SAT", "3: each rule names three switches   ·   SAT: satisfy every rule"],
                    width=10, size=30)
        name.move_to(0.2 * UP)
        dim = FullScreenRectangle().set_fill(BLACK, 0.85).set_stroke(width=0)
        self.play(FadeOut(q), FadeIn(dim), FadeIn(name))
        self.finish()
        self.play(FadeOut(name), FadeOut(dim))

        self.narrate("1.10")
        puzzle = VGroup(row, rules)
        self.play(puzzle.animate.scale(0.55).move_to(0.2 * DOWN))
        icons = VGroup(timetable_icon(), chip_icon(), route_icon(), sudoku_icon())
        names = ["timetables", "chip design", "routes", "Sudoku"]
        spots = [LEFT * 5.2 + UP * 1.7, RIGHT * 5.2 + UP * 1.7, LEFT * 5.2 + DOWN * 1.2, RIGHT * 5.2 + DOWN * 1.2]
        arrows = VGroup()
        for icon, name_, spot in zip(icons, names, spots):
            icon.move_to(spot)
            icon.add(txt(name_, 22, GREY_A).next_to(icon, DOWN, buff=0.12))
            arrows.add(Arrow(icon.get_center(), puzzle.get_center(), buff=1.2, fill_color=GREY_B, thickness=4))
        for icon, arrow, phrase in zip(icons, arrows, ["making timetables", "checking that", "planning routes",
                                                       "even solving Sudoku"]):
            self.cue(phrase)
            self.play(FadeIn(icon, scale=0.8), GrowArrow(arrow), run_time=0.8)
        self.finish()

        self.narrate("1.11")
        self.play(FadeOut(icons), FadeOut(arrows))
        goods = good_settings()
        stack = VGroup(*[mini_row(b) for b in goods]).arrange(DOWN, buff=0.12)
        stack.move_to(4.2 * RIGHT + 0.2 * DOWN)
        heads = VGroup(*[txt(k, 20, GREY_A) for k in PUZZLE_SWITCHES])
        for h, sq in zip(heads, stack[0]):
            h.next_to(sq, UP, buff=0.15)
        self.play(puzzle.animate.shift(2.5 * LEFT))
        self.cue("It counts")
        counter = Integer(0, font_size=48, color=YELLOW)
        lab = txt("good settings", 26, GREY_A)
        cnt = VGroup(counter, lab).arrange(RIGHT, buff=0.2).next_to(stack, LEFT, buff=0.8)
        self.play(FadeIn(heads), FadeIn(cnt))
        for i, r in enumerate(stack):
            self.play(FadeIn(r, shift=0.1 * LEFT), ChangeDecimalToValue(counter, i + 1), run_time=0.35)
        self.finish()

        self.recap("1.12", ["Switches, and rules that want at least one of their wishes.",
                            "The question: how many settings make every rule happy?"])


def timetable_icon():
    g = VGroup(*[Rectangle(0.42, 0.28).set_stroke(GREY_B, 1.5) for _ in range(12)]).arrange_in_grid(3, 4, buff=0)
    for i in (1, 6, 8):
        g[i].set_fill(BLUE_D, 1)
    return VGroup(g)


def chip_icon():
    body = Square(1.0).set_fill(GREY_E, 1).set_stroke(GREY_B, 2)
    pins = VGroup()
    for i in range(4):
        for side in (UP, DOWN, LEFT, RIGHT):
            off = (-0.36 + 0.24 * i)
            p = body.get_center() + 0.5 * side + (off * (RIGHT if side[1] else UP))
            pins.add(Line(p, p + 0.18 * side).set_stroke(GREY_B, 3))
    return VGroup(body, pins, txt("CPU", 22, GREY_A).move_to(body))


def route_icon():
    pts = [LEFT * 0.7 + DOWN * 0.4, LEFT * 0.2 + UP * 0.4, RIGHT * 0.3 + DOWN * 0.2, RIGHT * 0.7 + UP * 0.45]
    path = VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 3)
    return VGroup(path, *[Dot(p, radius=0.08, fill_color=WHITE) for p in pts])


def sudoku_icon():
    cells = VGroup(*[Square(0.34).set_stroke(GREY_B, 1.5) for _ in range(9)]).arrange_in_grid(3, 3, buff=0)
    nums = VGroup()
    for i, d in [(0, "5"), (4, "3"), (8, "9"), (2, "1")]:
        nums.add(txt(d, 20).move_to(cells[i]))
    return VGroup(cells, nums)


# ---------------------------------------------------------------------------
# Chapter 2 — why it gets hard so fast
# ---------------------------------------------------------------------------

class C2Doubling(Narrated):
    def construct(self):
        self.chapter(1, "2. Why it gets hard so fast")

        def table(n):
            rows = VGroup(*[mini_row(bits, size=0.28) for bits in itertools.product([0, 1], repeat=n)])
            rows.arrange(DOWN, buff=0.04)
            return rows

        counter_lab = txt("settings", 30, GREY_A)
        counter = Integer(2, font_size=56, color=YELLOW)
        cnt = VGroup(counter, counter_lab).arrange(RIGHT, buff=0.25).move_to(3.5 * RIGHT + 0.2 * UP)
        counter_lab.add_updater(lambda m: m.next_to(counter, RIGHT, buff=0.25))

        self.narrate("2.1")
        tab = table(1).move_to(2.5 * LEFT + 0.3 * UP)
        self.cue("How many settings")
        self.play(FadeIn(tab))
        self.cue("With one switch")
        self.play(FadeIn(cnt))
        self.finish()

        times = VGroup()
        for n, beat in ((2, "2.2"), (3, "2.3")):
            self.narrate(beat)
            new = table(n).move_to(2.5 * LEFT + 0.3 * UP)
            x2 = txt("×2", 30, YELLOW).next_to(cnt, DOWN, buff=0.3 + 0.5 * len(times))
            self.play(ReplacementTransform(tab, new),
                      ChangeDecimalToValue(counter, 2 ** n), FadeIn(x2))
            times.add(x2)
            tab = new
            if n == 3:
                self.cue("A fourth")
                new = table(4).move_to(2.5 * LEFT + 0.3 * UP)
                x2 = txt("×2", 30, YELLOW).next_to(cnt, DOWN, buff=0.3 + 0.5 * len(times))
                self.play(ReplacementTransform(tab, new), ChangeDecimalToValue(counter, 16), FadeIn(x2))
                times.add(x2)
                tab = new
            self.finish()

        self.narrate("2.4")
        self.play(LaggedStart(*[Indicate(t, scale_factor=1.3) for t in times], lag_ratio=0.3))
        self.finish()

        self.narrate("2.5")
        self.play(FadeOut(VGroup(tab, cnt, times)))
        ax = Chart((10, 100), (-6, 22), 8.2, 3.9, xticks=range(10, 101, 10), yticks=(-4, 4, 12, 20),
                   yfmt=power_label, xlabel="number of switches", ylabel="seconds to try every setting")
        ax.shift(0.5 * UP + 1.6 * LEFT - ax.box.get_center())
        xl = yl = xlab = ylab = VGroup()
        line = Line(ax.c2p(10, math.log10(2 ** 10 / 1e9)), ax.c2p(100, math.log10(2 ** 100 / 1e9)))
        line.set_stroke(BLUE_C, 5)
        self.play(FadeIn(VGroup(ax, xl, yl, xlab, ylab)))
        self.cue("Suppose a computer")
        self.play(ShowCreation(line, run_time=2))
        marks = [("1 second", 1.0, "With thirty"), ("1 year", 3.156e7, "With fifty-five"),
                 ("age of the universe", 4.35e17, "With eighty-eight")]
        for label, secs, phrase in marks:
            n = math.log2(secs * 1e9)
            y = math.log10(secs)
            self.cue(phrase)
            h = DashedLine(ax.c2p(10, y), ax.c2p(100, y)).set_stroke(GREY_C, 1.5)
            d = Dot(ax.c2p(n, y), radius=0.1, fill_color=YELLOW)
            t = txt(f"{label}\n{n:.0f} switches", 22).next_to(ax.c2p(100, y), RIGHT, buff=0.2)
            self.play(ShowCreation(h), FadeIn(d, scale=2), FadeIn(t))
        self.finish()

        self.narrate("2.6")
        far = txt("real puzzles: thousands to millions of switches →", 24, YELLOW)
        far.next_to(ax.c2p(55, 22), UP, buff=0.15)
        self.play(FadeIn(far, shift=0.5 * RIGHT))
        self.finish()

        self.narrate("2.7")
        self.play(line.animate.set_stroke(YELLOW, 7))
        self.cue("When every extra switch")
        defn = card(["Exponential growth: the work is multiplied by the same factor for every switch you add."],
                    width=10, size=30).move_to(1.6 * UP)
        self.play(FadeIn(defn))
        self.finish()

        self.narrate("2.8")
        self.play(FadeOut(defn))
        self.show_gauge(2.0)
        self.play(Indicate(self.gauge_mob, scale_factor=1.15))
        self.finish()

        self.recap("2.9", ["Trying everything doubles the work with every switch:",
                           "exponential growth, with a factor of ×2 per switch."])


# ---------------------------------------------------------------------------
# Chapter 3 — fifty years of shortcuts
# ---------------------------------------------------------------------------

class C3Shortcuts(Narrated):
    def construct(self):
        self.chapter(1, "3. Fifty years of shortcuts")
        self.show_gauge(2.0)

        self.narrate("3.1")
        rule = RuleCard(None, PUZZLE_RULES[0]).move_to(2.0 * UP)
        self.play(FadeIn(rule))
        self.finish()

        self.narrate("3.2")
        branches = [("A on", "fixes 1 switch"), ("A off, B off", "fixes 2 switches"),
                    ("A off, B on, C on", "fixes 3 switches")]
        boxes = VGroup()
        for i, (setting, _) in enumerate(branches):
            boxes.add(card([setting], width=3.6, size=28))
        boxes.arrange(RIGHT, buff=0.5).move_to(1.0 * DOWN)
        edges = VGroup(*[Line(rule.box.get_bottom(), b.get_top()).set_stroke(GREY_B, 2) for b in boxes])
        for b, e, phrase in zip(boxes, edges, ["Either its first", "or the first fails", "or the first two"]):
            self.cue(phrase)
            self.play(ShowCreation(e), FadeIn(b, shift=0.2 * DOWN))
        self.finish()

        self.narrate("3.3")
        badges = VGroup(*[txt(f, 24, YELLOW).next_to(b, DOWN, buff=0.2) for (_, f), b in zip(branches, boxes)])
        self.cue("each case settles")
        self.play(LaggedStart(*[FadeIn(bd, shift=0.1 * UP) for bd in badges], lag_ratio=0.4))
        self.finish()

        self.narrate("3.4")
        self.cue("one point eight four")
        self.play(self.set_gauge(1.84))
        self.finish()

        self.narrate("3.5")
        self.play(FadeOut(VGroup(rule, boxes, edges, badges)))
        ax, chart = history_chart()
        segs, dots = step_segments(ax)
        labels = [txt("try everything: ×2", 20).next_to(dots[0], UR, buff=0.1),
                  txt("1985: ×1.62", 20).next_to(ax.c2p(1985, 1.619), UR, buff=0.1),
                  txt("1999: ×1.33", 20).next_to(ax.c2p(1999, 1.333), UR, buff=0.1),
                  txt("2014: ×1.31", 20).next_to(ax.c2p(2014, 1.308), UP, buff=0.15),
                  txt("2026: ×1.307", 20).next_to(ax.c2p(2026, 1.307), DOWN, buff=0.2)]
        self.play(FadeIn(chart), FadeIn(dots[0]), FadeIn(labels[0]), self.set_gauge(2.0, 0.5))
        for i, phrase in [(1, "By 1985"), (2, "By 1999"), (3, "Today"), (4, "Today")]:
            self.cue(phrase)
            self.play(ShowCreation(segs[i - 1]), FadeIn(dots[i]), FadeIn(labels[i]),
                      self.set_gauge(HISTORY[i][1], 0.8), run_time=0.8)
        self.play(ShowCreation(segs[4]))
        self.finish()

        self.narrate("3.6")
        graph = VGroup(chart, *segs, *dots, *labels)
        dim = FullScreenRectangle().set_fill(BLACK, 0.85).set_stroke(width=0)
        self.play(FadeIn(dim))
        big = txt("1,000,000,000,000,000,000,000,000,000,000", 34, EXP_COLOR)
        small = txt("400,000,000,000", 34, BLUE_C)
        lab1 = txt("100 switches, ×2 per switch:", 26, GREY_A)
        lab2 = txt("100 switches, ×1.307 per switch:", 26, GREY_A)
        col = VGroup(VGroup(lab1, big).arrange(DOWN, buff=0.15), VGroup(lab2, small).arrange(DOWN, buff=0.15))
        col.arrange(DOWN, buff=0.6).move_to(0.3 * UP)
        self.cue("For a hundred")
        self.play(FadeIn(col[0]))
        self.cue("and about four")
        self.play(FadeIn(col[1]))
        self.finish()

        self.narrate("3.7")
        self.play(FadeOut(col), FadeOut(dim))
        flats = VGroup(*[s[0].copy().set_stroke(YELLOW, 8) for s in segs])
        self.cue("still multiplies")
        self.play(LaggedStart(*[ShowCreation(f) for f in flats], lag_ratio=0.2, run_time=2))
        note = txt("still a fixed factor per switch", 26, YELLOW).move_to(ax.c2p(2007, 1.8))
        self.play(FadeIn(note))
        self.finish()
        self.play(FadeOut(flats))

        self.recap("3.8", ["Shortcuts lowered the factor from ×2 to about ×1.3.",
                           "But it is still a fixed factor: still exponential."])


# ---------------------------------------------------------------------------
# Chapter 4 — the bet called ETH
# ---------------------------------------------------------------------------

class C4Bet(Narrated):
    def construct(self):
        self.chapter(2, "4. The bet called ETH")
        self.show_gauge(1.31)
        ax, chart = history_chart()
        segs, dots = step_segments(ax)
        graph = VGroup(chart, *segs, *dots)

        self.narrate("4.1")
        self.play(FadeIn(graph))
        one = DashedLine(ax.c2p(1965, 1.0), ax.c2p(2030, 1.0)).set_stroke(WHITE, 3)
        self.cue("all the way down")
        self.play(ShowCreation(one))
        arrow = Arrow(ax.c2p(2027, 1.28), ax.c2p(2027, 1.05), buff=0, fill_color=YELLOW, thickness=4)
        q = txt("?", 40, YELLOW).next_to(arrow, RIGHT, buff=0.1)
        self.play(GrowArrow(arrow), FadeIn(q))
        self.finish()

        self.narrate("4.2")
        lab = txt("×1: the work stops multiplying", 24).next_to(ax.c2p(1985, 1.0), UP, buff=0.12)
        self.play(FadeIn(lab))
        self.finish()

        self.narrate("4.3")
        names = txt("Russell Impagliazzo & Ramamohan Paturi, 2001", 28, YELLOW).to_edge(UP, buff=0.9)
        self.play(FadeIn(names))
        self.cue("There is some floor")
        floor = Rectangle(width=ax.c2p(2030, 1)[0] - ax.c2p(1965, 1)[0],
                          height=ax.c2p(2000, 1.12)[1] - ax.c2p(2000, 1.0)[1])
        floor.set_fill(RED_E, 0.5).set_stroke(width=0).move_to(ax.c2p(1997.5, 1.06))
        fq = txt("a floor somewhere here?", 22).move_to(floor).shift(2.5 * RIGHT)
        self.play(FadeOut(lab), FadeIn(floor), FadeIn(fq))
        self.cue("no method")
        self.play(Indicate(floor, color=RED_C, scale_factor=1.03))
        self.finish()

        self.narrate("4.4")
        defn = card(["The Exponential Time Hypothesis (ETH):",
                     "the factor per switch can never get arbitrarily close to ×1."], width=11, size=30)
        defn.move_to(0.6 * UP)
        self.play(FadeOut(names), FadeIn(defn))
        self.cue("It's a bet")
        bet = txt("a hypothesis = never proved", 26, YELLOW).next_to(defn, DOWN, buff=0.3)
        self.play(FadeIn(bet))
        self.finish()

        self.narrate("4.5")
        self.play(FadeOut(VGroup(defn, bet, graph, one, arrow, q, floor, fq)))
        stone = Rectangle(width=6, height=0.9).set_fill(GREY_D, 1).set_stroke(GREY_B, 2).move_to(1.8 * DOWN)
        stone_lab = txt("ETH", 34).move_to(stone)
        self.play(FadeIn(stone), FadeIn(stone_lab))
        blocks = VGroup()
        texts = ["if ETH, then problem X needs …", "if ETH, then Y can't be done in …",
                 "if ETH, then Z is optimal", "if ETH, then …", "if ETH, then …", "if ETH, then …"]
        for i, t in enumerate(texts):
            b = Rectangle(width=2.9, height=0.65).set_fill(BLUE_E, 1).set_stroke(BLUE_B, 1.5)
            b.add(txt(t, 16).move_to(b))
            col, row = i % 2, i // 2
            b.move_to(stone.get_top() + UP * (0.33 + 0.67 * row) + RIGHT * (-1.48 + 2.96 * col))
            blocks.add(b)
        self.cue("Researchers built")
        self.play(LaggedStart(*[FadeIn(b, shift=0.4 * DOWN) for b in blocks], lag_ratio=0.35, run_time=3))
        self.finish()

        self.recap("4.6", ["ETH: exponential growth is unavoidable for this puzzle.",
                           "A foundation stone for many results, but never proved."])


# ---------------------------------------------------------------------------
# Chapter 5 — the new claim
# ---------------------------------------------------------------------------

class C5Claim(Narrated):
    def construct(self):
        self.chapter(3, "5. The new claim")
        self.show_gauge(1.31)

        self.narrate("5.1")
        self.cue("It keeps shrinking")
        self.play(self.set_gauge(1.25, 1.0))
        self.play(self.set_gauge(1.31, 0.6))
        self.finish()

        ax, chart, exp, sub, pol = shapes_chart()

        def label(m, s, color):
            return txt(s, 22, color).next_to(m.get_end(), RIGHT, buff=0.15)

        self.narrate("5.2")
        self.play(FadeIn(chart))
        self.cue("First, exponential")
        lexp = label(exp, "exponential", EXP_COLOR)
        self.play(ShowCreation(exp), FadeIn(lexp))
        self.finish()

        self.narrate("5.3")
        side = VGroup(txt("10 switches → 1,000 steps", 24), txt("20 switches → 8,000 steps", 24),
                      txt("(not 1,000 × 1,000)", 22, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        side.move_to(ax.c2p(7.5, 1.65))
        self.cue("Here, doubling")
        self.play(FadeIn(side))
        self.cue("Spread over")
        lpol = label(pol, "polynomial", POLY_COLOR)
        self.play(ShowCreation(pol, run_time=1.5), FadeIn(lpol))
        self.finish()

        self.narrate("5.4")
        self.play(FadeOut(side))
        lsub = label(sub, "subexponential", SUB_COLOR)
        self.play(ShowCreation(sub, run_time=4))
        self.cue("This is called")
        self.play(FadeIn(lsub))
        self.finish()

        self.narrate("5.5")
        self.play(sub.animate.set_stroke(width=8), Indicate(lsub))
        claim = card(["The claim: counting the good settings of this puzzle takes subexponential time."],
                     width=9.5, size=28).move_to(ax.c2p(7, 1.7))
        self.play(FadeIn(claim))
        self.finish()

        self.narrate("5.6")
        self.play(FadeOut(claim))
        floor = Rectangle(width=ax.c2p(12, 1)[0] - ax.c2p(2, 1)[0], height=ax.c2p(2, 1.15)[1] - ax.c2p(2, 1.0)[1])
        floor.set_fill(RED_E, 0.5).set_stroke(width=0).move_to(ax.c2p(7, 1.075))
        flab = txt("any floor (ETH)", 22).move_to(ax.c2p(4, 1.075))
        self.play(FadeIn(floor), FadeIn(flab))
        self.cue("eventually goes below")
        x_cross = 1 / (math.log2(1.15) ** 2) / math.log2(10)
        dot = Dot(ax.c2p(x_cross, 1.15), radius=0.12, fill_color=YELLOW)
        self.play(FadeIn(dot, scale=2), Flash(dot.get_center(), color=YELLOW))
        self.cue("So there is no floor")
        cross = Cross(flab, stroke_color=RED_C)
        self.play(ShowCreation(cross))
        self.finish()

        self.narrate("5.7")
        dim = FullScreenRectangle().set_fill(BLACK, 0.85).set_stroke(width=0)
        self.play(FadeIn(dim))
        formula = Tex(R"\text{cost} \approx 2^{n / \sqrt{\log n}}", font_size=72)
        nlab = txt("n = number of switches", 28, GREY_A).next_to(formula, DOWN, buff=0.5)
        VGroup(formula, nlab).move_to(0.5 * UP)
        self.play(Write(formula))
        self.play(FadeIn(nlab))
        self.cue("The square root of log n grows")
        self.play(Indicate(formula, color=YELLOW))
        self.finish()

        self.recap("5.8", ["Exponential: a fixed factor per switch.",
                           "Subexponential: the factor sinks slowly toward ×1.",
                           "The paper claims subexponential, so ETH would be false."])


# ---------------------------------------------------------------------------
# Chapter 6 — how the method works
# ---------------------------------------------------------------------------

SMALL_RULES = [[("A", 1), ("B", 0), ("C", 1)], [("B", 1), ("C", 1)]]


def small_score(rule, st):
    return int(any(st[s] == w for s, w in rule))


class C6aArithmetic(Narrated):
    def construct(self):
        self.chapter(3, "6. How the method works")
        sub = self.subtitle("Step 1: turn checking into arithmetic")
        self.play(FadeIn(sub))

        self.narrate("6a.1")
        sw = {k: Switch(k, False, scale=0.8) for k in "ABC"}
        row = VGroup(*sw.values()).arrange(RIGHT, buff=1.0).move_to(4 * LEFT + 1.2 * UP)
        r1 = RuleCard(1, SMALL_RULES[0], width=2.7).scale(0.8)
        r2 = RuleCard(2, SMALL_RULES[1], width=2.7).scale(0.8)
        rules = VGroup(r1, r2).arrange(RIGHT, buff=0.4).move_to(4 * LEFT + 1.6 * DOWN)
        self.play(FadeIn(row, lag_ratio=0.2))
        self.cue("Rule one")
        self.play(FadeIn(r1))
        self.cue("Rule two")
        self.play(FadeIn(r2))
        self.finish()

        self.narrate("6a.2")
        st = {"A": 0, "B": 0, "C": 0}
        s1 = txt("1", 60, HAPPY).next_to(r1, UP, buff=0.15)
        s2 = txt("0", 60, SAD).next_to(r2, UP, buff=0.15)
        self.cue("With every switch off")
        self.play(r1.color_by(st), r2.color_by(st))
        self.cue("so it scores one")
        self.play(FadeIn(s1, scale=1.5))
        self.cue("so it scores zero")
        self.play(FadeIn(s2, scale=1.5))
        self.finish()

        self.narrate("6a.3")
        prod = txt("1 × 0 = 0", 54).move_to(2.5 * RIGHT + 0.5 * UP)
        self.play(TransformFromCopy(VGroup(s1, s2), prod))
        self.finish()

        self.narrate("6a.4")
        st = {"A": 0, "B": 1, "C": 1}
        self.play(*[sw[k].flip(bool(v)) for k, v in st.items()], r1.color_by(st), r2.color_by(st),
                  Transform(s2, txt("1", 60, HAPPY).move_to(s2)))
        prod2 = txt("1 × 1 = 1", 54).move_to(prod)
        self.play(Transform(prod, prod2))
        self.cue("A single unhappy rule")
        zero = txt("one unhappy rule → product 0", 28, YELLOW).next_to(prod, DOWN, buff=0.4)
        self.play(FadeIn(zero))
        self.finish()

        self.narrate("6a.5")
        self.play(FadeOut(VGroup(row, rules, s1, s2, prod, zero)))
        header = ["A", "B", "C", "rule 1", "rule 2", "product"]
        widths = [0.9, 0.9, 0.9, 1.5, 1.5, 1.7]
        xs = np.cumsum([0] + widths[:-1]) + np.array(widths) / 2
        x0 = -sum(widths) / 2
        top = 2.2
        head = VGroup(*[txt(h, 26, YELLOW).move_to([x0 + x, top, 0]) for h, x in zip(header, xs)])
        rule_line = Line([x0, top - 0.25, 0], [x0 + sum(widths), top - 0.25, 0]).set_stroke(GREY_B, 1.5)
        self.play(FadeIn(head), ShowCreation(rule_line))
        rows = VGroup()
        total = 0
        for i, bits in enumerate(itertools.product([0, 1], repeat=3)):
            st = dict(zip("ABC", bits))
            a, b = small_score(SMALL_RULES[0], st), small_score(SMALL_RULES[1], st)
            total += a * b
            vals = ["on" if v else "off" for v in bits] + [str(a), str(b), str(a * b)]
            y = top - 0.55 - 0.42 * i
            r = VGroup(*[txt(v, 24, (YELLOW if (j == 5 and a * b) else WHITE)).move_to([x0 + x, y, 0])
                         for j, (v, x) in enumerate(zip(vals, xs))])
            rows.add(r)
            self.play(FadeIn(r, shift=0.1 * DOWN), run_time=0.45)
        line2 = Line([x0, top - 0.55 - 0.42 * 7.6, 0], [x0 + sum(widths), top - 0.55 - 0.42 * 7.6, 0])
        line2.set_stroke(GREY_B, 1.5)
        tot = VGroup(txt("total", 26, GREY_A).move_to([x0 + xs[4], top - 0.55 - 0.42 * 8.3, 0]),
                     txt(str(total), 34, YELLOW).move_to([x0 + xs[5], top - 0.55 - 0.42 * 8.3, 0]))
        self.cue("and add them up")
        self.play(ShowCreation(line2), FadeIn(tot))
        self.cue("The total, five")
        self.play(Indicate(tot[1], scale_factor=1.6))
        self.finish()

        self.narrate("6a.6")
        table = VGroup(head, rule_line, rows, line2, tot)
        self.play(table.animate.scale(0.8).to_edge(LEFT, buff=0.5))
        formula = card(["count = add up, over all settings,", "the product of the rule scores"], width=6.5, size=28)
        formula.move_to(3.3 * RIGHT)
        self.play(FadeIn(formula))
        self.finish()


class C6bTeams(Narrated):
    def construct(self):
        self.roadmap_mob = self.roadmap(3)
        self.add(self.roadmap_mob)
        sub = self.subtitle("Step 2: the dream of independent teams")
        self.play(FadeIn(sub))

        self.narrate("6b.1")
        t1 = team_blob(3.2 * LEFT + 0.2 * DOWN, n=10, color=ON_COLOR, seed=1, links=9)
        t2 = team_blob(3.2 * RIGHT + 0.2 * DOWN, n=10, color=ORANGE, seed=2, links=9)
        l1 = txt("team 1: 20 switches", 24, GREY_A).next_to(t1, DOWN, buff=0.1)
        l2 = txt("team 2: 20 switches", 24, GREY_A).next_to(t2, DOWN, buff=0.1)
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(l1), FadeIn(l2))
        self.cue("every rule only")
        self.play(Indicate(t1[1], color=YELLOW), Indicate(t2[1], color=YELLOW), run_time=1.5)
        self.finish()

        self.narrate("6b.2")
        c1 = txt("300 good settings", 30, YELLOW).move_to(t1)
        c2 = txt("500 good settings", 30, YELLOW).move_to(t2)
        self.cue("Count the good settings of team one")
        self.play(t1.animate.set_opacity(0.3), FadeIn(c1))
        self.cue("Count team two")
        self.play(t2.animate.set_opacity(0.3), FadeIn(c2))
        self.finish()

        self.narrate("6b.3")
        prod = txt("300 × 500 = 150,000 good settings", 36).move_to(1.5 * UP)
        self.cue("So the total")
        self.play(TransformFromCopy(VGroup(c1, c2), prod))
        self.finish()

        self.narrate("6b.4")
        self.play(FadeOut(VGroup(t1, t2, l1, l2, c1, c2, prod)))
        base = 1.9 * DOWN
        bars = VGroup()
        for i, (val, lab, color, phrase) in enumerate([(2 ** 40, "all 40 switches at once", EXP_COLOR, "Trying all"),
                                                       (2 * 2 ** 20, "two teams of 20, separately", BLUE_C, "Two teams")]):
            h = math.log10(val) / 13 * 4.0
            bar = Rectangle(width=2.2, height=h).set_fill(color, 1).set_stroke(width=0)
            bar.move_to(base + (2.5 * (1 if i else -1)) * RIGHT, aligned_edge=DOWN)
            num = txt("about 1.1 trillion settings" if i == 0 else "about 2.1 million settings", 26)
            num.next_to(bar, UP, buff=0.15)
            name = txt(lab, 24, GREY_A).next_to(bar, DOWN, buff=0.15)
            self.cue(phrase)
            self.play(GrowFromEdge(bar, DOWN), FadeIn(num), FadeIn(name))
            bars.add(VGroup(bar, num, name))
        note = txt("(bar heights on a log scale)", 20, GREY_B).to_corner(DR, buff=0.4).shift(1.2 * UP)
        self.play(FadeIn(note))
        self.finish()

        self.narrate("6b.5")
        self.play(FadeOut(VGroup(bars, note)))
        t1 = team_blob(3.2 * LEFT + 0.2 * DOWN, n=10, color=ON_COLOR, seed=1, links=9)
        t2 = team_blob(3.2 * RIGHT + 0.2 * DOWN, n=10, color=ORANGE, seed=2, links=9)
        self.play(FadeIn(t1), FadeIn(t2))
        cross = VGroup(*[Line(t1.pts[a], t2.pts[b]).set_stroke(SAD, 3) for a, b in [(0, 4), (9, 5), (1, 3), (8, 6)]])
        self.cue("some rules reach across")
        self.play(LaggedStart(*[ShowCreation(c) for c in cross], lag_ratio=0.3))
        self.finish()


class C6cTotals(Narrated):
    def construct(self):
        self.roadmap_mob = self.roadmap(3)
        self.add(self.roadmap_mob)
        sub = self.subtitle("Step 3: teams that share only a total")
        self.play(FadeIn(sub))

        t1 = team_blob(4.2 * LEFT + 0.6 * DOWN, n=6, color=ON_COLOR, seed=3, links=5, radius=1.1)
        t2 = team_blob(4.2 * RIGHT + 0.6 * DOWN, n=6, color=ORANGE, seed=4, links=5, radius=1.1)
        a, x, y = t1.dots[0], t2.dots[2], t2.dots[3]
        names = VGroup(txt("A", 24).next_to(a, UR, buff=0.05), txt("X", 24).next_to(x, UL, buff=0.05),
                       txt("Y", 24).next_to(y, DL, buff=0.05))
        rule = card(["Rule: A on, or X on, or Y on"], width=5.4, size=28).move_to(1.7 * UP)

        self.narrate("6c.1")
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(names))
        self.play(FadeIn(rule))
        links = VGroup(*[Line(rule.get_bottom(), d.get_center()).set_stroke(SAD, 2.5) for d in (a, x, y)])
        self.cue("it mentions A")
        self.play(ShowCreation(links[0]))
        self.cue("and X and Y")
        self.play(ShowCreation(links[1]), ShowCreation(links[2]))
        self.finish()

        self.narrate("6c.2")
        box = card(["how many of X, Y are on?", "0, 1 or 2"], width=4.0, size=24).move_to(0.6 * DOWN)
        self.cue("only how many")
        self.play(FadeIn(box), links[1].animate.put_start_and_end_on(box.get_right(), x.get_center()),
                  links[2].animate.put_start_and_end_on(box.get_right(), y.get_center()))
        self.cue("Let's call that number a total")
        total_word = txt("a total", 30, YELLOW).next_to(box, DOWN, buff=0.2)
        self.play(FadeIn(total_word))
        self.finish()

        self.narrate("6c.3")
        cases = [("total = 0", "rule becomes: A on", "count team 1 with A on  ×  count team 2 with 0 of X, Y on"),
                 ("total = 1", "rule is already happy", "count team 1  ×  count team 2 with 1 of X, Y on"),
                 ("total = 2", "rule is already happy", "count team 1  ×  count team 2 with 2 of X, Y on")]
        self.play(FadeOut(total_word), FadeOut(rule), FadeOut(links[0]))
        lines = VGroup()
        for i, (t, effect, product) in enumerate(cases):
            phrase = ["say at zero", "with the total fixed at one", "and at two"][i]
            self.cue(phrase)
            tag = txt(f"{t}: {effect}", 26, YELLOW).move_to(box)
            if i == 0:
                self.play(FadeOut(box), FadeIn(tag), FadeOut(links[1]), FadeOut(links[2]))
                box = tag
            else:
                self.play(Transform(box, tag))
            line = txt(("+ " if i else "") + product, 24).move_to(2.35 * UP + 0.45 * i * DOWN)
            lines.add(line)
            self.play(FadeIn(line))
        self.cue("Add the three answers up")
        self.play(Indicate(lines, color=YELLOW, scale_factor=1.03))
        self.finish()

        self.narrate("6c.4")
        self.play(FadeOut(lines))
        note = card(["If teams share only a few totals:",
                     "fix the totals, count each team separately, multiply; repeat for every value; add."],
                    width=11, size=26).move_to(1.9 * UP)
        self.play(FadeIn(note))
        self.finish()


class C6dDial(Narrated):
    def construct(self):
        self.roadmap_mob = self.roadmap(3)
        self.add(self.roadmap_mob)
        sub = self.subtitle("Step 4: the dial")
        self.play(FadeIn(sub))

        t1 = team_blob(3.6 * LEFT + 0.35 * UP, n=7, color=ON_COLOR, seed=5, links=6, radius=1.1)
        t2 = team_blob(1.0 * RIGHT + 0.35 * UP, n=7, color=ORANGE, seed=6, links=6, radius=1.1)
        cross = VGroup(*[Line(t1.pts[a], t2.pts[b]).set_stroke(SAD, 2.5) for a, b in [(0, 3), (6, 4), (1, 2), (5, 3)]])
        d = dial(0).move_to(5.2 * RIGHT + 0.6 * UP)

        self.narrate("6d.1")
        self.play(FadeIn(t1), FadeIn(t2), FadeIn(cross))
        self.cue("So the paper")
        self.play(FadeIn(d))
        self.cue("It changes the arithmetic")
        arith = txt("add up, over all settings, the product of the rule scores", 24, GREY_A).to_edge(UP, buff=1.45)
        self.play(FadeIn(arith))
        self.finish()

        self.narrate("6d.2")
        rule = card(["Rule: A on, or B off, or C on"], width=5.2, size=28).move_to(1.95 * DOWN + 1.5 * LEFT)
        self.play(FadeIn(rule))
        self.cue("each switch is replaced")
        blend = card(["Rule: A on, or B off, or (a blend of C and other switches) on"], width=9, size=24)
        blend.move_to(rule).shift(0.6 * RIGHT)
        self.play(Transform(rule, blend))
        self.cue("and the dial controls")
        self.play(turn_dial(d, 0.5, 0.8))
        self.play(turn_dial(d, 0.0, 0.8))
        self.finish()

        self.narrate("6d.3")
        exact = txt("dial at 0: no blending  =  the true count", 30, HAPPY).move_to(1.95 * DOWN)
        self.play(FadeOut(rule), FadeIn(exact), Indicate(d.needle, color=HAPPY))
        self.finish()

        self.narrate("6d.4")
        self.play(FadeOut(exact))
        self.cue("one, two, three")
        self.play(turn_dial(d, 1.0, 1.2))
        mid = (t1.get_center() + t2.get_center()) / 2
        tbox = card(["a few", "totals"], width=1.6, size=22).move_to(mid)
        greens = VGroup(Line(t1.pts[0], tbox.get_left()).set_stroke(HAPPY, 3),
                        Line(t1.pts[6], tbox.get_left()).set_stroke(HAPPY, 3),
                        Line(tbox.get_right(), t2.pts[3]).set_stroke(HAPPY, 3),
                        Line(tbox.get_right(), t2.pts[4]).set_stroke(HAPPY, 3))
        self.cue("every rule sees")
        self.play(FadeOut(cross), FadeIn(tbox), ShowCreation(greens))
        self.cue("Exactly the situation")
        self.play(Indicate(tbox, color=YELLOW))
        self.finish()

        self.narrate("6d.5")
        note = card(["At dial 1, 2, 3, …: fast to compute.", "But the answer is not a count: just a number."],
                    width=9.5, size=28).move_to(1.95 * DOWN)
        self.play(FadeIn(note))
        self.cue("The count we want")
        self.play(turn_dial(d, 0.0, 1.0))
        self.play(turn_dial(d, 1.0, 1.0))
        self.finish()

        self.narrate("6d.6")
        self.play(FadeOut(note))
        line = txt("fast at 1, 2, 3, …        the answer we want is at 0", 30, YELLOW).move_to(1.95 * DOWN)
        self.play(FadeIn(line))
        self.finish()


def curve_axes():
    ax = Axes(x_range=(-0.25, 3.5, 0.5), y_range=(-5, 40, 10), width=8.0, height=3.9,
              axis_config=dict(stroke_color=GREY_B, include_tip=False))
    ax.move_to(0.45 * UP + 1.6 * LEFT)
    xl = VGroup(*[txt(str(v), 22, GREY_B).next_to(ax.c2p(v, -5), DOWN, buff=0.15) for v in range(0, 4)])
    yl = VGroup(*[txt(str(v), 20, GREY_B).next_to(ax.c2p(-0.25, v), LEFT, buff=0.12) for v in (0, 10, 20, 30, 40)])
    xlab = txt("dial", 24, GREY_A).next_to(ax.c2p(3.5, -5), RIGHT, buff=0.2)
    ylab = txt("the number", 22, GREY_A).next_to(ax.c2p(-0.25, 40), UP, buff=0.15)
    zero_line = DashedLine(ax.c2p(-0.25, 0), ax.c2p(3.5, 0)).set_stroke(GREY_D, 1)
    return ax, VGroup(ax, xl, yl, xlab, ylab, zero_line)


def h_alt(c):
    return lambda x: poly(H_COEFFS, x) + c * (x - 1) * (x - 2) * (x - 3)


def h_slope(x):
    return sum(k * c * x ** (k - 1) for k, c in enumerate(H_COEFFS) if k)


class C6eCurve(Narrated):
    def construct(self):
        self.roadmap_mob = self.roadmap(3)
        self.add(self.roadmap_mob)
        sub = self.subtitle("Step 5: from the easy points back to zero")
        self.play(FadeIn(sub))
        ax, frame = curve_axes()
        d = dial(0, radius=0.6).move_to(5.6 * RIGHT + 1.2 * UP)
        def poly_fn(x):
            return poly(H_COEFFS, x)

        true = curve(ax, poly_fn, -0.2, 3.25, color=BLUE_C, ylim=(-6, 42))

        self.narrate("6e.1")
        self.play(FadeIn(frame), FadeIn(d))
        tracker = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(ax.c2p(tracker.get_value(), poly_fn(tracker.get_value())), fill_color=YELLOW))
        self.add(dot)
        self.cue("It traces a curve")
        self.play(tracker.animate.set_value(3.2), ShowCreation(true), turn_dial(d, 3.2, 3.0), run_time=3.0)
        self.remove(dot)
        self.cue("can only wiggle")
        self.play(Indicate(true, color=YELLOW, scale_factor=1.02))
        self.finish()

        self.narrate("6e.2")
        pts = VGroup(*[Dot(ax.c2p(t, poly_fn(t)), radius=0.11, fill_color=POINT) for t in (1, 2, 3)])
        q = txt("?", 48, YELLOW).move_to(ax.c2p(0, 16))
        self.play(true.animate.set_stroke(opacity=0), FadeIn(pts, lag_ratio=0.3))
        self.cue("We want its height")
        self.play(FadeIn(q, scale=1.5))
        self.finish()

        self.narrate("6e.3")
        alts = VGroup(*[curve(ax, h_alt(c), -0.2, 3.25, color=GREY_B, width=2.5, ylim=(-6, 42))
                        for c in (-2, -1, 0, 1, 2)])
        ends = VGroup(*[Dot(ax.c2p(0, h_alt(c)(0)), radius=0.08, fill_color=GREY_B) for c in (-2, -1, 0, 1, 2)])
        self.play(FadeOut(q), LaggedStart(*[ShowCreation(a) for a in alts], lag_ratio=0.25, run_time=3))
        self.cue("At zero, they disagree")
        self.play(FadeIn(ends, lag_ratio=0.2))
        vals = txt("2?  8?  14?  20?  26?", 26, YELLOW).next_to(ax.c2p(0, 30), RIGHT, buff=0.3)
        self.play(FadeIn(vals))
        self.finish()

        self.narrate("6e.4")
        inset_box = RoundedRectangle(width=3.6, height=2.4, corner_radius=0.15).set_stroke(GREY_B, 1.5)
        inset_box.set_fill(BLACK, 1).move_to(4.9 * RIGHT + 1.3 * DOWN)
        hx = ValueTracker(-1.2)
        o = inset_box.get_center() + 0.6 * DOWN

        def hill(x):
            return 1.1 * math.exp(-x * x / 0.9)

        hill_curve = VMobject().set_points_smoothly([o + np.array([x, hill(x), 0]) for x in np.linspace(-1.6, 1.6, 50)])
        hill_curve.set_stroke(GREEN_D, 4)

        def walker():
            x = hx.get_value()
            p = o + np.array([x, hill(x), 0])
            s = -2 * x / 0.9 * hill(x)
            v = np.array([1, s, 0]) / math.sqrt(1 + s * s)
            return VGroup(Line(p - 0.55 * v, p + 0.55 * v).set_stroke(POINT, 5), Dot(p, radius=0.08, fill_color=WHITE))

        w = always_redraw(walker)
        slope_lab = txt("slope = how steeply it climbs", 22).next_to(inset_box, UP, buff=0.12)
        self.play(FadeIn(inset_box), d.animate.set_opacity(0))
        self.cue("Not just the height")
        self.play(ShowCreation(hill_curve), FadeIn(slope_lab))
        self.add(w)
        self.cue("how steeply")
        self.play(hx.animate.set_value(1.2), run_time=3.5)
        self.finish()

        self.narrate("6e.5")
        self.remove(w)
        self.play(FadeOut(VGroup(inset_box, hill_curve, slope_lab, vals)))
        ticks = VGroup()
        for t in (1, 2, 3):
            s = h_slope(t)
            sx, sy = ax.x_axis.get_unit_size(), ax.y_axis.get_unit_size()
            v = np.array([sx, s * sy, 0])
            v = v / np.linalg.norm(v)
            p = ax.c2p(t, poly_fn(t))
            ticks.add(Line(p - 0.6 * v, p + 0.6 * v).set_stroke(POINT, 7, opacity=0.8))
        self.cue("Once the slopes")
        self.play(LaggedStart(*[ShowCreation(t) for t in ticks], lag_ratio=0.3))
        self.cue("only one curve fits")
        keep = alts[2]
        self.play(*[FadeOut(a) for i, a in enumerate(alts) if i != 2],
                  *[FadeOut(e) for i, e in enumerate(ends) if i != 2], keep.animate.set_stroke(BLUE_C, 5))
        self.cue("it lands on fourteen")
        ring = Circle(radius=0.2).set_stroke(HAPPY, 5).move_to(ax.c2p(0, 14))
        fourteen = txt("14", 40, HAPPY).next_to(ring, UR, buff=0.1)
        self.play(ShowCreation(ring), FadeIn(fourteen, scale=1.5))
        self.finish()

        self.narrate("6e.6")
        check = card(["A real example from our code: 6 switches.", "Trying every setting also gives 14."],
                     width=4.3, size=24).move_to(4.85 * RIGHT + 0.9 * DOWN)
        self.play(FadeIn(check))
        self.finish()

        self.narrate("6e.7")
        self.play(FadeOut(check))
        more = card(["Wigglier curves need more at each point:", "height, slope, bend, and so on."],
                    width=4.3, size=24).move_to(4.85 * RIGHT + 0.9 * DOWN)
        self.play(FadeIn(more))
        self.finish()


class C6fBalance(Narrated):
    def construct(self):
        self.roadmap_mob = self.roadmap(3)
        self.add(self.roadmap_mob)
        sub = self.subtitle("The balancing act, and the rest")
        self.play(FadeIn(sub))

        self.narrate("6f.1")
        fulcrum = Triangle().set_fill(GREY_D, 1).set_stroke(GREY_B, 2).scale(0.5).move_to(1.2 * DOWN)
        beam = Rectangle(width=8, height=0.15).set_fill(GREY_B, 1).set_stroke(width=0)
        beam.next_to(fulcrum, UP, buff=0)
        left = card(["few wiggles"], width=2.8, size=26).next_to(beam.get_left(), UP, buff=0.05).shift(0.9 * RIGHT)
        right = card(["many easy points"], width=3.2, size=26).next_to(beam.get_right(), UP, buff=0.05).shift(
            1.0 * LEFT)
        saw = VGroup(beam, left, right)
        pivot = beam.get_center()
        self.play(FadeIn(fulcrum), FadeIn(saw))
        self.cue("Every extra piece")
        cost = txt("every extra piece of information costs work", 26, GREY_A).move_to(2.3 * UP)
        self.play(FadeIn(cost))
        self.cue("pull against each other")
        self.play(Rotate(saw, 0.18, about_point=pivot), run_time=1)
        self.play(Rotate(saw, -0.36, about_point=pivot), run_time=1.2)
        self.play(Rotate(saw, 0.18, about_point=pivot), run_time=1)
        self.finish()

        self.narrate("6f.2")
        inv = txt("the paper's main invention", 32, YELLOW).move_to(2.3 * UP)
        self.play(FadeOut(cost), FadeIn(inv), Indicate(saw, color=YELLOW, scale_factor=1.03))
        self.cue("most of the mixing cancels")
        note = txt("most of the blending cancels out; a small leftover is tracked with totals", 24, GREY_A)
        note.move_to(1.7 * UP)
        self.play(FadeIn(note))
        self.finish()

        self.narrate("6f.3")
        self.play(FadeOut(VGroup(fulcrum, saw, inv, note)))
        tidy = team_blob(3.5 * LEFT + 0.2 * DOWN, n=9, color=ON_COLOR, seed=7, links=5, radius=1.3)
        messy = team_blob(3.5 * RIGHT + 0.2 * DOWN, n=9, color=ON_COLOR, seed=8, links=22, radius=1.3)
        tl = txt("tidy: each switch in few rules", 24, GREY_A).next_to(tidy, DOWN, buff=0.1)
        ml = txt("any puzzle", 24, GREY_A).next_to(messy, DOWN, buff=0.1)
        self.play(FadeIn(tidy), FadeIn(tl))
        self.cue("The paper shows")
        arrow = Arrow(messy.get_left(), tidy.get_right(), buff=0.3, fill_color=YELLOW, thickness=4)
        alab = txt("split into tidy pieces", 24, YELLOW).next_to(arrow, UP, buff=0.1)
        self.play(FadeIn(messy), FadeIn(ml))
        self.play(GrowArrow(arrow), FadeIn(alab))
        self.finish()

        self.narrate("6f.4")
        self.play(FadeOut(VGroup(tidy, messy, tl, ml, arrow, alab)))
        steps = ["scores", "dial", "teams + totals", "curve", "back to 0"]
        boxes = VGroup(*[card([s], width=2.2, size=24) for s in steps]).arrange(RIGHT, buff=0.45).move_to(0.3 * UP)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, fill_color=GREY_B, thickness=4)
                          for a, b in zip(boxes, boxes[1:])])
        for i, phrase in enumerate(["Turn counting", "Add a dial", "At special settings", "Measure the curve",
                                    "follow it back"]):
            self.cue(phrase)
            anims = [FadeIn(boxes[i], shift=0.1 * RIGHT)]
            if i:
                anims.append(GrowArrow(arrows[i - 1]))
            self.play(*anims, run_time=0.6)
        self.finish()

        self.narrate("6f.5")
        self.show_gauge(1.31)
        self.cue("each part grows")
        self.play(self.set_gauge(1.05, 4.0))
        self.finish()


# ---------------------------------------------------------------------------
# Chapter 7 — the catch
# ---------------------------------------------------------------------------

def catch_data():
    sys.path.insert(0, str(HERE.parent / "code"))
    import make_figures as MF
    lams = [10 ** (math.log10(MF.LAMBDA0) + i / 100) for i in range(0, 501)]
    pts = [(math.log10(l * math.log10(2)), 2 ** sum(MF.cost_terms(int(l)))) for l in lams]
    x_brute = math.log10(MF.crossing(1.0) * math.log10(2))
    x_best = math.log10(MF.crossing(math.log2(MF.PPSZ_BEST[0])) * math.log10(2))
    return pts, x_brute, x_best


class C7Catch(Narrated):
    def construct(self):
        self.chapter(4, "7. The catch")

        self.narrate("7.1")
        q = txt("So is this a fast new puzzle solver?", 40).move_to(0.5 * UP)
        self.play(FadeIn(q))
        self.cue("No")
        no = txt("No.", 60, SAD).next_to(q, DOWN, buff=0.5)
        self.play(FadeIn(no, scale=1.4))
        self.finish()

        self.narrate("7.2")
        self.play(FadeOut(VGroup(q, no)))
        pts, x_brute, x_best = catch_data()
        ax = Chart((9.5, 14.5), (1.0, 3.0), 8.2, 3.9, xticks=range(10, 15), yticks=(1.0, 1.5, 2.0, 2.5, 3.0),
                   xfmt=power_label, yfmt=times_label, xlabel="how many DIGITS the number of switches has",
                   ylabel="average work per switch")
        ax.shift(0.5 * UP + 1.6 * LEFT - ax.box.get_center())
        xl = yl = xlab = ylab = VGroup()
        two = Line(ax.c2p(9.5, 2.0), ax.c2p(14.5, 2.0)).set_stroke(EXP_COLOR, 4)
        best = Line(ax.c2p(9.5, 1.307), ax.c2p(14.5, 1.307)).set_stroke(POLY_COLOR, 4)
        lab2 = txt("try everything ×2", 22).next_to(two.get_end(), RIGHT, buff=0.15)
        labb = txt("best old method ×1.307", 22).next_to(best.get_end(), RIGHT, buff=0.15)
        new = VMobject().set_points_smoothly([ax.c2p(x, y) for x, y in pts if 9.5 <= x <= 14.5])
        new.set_stroke(SUB_COLOR, 5)
        labn = txt("the new method", 22).next_to(new.get_end(), RIGHT, buff=0.15)
        self.play(FadeIn(VGroup(ax, xl, yl, xlab, ylab)), ShowCreation(two), ShowCreation(best),
                  FadeIn(lab2), FadeIn(labb))
        self.cue("We took the explicit")
        self.play(ShowCreation(new, run_time=3), FadeIn(labn))
        self.finish()

        self.narrate("7.3")
        d1 = Dot(ax.c2p(x_brute, 2.0), radius=0.12, fill_color=YELLOW)
        t1 = txt("about 18 billion digits", 24, YELLOW).next_to(d1, UR, buff=0.15)
        self.play(FadeIn(d1, scale=2), FadeIn(t1))
        self.cue("Not eighteen billion switches")
        self.play(Indicate(t1, scale_factor=1.15))
        self.finish()

        self.narrate("7.4")
        d2 = Dot(ax.c2p(x_best, 1.307), radius=0.12, fill_color=YELLOW)
        t2 = txt("about 340 billion digits", 24, YELLOW).next_to(d2, UR, buff=0.15)
        self.play(FadeIn(d2, scale=2), FadeIn(t2))
        self.cue("For comparison")
        atoms = card(["atoms in the observable universe:", "a number with about 80 digits"], width=4.0, size=22)
        atoms.move_to(5.05 * RIGHT + 1.75 * UP)
        self.play(FadeIn(atoms))
        self.finish()

        self.narrate("7.5")
        note = txt("rough figures, from an analysis that wasn't trying to be efficient", 22, GREY_A)
        note.next_to(ax, UP, buff=0.25)
        self.play(FadeIn(note))
        self.finish()

        self.recap("7.6", ["Not practical.", "What matters is what it proves is possible."])


# ---------------------------------------------------------------------------
# Chapter 8 — what it means
# ---------------------------------------------------------------------------

class C8Meaning(Narrated):
    def construct(self):
        self.chapter(4, "8. What it means, and what it doesn't")

        self.narrate("8.1")
        stone = Rectangle(width=6, height=0.9).set_fill(GREY_D, 1).set_stroke(GREY_B, 2).move_to(1.8 * DOWN)
        crack = VMobject().set_points_as_corners([stone.get_top() + 0.3 * LEFT, stone.get_center() + 0.1 * RIGHT,
                                                  stone.get_center() + 0.2 * LEFT + 0.1 * DOWN,
                                                  stone.get_bottom() + 0.1 * RIGHT]).set_stroke(BLACK, 5)
        stone_lab = txt("ETH", 34).move_to(stone).shift(1.5 * LEFT)
        blocks = VGroup()
        for i in range(6):
            b = Rectangle(width=2.9, height=0.65).set_fill(BLUE_E, 1).set_stroke(BLUE_B, 1.5)
            b.add(txt("if ETH, then …", 16).move_to(b))
            col, row = i % 2, i // 2
            b.move_to(stone.get_top() + UP * (0.33 + 0.67 * row) + RIGHT * (-1.48 + 2.96 * col))
            blocks.add(b)
        self.play(FadeIn(stone), FadeIn(stone_lab), FadeIn(blocks))
        self.cue("ETH is false")
        self.play(ShowCreation(crack), Flash(stone.get_center(), color=RED_C))
        self.cue("lose their footing")
        self.play(*[b.animate.rotate(0.12 * (1 if i % 2 else -1)).shift(0.1 * DOWN) for i, b in enumerate(blocks)])
        self.cue("Some can be rescued")
        pillars = VGroup()
        for x in (-4.2, 4.2):
            p = Rectangle(width=1.3, height=2.6).set_fill(GREEN_E, 1).set_stroke(GREEN_B, 1.5)
            p.move_to([x, -0.65, 0])
            p.add(txt("other\nassumptions", 16).move_to(p))
            pillars.add(p)
        self.play(FadeIn(pillars, shift=0.3 * UP))
        self.cue("Others will need")
        self.play(blocks[4:].animate.set_opacity(0.3))
        self.finish()

        self.narrate("8.2")
        self.play(FadeOut(VGroup(stone, crack, stone_lab, blocks, pillars)))
        pnp = card(["P vs NP", "one of the seven Millennium Prize Problems   ·   $1,000,000"], width=10, size=30)
        pnp.move_to(0.8 * UP)
        self.play(FadeIn(pnp))
        self.finish()

        self.narrate("8.3")
        ax, chart, exp, sub, pol = shapes_chart()
        self.play(pnp.animate.scale(0.55).move_to(5.3 * RIGHT + 0.9 * UP), FadeIn(chart), FadeIn(exp), FadeIn(pol),
                  FadeIn(sub))
        lp = txt("P = NP would need this kind", 22, POLY_COLOR).next_to(ax.c2p(7, 1.0), UP, buff=0.12)
        self.cue("polynomial growth")
        self.play(pol.animate.set_stroke(width=8), FadeIn(lp))
        self.finish()

        self.narrate("8.4")
        ls = txt("what the paper claims", 22, SUB_COLOR).next_to(sub.get_end(), UP, buff=0.15).shift(0.6 * LEFT)
        self.play(sub.animate.set_stroke(width=8), FadeIn(ls))
        self.cue("So P versus NP stays open")
        self.play(Indicate(pnp, color=YELLOW))
        self.finish()

        self.narrate("8.5")
        self.play(FadeOut(VGroup(chart, exp, sub, pol, lp, ls, pnp)))
        lock = padlock_icon().move_to(3 * LEFT + 0.3 * UP)
        laptop = laptop_icon().move_to(3 * RIGHT + 0.3 * UP)
        l1 = txt("not broken encryption", 26).next_to(lock, DOWN, buff=0.4)
        l2 = txt("not a faster solver", 26).next_to(laptop, DOWN, buff=0.4)
        self.play(FadeIn(lock), FadeIn(l1))
        self.play(ShowCreation(Cross(lock, stroke_color=RED_C)))
        self.cue("And it doesn't give")
        self.play(FadeIn(laptop), FadeIn(l2))
        self.play(ShowCreation(Cross(laptop, stroke_color=RED_C)))
        self.finish()

        self.recap("8.6", ["It changes what is possible in principle.",
                           "Not P vs NP. Not encryption. Not practice."])


def padlock_icon():
    body = RoundedRectangle(width=1.4, height=1.1, corner_radius=0.12).set_fill(YELLOW_E, 1).set_stroke(width=0)
    shackle = Arc(0, PI, radius=0.45).set_stroke(GREY_B, 10).next_to(body, UP, buff=-0.05)
    hole = Circle(radius=0.1).set_fill(BLACK, 1).set_stroke(width=0).move_to(body)
    return VGroup(shackle, body, hole)


def laptop_icon():
    screen = RoundedRectangle(width=2.0, height=1.3, corner_radius=0.08).set_stroke(GREY_B, 3)
    base = Polygon(LEFT * 1.25, RIGHT * 1.25, RIGHT * 1.05 + UP * 0.18, LEFT * 1.05 + UP * 0.18)
    base.set_fill(GREY_C, 1).set_stroke(width=0).next_to(screen, DOWN, buff=0.03)
    lines = VGroup(*[Line(LEFT * 0.7, RIGHT * (0.7 - 0.3 * i)).set_stroke(GREEN_C, 3) for i in range(3)])
    lines.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(screen)
    return VGroup(screen, base, lines)


# ---------------------------------------------------------------------------
# Chapter 9 — is it true?
# ---------------------------------------------------------------------------

class C9Status(Narrated):
    def construct(self):
        self.chapter(4, "9. Is it true?")

        self.narrate("9.1")
        c = card(["Preprint: not yet peer reviewed.", "Written by an AI model at OpenAI."], width=9, size=30)
        c.move_to(1.0 * UP)
        self.play(FadeIn(c))
        self.finish()

        self.narrate("9.2")
        doc = VGroup(Rectangle(width=1.4, height=1.8).set_stroke(GREY_B, 2),
                     *[Line(LEFT * 0.45, RIGHT * 0.45).set_stroke(GREY_C, 2).shift(UP * (0.5 - 0.25 * i))
                       for i in range(4)])
        tick = txt("✓", 60, HAPPY).next_to(doc, DR, buff=-0.35)
        lean = VGroup(doc, tick).move_to(4 * LEFT + 1.0 * DOWN)
        t = VGroup(txt("Lean: a computer checks every logical step", 26),
                   txt("covers a slightly weaker version, which still breaks ETH", 24, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).next_to(lean, RIGHT, buff=0.6)
        self.play(c.animate.shift(0.6 * UP))
        self.cue("checked by computer")
        self.play(FadeIn(lean), FadeIn(t[0]))
        self.cue("That check covers")
        self.play(FadeIn(t[1]))
        self.finish()

        self.narrate("9.3")
        self.play(FadeOut(VGroup(c, lean, t)))
        names = VGroup(*[txt(n, 34) for n in ["Russell Impagliazzo", "Ramamohan Paturi", "Ryan Williams"]])
        names.arrange(DOWN, buff=0.35).move_to(0.6 * UP)
        lab = txt("among the experts examining the proof", 26, GREY_A).next_to(names, DOWN, buff=0.5)
        self.play(LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.3), FadeIn(lab))
        self.finish()

        self.narrate("9.4")
        self.play(FadeOut(VGroup(names, lab)))
        term = RoundedRectangle(width=10, height=3.6, corner_radius=0.15).set_stroke(GREY_B, 2).set_fill(BLACK, 1)
        term.move_to(0.4 * UP)
        head = txt("$ python code/toy_eth.py", 24, GREY_A).next_to(term.get_corner(UL), DR, buff=0.3)
        checks = ["dial at 0 gives back the real puzzle", "at dial 1, 2, 3 the teams separate",
                  "values and slopes recover the curve", "11 random small puzzles: exact count matches trying everything"]
        lines = VGroup(*[txt("✓ " + c_, 24, HAPPY) for c_ in checks]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        lines.next_to(head, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(term), FadeIn(head))
        self.play(LaggedStart(*[FadeIn(l, shift=0.1 * RIGHT) for l in lines], lag_ratio=0.5, run_time=3))
        self.finish()


# ---------------------------------------------------------------------------
# Chapter 10 — closing
# ---------------------------------------------------------------------------

class C10Close(Narrated):
    def construct(self):
        self.narrate("10.1")
        big = self.roadmap(-1, big=True).move_to(2.2 * UP)
        self.play(FadeIn(big, lag_ratio=0.2))
        row = VGroup(*[Switch(k, False, scale=0.8) for k in "ABCDEFGH"]).arrange(RIGHT, buff=0.35).move_to(0.2 * DOWN)
        self.cue("A puzzle of switches")
        self.play(FadeIn(row, lag_ratio=0.1))
        self.cue("Fifty years")
        rng = random.Random(3)
        for _ in range(4):
            self.play(*[s.flip(rng.random() < 0.5, run_time=0.3) for s in row])
        self.finish()

        self.narrate("10.2")
        self.play(FadeOut(row))
        ax = Axes(x_range=(-0.25, 3.5, 0.5), y_range=(-5, 40, 10), width=6, height=3,
                  axis_config=dict(stroke_color=GREY_B, include_tip=False)).move_to(0.6 * DOWN)
        d = dial(3, radius=0.55).move_to(4.8 * RIGHT + 0.6 * DOWN)
        c = curve(ax, lambda x: poly(H_COEFFS, x), -0.2, 3.25, color=BLUE_C, ylim=(-6, 42))
        pts = VGroup(*[Dot(ax.c2p(t, poly(H_COEFFS, t)), radius=0.09, fill_color=POINT) for t in (1, 2, 3)])
        self.play(FadeIn(ax), FadeIn(d), FadeIn(pts))
        self.cue("follows a curve")
        self.play(ShowCreation(c, run_time=2), turn_dial(d, 0.0, 2.0))
        ring = Circle(radius=0.18).set_stroke(HAPPY, 5).move_to(ax.c2p(0, 14))
        self.play(ShowCreation(ring))
        self.finish()

        self.narrate("10.3")
        self.play(FadeOut(VGroup(ax, d, c, pts, ring, big)))
        title = txt("The Exponential Time Hypothesis is False", 48)
        links = VGroup(txt("Explainer, figures and code:", 26, GREY_A),
                       txt("github.com/htt210/awesome-millennium", 28, YELLOW)).arrange(DOWN, buff=0.15)
        links.next_to(title, DOWN, buff=0.6)
        self.play(Write(title))
        self.play(FadeIn(links))
        self.finish(3.0)
        self.clear_caption()
        self.wait(1)


class Thumbnail(Scene):
    def construct(self):
        title = txt("The Exponential Time Hypothesis is False", 54).to_edge(UP, buff=0.6)
        row = VGroup(*[Switch(k, v, scale=0.9) for k, v in zip("ABCDEF", [1, 0, 1, 1, 0, 1])])
        row.arrange(RIGHT, buff=0.4).move_to(1.0 * UP)
        ax = Axes(x_range=(-0.25, 3.5, 0.5), y_range=(-5, 40, 10), width=7, height=3.2,
                  axis_config=dict(stroke_color=GREY_B, include_tip=False)).move_to(2.0 * DOWN + 1.2 * LEFT)
        c = curve(ax, lambda x: poly(H_COEFFS, x), -0.2, 3.25, color=BLUE_C, width=6, ylim=(-6, 42))
        pts = VGroup(*[Dot(ax.c2p(t, poly(H_COEFFS, t)), radius=0.1, fill_color=POINT) for t in (1, 2, 3)])
        ring = Circle(radius=0.2).set_stroke(HAPPY, 6).move_to(ax.c2p(0, 14))
        d = dial(0, radius=0.7).move_to(4.6 * RIGHT + 2.0 * DOWN)
        sub = txt("explained for everyone", 30, GREY_A).next_to(title, DOWN, buff=0.25)
        self.add(title, sub, row, ax, c, pts, ring, d)
