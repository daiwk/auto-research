"""Extracted unchanged from auto_research.foundation_latest_20260919; stable mechanism boundary."""
from __future__ import annotations



def oda_cuda_kernel(query, local_keys, local_values, global_keys, global_values, recall_head, threshold=0.0):
    import torch
    if any(t.device.type != "cuda" for t in (query, local_keys, local_values, global_keys, global_values, recall_head)):
        raise ValueError("oda_cuda_kernel requires CUDA tensors")
    local_weights = torch.softmax(local_keys @ query / query.numel() ** 0.5, dim=0)
    local = local_weights @ local_values
    gate = (local @ recall_head) > threshold
    global_output = torch.softmax(global_keys @ query / query.numel() ** 0.5, dim=0) @ global_values
    return torch.where(gate, global_output, local), gate
