"""Paired-budget trajectory evaluation from arXiv:2610.21555 (§2, Appendix C).

No optimizer training is performed here. All accepted losses are explicitly
validation measurements; the protocol has no test-data or gold-result input.
"""
from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
import math
import random
import statistics
from typing import Mapping, Sequence


def _valid_curve(x: Sequence[float], losses: Sequence[float]) -> None:
    if len(x) < 2 or len(x) != len(losses) or x[0] != 0:
        raise ValueError("a curve needs aligned observations starting at budget zero")
    if (any(not math.isfinite(value) for value in (*x, *losses))
            or any(value <= 0 for value in losses)
            or any(right <= left for left, right in zip(x, x[1:]))):
        raise ValueError("finite strictly increasing budgets and positive finite losses required")


def interpolate_loss(x: Sequence[float], losses: Sequence[float], budget: float) -> float:
    _valid_curve(x, losses)
    if not math.isfinite(budget) or budget < 0 or budget > x[-1]:
        raise ValueError("interpolation cannot extrapolate outside measured budget")
    if budget == x[-1]:
        return float(losses[-1])
    index = bisect_right(x, budget) - 1
    fraction = (budget - x[index]) / (x[index + 1] - x[index])
    return losses[index] + fraction * (losses[index + 1] - losses[index])


def normalized_validation_auc(x: Sequence[float], losses: Sequence[float], horizon: float) -> float:
    _valid_curve(x, losses)
    if not math.isfinite(horizon) or not 0 < horizon <= x[-1]:
        raise ValueError("positive horizon must be within measured data")
    points = [value for value in x if value < horizon] + [horizon]
    values = [interpolate_loss(x, losses, value) for value in points]
    area = math.fsum((right - left) * (a + b) / 2
                     for left, right, a, b in zip(points, points[1:], values, values[1:]))
    return area / horizon


@dataclass(frozen=True)
class ValidationTrajectory:
    run_id: str
    seed: int
    data_units: tuple[float, ...]
    training_seconds: tuple[float, ...]
    validation_loss: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.run_id or not isinstance(self.run_id, str) or not isinstance(self.seed, int):
            raise ValueError("run id and integer replication seed required")
        _valid_curve(self.data_units, self.validation_loss)
        _valid_curve(self.training_seconds, self.validation_loss)


def select_by_validation_data_auc(candidates: Sequence[ValidationTrajectory]) -> ValidationTrajectory:
    """Lexicographic data-AUC, final validation loss, run-id on ONE dev seed.

    All candidates must have the same measured data horizon: a short failed run
    is not allowed to win selection by silently reducing the budget.
    """
    if (not candidates or len({candidate.seed for candidate in candidates}) != 1
            or len({candidate.run_id for candidate in candidates}) != len(candidates)
            or len({candidate.data_units[-1] for candidate in candidates}) != 1):
        raise ValueError("unique candidates on one dev seed and equal data horizon required")
    horizon = candidates[0].data_units[-1]
    return min(candidates, key=lambda candidate: (
        normalized_validation_auc(candidate.data_units, candidate.validation_loss, horizon),
        candidate.validation_loss[-1], candidate.run_id,
    ))


def paired_budget_comparison(reference: ValidationTrajectory, alternative: ValidationTrajectory,
                             *, axis: str) -> dict[str, float | int]:
    if reference.seed != alternative.seed or axis not in {"data", "time"}:
        raise ValueError("paired seeds and a data/time axis required")
    reference_x = reference.data_units if axis == "data" else reference.training_seconds
    alternative_x = alternative.data_units if axis == "data" else alternative.training_seconds
    horizon = min(reference_x[-1], alternative_x[-1])
    ref_auc = normalized_validation_auc(reference_x, reference.validation_loss, horizon)
    alt_auc = normalized_validation_auc(alternative_x, alternative.validation_loss, horizon)
    ref_end = interpolate_loss(reference_x, reference.validation_loss, horizon)
    alt_end = interpolate_loss(alternative_x, alternative.validation_loss, horizon)
    return {"seed": reference.seed, "common_horizon": horizon, "reference_auc": ref_auc,
            "alternative_auc": alt_auc, "relative_auc_gain": 1 - alt_auc / ref_auc,
            "reference_endpoint_loss": ref_end, "alternative_endpoint_loss": alt_end,
            "relative_endpoint_gain": 1 - alt_end / ref_end}


