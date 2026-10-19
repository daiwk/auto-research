"""Harness-Delta Attribution: paired significance plus reviewed four-arm controls."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class Arm:
    item_ids: tuple[str, ...]
    scores: tuple[float, ...]
    mean_inference_cost: float
    harness_sha256: str


@dataclass(frozen=True)
class ReviewedControl:
    reviewer: str
    evidence: str
    approved: bool


def _arm(arm: Arm) -> None:
    if (not arm.item_ids or any(not isinstance(i, str) or not i for i in arm.item_ids)
            or len(set(arm.item_ids)) != len(arm.item_ids)
            or len(arm.item_ids) != len(arm.scores)
            or any(type(v) not in (int, float) or not math.isfinite(v) for v in arm.scores)
            or type(arm.mean_inference_cost) not in (int, float)
            or not math.isfinite(arm.mean_inference_cost) or arm.mean_inference_cost < 0
            or not isinstance(arm.harness_sha256, str) or len(arm.harness_sha256) != 64
            or set(arm.harness_sha256)-set("0123456789abcdef")):
        raise ValueError("paired finite scores, cost and harness SHA256 required")


def attribute(baseline: Arm, evolved: Arm, scaled: Arm, neutralized: Arm, *,
              compute_review: ReviewedControl, neutralization_review: ReviewedControl,
              seed: int = 42, resamples: int = 10_000, alpha: float = .05,
              relative_cost_tolerance: float = .05) -> dict:
    """No actor invocation or ground truth access; use immutable evaluated arm records.

    Signed raw components retain the exact identity. Clipped reporting shares
    are not confidence bounds; residual is only an upper-bound interpretation.
    """
    arms = (baseline, evolved, scaled, neutralized)
    for arm in arms:
        _arm(arm)
    if any(a.item_ids != baseline.item_ids for a in arms[1:]):
        raise ValueError("four arms must have identical ordered item identities")
    for review in (compute_review, neutralization_review):
        if (review.approved is not True or not isinstance(review.reviewer, str)
                or not isinstance(review.evidence, str) or not review.reviewer.strip() or not review.evidence.strip()):
            raise ValueError("both task-specific human review checkpoints required")
    if (type(resamples) is not int or not 100 <= resamples <= 100_000 or
            type(alpha) not in (int, float) or not 0 < alpha < 1
            or type(relative_cost_tolerance) not in (int, float) or not 0 <= relative_cost_tolerance < 1):
        raise ValueError("invalid bootstrap/control settings")
    if evolved.mean_inference_cost <= baseline.mean_inference_cost:
        if scaled != baseline:
            raise ValueError("no extra evolved compute: scaled control must equal baseline")
    elif abs(scaled.mean_inference_cost-evolved.mean_inference_cost) > max(
            1e-12, evolved.mean_inference_cost*relative_cost_tolerance):
        raise ValueError("scaled baseline does not match evolved inference budget")
    diffs = np.asarray(evolved.scores)-np.asarray(baseline.scores)
    rng = np.random.default_rng(seed)
    # Bounded chunks avoid materializing resamples x unbounded corpus at once.
    if len(diffs) > 100_000:
        raise ValueError("too many items for local bootstrap budget")
    boot = np.empty(resamples)
    chunk = max(1, min(128, 1_000_000//len(diffs)))
    for start in range(0, resamples, chunk):
        end = min(start+chunk, resamples)
        indexes = rng.integers(0, len(diffs), size=(end-start, len(diffs)))
        boot[start:end] = diffs[indexes].mean(axis=1)
    lo, hi = np.percentile(boot, [100*alpha/2, 100*(1-alpha/2)])
    delta = float(diffs.mean())
    significant = not lo <= 0 <= hi
    tail = float(np.mean(boot <= 0)) if delta > 0 else float(np.mean(boot >= 0)) if delta < 0 else .5
    base_score, evo_score, scale_score, neutral_score = [float(np.mean(a.scores)) for a in arms]
    result = {"observed_gain": delta, "ci_low": float(lo), "ci_high": float(hi),
              "significant": bool(significant), "attributed": bool(significant and delta > 0),
              "n": len(diffs), "resamples": resamples, "bootstrap_p_value": min(1., 2*tail)}
    if not result["attributed"]:
        result["reason"] = "within_noise_or_no_positive_gain"
        return result
    t, o, g = scale_score-base_score, evo_score-neutral_score, neutral_score-scale_score
    o_share = min(1., max(0., o/delta))
    t_share = min(1-o_share, max(0., t/delta))
    result.update({"test_time_scaling": t, "detected_overfitting": o,
        "residual_upper_bound": g, "raw_identity_error": abs(delta-o-t-g),
        "overfitting_share": o_share, "scaling_share": t_share,
        "residual_share": 1-o_share-t_share,
        "interpretation": "detected overfitting lower estimate; residual not proof of transfer"})
    return result
