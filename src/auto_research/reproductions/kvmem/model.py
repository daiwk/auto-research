"""Query-conditioned paged KV workspace selection from arXiv:2609.04852."""

from __future__ import annotations


def select_workspace_blocks(keys, query, *, block_size: int, selected_blocks: int):
    import torch

    if keys.ndim != 2 or query.ndim != 1 or keys.shape[1] != query.shape[0]:
        raise ValueError("keys must be [tokens, dim] and query [dim]")
    if block_size < 1 or selected_blocks < 1:
        raise ValueError("block_size and selected_blocks must be positive")
    block_count = (len(keys) + block_size - 1) // block_size
    summaries = torch.stack([
        keys[start:min(start + block_size, len(keys))].float().mean(0)
        for start in range(0, len(keys), block_size)
    ])
    scores = torch.nn.functional.normalize(summaries, dim=-1) @ torch.nn.functional.normalize(query.float(), dim=0)
    chosen = torch.topk(scores, min(selected_blocks, block_count)).indices
    indices = [
        torch.arange(int(block) * block_size, min((int(block) + 1) * block_size, len(keys)), device=keys.device)
        for block in chosen
    ]
    return torch.sort(torch.cat(indices)).values, chosen, scores
