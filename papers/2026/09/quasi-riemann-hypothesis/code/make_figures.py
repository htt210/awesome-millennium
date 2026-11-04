#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png

Computed from data: `primes` (prime counts against the logarithmic integral),
`strip` (the first zeros of zeta, known values), `mobius` (the Mertens
function), `eisenstein` (Eisenstein primes) and `nonresidue` (least quadratic
nonresidues). `family` is a schematic; `timeline` is a list of dates.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "figures"

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834", s3="#1baf7a",
                  mid="#f0efec", red="#e34948", band="#dbe8f8", new="#f6c7ae"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926", s3="#199e70",
                 mid="#383835", red="#e66767", band="#1f3350", new="#6b3a24"),
}

# Imaginary parts of the first nontrivial zeros of zeta (all on Re s = 1/2).
ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 40.918719, 43.327073,
         48.005151, 49.773832, 52.970321, 56.446248, 59.347044]


def setup(th: dict, size=(10, 5.0)):
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12, "mathtext.fontset": "dejavusans",
        "axes.edgecolor": th["axis"], "axes.labelcolor": th["ink2"],
        "xtick.color": th["muted"], "ytick.color": th["muted"],
        "text.color": th["ink"], "axes.facecolor": th["surface"],
        "figure.facecolor": th["surface"], "savefig.facecolor": th["surface"],
        "axes.grid": True, "grid.color": th["grid"], "grid.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2.4,
        "lines.solid_capstyle": "round", "legend.frameon": False,
    })
    return plt.figure(figsize=size, dpi=160)


def title(fig, text: str, sub: str, th: dict):
    fig.text(0.012, 0.975, text, fontsize=16, fontweight="bold", color=th["ink"], va="top")
    fig.text(0.012, 0.915, sub, fontsize=11, color=th["ink2"], va="top")


def save(fig, name: str, mode: str):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}-{mode}.png")
    plt.close(fig)


def sieve(n: int) -> np.ndarray:
    is_p = np.ones(n + 1, dtype=bool)
    is_p[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i::i] = False
    return is_p


def mobius(n: int) -> np.ndarray:
    mu = np.ones(n + 1, dtype=np.int8)
    mu[0] = 0
    is_p = sieve(n)
    for p in np.nonzero(is_p)[0]:
        mu[p::p] *= -1
        mu[p * p::p * p] = 0
    return mu


def li(xs: np.ndarray) -> np.ndarray:
    """Offset logarithmic integral int_2^x dt / log t, by the trapezoid rule on a fine grid."""
    grid = np.linspace(2, xs.max(), 400001)
    vals = 1 / np.log(grid)
    cum = np.concatenate([[0], np.cumsum((vals[1:] + vals[:-1]) / 2 * np.diff(grid))])
    return np.interp(xs, grid, cum)


# ---------------------------------------------------------------------------
# 1. Primes and their wobble
# ---------------------------------------------------------------------------

def fig_primes():
    N = 1_000_000
    is_p = sieve(N)
    pi = np.cumsum(is_p)
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        ax = fig.add_axes([0.06, 0.13, 0.40, 0.66])
        xs = np.arange(2, 101)
        ax.step(xs, pi[xs], where="post", color=th["s1"], label="primes up to x (counted)")
        xx = np.linspace(2, 100, 400)
        ax.plot(xx, li(xx), color=th["s2"], label="smooth estimate")
        ax.set_xlabel("x")
        ax.set_xlim(0, 100)
        ax.legend(loc="upper left", fontsize=10)
        ax2 = fig.add_axes([0.56, 0.13, 0.42, 0.66])
        xs = np.unique(np.geomspace(100, N, 3000).astype(int))
        err = li(xs.astype(float)) - pi[xs]
        ax2.plot(xs, err, color=th["s1"], lw=1.6, label="estimate minus true count")
        env = np.sqrt(xs) * np.log(xs) / (8 * math.pi)
        ax2.plot(xs, env, color=th["s3"], lw=2, ls=(0, (4, 2)),
                 label=r"size allowed by the Riemann hypothesis")
        ax2.plot(xs, -env, color=th["s3"], lw=2, ls=(0, (4, 2)))
        ax2.set_xscale("log")
        ax2.set_xlabel("x (log scale)")
        ax2.legend(loc="upper left", fontsize=10)
        title(fig, "Primes follow a smooth curve, with a wobble",
              "Computed. Left: the count of primes up to x against the smooth estimate. Right: the error up to a "
              "million,\nwhich stays inside the band the Riemann hypothesis predicts.", th)
        save(fig, "primes", mode)


