"""Extracted unchanged from auto_research.recommendation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations



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
