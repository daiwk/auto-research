"""CCE-OPD (2610.21195v1), provided condition masks, dual frozen teacher views.

No semantic condition extractor is implemented or implied by this component.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
import torch
from torch import Tensor


@dataclass(frozen=True)
class ConditionPair:
    complete: str
    masked: str
    condition_span: tuple[int, int]
    semantic_reviewed: bool

    @classmethod
    def from_reviewed_span(cls, question: str, span: tuple[int, int], *, semantic_reviewed: bool):
        start, end = span
        if not semantic_reviewed or not 0 <= start < end <= len(question):
            raise ValueError("an externally reviewed exact condition span is required")
        if not question[:start].strip() and not question[end:].strip():
            raise ValueError("mask must preserve an identifiable request")
        return cls(question, question[:start] + "[MASKED]" + question[end:], span, True)


@torch.no_grad()
def score_teacher_views(score: Callable[[str, Tensor], Tensor], pair: ConditionPair,
                         student_prefix: Tensor) -> tuple[Tensor, Tensor]:
    """Both teacher calls receive the exact same generated response prefix."""
    if not pair.semantic_reviewed:
        raise ValueError("mask semantic validity must be supplied, not inferred")
    original = student_prefix.detach().clone()
    full = score(pair.complete, student_prefix).detach()
    masked = score(pair.masked, student_prefix).detach()
    if not torch.equal(student_prefix, original):
        raise ValueError("teacher scorer modified the student prefix")
    if full.shape != masked.shape:
        raise ValueError("teacher views must share vocabulary and token positions")
    return full, masked


@dataclass(frozen=True)
class CCECredit:
    target_probabilities: Tensor
    target_log_probabilities: Tensor
    support: Tensor
    teacher_entropy: Tensor
    auxiliary_mask: Tensor
    valid_mask: Tensor
    old_sample_logp: Tensor
    sampled_advantages: Tensor


@torch.no_grad()
def prepare_credit(old_logits: Tensor, full_teacher_logits: Tensor, masked_teacher_logits: Tensor,
                   sampled_ids: Tensor, valid_mask: Tensor, accepted_mask: Tensor, *,
                   top_k: int = 16, extrapolation: float = .2, contrast_clip: float = 5.,
                   entropy_threshold: float = .8) -> CCECredit:
    if old_logits.shape != full_teacher_logits.shape or old_logits.shape != masked_teacher_logits.shape:
        raise ValueError("same-prefix full vocabulary logits required")
    if valid_mask.shape != old_logits.shape[:-1] or sampled_ids.shape != valid_mask.shape:
        raise ValueError("sample and mask shape mismatch")
    if valid_mask.dtype != torch.bool or accepted_mask.dtype != torch.bool:
        raise ValueError("boolean valid and accepted-pair masks required")
    if accepted_mask.shape == valid_mask.shape[:-1]:
        accepted_mask = accepted_mask.unsqueeze(-1).expand_as(valid_mask)
    if accepted_mask.shape != valid_mask.shape:
        raise ValueError("accepted-pair mask must broadcast only over response positions")
    if not 1 <= top_k <= old_logits.shape[-1] or extrapolation < 0 or contrast_clip <= 0:
        raise ValueError("invalid extrapolation configuration")
    old = old_logits.log_softmax(-1)
    full, masked = full_teacher_logits.log_softmax(-1), masked_teacher_logits.log_softmax(-1)
    support = torch.zeros_like(full, dtype=torch.bool)
    support.scatter_(-1, full.topk(top_k, -1).indices, True)
    support.scatter_(-1, masked.topk(top_k, -1).indices, True)
    contrast = (full - masked).clamp(-contrast_clip, contrast_clip)
    target_logits = (full + extrapolation * contrast).masked_fill(~support, -torch.inf)
    target_lp = target_logits.log_softmax(-1)
    target_prob = target_lp.exp()
    # Store zero rather than -inf outside support: 0*(-inf) must not poison KL.
    target_lp = target_lp.masked_fill(~support, 0)
    entropy = -(full.exp() * full).sum(-1)
    aux_mask = valid_mask & accepted_mask & (entropy >= entropy_threshold)
    old_sample = old.gather(-1, sampled_ids.unsqueeze(-1)).squeeze(-1)
    teacher_sample = full.gather(-1, sampled_ids.unsqueeze(-1)).squeeze(-1)
    return CCECredit(target_prob, target_lp, support, entropy, aux_mask, valid_mask.clone(),
                     old_sample, (teacher_sample - old_sample).detach())


def cce_ppo_loss(current_logits: Tensor, sampled_ids: Tensor, credit: CCECredit, *,
                 clip_epsilon: float = .2, auxiliary_weight: float = 1.) -> tuple[Tensor, dict]:
    """Original sampled PPO-OPD at all valid tokens, plus entropy-gated FKL.

    q_E is support-normalized; p_theta remains full-vocabulary. Both objectives
    divide by *all* valid response tokens, not the selected-token count.
    """
    if not 0 < clip_epsilon < 1 or auxiliary_weight < 0:
        raise ValueError("invalid PPO configuration")
    lp = current_logits.log_softmax(-1)
    sampled = lp.gather(-1, sampled_ids.unsqueeze(-1)).squeeze(-1)
    ratio = (sampled - credit.old_sample_logp.detach()).exp()
    advantage = credit.sampled_advantages.detach()
    surrogate = torch.minimum(ratio * advantage, ratio.clamp(1 - clip_epsilon, 1 + clip_epsilon) * advantage)
    fkl = (credit.target_probabilities.detach() * (credit.target_log_probabilities.detach() - lp)).sum(-1)
    count = credit.valid_mask.sum().clamp_min(1)
    opd = -surrogate.masked_fill(~credit.valid_mask, 0).sum() / count
    auxiliary = fkl.masked_fill(~credit.auxiliary_mask, 0).sum() / count
    return opd + auxiliary_weight * auxiliary, {"opd_loss": float(opd.detach()),
        "auxiliary_loss": float(auxiliary.detach()), "valid_tokens": int(credit.valid_mask.sum()),
        "auxiliary_tokens": int(credit.auxiliary_mask.sum()),
        "max_union_size": int(credit.support.sum(-1).max())}
