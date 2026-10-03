"""Recommendation mechanisms selected from the 2026-10-03 intake."""

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


def agent_web_evidence(
    semantic_scores,
    temporal_ages,
    *,
    semantic_weight: float,
    memory_budget: int,
    confidence: float,
    confidence_threshold: float,
    collaborator_patterns=(),
    temporal_decay: float = .1,
):
    """Retrieve private evidence and gate AgentWebRec collaboration."""
    import torch

    if not 0 <= semantic_weight <= 1 or memory_budget <= 0:
        raise ValueError("invalid retrieval parameters")
    combined = semantic_weight * semantic_scores + (1 - semantic_weight) * torch.exp(
        -temporal_decay * temporal_ages
    )
    chosen = torch.topk(combined, min(memory_budget, combined.numel())).indices
    collaborate = confidence < confidence_threshold
    patterns = tuple(collaborator_patterns) if collaborate else ()
    return chosen, patterns, {
        "collaboration_activated": collaborate,
        "private_records_exposed": 0,
        "patterns_fused": len(patterns),
    }
