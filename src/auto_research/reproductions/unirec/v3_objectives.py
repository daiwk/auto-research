"""UniRec v3 Eqs. 8--19: trainable objectives, not the production fusion model.

The legacy NumPy adapter is a concept demo. These standalone differentiable
operators preserve contradictory preference evidence and group KL; they do not
claim to implement the paper's DCN/Mixer/AutoInt towers or RecFlow experiment.
"""
from __future__ import annotations

import math

import torch
from torch.nn import functional as F


def preference_evidence(predictions: torch.Tensor, weights: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Aggregate M detached objective labels over N candidates, retaining ties."""
    if predictions.ndim != 2 or weights.shape != (predictions.shape[1],) or predictions.shape[0] < 1:
        raise ValueError("expected N x M predictions and M non-negative weights")
    if not torch.isfinite(predictions).all() or not torch.isfinite(weights).all() or (weights < 0).any():
        raise ValueError("finite predictions and non-negative weights required")
    direction = (predictions[:, None, :] - predictions[None, :, :]).detach()
    weights = weights.detach()
    return ((direction > 0) * weights).sum(-1), ((direction < 0) * weights).sum(-1)


def confidence_pairs(positive: torch.Tensor, negative: torch.Tensor, k: int) -> torch.Tensor:
    """Per-row top-K directed pairs; ties resolve by original candidate index."""
    _validate_evidence(positive, negative)
    n = len(positive)
    if type(k) is not int or not 0 <= k <= max(n - 1, 0):
        raise ValueError("k must be in [0,N-1]")
    confidence = (positive - negative).abs().detach().clone()
    confidence.fill_diagonal_(-torch.inf)
    indices = confidence.argsort(dim=1, descending=True, stable=True)[:, :k]
    mask = torch.zeros_like(positive, dtype=torch.bool)
    mask.scatter_(1, indices, True)
    return mask


def _validate_evidence(positive: torch.Tensor, negative: torch.Tensor) -> None:
    if positive.ndim != 2 or positive.shape[0] != positive.shape[1] or negative.shape != positive.shape:
        raise ValueError("square aligned evidence required")
    if not torch.isfinite(positive).all() or not torch.isfinite(negative).all() or (positive < 0).any() or (negative < 0).any():
        raise ValueError("finite non-negative evidence required")


def cppa_loss(scores: torch.Tensor, positive: torch.Tensor, negative: torch.Tensor,
              *, pair_mask: torch.Tensor | None = None) -> torch.Tensor:
    """Exact sum loss, not softplus of an averaged/majority-voted direction."""
    _validate_evidence(positive, negative)
    if scores.shape != positive.shape[:1] or not torch.isfinite(scores).all():
        raise ValueError("one finite score per candidate required")
    if pair_mask is not None and (pair_mask.shape != positive.shape or pair_mask.dtype != torch.bool):
        raise ValueError("boolean N x N pair mask required")
    if pair_mask is None:
        margin = scores[:, None] - scores[None, :]
        return (positive.detach() * F.softplus(-margin) + negative.detach() * F.softplus(margin)).sum()
    first, second = pair_mask.nonzero(as_tuple=True)
    margin = scores[first] - scores[second]
    return (positive[first, second].detach() * F.softplus(-margin)
            + negative[first, second].detach() * F.softplus(margin)).sum()


def evidence_rewards(positive: torch.Tensor, negative: torch.Tensor, *, epsilon: float = 1e-8) -> torch.Tensor:
    """Eq.14: epsilon is inside the sum over j, before any CAPP pruning."""
    _validate_evidence(positive, negative)
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be positive")
    return ((positive - negative).sum(1) / (positive + negative + epsilon).sum(1)).detach()


def quantile_groups(attributes: torch.Tensor, buckets: int) -> torch.Tensor:
    """Quantile boundaries; equal attributes never split into different groups."""
    if attributes.ndim != 1 or len(attributes) < 1 or not torch.isfinite(attributes).all():
        raise ValueError("one finite attribute per candidate required")
    if type(buckets) is not int or not 1 <= buckets <= len(attributes):
        raise ValueError("invalid bucket count")
    boundaries = torch.quantile(attributes.detach(), torch.arange(1, buckets, device=attributes.device,
                                dtype=attributes.dtype) / buckets)
    return torch.bucketize(attributes.detach().contiguous(), boundaries, right=False)


def agrr_loss(scores: torch.Tensor, rewards: torch.Tensor, groups: torch.Tensor, *,
              temperature: float = 1., sigma_min: float = 1e-3, advantage_max: float = 5.,
              minimum_count: int = 2) -> torch.Tensor:
    """Eqs.15--16: KL(softmax(A/tau) || softmax(scores)), not signed likelihood.

    Population standard deviation is explicit. Eligible groups are averaged
    equally, not items; skipped groups contribute no gradient.
    """
    if scores.ndim != 1 or rewards.shape != scores.shape or groups.shape != scores.shape:
        raise ValueError("aligned one-dimensional scores, rewards and groups required")
    if not torch.isfinite(scores).all() or not torch.isfinite(rewards).all() or groups.is_floating_point():
        raise ValueError("finite values and integer groups required")
    if any(not math.isfinite(x) or x <= 0 for x in (temperature, sigma_min, advantage_max)) or minimum_count < 1:
        raise ValueError("positive regularization controls required")
    losses = []
    for group in torch.unique(groups):
        mask = groups == group
        if int(mask.sum()) < minimum_count:
            continue
        local = rewards[mask].detach()
        advantage = ((local - local.mean()) / local.std(unbiased=False).clamp_min(sigma_min)).clamp(-advantage_max, advantage_max)
        log_q = F.log_softmax(advantage / temperature, dim=0)
        losses.append((log_q.exp() * (log_q - F.log_softmax(scores[mask], dim=0))).sum())
    return torch.stack(losses).mean() if losses else scores.sum() * 0


def cross_stage_alignment(pre_scores: torch.Tensor, rank_scores: torch.Tensor) -> torch.Tensor:
    """Eq.12 on ranking survivors only, with frozen downstream directions."""
    if pre_scores.ndim != 1 or pre_scores.shape != rank_scores.shape or not torch.isfinite(rank_scores).all():
        raise ValueError("aligned scores on surviving candidates required")
    direction = (rank_scores[:, None] - rank_scores[None, :]).detach()
    return cppa_loss(pre_scores, (direction > 0).to(pre_scores), (direction < 0).to(pre_scores))
