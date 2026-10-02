"""Recommendation and training-fleet mechanisms from the Oct-2 intake."""

from __future__ import annotations


def basis_vq(latents, basis, codebook):
    """GEAR BasisVQ assignment in a shared orthogonal coordinate system."""
    import torch

    if basis.ndim != 2 or codebook.ndim != 2 or latents.shape[-1] != basis.shape[0]:
        raise ValueError("incompatible BasisVQ shapes")
    rotated = latents @ basis
    distances = torch.cdist(rotated, codebook)
    indices = distances.argmin(-1)
    quantized = codebook[indices] @ basis.T
    return quantized, indices


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


def effective_training_time(timeline):
    """Meta ETT% and independently owned lifecycle-loss accounting."""
    total = sum(float(duration) for duration in timeline.values())
    if total <= 0 or "training" not in timeline:
        raise ValueError("timeline requires positive training and wall time")
    losses = {stage: float(value) / total for stage, value in timeline.items() if stage != "training"}
    return float(timeline["training"]) / total, losses


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


def repair_preference_state(state, cached_states, query, *, top_k: int):
    """REPAIR cached-evidence selection and residual state correction."""
    import torch

    if cached_states.ndim != 2 or state.ndim != 1 or query.shape != state.shape:
        raise ValueError("invalid REPAIR states")
    scores = cached_states @ query - cached_states @ state
    chosen = scores.topk(min(top_k, len(scores))).indices
    weights = torch.softmax(scores[chosen], dim=0)
    correction = (weights[:, None] * cached_states[chosen]).sum(0) - state
    return state + correction, {"selected_timesteps": chosen, "weights": weights}
