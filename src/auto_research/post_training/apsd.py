"""APSD reverse KL to a student-dependent asymmetric product-of-experts target.

Only the feedback-conditioned self-teacher is detached. Detaching the complete
target would remove the paper's defining student-target gradient coupling.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor


def asymmetric_self_distillation_loss(student_logits: Tensor, self_teacher_logits: Tensor,
                                     correct: Tensor, actor_mask: Tensor,
                                     *, correct_alpha: float = .5,
                                     incorrect_alpha: float = 1.5) -> tuple[Tensor, dict]:
    """Equation 5: sum over response positions, mean over rollout instances.

    self_teacher_logits must come from the same underlying current policy with
    training-only feedback; this operator cannot itself verify model identity.
    Sampled contexts, feedback and correctness are fixed during differentiation.
    """
    if student_logits.ndim != 3 or student_logits.shape != self_teacher_logits.shape or min(student_logits.shape) < 1:
        raise ValueError("aligned nonempty [rollout,token,vocabulary] logits required")
    if not student_logits.is_floating_point() or self_teacher_logits.dtype != student_logits.dtype or self_teacher_logits.device != student_logits.device:
        raise ValueError("floating student/self-teacher logits need matching dtype/device")
    if actor_mask.shape != student_logits.shape[:2] or actor_mask.dtype != torch.bool or not bool(actor_mask.any(1).all()):
        raise ValueError("nonempty Boolean actor masks required")
    if correct.shape != (student_logits.shape[0],) or correct.dtype != torch.bool:
        raise ValueError("one Boolean correctness observation per rollout required")
    if actor_mask.device != student_logits.device or correct.device != student_logits.device:
        raise ValueError("all APSD inputs must share a device")
    if not torch.isfinite(student_logits[actor_mask]).all() or not torch.isfinite(self_teacher_logits[actor_mask]).all():
        raise ValueError("finite active logits required")
    if not math.isfinite(correct_alpha + incorrect_alpha) or not 0 <= correct_alpha <= 1 or incorrect_alpha < 1:
        raise ValueError("0<=correct alpha<=1 and incorrect alpha>=1 required; 0/1 are reference cases")
    if student_logits.dtype in (torch.float16, torch.bfloat16):
        student_logits, self_teacher_logits = student_logits.float(), self_teacher_logits.float()
    active = actor_mask[..., None]
    student = torch.where(active, student_logits, 0.).log_softmax(-1)
    teacher = torch.where(active, self_teacher_logits.detach(), 0.).log_softmax(-1)
    if not torch.isfinite(student[actor_mask]).all() or not torch.isfinite(teacher[actor_mask]).all():
        raise ValueError("active log probabilities are not representable")
    alpha = torch.where(correct, student.new_tensor(correct_alpha), student.new_tensor(incorrect_alpha))[:, None, None]
    target = ((1 - alpha) * student + alpha * teacher).log_softmax(-1)
    if not torch.isfinite(target[actor_mask]).all():
        raise ValueError("asymmetric target is not representable")
    # Intentionally no target.detach(): the normalizer also depends on student.
    token_loss = (student.exp() * (student - target)).sum(-1)
    loss = torch.where(actor_mask, token_loss, 0.).sum(1).mean()
    return loss, {"target_log_probs": target, "alpha": alpha.detach().flatten(),
                  "token_reverse_kl": token_loss.detach()}