# ---------------------------------------------------------------------------
# 2. The critical strip
# ---------------------------------------------------------------------------

def fig_strip():
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.6))
        panels = [("What was known before", False), ("What the paper claims", True)]
        for k, (name, new) in enumerate(panels):
            ax = fig.add_axes([0.06 + 0.48 * k, 0.11, 0.40, 0.60])
            ax.set_xlim(-0.05, 1.12)
            ax.set_ylim(0, 62)
            ax.axvspan(0, 1, color=th["mid"], zorder=0)
            ts = np.linspace(0, 62, 300)
            w = 0.3 / np.log(ts + 4)   # schematic width of the classical region
            ax.fill_betweenx(ts, 1 - w, 1, color=th["s3"], alpha=0.35, lw=0, zorder=1)
            ax.fill_betweenx(ts, 0, w, color=th["s3"], alpha=0.35, lw=0, zorder=1)
            if new:
                ax.axvspan(7 / 8, 1, color=th["new"], lw=0, zorder=2)
                ax.axvspan(0, 1 / 8, color=th["new"], lw=0, zorder=2)
                ax.axvline(7 / 8, color=th["s2"], lw=1.6, ls=(0, (4, 2)))
                ax.axvline(1 / 8, color=th["s2"], lw=1.6, ls=(0, (4, 2)))
                ax.text(15 / 16, 63, "claimed\nzero-free", ha="center", va="bottom", fontsize=9.5,
                        color=th["s2"], fontweight="bold")
            else:
                ax.text(0.97, 63, "proved\nzero-free", ha="center", va="bottom", fontsize=9.5, color=th["s3"],
                        fontweight="bold")
            ax.axvline(0.5, color=th["s1"], lw=1.6, ls=(0, (4, 2)))
            ax.plot([0.5] * len(ZEROS), ZEROS, "o", color=th["s1"], ms=6, zorder=3)
            ax.set_xticks([0, 1 / 8, 0.5, 7 / 8, 1])
            ax.set_xticklabels(["0", "1/8", "1/2", "7/8", "1"])
            ax.set_xlabel("real part of s")
            if k == 0:
                ax.set_ylabel("height (imaginary part of s)")
            ax.set_title(name, fontsize=12, color=th["ink"], loc="left", pad=30)
        title(fig, "Where the zeros of zeta may be",
              "The grey band is the critical strip. Blue dots: the first 13 zeros, all on the line at 1/2. Green: "
              "the classical zero-free\nzone, whose width shrinks with height (schematic width). Orange: the "
              "fixed-width zone the paper claims.", th)
        save(fig, "strip", mode)


# ---------------------------------------------------------------------------
# 3. The Moebius walk
# ---------------------------------------------------------------------------

def fig_mobius():
    N = 10_000_000
    mu = mobius(N)
    M = np.cumsum(mu.astype(np.int64))
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        ax = fig.add_axes([0.06, 0.13, 0.40, 0.66])
        xs = np.arange(1, 100_001)
        ax.plot(xs, M[xs], color=th["s1"], lw=1.0, label="running total of the coin flips")
        ax.plot(xs, np.sqrt(xs), color=th["s3"], lw=2, ls=(0, (4, 2)), label=r"$\pm\sqrt{x}$")
        ax.plot(xs, -np.sqrt(xs), color=th["s3"], lw=2, ls=(0, (4, 2)))
        ax.set_xlabel("x")
        ax.legend(loc="lower left", fontsize=10)
        ax2 = fig.add_axes([0.56, 0.13, 0.42, 0.66])
        xs = np.unique(np.geomspace(10, N, 2000).astype(int))
        runmax = np.maximum.accumulate(np.abs(M))
        ax2.plot(xs, runmax[xs], color=th["s1"], label="largest size so far")
        for e, lab, c, ls in [(1.0, "x  (no cancellation)", th["muted"], "-"),
                              (7 / 8, r"$x^{7/8}$  (what the claim guarantees)", th["s2"], (0, (4, 2))),
                              (0.5, r"$x^{1/2}$  (Riemann hypothesis)", th["s3"], (0, (4, 2)))]:
            ax2.plot(xs, xs.astype(float) ** e, color=c, lw=2, ls=ls, label=lab)
        ax2.set_xscale("log")
        ax2.set_yscale("log")
        ax2.set_xlabel("x (log scale)")
        ax2.legend(loc="upper left", fontsize=10)
        title(fig, "The Möbius coin flips cancel",
              "Computed up to ten million. Each whole number scores +1, −1 or 0 from its prime factors. The "
              "running total stays tiny\ncompared with x. A zero-free half-plane is the same as a guaranteed "
              "growth limit for this total.", th)
        save(fig, "mobius", mode)


