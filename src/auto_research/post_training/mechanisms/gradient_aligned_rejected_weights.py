"""Extracted unchanged from auto_research.post_training.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def gradient_aligned_rejected_weights(rejected_gradients, preferred_direction):
    """Down-weight rejected tokens whose update conflicts with preferred behavior."""
    import torch.nn.functional as F

    alignment = F.cosine_similarity(rejected_gradients, preferred_direction.unsqueeze(0), dim=-1)
    return (1 - alignment.clamp(min=0, max=1)).detach()
