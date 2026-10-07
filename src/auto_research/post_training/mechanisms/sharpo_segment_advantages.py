"""Extracted unchanged from auto_research.post_training.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def sharpo_segment_advantages(base_advantage, teacher_log_probs, student_log_probs, segments):
    """Apply a bounded teacher-student multiplier to each interaction segment."""
    import torch

    result = torch.empty_like(student_log_probs)
    for start, end in segments:
        gap = (teacher_log_probs[start:end] - student_log_probs[start:end]).mean().detach()
        result[start:end] = base_advantage * (2 * torch.sigmoid(gap))
    return result
