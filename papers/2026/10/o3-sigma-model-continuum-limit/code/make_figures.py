#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python o3_mc.py          # Monte Carlo of the lattice model, writes mc_results.json
    python make_figures.py   # writes ../figures/*.png from mc_results.json

Computed (from the Monte Carlo in o3_mc.py): `spins` (sampled configurations at
three couplings), `decay` (spin correlations against distance), `length` (the
correlation length against the coupling), `collapse` (correlations in the paper's
canonical units, at several couplings) and `blocking` (block averages of one sampled
configuration). `timeline` is a labelled diagram.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "figures"

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834", s3="#1baf7a", s4="#8a5cd1",
                  mid="#f0efec", red="#e34948"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926", s3="#199e70", s4="#9b74e0",
                 mid="#383835", red="#e66767"),
}
SEQ = ["#9ec5f4", "#6aa6ec", "#3987e5", "#2a6bc0", "#8a5cd1", "#eb6834", "#c2410c"]


def setup(th: dict, size=(10, 5.0)):
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12, "mathtext.fontset": "dejavusans",
        "axes.edgecolor": th["axis"], "axes.labelcolor": th["ink2"],
        "xtick.color": th["muted"], "ytick.color": th["muted"],
        "text.color": th["ink"], "axes.facecolor": th["surface"],
        "figure.facecolor": th["surface"], "savefig.facecolor": th["surface"],
        "axes.grid": True, "grid.color": th["grid"], "grid.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2.4,
        "lines.solid_capstyle": "round", "legend.frameon": False, "axes.axisbelow": True,
    })
    return plt.figure(figsize=size, dpi=160)


def title(fig, text: str, sub: str, th: dict):
    fig.text(0.012, 0.975, text, fontsize=16, fontweight="bold", color=th["ink"], va="top")
    fig.text(0.012, 0.915, sub, fontsize=11, color=th["ink2"], va="top")


def save(fig, name: str, mode: str):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}-{mode}.png")
    plt.close(fig)


def load():
    return json.loads((HERE / "mc_results.json").read_text())


def colours(q):
    """Map unit vectors to colours: the vector's direction, as RGB."""
    q = np.asarray(q)
    return np.clip((q + 1) / 2, 0, 1)


# ---------------------------------------------------------------------------

def fig_spins(res):
    pick = [r for r in res if r["beta"] in (0.6, 1.1, 1.6)]
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 4.6))
        for k, r in enumerate(pick):
            ax = fig.add_axes([0.03 + k * 0.33, 0.04, 0.28, 0.66])
            ax.imshow(colours(r["snapshot"]), interpolation="nearest")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(False)
            for s in ax.spines.values():
                s.set_visible(False)
            ax.set_title(f"β = {r['beta']}" + ("  (weak alignment)" if k == 0 else "  (strong)" if k == 2 else ""),
                         fontsize=12, color=th["ink"])
        title(fig, "Spins on a grid: sampled configurations of the O(3) model",
              "Computed (Monte Carlo, 32 × 32 window). Each square is a unit arrow in 3D, shown as a colour. "
              "Larger β: larger patches.", th)
        save(fig, "spins", mode)


def fig_decay(res):
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.2))
        ax = fig.add_axes([0.09, 0.13, 0.62, 0.66])
        for r, c in zip(res, SEQ):
            C = np.array(r["C_axis"])
            rr = np.arange(len(C))
            bad = np.nonzero(C < 5e-4)[0]              # stop where statistical noise takes over
            keep = (rr < (bad[0] if len(bad) else len(C))) & (rr <= 60)
            ax.semilogy(rr[keep], C[keep], color=c, lw=2, label=f"β = {r['beta']}  (L = {r['L']})")
        ax.set_xlabel("distance r (lattice steps)")
        ax.set_ylabel("correlation of two spins")
        ax.set_xlim(0, 60)
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=10)
        title(fig, "Spins forget each other exponentially fast",
              "Computed. On a log scale, exponential decay is a straight line; it gets slower as β grows.", th)
        save(fig, "decay", mode)


def fig_length(res):
    b = np.array([r["beta"] for r in res])
    xi = np.array([r["xi2"] for r in res])
    xim = np.array([1 / r["mass"] if r["mass"] and r["mass"] > 0 else np.nan for r in res])
    shape = lambda x: np.exp(2 * math.pi * x) / x                 # leading asymptotic-freedom form
    sel = b >= 1.3
    const = float(np.exp(np.mean(np.log(xi[sel] / shape(b[sel])))))
    grid = np.linspace(1.0, 1.75, 100)
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.2))
        ax = fig.add_axes([0.09, 0.13, 0.86, 0.66])
        ax.semilogy(grid, const * shape(grid), color=th["muted"], ls="--", lw=1.6,
                    label="shape e^(2πβ) / β from asymptotic freedom (constant fitted)")
        ax.semilogy(b, xi, "o", color=th["s1"], ms=8, label="second-moment correlation length ξ (computed)")
        ax.semilogy(b, xim, "s", color=th["s2"], ms=6, mfc="none", mew=2,
                    label="1 / mass gap, from row correlations (computed)")
        for x, y in zip(b, xi):
            ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points", xytext=(-6, 9), fontsize=9.5,
                        color=th["ink2"], ha="right")
        ax.set_xlabel("coupling β")
        ax.set_ylabel("correlation length (lattice steps)")
        ax.legend(loc="upper left", fontsize=10)
        title(fig, "The correlation length explodes as β grows",
              "Computed. Measured in lattice steps, ξ grows roughly like e^(2πβ): "
              "large β means a fine lattice in physical units.", th)
        save(fig, "length", mode)
    return dict(zip(b.tolist(), xi.tolist())), const


