"""Scoring-time operator from Meta's baseline/incremental decomposition (Eq. 3).

This consumes externally supplied predictions and historical baselines. It does
not estimate causal uplift or reproduce Instagram's production value model.
"""
from __future__ import annotations

import math
import numpy as np


def incremental_term(predictions, baselines, *, scale="logit", magnitude="prediction",
                     sharpness=1.0, shift=0.0, direction="promotion", constant=1.0,
                     clamp=1e-6):
    p, b = np.broadcast_arrays(np.asarray(predictions, dtype=float),
                               np.asarray(baselines, dtype=float))
    if not (np.isfinite(p).all() and np.isfinite(b).all()):
        raise ValueError("predictions/baselines must be finite")
    if scale not in {"logit", "raw"} or magnitude not in {"prediction", "gap", "constant"}:
        raise ValueError("unknown comparison scale or magnitude")
    if direction not in {"promotion", "demotion"}:
        raise ValueError("unknown direction")
    if not (0 < clamp < .5 and math.isfinite(shift) and math.isfinite(constant)
            and constant >= 0 and sharpness > 0 and not math.isnan(sharpness)):
        raise ValueError("invalid operator parameters")
    gap = p - b
    if scale == "logit":
        if np.any((p < 0) | (p > 1)):
            raise ValueError("logit predictions must be probabilities")
        # Historical features can exceed one; the paper explicitly clamps them.
        pc, bc = np.clip(p, clamp, 1-clamp), np.clip(b, clamp, 1-clamp)
        comparison = (np.log(pc) - np.log1p(-pc)) - (np.log(bc) - np.log1p(-bc))
    else:
        comparison = gap
    if direction == "demotion":
        comparison = -comparison
        if magnitude == "prediction":
            raise ValueError("paper demotions must not vanish at the prediction floor")
    if math.isinf(sharpness):
        gate = np.where(comparison > 0, 1.0, np.where(comparison < 0, 0.0, .5))
    else:
        z = sharpness * comparison
        gate = np.exp(-np.logaddexp(0, -z))
    mag = p if magnitude == "prediction" else gap if magnitude == "gap" else constant
    if direction == "demotion" and magnitude == "constant":
        mag = -constant
    return mag * (gate - shift)


def value_model(raw_predictions, increments, *, raw_weights, incremental_weights):
    """Sum signals on the last axis with independent raw/incremental weights."""
    p, d = np.asarray(raw_predictions, float), np.asarray(increments, float)
    wr, wi = np.asarray(raw_weights, float), np.asarray(incremental_weights, float)
    if p.shape != d.shape or p.ndim < 1 or wr.shape != (p.shape[-1],) or wi.shape != wr.shape:
        raise ValueError("signals and weight dimensions do not match")
    if not all(np.isfinite(x).all() for x in (p, d, wr, wi)):
        raise ValueError("scores/weights must be finite")
    return (p * wr + d * wi).sum(axis=-1)


def request_baseline(predictions, *, statistic="p75"):
    p = np.asarray(predictions, float)
    if p.ndim != 1 or not p.size or not np.isfinite(p).all():
        raise ValueError("one nonempty finite request pool required")
    if statistic == "mean":
        return float(p.mean())
    if statistic not in {"p10", "p25", "p50", "p75", "p90"}:
        raise ValueError("unsupported request statistic")
    return float(np.quantile(p, int(statistic[1:])/100, method="linear"))
