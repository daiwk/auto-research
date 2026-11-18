"""Yuanbao rubric scoring and exact positive-GRPO/best-rollout loss (v1 §2).

External LLM rubric generation, judgment and production search are not simulated.
The supplied evidence and rewards must be independent of evaluation gold labels.
"""

from __future__ import annotations

import torch
from torch import Tensor
import torch.nn.functional as F

REQUIRES_GPU_VALIDATION = True


def rubric_utility(
    coverage: Tensor, violations: Tensor, positive_weights: Tensor, deductions: Tensor
) -> Tensor:
    """A criterion can be covered collectively; a single violation triggers deduction."""
    if (
        coverage.dtype != torch.bool
        or violations.dtype != torch.bool
        or coverage.ndim != 2
        or violations.ndim != 2
        or coverage.shape[0] != violations.shape[0]
        or positive_weights.shape != coverage.shape[1:]
        or deductions.shape != violations.shape[1:]
        or not torch.isfinite(positive_weights).all()
        or not torch.isfinite(deductions).all()
        or (positive_weights < 0).any()
        or (deductions < 0).any()
    ):
        raise ValueError("boolean document/criterion evidence and nonnegative weights required")
    return (coverage.any(0) * positive_weights).sum() - (violations.any(0) * deductions).sum()


def focal_pairwise(scores: Tensor, labels: Tensor, gamma: float = 2) -> Tensor:
    """Eq.4 is focal-weighted hinge on label/score gaps, not logistic CE."""
    if scores.ndim != 2 or scores.shape != labels.shape or gamma < 0:
        raise ValueError("equal batch-by-document scores and grades required")
    gap = labels[:, :, None] - labels[:, None, :]
    delta = scores[:, :, None] - scores[:, None, :]
    valid = gap > 0
    values = (1 - delta.sigmoid()).pow(gamma) * F.relu(gap - delta)
    return values[valid].mean() if valid.any() else scores.sum() * 0


def dual_branch_loss(
    logp: Tensor,
    old_logp: Tensor,
    mask: Tensor,
    rewards: Tensor,
    *,
    reference_kl: Tensor | None = None,
    kl_weight: float = 0,
    clip: float = 0.2,
    distill_weight: float = 0.5,
) -> dict[str, Tensor]:
    """Eqs.5--6. Each poor rollout weights the same best trajectory, not itself.

    Branch means are separate, and empty branches contribute zero. Exact ties
    have zero distillation weight. Padding never contributes. The reference KL
    is supplied as an explicit per-token quantity; no undocumented estimator.
    """
    if (
        logp.ndim != 3
        or old_logp.shape != logp.shape
        or mask.shape != logp.shape
        or mask.dtype != torch.bool
        or rewards.shape != logp.shape[:2]
        or not mask.any(-1).all()
        or not torch.isfinite(logp).all()
        or not torch.isfinite(old_logp).all()
        or not torch.isfinite(rewards).all()
        or not 0 < clip < 1
        or distill_weight < 0
        or kl_weight < 0
    ):
        raise ValueError("finite B,G,T log probabilities and nonempty rollout masks required")
    if kl_weight > 0 and reference_kl is None:
        raise ValueError("nonzero reference penalty requires explicit per-token KL")
    reward = rewards.detach()
    mean = reward.mean(-1, keepdim=True)
    advantage = (reward - mean) / (reward.std(-1, correction=0, keepdim=True) + 1e-4)
    positive = reward > mean
    ratio = (logp - old_logp.detach()).exp()
    surrogate = torch.minimum(
        ratio * advantage[..., None], ratio.clamp(1 - clip, 1 + clip) * advantage[..., None]
    )
    per_rollout = (surrogate * mask).sum(-1) / mask.sum(-1)
    zero = logp.sum() * 0
    grpo = -per_rollout[positive].mean() if positive.any() else zero
    best = reward.argmax(-1)
    batch = torch.arange(logp.shape[0], device=logp.device)
    best_nll = -(logp[batch, best] * mask[batch, best]).sum(-1) / mask[batch, best].sum(-1)
    weights = reward.max(-1, keepdim=True).values - reward
    correction = weights * best_nll[:, None]
    poor = ~positive
    distill = correction[poor].mean() if poor.any() else zero
    kl = zero
    if reference_kl is not None:
        if reference_kl.shape != logp.shape or not torch.isfinite(reference_kl).all():
            raise ValueError("reference KL must match token scope")
        kl = ((reference_kl * mask).sum(-1) / mask.sum(-1)).mean()
    return {
        "loss": grpo + distill_weight * distill + kl_weight * kl,
        "grpo": grpo,
        "distill": distill,
        "reference_kl": kl,
    }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device not in {"cpu", "cuda"}:
        raise ValueError("integer seed and explicit cpu/cuda device required")
    torch.manual_seed(seed)
    logits = torch.randn(1, 3, 4, 7, device=device, requires_grad=True)
    logp = logits.log_softmax(-1)[..., 0]
    mask = torch.tensor(
        [[[1, 1, 1, 0], [1, 1, 0, 0], [1, 1, 1, 1]]], device=device, dtype=torch.bool
    )
    rewards = torch.tensor([[0.0, 1.0, 3.0]], device=device, requires_grad=True)
    result = dual_branch_loss(logp, logp.detach(), mask, rewards)
    (grad,) = torch.autograd.grad(result["distill"], logits, retain_graph=True)
    result["loss"].backward()
    zero = dual_branch_loss(logp.detach(), logp.detach(), mask, torch.ones_like(rewards))["loss"]
    coverage = torch.tensor([[1, 0], [0, 1]], device=device, dtype=torch.bool)
    violations = torch.tensor([[0], [1]], device=device, dtype=torch.bool)
    value = rubric_utility(
        coverage,
        violations,
        torch.tensor([2.0, 3.0], device=device),
        torch.tensor([4.0], device=device),
    )
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "best_rollout_receives_correction": bool(grad[0, 2].abs().sum() > 0),
            "poor_rollout_not_imitation_target": bool(grad[0, :2].abs().sum() == 0),
            "rewards_detached": rewards.grad is None,
            "padding_has_zero_gradient": bool(logits.grad[~mask].abs().sum() == 0),
            "tied_group_zero_update": bool(zero == 0),
            "set_level_penalty": bool(value == 1),
        },
        "metrics": {
            "diagnostic_loss": float(result["loss"].detach()),
            "best_rollout_distill_gradient_l1": float(grad[0, 2].abs().sum()),
        },
    }
