# Video: Finite Time Blowup for Navier–Stokes

An explainer for a general audience, DURATION long, in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). It follows the plain-language page ([`../README.md`](../README.md)) and introduces every idea with a picture before naming it. It comes in two voices with identical pictures and timing:

| Video | Narrator |
|---|---|
| [`navier-stokes-blowup.mp4`](navier-stokes-blowup.mp4) | American man (BookVoice "US-M1") |
| [`navier-stokes-blowup-us-female.mp4`](navier-stokes-blowup-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`captions.srt`](captions.srt) and [`script.md`](script.md), with timestamps.

## The script comes first

[`storyboard.md`](storyboard.md) is the script: for every beat, what is on screen and the exact narration. Each scene calls `self.narrate("2.4")`, and the words of beat 2.4 become the captions and the voiceover, so changing a sentence in the storyboard changes the video on the next render.

| File | What it is |
|---|---|
| [`storyboard.md`](storyboard.md) | the script: on-screen action and narration, beat by beat |
| [`ns_video.py`](ns_video.py) | the scenes `C0Open` … `C9Close`, plus `Thumbnail` |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`poster.png`](poster.png) | thumbnail |

The narration engine, voice, caption and render tools are shared by every video in this repository and live in [`tools/video/`](../../../../../tools/video/).

## Chapters

0. **Cold open.** A swirl tightens and spins faster; the question.
1. **The equations.** The four effects (the fluid carrying itself, friction, pressure, an outside force), then the equation itself.
2. **The question.** A smooth flow that might blow up; ninety years of work; the prize; the four ways to win, and the two the paper claims.
3. **Why the force is not a cheat.** Forcing a blowup by hand needs a force that blows up first; the paper's force is a smooth bump.
4. **The claim.** The theorem in words: every viscosity, a fluid at rest, a smooth force, infinite speed at time 1, finite energy.
5. **The collapsing vortex.** A core that shrinks and spins faster, on the exact scales the paper uses.
6. **Pulses, corrections and the rest.** (a) The seam around the core. (b) Amplified pulses that cancel its imbalance. (c) Infinitely many rounds of correction. (d) The calm exterior, and the force as the leftover. (e) Uniqueness: no other solution can escape. (f) Every viscosity at once, and the whole construction in one row.
7. **Is it right?** The Lean proof, what it checks, and the dispute over whether it follows the paper.
8. **What it would mean.** It would settle the problem as written; it would not show that flows with no force break down, or that real water does.
9. **Closing.**

## Rendering

From this directory, with the setup described in [`tools/video/`](../../../../../tools/video/) and the [ETH video](../../../10/eth-is-false/video/README.md#rendering):

```bash
./render.sh                # silent 1080p30
QUALITY=-l ./render.sh     # quick 480p preview
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) JOBS=4 ./render.sh
```

The BookVoice models are not in this repository; any Piper voice works in their place. The pronunciation of a few names (Leray, Bastounis, Circelli, Martínez-Zoroa) is set in `PRONOUNCE` in `ns_video.py`. Voice clips are cached in `build/voice/` (ignored by git) so the scenes and the soundtrack use the same take.
