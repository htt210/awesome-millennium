#!/usr/bin/env python3
"""Monte Carlo for the two-dimensional O(3) model (the lattice model of the paper),
with Wolff's single-cluster algorithm, in plain numpy/Python.

    python o3_mc.py               # runs every coupling, writes mc_results.json (about fifteen minutes)
    python o3_mc.py --quick       # a short run, as a test

The model: unit vectors q_x in R^3 on an L x L periodic square lattice, with weight
exp(beta * sum over neighbouring pairs of q_x . q_y).  For each beta we measure

  * C(r): the spin correlation along a lattice axis, E[q_0 . q_(r,0)] / 3 per component;
  * G(t): the correlation of whole rows ("zero momentum"), whose decay rate is the mass gap;
  * chi, xi2: the susceptibility and second-moment correlation length used by the paper
    to normalize its continuum fields (equation (1.2) there, per spin component);
  * m: the mass gap in lattice units, from a cosh fit to G(t); its inverse is the
    exponential correlation length.

Wolff's algorithm (Phys. Rev. Lett. 62, 361 (1989)) samples the model exactly; the
only errors here are statistical.  Seeds are fixed so the results are reproducible.
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUNS = [  # (beta, L, sweeps' worth of cluster updates used for measurement)
    (0.6, 32, 4000),
    (0.9, 32, 4000),
    (1.1, 64, 3000),
    (1.3, 64, 3000),
    (1.45, 128, 2000),
    (1.6, 192, 1500),
    (1.7, 256, 1000),
]


def random_unit(rng, size=None):
    v = rng.normal(size=(size, 3) if size else 3)
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def wolff_update(s, beta, rng, nbr):
    """One Wolff cluster flip on the flattened spins s (V x 3). Returns the cluster size."""
    V = s.shape[0]
    r = random_unit(rng)
    proj = s @ r                                       # projections before the flip
    seed = int(rng.integers(V))
    in_cluster = np.zeros(V, dtype=bool)
    in_cluster[seed] = True
    stack = [seed]
    members = [seed]
    rand = rng.random
    while stack:
        i = stack.pop()
        pi = proj[i]
        for j in nbr[i]:
            if in_cluster[j]:
                continue
            x = 2.0 * beta * pi * proj[j]
            if x > 0 and rand() < 1.0 - math.exp(-x):
                in_cluster[j] = True
                stack.append(j)
                members.append(j)
    m = np.array(members)
    s[m] -= 2.0 * np.outer(proj[m], r)
    return len(members)


def neighbours(L):
    idx = np.arange(L * L).reshape(L, L)
    return [tuple(int(v) for v in (idx[(x + 1) % L, y], idx[(x - 1) % L, y], idx[x, (y + 1) % L],
                                    idx[x, (y - 1) % L])) for x in range(L) for y in range(L)]


def measure(s, L):
    q = s.reshape(L, L, 3)
    f = np.fft.fft2(q, axes=(0, 1))
    corr = np.fft.ifft2((f * f.conj()).real, axes=(0, 1)).real.sum(axis=2) / (L * L)   # sum_x q_x . q_(x+r)
    rows = q.sum(axis=1)                                                                   # row sums, L x 3
    fr = np.fft.fft(rows, axis=0)
    G = np.fft.ifft((fr * fr.conj()).real, axis=0).real.sum(axis=1) / L                   # row-row correlation
    return corr, G


def fit_mass(G, L, tmin):
    """Fit G(t) ~ A cosh(m (t - L/2)) by the effective mass from ratios, averaged over a window."""
    t = np.arange(L)
    g = G / G[0]
    ms = []
    for k in range(tmin, L // 2 - 1):
        a, b, c = g[k - 1], g[k], g[k + 1]
        if b <= 0 or a <= 0 or c <= 0:
            break
        x = (a + c) / (2 * b)              # cosh(m) for a pure cosh; robust to the periodic image
        if x <= 1:
            break
        ms.append(math.acosh(x))
    return float(np.median(ms)) if ms else float("nan"), t


def run(beta, L, sweeps, seed, therm_frac=0.2):
    rng = np.random.default_rng(seed)
    nbr = neighbours(L)
    s = random_unit(rng, L * L)
    V = L * L
    # thermalize: cluster updates until roughly therm_frac * sweeps sweeps' worth of sites were flipped
    flipped, target = 0, therm_frac * sweeps * V
    while flipped < target:
        flipped += wolff_update(s, beta, rng, nbr)
    corr_sum = np.zeros((L, L))
    G_sum = np.zeros(L)
    nmeas = 0
    flipped, target, next_meas = 0, sweeps * V, 0
    snapshot = None
    while flipped < target:
        flipped += wolff_update(s, beta, rng, nbr)
        if flipped >= next_meas:
            c, g = measure(s, L)
            corr_sum += c
            G_sum += g
            nmeas += 1
            next_meas = flipped + V // 2
            if snapshot is None and flipped > target / 2:
                snapshot = s.reshape(L, L, 3)[:32, :32].copy()
    corr = corr_sum / nmeas / 3.0                       # per component: E[q^1_0 q^1_r]
    G = G_sum / nmeas
    chi = float(corr.sum())
    xs = np.minimum(np.arange(L), L - np.arange(L))
    r2 = xs[:, None] ** 2 + xs[None, :] ** 2
    xi2 = math.sqrt(float((r2 * corr).sum()) / (4 * chi))
    m, _ = fit_mass(G, L, tmin=max(2, int(0.5 * xi2)))
    return dict(beta=beta, L=L, measurements=nmeas, chi=chi, xi2=xi2, mass=m,
                C_axis=[float(v) for v in corr[0, :L // 2 + 1]], G=[float(v) for v in G[:L // 2 + 1]],
                snapshot=snapshot.round(4).tolist())


def main(argv):
    quick = "--quick" in argv
    runs = [(0.9, 16, 200), (1.3, 32, 200)] if quick else RUNS
    out = []
    for k, (beta, L, sweeps) in enumerate(runs):
        t0 = time.time()
        r = run(beta, L, sweeps, seed=1000 + k)
        print(f"beta={beta:<5} L={L:<4} meas={r['measurements']:<5} chi={r['chi']:8.2f} xi2={r['xi2']:7.3f} "
              f"1/m={1 / r['mass'] if r['mass'] == r['mass'] and r['mass'] > 0 else float('nan'):7.3f} "
              f"({time.time() - t0:.0f} s)", flush=True)
        out.append(r)
    if not quick:
        (HERE / "mc_results.json").write_text(json.dumps(out))
        print("wrote mc_results.json")


if __name__ == "__main__":
    main(sys.argv[1:])