# ---------------------------------------------------------------------------
# 4. The family trick (schematic)
# ---------------------------------------------------------------------------

def fig_family():
    rng = np.random.default_rng(7)
    n = 60
    base = rng.exponential(1.0, n)
    copies = rng.choice(n, 9, replace=False)
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        for k, big in enumerate([True, False]):
            ax = fig.add_axes([0.05 + 0.49 * k, 0.12, 0.43, 0.62])
            vals = base.copy()
            vals[copies] = 9.0 if big else 0.6
            cols = [th["s2"] if i in copies else th["s1"] for i in range(n)]
            ax.bar(np.arange(n), vals, color=cols, width=0.8)
            budget = 1.6
            ax.axhline(budget, color=th["s3"], lw=2, ls=(0, (4, 2)), label="the proved bound on the average")
            avg = vals.mean()
            ax.axhline(avg, color=th["red"] if big else th["muted"], lw=1.8,
                       label="actual average: " + ("too big" if big else "fits"))
            ax.legend(loc="upper right", fontsize=10, frameon=True, facecolor=th["surface"], edgecolor=th["axis"])
            ax.set_ylim(0, 12.5)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlabel("the sums in the family")
            ax.set_ylabel("size of each sum")
            ax.set_title("if the one sum were big" if big else "so the one sum must be small", fontsize=12,
                         color=th["ink"], loc="left")
        title(fig, "Hiding one sum in a crowd",
              "Schematic. Orange bars are copies of the one sum we care about, which turns up many times in the "
              "family. The proof bounds\nthe average size of the whole family. If the one sum were big, its "
              "copies alone would push the average over that bound.", th)
        save(fig, "family", mode)


# ---------------------------------------------------------------------------
# 5. Eisenstein integers
# ---------------------------------------------------------------------------

def fig_eisenstein():
    R = 9
    is_p = sieve(R * R * 4)
    pts, prime = [], []
    for a in range(-R - 4, R + 5):
        for b in range(-R - 4, R + 5):
            x, y = a - b / 2, b * math.sqrt(3) / 2
            if x * x + y * y > R * R or (a == 0 and b == 0):
                continue
            n = a * a - a * b + b * b
            q = math.isqrt(n)
            p = is_p[n] or (q * q == n and is_p[q] and q % 3 == 2)
            pts.append((x, y))
            prime.append(p)
    pts = np.array(pts)
    prime = np.array(prime)
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 5.4))
        ax = fig.add_axes([0.02, 0.04, 0.50, 0.80])
        ax.set_aspect("equal")
        ax.axis("off")
        ax.plot(pts[~prime, 0], pts[~prime, 1], "o", color=th["muted"], ms=3.2, alpha=0.6)
        ax.plot(pts[prime, 0], pts[prime, 1], "o", color=th["s2"], ms=6)
        units = [(math.cos(k * math.pi / 3), math.sin(k * math.pi / 3)) for k in range(6)]
        for ux, uy in units:
            ax.plot([ux], [uy], "o", color=th["s1"], ms=7)
        ax.plot([0], [0], "o", color=th["ink"], ms=5)
        ax2 = fig.add_axes([0.55, 0.10, 0.43, 0.70])
        ax2.axis("off")
        lines = [("The Eisenstein integers", th["ink"], 14, "bold"),
                 (r"Numbers $a + b\,\omega$, where $\omega$ is a cube root of 1.", th["ink2"], 12, "normal"),
                 ("They sit on a grid of triangles, with six-fold symmetry.", th["ink2"], 12, "normal"),
                 ("", th["ink2"], 8, "normal"),
                 ("blue: the six units, which divide everything", th["s1"], 12, "normal"),
                 ("orange: Eisenstein primes, which cannot be split", th["s2"], 12, "normal"),
                 ("", th["ink2"], 8, "normal"),
                 ("They factor uniquely, like whole numbers.", th["ink2"], 12, "normal"),
                 ("Every Dirichlet L-function hides inside one", th["ink2"], 12, "normal"),
                 ("of their L-functions, so a zero-free region", th["ink2"], 12, "normal"),
                 ("proved here carries over to all of them.", th["ink2"], 12, "normal")]
        y = 0.96
        for text, c, size, weight in lines:
            ax2.text(0, y, text, color=c, fontsize=size, fontweight=weight, va="top", transform=ax2.transAxes)
            y -= 0.085 if size > 8 else 0.04
        title(fig, "The number system the proof works in",
              r"Computed: Eisenstein integers within distance 9 of 0, the field the paper calls $\mathbb{Q}(\sqrt{-3})$.",
              th)
        save(fig, "eisenstein", mode)


