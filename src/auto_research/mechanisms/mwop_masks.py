"""Extracted unchanged from auto_research.foundation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def mwop_masks(attention_importance, visual_ffn_importance, text_ffn_importance, *, keep: int):
    """Create separate modality-path and modality-FFN masks for MWOP."""
    import torch

    if attention_importance.ndim != 2 or attention_importance.shape[-1] != 3:
        raise ValueError("attention importance must be [heads, V2V/T2V/T2T]")
    if keep <= 0:
        raise ValueError("keep must be positive")

    def mask(values):
        result = torch.zeros_like(values, dtype=torch.bool)
        count = min(keep, values.numel())
        result.flatten()[torch.topk(values.flatten(), count).indices] = True
        return result

    return mask(attention_importance), mask(visual_ffn_importance), mask(text_ffn_importance)
