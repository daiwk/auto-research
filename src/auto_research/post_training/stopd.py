"""STOPD (2610.21337v1): pre-generation cutoff and lagged IPW normalization."""
from __future__ import annotations

from dataclasses import dataclass
import torch
from torch import Tensor


def inclusion_probabilities(max_length: int, block_width: int, *, device=None,
                             dtype=torch.float64) -> Tensor:
    """Exact P(S >= t), including a final partial block and natural EOS positions."""
    if max_length < 1 or block_width < 1:
        raise ValueError("positive length and block width required")
    positions = torch.arange(max_length, device=device)
    return (max_length - block_width * (positions // block_width)).to(dtype) / max_length


def cutoffs_from_anchors(anchors: Tensor, max_length: int, block_width: int) -> Tensor:
    if max_length < 1 or block_width < 1 or anchors.is_floating_point():
        raise ValueError("positive length/block and integer anchors required")
    if not ((anchors >= 0) & (anchors < max_length)).all():
        raise ValueError("anchors must lie in [0,L)")
    return (block_width * (anchors // block_width + 1)).clamp_max(max_length)


@dataclass(frozen=True)
class TruncationPlan:
    step: int
    cutoffs: Tensor
    warmup: bool
    denominator: float | None


class STOPDSchedule:
    """A plan is drawn before generation; normalization advances after the update.

    This two-phase API prevents using this batch's random weighted token count
    as its own denominator, which would destroy the gradient-sum guarantee.
    """
    def __init__(self, max_length: int, block_width: int, warmup_steps: int = 1):
        inclusion_probabilities(max_length, block_width)
        if warmup_steps < 1:
            raise ValueError("at least one Vanilla OPD warmup update required")
        self.max_length, self.block_width, self.warmup_steps = max_length, block_width, warmup_steps
        self.step, self.previous_count, self._active = 0, None, None

    def begin_batch(self, batch_size: int, *, device=None, generator=None) -> TruncationPlan:
        if batch_size < 1 or self._active is not None:
            raise ValueError("positive batch and completed preceding plan required")
        warmup = self.step < self.warmup_steps
        if warmup:
            cutoffs = torch.full((batch_size,), self.max_length, dtype=torch.long, device=device)
        else:
            anchors = torch.randint(self.max_length, (batch_size,), device=device, generator=generator)
            cutoffs = cutoffs_from_anchors(anchors, self.max_length, self.block_width)
        plan = TruncationPlan(self.step, cutoffs, warmup, None if warmup else self.previous_count)
        self._active = plan
        return plan

    def _weights(self, plan: TruncationPlan, mask: Tensor) -> Tensor:
        if plan is not self._active or plan.step != self.step:
            raise ValueError("stale or inactive truncation plan")
        if mask.dtype != torch.bool or mask.ndim != 2 or mask.shape[0] != len(plan.cutoffs):
            raise ValueError("boolean [batch,positions] response mask required")
        if mask.shape[1] > self.max_length or not mask.any(-1).all():
            raise ValueError("each response must contain 1..L generated tokens")
        # Prefix masks retain natural EOS but cannot mark post-EOS padding valid.
        if (mask[:, 1:] & ~mask[:, :-1]).any():
            raise ValueError("response masks must be contiguous prefixes")
        positions = torch.arange(mask.shape[1], device=mask.device)
        if (mask & (positions.unsqueeze(0) >= plan.cutoffs.to(mask.device).unsqueeze(1))).any():
            raise ValueError("generation exceeded the pre-sampled cutoff")
        weights = torch.ones(mask.shape[1], device=mask.device, dtype=torch.float64)
        if not plan.warmup:
            weights = inclusion_probabilities(self.max_length, self.block_width, device=mask.device)[:mask.shape[1]].reciprocal()
        return weights.unsqueeze(0).expand_as(mask).masked_fill(~mask, 0).detach()

    def loss(self, plan: TruncationPlan, token_losses: Tensor, mask: Tensor) -> tuple[Tensor, dict]:
        if token_losses.shape != mask.shape:
            raise ValueError("local loss shape mismatch")
        exact_weights = self._weights(plan, mask)
        weights = exact_weights.to(token_losses)
        denominator = float(mask.sum()) if plan.warmup else plan.denominator
        if denominator is None or denominator <= 0:
            raise ValueError("previous batch normalizer is not initialized")
        loss = (token_losses.masked_fill(~mask, 0) * weights).sum() / denominator
        return loss, {"warmup": plan.warmup, "denominator": denominator,
            "weighted_count_for_next_batch": float(exact_weights.sum()), "retained_tokens": int(mask.sum()),
            "cutoffs": plan.cutoffs.tolist(), "normalizer_source": "current_exact_warmup" if plan.warmup else "previous_batch"}

    def finish_batch(self, plan: TruncationPlan, mask: Tensor) -> None:
        self.previous_count = float(self._weights(plan, mask).sum())
        self.step += 1
        self._active = None


def reverse_kl_token_losses(student_logits: Tensor, teacher_logits: Tensor) -> Tensor:
    """Full-vocabulary local RKL. Teacher feedback never receives gradients."""
    if student_logits.shape != teacher_logits.shape:
        raise ValueError("shared prefix/vocabulary required")
    student_lp = student_logits.log_softmax(-1)
    return (student_lp.exp() * (student_lp - teacher_logits.detach().log_softmax(-1))).sum(-1)
