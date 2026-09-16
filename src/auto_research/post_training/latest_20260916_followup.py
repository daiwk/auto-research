"""Executable L1 mechanisms for TIAO and Style-Debiased DPO."""

from __future__ import annotations

import numpy as np


def tiao_credit(full_log_probs, masked_log_probs, advantage: float, threshold_quantile: float = 0.5, tau: float = 5.0):
    """Source-dependency estimation and dual-scale trajectory/token credit."""
    full = np.asarray(full_log_probs, dtype=np.float64)
    masked = np.asarray(masked_log_probs, dtype=np.float64)
    shift = np.clip(masked - full, -tau, tau)
    importance = np.exp(shift) - shift - 1.0
    trajectory_dependency = float(importance.mean())
    cutoff = float(np.quantile(importance, threshold_quantile))
    token_mask = importance >= cutoff
    shaped = float(advantage) * (1.0 + trajectory_dependency) * token_mask * importance
    return shaped, {
        "trajectory_dependency": trajectory_dependency,
        "selected_token_fraction": float(token_mask.mean()),
        "credit_l1": float(np.abs(shaped).sum()),
    }


def style_debiased_dpo(factual_agreement, margins, beta: float = 0.1, threshold: float = 0.5):
    """SD-DPO inversion and group balancing from Equation 4."""
    factual = np.asarray(factual_agreement, dtype=np.float64)
    margins = np.asarray(margins, dtype=np.float64)
    wrong = factual < threshold
    p = float(wrong.mean())
    direction = np.where(wrong, 1.0, -1.0)
    group_weight = np.where(wrong, 1.0 - p, p)
    confidence = np.abs(factual - threshold) + 1e-6
    for mask in (wrong, ~wrong):
        if mask.any():
            confidence[mask] /= confidence[mask].mean()
    signed = direction * margins
    loss = np.logaddexp(0.0, -beta * signed) * group_weight * confidence
    return loss, {
        "wrong_pair_fraction": p,
        "inverted_pair_fraction": float((~wrong).mean()),
        "style_balance_residual": float(abs(group_weight[wrong].sum() - group_weight[~wrong].sum())),
    }


def update_latest(algorithm, state, group, probabilities, reference, rollout_training_probabilities, sampled, rng):
    del rollout_training_probabilities, rng
    expected = probabilities @ group.features
    diagnostics = {}
    if algorithm == "tiao":
        full = np.log(reference[sampled] + 1e-12)
        masked = np.log(probabilities[sampled] + 1e-12)
        rewards = group.rewards[sampled] @ np.asarray((0.7, 0.05, 0.2, 0.05))
        credit, diagnostics = tiao_credit(full, masked, float(rewards.mean()))
        advantages = credit - credit.mean()
    elif algorithm == "sd-dpo":
        margins = np.log(reference[sampled] + 1e-12) - np.log(probabilities[sampled] + 1e-12)
        factual = np.clip(reference[sampled] / (reference[sampled] + probabilities[sampled] + 1e-12), 0.0, 1.0)
        losses, diagnostics = style_debiased_dpo(factual, margins)
        advantages = losses.mean() - losses
    else:  # pragma: no cover
        raise ValueError(algorithm)
    gradient = np.zeros_like(state.weights)
    for index, advantage in zip(sampled, advantages):
        gradient += float(advantage) * (group.features[index] - expected)
    gradient /= max(1, len(sampled))
    return gradient, float(np.mean(np.abs(advantages))), diagnostics


def tiao_cuda_kernel(full_log_probs, masked_log_probs, advantages, tau: float = 5.0):
    """CUDA-compatible TIAO token dependency and dual-scale credit."""
    import torch

    if any(tensor.device.type != "cuda" for tensor in (full_log_probs, masked_log_probs, advantages)):
        raise ValueError("tiao_cuda_kernel requires CUDA tensors")
    shift = torch.clamp(masked_log_probs - full_log_probs, -tau, tau)
    importance = torch.exp(shift) - shift - 1.0
    trajectory = importance.mean(dim=-1, keepdim=True)
    cutoff = torch.quantile(importance, 0.5, dim=-1, keepdim=True)
    mask = importance >= cutoff
    credit = advantages[:, None] * (1.0 + trajectory) * mask * importance
    return credit, importance, mask
