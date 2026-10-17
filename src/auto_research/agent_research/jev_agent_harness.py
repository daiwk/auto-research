"""Shadow-calibrated decision delegation with safe fallback and cost accounting.

Calibration labels are private fit-only inputs. Execution callbacks receive
only PublicDecision; no teacher, gold option, task outcome or calibration row.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import math
from typing import Mapping


@dataclass(frozen=True)
class ShadowDecision:
    task_id: str
    decision_class: str
    confidence: float
    decision_correct: bool
    strong_correct: bool
    saved_cost: float


@dataclass(frozen=True)
class Calibration:
    thresholds: Mapping[str, float | None]
    task_ids: frozenset[str]
    bins: Mapping[str, tuple[tuple[float, float, int], ...]]


def calibrate(rows, *, task_value=1., min_bin=20, split="calibration", excluded_task_ids=()) -> Calibration:
    """Lowest confidence whose every higher bin has nonnegative advantage.

Equal-confidence rows are never split across bins. The last underfilled bin is
merged into its neighbor; a class with fewer than min_bin rows always defers.
"""
    values = tuple(rows)
    if split not in {"calibration", "validation"} or not values:
        raise ValueError("nonempty held-out calibration rows required")
    if (not math.isfinite(task_value) or task_value <= 0 or type(min_bin) is not int or min_bin < 1):
        raise ValueError("positive task value and integer bin size required")
    ids = frozenset(x.task_id for x in values)
    if not all(ids) or ids & set(excluded_task_ids):
        raise ValueError("calibration and held-out task identities must be disjoint")
    grouped: dict[str, list[ShadowDecision]] = {}
    for row in values:
        if (not row.decision_class or not math.isfinite(row.confidence) or not 0 <= row.confidence <= 1
                or not math.isfinite(row.saved_cost) or row.saved_cost < 0
                or type(row.decision_correct) is not bool or type(row.strong_correct) is not bool):
            raise ValueError("finite confidence, costs and binary shadow verdicts required")
        grouped.setdefault(row.decision_class, []).append(row)
    thresholds, reports = {}, {}
    for name, group in grouped.items():
        group.sort(key=lambda row: row.confidence)
        chunks, pending = [], []
        for i, row in enumerate(group):
            pending.append(row)
            if len(pending) >= min_bin and (i == len(group)-1 or group[i+1].confidence != row.confidence):
                chunks.append(pending)
                pending = []
        if pending and chunks:
            chunks[-1].extend(pending)
        elif pending:
            chunks = []
        bins = tuple((chunk[0].confidence,
                      sum(task_value * (int(x.decision_correct)-int(x.strong_correct)) + x.saved_cost
                          for x in chunk) / len(chunk), len(chunk)) for chunk in chunks)
        reports[name] = bins
        valid = [i for i in range(len(bins)) if all(b[1] >= 0 for b in bins[i:])]
        thresholds[name] = bins[min(valid)][0] if valid else None
    return Calibration(thresholds, ids, reports)


@dataclass(frozen=True)
class PublicDecision:
    task_id: str
    decision_class: str
    context: str
    options: tuple[str, ...]


@dataclass(frozen=True)
class RoutedDecision:
    action_index: int
    source: str
    confidence: float | None
    total_cost: float
    fallback_reason: str | None


def route(request: PublicDecision, calibration: Calibration, *, decision_model, strong_model,
          decision_cost=0., strong_cost=0.) -> RoutedDecision:
    if not request.options or len(set(request.options)) != len(request.options):
        raise ValueError("distinct nonempty public options required")
    if request.task_id in calibration.task_ids:
        raise ValueError("execution tasks must be held out from calibration")
    if any(not math.isfinite(x) or x < 0 for x in (decision_cost, strong_cost)):
        raise ValueError("nonnegative finite declared costs required")
    confidence, reason = None, "unfitted_class"
    threshold = calibration.thresholds.get(request.decision_class)
    if threshold is not None:
        try:
            probabilities = tuple(decision_model(deepcopy(request)))
            if (len(probabilities) != len(request.options)
                    or any(not math.isfinite(x) or x < 0 for x in probabilities)
                    or not math.isclose(sum(probabilities), 1., abs_tol=1e-6)):
                raise ValueError("invalid decision probabilities")
            index = max(range(len(probabilities)), key=probabilities.__getitem__)
            confidence = probabilities[index]
            if confidence >= threshold:
                return RoutedDecision(index, "decision_model", confidence, decision_cost, None)
            reason = "below_fitted_threshold"
        except Exception:
            reason = "decision_model_failure"
    index = strong_model(deepcopy(request))
    if type(index) is not int or not 0 <= index < len(request.options):
        raise ValueError("strong fallback returned an invalid action")
    # Unfitted classes never invoke a decision model, so do not charge that call.
    cost = strong_cost + (decision_cost if threshold is not None else 0.)
    return RoutedDecision(index, "strong_model", confidence, cost, reason)
