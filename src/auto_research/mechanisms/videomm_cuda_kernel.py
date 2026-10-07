"""Extracted unchanged from auto_research.foundation_latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations



def videomm_cuda_kernel(tokens, query, group_size: int = 8, keep_groups: int = 4):
    """CUDA-compatible macro-proxy selection and micro-token gather."""
    import torch

    if tokens.device.type != "cuda" or query.device.type != "cuda":
        raise ValueError("videomm_cuda_kernel requires CUDA tensors")
    usable = tokens.shape[0] - tokens.shape[0] % group_size
    macro = tokens[:usable].reshape(-1, group_size, tokens.shape[1]).mean(dim=1)
    scores = torch.nn.functional.cosine_similarity(macro, query.unsqueeze(0), dim=1)
    chosen = torch.topk(scores, min(int(keep_groups), len(macro))).indices
    offsets = torch.arange(group_size, device=tokens.device)
    indices = (chosen[:, None] * group_size + offsets[None, :]).reshape(-1)
    return tokens.index_select(0, indices), indices, scores
