"""SciResearch-Eval's proper interval score, not a scientist agent (§2.3)."""

from __future__ import annotations

import math
from collections.abc import Mapping

REQUIRES_GPU_VALIDATION = False


def interval_score(truth: float, low: float, high: float, *, alpha: float = 0.05) -> float:
    values = (truth, low, high, alpha)
    if any(
        isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x)
        for x in values
    ):
        raise ValueError("finite numeric interval values required")
    if not 0 < alpha < 1 or low > high:
        raise ValueError("ordered interval and alpha in (0,1) required")
    return high - low + 2 / alpha * max(low - truth, 0) + 2 / alpha * max(truth - high, 0)


def parameter_score(
    predictions: Mapping[str, tuple[float, float]], evaluator_truth: Mapping[str, float]
) -> dict:
    """Evaluator-only positive physical truths; return mean log10 interval score.

    There is no actor callback here. A simulator, fitted interval, or fixture
    must not be given these truths as the agent's observations.
    """
    if not evaluator_truth or set(predictions) != set(evaluator_truth):
        raise ValueError("all and only declared physical parameters must be scored")
    scores, covered = [], []
    for name, truth in evaluator_truth.items():
        interval = predictions[name]
        if len(interval) != 2:
            raise ValueError("two interval endpoints required")
        lo, hi = interval
        if any(
            isinstance(x, bool) or not isinstance(x, (float, int)) or not math.isfinite(x) or x <= 0
            for x in (truth, lo, hi)
        ):
            raise ValueError("positive finite physical values required before log10")
        scores.append(interval_score(math.log10(truth), math.log10(lo), math.log10(hi)))
        covered.append(lo <= truth <= hi)
    return {
        "mean_parameter_interval_score": sum(scores) / len(scores),
        "parameter_coverage": sum(covered) / len(covered),
    }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    narrow_miss = interval_score(2, 0.9, 1.1)
    wide_cover = interval_score(2, 0, 3)
    unit_a = parameter_score({"k": (1, 10)}, {"k": 2})
    unit_b = parameter_score({"k": (1000, 10000)}, {"k": 2000})
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "miscoverage_penalty": narrow_miss > wide_cover,
            "log_unit_shift_invariant": math.isclose(
                unit_a["mean_parameter_interval_score"], unit_b["mean_parameter_interval_score"]
            ),
            "exact_boundary_covered": interval_score(1, 1, 1) == 0,
            "wider_not_free": interval_score(1, 0, 3) > interval_score(1, 0.5, 1.5),
        },
        "metrics": {
            "narrow_miss_score": narrow_miss,
            "wide_cover_score": wide_cover,
            "parameter_score": unit_a["mean_parameter_interval_score"],
        },
    }
