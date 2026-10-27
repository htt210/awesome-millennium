#!/usr/bin/env python3
"""Toy, fully checked implementation of the counting algorithm in
"The Exponential Time Hypothesis is False" (OpenAI, 25 October 2026).

It follows Section 2 of the paper ("Technique overview"): exact counting of
satisfying assignments of a CNF in which every clause has at most three
literals and every variable occurs in at most three clauses.

This is NOT a fast SAT counter.  The paper's parameter choices only pay off
for astronomically large n (see `galactic_threshold` below).  The point is to
make every identity the algorithm relies on executable, and to check each one
against brute force on random small formulas:

  (1) restore      H(0) = #F: the replacement forms restore every input at T = 0
  (2) design       at every t in [Q] a clause reads only its own group of
                   variables plus a few shared integer "measurements"
  (3) separation   H(t) = sum_y prod_g B_{t,g}(y)  (fix measurements, then
                   every group is summed independently)
  (4) Taylor       H(t+z) mod z^J from the restricted sums Z_{t,E,U}
                   (inclusion-exclusion over at most q-element sets E)
  (5) Hermite      the Taylor data at t = 1..Q determine H, hence H(0) = #F

together with the matrix facts behind the construction (Section 2, Step 2)
and the Beigel-Tarui parity polynomial of Lemma 5.1.

Arithmetic: the matrix construction is done with exact Fractions.  The heavy
sums run modulo the Mersenne prime 2^61 - 1.  Every quantity is a rational
number whose denominator is a product of small integers, and the final answer
#F <= 2^n is far below the modulus, so the answer is recovered exactly.

Usage:
    python toy_eth.py            # run all checks (about 30 seconds)
    python toy_eth.py --quick    # smaller instances (about a second)
"""

from __future__ import annotations

import argparse
import itertools
import math
import random
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from functools import lru_cache

MOD = (1 << 61) - 1  # prime


# ---------------------------------------------------------------------------
# Arithmetic helpers
# ---------------------------------------------------------------------------

def to_mod(x: Fraction | int) -> int:
    """The rational number x as an element of Z/MOD."""
    x = Fraction(x)
    return x.numerator % MOD * pow(x.denominator, MOD - 2, MOD) % MOD


def p_add(a: list[int], b: list[int]) -> list[int]:
    if len(a) < len(b):
        a, b = b, a
    out = list(a)
    for i, c in enumerate(b):
        out[i] = (out[i] + c) % MOD
    return out


def p_scale(a: list[int], c: int) -> list[int]:
    return [x * c % MOD for x in a]


def p_mul(a: list[int], b: list[int], trunc: int | None = None) -> list[int]:
    """Product of coefficient lists, keeping powers below `trunc` if given."""
    size = len(a) + len(b) - 1
    if trunc is not None:
        size = min(size, trunc)
    out = [0] * size
    for i, x in enumerate(a):
        if x == 0 or i >= size:
            continue
        for j, y in enumerate(b[: size - i]):
            out[i + j] = (out[i + j] + x * y) % MOD
    return out


def p_eval(a: list[int], t: int) -> int:
    acc = 0
    for c in reversed(a):
        acc = (acc * t + c) % MOD
    return acc


def p_taylor(a: list[int], t: int, J: int) -> list[int]:
    """Coefficients of a(t + z) for z^0, ..., z^(J-1)."""
    out = []
    for i in range(J):
        s = 0
        for k in range(i, len(a)):
            s += a[k] * math.comb(k, i) % MOD * pow(t, k - i, MOD)
        out.append(s % MOD)
    return out


