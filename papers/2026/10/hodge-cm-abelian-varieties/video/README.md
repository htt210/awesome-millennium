# Video: The Hodge conjecture for CM abelian varieties

An explainer for a general audience, 10 minutes long, in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). It follows the plain-language page ([`../README.md`](../README.md)) and introduces every idea with a picture before naming it. It comes in two voices with identical pictures and timing:

| Video | Narrator |
|---|---|
| [`hodge-cm-abelian-varieties.mp4`](hodge-cm-abelian-varieties.mp4) | American man (BookVoice "US-M1") |
| [`hodge-cm-abelian-varieties-us-female.mp4`](hodge-cm-abelian-varieties-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`captions.srt`](captions.srt) and [`script.md`](script.md), with timestamps.

## The script comes first

[`storyboard.md`](storyboard.md) is the script: for every beat, what is on screen and the exact narration. Each scene calls `self.narrate("3.4")`, and the words of beat 3.4 become the captions and the voiceover, so changing a sentence in the storyboard changes the video on the next render.

| File | What it is |
|---|---|
| [`storyboard.md`](storyboard.md) | the script: on-screen action and narration, beat by beat |
| [`hodge_video.py`](hodge_video.py) | the scenes `C0Open` … `C8Close`, plus `Thumbnail` |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`poster.png`](poster.png) | thumbnail |

The narration engine, voice, caption and render tools are shared by every video in this repository and live in [`tools/video/`](../../../../../tools/video/).

Several pictures are computed, not sketched:
- the Hodge numbers of an abelian threefold, arranged in the Hodge diamond;
- which lattices a quarter turn or a sixth turn carries to themselves;
- the balanced sign quadruples of the paper's four-factor relation (216 of them for three pairs of directions).

The doughnuts, shadows, the ball quotient and the landscape of varieties are schematics.

## Chapters

0. **Cold open.** Holes, shadows, and the question.
1. **Shapes, holes and shadows.** Varieties; cohomology classes; algebraic cycles and their shadows.
2. **The conjecture.** The (p, q) splitting; Hodge classes; Lefschetz in degree two; exotic classes.
3. **Abelian varieties and complex multiplication.** Lattices and doughnuts; extra symmetry; Weil classes.
4. **The claim.** Deligne and Markman before; the theorem.
5. **How it works.** Balanced blocks; a surface with a nonzero integral; theta functions; Hecke and Frobenius; back to rational coefficients.
6. **What follows.** The Tate and Hodge standard conjectures for abelian varieties (Milne); companion papers.
7. **Is it right?** The Lean proof; the withdrawn sister papers; no expert verdict yet.
8. **What it does not do.** One special family; closing.

## Rendering

From this directory, with the setup described in the [ETH video](../../eth-is-false/video/README.md#rendering):

```bash
./render.sh                # silent 1080p30
QUALITY=-l ./render.sh     # quick 480p preview
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) JOBS=4 ./render.sh
```

The BookVoice models are not in this repository; any Piper voice works in their place. The pronunciation of a few names (Weil, Grothendieck, Milne, Hecke, Deligne) and years is set in `PRONOUNCE` in `hodge_video.py`. Voice clips are cached in `build/voice/` (ignored by git) so the scenes and the soundtrack use the same take.
