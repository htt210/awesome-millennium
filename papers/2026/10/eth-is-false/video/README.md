# Video: The Exponential Time Hypothesis is False

A 9¾-minute explainer in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2), narrated and captioned. It comes in two voices with identical pictures and timing, so they can be compared side by side:

| Video | Narrator |
|---|---|
| [`eth-is-false.mp4`](eth-is-false.mp4) | American man (BookVoice "US-M1") |
| [`eth-is-false-us-female.mp4`](eth-is-false-us-female.mp4) | American woman (BookVoice "US-F1") |

Both narrators are synthetic voices from the BookVoice reading app (Ru's designed voices: no real person was cloned), run locally as Piper/VITS ONNX models. The narration is also burned in as captions and provided as [`script.md`](script.md) and [`captions.srt`](captions.srt).

| File | What it is |
|---|---|
| [`poster.png`](poster.png) | thumbnail |
| [`eth_video.py`](eth_video.py) | the scenes; every caption has a `say` text, the same sentence written for the ear |
| [`voice.py`](voice.py) | reads a `say` text with a Piper voice, phonemized the way BookVoice reads English |
| [`make_voiceover.py`](make_voiceover.py) | lays the narration clips under the rendered video, one soundtrack per voice |
| [`captions_util.py`](captions_util.py) | caption wrapping and plain-text conversion |
| [`render.sh`](render.sh) | renders every scene, concatenates them, adds the narration, writes the poster and captions |
| [`make_captions.py`](make_captions.py) | builds `captions.srt` and `script.md` from the caption timings each scene logs |
| [`custom_config.yml`](custom_config.yml) | manimgl settings (black background, CMU Serif) |

## Scenes

1. **The claim.** 3-SAT, brute force, decades of exponential algorithms, ETH, and the new subexponential counting theorem.
2. **Counting is a polynomial sum.** Clause polynomials and $N(F)=\sum_x\prod_e\Phi_e(x)$.
3. **The dream: independent groups.** Why separated clauses would make counting easy.
4. **Deform, then separate.** Replacement linear forms, $H(T)$, and fixing integer measurements to decouple the groups.
5. **From easy points back to $T=0$.** Taylor data at $t=1,\dots,Q$ and Hermite interpolation, using a real $H(T)$ computed by [`../code/toy_eth.py`](../code/toy_eth.py).
6. **Low degree, many points: the matrix trick.** Swaps, $M_0=V_0f(W_0)$, the binomial spectrum, and the degree budget.
7. **Paying the bill.** The three costs, the reduction for general $k$-CNF, and the Beigel–Tarui lift.
8. **What falls, and what does not.** The refuted hypotheses, the consequences, what is not implied, and the verification status.

## Rendering

```bash
pip install manimgl==1.7.2 "setuptools<81" audioop-lts   # the last one is only needed on Python 3.13+
# plus LaTeX with dvisvgm, ffmpeg, and the CMU Serif font (Debian/Ubuntu: texlive-latex-extra
# texlive-fonts-extra texlive-science tipa dvisvgm cm-super fonts-cmu ffmpeg)
./render.sh                # silent 1080p30, paced for reading; without a display it uses xvfb-run
QUALITY=-l ./render.sh     # quick 480p preview
JOBS=3 ./render.sh         # render scenes in parallel

# narrated: one video per voice, every scene waits for the slowest voice
pip install piper-tts onnxruntime numpy                  # into the same environment as manimgl
NARRATION_VOICES="us-male=/path/to/eam.onnx,us-female=/path/to/eaf.onnx" PYTHON=$(which python) ./render.sh
```

The BookVoice models are not in this repository. Any Piper voice works in their place, for example `en_US-ryan-high` from [rhasspy/piper-voices](https://huggingface.co/rhasspy/piper-voices). VITS samples a new take each time, so `voice.py` caches every clip in `build/voice/` and the scenes and the soundtrack use the same take; delete that folder to get new takes. To hear one line: `python voice.py MODEL.onnx "Text to read." out.wav`.

Intermediate files go to `build/` (ignored by git). Rendering the full video takes about 40 minutes on four CPU cores with Mesa's software renderer.