def fig_collapse(res):
    sel = [r for r in res if r["beta"] >= 1.1]
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.2))
        ax = fig.add_axes([0.09, 0.13, 0.62, 0.66])
        for r, c in zip(sel, SEQ[2:]):
            C = np.array(r["C_axis"])
            rr = np.arange(len(C))
            y = r["xi2"] ** 2 * C / r["chi"]
            x = rr / r["xi2"]
            keep = x <= 2.5                             # well inside half the lattice
            ax.semilogy(x[keep], y[keep], "o-", color=c, ms=3.5, lw=1.4,
                        label=f"β = {r['beta']}: ξ = {r['xi2']:.1f} lattice steps")
        ax.set_xlabel("distance in units of the correlation length, r / ξ")
        ax.set_ylabel("ξ² · correlation / χ")
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), fontsize=10)
        title(fig, "In the paper's units, the lattices agree",
              "Computed. Rescaled by ξ and χ (the paper's canonical units), curves from very different "
              "lattices fall on one: a continuum limit.", th)
        save(fig, "collapse", mode)


def block(q, k):
    L = q.shape[0] // k
    b = q[:L * k, :L * k].reshape(L, k, L, k, 3).sum(axis=(1, 3))
    return b / np.linalg.norm(b, axis=-1, keepdims=True)


def fig_blocking(res):
    r = next(r for r in res if r["beta"] == 1.6)
    q = np.array(r["snapshot"])
    levels = [(q, "32 × 32 spins"), (block(q, 2), "16 × 16 blocks"), (block(q, 4), "8 × 8 blocks"),
              (block(q, 8), "4 × 4 blocks")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 3.9))
        for k, (img, lab) in enumerate(levels):
            ax = fig.add_axes([0.02 + k * 0.245, 0.06, 0.21, 0.62])
            ax.imshow(colours(img), interpolation="nearest")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(False)
            for s in ax.spines.values():
                s.set_visible(False)
            ax.set_title(lab, fontsize=11.5, color=th["ink"])
            if k < 3:
                fig.text(0.02 + k * 0.245 + 0.222, 0.37, "→", fontsize=20, color=th["muted"], ha="center",
                         va="center")
        title(fig, "Blocking: replace each square of spins by one averaged spin",
              "Computed from one sampled configuration at β = 1.6. The paper does this exactly, "
              "keeping track of every correction.", th)
        save(fig, "blocking", mode)


def fig_timeline():
    events = [(1966, "Mermin–Wagner:\nno magnetization\nin 2D"), (1975, "Polyakov:\nasymptotic\nfreedom"),
              (1979, "Zamolodchikovs:\nexact scattering\n(integrability)"), (1980, "Kupiainen:\nmass gap for\nlarge N"),
              (1990, "Hasenfratz,\nMaggiore, Niedermayer:\nexact mass, O(3)"), (2000, "Clay: Yang–Mills\nmass gap\nprize problem"),
              (2026, "OpenAI: O(3)\ncontinuum limit\n(claimed)")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.6))
        ax = fig.add_axes([0.03, 0.04, 0.94, 0.80])
        ax.axis("off")
        ax.set_xlim(-0.6, len(events) - 0.4)
        ax.set_ylim(-1.8, 1.6)
        ax.plot([-0.4, len(events) - 0.6], [0, 0], color=th["axis"], lw=2)
        for k, (year, text) in enumerate(events):
            up = k % 2 == 0
            ax.plot([k], [0], "o", ms=9, color=th["s2"] if year == 2026 else th["s1"], zorder=3)
            ax.plot([k, k], [0, 0.3 if up else -0.3], color=th["axis"], lw=1)
            ax.text(k, 0.4 if up else -0.4, f"{year}\n{text}", ha="center", va="bottom" if up else "top",
                    fontsize=10, color=th["ink"])
        title(fig, "The two-dimensional O(3) model, from physics to proof", "Evenly spaced steps, not to scale.", th)
        save(fig, "timeline", mode)


def main():
    res = load()
    fig_spins(res)
    fig_decay(res)
    print("length:", fig_length(res))
    fig_collapse(res)
    fig_blocking(res)
    fig_timeline()


if __name__ == "__main__":
    main()
