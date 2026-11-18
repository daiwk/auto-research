"""VisHead-Spec v1 §3/B.4: routed GQA and drafter loss, not a trained decoder."""

from __future__ import annotations

import torch
from torch import Tensor
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/vishead-spec-a100-20261118-latest.json"


def routed_attention(
    q: Tensor, k: Tensor, v: Tensor, image_rows: Tensor, image_heads: Tensor, visibility: Tensor
) -> Tensor:
    """KV-head routing repeats to its query group; visibility owns causal/block rules."""
    if (
        q.ndim != 4
        or k.ndim != 4
        or v.shape != k.shape
        or q.shape[0] != k.shape[0]
        or q.shape[-1] != k.shape[-1]
        or q.shape[1] % k.shape[1]
        or image_rows.shape != (k.shape[2],)
        or image_heads.shape != (k.shape[1],)
        or visibility.shape != (q.shape[2], k.shape[2])
    ):
        raise ValueError("compatible [B,H,T,D] Q/K/V and row/head/visibility masks required")
    if (
        any(x.dtype != torch.bool for x in (image_rows, image_heads, visibility))
        or any(x.device != q.device for x in (k, v, image_rows, image_heads, visibility))
        or not all(bool(torch.isfinite(x).all()) for x in (q, k, v))
    ):
        raise ValueError("finite colocated tensors and boolean masks required")
    groups = q.shape[1] // k.shape[1]
    routed = image_heads.repeat_interleave(groups)
    allowed = visibility[None] & (~image_rows[None, None] | routed[:, None, None])
    if not bool(allowed.any(-1).all()):
        raise ValueError("every query/head needs a visible nonmasked key")
    return F.scaled_dot_product_attention(
        q, k.repeat_interleave(groups, 1), v.repeat_interleave(groups, 1), attn_mask=allowed
    )


def drafter_loss(
    logits: Tensor,
    target_probabilities: Tensor,
    labels: Tensor,
    confidence: Tensor,
    offsets: Tensor,
) -> Tensor:
    """0.1 CE + 0.9 L1 + soft-acceptance BCE; normalized exp(-offset/4) weights."""
    if (
        logits.ndim != 3
        or target_probabilities.shape != logits.shape
        or labels.shape != logits.shape[:2]
        or confidence.shape != labels.shape
        or offsets.shape != logits.shape[1:2]
        or labels.dtype != torch.long
    ):
        raise ValueError("[B,Q,V] distributions, [B,Q] labels/confidence and [Q] offsets required")
    target = target_probabilities.detach()
    if (
        not all(bool(torch.isfinite(x).all()) for x in (logits, target, confidence, offsets))
        or bool((target < 0).any())
        or not torch.allclose(target.sum(-1), torch.ones_like(confidence))
        or bool(((confidence <= 0) | (confidence >= 1)).any())
        or bool((offsets < 0).any())
    ):
        raise ValueError("finite probabilities and nonnegative offsets required")
    p = logits.softmax(-1)
    l1 = (p - target).abs().sum(-1)
    acceptance = (1 - 0.5 * l1).detach()
    ce = F.cross_entropy(logits.flatten(0, 1), labels.flatten(), reduction="none").view_as(
        confidence
    )
    terms = 0.1 * ce + 0.9 * l1 + F.binary_cross_entropy(confidence, acceptance, reduction="none")
    weights = (-offsets.to(logits) / 4).softmax(0)
    return (terms * weights).sum(-1).mean()


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    q = torch.randn(1, 4, 3, 4, device=device, requires_grad=True)
    k, v = (torch.randn(1, 2, 5, 4, device=device) for _ in range(2))
    images = torch.tensor([True, True, False, False, False], device=device)
    heads = torch.tensor([True, False], device=device)
    visible = torch.ones(3, 5, dtype=torch.bool, device=device)
    output = routed_attention(q, k, v, images, heads, visible)
    changed = v.clone()
    changed[:, :, :2] += 9
    alternate = routed_attention(q, k, changed, images, heads, visible)
    logits = torch.randn(1, 3, 7, device=device, requires_grad=True)
    target = torch.randn_like(logits, requires_grad=True).softmax(-1)
    loss = drafter_loss(
        logits,
        target,
        torch.tensor([[1, 2, 3]], device=device),
        torch.full((1, 3), 0.7, device=device),
        torch.arange(3, device=device),
    )
    loss.backward()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "drafter_objective": float(loss.detach()),
            "routed_image_effect": float((output[:, :2] - alternate[:, :2]).abs().max().detach()),
        },
        "checks": {
            "text_only_group_ignores_image": bool(torch.equal(output[:, 2:], alternate[:, 2:])),
            "routed_group_reads_image": bool(not torch.allclose(output[:, :2], alternate[:, :2])),
            "loss_has_gradient": bool(logits.grad is not None and logits.grad.abs().sum() > 0),
            "target_distribution_detached": bool(
                target.grad_fn is not None
                and target.grad_fn.next_functions[0][0].variable.grad is None
            ),
        },
    }
