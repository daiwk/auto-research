"""Extracted unchanged from auto_research.recommendation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations

import math

def rptune_curate(query_embedding, item_embeddings, learned_adjustment, *, prune_rate: float):
    """Rank, prune and position a catalog as defined by RPTune."""
    import torch
    import torch.nn.functional as F

    if not 0 <= prune_rate < 1:
        raise ValueError("prune_rate must be in [0, 1)")
    query = F.normalize(query_embedding, dim=-1)
    items = F.normalize(item_embeddings, dim=-1)
    if learned_adjustment.shape != (items.shape[0],):
        raise ValueError("one learned adjustment is required per catalog item")
    scores = 10 * (items @ query) + learned_adjustment
    keep = max(1, math.ceil((1 - prune_rate) * items.shape[0]))
    selected = torch.topk(scores, keep).indices
    # RPTune puts the highest-priority item closest to the generation suffix.
    order = selected[torch.argsort(scores[selected])]
    return order, scores
