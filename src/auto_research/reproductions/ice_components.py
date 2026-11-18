"""ICE display–impression–click tensor contracts, arXiv:2611.07591v1 §§3.3–4.4.

The caller supplies depth/click logits and observation labels. No production
features, generator, learned backbone, or treatment-effect estimation here.
"""
from __future__ import annotations

import math

import torch
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


def _matrix(value: torch.Tensor, name: str) -> None:
    if (not isinstance(value, torch.Tensor) or value.ndim != 2 or not all(value.shape)
            or value.dtype not in (torch.float32, torch.float64) or not torch.isfinite(value).all()):
        raise ValueError(f"{name} must be a nonempty finite [batch, positions] float32/64 tensor")


def _probabilities(value: torch.Tensor) -> None:
    _matrix(value, "impressions")
    if ((value < 0) | (value > 1)).any():
        raise ValueError("impression probabilities must lie in [0, 1]")


def _matching(left: torch.Tensor, right: torch.Tensor) -> None:
    if left.shape != right.shape or left.dtype != right.dtype or left.device != right.device:
        raise ValueError("shapes, dtype and device must match")


def impression_survival(depth_logits: torch.Tensor) -> torch.Tensor:
    """Eq. 9, with T=1..L; the first position is reached by construction."""
    _matrix(depth_logits, "depth_logits")
    probabilities = depth_logits.softmax(-1)
    tail = probabilities.flip(-1).cumsum(-1).flip(-1)
    return torch.cat((torch.ones_like(tail[:, :1]), tail[:, 1:].clamp(max=1)), dim=-1)


def impression_attention_bias(impressions: torch.Tensor, epsilon: float = 1e-8) -> torch.Tensor:
    """Eq. 10 additive bias; click gradients never update the depth signal here."""
    _probabilities(impressions)
    if not math.isfinite(epsilon) or not torch.finfo(impressions.dtype).tiny <= epsilon <= 1:
        raise ValueError("epsilon must be representable and in (0, 1]")
    p = impressions.detach()
    return (p.unsqueeze(-1) * p.unsqueeze(-2) + epsilon).log()


def gate_click_features(features: torch.Tensor, impressions: torch.Tensor, alpha: float = 1.0) -> torch.Tensor:
    """Eq. 11 feature gate for nonattention backbones."""
    _probabilities(impressions)
    if (features.ndim != 3 or not features.shape[-1] or features.shape[:2] != impressions.shape
            or features.dtype != impressions.dtype or features.device != impressions.device
            or not torch.isfinite(features).all()):
        raise ValueError("features must be finite matching [batch, positions, channels]")
    if not math.isfinite(alpha) or not 0 <= alpha <= 1:
        raise ValueError("alpha must lie in [0, 1]")
    return features * (alpha * impressions.detach() + (1 - alpha)).unsqueeze(-1)


def _event_labels(labels: torch.Tensor, logits: torch.Tensor) -> torch.Tensor:
    if labels.shape != logits.shape or labels.device != logits.device:
        raise ValueError("event labels must match logits shape/device")
    if not ((labels == 0) | (labels == 1)).all():
        raise ValueError("event labels must be binary")
    return labels.detach().to(dtype=logits.dtype)


def click_distribution_loss(logits: torch.Tensor, clicks: torch.Tensor, temperature: float = 1.0) -> torch.Tensor:
    """Eq. 12, KL(target || predicted), sum over slates, including zero-click slates."""
    _matrix(logits, "click_logits")
    labels = _event_labels(clicks, logits)
    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be finite and positive")
    scaled = logits / temperature
    if not torch.isfinite(scaled).all():
        raise ValueError("scaled click logits overflow")
    count = labels.sum(-1, keepdim=True)
    target = torch.where(count > 0, labels / count.clamp(min=1), 1.0 / logits.shape[-1])
    log_prediction = scaled.log_softmax(-1)
    if not torch.isfinite(log_prediction).all():
        raise ValueError("click log probabilities overflow")
    return F.kl_div(log_prediction, target, reduction="sum")