# ---------------------------------------------------------------------------
# 6. Least quadratic nonresidues
# ---------------------------------------------------------------------------

def fig_nonresidue():
    N = 2_000_000
    is_p = sieve(N)
    ps = np.nonzero(is_p)[0]
    ps = ps[ps > 2]
    least = np.empty(len(ps), dtype=int)
    for i, p in enumerate(ps):
        p = int(p)
        n = 2
        while pow(n, (p - 1) // 2, p) == 1:
            n += 1
        least[i] = n
    rec_idx = [0]
    for i in range(1, len(least)):
        if least[i] > least[rec_idx[-1]]:
            rec_idx.append(i)
    rec_idx = np.array(rec_idx)
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.8))
        ax = fig.add_axes([0.07, 0.13, 0.62, 0.66])
        ax.plot(ps, least, "o", color=th["s1"], ms=1.2, alpha=0.25, rasterized=True)
        ax.plot(ps[rec_idx], least[rec_idx], "o-", color=th["s2"], ms=5, lw=1.4, label="new records")
        xs = np.geomspace(3, N, 300)
        ax.plot(xs, np.log(xs) ** 2, color=th["s3"], lw=2, ls=(0, (4, 2)), label=r"$(\log p)^2$")
        ax.set_xscale("log")
        ax.set_xlabel("prime p (log scale)")
        ax.set_ylabel("smallest non-square mod p")
        ax.legend(loc="upper left", fontsize=10)
        ax2 = fig.add_axes([0.73, 0.13, 0.26, 0.66])
        ax2.axis("off")
        txt = ("Below every prime p, some\nsmall number fails to be a\nperfect square mod p.\n\n"
               "In data it is always tiny.\nThe paper's half-plane would\nprove it is at most a fixed\n"
               "power of log p for every p,\nso square roots mod p can be\nfound quickly without luck.")
        ax2.text(0, 0.98, txt, va="top", fontsize=11.5, color=th["ink2"], transform=ax2.transAxes)
        title(fig, "A consequence: small non-squares",
              f"Computed for all {len(ps):,} odd primes below two million. The largest value is {least.max()}.",
              th)
        save(fig, "nonresidue", mode)


# ---------------------------------------------------------------------------
# 7. Timeline
# ---------------------------------------------------------------------------

def fig_timeline():
    events = [(1859, "Riemann: zeros\ncontrol the primes"), (1896, "no zeros on the\nedge: prime\nnumber theorem"),
              (1899, "de la Vallée Poussin:\na thin zero-free zone"), (1935, "Siegel: a possible\nrogue real zero"),
              (1958, "Vinogradov–Korobov:\na slightly wider zone"), (2000, "Clay prize"),
              (2024, "Guth–Maynard:\nfewer zeros\nnear the edge"), (2026, "OpenAI: a fixed\nzone past 7/8\n(claimed)")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.6))
        ax = fig.add_axes([0.03, 0.06, 0.94, 0.76])
        ax.axis("off")
        ax.set_xlim(-0.6, len(events) - 0.4)
        ax.set_ylim(-1.6, 1.6)
        ax.plot([-0.4, len(events) - 0.6], [0, 0], color=th["axis"], lw=2)
        for k, (year, text) in enumerate(events):
            up = k % 2 == 0
            ax.plot([k], [0], "o", ms=9, color=th["s2"] if year == 2026 else th["s1"], zorder=3)
            ax.plot([k, k], [0, 0.3 if up else -0.3], color=th["axis"], lw=1)
            ax.text(k, 0.4 if up else -0.4, f"{year}\n{text}", ha="center", va="bottom" if up else "top",
                    fontsize=10, color=th["ink"])
        title(fig, "A century and a half of zero-free zones",
              "Evenly spaced steps, not to scale.", th)
        save(fig, "timeline", mode)


def main():
    fig_primes()
    fig_strip()
    fig_mobius()
    fig_family()
    fig_eisenstein()
    fig_nonresidue()
    fig_timeline()


if __name__ == "__main__":
    main()
