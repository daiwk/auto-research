"""Safety-as-a-Budget: training-only isotonic maps and two-channel dual arithmetic.

Only CPU calibration/controller mechanisms are supplied. There is no VLM,
scorer, judge, policy optimizer or capability/safety benchmark. PAV is exact on
observed scores; right-continuous step interpolation is a local explicit choice.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _array(values, *, dimension=None, probability=False):
    result = np.asarray(values)
    if (
        result.dtype.kind not in "fiu"
        or result.dtype.kind == "b"
        or result.size == 0
        or (dimension is not None and result.ndim != dimension)
        or not np.isfinite(result).all()
    ):
        raise ValueError("nonempty finite numeric array of the declared dimension required")
    result = result.astype(float)
    if probability and ((result < 0).any() or (result > 1).any()):
        raise ValueError("probabilities must be in [0,1]")
    return result


@dataclass(frozen=True)
class IsotonicMap:
    x: tuple[float, ...]
    y: tuple[float, ...]
    fitted_split: str = "train"

    def __post_init__(self):
        x, y = (
            _array(self.x, dimension=1, probability=True),
            _array(self.y, dimension=1, probability=True),
        )
        if (
            self.fitted_split != "train"
            or x.shape != y.shape
            or (np.diff(x) <= 0).any()
            or (np.diff(y) < 0).any()
        ):
            raise ValueError("training-only ordered unique knots and nondecreasing levels required")

    def predict(self, scores):
        p = _array(scores, probability=True)
        indices = np.searchsorted(np.asarray(self.x), p, side="right") - 1
        return np.asarray(self.y)[indices.clip(0, len(self.y) - 1)]


def fit_isotonic(scores, labels, *, split: str, weights=None) -> IsotonicMap:
    """Weighted least-squares PAV; labels come from training-trajectory judging.

    Equal score values are merged first. No held-out evaluation/test responses
    may fit a map. Their source/provenance remains the caller's responsibility.
    """
    x, y = (
        _array(scores, dimension=1, probability=True),
        _array(labels, dimension=1, probability=True),
    )
    if split != "train" or x.shape != y.shape or not np.isin(y, [0.0, 1.0]).all():
        raise ValueError("matching training-only scores and binary judge labels required")
    w = np.ones_like(x) if weights is None else _array(weights, dimension=1)
    if w.shape != x.shape or (w <= 0).any():
        raise ValueError("positive calibration weights matching observations required")
    order = np.argsort(x, kind="stable")
    x, y, w = x[order], y[order], w[order]
    knots, starts = np.unique(x, return_index=True)
    sums, totals = np.add.reduceat(w * y, starts), np.add.reduceat(w, starts)
    blocks = []
    for index, (total, weighted_sum) in enumerate(zip(totals, sums, strict=True)):
        blocks.append([index, index + 1, total, weighted_sum])
        while len(blocks) >= 2 and blocks[-2][3] / blocks[-2][2] > blocks[-1][3] / blocks[-1][2]:
            right, left = blocks.pop(), blocks.pop()
            blocks.append([left[0], right[1], left[2] + right[2], left[3] + right[3]])
    fitted = np.empty(len(knots))
    for start, end, total, weighted_sum in blocks:
        fitted[start:end] = weighted_sum / total
    return IsotonicMap(tuple(knots.tolist()), tuple(fitted.tolist()))


def two_channel_reward(
    p_h,
    p_r,
    p_f,
    harmful_prompt,
    multipliers,
    *,
    harm_map: IsotonicMap,
    refusal_map: IsotonicMap,
    helpful_weight: float = 0.65,
) -> dict[str, np.ndarray]:
    """Eqs.1/3: raw base reward, mapped penalty; each row is one prompt group."""
    ph, pr, pf = [_array(x, dimension=2, probability=True) for x in (p_h, p_r, p_f)]
    harmful = np.asarray(harmful_prompt)
    lam = _array(multipliers, dimension=1)
    if (
        pr.shape != ph.shape
        or pf.shape != ph.shape
        or harmful.shape != (ph.shape[0],)
        or harmful.dtype != bool
        or lam.shape != (2,)
        or (lam < 0).any()
        or not isinstance(harm_map, IsotonicMap)
        or not isinstance(refusal_map, IsotonicMap)
        or isinstance(helpful_weight, bool)
        or not math.isfinite(helpful_weight)
        or not 0 <= helpful_weight <= 1
    ):
        raise ValueError(
            "aligned probability groups, Boolean prompt classes, maps and nonnegative multipliers required"
        )
    base = np.where(harmful[:, None], 1 - ph, helpful_weight * pf + (1 - helpful_weight) * (1 - pr))
    mapped_h, mapped_r = harm_map.predict(ph), refusal_map.predict(pr)
    penalty = np.where(harmful[:, None], lam[0] * mapped_h, lam[1] * mapped_r)
    return {
        "base": base,
        "mapped_harm": mapped_h,
        "mapped_refusal": mapped_r,
        "penalty": penalty,
        "reward": base - penalty,
    }


def unscaled_advantage(reward):
    """Section3.3: subtract group mean, never divide the penalized reward by std."""
    values = _array(reward, dimension=2)
    if values.shape[1] < 2:
        raise ValueError("at least two responses per prompt required")
    return values - values.mean(axis=1, keepdims=True)


def update_dual(
    multipliers,
    previous_ema,
    batch_cost_means,
    budgets,
    *,
    current_weight=0.3,
    step_size=0.5,
    maximum=10.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Eq.4 with explicit previous EMA; weight .3 multiplies the current batch.

    The source does not uniquely specify initialization. Requiring a previous
    state avoids silently claiming a recovered initialization or absent-class
    convention. Callers must supply observed means for both constraints.
    """
    lam = _array(multipliers, dimension=1)
    previous, current, eps = [
        _array(x, dimension=1, probability=True) for x in (previous_ema, batch_cost_means, budgets)
    ]
    if any(x.shape != (2,) for x in (lam, previous, current, eps)) or (lam < 0).any():
        raise ValueError("two explicit constraint states, means and budgets required")
    if (
        any(
            isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x)
            for x in (current_weight, step_size, maximum)
        )
        or not 0 < current_weight <= 1
        or step_size <= 0
        or maximum <= 0
        or (lam > maximum).any()
    ):
        raise ValueError("valid EMA weight, positive step/cap and multipliers within cap required")
    ema = (1 - current_weight) * previous + current_weight * current
    return np.clip(lam + step_size * (ema - eps), 0, maximum), ema


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only calibration/controller required")
    order = np.random.default_rng(seed).permutation(5)
    x, y = np.array([0.1, 0.1, 0.2, 0.4, 0.8]), np.array([0.0, 1.0, 0.0, 1.0, 1.0])
    fitted = fit_isotonic(x[order], y[order], split="train")
    expected = np.array([1 / 3, 1 / 3, 1.0, 1.0])
    values = two_channel_reward(
        [[0.1, 0.2]],
        [[0.0, 0.0]],
        [[0.0, 0.0]],
        [True],
        [2.0, 0.0],
        harm_map=fitted,
        refusal_map=fitted,
    )
    ph = np.array([[0.2, 0.8]])
    a0, a2 = unscaled_advantage(1 - ph), unscaled_advantage(1 - 3 * ph)
    lam, ema = update_dual([0.1, 9.9], [0.0, 1.0], [0.0, 1.0], [0.5, 0.1])
    checks = {
        "weighted_tie_pav_solution": bool(np.allclose(fitted.y, expected)),
        "base_raw_ranking_preserved": bool(values["base"][0, 0] > values["base"][0, 1])
        and values["mapped_harm"][0, 0] == values["mapped_harm"][0, 1],
        "lambda_reaches_unscaled_advantage": bool(np.allclose(a2, 3 * a0)),
        "dual_projects_lower_and_upper": bool(np.array_equal(lam, [0.0, 10.0])),
        "explicit_previous_ema": bool(np.array_equal(ema, [0.0, 1.0])),
        "map_monotone": bool((np.diff(fitted.y) >= 0).all()),
    }
    return {
        "seed": seed,
        "device": device,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": checks,
        "metrics": {
            "calibration_observations": 5,
            "unique_score_knots": len(fitted.x),
            "mapped_level_error": float(np.max(np.abs(np.asarray(fitted.y) - expected))),
            "lower_multiplier": float(lam[0]),
            "upper_multiplier": float(lam[1]),
            "pretrained_model_calls": 0,
        },
    }
