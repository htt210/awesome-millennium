"""Shared machinery for narrated explainer videos (3b1b's manim, manimgl 1.7.2).

A video directory holds a `storyboard.md` (the reviewed script: for every beat,
what is on screen and the exact narration) and a scene file. The scene file
subclasses `Narrated`, points it at the storyboard, and calls
`self.narrate("1.4")` in its scenes: the words of beat 1.4 appear as captions
and, with NARRATION_VOICES set, are spoken by voice.py while the following
animations play; `finish()` waits for the voice. Each scene logs what it said
and when to build/captions/<Scene>.json, which make_captions.py and
make_voiceover.py turn into captions, a script and the soundtracks.

    import sys; sys.path.insert(0, "<repo>/tools/video")
    from narrated import *

    class Video(Narrated):
        STORY = load_storyboard(HERE / "storyboard.md")
        ROADMAP = ["The puzzle", "Why it's hard", ...]
        PRONOUNCE = [(r"\\bETH\\b", "E T H")]     # written form -> spoken form
        BUILD = HERE / "build"

The ETH video (papers/2026/10/eth-is-false/video) predates this module and
keeps its own copy of the same code.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

from manimlib import *
import random  # noqa: E402,F811  (after the star import, which may shadow it)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from voice import voices_from_env  # noqa: E402

SERIF = "CMU Serif"
LEAD = 0.25          # the voice starts this long after its caption appears
CHUNK_GAP = 0.3      # silence between two captions of one beat
BEAT_PAUSE = 1.25    # silence after a beat (plus the next beat's lead: about 1.5 s)
RECAP_PAUSE = 3.0


# ---------------------------------------------------------------------------
# the script
# ---------------------------------------------------------------------------

def load_storyboard(path: Path) -> dict[str, str]:
    """Beat id -> narration, from the tables of a storyboard.md."""
    beats = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(\d+[a-f]?\.\d+)\s*\|(.*)\|(.*)\|\s*$", line)
        if m:
            beats[m.group(1)] = m.group(3).strip()
    return beats


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


def curve(ax, f, x0, x1, n=200, color=BLUE, width=4, ylim=None):
    """The graph of f on [x0, x1] in chart coordinates, dropping points outside ylim."""
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = f(x)
        if ylim and not (ylim[0] <= y <= ylim[1]):
            continue
        pts.append(ax.c2p(x, y))
    m = VMobject().set_points_smoothly(pts) if len(pts) > 2 else VMobject()
    return m.set_stroke(color, width)


# ---------------------------------------------------------------------------
# the narrated scene
# ---------------------------------------------------------------------------

class Narrated(Scene):
    """Captions and voice for the beats of a storyboard, plus the road map."""

    STORY: dict[str, str] = {}
    ROADMAP: list[str] = []
    PRONOUNCE: list[tuple[str, str]] = []
    BUILD: Path = Path("build")

    def setup(self):
        super().setup()
        self.voices = voices_from_env(self.BUILD / "voice")
        self.log = []
        self.beat_end = 0.0
        self.chunks = []
        self.beat_chunks = []
        self.caption_box = VGroup().fix_in_frame()
        self.current_caption = None
        self.caption_box.add_updater(lambda m: self._update_caption())
        self.add(self.caption_box)
        self.roadmap_mob = None
        self.chapter_title = type(self).__name__

    # -- narration ----------------------------------------------------------
    def spoken(self, text: str) -> str:
        for pattern, said in self.PRONOUNCE:
            text = re.sub(pattern, said, text)
        return text

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
            self.log.append({"start": round(float(c["shown_real"]), 3), "end": round(float(self.time), 3),
                             "text": c["text"], "say": c["say"], "voice_at": round(float(c["voice_at"]), 3)})
            self.current_caption = None
            self.caption_box.set_submobjects([])

    def narrate(self, beat: str):
        """Start beat `beat`: its captions and voice run while the following
        animations play. Call finish() to wait for the end."""
        if self.time < self.beat_end:
            self.wait(self.beat_end - self.time)
        text = self.STORY[beat]
        self.chunks = [c for c in self.chunks if c is self.current_caption]
        t = self.time
        for i, chunk in enumerate(caption_chunks(text) if text else []):
            said = self.spoken(chunk)
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

    def clear_content(self, *keep):
        """Fade out everything except captions, the road map and `keep`."""
        gone = [m for m in self.mobjects if m not in (self.caption_box, self.roadmap_mob, *keep)]
        if gone:
            self.play(FadeOut(Group(*gone)))

    def content(self) -> Group:
        """Everything on screen except captions and the road map."""
        keep = {self.caption_box, self.roadmap_mob}
        return Group(*[m for m in self.mobjects if m not in keep])

    # -- signposts -------------------------------------------------------------
    def roadmap(self, active: int | None, big=False) -> VGroup:
        boxes = VGroup()
        for i, name in enumerate(self.ROADMAP):
            lit = active is not None and (i == active or active == -1)
            box = RoundedRectangle(width=2.05, height=0.5, corner_radius=0.1)
            box.set_fill(YELLOW if lit else BLACK, 1).set_stroke(YELLOW if lit else GREY_D, 1.5)
            label = txt(name, 22, GREY_B)
            if lit:
                label.set_fill(BLACK, 1)
            label.move_to(box)
            boxes.add(VGroup(box, label))
        boxes.arrange(RIGHT, buff=0.12)
        if big:
            boxes.scale(1.3)
        else:
            boxes.scale(0.75).to_corner(UL, buff=0.22)
        return boxes.fix_in_frame()

    def chapter(self, active: int, title: str):
        self.chapter_title = title
        heading = txt(title, 56).move_to(0.6 * UP)
        big = self.roadmap(active, big=True).move_to(0.9 * DOWN)
        self.play(FadeIn(heading, shift=0.3 * UP), FadeIn(big, lag_ratio=0.1))
        self.wait(1.2)
        small = self.roadmap(active)
        if self.roadmap_mob is not None:
            self.remove(self.roadmap_mob)
        self.play(FadeOut(heading), ReplacementTransform(big, small))
        self.roadmap_mob = small

    def keep_roadmap(self, active: int, title: str):
        """Continue a chapter in a new scene: the small road map, no title card."""
        self.chapter_title = title
        self.roadmap_mob = self.roadmap(active)
        self.add(self.roadmap_mob)

    def subtitle(self, text: str) -> Text:
        return txt(text, 30, YELLOW).to_edge(UP, buff=0.85)

    def dim(self) -> Rectangle:
        """A dark veil over everything drawn so far, kept under the captions.
        Fade it in with veil.animate.set_fill(opacity=0.85)."""
        veil = FullScreenRectangle().set_fill(BLACK, 0).set_stroke(width=0)
        self.add(veil)
        self.bring_to_front(self.caption_box)
        return veil

    def tear_down(self):
        self._close_caption()
        out = self.BUILD / "captions"
        out.mkdir(parents=True, exist_ok=True)
        data = {"scene": type(self).__name__, "title": self.chapter_title, "duration": round(float(self.time), 3),
                "voices": sorted(self.voices), "captions": self.log}
        (out / f"{type(self).__name__}.json").write_text(json.dumps(data, indent=1))
        super().tear_down()
