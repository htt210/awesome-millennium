# Video: The Quasi-Riemann Hypothesis

An explainer for a general audience, 13 minutes 28 seconds long, in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). It follows the plain-language page ([`../README.md`](../README.md)) and introduces every idea with a picture before naming it. It comes in two voices with identical pictures and timing:

| Video | Narrator |
|---|---|
| [`quasi-riemann-hypothesis.mp4`](quasi-riemann-hypothesis.mp4) | American man (BookVoice "US-M1") |
| [`quasi-riemann-hypothesis-us-female.mp4`](quasi-riemann-hypothesis-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`captions.srt`](captions.srt) and [`script.md`](script.md), with timestamps.

## The script comes first

[`storyboard.md`](storyboard.md) is the script: for every beat, what is on screen and the exact narration. Each scene calls `self.narrate("2.4")`, and the words of beat 2.4 become the captions and the voiceover, so changing a sentence in the storyboard changes the video on the next render.

| File | What it is |
|---|---|
| [`storyboard.md`](storyboard.md) | the script: on-screen action and narration, beat by beat |
| [`qrh_video.py`](qrh_video.py) | the scenes `C0Open` … `C9Close`, plus `Thumbnail` |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`poster.png`](poster.png) | thumbnail |

The narration engine, voice, caption and render tools are shared by every video in this repository and live in [`tools/video/`](../../../../../tools/video/).

Several pictures are computed, not sketched:
- the prime staircase and its error up to a million;
- Riemann's explicit formula, with the waves of the first 13 zeros of zeta added one by one until they trace the weighted prime count;
- the Möbius running total up to 100,000;
- the Eisenstein primes;
- the smallest non-square for every prime below 200,000.

The "crowd" of bars and the folding rows in chapter 6 are schematics.

## Chapters

0. **Cold open.** The primes one by one, their staircase, and the question of the wobble.
1. **Primes.** What a prime is; the staircase and the smooth curve; the error up to a million.
2. **Zeta.** The zeta sum; complex inputs; Euler's product over primes; one wave per zero; loud and quiet waves; the critical strip and its mirror symmetry.
3. **The question.** The Riemann hypothesis; what was proved before; the quasi-Riemann hypothesis; Dirichlet L-functions and the rogue Landau–Siegel zero.
4. **The claim.** No zeros past 7/8, nor before 1/8; the rogue zero ruled out; the two stages and the companion paper.
5. **Sums that cancel.** The Möbius coin flips; why a zero-free line means a sum that provably cancels.
6. **A crowd and a symmetry.** Hiding the sum in a family; the cubic theta function; the Eisenstein integers; from 11/12 to 7/8.
7. **What would follow.** No Landau–Siegel zeros; small non-squares; fast square roots; primes in patterns; idoneal numbers.
8. **Is it right?** The Lean statement; human readers; the reworked Landau–Siegel arguments.
9. **What it does not do.** Not the Riemann hypothesis; 7/8 against 1/2; closing.

## Rendering

From this directory, with the setup described in the [ETH video](../../../10/eth-is-false/video/README.md#rendering):

```bash
./render.sh                # silent 1080p30
QUALITY=-l ./render.sh     # quick 480p preview
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) JOBS=4 ./render.sh
```

The BookVoice models are not in this repository; any Piper voice works in their place. The pronunciation of a few names (Dirichlet, Siegel, idoneal) and years is set in `PRONOUNCE` in `qrh_video.py`. Voice clips are cached in `build/voice/` (ignored by git) so the scenes and the soundtrack use the same take.
