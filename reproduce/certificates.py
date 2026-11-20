"""Section 6: false acceptance and false rejection on a programmatically verifiable subfamily.

600 equality-constrained strongly convex quadratic task families, all in exact rational
arithmetic (fractions.Fraction). Each family yields six submissions:

  valid    L   Lagrange-multiplier proof: (x*, nu*, v*)
  valid    E   equality-elimination proof: x* = x_p + Z y*, no multiplier, value v*
  invalid  D1  infeasible point (A x != b) reported with the exact optimal value v*
  invalid  D2  feasible point off the optimum (stationarity fails along ker A), reporting v*
  invalid  D3  the optimal x* with a multiplier that fails H x + c + A^T nu = 0, reporting v*
  invalid  D4  the optimal x* and nu* with a wrong objective value

Three deterministic acceptance protocols are compared:

  final_answer    accept iff the reported value equals v*
  reference_path  accept iff the submission reproduces the reference Lagrange route exactly
  certificate     check feasibility, verified curvature on ker A, zero projected residual,
                  the claimed value against f(x), and full stationarity for any claimed multiplier

The script also checks the projected-residual bound 0 <= f(x) - v* <= ||P r||^2 / (2 mu)
at one feasible perturbation per family.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction as Q

DIM, CONS, FAMILIES, MU = 4, 2, 600, Q(1)


# ------------------------------------------------------------------ exact linear algebra


def mat(rows):
    return [[Q(v) for v in r] for r in rows]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def mv(a, x):
    return [sum(ai * xi for ai, xi in zip(row, x)) for row in a]


def tr(a):
    return [list(r) for r in zip(*a)]


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def solve(a, rhs):
    """Exact Gauss-Jordan solve of a nonsingular system."""
    n = len(a)
    m = [row[:] + [r] for row, r in zip(a, rhs)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [v / piv for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [v - f * w for v, w in zip(m[r], m[c])]
    return [row[-1] for row in m]


def rank(a):
    m = [row[:] for row in a]
    r = 0
    for c in range(len(m[0])):
        p = next((i for i in range(r, len(m)) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        for i in range(len(m)):
            if i != r and m[i][c] != 0:
                f = m[i][c] / m[r][c]
                m[i] = [v - f * w for v, w in zip(m[i], m[r])]
        r += 1
    return r


def null_basis(a):
    """Exact basis of ker A from the reduced row echelon form (columns returned as a d x k matrix)."""
    m = [row[:] for row in a]
    rows, cols = len(m), len(m[0])
    pivots, r = [], 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        m[r] = [v / m[r][c] for v in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [v - f * w for v, w in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for fcol in free:
        v = [Q(0)] * cols
        v[fcol] = Q(1)
        for i, pc in enumerate(pivots):
            v[pc] = -m[i][fcol]
        basis.append(v)
    return tr(basis)


def positive_definite(a):
    """Sylvester's criterion, exactly."""

    def det(m):
        n = len(m)
        if n == 1:
            return m[0][0]
        total = Q(0)
        for j in range(n):
            minor = [row[:j] + row[j + 1:] for row in m[1:]]
            total += (-1) ** j * m[0][j] * det(minor)
        return total

    return all(det([row[:k] for row in a[:k]]) > 0 for k in range(1, len(a) + 1))


# ------------------------------------------------------------------ task families


@dataclass
class Family:
    H: list
    c: list
    A: list
    b: list
    x_star: list
    nu_star: list
    v_star: Q
    Z: list
    P: list  # orthogonal projector onto ker A

    def f(self, x):
        return dot(x, mv(self.H, x)) / 2 + dot(self.c, x)


def make_family(rng: random.Random) -> Family:
    while True:
        A = mat([[rng.randint(-3, 3) for _ in range(DIM)] for _ in range(CONS)])
        if rank(A) == CONS:
            break
    M = mat([[rng.randint(-2, 2) for _ in range(DIM)] for _ in range(DIM)])
    H = [[v + (MU if i == j else 0) for j, v in enumerate(row)] for i, row in enumerate(mul(tr(M), M))]
    c = [Q(rng.randint(-5, 5)) for _ in range(DIM)]
    x0 = [Q(rng.randint(-3, 3)) for _ in range(DIM)]
    b = mv(A, x0)
    # KKT system [[H, A^T], [A, 0]] [x; nu] = [-c; b]
    At = tr(A)
    kkt = [H[i] + At[i] for i in range(DIM)] + [A[r] + [Q(0)] * CONS for r in range(CONS)]
    sol = solve(kkt, [-ci for ci in c] + b)
    x_star, nu_star = sol[:DIM], sol[DIM:]
    AAt_inv_A = [solve(mul(A, At), col) for col in tr(A)]  # columns of (A A^T)^-1 A
    AtAAtA = mul(At, tr(AAt_inv_A))
    P = [[(Q(1) if i == j else Q(0)) - AtAAtA[i][j] for j in range(DIM)] for i in range(DIM)]
    fam = Family(H, c, A, b, x_star, nu_star, Q(0), null_basis(A), P)
    fam.v_star = fam.f(x_star)
    return fam


# ------------------------------------------------------------------ submissions