def ice_objective(
    depth_logits: torch.Tensor,
    click_logits: torch.Tensor,
    impressions: torch.Tensor,
    clicks: torch.Tensor,
    *,
    temperature: float = 1.0,
    distribution_weight: float = 20.0,
) -> dict[str, torch.Tensor]:
    """§4.4 loss from logits, with stable log-tail/log-head BCE for ITR."""
    _matrix(depth_logits, "depth_logits")
    _matrix(click_logits, "click_logits")
    _matching(depth_logits, click_logits)
    shown = _event_labels(impressions, depth_logits)
    clicked = _event_labels(clicks, click_logits)
    if (not shown[:, 0].all() or (shown[:, 1:] > shown[:, :-1]).any() or (clicked > shown).any()):
        raise ValueError("ICE requires a nonempty reached prefix and no click outside it")
    if not math.isfinite(distribution_weight) or distribution_weight < 0:
        raise ValueError("distribution weight must be finite and nonnegative")
    log_depth = depth_logits.log_softmax(-1)
    if not torch.isfinite(log_depth).all():
        raise ValueError("depth log probabilities overflow")
    # First position is always reached. The remaining positions have nonempty
    # disjoint sets of depths on either side of their visibility threshold.
    tails = log_depth.flip(-1).logcumsumexp(-1).flip(-1)[:, 1:]
    heads = log_depth.logcumsumexp(-1)[:, :-1]
    itr = -torch.where(shown[:, 1:].bool(), tails, heads).sum()
    ctr = F.binary_cross_entropy_with_logits(click_logits[shown.bool()], clicked[shown.bool()], reduction="sum")
    distribution = click_distribution_loss(click_logits, clicked, temperature)
    total = itr + ctr + distribution_weight * distribution
    if not torch.isfinite(total):
        raise ValueError("ICE loss overflow")
    return {"impression": itr, "conditional_click": ctr, "click_distribution": distribution, "total": total}


def sequence_value(depth_logits: torch.Tensor, click_logits: torch.Tensor, reward: torch.Tensor) -> torch.Tensor:
    """Eqs. 8/13: score with joint display-to-click probability."""
    impressions = impression_survival(depth_logits)
    _matrix(click_logits, "click_logits")
    _matrix(reward, "reward")
    _matching(impressions, click_logits)
    _matching(impressions, reward)
    value = (impressions * click_logits.sigmoid() * reward).sum(-1)
    if not torch.isfinite(value).all():
        raise ValueError("sequence value overflow")
    return value


def diagnostic(seed: int, device: str = "cpu") -> dict:
    rng = torch.Generator().manual_seed(seed)
    depth = torch.randn(2, 4, generator=rng, dtype=torch.float64).to(device).requires_grad_()
    click = torch.randn(2, 4, generator=rng, dtype=torch.float64).to(device).requires_grad_()
    shown = depth.new_tensor([[1, 1, 0, 0], [1, 1, 1, 0]])
    observed = depth.new_tensor([[0, 1, 0, 0], [0, 0, 0, 0]])
    p = impression_survival(depth)
    reference = torch.stack([depth.softmax(-1)[:, k:].sum(-1) for k in range(4)], -1)
    loss = ice_objective(depth, click, shown, observed)
    grad_depth, grad_click = torch.autograd.grad(loss["total"], (depth, click))
    bias = impression_attention_bias(p)
    zero = click_distribution_loss(torch.zeros_like(click), torch.zeros_like(observed))
    joint = sequence_value(depth, click, torch.ones_like(depth))
    error = float((p - reference).abs().max().detach())
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"tail_sum_max_error": error, "zero_click_uniform_kl": float(zero),
                        "diagnostic_loss": float(loss["total"].detach()),
                        "mean_expected_clicks": float(joint.mean().detach())},
            "checks": {"suffix_probability_reference": error < 1e-12,
                       "monotone_reach": bool((p[:, 1:] <= p[:, :-1]).all()),
                       "detached_attention_bias": not bias.requires_grad,
                       "uniform_zero_click_target": abs(float(zero)) < 1e-12,
                       "finite_gradients": bool(torch.isfinite(grad_depth).all() & torch.isfinite(grad_click).all()),
                       "joint_le_conditional": bool((joint <= click.sigmoid().sum(-1)).all())}}
