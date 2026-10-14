"""TAPO Eqs. 9, 13--15: trajectory forward value, local action gradient."""
from __future__ import annotations
import torch


def trajectory_ratio(current_log_probability, behavior_log_probability, mask):
    if current_log_probability.shape != behavior_log_probability.shape or current_log_probability.shape != mask.shape:
        raise ValueError("likelihoods and response mask must align")
    positions = mask.long().cumsum(-1).clamp_min(1)
    log_ratio = (current_log_probability - behavior_log_probability.detach()) * mask
    geometric = (log_ratio.cumsum(-1) / positions).exp()
    # The prefix value is NOT backpropagated. Eq.15 has no 1/t dilution and
    # cannot create cross-position gradients through the cumulative product.
    local = (current_log_probability - current_log_probability.detach()).exp()
    return geometric.detach() * local


def length_aware_clipping(mask, *, horizon, low_max=.2, high_max=.2, low_min=.0003, high_min=.0004):
    if horizon < 1 or not 0 <= low_min <= low_max < 1 or not 0 <= high_min <= high_max:
        raise ValueError("invalid clipping schedule")
    positions = mask.long().cumsum(-1).clamp_min(1).to(torch.float32)
    if (positions > horizon).any():
        raise ValueError("response exceeds configured clipping horizon")
    if horizon == 1:
        fraction = torch.ones_like(positions)
    else:
        endpoint = horizon ** -.5
        fraction = (positions.rsqrt() - endpoint) / (1 - endpoint)
    low = low_min + (low_max - low_min) * fraction
    high = high_min + (high_max - high_min) * fraction
    return 1 - low, 1 + high


def tapo_loss(current_log_probability, behavior_log_probability, advantages, mask, *, horizon,
              low_max=.2, high_max=.2, low_min=.0003, high_min=.0004):
    if (mask.sum(-1) == 0).any():
        raise ValueError("each trajectory needs at least one response token")
    ratio = trajectory_ratio(current_log_probability, behavior_log_probability, mask)
    lower, upper = length_aware_clipping(mask, horizon=horizon, low_max=low_max, high_max=high_max,
                                         low_min=low_min, high_min=high_min)
    clipped = torch.maximum(lower, torch.minimum(upper, ratio))
    advantage = advantages.detach()
    if advantage.ndim == ratio.ndim - 1:
        advantage = advantage[..., None]
    surrogate = torch.minimum(ratio * advantage, clipped * advantage)
    loss = -((surrogate * mask).sum(-1) / mask.sum(-1)).mean()
    return loss, {"clip_fraction": float((((ratio < lower) | (ratio > upper)) * mask).sum().detach() / mask.sum()),
                  "horizon": horizon, "prefix_stop_gradient": True,
                  "ratio_mean": float((ratio.detach() * mask).sum() / mask.sum())}
