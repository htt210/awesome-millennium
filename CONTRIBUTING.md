# Contributing

Thanks for helping explain hard mathematics well. This guide covers what belongs here, the workflow for adding an explainer, the metadata vocabulary, and the style conventions that keep thousands of explainers consistent.

## What belongs here

A paper belongs here if it **bears on one of the seven Millennium Prize Problems**, in one of three ways (the `relation` field):

| Relation | Meaning | Example |
|---|---|---|
| `resolves` | claims to settle the problem as the Clay Institute states it | a claimed proof of finite-time breakdown for Navier–Stokes |
| `partial` | proves a special case or a significant piece of the problem | the Hodge conjecture for one class of varieties |
| `adjacent` | settles a closely related question in the problem's landscape without deciding it | refuting the Exponential Time Hypothesis (P vs NP) |

Papers that are not yet explained can be queued in [`backlog.yaml`](backlog.yaml); they appear on the problem pages under "Queue".

## Workflow

```bash
pip install -r tools/requirements.txt
python tools/catalog.py new --date YYYY-MM-DD --slug short-name --title "Exact title of the paper"
```

This creates `papers/YYYY/MM/short-name/` from [`templates/paper/`](templates/paper/). Then:

1. Fill in `paper.yaml`. The validator rejects any leftover `TODO`.
2. Write `README.md`, the explainer (style guide below).
3. Put figure-generating scripts in `code/` and their output in `figures/`.
4. Optionally add a video in `video/` (see [Videos](#videos)).
5. Run `python tools/catalog.py build` to validate metadata, lint the math and relative links of every markdown file, and regenerate every index; then `python tools/catalog.py run-checks <slug>` to run your paper's self-checks.
6. Commit the paper directory **and** the regenerated files (`README.md`, `problems/*.md`, `catalog/*`). CI runs `catalog.py check` and fails if anything is stale.

If you remove an entry from `backlog.yaml` because you explained it, do it in the same change.

### Conventions

- **Directory:** `papers/YYYY/MM/<slug>/`, where `YYYY-MM` is the date of the version you explain. Sharding by month keeps every directory listing under GitHub's 1,000-entry display limit.
- **Slug:** lowercase kebab-case, at most 60 characters, unique across the repository (the tool enforces this). Prefer the paper's claim over its authors: `eth-is-false`, not `openai-oct-2026`.
- **Never edit generated files by hand.** Everything between `<!-- BEGIN:x -->` and `<!-- END:x -->` markers, and everything in `catalog/`, is rewritten by `tools/catalog.py`.

## Metadata vocabulary

`paper.yaml` is validated by [`tools/catalog.py`](tools/catalog.py); [`schema/paper.schema.json`](schema/paper.schema.json) gives editors autocompletion. The status block is the most important part: it is how readers know what to trust.

| Field | Values | Meaning |
|---|---|---|
| `status.review` | `preprint`, `under-review`, `peer-reviewed`, `withdrawn` | journal status of the explained version |
| `status.formalization` | `none`, `partial`, `complete` | machine-checked proof of the **main theorem** (say which system in `formalization_system`) |
| `status.community` | `unexamined`, `under-examination`, `accepted`, `disputed`, `refuted` | what experts have said, with sources |
| `status.as_of` | date | when you last checked; update it whenever you update the status |

A claim reported by its authors is still a claim. "Formalized" means the authors (or someone else) published a machine-checked proof; say in the explainer whether *you* re-ran the check, and what exactly the formal statement covers.

## Explainer style guide

**Audience.** A curious reader with undergraduate mathematics who has not read the paper. Experts should still find the explainer accurate enough to cite.

**Structure.** Start from [`templates/paper/README.md`](templates/paper/README.md): a short summary, a fact table (paper, claim, problem, status), background, the result, the proof idea by idea, what it does and does not imply, verification status, sources.

**Accuracy rules.**

- State the main theorem **exactly** as the source does and cite its section or theorem number. Paraphrase only after the exact statement.
- Every step in "how the proof works" should point to the section of the source it summarizes.
- Separate what the authors claim from what has been checked, and by whom, with dates.
- Say what the result does **not** imply. This is often the most useful paragraph on the page.
- If the source changes (new version, erratum, withdrawal), update the explainer and `status`, and say so near the top.

**Math.** Typeset all mathematics in LaTeX: `$...$` inline and `$$...$$` for displays on their own lines, including single variables in prose. Never approximate math with Unicode glyphs (write `$x_1 \le n^2$`, not `x₁ ≤ n²`). GitHub runs its markdown parser *before* MathJax, and that parser deletes a backslash in front of any non-letter. So:

- never use backslash-punctuation commands: write `\lbrace` and `\rbrace` instead of `\{` and `\}`, drop manual spacing like `\,` and `\;` (it turns into a visible comma or semicolon), and avoid `\#`, `\|` and `\\` (line breaks; use one display per line instead of `aligned`);
- write `\lt` and `\gt` instead of `<` and `>` next to letters, `\ast` instead of `*`, and `\vert` or `\mid` instead of `|` (which also breaks tables); keep `tldr`/`note` fields free of `|`;
- avoid an underscore right after `)`, `]` or `}` (markdown may read it as emphasis); rephrase or move the subscript;
- when a display genuinely needs one of these (an `\underbrace{...}_{...}`, a line break, a subscript after a bracket), put it in a ```` ```math ```` block instead of `$$`: GitHub passes that block to MathJax untouched;
- keep the opening `$` directly before the formula and the closing `$` directly after it, with no spaces inside.

**Figures.** Generate figures with a script in `code/` so they can be regenerated. Provide light and dark variants and embed them with `<picture>` so they look right in both GitHub themes; always write meaningful alt text. Prefer SVG for diagrams and PNG for dense plots.

**Code.** Use the standard library where possible (otherwise pin versions in `code/requirements.txt`). If your code checks the mathematics, give it a fast mode and declare it in `paper.yaml` under `explainer.checks`, for example `python code/toy.py --quick`; CI runs these.

## Videos

Videos use [3Blue1Brown's manim](https://github.com/3b1b/manim) (`manimgl`), not the community edition. Keep in `video/`:

- the scene file (`*.py`) and a `render.sh` that renders every scene and concatenates them,
- `script.md`, the narration, scene by scene,
- `captions.srt`, burned in or shipped alongside,
- `poster.png`, a still used as the thumbnail.

**Script first.** Write the script before animating: a `storyboard.md` that gives, for every beat, what is on screen and the exact narration, with one idea per beat and an example before every new term. Get it reviewed, then animate from it (the ETH video reads its narration straight from its storyboard).

**Narration.** A voiceover is optional. If you add one, keep a spoken version of each caption next to it in the scene file (numbers, symbols and names written out the way they should be read) and let the scene wait for the voice, as the ETH video does with `voice.py` and `make_voiceover.py`. Do not commit voice models: the scripts take model paths at render time.

**Size policy.** A rendered video up to about 50 MB may be committed next to its sources. Larger videos should be uploaded as a GitHub Release asset (or another stable host) and linked with `explainer.video_url`; keep only the sources, captions and poster in git. This keeps clones small as the collection grows.

## Checklist before opening a pull request

- [ ] `python tools/catalog.py build` reports no errors and you committed the regenerated files
- [ ] `python tools/catalog.py run-checks <slug>` passes
- [ ] the main theorem is quoted exactly, with its source location
- [ ] status fields are current and dated, and the explainer says what is *not* implied
- [ ] all math is LaTeX; figures have alt text and work in light and dark themes
