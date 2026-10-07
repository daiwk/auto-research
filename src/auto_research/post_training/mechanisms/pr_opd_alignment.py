"""Extracted unchanged from auto_research.post_training.latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def pr_opd_alignment(student_layers, privileged_layers, response_mask, *, layer_weights=None):
    """PR-OPD hidden-state alignment to a stop-gradient skill-conditioned teacher."""
    import torch

    if len(student_layers) != len(privileged_layers) or not student_layers:
        raise ValueError("student and privileged layer lists must align")
    weights = torch.ones(len(student_layers), device=student_layers[0].device) if layer_weights is None else torch.as_tensor(layer_weights, device=student_layers[0].device)
    weights = weights / weights.sum()
    mask = response_mask.to(student_layers[0].dtype)
    losses = []
    for student, teacher in zip(student_layers, privileged_layers):
        if student.shape != teacher.shape or student.shape[:-1] != response_mask.shape:
            raise ValueError("layer and response-mask shapes do not align")
        cosine = torch.nn.functional.cosine_similarity(student, teacher.detach(), dim=-1)
        losses.append(((1 - cosine) * mask).sum() / mask.sum().clamp_min(1))
    return sum(weight * loss for weight, loss in zip(weights, losses))
