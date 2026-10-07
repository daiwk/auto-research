"""Extracted unchanged from auto_research.foundation_latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def lift_topk_state(logits, *, k: int, temperature: float = 1.0):
    """LIFT Eq. (4): sparse next-token distribution used as feedback state."""
    import torch

    if logits.ndim < 2 or not 0 < k <= logits.shape[-1] or temperature <= 0:
        raise ValueError("invalid logits, k, or temperature")
    values, indices = torch.topk(logits, k, dim=-1)
    probabilities = torch.softmax(values / temperature, dim=-1)
    return torch.zeros_like(logits).scatter(-1, indices, probabilities)

def lift_loss(student_logits, teacher_logits, target_ids, *, state_weight: float = 1.0, k: int = 8):
    """LIFT Eq. (6): next-token CE plus forward KL on teacher top-k states."""
    import torch
    import torch.nn.functional as F

    if student_logits.shape != teacher_logits.shape or target_ids.shape != student_logits.shape[:-1]:
        raise ValueError("logit and target shapes do not align")
    ce = F.cross_entropy(student_logits.reshape(-1, student_logits.shape[-1]), target_ids.reshape(-1))
    teacher_state = lift_topk_state(teacher_logits.detach(), k=k)
    state_kl = (teacher_state * (teacher_state.clamp_min(1e-12).log() - F.log_softmax(student_logits, -1))).sum(-1).mean()
    return ce + state_weight * state_kl, {"token_ce": float(ce.detach()), "state_kl": float(state_kl.detach())}
