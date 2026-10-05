"""Forward-only output-layer gradient features from LESSER (arXiv:2610.03702).

The hidden states must be treated as fixed with respect to a *copy* of the
readout matrix. This module implements the paper's feature, not its LLM-scale
SFT/RL/teacher-selection experiments.
"""

from __future__ import annotations

import torch
from torch import Tensor


def rademacher_projection(vocabulary: int, hidden: int, left: int, right: int,
                          *, seed: int, device: torch.device | str = "cpu") -> tuple[Tensor, Tensor]:
    """Draw paper Appendix B.2's shared two-sided ±1/sqrt(width) projection."""
    if min(vocabulary, hidden, left, right) <= 0:
        raise ValueError("all projection dimensions must be positive")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    a = torch.randint(0, 2, (left, vocabulary), generator=generator).to(torch.float64)
    b = torch.randint(0, 2, (hidden, right), generator=generator).to(torch.float64)
    return ((a * 2 - 1) / left**0.5).to(device), ((b * 2 - 1) / right**0.5).to(device)


def output_gradient_feature(
    hidden_states: Tensor,
    logits: Tensor,
    targets: Tensor,
    token_weights: Tensor,
    *,
    projection: tuple[Tensor, Tensor] | None = None,
    normalize: bool = True,
) -> Tensor:
    """Compute Σ_t α_t (softmax(W h_t) − onehot(y_t)) h_tᵀ.

    With a projection, compute Π₁ g Π₂ token by token without constructing
    the full vocabulary-by-hidden gradient. Pool and query must share Π₁, Π₂.
    Signed RL advantages are allowed; zero-weight positions are masked.
    """
    if hidden_states.ndim != 2 or logits.ndim != 2:
        raise ValueError("hidden_states and logits must be [tokens, features]")
    tokens, width = hidden_states.shape
    if logits.shape[0] != tokens or targets.shape != (tokens,) or token_weights.shape != (tokens,):
        raise ValueError("token dimensions do not agree")
    if targets.dtype not in (torch.int64, torch.int32, torch.long):
        raise TypeError("targets must be integer token ids")
    vocabulary = logits.shape[1]
    if torch.any((targets < 0) | (targets >= vocabulary)):
        raise ValueError("target outside vocabulary")
    if not bool(torch.isfinite(logits).all() and torch.isfinite(hidden_states).all()
                and torch.isfinite(token_weights).all()):
        raise ValueError("features must be finite")
    residual = logits.softmax(-1).clone()
    residual.scatter_add_(1, targets[:, None].long(), -torch.ones((tokens, 1), device=logits.device, dtype=logits.dtype))
    residual = residual * token_weights[:, None]
    if projection is None:
        feature = residual.T @ hidden_states
    else:
        left, right = projection
        if left.ndim != 2 or right.ndim != 2 or left.shape[1] != vocabulary or right.shape[0] != width:
            raise ValueError("projection shapes do not match vocabulary and hidden width")
        left = left.to(device=logits.device, dtype=logits.dtype)
        right = right.to(device=logits.device, dtype=logits.dtype)
        feature = (left @ residual.T) @ (hidden_states @ right)
    if normalize:
        norm = torch.linalg.vector_norm(feature)
        if not bool(torch.isfinite(norm)) or float(norm) == 0:
            raise ValueError("zero/nonfinite feature cannot be cosine-normalized")
        feature = feature / norm
    return feature.reshape(-1)


def round_robin_select(pool_features: Tensor, query_features: Tensor, budget: int) -> list[int]:
    """Keep the query-wise round-robin selector while replacing only features.

    Stable index tie-breaking and uniqueness make the selected subset auditable.
    Query features must come from a validation/query split, never held-out test.
    """
    if pool_features.ndim != 2 or query_features.ndim != 2 or pool_features.shape[1] != query_features.shape[1]:
        raise ValueError("pool/query features must share [samples, dimension]")
    n, q = pool_features.shape[0], query_features.shape[0]
    if not (0 <= budget <= n) or q == 0:
        raise ValueError("invalid budget or empty query set")
    if not bool(torch.isfinite(pool_features).all() and torch.isfinite(query_features).all()):
        raise ValueError("nonfinite features")
    p = torch.nn.functional.normalize(pool_features, dim=1)
    query = torch.nn.functional.normalize(query_features, dim=1)
    similarities = (query @ p.T).detach().cpu().tolist()
    rankings = [sorted(range(n), key=lambda i: (-row[i], i)) for row in similarities]
    cursors = [0] * q
    selected: list[int] = []
    seen: set[int] = set()
    while len(selected) < budget:
        for j, ranking in enumerate(rankings):
            while cursors[j] < n and ranking[cursors[j]] in seen:
                cursors[j] += 1
            if cursors[j] < n:
                index = ranking[cursors[j]]
                selected.append(index)
                seen.add(index)
                cursors[j] += 1
                if len(selected) == budget:
                    break
    return selected
