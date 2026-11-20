"""Sections 1, 4, 5 and 7: how grading error moves scores, rankings and training targets.

1. Observed score s = alpha + (1 - alpha - beta) theta, and the ranking reversal example.
2. Tolerance propagation a*delta + 2*eps under a verified bijection, with a tightness example.
3. Process-reward target under noisy grading: p_tilde = alpha + (1 - alpha - beta) p, and the
   expected binary-cross-entropy gradient shift p - p_tilde, checked by direct sampling.
4. Class-conditional correction: unbiased, variance inflated by 1 / (1 - alpha - beta)^2.
5. Effective sample size of clustered task variants, and the certificate break-even volume.
"""

from __future__ import annotations

import math
import random


def observed_score(theta, alpha, beta):
    return alpha + (1 - alpha - beta) * theta


def ranking_example():
    a = observed_score(0.72, 0.04, 0.0)
    b = observed_score(0.64, 0.36, 0.0)
    return {"s_A": a, "s_B": b, "weaker_model_ranks_first": b > a}


def tolerance_propagation(trials=20_000, seed=8):
    """Random finite problems with a verified bijection Phi and |J'(Phi u) - a J(u) - b| <= eps."""
    rng = random.Random(seed)
    for _ in range(trials):
        n = rng.randint(2, 30)
        a, b = rng.uniform(0.1, 5), rng.uniform(-10, 10)
        eps, delta = rng.uniform(0, 1), rng.uniform(0, 2)
        J = [rng.uniform(-5, 5) for _ in range(n)]
        Jp = [a * j + b + rng.uniform(-eps, eps) for j in J]   # J'(Phi(u)) for each u
        v, vp = min(J), min(Jp)
        if not (a * v + b - eps - 1e-12 <= vp <= a * v + b + eps + 1e-12):
            return False
        for j, jp in zip(J, Jp):
            if j - v <= delta and jp - vp > a * delta + 2 * eps + 1e-12:
                return False
    return True


def tolerance_tight_example(a=2.0, b=1.0, eps=0.1, delta=0.5, v=0.0):
    """Two feasible points where the bound a*delta + 2*eps is attained exactly."""
    J = [v, v + delta]
    Jp = [a * J[0] + b - eps, a * J[1] + b + eps]
    gap = Jp[1] - min(Jp)
    return {"transformed_gap": gap, "bound": a * delta + 2 * eps}


def prm_target_shift(p=0.7, alpha=0.2, beta=0.1, logit=0.3, draws=1_000_000, seed=9):
    rng = random.Random(seed)
    sig = 1 / (1 + math.exp(-logit))
    diff = 0.0
    for _ in range(draws):
        z = rng.random() < p
        if z:
            v = rng.random() >= beta     # false rejection with probability beta
        else:
            v = rng.random() < alpha     # false acceptance with probability alpha
        diff += (sig - v) - (sig - z)
    p_tilde = alpha + (1 - alpha - beta) * p
    return {"p_tilde": p_tilde, "expected_shift": p - p_tilde, "mc_shift": diff / draws}


def noise_correction(theta=0.6, alpha=0.15, beta=0.1, n=400, reps=40_000, seed=10):
    rng = random.Random(seed)
    s = observed_score(theta, alpha, beta)
    ests = []
    for _ in range(reps):
        vbar = sum(rng.random() < s for _ in range(n)) / n
        ests.append((vbar - alpha) / (1 - alpha - beta))
    mean = sum(ests) / reps
    var = sum((e - mean) ** 2 for e in ests) / (reps - 1)
    var_vbar = s * (1 - s) / n
    return {"mean": mean, "theta": theta, "variance_ratio": var / var_vbar,
            "predicted_ratio": 1 / (1 - alpha - beta) ** 2}


def effective_sample_size(families=50, variants=8, rho_w=0.6):
    return families * variants / (1 + (variants - 1) * rho_w)


def break_even_volume(C0, c_e, c_v, u):
    """Smallest volume above which certificate checking is cheaper than full expert review."""
    margin = (1 - u) * c_e - c_v
    return math.inf if margin <= 0 else C0 / margin


def break_even_consistent(trials=10_000, seed=12):
    rng = random.Random(seed)
    for _ in range(trials):
        C0, c_e, c_v, u = rng.uniform(1, 1e5), rng.uniform(1, 100), rng.uniform(0, 10), rng.uniform(0, 0.9)
        n_star = break_even_volume(C0, c_e, c_v, u)
        if math.isinf(n_star):
            continue
        for n in (0.9 * n_star, 1.1 * n_star):
            cheaper = C0 + n * (c_v + u * c_e) < n * c_e
            if cheaper != (n > n_star):
                return False
    return True


if __name__ == "__main__":
    import json

    print(json.dumps({"ranking": ranking_example(), "tolerance": tolerance_propagation(),
                      "tight": tolerance_tight_example(), "prm": prm_target_shift(draws=200_000),
                      "correction": noise_correction(reps=5_000), "n_eff": effective_sample_size(),
                      "break_even": break_even_consistent()}, indent=2))
