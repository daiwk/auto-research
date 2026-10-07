"""Extracted unchanged from auto_research.foundation_latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations



def echo_cuda_kernel(early_logits, final_logits, top_k: int = 8):
    """CUDA-compatible ECHO bonus-logit union using torch tensors."""
    import torch

    if early_logits.device.type != "cuda" or final_logits.device.type != "cuda":
        raise ValueError("echo_cuda_kernel requires CUDA tensors")
    k = max(1, min(int(top_k), early_logits.numel()))
    early_bonus = early_logits + torch.relu(final_logits - early_logits)
    final_bonus = final_logits + torch.relu(early_logits - final_logits)
    candidates = torch.unique(torch.cat((torch.topk(early_bonus, k).indices, torch.topk(final_bonus, k).indices)))
    return candidates, early_bonus, final_bonus
