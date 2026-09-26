"""Interval-aware frozen offline/online audit from Meta's layered protocol.

This module implements the *audit contract*, not Meta's private engagement
classifier, undisclosed calibration coefficients or reported empirical result.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

import numpy as np


@dataclass(frozen=True)
class Interval:
    lower: float
    upper: float

    def __post_init__(self) -> None:
        if not np.isfinite((self.lower, self.upper)).all() or self.lower > self.upper:
            raise ValueError("interval endpoints must be finite and ordered")

    @property
    def sign(self) -> int:
        if self.lower > 0:
            return 1
        if self.upper < 0:
            return -1
        return 0


@dataclass(frozen=True)
class Contrast:
    experiment_id: str
    contrast_id: str
    frozen_at: datetime
    offline_scored_at: datetime
    exposure_started_at: datetime
    offline: Interval
    online: Interval

    def __post_init__(self) -> None:
        if not self.experiment_id or not self.contrast_id:
            raise ValueError("experiment and contrast identifiers are required")
        if any(value.tzinfo is None for value in (self.frozen_at, self.offline_scored_at,
                                                   self.exposure_started_at)):
            raise ValueError("timestamps must be timezone-aware")
        if not (self.frozen_at <= self.offline_scored_at < self.exposure_started_at):
            raise ValueError("calibration and offline scoring must predate treatment exposure")


def paired_scoring_interval(control: np.ndarray, treatment: np.ndarray, *,
                            scale: float, seed: int = 42,
                            draws: int = 10_000) -> Interval:
    """Bootstrap *paired cases* through a frozen linear map (no online residual)."""
    control = np.asarray(control, dtype=float)
    treatment = np.asarray(treatment, dtype=float)
    if (control.ndim != 1 or treatment.shape != control.shape or
            len(control) < 2 or not np.isfinite(control).all() or
            not np.isfinite(treatment).all() or draws < 2):
        raise ValueError("paired finite arrays of at least two cases are required")
    # Same sampled case indices in both arms; auxiliary pre-exposure terms, if
    # used, belong in the frozen map upstream, not in this resampling step.
    rng = np.random.default_rng(seed)
    differences = treatment - control
    estimates = np.empty(draws)
    for index in range(draws):
        samples = rng.integers(0, len(differences), len(differences))
        estimates[index] = scale * differences[samples].mean()
    low, high = np.quantile(estimates, (0.025, 0.975))
    return Interval(float(low), float(high))


def audit(contrasts: tuple[Contrast, ...]) -> dict[str, float | int]:
    """Micro/macro directional F1, wrong-direction calls and abstentions."""
    if not contrasts:
        raise ValueError("at least one paired contrast is required")
    seen = set()
    by_experiment: dict[str, list[Contrast]] = defaultdict(list)
    for row in contrasts:
        key = (row.experiment_id, row.contrast_id)
        if key in seen:
            raise ValueError(f"duplicate contrast: {key}")
        seen.add(key)
        by_experiment[row.experiment_id].append(row)
    counts = []
    wrong = abstained = 0
    power_support = []
    for rows in by_experiment.values():
        calls = sum(row.offline.sign != 0 for row in rows)
        movers = sum(row.online.sign != 0 for row in rows)
        correct = sum(row.offline.sign != 0 and row.offline.sign == row.online.sign
                      for row in rows)
        counts.append((correct, calls, movers))
        wrong += sum(row.offline.sign * row.online.sign == -1 for row in rows)
        abstained += len(rows) - calls
        for row in rows:
            if row.offline.sign == 0:
                continue
            width = row.online.upper - row.online.lower
            if width == 0:
                power_support.append(float(row.offline.sign == row.online.sign))
            elif row.offline.sign > 0:
                power_support.append(float(np.clip(row.online.upper / width, 0, 1)))
            else:
                power_support.append(float(np.clip(-row.online.lower / width, 0, 1)))
    correct, calls, movers = map(sum, zip(*counts))
    return {"contrasts": len(contrasts), "experiments": len(by_experiment),
            "decisive_calls": calls, "online_significant": movers,
            "correct_decisive": correct, "wrong_direction": wrong,
            "abstained": abstained,
            "contrast_micro_f1": 2 * correct / (calls + movers) if calls + movers else 0.0,
            "experiment_macro_f1": float(np.mean([
                2 * c / (p + o) if p + o else 0.0 for c, p, o in counts])),
            "power_aware_precision": float(np.mean(power_support)) if calls else 0.0}
