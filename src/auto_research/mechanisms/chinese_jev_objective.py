"""Extracted unchanged from auto_research.foundation_latest_20260930; stable mechanism boundary."""
from __future__ import annotations

import math

def chinese_jev_objective(logits, targets, decision_types, *, perturbations: int = 4, sigma: float = 0.3, generator=None):
    """Chinese-Jev CE plus RLCD objective from Eqs. (6)-(13)."""
    import torch
    import torch.nn.functional as F

    if logits.shape != targets.shape or logits.ndim != 2:
        raise ValueError("logits and target distributions must be [batch, candidates]")
    if decision_types.shape != logits.shape[:1]:
        raise ValueError("one decision type per batch row is required")
    targets = targets / targets.sum(-1, keepdim=True).clamp_min(1e-12)
    ce = -(targets * torch.log_softmax(logits, -1)).sum(-1).mean()
    noise = torch.randn((*logits.shape[:1], perturbations, logits.shape[-1]), device=logits.device, dtype=logits.dtype, generator=generator) * sigma
    noise = noise - noise.mean(-1, keepdim=True)
    sampled_logits = logits.detach()[:, None, :] + noise
    probabilities = torch.softmax(sampled_logits, -1)
    target = targets[:, None, :]
    log_score = (target * probabilities.clamp_min(math.exp(-9.21)).log()).sum(-1)
    spherical = 0.75 * (target * probabilities).sum(-1) / probabilities.square().sum(-1).sqrt().clamp_min(1e-12)
    cumulative = (probabilities - target).cumsum(-1)[..., :-1]
    rps = cumulative.square().mean(-1)
    ordered = (decision_types == 2).to(logits.dtype)[:, None]
    rewards = log_score + spherical - ordered * rps
    advantages = rewards - rewards.mean(-1, keepdim=True)
    advantages = advantages / advantages.std().clamp_min(1e-6)
    gaussian_log_prob = -noise.square().sum(-1) / (2 * sigma**2)
    rlcd = -(advantages.detach() * gaussian_log_prob).mean()
    return ce + rlcd, {"cross_entropy": float(ce.detach()), "rlcd": float(rlcd.detach()), "reward_std": float(rewards.std().detach())}
