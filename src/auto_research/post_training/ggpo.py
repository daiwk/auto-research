"""Gibbs-Gap Policy Optimization (2610.20814v1), direct and clipped branches.

Behavior determines sampled groups; reference determines the adjusted rewards.
They are deliberately distinct roles, and neither is a learner importance weight.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import math
import torch
from torch import Tensor, nn


def _validate(current: Tensor, reference: Tensor, rewards: Tensor, mask: Tensor, beta: float):
    if current.ndim != 3 or current.shape != reference.shape or mask.shape != current.shape:
        raise ValueError("expected [groups,responses,tokens] current/reference/mask")
    if rewards.shape != current.shape[:-1] or current.shape[1] < 2 or beta <= 0:
        raise ValueError("at least two responses, matching rewards and positive beta required")
    if mask.dtype != torch.bool or not mask.any(-1).all():
        raise ValueError("each response requires a nonempty boolean token mask")
    if not all(torch.isfinite(x).all() for x in (current, reference, rewards)):
        raise ValueError("finite scores and rewards required")


def ggpo_loss(current_logp: Tensor, reference_logp: Tensor, rewards: Tensor,
              token_mask: Tensor, *, beta: float = .01, mixed_only: bool = True,
              normalize: bool = True) -> tuple[Tensor, dict]:
    """Stable raw LME gap with direct autograd; Eq. 6 and Eq. 11 normalization."""
    _validate(current_logp, reference_logp, rewards, token_mask, beta)
    m = current_logp.shape[1]
    selected = torch.ones(rewards.shape[0], dtype=torch.bool, device=rewards.device)
    if mixed_only:
        if not ((rewards == 0) | (rewards == 1)).all():
            raise ValueError("mixed-reward filtering is defined for binary verifier rewards")
        selected = (rewards.sum(-1) > 0) & (rewards.sum(-1) < m)
    sequence_lp = current_logp.masked_fill(~token_mask, 0).sum(-1)
    reference_lp = reference_logp.detach().masked_fill(~token_mask, 0).sum(-1)
    adjusted = rewards.detach() - beta * (sequence_lp - reference_lp)
    # Center before logsumexp: translation invariant and stable even for very
    # large common offsets. This is not a detached-coefficient PG surrogate.
    centered = (adjusted - adjusted.mean(-1, keepdim=True)) / beta
    gaps = beta * (torch.logsumexp(centered, -1) - math.log(m))
    if not selected.any():
        return current_logp.sum() * 0, {"retained_groups": 0, "raw_gap": 0., "mean_length": 0.}
    mean_length = token_mask[selected].sum(-1).float().mean().detach()
    raw = gaps[selected].mean()
    loss = raw / (beta * mean_length * math.sqrt(m - 1)) if normalize else raw
    return loss, {"retained_groups": int(selected.sum()), "raw_gap": float(raw.detach()),
        "mean_length": float(mean_length), "branch": "direct_autograd"}


def clipped_coefficient_surrogate(current_logp: Tensor, reference_logp: Tensor,
                                  rewards: Tensor, token_mask: Tensor, *, beta: float = .01,
                                  clipping_radius: float = .05) -> tuple[Tensor, dict]:
    """Appendix E: clipped reference correction, *unclipped* score gradients.

    This is a separate optional update, not differentiation through a clamp/LME.
    """
    _validate(current_logp, reference_logp, rewards, token_mask, beta)
    if clipping_radius <= 0:
        raise ValueError("positive clipping radius required")
    m = current_logp.shape[1]
    with torch.no_grad():
        correction = (current_logp - reference_logp).clamp(-clipping_radius, clipping_radius)
        adjusted = rewards - beta * correction.masked_fill(~token_mask, 0).sum(-1)
        coefficients = (m * (adjusted / beta).softmax(-1) - 1) / math.sqrt(m - 1)
    sequence_lp = current_logp.masked_fill(~token_mask, 0).sum(-1)
    loss = -(coefficients.detach() * sequence_lp).sum() / token_mask.sum()
    return loss, {"branch": "clipped_detached_coefficient", "valid_tokens": int(token_mask.sum())}


@dataclass
class GGPOPolicies:
    """Explicit frozen behavior collection and periodic reference-refresh state."""
    reference: nn.Module
    behavior: nn.Module
    refresh_interval: int
    updates: int = 0
    reference_refreshes: int = 0
    behavior_syncs: int = 0

    @classmethod
    def from_learner(cls, learner: nn.Module, *, refresh_interval: int = 160):
        if refresh_interval < 1:
            raise ValueError("positive reference refresh interval required")
        reference = deepcopy(learner).eval().requires_grad_(False)
        behavior = deepcopy(learner).eval().requires_grad_(False)
        return cls(reference, behavior, refresh_interval)

    @torch.no_grad()
    def sync_behavior(self, learner: nn.Module):
        self.behavior.load_state_dict(learner.state_dict())
        self.behavior.eval().requires_grad_(False)
        self.behavior_syncs += 1

    @torch.no_grad()
    def after_optimizer_step(self, learner: nn.Module) -> bool:
        self.updates += 1
        if self.updates % self.refresh_interval:
            return False
        self.reference.load_state_dict(learner.state_dict())
        self.reference.eval().requires_grad_(False)
        self.reference_refreshes += 1
        # No behavior synchronization here: already collected data remain fixed.
        return True
