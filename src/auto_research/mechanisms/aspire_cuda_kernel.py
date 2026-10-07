"""Extracted unchanged from auto_research.foundation_latest_20260919; stable mechanism boundary."""
from __future__ import annotations



def aspire_cuda_kernel(acceptance, draft_cost, verify_cost, batch_sizes, refresh_interval=4):
    import torch
    if any(t.device.type != "cuda" for t in (acceptance, batch_sizes)):
        raise ValueError("aspire_cuda_kernel requires CUDA tensors")
    gain = acceptance * verify_cost - draft_cost * (1 + 0.1 * batch_sizes)
    lengths = torch.clamp(torch.floor(1 + 7 * torch.clamp(gain / verify_cost, 0, 1)), min=1).long()
    refresh = torch.arange(len(lengths), device=lengths.device) % refresh_interval == 0
    return lengths, refresh
