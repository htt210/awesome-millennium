# Video: The O(3) continuum limit

An explainer for a general audience, 7 minutes long, in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). It follows the plain-language page ([`../README.md`](../README.md)) and introduces every idea with a picture before naming it. It comes in two voices with identical pictures and timing:

| Video | Narrator |
|---|---|
| [`o3-sigma-model-continuum-limit.mp4`](o3-sigma-model-continuum-limit.mp4) | American man (BookVoice "US-M1") |
| [`o3-sigma-model-continuum-limit-us-female.mp4`](o3-sigma-model-continuum-limit-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`captions.srt`](captions.srt) and [`script.md`](script.md), with timestamps.

## The script comes first

[`storyboard.md`](storyboard.md) is the script: for every beat, what is on screen and the exact narration. Each scene calls `self.narrate("2.3")`, and the words of beat 2.3 become the captions and the voiceover, so changing a sentence in the storyboard changes the video on the next render.

| File | What it is |
|---|---|
| [`storyboard.md`](storyboard.md) | the script: on-screen action and narration, beat by beat |
| [`o3_video.py`](o3_video.py) | the scenes `C0Open` … `C6Close`, plus `Thumbnail` |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`poster.png`](poster.png) | thumbnail |

The narration engine, voice, caption and render tools are shared by every video in this repository and live in [`tools/video/`](../../../../../tools/video/).

Several pictures are computed, not sketched:
- every spin configuration, from a Wolff-cluster Monte Carlo of the lattice model ([`../code/o3_mc.py`](../code/o3_mc.py));
- the spin correlations against distance, for couplings from 0.6 to 1.7;
- the correlation length against the coupling;
- the correlations in the paper's canonical units, falling on one curve;
- block averages of one sampled configuration.

The energy ladders, the shrinking grid, the tilted grids and the four-point picture are schematics.

## Chapters

0. **Cold open.** Arrows on a grid; shrink the grid.
1. **The mass gap.** Fields and particles; the Yang–Mills problem.
2. **The model.** Arrows of length one; samples at three couplings; asymptotic freedom; exponential decay.
3. **The continuum.** The correlation length; shrinking the grid; the canonical units.
4. **The claim.** One limit; the Osterwalder–Schrader axioms; the mass gap; interaction.
5. **How it works.** Blocking; corrections; rotations; reconstruction.
6. **Is it right?** The companion papers; the Lean scope; not Yang–Mills; closing.

## Rendering

From this directory, with the setup described in the [ETH video](../../eth-is-false/video/README.md#rendering):

```bash
./render.sh                # silent 1080p30
QUALITY=-l ./render.sh     # quick 480p preview
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) JOBS=4 ./render.sh
```

The BookVoice models are not in this repository; any Piper voice works in their place. The pronunciation of a few names (O(3), Polyakov) and years is set in `PRONOUNCE` in `o3_video.py`. Voice clips are cached in `build/voice/` (ignored by git) so the scenes and the soundtrack use the same take.
