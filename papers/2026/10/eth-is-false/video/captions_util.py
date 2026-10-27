"""Caption helpers shared by eth_video.py (on-screen captions) and
make_captions.py (captions.srt and script.md). No manim dependency."""

from __future__ import annotations

import re


def plain(tex: str) -> str:
    """Caption text without LaTeX markup: used for reading-time estimates and
    for the .srt file, which players display as plain text."""
    s = tex.replace(R"\\", " ").replace("$", "").replace("---", "\u2014").replace("--", "\u2013")
    s = re.sub(r"\\(mathsf|mathrm|text|textbf|emph)\{([^}]*)\}", r"\2", s)
    s = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\frac(\d)(\d)", r"\1/\2", s)
    s = re.sub(r"\\sqrt\{([^}]*)\}", r"sqrt(\1)", s)
    for tex_cmd, text in ((R"\log", " log "), (R"\in", " in "), (R"\sum", "sum "), (R"\prod", "prod "),
                          (R"\lbrace", "{"), (R"\rbrace", "}"), (R"\#", "#"), (R"\le", "<="), (R"\ge", ">="),
                          (R"\ll", "<<"), (R"\gg", ">>"), (R"\times", "x"), (R"\cdot", "*"),
                          (R"\approx", "~"), (R"\dots", "..."), (R"\,", " "), (R"\ ", " "), (R"\ne", "!="),
                          (R"\sqrt", "sqrt")):
        s = s.replace(tex_cmd, text)
    s = re.sub(r"\\([A-Za-z]+)", r"\1", s)
    return re.sub(r"\s+", " ", s.replace("{", "").replace("}", "")).strip()


def wrap_caption(text: str, width: int = 74) -> str:
    """Greedy line breaking for TexText that never splits inside $...$."""
    tokens = re.findall(r"\$[^$]*\$\S*|\S+", text)
    lines, cur, cur_len = [], [], 0
    for tok in tokens:
        visible = len(plain(tok))
        if cur and cur_len + 1 + visible > width:
            lines.append(" ".join(cur))
            cur, cur_len = [], 0
        cur.append(tok)
        cur_len += visible + (1 if cur_len else 0)
    if cur:
        lines.append(" ".join(cur))
    return R" \\ ".join(lines)


def to_markdown(tex: str) -> str:
    """Caption TeX -> GitHub markdown for script.md: text-mode commands become
    plain markdown, math stays in $...$. The count #F is written N(F) there,
    because GitHub drops the backslash of \\# inside $...$."""
    out = []
    for part in re.split(r"(\$[^$]*\$)", tex):
        if len(part) > 1 and part.startswith("$") and part.endswith("$"):
            out.append(part.replace(R"\#F", "N(F)").replace("<", R"\lt ").replace(">", R"\gt "))
            continue
        t = part.replace("---", "\u2014").replace("--", "\u2013")
        t = re.sub(r"\\emph\{([^}]*)\}", r"*\1*", t)
        t = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", t)
        t = t.replace(R"\dots\ ", "\u2026 ").replace(R"\dots", "\u2026").replace(R"\#", "#").replace(R"\ ", " ")
        out.append(t)
    return "".join(out)
