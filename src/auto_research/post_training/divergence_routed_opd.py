"""DrOPD (2610.19572), equations 6--10; not the unrelated Dr. OPD.

The candidate set, routing decisions, teacher and behavior policy are frozen
for a PPO update. Gradients flow only through the current student policy.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch


@dataclass(frozen=True)
class RoutedCandidates:
    indices: torch.Tensor
    support: torch.Tensor
    old_log_probs: torch.Tensor
    teacher_log_probs: torch.Tensor
    response_mask: torch.Tensor
    js: torch.Tensor
    gate: torch.Tensor


def _candidate_log_probs(logits, indices, support):
    selected = logits.float().gather(-1, indices)
    return selected.masked_fill(~support, -torch.inf).log_softmax(-1)


def prepare_routing(student_logits, teacher_logits, response_mask, *, top_k=16, fraction=.2):
    """Freeze top-k union and the Kth-largest valid JS cutoff (Appendix B.1).

    K=round(fraction * valid_positions); K=0 routes nothing. Cutoff ties are
    retained, so the realized routed count may exceed K for tied JS scores.
    """
    if student_logits.shape != teacher_logits.shape or student_logits.ndim < 2:
        raise ValueError("aligned student/teacher vocabulary logits required")
    if response_mask.shape != student_logits.shape[:-1] or response_mask.dtype != torch.bool:
        raise ValueError("boolean response mask must match token positions")
    if not 1 <= top_k <= student_logits.shape[-1] or not 0 < fraction <= 1:
        raise ValueError("invalid candidate count or routing fraction")
    if not bool(response_mask.any()):
        raise ValueError("at least one valid generated response position required")
    if not torch.isfinite(student_logits).all() or not torch.isfinite(teacher_logits).all():
        raise ValueError("finite model logits required")
    with torch.no_grad():
        student_top = student_logits.topk(top_k, -1).indices
        teacher_top = teacher_logits.topk(top_k, -1).indices
        # Keep fixed-width storage but count a shared token only once.
        unique_teacher = ~(teacher_top.unsqueeze(-1) == student_top.unsqueeze(-2)).any(-1)
        support = torch.cat((torch.ones_like(student_top, dtype=torch.bool), unique_teacher), -1)
        indices = torch.cat((student_top, teacher_top), -1)
        lp = _candidate_log_probs(student_logits.detach(), indices, support)
        lq = _candidate_log_probs(teacher_logits.detach(), indices, support)
        lm = torch.logaddexp(lp, lq) - math.log(2.)
        p, q = lp.exp(), lq.exp()
        dp = torch.where(support, lp - lm, 0.)
        dq = torch.where(support, lq - lm, 0.)
        js = .5 * (p * dp + q * dq).sum(-1)
        scores = js[response_mask]
        selected_count = round(fraction * scores.numel())
        if selected_count == 0:
            gate = torch.zeros_like(response_mask)
        else:
            threshold = scores.topk(selected_count).values[-1]
            gate = (js >= threshold) & response_mask
    return RoutedCandidates(indices, support, lp, lq, response_mask.detach().clone(), js, gate)


def candidate_rewards(routing):
    """Detached candidate advantages, eq. 9, including unsampled teacher modes."""
    p, q = routing.old_log_probs.exp(), routing.teacher_log_probs.exp()
    difference = torch.where(routing.support,
                             routing.old_log_probs - routing.teacher_log_probs, 0.)
    reward = -p * difference + routing.gate.unsqueeze(-1) * q
    return reward.masked_fill(~routing.support, 0.).detach()


def routed_ppo_loss(current_logits, routing, *, clip_epsilon=.2):
    """Actual candidate-summed PPO surrogate, not a static mixed-KL stand-in."""
    if not 0 < clip_epsilon < 1:
        raise ValueError("clip epsilon must lie in (0, 1)")
    if current_logits.shape[:-1] != routing.response_mask.shape:
        raise ValueError("current logits must align with frozen rollout positions")
    if not torch.isfinite(current_logits).all():
        raise ValueError("finite current logits required")
    lp = _candidate_log_probs(current_logits, routing.indices, routing.support)
    log_ratio = torch.where(routing.support, lp - routing.old_log_probs, 0.)
    ratio = log_ratio.exp()
    advantages = candidate_rewards(routing)
    surrogate = torch.minimum(ratio * advantages,
                              ratio.clamp(1. - clip_epsilon, 1. + clip_epsilon) * advantages)
    loss = -surrogate.sum(-1)[routing.response_mask].mean()
    if not torch.isfinite(loss):
        raise FloatingPointError("nonfinite PPO surrogate; abort rather than conceal unstable policy ratios")
    safe_difference = torch.where(routing.support, lp - routing.teacher_log_probs, 0.)
    reverse_kl = (lp.exp() * safe_difference).sum(-1)
    forward_kl = (-routing.teacher_log_probs.exp() * safe_difference).sum(-1)
    diagnostics = {
        "reverse_kl": float(reverse_kl[routing.response_mask].detach().mean()),
        "forward_kl": float(forward_kl[routing.response_mask].detach().mean()),
        "js": float(routing.js[routing.response_mask].mean()),
        "routed_fraction": float(routing.gate[routing.response_mask].float().mean()),
        "mean_unique_candidates": float(routing.support.sum(-1)[routing.response_mask].float().mean()),
        "response_positions": int(routing.response_mask.sum()),
    }
    return loss, diagnostics
