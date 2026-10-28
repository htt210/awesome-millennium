# Video: The Exponential Time Hypothesis is False

An explainer for a general audience, 22 minutes 42 seconds long, in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). It follows the plain-language page ([`../README.md`](../README.md)) and introduces every idea with an example before naming it. It comes in two voices with identical pictures and timing:

| Video | Narrator |
|---|---|
| [`eth-is-false.mp4`](eth-is-false.mp4) | American man (BookVoice "US-M1") |
| [`eth-is-false-us-female.mp4`](eth-is-false-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (Ru's designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`captions.srt`](captions.srt) and [`script.md`](script.md), with timestamps.

## The script comes first

[`storyboard.md`](storyboard.md) is the script: for every beat, what is on screen and the exact narration. It was reviewed before anything was animated, and it is also the source of the narration. Each scene calls `self.narrate("1.4")`, and the words of beat 1.4 become the captions and the voiceover. Changing a sentence in the storyboard changes the video on the next render, and the scenes wait for the voice, so the timing follows.

| File | What it is |
|---|---|
| [`storyboard.md`](storyboard.md) | the script: on-screen action and narration, beat by beat |
| [`eth_video.py`](eth_video.py) | the scenes `C0Open` … `C10Close`, plus `Thumbnail` |
| [`voice.py`](voice.py) | reads a caption with a Piper voice, phonemized the way BookVoice reads English |
| [`make_voiceover.py`](make_voiceover.py) | lays the narration clips under the rendered video, one soundtrack per voice |
| [`make_captions.py`](make_captions.py) | builds `captions.srt` and `script.md` from the caption timings each scene logs |
| [`captions_util.py`](captions_util.py) | plain-text and markdown conversion for those files |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`custom_config.yml`](custom_config.yml) | manimgl settings (black background, CMU Serif) |
| [`poster.png`](poster.png) | thumbnail |

## Chapters

0. **Cold open.** A switch, a wall, the title.
1. **The puzzle.** Switches and rules, a happy and an unhappy rule, solving a small puzzle, the name 3-SAT, counting.
2. **Why it gets hard so fast.** Settings double with every switch; a second, a year, the age of the universe; exponential growth and the "factor per switch" gauge.
3. **Fifty years of shortcuts.** The three-case shortcut (×1.84), the record from ×2 to ×1.307, still a fixed factor.
4. **The bet called ETH.** A floor above ×1 that no method can cross; results built on it.
5. **The new claim.** Exponential, polynomial and subexponential growth, per switch; why a sinking factor breaks ETH; the one formula.
6. **How the method works.** (a) Scores and products turn counting into arithmetic, with a worked table. (b) Independent teams. (c) Teams that share only a total. (d) The dial. (e) Back to dial 0: values and slopes pin down the curve, on a real example from [`../code/toy_eth.py`](../code/toy_eth.py). (f) The balancing act, and tidy pieces.
7. **The catch.** The paper's explicit numbers: it wins only when the number of switches has billions of digits.
8. **What it means, and what it doesn't.** Results built on ETH, P vs NP, encryption, practical solvers.
9. **Is it true?** Preprint, Lean check, expert examination, our own checks.
10. **Closing.**

## Rendering

```bash
pip install manimgl==1.7.2 "setuptools<81" audioop-lts   # the last one is only needed on Python 3.13+
# plus LaTeX with dvisvgm, ffmpeg, and the CMU Serif font (Debian/Ubuntu: texlive-latex-extra
# texlive-fonts-extra texlive-science tipa dvisvgm cm-super fonts-cmu ffmpeg)
./render.sh                # silent 1080p30, paced for reading; without a display it uses xvfb-run
QUALITY=-l ./render.sh     # quick 480p preview
JOBS=4 ./render.sh         # render scenes in parallel

# narrated: one video per voice, every scene waits for the slowest voice
pip install piper-tts onnxruntime numpy                  # into the same environment as manimgl
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) ./render.sh
```

The BookVoice models are not in this repository. Any Piper voice works in their place, for example `en_US-ryan-high` from [rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices). The narrator's pronunciation of a few words (ETH, 3-SAT, Paturi, years) is set in `PRONOUNCE` in `eth_video.py`. VITS samples a new take each time, so `voice.py` caches every clip in `build/voice/`, and the scenes and the soundtrack use the same take; delete that folder to get new takes. To hear one line: `python voice.py MODEL.onnx "Text to read." out.wav`.

Intermediate files go to `build/` (ignored by git). Rendering the full narrated video takes about three hours on four CPU cores with Mesa's software renderer.
