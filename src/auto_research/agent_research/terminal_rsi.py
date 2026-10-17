"""NumPy TB-GAE and frozen-family reward operators, not a terminal agent.

TB-GAE deployment in the paper's reported checkpoints is unverified; these
functions implement the proposed equations, not a claimed online gain.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from types import MappingProxyType

import numpy as np


@dataclass(frozen=True)
class Continuation:
    value: float
    advantage: float
    turn_id: int


@dataclass(frozen=True)
class AdvantageResult:
    advantages: np.ndarray
    returns: np.ndarray
    generated_indices: np.ndarray


def tb_gae(rewards, values, turn_ids, generated_mask, terminated, *, gamma_turn=.99,
           lambda_turn=.95, continuation: Continuation | None = None):
    """Eq.8–12: observation tokens are context, never recursion nodes.

    A nonterminal computational cutoff requires both successor value and
    successor advantage. Dropping either is not exact chunk continuation.
    """
    r, v = np.asarray(rewards, float), np.asarray(values, float)
    t = np.asarray(turn_ids)
    mask, done = np.asarray(generated_mask), np.asarray(terminated)
    if (r.ndim != 1 or not r.size or any(a.shape != r.shape for a in (v, t, mask, done))
            or not np.isfinite(r).all() or not np.isfinite(v).all()
            or t.dtype.kind not in "iu" or mask.dtype.kind != "b" or done.dtype.kind != "b"):
        raise ValueError("matched finite vectors, integer turns and boolean masks required")
    if not (math.isfinite(gamma_turn) and math.isfinite(lambda_turn)
            and 0 <= gamma_turn <= 1 and 0 <= lambda_turn <= 1):
        raise ValueError("turn clocks must lie in [0,1]")
    indices = np.flatnonzero(mask)
    if not len(indices) or np.any(r[~mask] != 0) or np.any(done[~mask]):
        raise ValueError("generated tokens required; observations cannot own reward/termination")
    if np.any(t[indices] < 0):
        raise ValueError("nonnegative turn identifiers required")
    if continuation is not None:
        if (not math.isfinite(continuation.value) or not math.isfinite(continuation.advantage)
                or not isinstance(continuation.turn_id, int) or continuation.turn_id < 0):
            raise ValueError("finite explicit chunk continuation required")
    if not done[indices[-1]] and continuation is None:
        raise ValueError("nonterminal cutoff needs successor value and advantage")
    advantages, returns = np.zeros_like(r), np.zeros_like(r)
    for position in range(len(indices) - 1, -1, -1):
        i = indices[position]
        if done[i]:
            next_value, next_advantage, gamma, trace = 0., 0., 1., 1.
        else:
            if position + 1 < len(indices):
                j = indices[position + 1]
                next_value, next_advantage, next_turn = v[j], advantages[j], int(t[j])
            else:
                next_value, next_advantage, next_turn = (
                    continuation.value, continuation.advantage, continuation.turn_id)
            if next_turn < t[i]:
                raise ValueError("turn IDs cannot move backwards within an episode")
            gamma, trace = (1., 1.) if next_turn == t[i] else (gamma_turn, lambda_turn)
        delta = r[i] + gamma * next_value - v[i]
        advantages[i] = delta + gamma * trace * next_advantage
        returns[i] = advantages[i] + v[i]
    if not np.isfinite(advantages).all():
        raise ValueError("advantage overflow")
    return AdvantageResult(advantages, returns, indices)


@dataclass(frozen=True)
class FamilyDivisors:
    values: object
    fallback: float = 82.

    def __post_init__(self):
        values = {str(k): float(v) for k, v in dict(self.values).items()}
        if (not math.isfinite(self.fallback) or self.fallback <= 0
                or any(not k or not math.isfinite(v) or v <= 0 for k, v in values.items())):
            raise ValueError("positive finite frozen divisors required")
        object.__setattr__(self, "values", MappingProxyType(values))

    def for_family(self, family):
        return self.values.get(family, self.fallback)


def calibrate_family_divisors(calibration_totals, *, quantile=.9, split="calibration"):
    """Historical family quantile, frozen per phase; never fit on test outcomes."""
    if split != "calibration" or not 0 <= quantile <= 1:
        raise ValueError("calibration-only family quantile required")
    divisors = {}
    for family, totals in dict(calibration_totals).items():
        x = np.asarray(totals, float)
        if x.ndim != 1 or not x.size or not np.isfinite(x).all() or np.any(x < 0):
            raise ValueError("nonnegative finite historical check counts required")
        value = float(np.quantile(x, quantile, method="linear"))
        if value <= 0:
            raise ValueError("family quantile must be positive")
        divisors[family] = value
    return FamilyDivisors(divisors)


def reward(passed_checks, success, family, divisors: FamilyDivisors, *, kind="spr",
           report_valid=True):
    """FDR is unbounded; SPR has bounded partial progress below strict success."""
    if (isinstance(passed_checks, bool) or not math.isfinite(passed_checks)
            or passed_checks < 0 or success not in (False, True, 0, 1)
            or kind not in ("fdr", "spr") or not isinstance(report_valid, bool)):
        raise ValueError("valid passed-check count, strict-success flag and reward kind required")
    if not report_valid:
        return float(success)
    p, d = float(passed_checks), divisors.for_family(family)
    if kind == "fdr":
        result = p / d
        if not math.isfinite(result):
            raise ValueError("FDR exceeds representable numeric range")
        return result
    scale = max(p, d)
    progress = (p / scale) / (p / scale + d / scale)
    # Rounding at extreme P/D must not turn a failed rollout into strict success.
    progress = min(progress, float(np.nextafter(1., 0.)))
    return float(success) + progress
