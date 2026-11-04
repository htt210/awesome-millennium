# Video: The Birch–Swinnerton-Dyer formula, in low rank

An explainer for a general audience, 13 minutes long, in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). It follows the plain-language page ([`../README.md`](../README.md)) and introduces every idea with a picture before naming it. It comes in two voices with identical pictures and timing:

| Video | Narrator |
|---|---|
| [`exact-bsd-low-selmer-corank.mp4`](exact-bsd-low-selmer-corank.mp4) | American man (BookVoice "US-M1") |
| [`exact-bsd-low-selmer-corank-us-female.mp4`](exact-bsd-low-selmer-corank-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`captions.srt`](captions.srt) and [`script.md`](script.md), with timestamps.

## The script comes first

[`storyboard.md`](storyboard.md) is the script: for every beat, what is on screen and the exact narration. Each scene calls `self.narrate("2.4")`, and the words of beat 2.4 become the captions and the voiceover, so changing a sentence in the storyboard changes the video on the next render.

| File | What it is |
|---|---|
| [`storyboard.md`](storyboard.md) | the script: on-screen action and narration, beat by beat |
| [`bsd_video.py`](bsd_video.py) | the scenes `C0Open` … `C9Close`, plus `Thumbnail` |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`poster.png`](poster.png) | thumbnail |

The narration engine, voice, caption and render tools are shared by every video in this repository and live in [`tools/video/`](../../../../../tools/video/).

Several pictures are computed, not sketched:
- the curve $y^2 + y = x^3 - x$ and the multiples of $(0, 0)$, with exact fractions;
- the solutions of that curve modulo 5, 7, 11 and 13;
- Birch and Swinnerton-Dyer's products over all primes up to 100,000 for curves of rank 0 to 3 (Cremona's 11a1, 37a1, 389a1 and 5077a1);
- primes as sums of two rational cubes.

The L-function sketches, the error gauge and the stages of the proof are schematics.

## Chapters

0. **Cold open.** A curve and its rational points; the question.
1. **Points on a curve.** Adding points; multiples of one point; Mordell's theorem and the rank.
2. **The experiment.** Counting solutions modulo primes; the products for ranks 0 to 3; the L-function and the conjecture.
3. **The exact formula.** Each measurement in the formula; the Tate–Shafarevich group.
4. **What was known.** Gross–Zagier, Kolyvagin, modularity; the formula prime by prime.
5. **The claim.** The Selmer group; the theorem.
6. **How it works.** The four inputs; the error at each odd prime; the squeeze; the pair identity.
7. **What follows.** Almost all twists; primes as sums of two cubes.
8. **Is it right?** Four unreviewed papers; no Lean proof; no expert verdict yet.
9. **What it does not do.** Rank 2 and up; closing.

## Rendering

From this directory, with the setup described in the [ETH video](../../eth-is-false/video/README.md#rendering):

```bash
./render.sh                # silent 1080p30
QUALITY=-l ./render.sh     # quick 480p preview
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) JOBS=4 ./render.sh
```

The BookVoice models are not in this repository; any Piper voice works in their place. The pronunciation of a few names (Shafarevich, Kolyvagin, Zagier, Burungale) and years is set in `PRONOUNCE` in `bsd_video.py`. Voice clips are cached in `build/voice/` (ignored by git) so the scenes and the soundtrack use the same take.
