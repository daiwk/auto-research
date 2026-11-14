"""MaxIM (2611.12825), Eqs. 4--7: CPU-only reward arithmetic.

This module does not supply/train a critic or summarization policy. All critic
log probabilities are externally supplied, teacher-forced, frozen scores.
"""
from __future__ import annotations

import math
import numpy as np

REQUIRES_GPU_VALIDATION = False


def normalized_pmi(conditional: np.ndarray, null: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Mean conditional-minus-null log probability over valid target tokens."""
    conditional, null = np.asarray(conditional, dtype=np.float64), np.asarray(null, dtype=np.float64)
    mask = np.asarray(mask)
    if conditional.ndim < 1 or conditional.shape != null.shape or mask.shape != conditional.shape or mask.dtype != np.bool_:
        raise ValueError("aligned token log probabilities and Boolean mask required")
    if not np.all(mask.any(-1)) or not np.isfinite(conditional[mask]).all() or not np.isfinite(null[mask]).all():
        raise ValueError("each target needs finite valid tokens")
    if np.any(conditional[mask] > 0) or np.any(null[mask] > 0):
        raise ValueError("log probabilities must be nonpositive")
    return np.where(mask, np.where(mask, conditional, 0) - np.where(mask, null, 0), 0).sum(-1) / mask.sum(-1)


def shaping_reward(pred: np.ndarray, cons: np.ndarray, *, sufficiency_weight: float = 1., consistency_weight: float = .25,
                   pred_scale: float = 1., pred_center: float = 0., cons_scale: float = 1., cons_center: float = 0.) -> np.ndarray:
    """Eq. 6; calibration parameters must come from pre-RL data, not test tuning."""
    pred, cons = np.asarray(pred, dtype=np.float64), np.asarray(cons, dtype=np.float64)
    parameters = (sufficiency_weight, consistency_weight, pred_scale, pred_center, cons_scale, cons_center)
    if pred.shape != cons.shape or not np.isfinite(pred).all() or not np.isfinite(cons).all() or not all(math.isfinite(x) for x in parameters):
        raise ValueError("aligned finite scores and calibration required")
    if not 0 <= consistency_weight < sufficiency_weight or pred_scale <= 0 or cons_scale <= 0:
        raise ValueError("require 0 <= consistency_weight < sufficiency_weight and positive scales")
    # sigmoid(x)-1/2 = tanh(x/2)/2 avoids exponential overflow.
    return .5 * (sufficiency_weight * np.tanh(.5 * pred_scale * (pred - pred_center))
                 + consistency_weight * np.tanh(.5 * cons_scale * (cons - cons_center)))


def cosine_weight(step: int, *, hold_until: int, decay_until: int) -> float:
    """Hold at one, cosine-decay to zero, then stay zero (caller fixes schedule)."""
    if any(type(v) is not int for v in (step, hold_until, decay_until)) or step < 0 or hold_until < 0 or decay_until <= hold_until:
        raise ValueError("nonnegative integer steps and decay_until > hold_until required")
    if step <= hold_until:
        return 1.
    if step >= decay_until:
        return 0.
    return .5 * (1 + math.cos(math.pi * (step - hold_until) / (decay_until - hold_until)))


def discounted_returns(task: np.ndarray, shape: np.ndarray, mask: np.ndarray, *, gamma: float, shape_weight: float) -> np.ndarray:
    """Eq. 7 on right-padded episodes; padding cannot leak across a termination."""
    task, shape, mask = np.asarray(task, dtype=np.float64), np.asarray(shape, dtype=np.float64), np.asarray(mask)
    if task.ndim < 1 or task.shape != shape.shape or task.shape != mask.shape or mask.dtype != np.bool_ or task.shape[-1] < 1:
        raise ValueError("aligned nonempty episode arrays and Boolean mask required")
    if not math.isfinite(gamma) or not 0 <= gamma < 1 or not math.isfinite(shape_weight) or not 0 <= shape_weight <= 1:
        raise ValueError("gamma in [0,1) and shape_weight in [0,1] required")
    if not np.isfinite(task[mask]).all() or not np.isfinite(shape[mask]).all() or np.any(mask[..., 1:] & ~mask[..., :-1]):
        raise ValueError("finite scores and right padding required")
    rewards = np.where(mask, np.where(mask, task, 0) + (1 - gamma) * shape_weight * np.where(mask, shape, 0), 0)
    result = np.zeros_like(rewards)
    carry = np.zeros(task.shape[:-1], dtype=np.float64)
    for t in range(task.shape[-1] - 1, -1, -1):
        carry = np.where(mask[..., t], rewards[..., t] + gamma * carry, 0)
        result[..., t] = carry
    return result


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("MaxIM arithmetic is a CPU-only component")
    rng = np.random.default_rng(seed)
    scores = -rng.uniform(.1, 4., (3, 6))
    mask = np.ones(scores.shape, dtype=bool)
    mask[0, -2:] = False
    shifted = normalized_pmi(scores + .05, scores, mask)
    zero = shaping_reward(np.zeros(3), np.zeros(3))
    shape = shaping_reward(shifted, -shifted)
    task = np.zeros((3, 6)); task[:, -1] = 1.
    masks = np.ones(task.shape, dtype=bool)
    returns = discounted_returns(task, np.broadcast_to(shape[:, None], task.shape), masks, gamma=.9, shape_weight=.5)
    baseline = discounted_returns(task, np.zeros_like(task), masks, gamma=.9, shape_weight=0.)
    checks = {
        "pmi_uses_null_baseline": bool(np.allclose(shifted, .05)),
        "centered_reward_zero_at_calibration_center": bool(np.all(zero == 0)),
        "shaping_bounded": bool(np.all(np.abs(shape) <= .625)),
        "late_schedule_removes_critic": cosine_weight(20, hold_until=5, decay_until=15) == 0.,
        "terminal_task_discounted": bool(np.allclose(baseline[:, 0], .9 ** 5)),
        "shape_balanced_by_one_minus_gamma": bool(np.allclose(returns[:, 0] - baseline[:, 0], .5 * shape * (1 - .9 ** 6))),
    }
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"pmi_mean": float(shifted.mean()), "shape_mean": float(shape.mean()), "initial_return_mean": float(returns[:, 0].mean()), "critic_model_calls": 0}, "checks": checks}
