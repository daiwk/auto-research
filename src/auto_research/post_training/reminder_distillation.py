"""OPRD (2610.21496v1): scoped teacher contexts and outcome-routed loss.

This module implements a bounded training operator, not a coding-agent harness.
Reminders are training-only inputs to the teacher. Student-generated assistant
prefixes are identical in both branches; tool/history tokens are never targets.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import math

import torch
from torch import Tensor, nn


@dataclass(frozen=True)
class AssistantTurn:
    history: tuple[int, ...]
    response: tuple[int, ...]

    def __post_init__(self):
        if not self.history or not self.response:
            raise ValueError("nonempty reminder-free history and assistant response required")
        if any(not isinstance(v, int) or v < 0 for v in self.history + self.response):
            raise ValueError("token IDs must be nonnegative integers")


@dataclass(frozen=True)
class ScopedReminders:
    global_tokens: tuple[int, ...] = ()
    # Zero-based observation k follows assistant turn k; its reminder applies to k+1.
    local_by_observation: tuple[tuple[int, tuple[int, ...]], ...] = ()

    def __post_init__(self):
        indices = [index for index, _ in self.local_by_observation]
        if len(set(indices)) != len(indices) or any(i < 0 for i in indices):
            raise ValueError("local observation indices must be distinct and nonnegative")
        tokens = self.global_tokens + tuple(v for _, values in self.local_by_observation for v in values)
        if any(not isinstance(v, int) or v < 0 for v in tokens):
            raise ValueError("reminder token IDs must be nonnegative integers")
        if any(not values for _, values in self.local_by_observation):
            raise ValueError("a local reminder must have tokens")

    def active(self, turn_index: int) -> tuple[int, ...]:
        if turn_index < 0:
            raise ValueError("turn index must be nonnegative")
        local = dict(self.local_by_observation).get(turn_index - 1, ())
        return self.global_tokens + local


def contexts_for_turn(turn: AssistantTurn, reminders: ScopedReminders,
                      turn_index: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Contexts before this turn; callers must keep reminder-free histories.

    Each context is rebuilt from the original history. A turn-local reminder
    cannot leak into the next turn by being appended to a persistent transcript.
    """
    return turn.history, turn.history + reminders.active(turn_index)


def score_trajectory(student: nn.Module, teacher: nn.Module,
                     turns: tuple[AssistantTurn, ...], reminders: ScopedReminders,
                     *, device: str | torch.device) -> tuple[Tensor, Tensor, Tensor]:
    """Teacher-force the exact same assistant tokens, with teacher-only scope.

    Models return (batch, prefix length, vocabulary) causal next-token logits.
    This API, rather than caller-supplied unrelated teacher logits, enforces the
    shared-prefix protocol. Only the student branch retains an autograd graph.
    """
    if not turns or student is teacher:
        raise ValueError("nonempty turns and a separate teacher snapshot required")
    student_storage = {(str(p.device), p.untyped_storage().data_ptr()) for p in student.parameters() if p.numel()}
    teacher_storage = {(str(p.device), p.untyped_storage().data_ptr()) for p in teacher.parameters() if p.numel()}
    if student_storage & teacher_storage:
        raise ValueError("teacher snapshot must not share parameter storage with student")
    if any(index >= len(turns) - 1 for index, _ in reminders.local_by_observation):
        raise ValueError("local reminders must anchor an observation with a following turn")
    current, privileged, labels = [], [], []
    previous_mode = teacher.training
    teacher.eval()
    try:
        for index, turn in enumerate(turns):
            plain, augmented = contexts_for_turn(turn, reminders, index)
            student_ids = torch.tensor([plain + turn.response[:-1]], device=device, dtype=torch.long)
            teacher_ids = torch.tensor([augmented + turn.response[:-1]], device=device, dtype=torch.long)
            student_scores = student(student_ids)
            with torch.no_grad():
                teacher_scores = teacher(teacher_ids)
            for scores, ids in ((student_scores, student_ids), (teacher_scores, teacher_ids)):
                if not isinstance(scores, Tensor) or scores.ndim != 3 or scores.shape[:2] != ids.shape:
                    raise ValueError("model must return causal next-token logits (1, sequence, vocabulary)")
            if student_scores.shape[-1] != teacher_scores.shape[-1]:
                raise ValueError("teacher and student must share a vocabulary")
            start_s, start_t = len(plain) - 1, len(augmented) - 1
            current.append(student_scores[0, start_s:start_s + len(turn.response)])
            privileged.append(teacher_scores[0, start_t:start_t + len(turn.response)].detach())
            labels.append(torch.tensor(turn.response, device=device, dtype=torch.long))
    finally:
        teacher.train(previous_mode)
    return torch.cat(current), torch.cat(privileged), torch.cat(labels)


def _safe_logits(logits: Tensor, mask: Tensor) -> Tensor:
    if logits.ndim != 3 or mask.shape != logits.shape[:-1] or mask.dtype != torch.bool:
        raise ValueError("logits (B,T,V) and matching boolean mask required")
    if not logits.is_floating_point() or logits.shape[-1] < 2:
        raise ValueError("floating-point logits and at least two vocabulary entries required")
    if not torch.isfinite(logits[mask]).all():
        raise ValueError("valid logits must be finite")
    return logits.masked_fill(~mask.unsqueeze(-1), 0)


