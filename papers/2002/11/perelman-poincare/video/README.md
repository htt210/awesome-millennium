# Video: Perelman's proof of the Poincaré conjecture

An explainer for a general audience, 13 minutes 41 seconds long, in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). It follows the plain-language page ([`../README.md`](../README.md)) and introduces every idea with a picture before naming it. It comes in two voices with identical pictures and timing:

| Video | Narrator |
|---|---|
| [`perelman-poincare.mp4`](perelman-poincare.mp4) | American man (BookVoice "US-M1") |
| [`perelman-poincare-us-female.mp4`](perelman-poincare-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`captions.srt`](captions.srt) and [`script.md`](script.md), with timestamps.

## The script comes first

[`storyboard.md`](storyboard.md) is the script: for every beat, what is on screen and the exact narration. Each scene calls `self.narrate("3.4")`, and the words of beat 3.4 become the captions and the voiceover, so changing a sentence in the storyboard changes the video on the next render.

| File | What it is |
|---|---|
| [`storyboard.md`](storyboard.md) | the script: on-screen action and narration, beat by beat |
| [`poincare_video.py`](poincare_video.py) | the scenes `C0Open` … `C9Close`, plus `Thumbnail` |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`poster.png`](poster.png) | thumbnail |

The narration engine, voice, caption and render tools are shared by every video in this repository and live in [`tools/video/`](../../../../../tools/video/).

Three-dimensional shapes are drawn as their two-dimensional cousins: a ball's surface, a doughnut, the outline of a dumbbell. The curve in chapter 3 is computed, not sketched: it is the curve-shortening flow of the explainer's figure, solved numerically in `curve_shortening()`.

## Chapters

0. **Cold open.** A loop slides off a ball and gets stuck on a doughnut; the question.
1. **Shapes.** Stretching without tearing; mug and doughnut; living inside a shape; the lasso test; simply connected; surfaces.
2. **The question.** Finite spaces with no edge; gluing a circle, a sphere and the three-sphere; the conjecture; Smale, Freedman, and the prize.
3. **Ricci flow.** Hamilton's idea; heat; the equation; curves that round themselves out; positively curved shapes.
4. **Necks that pinch.** A dumbbell's neck pinches; surgery; the three missing pieces; the cigar.
5. **What Perelman added.** The three papers; a quantity that only rises; no collapsing; the short list of models; controlled surgery; extinction in finite time.
6. **Putting it together.** Flow, cut, burn away, and read the answer backwards.
7. **Checked.** Kleiner–Lott, Morgan–Tian, Cao–Zhu; the Fields Medal and the Millennium Prize, both declined.
8. **What it means.** The conjecture and geometrization; what stays open.
9. **Closing.**

## Rendering

From this directory, with the setup described in the [ETH video](../../../../2026/10/eth-is-false/video/README.md#rendering):

```bash
./render.sh                # silent 1080p30
QUALITY=-l ./render.sh     # quick 480p preview
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) JOBS=4 ./render.sh
```

The BookVoice models are not in this repository; any Piper voice works in their place. The pronunciation of a few names (Ricci, Cao, Zhu, Huai-Dong, Xi-Ping) and years is set in `PRONOUNCE` in `poincare_video.py`. Voice clips are cached in `build/voice/` (ignored by git) so the scenes and the soundtrack use the same take.
