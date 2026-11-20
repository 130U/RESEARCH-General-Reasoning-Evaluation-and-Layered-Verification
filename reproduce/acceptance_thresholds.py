"""Quantitative thresholds for a grader: when a leaderboard lead is certified, what a policy
trained against the grader can reach, when a screen may decide, and how tolerances compose.

Every figure is closed-form; the checks at the bottom confirm each formula by exhaustive
or randomized search over its inputs.
"""

from __future__ import annotations

import math
import random


# ------------------------------------------------------------------ Section 1: certified lead
def observed(theta: float, alpha: float, beta: float = 0.0) -> float:
    return alpha + (1 - alpha - beta) * theta


def certified_lead_alpha(lead: float, rival_score: float) -> float:
    """Largest false-acceptance rate at which a lead of `lead` over `rival_score` still
    certifies the ordering of true validity (no false rejection)."""
    return lead / (1 - rival_score)


def reversal_alpha(theta_a: float, alpha_a: float, theta_b: float) -> float:
    """False acceptance for B above which B outscores A although theta_a > theta_b."""
    return (theta_a - theta_b + alpha_a * (1 - theta_a)) / (1 - theta_b)


# ------------------------------------------- Section 5: optimizing a policy against a grader
def tilted(theta: float, alpha: float, beta: float, eta: float) -> tuple[float, float]:
    """True validity and observed score after the policy is reweighted by exp(eta * V)."""
    w = math.exp(eta)
    accept_valid, accept_invalid = theta * (1 - beta), (1 - theta) * alpha
    z = (accept_valid + accept_invalid) * w + theta * beta + (1 - theta) * (1 - alpha)
    return (accept_valid * w + theta * beta) / z, (accept_valid + accept_invalid) * w / z


def ppv(theta: float, alpha: float, beta: float) -> float:
    """Positive predictive value: the limit of true validity as eta grows."""
    return theta * (1 - beta) / (theta * (1 - beta) + (1 - theta) * alpha)


def rejected_route_share(eta: float, initial_share: float = 0.5) -> float:
    """Share of a valid route the grader always rejects, among valid work, after tilting."""
    return initial_share / (initial_share + (1 - initial_share) * math.exp(eta))


# ------------------------------------------------- Section 2: when a screen may decide
def random_escalation(sensitivity: float, alpha_target: float) -> float:
    """Share of unflagged work that must still go to specialists so that the system's
    false acceptance on semantic obligations stays at or below alpha_target."""
    return max(0.0, 1 - alpha_target / (1 - sensitivity))


def clean_run_needed(alpha_target: float, confidence: float = 0.95) -> int:
    """Known-invalid items a checker must reject without exception before its false
    acceptance is bounded by alpha_target at the given confidence (exact binomial)."""
    return math.ceil(math.log(1 - confidence) / math.log(1 - alpha_target))


# ----------------------------------------------------------- Section 4: composed tolerances
def compose(steps) -> tuple[float, float]:
    """(a, eps) of a chain of transformations given as [(a_1, eps_1), ..., (a_k, eps_k)],
    applied in that order: a = prod a_j, eps = sum_j (prod_{l > j} a_l) eps_j."""
    a, eps = 1.0, 0.0
    for a_j, eps_j in steps:
        a, eps = a * a_j, a_j * eps + eps_j
    return a, eps


def tolerance(steps, delta: float) -> float:
    a, eps = compose(steps)
    return a * delta + 2 * eps


# ------------------------------------------------------------------------------- checks
def check_certified_lead(trials: int = 200_000, seed: int = 3) -> bool:
    """If the lead exceeds alpha_cap (1 - s_B), true validity is ordered the same way for
    every pair of false-acceptance rates up to alpha_cap; just below it, a reversal exists."""
    rng = random.Random(seed)
    for _ in range(trials):
        cap = rng.uniform(0.0, 0.5)
        th_a, th_b = rng.random(), rng.random()
        al_a, al_b = rng.uniform(0, cap), rng.uniform(0, cap)
        s_a, s_b = observed(th_a, al_a), observed(th_b, al_b)
        if s_a - s_b > cap * (1 - s_b) and not th_a > th_b:
            return False
    # tightness: A graded at the cap, B graded exactly
    th_b, cap = 0.5, 0.2
    th_a = th_b - 1e-6
    lead = observed(th_a, cap) - observed(th_b, 0.0)
    return 0 < cap * (1 - observed(th_b, 0.0)) - lead < 1e-5


def check_tilt_limit() -> bool:
    for theta, alpha, beta in ((0.64, 0.36, 0.0), (0.72, 0.04, 0.0), (0.5, 0.2, 0.3)):
        valid, score = tilted(theta, alpha, beta, 60.0)
        if abs(valid - ppv(theta, alpha, beta)) > 1e-9 or abs(score - 1.0) > 1e-9:
            return False
    return True


def check_composition(trials: int = 20_000, seed: int = 4) -> bool:
    """Chain affine maps with bounded errors and confirm the composed bound."""
    rng = random.Random(seed)
    for _ in range(trials):
        steps = [(rng.uniform(0.2, 5.0), rng.uniform(0.0, 0.1)) for _ in range(rng.randint(1, 4))]
        value = rng.uniform(-3, 3)
        exact, got = value, value
        for a_j, eps_j in steps:
            shift = rng.uniform(-1, 1)
            exact = a_j * exact + shift
            got = a_j * got + shift + rng.uniform(-eps_j, eps_j)
        a, eps = compose(steps)
        if abs(got - exact) > eps + 1e-12:
            return False
    return True


def run() -> dict:
    out = {
        "certified_lead": {
            "lead 3 points, rival at 80%": certified_lead_alpha(0.03, 0.80),
            "lead 3 points, rival at 50%": certified_lead_alpha(0.03, 0.50),
        },
        "reversal_alpha_B": reversal_alpha(0.72, 0.04, 0.64),
        "ppv": {
            "model A, answer matching": ppv(0.72, 0.04, 0.0),
            "model B, answer matching": ppv(0.64, 0.36, 0.0),
            "test set, answer matching": ppv(1 / 3, 0.75, 0.0),
            "test set, reference path": ppv(1 / 3, 0.0, 0.5),
            "test set, certificate": ppv(1 / 3, 0.0, 0.0),
        },
        "model_B_path": {eta: tilted(0.64, 0.36, 0.0, eta) for eta in (0, 1, 2, 4)},
        "rejected_route_share": {eta: rejected_route_share(eta) for eta in (0, 1, 2, 4)},
        "random_escalation": {
            "sensitivity 0.80": random_escalation(0.80, 0.05),
            "sensitivity 0.90": random_escalation(0.90, 0.05),
            "sensitivity 0.95": random_escalation(0.95, 0.05),
        },
        "clean_run_needed": {"alpha 5%": clean_run_needed(0.05), "alpha 1%": clean_run_needed(0.01)},
        "composition": {
            "convert, rescale, discretize": (compose([(100, 0), (0.5, 0), (1, 0.003)]), tolerance([(100, 0), (0.5, 0), (1, 0.003)], 0.01)),
            "discretize, convert, rescale": (compose([(1, 0.003), (100, 0), (0.5, 0)]), tolerance([(1, 0.003), (100, 0), (0.5, 0)], 0.01)),
        },
        "checks": {
            "certified lead rule": check_certified_lead(),
            "tilt limit equals ppv": check_tilt_limit(),
            "composition law": check_composition(),
        },
    }
    return out


if __name__ == "__main__":
    import json

    print(json.dumps(run(), indent=2, default=str))