def shared_support_reverse_kl(student_logits: Tensor, teacher_logits: Tensor,
                              mask: Tensor, *, top_k: int = 100,
                              temperature: float = 1.) -> tuple[Tensor, Tensor]:
    """Appendix B: max(log p_s,log p_t) shared support, then renormalize both.

    Returns per-token reverse KL including T^2 and selected indices. Support
    selection and teacher probabilities stop gradient. Padding is sanitized
    before softmax, so masked NaNs cannot poison backward.
    """
    if student_logits.shape != teacher_logits.shape:
        raise ValueError("teacher and student score shapes must agree")
    if not isinstance(top_k, int) or not 1 <= top_k <= student_logits.shape[-1]:
        raise ValueError("top_k must fit the shared vocabulary")
    if not math.isfinite(temperature) or temperature <= 0 or temperature > math.sqrt(torch.finfo(student_logits.dtype).max):
        raise ValueError("positive finite temperature required")
    student = _safe_logits(student_logits, mask) / temperature
    teacher = _safe_logits(teacher_logits.detach(), mask) / temperature
    if not torch.isfinite(student[mask]).all() or not torch.isfinite(teacher[mask]).all():
        raise ValueError("temperature-scaled logits must remain representable")
    with torch.no_grad():
        score = torch.maximum(student.detach().log_softmax(-1), teacher.log_softmax(-1))
        indices = score.topk(top_k, dim=-1).indices
    log_s = student.gather(-1, indices).log_softmax(-1)
    log_t = teacher.gather(-1, indices).log_softmax(-1)
    values = (log_s.exp() * (log_s - log_t)).sum(-1) * temperature ** 2
    return values.masked_fill(~mask, 0), indices.detach()


def outcome_routed_loss(student_logits: Tensor, teacher_logits: Tensor, labels: Tensor,
                        assistant_mask: Tensor, successful: Tensor, *, top_k: int = 100,
                        temperature: float = 1., success_weight: float = 1.,
                        failure_weight: float = 1.) -> tuple[Tensor, dict[str, Tensor]]:
    """Eqs. 6,9,10: token mean per trajectory, then mean within each outcome.

    Success uses only autoregressive NLL; failure uses only detached teacher KL.
    An absent branch contributes zero, not NaN. No tool/prompt/padding target is
    admitted; labels at excluded positions may be -1.
    """
    if labels.shape != assistant_mask.shape or labels.dtype != torch.long:
        raise ValueError("matching long labels and assistant mask required")
    if successful.shape != (student_logits.shape[0],) or successful.dtype != torch.bool:
        raise ValueError("one boolean verified outcome per trajectory required")
    if not all(math.isfinite(w) and w >= 0 for w in (success_weight, failure_weight)):
        raise ValueError("finite nonnegative branch weights required")
    current = _safe_logits(student_logits, assistant_mask)
    if teacher_logits.shape != student_logits.shape or not assistant_mask.any(-1).all():
        raise ValueError("matching teacher shape and nonempty assistant tokens per trajectory required")
    if ((labels[assistant_mask] < 0) | (labels[assistant_mask] >= current.shape[-1])).any():
        raise ValueError("valid labels must be in vocabulary")
    safe_labels = labels.masked_fill(~assistant_mask, 0)
    success_mask = assistant_mask & successful[:, None]
    failure_mask = assistant_mask & ~successful[:, None]
    logp = current.log_softmax(-1).gather(-1, safe_labels.unsqueeze(-1)).squeeze(-1)
    per_trajectory_nll = -logp.masked_fill(~success_mask, 0).sum(-1) / assistant_mask.sum(-1)
    kl, _ = shared_support_reverse_kl(current, teacher_logits, failure_mask,
                                     top_k=top_k, temperature=temperature)
    per_trajectory_kl = kl.sum(-1) / assistant_mask.sum(-1)
    zero = current.sum() * 0
    nll = per_trajectory_nll[successful].mean() if successful.any() else zero
    distill = per_trajectory_kl[~successful].mean() if (~successful).any() else zero
    total = success_weight * nll + failure_weight * distill
    if not torch.isfinite(total):
        raise ValueError("nonfinite outcome-routed objective")
    return total, {
        "success_nll": nll.detach(), "failure_reverse_kl": distill.detach(),
        "successful_trajectories": successful.sum().detach(),
        "failed_trajectories": (~successful).sum().detach()}


class RefreshingTeacher:
    """Frozen student snapshots refreshed after crossing 20/40/60/80% updates."""

    def __init__(self, student: nn.Module, total_updates: int):
        if total_updates < 1:
            raise ValueError("positive update budget required")
        self.model = deepcopy(student).eval().requires_grad_(False)
        self.total_updates = total_updates
        self.thresholds = tuple(math.ceil(total_updates * f) for f in (.2, .4, .6, .8))
        self.completed_updates = 0
        self.refresh_count = 0

    def after_update(self, student: nn.Module, completed_updates: int) -> int:
        if not self.completed_updates < completed_updates <= self.total_updates:
            raise ValueError("teacher refresh progress must increase within the fixed budget")
        crossed = sum(self.completed_updates < t <= completed_updates for t in self.thresholds)
        if crossed:
            self.model.load_state_dict(student.state_dict())
            self.model.eval().requires_grad_(False)
            self.refresh_count += crossed
        self.completed_updates = completed_updates
        return crossed
