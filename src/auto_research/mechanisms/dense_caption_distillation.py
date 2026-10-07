"""Extracted unchanged from auto_research.foundation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def dense_caption_distillation(student_embeddings, caption_teacher_embeddings):
    """Omni-Embed-Mini cosine distillation into the frozen text geometry."""
    import torch.nn.functional as F

    student = F.normalize(student_embeddings, dim=-1)
    teacher = F.normalize(caption_teacher_embeddings.detach(), dim=-1)
    return (1 - (student * teacher).sum(-1)).mean()