def stable_data_crossover(reference: ValidationTrajectory, alternative: ValidationTrajectory,
                          *, relative_margin: float = .01) -> float | None:
    """First observed budget whose whole remaining checkpoint suffix meets margin.

    The candidate grid is the union of both measured data checkpoints within the
    common horizon. This reports checkpoint resolution, not continuous crossing.
    """
    if reference.seed != alternative.seed or not 0 <= relative_margin < 1:
        raise ValueError("paired seeds and margin in [0,1) required")
    horizon = min(reference.data_units[-1], alternative.data_units[-1])
    grid = sorted({value for value in (*reference.data_units, *alternative.data_units, horizon) if value <= horizon})
    qualifies = [interpolate_loss(alternative.data_units, alternative.validation_loss, value)
                 <= (1 - relative_margin) * interpolate_loss(reference.data_units, reference.validation_loss, value)
                 for value in grid]
    suffix = True
    answer = None
    for value, passes in reversed(list(zip(grid, qualifies))):
        suffix = suffix and passes
        if suffix:
            answer = value
    return answer


def _percentile(values: Sequence[float], fraction: float) -> float:
    ordered = sorted(values)
    index = (len(ordered) - 1) * fraction
    lo, hi = math.floor(index), math.ceil(index)
    return ordered[lo] + (index - lo) * (ordered[hi] - ordered[lo])


def paired_relative_gain_interval(reference: Mapping[int, float], alternative: Mapping[int, float],
                                  *, seed: int = 42, resamples: int = 10000,
                                  confidence: float = .95) -> dict[str, float | int]:
    if (len(reference) < 2 or set(reference) != set(alternative) or resamples < 1
            or not isinstance(resamples, int) or not 0 < confidence < 1
            or any(not math.isfinite(value) or value <= 0
                   for value in (*reference.values(), *alternative.values()))):
        raise ValueError("at least two exact matched seeds and finite positive measurements required")
    keys = sorted(reference)
    rng = random.Random(seed)
    samples = []
    for _ in range(resamples):
        selected = rng.choices(keys, k=len(keys))
        # Sample the same seed indices jointly in both strategies.
        samples.append(1 - math.fsum(alternative[key] for key in selected)
                       / math.fsum(reference[key] for key in selected))
    tail = (1 - confidence) / 2
    return {"paired_seeds": len(keys), "bootstrap_resamples": resamples,
            "relative_gain": 1 - math.fsum(alternative.values()) / math.fsum(reference.values()),
            "lower": _percentile(samples, tail), "upper": _percentile(samples, 1 - tail)}


def frozen_pool_regret(aucs: Sequence[float], *, seed: int = 42,
                       permutations: int = 10000) -> tuple[float, ...]:
    """Expected relative incumbent gap under uniform permutation of a frozen pool.

    This is not a prospective adaptive HPO policy or a comparison of tuning time.
    """
    if (not aucs or any(not math.isfinite(value) or value <= 0 for value in aucs)
            or not isinstance(permutations, int) or permutations < 1):
        raise ValueError("nonempty positive AUC pool and positive permutation count required")
    best = min(aucs)
    total = [0.] * len(aucs)
    rng = random.Random(seed)
    for _ in range(permutations):
        order = list(aucs)
        rng.shuffle(order)
        incumbent = math.inf
        for budget, value in enumerate(order):
            incumbent = min(incumbent, value)
            total[budget] += (incumbent - best) / abs(best)
    return tuple(value / permutations for value in total)


def optimizer_time_share(training_seconds: float, optimizer_seconds: float) -> float:
    """Training clock must already exclude validation, logging and checkpoint I/O."""
    if (not math.isfinite(training_seconds) or not math.isfinite(optimizer_seconds)
            or training_seconds <= 0 or not 0 <= optimizer_seconds <= training_seconds):
        raise ValueError("optimizer time must lie within the positive measured training clock")
    return optimizer_seconds / training_seconds


def paired_mean(values: Sequence[float]) -> float:
    """Finite summary helper, deliberately not a best-seed selection."""
    if not values or any(not math.isfinite(value) for value in values):
        raise ValueError("nonempty finite observations required")
    return statistics.mean(values)
