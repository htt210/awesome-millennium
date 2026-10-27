# Video: The Exponential Time Hypothesis is False

An 8½-minute explainer in the style of 3Blue1Brown, made with [3b1b's manim](https://github.com/3b1b/manim) (`manimgl` 1.7.2). There is no voiceover; the narration is burned in as captions and also provided as [`script.md`](script.md) (for recording a voiceover) and [`captions.srt`](captions.srt).

| File | What it is |
|---|---|
| [`eth-is-false.mp4`](eth-is-false.mp4) | the rendered video, 1080p30 |
| [`poster.png`](poster.png) | thumbnail |
| [`eth_video.py`](eth_video.py) | the scenes |
| [`captions_util.py`](captions_util.py) | caption wrapping and plain-text conversion |
| [`render.sh`](render.sh) | renders every scene, concatenates them, writes the poster and captions |
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
./render.sh                # 1080p30; on a machine without a display it uses xvfb-run
QUALITY=-l ./render.sh     # quick 480p preview
JOBS=3 ./render.sh         # render scenes in parallel
```

Intermediate files go to `build/` (ignored by git). Rendering the full video takes about 40 minutes on four CPU cores with Mesa's software renderer.
