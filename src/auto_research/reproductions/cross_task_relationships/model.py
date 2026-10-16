"""Trainable marginal/cross-label heads, independent implementation of §2/4/5."""
from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def validate_pair(labels: Tensor) -> dict[str, int]:
    """Screen training labels only: constant, nested and disjoint pairs add no information."""
    if labels.ndim != 2 or labels.shape[1] != 2 or not torch.all((labels == 0) | (labels == 1)):
        raise ValueError("expected a binary N × 2 label matrix")
    counts = {f"{x}{y}": int(((labels[:, 0] == x) & (labels[:, 1] == y)).sum())
              for x in (0, 1) for y in (0, 1)}
    if any(count == 0 for count in counts.values()):
        raise ValueError("pair is constant, nested, mutually exclusive or unsupported in this training slice")
    return counts


def joint_distribution(marginals: Tensor, joint: Tensor) -> tuple[Tensor, Tensor]:
    """Return the raw pairwise table and its feasibility; do not hide invalid estimates."""
    if marginals.shape[-1] != 2 or marginals.shape[:-1] != joint.shape:
        raise ValueError("marginal and joint probability shapes differ")
    x, y = marginals.unbind(-1)
    table = torch.stack((1 - x - y + joint, y - joint, x - joint, joint), -1)
    feasible = torch.isfinite(table).all(-1) & (table >= 0).all(-1) & (table <= 1).all(-1)
    return table.reshape(*joint.shape, 2, 2), feasible


class CrossTaskModel(nn.Module):
    def __init__(self, users: int, items: int, dimension: int = 16):
        super().__init__()
        self.users = nn.Embedding(users, dimension)
        self.items = nn.Embedding(items, dimension)
        self.body = nn.Sequential(nn.Linear(2 * dimension + 3, dimension), nn.Tanh())
        self.marginal = nn.Linear(dimension, 2)
        self.cross = nn.Linear(dimension, 1)

    def forward(self, users: Tensor, items: Tensor, context: Tensor) -> tuple[Tensor, Tensor]:
        state = self.body(torch.cat((self.users(users), self.items(items), context), -1))
        return self.marginal(state), self.cross(state).squeeze(-1)


def auxiliary_loss(marginal_logits: Tensor, cross_logits: Tensor, labels: Tensor, *,
                   weight: float = 0.1, auxiliary_labels: Tensor | None = None) -> tuple[Tensor, dict]:
    if weight < 0 or marginal_logits.shape != labels.shape or cross_logits.shape != labels.shape[:-1]:
        raise ValueError("invalid weight or task dimensions")
    target = labels.prod(-1) if auxiliary_labels is None else auxiliary_labels
    if target.shape != cross_logits.shape:
        raise ValueError("auxiliary labels must match the cross head")
    base = F.binary_cross_entropy_with_logits(marginal_logits, labels)
    cross = F.binary_cross_entropy_with_logits(cross_logits, target)
    return base + weight * cross, {"marginal_bce": base.detach(), "cross_bce": cross.detach()}
