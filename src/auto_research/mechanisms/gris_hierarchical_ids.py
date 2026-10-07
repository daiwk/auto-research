"""Extracted unchanged from auto_research.recommendation_latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def gris_hierarchical_ids(semantic_features, adjacency, *, levels: int):
    """Graph-informed recursive binary partition IDs for GrIS."""
    import torch

    features = torch.as_tensor(semantic_features, dtype=torch.float32)
    graph = torch.as_tensor(adjacency, dtype=torch.float32)
    if levels < 1 or graph.shape != (len(features), len(features)):
        raise ValueError("invalid GrIS graph")
    ids = torch.zeros((len(features), levels), dtype=torch.long)
    groups = [torch.arange(len(features))]
    for level in range(levels):
        next_groups = []
        for group in groups:
            if len(group) <= 1:
                next_groups.append(group)
                continue
            smooth = features[group] + graph[group][:, group] @ features[group] / graph[group][:, group].sum(-1, keepdim=True).clamp_min(1)
            direction = smooth[:, 0] - smooth[:, 0].median()
            right = group[direction > 0]
            left = group[direction <= 0]
            if not len(right) or not len(left):
                midpoint = len(group) // 2
                left, right = group[:midpoint], group[midpoint:]
            ids[right, level] = 1
            next_groups.extend((left, right))
        groups = next_groups
    return ids
