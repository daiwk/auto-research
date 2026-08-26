from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
import random
import statistics

import numpy as np


def mean_with_std(rows: Sequence[Mapping[str, float]]) -> dict[str, float]:
    """Return per-seed means and population stds using stable ``*_std`` keys."""

    if not rows:
        raise ValueError("at least one seed result is required")
    result: dict[str, float] = {}
    for key in rows[0]:
        values = np.asarray([row[key] for row in rows], dtype=np.float64)
        result[key] = float(values.mean())
        result[f"{key}_std"] = float(values.std(ddof=1)) if len(values) > 1 else 0.0
    return result


@dataclass(frozen=True)
class StatisticalDecision:
    decision: str
    mean_delta: float
    confidence_interval: tuple[float, float]
    p_value: float
    adjusted_p_value: float
    alpha: float
    minimum_effect: float
    seeds: int
    additional_seeds: int
    reason: str

    def to_dict(self):
        return asdict(self)


def bootstrap_paired_interval(baseline, candidate, *, samples=4000,
                              confidence=0.95, seed=0):
    deltas = _paired_deltas(baseline, candidate)
    rng = random.Random(seed)
    means = sorted(statistics.mean(rng.choices(deltas, k=len(deltas))) for _ in range(samples))
    tail = (1.0 - confidence) / 2.0
    return means[int(tail * samples)], means[min(samples - 1, int((1 - tail) * samples))]


def paired_permutation_p_value(baseline, candidate, *, samples=10000, seed=0):
    deltas = _paired_deltas(baseline, candidate)
    observed = abs(statistics.mean(deltas))
    rng = random.Random(seed)
    extreme = 0
    for _ in range(samples):
        value = abs(statistics.mean(value if rng.random() < .5 else -value for value in deltas))
        extreme += value >= observed - 1e-15
    return (extreme + 1) / (samples + 1)


def holm_bonferroni(p_values):
    values = tuple(float(value) for value in p_values)
    ordered = sorted(enumerate(values), key=lambda item: item[1])
    adjusted, running = [0.0] * len(values), 0.0
    for rank, (index, value) in enumerate(ordered):
        running = max(running, min(1.0, (len(values) - rank) * value))
        adjusted[index] = running
    return tuple(adjusted)


def decide_experiment(baseline, candidate, *, minimum_effect=0.0, alpha=.05,
                      adjusted_p_value=None, maximum_seeds=9,
                      estimated_cost=0.0, maximum_cost=None, maximize=True):
    deltas = _paired_deltas(baseline, candidate)
    if not maximize:
        deltas = tuple(-value for value in deltas)
    mean_delta = statistics.mean(deltas)
    low, high = bootstrap_paired_interval([0.0] * len(deltas), deltas)
    p_value = paired_permutation_p_value([0.0] * len(deltas), deltas)
    adjusted = p_value if adjusted_p_value is None else adjusted_p_value
    if maximum_cost is not None and estimated_cost > maximum_cost:
        decision, reason = "reject", "estimated cost exceeds the configured budget"
    elif low > minimum_effect and adjusted <= alpha:
        decision, reason = "promote", "paired effect clears effect-size and corrected significance gates"
    elif high < minimum_effect or (len(deltas) >= maximum_seeds and mean_delta <= minimum_effect):
        decision, reason = "reject", "confidence interval cannot clear the minimum useful effect"
    else:
        decision, reason = "continue", "evidence is inconclusive; collect additional paired seeds"
    additional = 0 if decision != "continue" else max(0, min(3, maximum_seeds - len(deltas)))
    return StatisticalDecision(decision, mean_delta, (low, high), p_value, adjusted,
                               alpha, minimum_effect, len(deltas), additional, reason)


def _paired_deltas(baseline, candidate):
    left = np.asarray(tuple(baseline), dtype=np.float64)
    right = np.asarray(tuple(candidate), dtype=np.float64)
    if not len(left) or left.shape != right.shape:
        raise ValueError("paired samples must be non-empty and have equal length")
    if not np.isfinite(np.concatenate((left, right))).all():
        raise ValueError("paired samples must be finite")
    return tuple(float(value) for value in right - left)