def q_mul(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
    out = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def solve_mod(rows: list[list[int]], rhs: list[int]) -> list[int]:
    """Solve an overdetermined but consistent, full-column-rank system mod MOD."""
    ncols = len(rows[0])
    aug = [list(r) + [b] for r, b in zip(rows, rhs)]
    piv_row = 0
    where = [-1] * ncols
    for col in range(ncols):
        sel = next((i for i in range(piv_row, len(aug)) if aug[i][col]), None)
        if sel is None:
            raise ValueError("system is not full column rank")
        aug[piv_row], aug[sel] = aug[sel], aug[piv_row]
        inv = pow(aug[piv_row][col], MOD - 2, MOD)
        aug[piv_row] = [v * inv % MOD for v in aug[piv_row]]
        for i in range(len(aug)):
            if i != piv_row and aug[i][col]:
                f = aug[i][col]
                aug[i] = [(v - f * w) % MOD for v, w in zip(aug[i], aug[piv_row])]
        where[col] = piv_row
        piv_row += 1
    for i in range(piv_row, len(aug)):  # consistency of the extra equations
        if aug[i][-1] % MOD:
            raise ValueError("inconsistent system")
    return [aug[where[c]][-1] for c in range(ncols)]


# ---------------------------------------------------------------------------
# Formulas
# ---------------------------------------------------------------------------

Literal = tuple[int, bool]  # (variable index, True for x_v / False for not x_v)
Clause = tuple[Literal, ...]


def random_bounded_cnf(n: int, rng: random.Random, width: int = 3, max_occ: int = 3) -> list[Clause]:
    """Random CNF with clause width <= 3 and at most 3 occurrences per variable."""
    slots = [v for v in range(n) for _ in range(rng.randint(0, max_occ))]
    rng.shuffle(slots)
    clauses: list[Clause] = []
    cur: list[Literal] = []
    for v in slots:
        if len(cur) == width or any(v == w for w, _ in cur):
            clauses.append(tuple(cur))
            cur = []
        cur.append((v, rng.random() < 0.5))
    if cur:
        clauses.append(tuple(cur))
    return clauses


def brute_force_count(n: int, clauses: list[Clause]) -> int:
    return sum(
        all(any(x[v] == pos for v, pos in c) for c in clauses)
        for x in itertools.product((0, 1), repeat=n)
    )


def clause_poly(lits: Clause, vals: list[list[int]], trunc: int | None) -> list[int]:
    """Phi_e = 1 - prod_v (1 - L_v) evaluated on (truncated) polynomial inputs.

    L_v = X_v for a positive literal and 1 - X_v for a negative one, so the
    factor 1 - L_v is (1 - X_v) or X_v.  On Boolean inputs Phi_e is the
    satisfaction indicator of the clause; at other inputs it is just a
    polynomial."""
    prod = [1]
    for (_, pos), val in zip(lits, vals):
        factor = p_add([1], p_scale(val, MOD - 1)) if pos else val
        prod = p_mul(prod, factor, trunc)
    return p_add([1], p_scale(prod, MOD - 1))


# ---------------------------------------------------------------------------
# Step 2 of the overview: the matrix M_0 = V_0 f(W_0) on ([r] x [r])^Q
# ---------------------------------------------------------------------------

Label = tuple[tuple[int, int], ...]  # Q pairs (a(s), d(s)): (variable group, clause group)


@dataclass(frozen=True)
class Params:
    r: int  # number of groups
    Q: int  # evaluation points t = 1, ..., Q
    R: int  # length of the interpolation interval; replacement degree <= R - 1

    @property
    def interval(self) -> range:
        """R consecutive integers near Q*p, p = (r-1)/(2r), clamped into [0, Q]."""
        p = Fraction(self.r - 1, 2 * self.r)
        a0 = math.floor(self.Q * p - Fraction(self.R - 1, 2))
        a0 = max(0, min(a0, self.Q - self.R + 1))
        return range(a0, a0 + self.R)

    @property
    def D(self) -> int:
        return self.r ** (2 * self.Q)


@lru_cache(maxsize=None)
def eigenvalues(params: Params) -> tuple[Fraction, ...]:
    """g(j) = (-1)^j f(j), j = 0..Q, where deg f <= R-1 and f(i) = (-1)^i on I.

    M_0 acts on the joint eigenvectors of the swaps with exactly j
    antisymmetric factors by the scalar g(j); g = 1 on the interval I."""
    I = list(params.interval)

    def f(j: int) -> Fraction:
        total = Fraction(0)
        for i in I:
            term = Fraction((-1) ** i)
            for k in I:
                if k != i:
                    term *= Fraction(j - k, i - k)
            total += term
        return total

    return tuple((-1) ** j * f(j) for j in range(params.Q + 1))


@lru_cache(maxsize=None)
def m0_coefficient(params: Params, k: int, e: int) -> Fraction:
    """Entry M_0[u, w] when u has k asymmetric pairs and w keeps e of them.

    M_0 = sum_j g(j) P_j, where P_j projects onto the joint eigenspace with j
    antisymmetric factors.  Per asymmetric position the projector entries are
    (1 + y)/2 (pair kept) or (1 - y)/2 (pair swapped), with y marking an
    antisymmetric factor; symmetric positions contribute 1."""
    poly = [Fraction(1)]
    for _ in range(e):
        poly = q_mul(poly, [Fraction(1), Fraction(1)])
    for _ in range(k - e):
        poly = q_mul(poly, [Fraction(1), Fraction(-1)])
    g = eigenvalues(params)
    return sum((g[j] * c for j, c in enumerate(poly)), Fraction(0)) / 2**k


def asym_positions(u: Label) -> list[int]:
    return [s for s, (a, d) in enumerate(u) if a != d]


def m0_row(params: Params, u: Label) -> dict[Label, tuple[Fraction, tuple[int, ...]]]:
    """Nonzero entries of row u of M_0, as w -> (M_0[u, w], E_{u,w}).

    w differs from u by swapping some asymmetric pairs; E_{u,w} is the set of
    points t (1-based) with a_w(t) != d_u(t), i.e. the asymmetric pairs that
    were NOT swapped."""
    asym = asym_positions(u)
    row = {}
    for mask in range(1 << len(asym)):
        keep = tuple(asym[i] for i in range(len(asym)) if mask >> i & 1)
        coeff = m0_coefficient(params, len(asym), len(keep))
        if coeff == 0:
            continue
        w = tuple(pair if (s in keep or pair[0] == pair[1]) else (pair[1], pair[0])
                  for s, pair in enumerate(u))
        row[w] = (coeff, tuple(s + 1 for s in keep))
    return row


def replacement_row(params: Params, u: Label) -> dict[Label, list[Fraction]]:
    """<P_u(T), zeta> = ((I - M_0) zeta)_u + sum_w M_0[u,w] phi_{u,w}(T) zeta_w,

    with phi_{u,w}(T) = prod_{s in E_{u,w}} (1 - T/s).  Equivalently
    P_u(T) = e_u + sum_w M_0[u,w] (phi_{u,w}(T) - 1) e_w.
    Returns w -> coefficient polynomial in T (exact)."""
    row: dict[Label, list[Fraction]] = {u: [Fraction(1)]}
    for w, (coeff, E) in m0_row(params, u).items():
        phi = [Fraction(1)]
        for s in E:
            phi = q_mul(phi, [Fraction(1), Fraction(-1, s)])
        delta = [coeff * c for c in phi]
        delta[0] -= coeff
        if any(delta):
            old = row.get(w, [Fraction(0)])
            size = max(len(old), len(delta))
            row[w] = [(old[i] if i < len(old) else 0) + (delta[i] if i < len(delta) else 0)
                      for i in range(size)]
    return row


def psi_key(u: Label, A: frozenset[int]) -> tuple:
    """Key of the product eigenvector psi^A touching coordinate u.

    Per position: (a, a) -> e_aa; an asymmetric pair {a < b} -> e_ab + e_ba,
    or e_ab - e_ba at positions in A (the antisymmetric choices)."""
    key = []
    for s, (a, d) in enumerate(u):
        lo, hi = min(a, d), max(a, d)
        key.append((lo, hi, -1 if s in A else 1))
    return tuple(key)


def psi_value(key: tuple, w: Label) -> int:
    """Coordinate w of the (unnormalized) eigenvector with the given key."""
    val = 1
    for (lo, hi, sign), (a, d) in zip(key, w):
        if lo == hi:
            if (a, d) != (lo, lo):
                return 0
        elif (a, d) == (lo, hi):
            pass
        elif (a, d) == (hi, lo):
            val *= sign
        else:
            return 0
    return val


def measurement_terms(params: Params, u: Label) -> list[tuple[tuple, Fraction]]:
    """Row u of I - M_0 as a combination of measured eigenvectors:

        ((I - M_0) zeta)_u = sum_A (1 - g(|A|)) psi^A_u / ||psi^A||^2 <psi^A, zeta>

    over A subset of the asymmetric positions of u with |A| outside I.  Returns
    a list of (psi key, coefficient)."""
    g = eigenvalues(params)
    asym = asym_positions(u)
    norm2 = 2 ** len(asym)
    terms = []
    for size in range(len(asym) + 1):
        if size in params.interval:
            continue
        for A in itertools.combinations(asym, size):
            key = psi_key(u, frozenset(A))
            coeff = (1 - g[size]) * psi_value(key, u) / norm2
            if coeff:
                terms.append((key, coeff))
    return terms


# ---------------------------------------------------------------------------
# Step 4: schedules, labels, copies; the replacement forms for a formula
# ---------------------------------------------------------------------------

@dataclass
class Occurrence:
    clause: int
    var: int
    label: Label
    copy: int
    coeffs: dict[int, list[Fraction]] = field(default_factory=dict)  # var -> poly in T


@dataclass
class Construction:
    n: int
    clauses: list[Clause]  # including dummy clauses () for unused variables
    scopes: list[tuple[int, ...]]  # variables read by each clause
    params: Params
    a: list[tuple[int, ...]]  # variable schedules a_v in [r]^Q
    d: list[tuple[int, ...]]  # clause schedules d_e in [r]^Q
    occ: dict[tuple[int, int], Occurrence]
    copies: list[dict[Label, int]]  # copy j: label -> variable stored there

    @property
    def M(self) -> int:
        return len(self.occ)

    @property
    def degree_bound(self) -> int:
        return self.M * (self.params.R - 1)


def build(n: int, clauses: list[Clause], params: Params, rng: random.Random) -> Construction:
    used = {v for c in clauses for v, _ in c}
    all_clauses = list(clauses) + [() for v in range(n) if v not in used]
    scopes = [tuple(v for v, _ in c) for c in clauses] + [(v,) for v in range(n) if v not in used]
    r, Q = params.r, params.Q
    # Any schedules give a correct algorithm; balanced ones (Lemma 3.4 of the
    # paper, by conditional expectations) are what make it fast.
    a = [tuple(rng.randrange(r) for _ in range(Q)) for _ in range(n)]
    d = [tuple(rng.randrange(r) for _ in range(Q)) for _ in range(len(all_clauses))]
    occ: dict[tuple[int, int], Occurrence] = {}
    copies: list[dict[Label, int]] = []
    for e, scope in enumerate(scopes):
        for v in scope:
            label = tuple(zip(a[v], d[e]))
            j = next((j for j, cp in enumerate(copies) if label not in cp), len(copies))
            if j == len(copies):
                copies.append({})
            copies[j][label] = v
            occ[(e, v)] = Occurrence(e, v, label, j)
    for o in occ.values():  # transfer the auxiliary row to the original variables
        for w, poly in replacement_row(params, o.label).items():
            if w in copies[o.copy]:
                var = copies[o.copy][w]
                old = o.coeffs.get(var, [])
                size = max(len(old), len(poly))
                o.coeffs[var] = [(old[i] if i < len(old) else 0) + (poly[i] if i < len(poly) else 0)
                                 for i in range(size)]
    return Construction(n, all_clauses, scopes, params, a, d, occ, copies)


def direct_H(con: Construction) -> list[int]:
    """H(T) = sum_x prod_e Phi_e(<P_{e,v}(T), x>) by brute force over x (mod MOD)."""
    coeffs = {key: {var: [to_mod(c) for c in poly] for var, poly in o.coeffs.items()}
              for key, o in con.occ.items()}
    total = [0]
    for x in itertools.product((0, 1), repeat=con.n):
        prod = [1]
        for e, lits in enumerate(con.clauses):
            if not lits:
                continue  # dummy clause: Phi_e = 1
            vals = []
            for v, _ in lits:
                form = [0]
                for var, poly in coeffs[(e, v)].items():
                    if x[var]:
                        form = p_add(form, poly)
                vals.append(form)
            prod = p_mul(prod, clause_poly(lits, vals, None))
        total = p_add(total, prod)
    return total


# ---------------------------------------------------------------------------
# Step (2)-(3): the design at a point t and the separated sum
# ---------------------------------------------------------------------------

@dataclass
class Design:
    t: int
    groups: list[list[int]]  # S_{t,g}
    clause_group: list[int]  # sigma_e(t)
    local: dict[tuple[int, int], dict[int, int]]  # occurrence -> {var in own group: coeff}
    meas_terms: dict[tuple[int, int], list[tuple[tuple, int]]]  # occurrence -> [(meas id, coeff)]
    meas_forms: dict[tuple, dict[int, dict[int, int]]]  # meas id -> group -> {var: int coeff}

    @property
    def num_measurements(self) -> int:
        return sum(len(by_group) for by_group in self.meas_forms.values())


def design_at(con: Construction, t: int) -> Design:
    params, s = con.params, t - 1
    groups = [[v for v in range(con.n) if con.a[v][s] == g] for g in range(params.r)]
    clause_group = [con.d[e][s] for e in range(len(con.clauses))]
    local: dict[tuple[int, int], dict[int, int]] = {}
    meas_terms: dict[tuple[int, int], list[tuple[tuple, int]]] = {}
    meas_forms: dict[tuple, dict[int, dict[int, int]]] = {}
    for key, o in con.occ.items():
        g = clause_group[o.clause]
        # second term: sum over w with t not in E_{u,w}; these coordinates hold
        # variables of the clause's own group
        loc: dict[int, int] = {}
        for w, (coeff, E) in m0_row(params, o.label).items():
            if t in E or w not in con.copies[o.copy]:
                continue
            var = con.copies[o.copy][w]
            assert con.a[var][s] == g, "design violated: foreign variable in local part"
            phi_t = math.prod((Fraction(1) - Fraction(t, p) for p in E), start=Fraction(1))
            loc[var] = (loc.get(var, 0) + to_mod(coeff * phi_t)) % MOD
        local[key] = loc
        # first term: a combination of the measurements <psi, zeta^(copy)>
        terms = []
        for pkey, coeff in measurement_terms(params, o.label):
            mid = (o.copy, pkey)
            if mid not in meas_forms:
                by_group: dict[int, dict[int, int]] = {}
                for w, var in con.copies[o.copy].items():
                    val = psi_value(pkey, w)
                    if val:
                        grp = by_group.setdefault(con.a[var][s], {})
                        grp[var] = grp.get(var, 0) + val
                meas_forms[mid] = {h: f for h, f in by_group.items() if any(f.values())}
            terms.append((mid, to_mod(coeff)))
        meas_terms[key] = terms
    return Design(t, groups, clause_group, local, meas_terms, meas_forms)


def check_design(con: Construction, des: Design) -> None:
    """The decomposition reproduces the full replacement form at t exactly."""
    for key, o in con.occ.items():
        full = {var: p_eval([to_mod(c) for c in poly], des.t) for var, poly in o.coeffs.items()}
        rebuilt: dict[int, int] = dict(des.local[key])
        for mid, coeff in des.meas_terms[key]:
            for form in des.meas_forms[mid].values():
                for var, c in form.items():
                    rebuilt[var] = (rebuilt.get(var, 0) + coeff * c) % MOD
        for var in set(full) | set(rebuilt):
            assert full.get(var, 0) % MOD == rebuilt.get(var, 0) % MOD, "design mismatch"


def separated_sum(con: Construction, des: Design, ones: frozenset[int] = frozenset(),
                  shifts: dict[tuple[int, int], list[int]] | None = None, J: int = 1) -> list[int]:
    """sum over x (with x_i = 1 for i in `ones`) of prod_e Phi_e(value + shift),
    computed group by group after fixing the measurement tuple y.

    Returns a truncated polynomial in z (length J); with no shifts it is the
    scalar H(t) as a length-1 list."""
    r = len(des.groups)
    mids = sorted(des.meas_forms, key=repr)
    clauses_of = [[e for e in range(len(con.clauses)) if des.clause_group[e] == g and con.clauses[e]]
                  for g in range(r)]
    buckets: list[dict[tuple, list[dict[int, int]]]] = []
    for g in range(r):
        bucket: dict[tuple, list[dict[int, int]]] = {}
        for bits in itertools.product((0, 1), repeat=len(des.groups[g])):
            x = dict(zip(des.groups[g], bits))
            if any(x[v] == 0 for v in ones if v in x):
                continue
            y = tuple(sum(c * x[v] for v, c in des.meas_forms[m].get(g, {}).items()) for m in mids)
            bucket.setdefault(y, []).append(x)
        buckets.append(bucket)
    total = [0] * J
    for ys in itertools.product(*(list(b) for b in buckets)):
        y_total = {m: sum(y[i] for y in ys) for i, m in enumerate(mids)}
        prod = [1]
        for g in range(r):
            B = [0] * J
            for x in buckets[g][ys[g]]:
                A = [1]
                for e in clauses_of[g]:
                    vals = []
                    for v, _ in con.clauses[e]:
                        key = (e, v)
                        val = sum(c * x[var] for var, c in des.local[key].items())
                        val += sum(c * y_total[m] for m, c in des.meas_terms[key])
                        poly = [val % MOD]
                        if shifts is not None:
                            poly = p_add(poly, shifts[key])
                        vals.append(poly)
                    A = p_mul(A, clause_poly(con.clauses[e], vals, J), J)
                B = p_add(B, A)
            prod = p_mul(prod, B, J)
        total = p_add(total, prod)
    return (total + [0] * J)[:J]


# ---------------------------------------------------------------------------
# Step (4)-(5): Taylor coefficients by inclusion-exclusion, Hermite recovery
# ---------------------------------------------------------------------------

def taylor_by_inclusion_exclusion(con: Construction, des: Design, J: int) -> list[int]:
    """H(t+z) mod z^J = sum_{|E|<=q} sum_{U subset E} (-1)^{|E|-|U|} Z_{t,E,U}(z)."""
    t, q = des.t, J - 1
    delta = {}  # occurrence -> var -> Delta p(z) = p(t+z) - p(t), truncated
    for key, o in con.occ.items():
        dv = {}
        for var, poly in o.coeffs.items():
            tay = p_taylor([to_mod(c) for c in poly], t, J)
            tay[0] = 0
            dv[var] = tay
        delta[key] = dv
    total = [0] * J
    for size in range(min(q, con.n) + 1):
        for E in itertools.combinations(range(con.n), size):
            for usize in range(size + 1):
                sign = 1 if (size - usize) % 2 == 0 else MOD - 1
                for U in itertools.combinations(E, usize):
                    shifts = {}
                    for key in con.occ:
                        sh = [0] * J
                        for var in U:
                            if var in delta[key]:
                                sh = p_add(sh, delta[key][var])
                        shifts[key] = sh
                    Z = separated_sum(con, des, frozenset(E), shifts, J)
                    total = p_add(total, p_scale(Z, sign))
    return total


def hermite_recover(taylor: dict[int, list[int]], degree: int) -> list[int]:
    """Coefficients of the unique polynomial of degree <= `degree` with the
    given Taylor coefficients (z^0..z^{J-1} of H(t+z)) at each point t."""
    rows, rhs = [], []
    for t, coeffs in taylor.items():
        for i, h in enumerate(coeffs):
            rows.append([math.comb(k, i) * pow(t, k - i, MOD) % MOD if k >= i else 0
                         for k in range(degree + 1)])
            rhs.append(h)
    return solve_mod(rows, rhs)


def count_by_interpolation(con: Construction, verbose: bool = False) -> int:
    """The whole bounded-occurrence algorithm: designs at t = 1..Q, Taylor data
    by inclusion-exclusion over separated sums, Hermite interpolation."""
    Q, dbound = con.params.Q, con.degree_bound
    q = dbound // Q
    J = q + 1
    assert Q * J > dbound
    data = {}
    for t in range(1, Q + 1):
        des = design_at(con, t)
        data[t] = taylor_by_inclusion_exclusion(con, des, J)
        if verbose:
            print(f"    t={t}: groups {[len(g) for g in des.groups]}, "
                  f"{des.num_measurements} group measurements, J={J}")
    return hermite_recover(data, dbound)[0]


# ---------------------------------------------------------------------------
# Section 5: the Beigel-Tarui parity polynomial (Lemma 5.1) and truncation
# ---------------------------------------------------------------------------

def beigel_tarui(ell: int) -> list[int]:
    """p_ell(Y) = (1 - Y)^ell * sum_{j<ell} C(ell+j-1, j) Y^j (integer coefficients)."""
    left = [1]
    for _ in range(ell):
        left = [a - b for a, b in zip(left + [0], [0] + left)]
    right = [math.comb(ell + j - 1, j) for j in range(ell)]
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return out


def h_expansion(poly: list[int]) -> list[tuple[int, int]]:
    """Write poly = sum_j e_j(Y) h(Y)^j, h = Y^2 - Y, deg e_j <= 1.
    Returns [(e_j(0), e_j'(0))] (constant and linear coefficients)."""
    rest = list(poly)
    out = []
    while any(rest):
        while len(rest) < 2:
            rest.append(0)
        quot = [0] * max(len(rest) - 2, 0)
        cur = list(rest)
        for k in range(len(cur) - 1, 1, -1):  # divide by Y^2 - Y
            c = cur[k]
            if c:
                quot[k - 2] += c
                cur[k] -= c
                cur[k - 1] += c
        out.append((cur[0], cur[1]))
        rest = quot
    return out


def check_beigel_tarui(max_ell: int = 9) -> None:
    for ell in range(1, max_ell + 1):
        p = beigel_tarui(ell)
        for y in range(-80, 81):
            val = sum(c * y**k for k, c in enumerate(p))
            assert val % 2**ell == (1 if y % 2 == 0 else 0), (ell, y)
        exp = h_expansion(p)
        assert len(exp) <= ell
        for y in range(-20, 21):
            h = y * y - y
            assert sum((c0 + c1 * y) * h**j for j, (c0, c1) in enumerate(exp)) == \
                sum(c * y**k for k, c in enumerate(p))
    assert beigel_tarui(2) == [1, 0, -3, 2]  # p_2(Y) = 1 - 3Y^2 + 2Y^3
    assert h_expansion(beigel_tarui(2)) == [(1, -1), (-1, 2)]  # (1 - Y) + (2Y - 1) h(Y)
    # Lemma 5.2: truncating the product across all equations at V^ell keeps
    # the evenness indicator modulo 2^ell.
    rng = random.Random(7)
    for ell in range(1, 7):
        exp = h_expansion(beigel_tarui(ell))
        for _ in range(200):
            ys = [rng.randint(-30, 30) for _ in range(rng.randint(1, 6))]
            prod = [1]  # polynomial in V, truncated at V^ell
            for y in ys:
                h = y * y - y
                B = [(c0 + c1 * y) * h**j for j, (c0, c1) in enumerate(exp)][:ell]
                nxt = [0] * ell
                for i, a in enumerate(prod):
                    for j, b in enumerate(B):
                        if i + j < ell:
                            nxt[i + j] += a * b
                prod = nxt
            want = 1 if all(y % 2 == 0 for y in ys) else 0
            assert sum(prod) % 2**ell == want


# ---------------------------------------------------------------------------
# Matrix facts (Section 2, Step 2), checked exactly
# ---------------------------------------------------------------------------

def all_labels(params: Params):
    pairs = [(a, d) for a in range(params.r) for d in range(params.r)]
    return itertools.product(pairs, repeat=params.Q)


def psi_support(key: tuple):
    """All coordinates where the eigenvector with this key is nonzero."""
    return itertools.product(*([(lo, lo)] if lo == hi else [(lo, hi), (hi, lo)]
                               for lo, hi, _ in key))


def check_matrix(params: Params, sample: int = 400) -> dict:
    """Check, exactly over Q:
      * M_0 is symmetric
      * M_0[u,w] != 0  =>  |E_{u,w}| <= R - 1           (restricted support)
      * M_0 psi = g(j) psi for the product eigenvectors  (spectrum; all of
        them when D is small, a random sample otherwise)
      * g(j) = 1 on the interval I                        (fixes most directions)
    and return a few statistics, including the number of measured directions
    (eigenvectors with j outside I) and rank(I - M_0) (those with g(j) != 1)."""
    g = eigenvalues(params)
    assert all(g[j] == 1 for j in params.interval)
    labels = list(all_labels(params))
    rows = {u: m0_row(params, u) for u in labels}
    for u, row in rows.items():
        for w, (c, _) in row.items():
            assert rows[w][u][0] == c, "M_0 is not symmetric"
    max_E = max((len(E) for row in rows.values() for _, E in row.values()), default=0)
    assert max_E <= params.R - 1, "support condition violated"
    rng = random.Random(1)
    starts = labels if len(labels) <= sample else rng.sample(labels, sample)
    keys = {}
    for u in starts:
        asym = asym_positions(u)
        for size in range(len(asym) + 1):
            for A in itertools.combinations(asym, size):
                keys[psi_key(u, frozenset(A))] = size
    for key, size in keys.items():
        image: dict[Label, Fraction] = {}
        for w in psi_support(key):  # M_0 psi, using the symmetry of M_0
            pv = psi_value(key, w)
            for x, (c, _) in rows[w].items():
                image[x] = image.get(x, Fraction(0)) + c * pv
        for x in set(image) | set(psi_support(key)):
            assert image.get(x, 0) == g[size] * psi_value(key, x), "eigenvector check failed"
    sym = params.r * (params.r + 1) // 2
    anti = params.r * (params.r - 1) // 2
    dims = [math.comb(params.Q, j) * anti**j * sym ** (params.Q - j) for j in range(params.Q + 1)]
    assert sum(dims) == params.D
    nnz = sum(len(row) for row in rows.values())
    return {"D": params.D, "interval": (params.interval.start, params.interval.stop - 1),
            "eigenvalues": [str(v) for v in g],
            "measured": sum(dim for j, dim in enumerate(dims) if j not in params.interval),
            "rank_I_minus_M0": sum(dim for j, dim in enumerate(dims) if g[j] != 1),
            "eigenvectors_checked": len(keys),
            "max_E": max_E, "avg_row_nnz": nnz / len(labels)}


# ---------------------------------------------------------------------------
# How large must n be for the paper's explicit parameters?
# ---------------------------------------------------------------------------

def overview_parameters(lam: int) -> dict:
    """The explicit parameter choices (2.19) of the overview, for lambda = ceil(log2 n)."""
    nu = (lam - 1).bit_length()  # ceil(log2 lambda)
    r = math.isqrt(lam // nu**4)  # floor(sqrt(lambda) / nu^2)
    Q = lam // (128 * nu)
    R = 4 * (math.isqrt(lam - 1) + 1)  # 4 * ceil(sqrt(lambda))
    return {"lambda": lam, "nu": nu, "r": r, "Q": Q, "R": R}


def overview_engaged(lam: int) -> bool:
    p = overview_parameters(lam)
    return p["r"] >= 2 and p["R"] >= 32 and 6 * p["R"] <= p["Q"]


def galactic_threshold() -> int:
    """Smallest lambda = ceil(log2 n) from which on r >= 2, R >= 32 and
    6R <= Q all hold for the overview's explicit choices; smaller inputs are
    handled by exhaustive search.  nu is constant on (2^(nu-1), 2^nu], and the
    conditions are monotone in lambda there, so search block by block."""
    for nu in range(2, 64):
        lo, hi = 2 ** (nu - 1) + 1, 2**nu
        if not overview_engaged(hi):
            continue
        while lo < hi:
            mid = (lo + hi) // 2
            if overview_engaged(mid):
                hi = mid
            else:
                lo = mid + 1
        # it must also stay engaged in every later block
        assert all(overview_engaged(2 ** (k - 1) + 1) for k in range(nu + 1, 64))
        return lo
    raise RuntimeError("not reached")


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def run_checks(quick: bool) -> None:
    rng = random.Random(2026)
    t0 = time.time()

    print("[matrix] M_0 = V_0 f(W_0): support, spectrum, measured directions")
    for params in (Params(2, 3, 2), Params(3, 2, 2), Params(2, 4, 3), Params(3, 4, 3)):
        stats = check_matrix(params)
        print(f"    r={params.r} Q={params.Q} R={params.R}: D={stats['D']}, I={stats['interval']}, "
              f"g(j)={stats['eigenvalues']}, measured={stats['measured']} "
              f"(rank(I-M0)={stats['rank_I_minus_M0']}), max|E_uw|={stats['max_E']}, "
              f"avg nnz/row={stats['avg_row_nnz']:.2f}, eigenvectors checked={stats['eigenvectors_checked']}")

    print("[parity] Beigel-Tarui polynomial and the total-order truncation")
    check_beigel_tarui()
    print("    p_ell(y) = [y even] mod 2^ell for ell <= 9; p_2 = (1-Y) + (2Y-1)h(Y); Lemma 5.2 ok")

    print("[identities] restore / design / separation / Hermite on random formulas")
    cases = [(Params(2, 3, 2), 7), (Params(3, 4, 3), 7), (Params(2, 4, 3), 8)]
    if quick:
        cases = cases[:2]
    for params, n in cases:
        for trial in range(2 if quick else 4):
            clauses = random_bounded_cnf(n, rng)
            con = build(n, clauses, params, rng)
            truth = brute_force_count(n, clauses)
            H = direct_H(con)
            assert len(H) - 1 <= con.degree_bound
            assert p_eval(H, 0) == truth, "(1) restore failed"
            for t in range(1, params.Q + 1):
                des = design_at(con, t)
                check_design(con, des)
                assert separated_sum(con, des)[0] == p_eval(H, t), "(3) separation failed"
            J = con.degree_bound // params.Q + 1
            data = {t: p_taylor(H, t, J) for t in range(1, params.Q + 1)}
            assert hermite_recover(data, con.degree_bound)[0] == truth, "(5) Hermite failed"
            print(f"    r={params.r} Q={params.Q} R={params.R} n={n}: #F={truth:3d}  "
                  f"M={con.M}, deg H={len(H) - 1} <= {con.degree_bound}, copies={len(con.copies)}  ok")

    print("[end-to-end] Taylor data by inclusion-exclusion over separated sums + Hermite")
    e2e = [(Params(2, 3, 2), 5, 1)] if quick else [
        (Params(2, 3, 2), 7, 3), (Params(2, 4, 3), 7, 3), (Params(3, 4, 3), 7, 3), (Params(2, 3, 2), 8, 2)]
    for params, n, trials in e2e:
        for _ in range(trials):
            clauses = random_bounded_cnf(n, rng)
            con = build(n, clauses, params, rng)
            truth = brute_force_count(n, clauses)
            got = count_by_interpolation(con, verbose=quick)
            assert got == truth, (got, truth)
            J = con.degree_bound // params.Q + 1
            print(f"    r={params.r} Q={params.Q} R={params.R} n={n}: algorithm={got:3d}, "
                  f"brute force={truth:3d}  (J={J} Taylor coefficients per point)  ok")

    lam = galactic_threshold()
    p = overview_parameters(lam)
    print(f"[scale] the overview's explicit parameters engage once log2(n) >= {lam:,} "
          f"(r={p['r']}, Q={p['Q']:,}, R={p['R']:,}); smaller n fall back to exhaustive search")
    print(f"all checks passed in {time.time() - t0:.1f}s")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--quick", action="store_true", help="smaller instances")
    args = ap.parse_args(argv)
    run_checks(args.quick)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
