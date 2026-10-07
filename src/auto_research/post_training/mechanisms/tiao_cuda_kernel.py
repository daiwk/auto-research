"""Extracted unchanged from auto_research.post_training.latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations



def tiao_cuda_kernel(full_log_probs, masked_log_probs, advantages, tau: float = 5.0):
    """CUDA-compatible TIAO token dependency and dual-scale credit."""
    import torch

    if any(tensor.device.type != "cuda" for tensor in (full_log_probs, masked_log_probs, advantages)):
        raise ValueError("tiao_cuda_kernel requires CUDA tensors")
    shift = torch.clamp(masked_log_probs - full_log_probs, -tau, tau)
    importance = torch.exp(shift) - shift - 1.0
    trajectory = importance.mean(dim=-1, keepdim=True)
    cutoff = torch.quantile(importance, 0.5, dim=-1, keepdim=True)
    mask = importance >= cutoff
    credit = advantages[:, None] * (1.0 + trajectory) * mask * importance
    return credit, importance, mask