def submissions(fam: Family, rng: random.Random):
    """The six submissions for one family. The elimination route never touches the KKT
    solution: it starts from a particular solution of A x = b (free coordinates zero) and
    solves the reduced system Z^T H Z y = -Z^T (H x_p + c)."""
    zt = tr(fam.Z)
    x_p = particular_solution(fam.A, fam.b)
    reduced_h = mul(mul(zt, fam.H), fam.Z)
    grad_p = [hx + ci for hx, ci in zip(mv(fam.H, x_p), fam.c)]
    y = solve(reduced_h, [-v for v in mv(zt, grad_p)])
    x_elim = [xp + dz for xp, dz in zip(x_p, mv(fam.Z, y))]
    assert x_elim == fam.x_star, "elimination and KKT routes must agree on the unique optimum"

    off = [row[0] for row in fam.Z]                               # first ker-A direction
    row_dir = fam.A[0]                                            # a direction with A d != 0
    bump = Q(rng.randint(1, 3))
    return [
        ("L", True, {"route": "lagrange", "x": fam.x_star, "nu": fam.nu_star, "value": fam.v_star}),
        ("E", True, {"route": "elimination", "x": x_elim, "Z": fam.Z, "y": y, "value": fam.v_star}),
        ("D1", False, {"route": "lagrange", "x": [x + bump * d for x, d in zip(fam.x_star, row_dir)],
                       "nu": fam.nu_star, "value": fam.v_star}),
        ("D2", False, {"route": "elimination", "x": [x + bump * d for x, d in zip(fam.x_star, off)],
                       "Z": fam.Z, "y": y, "value": fam.v_star}),
        ("D3", False, {"route": "lagrange", "x": fam.x_star,
                       "nu": [fam.nu_star[0] + bump] + fam.nu_star[1:], "value": fam.v_star}),
        ("D4", False, {"route": "lagrange", "x": fam.x_star, "nu": fam.nu_star, "value": fam.v_star + bump}),
    ]


def particular_solution(A, b):
    """Solve A x = b exactly with the non-pivot coordinates set to zero."""
    m = [row[:] + [bi] for row, bi in zip(A, b)]
    rows, cols = len(m), len(A[0])
    pivots, r = [], 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        m[r] = [v / m[r][c] for v in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [v - f * w for v, w in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
    x = [Q(0)] * cols
    for i, pc in enumerate(pivots):
        x[pc] = m[i][-1]
    return x


# ------------------------------------------------------------------ acceptance protocols


def final_answer(fam: Family, sub: dict) -> bool:
    return sub["value"] == fam.v_star


def reference_path(fam: Family, sub: dict) -> bool:
    return (sub["route"] == "lagrange" and sub["x"] == fam.x_star
            and sub.get("nu") == fam.nu_star and sub["value"] == fam.v_star)


def certificate(fam: Family, sub: dict) -> bool:
    x = sub["x"]
    if mv(fam.A, x) != fam.b:                                    # feasibility
        return False
    if not positive_definite(mul(mul(tr(fam.Z), fam.H), fam.Z)):  # verified curvature on ker A
        return False
    r = [hx + ci for hx, ci in zip(mv(fam.H, x), fam.c)]
    if any(v != 0 for v in mv(fam.P, r)):                        # projected stationarity residual
        return False
    if sub["value"] != fam.f(x):                                 # claimed objective value
        return False
    if "nu" in sub:                                              # a claimed multiplier must be a witness
        full = [ri + ai for ri, ai in zip(r, mv(tr(fam.A), sub["nu"]))]
        if any(v != 0 for v in full):
            return False
    return True


PROTOCOLS = {"final_answer": final_answer, "reference_path": reference_path, "certificate": certificate}


def residual_bound_holds(fam: Family, rng: random.Random) -> bool:
    """0 <= f(x) - v* <= ||P r||^2 / (2 mu) at a random feasible perturbation x = x* + Z d."""
    d = [Q(rng.randint(-4, 4), rng.randint(1, 3)) for _ in range(len(fam.Z[0]))]
    x = [xs + dz for xs, dz in zip(fam.x_star, mv(fam.Z, d))]
    r = [hx + ci for hx, ci in zip(mv(fam.H, x), fam.c)]
    pr = mv(fam.P, r)
    gap = fam.f(x) - fam.v_star
    return Q(0) <= gap <= dot(pr, pr) / (2 * MU)


def run(seed: int = 600) -> dict:
    rng = random.Random(seed)
    counts = {p: {"valid_accepted": 0, "invalid_accepted": 0} for p in PROTOCOLS}
    by_class = {p: {} for p in PROTOCOLS}
    n_valid = n_invalid = bound_ok = 0
    reports_vstar_invalid = 0
    for _ in range(FAMILIES):
        fam = make_family(rng)
        for label, valid, sub in submissions(fam, rng):
            n_valid += valid
            n_invalid += not valid
            if not valid and sub["value"] == fam.v_star:
                reports_vstar_invalid += 1
            for name, proto in PROTOCOLS.items():
                ok = proto(fam, sub)
                key = "valid_accepted" if valid else "invalid_accepted"
                counts[name][key] += ok
                by_class[name][label] = by_class[name].get(label, 0) + ok
        bound_ok += residual_bound_holds(fam, rng)
    table = {}
    for name, c in counts.items():
        accepted = c["valid_accepted"] + c["invalid_accepted"]
        table[name] = {
            "false_acceptance_percent": 100 * c["invalid_accepted"] / n_invalid,
            "false_rejection_percent": 100 * (n_valid - c["valid_accepted"]) / n_valid,
            "valid_share_of_accepted_percent": 100 * c["valid_accepted"] / accepted if accepted else float("nan"),
            "invalid_accepted": c["invalid_accepted"],
            "valid_rejected": n_valid - c["valid_accepted"],
            "accepted_by_class": by_class[name],
        }
    return {"families": FAMILIES, "submissions": n_valid + n_invalid, "valid": n_valid, "invalid": n_invalid,
            "invalid_reporting_v_star": reports_vstar_invalid, "residual_bound_checks_passed": bound_ok,
            "protocols": table}


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, default=str))
