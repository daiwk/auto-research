"""Two-level repeated-artifact variance estimators, Appendix B.2.

Scores are already measured data, not generated or selected here. Negative
unbiased run-variance estimates are retained; only the reported SD clips to0.
"""

from __future__ import annotations

import math
from statistics import mean, variance

REQUIRES_GPU_VALIDATION = False


def variance_components(scores: list[list[float]]) -> dict[str, float]:
    if len(scores) < 2 or len(scores[0]) < 2 or any(len(r) != len(scores[0]) for r in scores):
        raise ValueError("balanced >=2 independent artifacts × >=2 evaluations required")
    if any(
        isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x)
        for row in scores
        for x in row
    ):
        raise ValueError("finite measured scores required")
    m = len(scores[0])
    sigma2 = mean(variance(row) for row in scores)
    tau2 = variance(mean(row) for row in scores) - sigma2 / m
    return {
        "evaluation_variance": sigma2,
        "run_variance_unbiased": tau2,
        "evaluation_sd": math.sqrt(sigma2),
        "run_sd": math.sqrt(max(0, tau2)),
        "single_run_variance_estimate": sigma2 + tau2,
        "grand_mean": mean(mean(row) for row in scores),
    }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    noisy = variance_components([[0.0, 1.0], [0.0, 1.0]])
    shifted = variance_components([[2.0, 3.0], [2.0, 3.0]])
    stable = variance_components([[0.0, 0.0], [1.0, 1.0]])
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "negative_unbiased_retained": noisy["run_variance_unbiased"] == -0.25,
            "reported_sd_clipped_only": noisy["run_sd"] == 0,
            "noise_not_run_variation": noisy["evaluation_variance"] == 0.5,
            "offset_invariant": noisy["evaluation_variance"] == shifted["evaluation_variance"],
            "independent_run_variance": stable["run_variance_unbiased"] == 0.5,
        },
        "metrics": {
            "evaluation_variance": noisy["evaluation_variance"],
            "run_variance_unbiased": noisy["run_variance_unbiased"],
            "stable_run_variance": stable["run_variance_unbiased"],
        },
    }
