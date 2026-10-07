"""Extracted unchanged from auto_research.foundation_latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def veto_compress(video_tokens, *, spatial_keep: int, temporal_keep: int):
    """VETO spatial-first token merging followed by frame-level merging."""
    import torch
    import torch.nn.functional as F

    if video_tokens.ndim != 3:
        raise ValueError("video tokens must have [frames, spatial_tokens, dim]")
    frames, tokens, _ = video_tokens.shape
    if not 0 < spatial_keep <= tokens or not 0 < temporal_keep <= frames:
        raise ValueError("invalid VETO budgets")
    # Deterministic farthest-point representatives approximate OT matching.
    representatives = [0]
    normalized = F.normalize(video_tokens, dim=-1)
    while len(representatives) < spatial_keep:
        similarity = normalized @ normalized[:, representatives].transpose(1, 2)
        distance = 1 - similarity.max(-1).values.mean(0)
        representatives.append(int(distance.argmax()))
    spatial = video_tokens[:, representatives]
    frame_repr = F.normalize(spatial.mean(1), dim=-1)
    selected = [0]
    while len(selected) < temporal_keep:
        distance = 1 - (frame_repr @ frame_repr[selected].T).max(-1).values
        distance[selected] = -1
        selected.append(int(distance.argmax()))
    return spatial[selected], {
        "spatial_indices": tuple(representatives),
        "frame_indices": tuple(selected),
        "compression_ratio": spatial_keep * temporal_keep / (tokens * frames),
    }
