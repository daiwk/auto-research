"""SPOD success-preserving action masking and soft probability floor.

This is an L1 objective component, not an Agent environment or a hard guarantee
of preserved task success under shared-parameter optimization.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
import math

import torch
from torch import Tensor


def success_preserving_loss(student_logits: Tensor, teacher_logits: Tensor,
                           sampled_tokens: Tensor, actor_mask: Tensor,
                           episode_ids: Sequence[str], successes: Mapping[str, bool],
                           *, floor: float = .5, floor_weight: float = 1.) -> tuple[Tensor, dict]:
    """Exact full-vocabulary FKL or sequence floor; episode/state/token mean.

    Each row is one complete action, including its end-of-action token. The
    caller supplies untempered model logits, not constrained sampling scores.
    Gate comparisons use current student probabilities and are stop-gradient.
    Observations and padding are excluded by actor_mask.
    """
    if student_logits.ndim != 3 or student_logits.shape != teacher_logits.shape or min(student_logits.shape) < 1:
        raise ValueError("aligned nonempty [action,token,vocabulary] logits required")
    if not student_logits.is_floating_point() or student_logits.dtype != teacher_logits.dtype or student_logits.device != teacher_logits.device:
        raise ValueError("floating logits with matching dtype/device required")
    if actor_mask.shape != student_logits.shape[:2] or actor_mask.dtype != torch.bool or not bool(actor_mask.any(1).all()):
        raise ValueError("each action needs a nonempty Boolean actor mask")
    if sampled_tokens.shape != actor_mask.shape or sampled_tokens.dtype != torch.long:
        raise ValueError("aligned int64 sampled tokens required")
    if actor_mask.device != student_logits.device or sampled_tokens.device != student_logits.device:
        raise ValueError("all action tensors must share a device")
    if not torch.isfinite(student_logits[actor_mask]).all() or not torch.isfinite(teacher_logits[actor_mask]).all():
        raise ValueError("finite active logits required")
    if bool(((sampled_tokens[actor_mask] < 0) | (sampled_tokens[actor_mask] >= student_logits.shape[-1])).any()):
        raise ValueError("sampled actor token outside vocabulary")
    if len(episode_ids) != student_logits.shape[0] or any(not isinstance(i, str) or not i for i in episode_ids):
        raise ValueError("one nonempty episode ID per action required")
    if set(successes) != set(episode_ids) or any(type(v) is not bool for v in successes.values()):
        raise ValueError("exact episode coverage with binary Boolean training outcomes required")
    if not math.isfinite(floor) or not 0 < floor <= 1 or not math.isfinite(floor_weight) or floor_weight < 0:
        raise ValueError("finite 0<floor<=1 and nonnegative floor weight required")
    if student_logits.dtype in (torch.float16, torch.bfloat16):
        student_logits, teacher_logits = student_logits.float(), teacher_logits.float()
    mask = actor_mask[..., None]
    log_student = torch.where(mask, student_logits, 0.).log_softmax(-1)
    log_teacher = torch.where(mask, teacher_logits.detach(), 0.).log_softmax(-1)
    if not torch.isfinite(log_student[actor_mask]).all() or not torch.isfinite(log_teacher[actor_mask]).all():
        raise ValueError("active log probabilities are not representable")
    labels = torch.where(actor_mask, sampled_tokens, 0)[..., None]
    student_sequence = torch.where(actor_mask, log_student.gather(-1, labels).squeeze(-1), 0.).sum(1)
    teacher_sequence = torch.where(actor_mask, log_teacher.gather(-1, labels).squeeze(-1), 0.).sum(1)
    success = torch.tensor([successes[i] for i in episode_ids], dtype=torch.bool, device=actor_mask.device)
    gate = (success & (teacher_sequence < student_sequence.detach())).detach()
    lengths = actor_mask.sum(1)
    token_kl = (log_teacher.exp() * (log_teacher - log_student)).sum(-1)
    action_kl = torch.where(actor_mask, token_kl, 0.).sum(1) / lengths
    action_floor = (math.log(floor) - student_sequence).clamp_min(0) / lengths
    action_loss = torch.where(gate, floor_weight * action_floor, action_kl)
    # Every episode gets equal mass, every sampled state within it equal mass.
    episode_loss = torch.stack([action_loss[[i for i, value in enumerate(episode_ids) if value == episode]].mean()
                                for episode in dict.fromkeys(episode_ids)])
    return episode_loss.mean(), {"gate": gate, "student_sequence_logp": student_sequence.detach(),
        "teacher_sequence_logp": teacher_sequence.detach(), "action_forward_kl": action_kl.detach(),
        "action_floor": action_floor.detach(), "action_loss": action_loss.detach(),
        "episode_loss": episode_loss.detach()}
