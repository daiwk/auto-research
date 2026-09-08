"""Beacon-query guided KV selection from arXiv:2609.04971."""

from __future__ import annotations


def farthest_point_beacons(queries, count: int):
    import torch

    if queries.ndim != 2 or not 0 < count <= len(queries):
        raise ValueError("queries must be [tokens, dim] and count must be valid")
    normalized = torch.nn.functional.normalize(queries.float(), dim=-1)
    selected = [int(torch.linalg.vector_norm(normalized, dim=-1).argmax())]
    nearest = 1.0 - normalized @ normalized[selected[0]]
    for _ in range(1, count):
        nearest[selected] = -torch.inf
        index = int(nearest.argmax())
        selected.append(index)
        nearest = torch.minimum(nearest, 1.0 - normalized @ normalized[index])
    return torch.as_tensor(selected, device=queries.device)


def beacon_retained_indices(keys, queries, retained_tokens: int, *, beacon_count: int, recent_tokens: int):
    import torch

    if keys.ndim != 2 or queries.ndim != 2 or keys.shape[1] != queries.shape[1]:
        raise ValueError("keys and queries must be [tokens, dim]")
    if not 0 < recent_tokens <= retained_tokens <= len(keys):
        raise ValueError("invalid retention budget")
    beacons = queries[farthest_point_beacons(queries, min(beacon_count, len(queries)))]
    score = torch.max(
        torch.nn.functional.normalize(keys.float(), dim=-1)
        @ torch.nn.functional.normalize(beacons.float(), dim=-1).T,
        dim=-1,
    ).values
    recent = torch.arange(len(keys) - recent_tokens, len(keys), device=keys.device)
    score[recent] = torch.inf
    return torch.sort(torch.topk(score, retained_tokens, sorted=False).indices).values
