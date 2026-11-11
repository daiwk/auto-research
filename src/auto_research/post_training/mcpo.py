"""MCPO (2611.14015): old-policy margin, sign-aware token credit, Eqs. 2--3.

CPU numerical component only, not an RL trainer or a task-capability benchmark.
"""
from __future__ import annotations

import math
import numpy as np

REQUIRES_GPU_VALIDATION = False


def token_credit(top_two_probabilities: np.ndarray, advantages: np.ndarray, mask: np.ndarray,
                 *, lower: float = .1, upper: float = .7, kappa: float = math.log(4.)) -> np.ndarray:
    """Use top-2 probabilities AFTER rollout temperature, frozen at old policy.

    Each sequence's mean token advantage is its sequence advantage. ``lower``
    and ``upper`` bound uncertainty 1-margin, not margin itself or a band-pass.
    """
    probs = np.asarray(top_two_probabilities, dtype=np.float64)
    advantages, mask = np.asarray(advantages, dtype=np.float64), np.asarray(mask)
    if probs.ndim != 3 or probs.shape[-1] != 2 or probs.shape[:2] != mask.shape or advantages.shape != probs.shape[:1] or mask.dtype != np.bool_:
        raise ValueError("top-two [batch,tokens,2], advantages [batch], and Boolean mask required")
    if not mask.any(-1).all() or not np.isfinite(advantages).all() or not np.isfinite(probs[mask]).all():
        raise ValueError("finite advantages/probabilities and nonempty sequences required")
    active = probs[mask]
    if np.any(active < 0) or np.any(active > 1) or np.any(active[:, 0] < active[:, 1]) or np.any(active.sum(-1) > 1 + 1e-12):
        raise ValueError("ordered top-two valid probabilities required")
    if not all(math.isfinite(v) for v in (lower, upper, kappa)) or not 0 <= lower < upper <= 1 or kappa < 0:
        raise ValueError("0 <= lower < upper <= 1 and finite nonnegative kappa required")
    safe_probs = np.where(mask[..., None], probs, 0.)
    margin = safe_probs[..., 0] - safe_probs[..., 1]
    uncertainty = np.clip((1 - margin - lower) / (upper - lower), 0., 1.)
    # Subtracting the per-row maximum leaves normalization unchanged and avoids overflow.
    log_weight = kappa * np.sign(advantages[:, None]) * uncertainty
    log_weight -= np.max(np.where(mask, log_weight, -np.inf), axis=-1, keepdims=True)
    weight = np.where(mask, np.exp(log_weight), 0.)
    mean_weight = weight.sum(-1, keepdims=True) / mask.sum(-1, keepdims=True)
    return advantages[:, None] * weight / mean_weight


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("MCPO token credit is a CPU-only component")
    rng = np.random.default_rng(seed)
    logits = rng.normal(size=(3, 12, 9))
    logits -= logits.max(-1, keepdims=True)
    probs = np.exp(logits); probs /= probs.sum(-1, keepdims=True)
    top = np.sort(probs, axis=-1)[..., -2:][..., ::-1]
    mask = np.ones((3, 12), dtype=bool); mask[0, -3:] = False
    advantages = np.array([2., -1., 0.])
    credit = token_credit(top, advantages, mask)
    probe = np.array([[[.95, .02], [.45, .40]], [[.95, .02], [.45, .40]]])
    signed = token_credit(probe, np.array([1., -1.]), np.ones((2, 2), dtype=bool))
    checks = {
        "per_sequence_credit_mean_preserved": bool(np.allclose(credit.sum(-1) / mask.sum(-1), advantages)),
        "positive_uncertain_token_receives_more_credit": bool(signed[0, 1] > signed[0, 0]),
        "negative_uncertain_token_receives_less_penalty": bool(abs(signed[1, 1]) < abs(signed[1, 0])),
        "zero_advantage_stays_zero": bool(np.all(credit[2] == 0)),
        "padding_is_zero": bool(np.all(credit[~mask] == 0)),
        "raw_weight_ratio_four": bool(np.isclose(signed[0, 1] / signed[0, 0], 4.)),
    }
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"max_mean_preservation_error": float(np.max(np.abs(credit.sum(-1) / mask.sum(-1) - advantages))), "positive_credit_ratio": float(signed[0, 1] / signed[0, 0]), "negative_penalty_ratio": float(signed[1, 1] / signed[1, 0]), "model_calls": 0}, "checks": checks}
