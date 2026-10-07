"""Extracted unchanged from auto_research.recommendation_latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def gear_collision_rerank(context, item_embeddings, token_ids):
    """Context-conditioned reranking of items sharing generated token IDs."""
    import torch

    if item_embeddings.shape[0] != len(token_ids):
        raise ValueError("one token ID is required per item")
    scores = item_embeddings @ context
    groups = {}
    for index, token_id in enumerate(token_ids):
        groups.setdefault(tuple(token_id), []).append(index)
    ranked = []
    for token_id, members in groups.items():
        ranked.extend(sorted(members, key=lambda index: float(scores[index]), reverse=True))
    return torch.as_tensor(ranked, device=item_embeddings.device), scores
