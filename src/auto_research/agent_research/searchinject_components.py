"""SearchInject score/admission formulas, not a fitted injection detector.

The paper does not release the fitted vocabularies, IDF, scaler or coefficients.
Caller-supplied r/a/i and coefficients are explicit; fixtures cannot certify
security. Calibration labels are not accepted by the inference admission API.
"""

from __future__ import annotations
import math
import random

REQUIRES_GPU_VALIDATION = False


def _prob(x):
    if (
        isinstance(x, bool)
        or not isinstance(x, (int, float))
        or not math.isfinite(x)
        or not 0 <= x <= 1
    ):
        raise ValueError("finite probability/normalized feature required")
    return x


def risk_score(
    relevance: float, abuse: float, instruction: float, coefficients, bias: float = 0.0
) -> float:
    r, a, i = map(_prob, (relevance, abuse, instruction))
    if len(coefficients) != 5 or any(
        isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x)
        for x in (*coefficients, bias)
    ):
        raise ValueError("five finite fixed coefficients and bias required")
    logit = bias + sum(w * x for w, x in zip(coefficients, (r, a, i, a * r, i * r), strict=True))
    return 1 / (1 + math.exp(-logit)) if logit >= 0 else math.exp(logit) / (1 + math.exp(logit))


def calibrate_threshold(clean_scores, crafted_scores, ceiling: float = 0.005) -> dict:
    clean, crafted = tuple(map(_prob, clean_scores)), tuple(map(_prob, crafted_scores))
    if not clean or not crafted or not 0 <= _prob(ceiling) < 1:
        raise ValueError("nonempty disjoint calibration score sets required")
    choices = sorted(set((*clean, *crafted, 1.0)))
    feasible = []
    for t in choices:
        false_quarantine = sum(s > t for s in clean) / len(clean)
        if false_quarantine <= ceiling:
            recall = sum(s > t for s in crafted) / len(crafted)
            feasible.append((recall, -t, t, false_quarantine))
    recall, _, threshold, fq = max(feasible)
    return {
        "threshold": threshold,
        "calibration_recall": recall,
        "calibration_false_quarantine": fq,
        "out_of_sample_guarantee": False,
    }


def admit(
    ranked_ids, scores, threshold: float, *, context_size: int = 10, retrieval_depth: int = 100
):
    _prob(threshold)
    ids, values = tuple(ranked_ids), tuple(map(_prob, scores))
    if (
        len(ids) != len(values)
        or len(set(ids)) != len(ids)
        or any(type(v) is not int or v <= 0 for v in (context_size, retrieval_depth))
    ):
        raise ValueError("aligned unique candidates and positive budgets required")
    return tuple(
        identifier
        for identifier, score in zip(ids[:retrieval_depth], values[:retrieval_depth], strict=True)
        if score <= threshold
    )[:context_size]


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU required")
    rng = random.Random(seed)
    clean = [rng.random() * 0.8 for _ in range(200)]
    calibrated = calibrate_threshold(clean, [0.81, 0.9, 0.95])
    out = admit(("a", "b", "c", "d"), (0.9, 0.2, 0.8, 0.1), 0.8, context_size=2)
    base = risk_score(0.7, 0.3, 0.4, (1, 2, 3, 4, 5))
    reduced = risk_score(0.7, 0.3, 0.4, (1, 2, 3, 0, 0))
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "interaction_terms_used": base != reduced,
            "strict_threshold_refills_order": out == ("b", "c"),
            "empirical_cost_ceiling": calibrated["calibration_false_quarantine"] <= 0.005,
            "no_generalization_guarantee": calibrated["out_of_sample_guarantee"] is False,
        },
        "metrics": {
            "fixture_threshold": calibrated["threshold"],
            "fixture_calibration_recall": calibrated["calibration_recall"],
        },
    }
