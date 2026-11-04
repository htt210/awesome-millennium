# Video: Navier–Stokes flows that compute

An explainer for a general audience, 6 minutes long, in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). It follows the plain-language page ([`../README.md`](../README.md)) and introduces every idea with a picture before naming it. It comes in two voices with identical pictures and timing:

| Video | Narrator |
|---|---|
| [`navier-stokes-universal-computation.mp4`](navier-stokes-universal-computation.mp4) | American man (BookVoice "US-M1") |
| [`navier-stokes-universal-computation-us-female.mp4`](navier-stokes-universal-computation-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`captions.srt`](captions.srt) and [`script.md`](script.md), with timestamps.

## The script comes first

[`storyboard.md`](storyboard.md) is the script: for every beat, what is on screen and the exact narration. Each scene calls `self.narrate("2.3")`, and the words of beat 2.3 become the captions and the voiceover, so changing a sentence in the storyboard changes the video on the next render.

| File | What it is |
|---|---|
| [`storyboard.md`](storyboard.md) | the script: on-screen action and narration, beat by beat |
| [`nscomp_video.py`](nscomp_video.py) | the scenes `C0Open` … `C5Close`, plus `Thumbnail` |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`poster.png`](poster.png) | thumbnail |

The narration engine, voice, caption and render tools are shared by every video in this repository and live in [`tools/video/`](../../../../../tools/video/).

Several pictures are computed, not sketched:
- the run of the two-state busy beaver machine, step by step;
- its encoding as a point of a square, checked step by step in exact arithmetic against the area-keeping maps of the rule rectangles (the same code as [`../code/make_figures.py`](../code/make_figures.py));
- the area of one rule's rectangle before and after.

The fluid box, the swirls, the drop's path, the parking and the clock are schematics.

## Chapters

0. **Cold open.** A pushed fluid and one drop.
1. **Fluids.** The Navier–Stokes equations; the Millennium question; Tao's fluid computer.
2. **Machines.** A Turing machine run; the halting problem.
3. **The claim.** The setting, the compiled force, smoothness, the halting drop.
4. **How it works.** Moore's tape-as-a-point; area-keeping rules; Bennett's records; swirls; the clock; reading off the force.
5. **Is it right?** The Lean scope; no blowup; Tao's program; closing.

## Rendering

From this directory, with the setup described in the [ETH video](../../eth-is-false/video/README.md#rendering):

```bash
./render.sh                # silent 1080p30
QUALITY=-l ./render.sh     # quick 480p preview
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) JOBS=4 ./render.sh
```

The BookVoice models are not in this repository; any Piper voice works in their place. The pronunciation of a few names (years) and years is set in `PRONOUNCE` in `nscomp_video.py`. Voice clips are cached in `build/voice/` (ignored by git) so the scenes and the soundtrack use the same take.
