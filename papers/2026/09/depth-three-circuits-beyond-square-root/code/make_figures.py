#!/usr/bin/env python3
"""Figures for the plain-language explainer (../README.md), light and dark.

    pip install -r requirements.txt
    python make_figures.py            # writes ../figures/*.png
    python make_figures.py --check    # quick self-test only, no figures

Computed: `circuit` (a three-layer circuit for 4-bit parity, checked on all 16
inputs), `parity` (the size of the standard three-layer parity circuit, best block
split, against the square root of n), `restriction` (a wide CNF under random
restrictions: how many clauses survive, and how wide they are) and `language`
(the paper's language, implemented exactly as defined, at n = 20480: its input
blocks, and the fraction of inputs it accepts for random parameter settings).
`proof` and `timeline` are labelled diagrams.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

OUT = Path(__file__).resolve().parent.parent / "figures"

THEMES = {
    "light": dict(surface="#fcfcfb", ink="#0b0b0b", ink2="#52514e", muted="#898781",
                  grid="#e1e0d9", axis="#c3c2b7", s1="#2a78d6", s2="#eb6834", s3="#1baf7a", s4="#8a5cd1",
                  mid="#f0efec", red="#e34948"),
    "dark": dict(surface="#1a1a19", ink="#f0efec", ink2="#c3c2b7", muted="#898781",
                 grid="#2c2c2a", axis="#383835", s1="#3987e5", s2="#d95926", s3="#199e70", s4="#9b74e0",
                 mid="#383835", red="#e66767"),
}


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


# ---------------------------------------------------------------------------
# 1. Three-layer parity circuits
# ---------------------------------------------------------------------------
# Split the n inputs into m blocks.  Parity is the XOR of the block parities y_j.
# Top OR over the 2^(m-1) odd patterns of (y_1..y_m); each pattern is an AND of
# "y_j = 1" or "y_j = 0", and each of those is a CNF on block j with 2^(b_j - 1)
# clauses.  An AND of CNFs is one CNF, so the circuit is OR (top) - AND (middle)
# - OR (bottom clauses): the model of the paper.

def block_sizes(n: int, m: int) -> list[int]:
    q, r = divmod(n, m)
    return [q + 1] * r + [q] * (m - r)


def parity_circuit(n: int, m: int):
    """Return (bottom clauses, middle gates); a clause is a tuple of (variable, value making it true)."""
    sizes = block_sizes(n, m)
    starts = [sum(sizes[:j]) for j in range(m)]
    clauses, index = [], {}

    def cnf(block: int, value: int) -> list[int]:
        """Clauses of 'parity of this block = value': one clause rules out each wrong assignment."""
        key = (block, value)
        if key not in index:
            vs = list(range(starts[block], starts[block] + sizes[block]))
            ids = []
            for a in range(2 ** len(vs)):
                bits = [(a >> i) & 1 for i in range(len(vs))]
                if sum(bits) % 2 != value:
                    ids.append(len(clauses))
                    clauses.append(tuple((v, 1 - bit) for v, bit in zip(vs, bits)))
            index[key] = ids
        return index[key]

    middle = []
    for pat in range(2 ** m):
        ys = [(pat >> j) & 1 for j in range(m)]
        if sum(ys) % 2 == 1:
            middle.append(sorted(c for j in range(m) for c in cnf(j, ys[j])))
    return clauses, middle


def evaluate(clauses, middle, x) -> int:
    val = [any(x[v] == s for v, s in c) for c in clauses]
    return int(any(all(val[c] for c in g) for g in middle))


def parity_size(n: int, m: int) -> int:
    """Gate count of the circuit above for m >= 2, without building it: bottom + middle + top."""
    return sum(2 ** b for b in block_sizes(n, m)) + 2 ** (m - 1) + 1


def best_parity_size(n: int) -> tuple[int, int]:
    """Best number of blocks.  The optimum is near sqrt(n): fewer blocks make each block's CNF
    huge, more blocks make the top layer huge, so only that window is searched for large n."""
    lo, hi = (2, n) if n <= 64 else (max(2, math.isqrt(n) // 2), 2 * math.isqrt(n) + 2)
    return min((parity_size(n, m), m) for m in range(lo, hi + 1))


def check_parity():
    for n, m in [(4, 2), (6, 2), (6, 3), (7, 3)]:
        clauses, middle = parity_circuit(n, m)
        assert len(clauses) + len(middle) + 1 == parity_size(n, m)
        for a in range(2 ** n):
            x = [(a >> i) & 1 for i in range(n)]
            assert evaluate(clauses, middle, x) == sum(x) % 2
    return parity_circuit(4, 2)


def fig_circuit():
    clauses, middle = check_parity()
    names = ["x₁", "x₂", "x₃", "x₄"]
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.6))
        ax = fig.add_axes([0.03, 0.02, 0.94, 0.82])
        ax.axis("off")
        ax.set_xlim(-0.5, 9.5)
        ax.set_ylim(-0.3, 4.2)
        xs_in = [1.5, 3.5, 5.5, 7.5]
        xs_bot = np.linspace(0.6, 8.4, len(clauses))
        xs_mid = [3.0, 6.0]
        for i, c in enumerate(clauses):
            for v, _ in c:
                ax.plot([xs_bot[i], xs_in[v]], [1.2, 0.2], color=th["grid"], lw=1, zorder=1)
        for k, g in enumerate(middle):
            for c in g:
                ax.plot([xs_mid[k], xs_bot[c]], [2.5, 1.6], color=th["axis"], lw=1.2, zorder=1)
            ax.plot([4.5, xs_mid[k]], [3.6, 2.95], color=th["axis"], lw=1.6, zorder=1)
        for v, x in enumerate(xs_in):
            ax.text(x, 0.05, names[v], ha="center", va="center", fontsize=14, color=th["ink"])
        for i, x in enumerate(xs_bot):
            ax.add_patch(FancyBboxPatch((x - 0.42, 1.2), 0.84, 0.4, boxstyle="round,pad=0.02",
                                        fc=th["mid"], ec=th["s1"], lw=1.4, zorder=2))
            ax.text(x, 1.4, "OR", ha="center", va="center", fontsize=9, color=th["s1"], zorder=3)
            lits = "∨".join(("" if s else "¬") + names[v] for v, s in clauses[i])
            ax.text(x, 1.78, lits, ha="center", va="center", fontsize=7.5, color=th["muted"], zorder=3)
        for x in xs_mid:
            ax.add_patch(FancyBboxPatch((x - 0.5, 2.5), 1.0, 0.45, boxstyle="round,pad=0.02",
                                        fc=th["mid"], ec=th["s3"], lw=1.6, zorder=2))
            ax.text(x, 2.72, "AND", ha="center", va="center", fontsize=10, color=th["s3"], zorder=3)
        ax.add_patch(FancyBboxPatch((4.0, 3.6), 1.0, 0.45, boxstyle="round,pad=0.02",
                                    fc=th["mid"], ec=th["s2"], lw=1.8, zorder=2))
        ax.text(4.5, 3.82, "OR", ha="center", va="center", fontsize=10, color=th["s2"], zorder=3)
        ax.text(9.4, 3.82, "top: 1 gate", ha="right", va="center", fontsize=10, color=th["s2"])
        ax.text(9.4, 2.72, f"middle: {len(middle)} gates", ha="right", va="center", fontsize=10,
                color=th["s3"])
        ax.text(9.4, 0.6, f"bottom: {len(clauses)} gates", ha="right", va="center", fontsize=10,
                color=th["s1"])
        title(fig, f"A three-layer circuit for parity of 4 bits: {len(clauses) + len(middle) + 1} gates",
              "Computed and checked on all 16 inputs. It outputs 1 exactly when an odd number of inputs are 1.",
              th)
        save(fig, "circuit", mode)


def fig_parity():
    ns = np.unique(np.round(np.geomspace(16, 40000, 140)).astype(int))
    ratio = [math.log2(best_parity_size(int(n))[0]) / math.sqrt(n) for n in ns]
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.2))
        ax = fig.add_axes([0.09, 0.13, 0.86, 0.66])
        ax.plot(ns, ratio, color=th["s1"], label="parity: best three-layer circuit of this kind (computed)")
        ax.axhline(1, color=th["muted"], ls="--", lw=1.2)
        ax.text(ns[-1], 1.05, "exponent = √n", ha="right", va="bottom", fontsize=10, color=th["muted"])
        for a in (2, 4):
            ax.axhline(a, color=th["s2"], ls=":", lw=1.2)
            ax.text(ns[0], a + 0.06, f"exponent = {a}√n", fontsize=10, color=th["s2"], va="bottom")
        ax.annotate("claimed: one explicit function\nends up above every such line",
                    xy=(ns[-1] * 0.9, 4.75), xytext=(ns[0] * 6, 4.75), fontsize=11, color=th["s2"],
                    va="center", arrowprops=dict(arrowstyle="-|>", color=th["s2"], lw=1.6))
        ax.set_xscale("log")
        ax.set_ylim(0, 5.3)
        ax.set_xlabel("number of inputs n")
        ax.set_ylabel("log₂(gates) ÷ √n")
        ax.legend(loc="lower left", fontsize=10)
        title(fig, "Parity sits at the square-root scale",
              "The ratio for parity tends to 1: about 2^√n gates, known to be optimal up to a constant factor.",
              th)
        save(fig, "parity", mode)
    return ratio[-1]


# ---------------------------------------------------------------------------
# 2. Random restrictions
# ---------------------------------------------------------------------------

def restriction_trial(rng, d=400, k=20, clauses=1_000_000, p=0.1, batch=10_000):
    """One random width-k CNF on d variables, one p-random restriction.
    Returns the widths of the clauses that survive (no fixed literal made them true)."""
    live = rng.random(d) < p
    rho = rng.integers(0, 2, d)
    out = []
    for start in range(0, clauses, batch):
        c = min(batch, clauses - start)
        scopes = np.argpartition(rng.random((c, d)), k, axis=1)[:, :k]   # k distinct variables
        signs = rng.integers(0, 2, (c, k))                                 # value that makes the literal true
        fixed = ~live[scopes]
        sat = (fixed & (rho[scopes] == signs)).any(axis=1)                 # a true fixed literal: clause vanishes
        out.append(live[scopes].sum(axis=1)[~sat])
    return np.concatenate(out)


def fig_restriction(trials=6, seed=3, d=400, k=20, clauses=1_000_000, p=0.1):
    rng = np.random.default_rng(seed)
    hist = np.zeros(k + 1)
    survived = []
    for _ in range(trials):
        w = restriction_trial(rng, d, k, clauses, p)
        survived.append(len(w))
        hist += np.bincount(w, minlength=k + 1)
    hist /= trials
    mean_surv = float(np.mean(survived))
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.2))
        ax = fig.add_axes([0.09, 0.13, 0.86, 0.64])
        ax.bar([k], [clauses], color=th["muted"], width=0.7, label=f"before: {clauses:,} clauses, all of width {k}")
        ax.bar(np.arange(k + 1), hist, color=th["s1"], width=0.7,
               label=f"after (average of {trials} restrictions): {mean_surv:.0f} clauses left")
        ax.set_yscale("log")
        ax.set_ylim(0.1, clauses * 4)
        ax.set_xlabel("clause width (number of free variables a clause still reads)")
        ax.set_ylabel("number of clauses")
        ax.set_xticks(range(0, k + 1, 2))
        ax.legend(loc="upper left", fontsize=10)
        title(fig, "A random restriction shrinks a wide formula",
              f"Computed: {d} variables, each left free with probability {p}, the rest fixed at random. "
              "A clause with a true fixed literal vanishes.", th)
        save(fig, "restriction", mode)
    return mean_surv, hist


# ---------------------------------------------------------------------------
# 3. The language, exactly as defined (Definition 4.1 of the paper)
# ---------------------------------------------------------------------------

def params(n: int):
    d = n // 5
    if d < 64:
        return None
    r = 1
    while r ** 3 < d * d:          # r = ceil(d^(2/3)), in integers
        r += 1
    t = 0
    while (t + 2) ** 6 <= d:       # largest even t with t^6 <= d
        t += 2
    return d, r, t


def pmulmod(a: int, b: int, P: int, r: int) -> int:
    """Multiply polynomials over GF(2) (bit i = coefficient of Z^i), reduced mod P of degree r."""
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if (a >> r) & 1:
            a ^= P
    return out


def pmod(a: int, P: int) -> int:
    r = P.bit_length() - 1
    while a and a.bit_length() - 1 >= r:
        a ^= P << (a.bit_length() - 1 - r)
    return a


def pgcd(a: int, b: int) -> int:
    while b:
        a, b = b, pmod(a, b)
    return a


def irreducible(P: int) -> bool:
    """Rabin's irreducibility test over GF(2)."""
    r = P.bit_length() - 1

    def frob(k):                   # Z^(2^k) mod P
        y = 2
        for _ in range(k):
            y = pmulmod(y, y, P, r)
        return y
    if frob(r) != 2:
        return False
    primes = [q for q in range(2, r + 1) if r % q == 0 and all(q % s for s in range(2, q))]
    return all(pgcd(P, frob(r // q) ^ 2) == 1 for q in primes)


def find_irreducible(r: int, rng) -> int:
    while True:
        P = (1 << r) | (int.from_bytes(rng.bytes(r // 8 + 1), "little") % (1 << r)) | 1
        if irreducible(P):
            return P


def member(bits: list[int]) -> int:
    """The membership test of the paper's language L on one input, written out directly."""
    n = len(bits)
    pr = params(n)
    if pr is None:
        return 0
    d, r, t = pr
    if n < 2 * d + (t + 2) * r - 1:
        return 0
    x = bits[:d]
    u = bits[d:2 * d + r - 1]
    praw = bits[2 * d + r - 1:2 * d + 2 * r - 1]
    P = (1 << r) | sum(b << i for i, b in enumerate(praw))
    base = 2 * d + 2 * r - 1
    beta = [sum(b << i for i, b in enumerate(bits[base + j * r: base + (j + 1) * r])) for j in range(t)]
    ones = [s for s in range(d) if x[s]]
    h = 0
    for i in range(r):             # h_i = sum_s u_{i+s-1} x_s (mod 2)
        if sum(u[i + s] for s in ones) & 1:
            h |= 1 << i
    acc, power = 0, 1
    for j in range(t):             # sum_j beta_j h^j in GF(2)[Z]/(P)
        acc ^= pmulmod(beta[j], power, P, r)
        power = pmulmod(power, h, P, r)
    return int((acc & 1) == 0)     # accept when the constant coefficient is 0


def slice_evaluator(n: int, P: int, u: list[int], betas: list[int]):
    """The same test with the parameter bits fixed (a 'slice'), with the hash done by numpy."""
    d, r, t = params(n)
    hankel = np.array([u[i:i + d] for i in range(r)], dtype=np.int32)
    beta = [sum(int(b) << i for i, b in enumerate(betas[j * r:(j + 1) * r])) for j in range(t)]

    def g(x) -> int:
        hb = (hankel @ np.asarray(x, dtype=np.int32)) & 1
        h = sum(int(b) << i for i, b in enumerate(hb))
        acc, power = 0, 1
        for j in range(t):
            acc ^= pmulmod(beta[j], power, P, r)
            power = pmulmod(power, h, P, r)
        return int((acc & 1) == 0)
    return g


def language_rates(n=20480, settings=12, samples=1500, seed=7, checks=5):
    rng = np.random.default_rng(seed)
    d, r, t = params(n)
    used = 2 * d + (t + 2) * r - 1
    rates = []
    for k in range(settings):
        P = find_irreducible(r, rng)
        u = [int(b) for b in rng.integers(0, 2, d + r - 1)]
        pbits = [(P >> i) & 1 for i in range(r)]
        betas = [int(b) for b in rng.integers(0, 2, t * r)]
        rest = [0] * (n - used)
        g = slice_evaluator(n, P, u, betas)
        acc = 0
        for s in range(samples):
            x = [int(b) for b in rng.integers(0, 2, d)]
            v = g(x)
            if k == 0 and s < checks:              # the fast slice agrees with the direct test
                assert v == member(x + u + pbits + betas + rest)
            acc += v
        rates.append(acc / samples)
    return (d, r, t), rates


def fig_language(n=20480, settings=12, samples=1500):
    (d, r, t), rates = language_rates(n, settings, samples)
    blocks = [("data x", d), ("hash bits u", d + r - 1), ("P", r), (f"{t} coefficients β", t * r)]
    used = sum(b for _, b in blocks)
    for mode, th in THEMES.items():
        fig = setup(th, size=(10, 5.6))
        ax = fig.add_axes([0.03, 0.55, 0.94, 0.22])
        ax.axis("off")
        ax.set_xlim(0, n)
        ax.set_ylim(-0.3, 1.3)
        x0 = 0
        cols = [th["s1"], th["s4"], th["s2"], th["s3"], th["mid"]]
        for k, ((lab, w), c) in enumerate(zip(blocks + [("ignored", n - used)], cols)):
            ax.add_patch(plt.Rectangle((x0, 0.1), w, 0.5, fc=c, ec=th["surface"], lw=1.5))
            if k == 2:                                   # the thin block: label below the bar
                ax.text(x0 + w / 2, 0.02, f"{lab}: {w:,} bits", ha="center", va="top", fontsize=9.5,
                        color=th["ink"])
            else:
                ax.text(x0 + w / 2, 0.68, f"{lab}\n{w:,} bits", ha="center", va="bottom", fontsize=9.5,
                        color=th["ink"])
            x0 += w
        ax2 = fig.add_axes([0.09, 0.1, 0.86, 0.32])
        ax2.bar(range(1, settings + 1), rates, color=th["s1"], width=0.6)
        ax2.axhline(0.5, color=th["muted"], ls="--", lw=1.2)
        ax2.set_ylim(0, 1)
        ax2.set_xticks(range(1, settings + 1))
        ax2.set_xlabel("random setting of the hash and coefficient bits (a 'slice')")
        ax2.set_ylabel("fraction\naccepted")
        title(fig, f"The paper's language at n = {n:,}: d = {d:,}, r = {r}, t = {t}",
              f"Computed: membership as defined, {samples:,} random data blocks per setting. "
              "Each slice accepts about half its inputs.", th)
        save(fig, "language", mode)
    return (d, r, t), rates


# ---------------------------------------------------------------------------
# 4. Diagrams
# ---------------------------------------------------------------------------

def fig_proof():
    steps = [("1. One language", "Evaluate a polynomial\nat a hash of the data.\nFast to compute.", "s1"),
             ("2. A hard slice", "Fix the extra bits well:\nnarrow CNFs barely\ncorrelate with it.", "s4"),
             ("3. Restriction lemma", "A random restriction turns\nany width-k CNF into narrow\nones, total weight ≤ 2.", "s3"),
             ("4. Counting gates", "Each middle AND accepts\nfew inputs. Too few gates\ncannot cover ¼ of them.", "s2")]
    for mode, th in THEMES.items():
        fig = setup(th, size=(11, 4.2))
        ax = fig.add_axes([0.02, 0.04, 0.96, 0.78])
        ax.axis("off")
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 1)
        for i, (head, body, c) in enumerate(steps):
            ax.add_patch(FancyBboxPatch((i + 0.06, 0.1), 0.82, 0.8, boxstyle="round,pad=0.02",
                                        fc=th["mid"], ec=th[c], lw=2))
            ax.text(i + 0.47, 0.78, head, ha="center", va="center", fontsize=11.5, fontweight="bold",
                    color=th[c])
            ax.text(i + 0.47, 0.42, body, ha="center", va="center", fontsize=10.5, color=th["ink"])
            if i < 3:
                ax.annotate("", xy=(i + 1.05, 0.5), xytext=(i + 0.9, 0.5),
                            arrowprops=dict(arrowstyle="-|>", color=th["axis"], lw=1.8))
        title(fig, "The route of the proof", "A labelled diagram of Sections 2 to 5 of the paper.", th)
        save(fig, "proof", mode)


def fig_timeline():
    events = [(1989, "Håstad: parity\nneeds 2^Ω(√n)\ngates"), (1995, "Håstad, Jukna,\nPudlák: top-down\nbounds"),
              (1999, "Paturi, Pudlák,\nZane: parity\nexactly ≈ 2^√n"),
              (2000, "Paturi, Saks,\nZane: 2^(n−o(n))\nfor fan-in 2"),
              (2005, "Paturi, Pudlák,\nSaks, Zane:\n(π/√6)·√n"), (2024, "Gurumukhani\net al.: the\nquestion, open"),
              (2026, "OpenAI: past\nevery constant\n(claimed)")]
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
        title(fig, "Lower bounds for three-layer circuits", "Evenly spaced steps, not to scale.", th)
        save(fig, "timeline", mode)


def main(argv):
    if "--check" in argv:
        check_parity()
        assert params(20480) == (4096, 256, 4)
        assert irreducible(0b10011) and not irreducible(0b10101)       # Z^4+Z+1 yes, (Z^2+Z+1)^2 no
        print("language (small run):", language_rates(settings=2, samples=50, checks=3))
        print("ok")
        return
    fig_circuit()
    print("parity ratio at n = 40000:", fig_parity())
    print("restriction:", fig_restriction())
    print("language:", fig_language())
    fig_proof()
    fig_timeline()


if __name__ == "__main__":
    main(sys.argv[1:])
