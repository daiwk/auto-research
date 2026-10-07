"""Extracted unchanged from auto_research.post_training.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def lego_opd_teacher(language_logits, grounded_logits, *, grounding_strength: float):
    """Compose a language prior with a grounding likelihood factor."""
    import torch

    language_prior = torch.softmax(language_logits.detach(), dim=-1)
    visual_likelihood = torch.softmax(grounded_logits.detach(), dim=-1)
    composed = language_prior * visual_likelihood.pow(grounding_strength)
    return composed / composed.sum(dim=-1, keepdim=True).clamp_min(1e-12)
