# Video: Can a shape tear quietly? Ricci flow and scalar curvature

An explainer for a general audience, 5 minutes long, in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). It follows the plain-language page ([`../README.md`](../README.md)) and introduces every idea with a picture before naming it. It comes in two voices with identical pictures and timing:

| Video | Narrator |
|---|---|
| [`ricci-flow-scalar-curvature-extension.mp4`](ricci-flow-scalar-curvature-extension.mp4) | American man (BookVoice "US-M1") |
| [`ricci-flow-scalar-curvature-extension-us-female.mp4`](ricci-flow-scalar-curvature-extension-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`captions.srt`](captions.srt) and [`script.md`](script.md), with timestamps.

## The script comes first

[`storyboard.md`](storyboard.md) is the script: for every beat, what is on screen and the exact narration. Each scene calls `self.narrate("2.3")`, and the words of beat 2.3 become the captions and the voiceover, so changing a sentence in the storyboard changes the video on the next render.

| File | What it is |
|---|---|
| [`storyboard.md`](storyboard.md) | the script: on-screen action and narration, beat by beat |
| [`ricci_video.py`](ricci_video.py) | the scenes `C0Open` … `C5Close`, plus `Thumbnail` |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`poster.png`](poster.png) | thumbnail |

The narration engine, voice, caption and render tools are shared by every video in this repository and live in [`tools/video/`](../../../../../tools/video/).

Several pictures are computed, not sketched:
- the curvature of a round four-sphere under Ricci flow, from the exact solution;
- how many independent numbers the full, Ricci and scalar curvature carry, by dimension.

The smoothing shapes, the pinching neck, the bubble profiles, the power-law rates, the tree of pieces and the warped shape are schematics.

## Chapters

0. **Cold open.** A shape smooths and tears; a calm dial.
1. **Ricci flow.** The equation; the shrinking sphere; necks and Perelman.
2. **Curvature.** Full, Ricci and scalar curvature; what scalar curvature misses.
3. **The question.** Hamilton and Šešum; the shrinking bubble; how fast a tear must be.
4. **The claims.** Four dimensions: the tree of pieces and the energy; high dimensions: the warped counterexample.
5. **Is it right?** No Lean, no assessment yet; Poincaré itself untouched; closing.

## Rendering

From this directory, with the setup described in the [ETH video](../../../10/eth-is-false/video/README.md#rendering):

```bash
./render.sh                # silent 1080p30
QUALITY=-l ./render.sh     # quick 480p preview
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) JOBS=4 ./render.sh
```

The BookVoice models are not in this repository; any Piper voice works in their place. The pronunciation of a few names (Ricci, Šešum) and years is set in `PRONOUNCE` in `ricci_video.py`. Voice clips are cached in `build/voice/` (ignored by git) so the scenes and the soundtrack use the same take.
