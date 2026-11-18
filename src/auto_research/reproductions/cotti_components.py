"""COTTI v1 Eqs.6--16: CPC/RW/ABA, not a production recommendation model."""

from __future__ import annotations

import math
import torch
from torch import Tensor
import torch.nn.functional as F

REQUIRES_GPU_VALIDATION = True


def cross_period_contrast(regular: Tensor, promo: Tensor, temperature: float = 0.1) -> Tensor:
    if regular.ndim != 2 or regular.shape != promo.shape or temperature <= 0:
        raise ValueError("paired nonempty history views required")
    if not regular.shape[0] or not torch.isfinite(regular).all() or not torch.isfinite(promo).all():
        raise ValueError("finite nonempty views required")
    logits = F.normalize(regular, dim=-1) @ F.normalize(promo, dim=-1).T / temperature
    per_user = F.cross_entropy(
        logits, torch.arange(len(regular), device=regular.device), reduction="none"
    )
    # Eq.8 uses raw representation distance, not the normalized contrastive vectors.
    variance = (regular - promo).square().mean(-1) / 4
    gate = 1 - variance.sigmoid()  # intentionally differentiable, unlike RW
    return (gate * per_user).sum()


def historical_weights(item: Tensor, regular: Tensor, gamma: float, eps: float = 1e-8) -> Tensor:
    if item.ndim != 2 or item.shape != regular.shape or gamma < 0 or eps <= 0:
        raise ValueError("compatible item/history vectors and nonnegative scale required")
    distance = (item - regular).square().sum(-1)
    standardized = (distance - distance.mean()) / (distance.std(correction=0) + eps)
    weights = (-gamma * standardized).exp().detach()
    if not torch.isfinite(weights).all():
        raise ValueError("unclipped paper weights overflowed; do not silently change their scale")
    return weights


def weighted_supervision(logits: Tensor, labels: Tensor, weights: Tensor) -> Tensor:
    if logits.shape != labels.shape or logits.shape != weights.shape or (weights < 0).any():
        raise ValueError("aligned logits, binary labels and nonnegative weights required")
    return (
        F.binary_cross_entropy_with_logits(logits, labels, reduction="none") * weights.detach()
    ).sum()


def event_adjustment(
    logit: Tensor,
    dropout_head_logits: Tensor,
    *,
    time: float,
    peak: float,
    event_width: float,
    amplitude: float,
    beta: float,
) -> Tensor:
    """Fixed predictor; population variance, one-sided bounded correction (§III-D)."""
    if (
        dropout_head_logits.ndim != logit.ndim + 1
        or dropout_head_logits.shape[1:] != logit.shape
        or not dropout_head_logits.shape[0]
        or event_width <= 0
        or amplitude < 0
        or beta <= 0
        or not all(math.isfinite(x) for x in (time, peak, event_width, amplitude, beta))
        or not torch.isfinite(logit).all()
        or not torch.isfinite(dropout_head_logits).all()
    ):
        raise ValueError("finite head-only dropout samples and predeclared event settings required")
    variance = dropout_head_logits.var(0, correction=0)
    alpha = amplitude * math.exp(-((time - peak) ** 2) / (2 * event_width**2))
    return (logit + alpha * (beta * variance).tanh()).sigmoid()


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device not in {"cpu", "cuda"}:
        raise ValueError("integer seed and explicit cpu/cuda device required")
    torch.manual_seed(seed)
    regular = torch.randn(5, 6, device=device, requires_grad=True)
    promo = torch.randn(5, 6, device=device, requires_grad=True)
    cpc = cross_period_contrast(regular, promo)
    (correct_gradient,) = torch.autograd.grad(cpc, regular, retain_graph=True)
    pair_logits = F.normalize(regular, dim=-1) @ F.normalize(promo, dim=-1).T / 0.1
    detached_gate = (1 - ((regular - promo).square().mean(-1) / 4).sigmoid()).detach()
    detached_loss = (
        detached_gate
        * F.cross_entropy(pair_logits, torch.arange(5, device=device), reduction="none")
    ).sum()
    (detached_gradient,) = torch.autograd.grad(detached_loss, regular)
    gate_gradient_present = bool(not torch.allclose(correct_gradient, detached_gradient, atol=1e-7))
    cpc.backward()
    weights = historical_weights(promo, regular, 0.3)
    logits = torch.zeros(5, device=device, requires_grad=True)
    loss = weighted_supervision(
        logits, torch.tensor([0.0, 1.0, 0.0, 1.0, 1.0], device=device), weights
    )
    loss.backward()
    samples = torch.stack((logits.detach() - 1, logits.detach() + 1))
    adjusted = event_adjustment(
        logits.detach(), samples, time=0, peak=0, event_width=1, amplitude=0.5, beta=1
    )
    absent = event_adjustment(
        logits.detach(), samples, time=0, peak=0, event_width=1, amplitude=0, beta=1
    )
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "cpc_gate_differentiable": gate_gradient_present,
            "rw_detached": not weights.requires_grad,
            "rw_not_mean_normalized": not bool(
                torch.isclose(weights.mean(), weights.new_tensor(1))
            ),
            "aba_one_sided": bool((adjusted >= 0.5).all()),
            "aba_bounded": bool((adjusted <= torch.tensor(0.5, device=device).sigmoid()).all()),
            "zero_event_recovers_base": bool(torch.equal(absent, logits.detach().sigmoid())),
        },
        "metrics": {
            "cpc_loss": float(cpc.detach()),
            "rw_weight_sum": float(weights.sum()),
            "adjusted_probability": float(adjusted.mean()),
        },
    }
