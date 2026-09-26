"""Google Light Heads: dynamically injected, stop-gradient, stateless task heads."""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn


@dataclass(frozen=True)
class HeadSpec:
    name: str
    hidden: int = 16
    objective: str = "binary"
    reset_each_run: bool = True

    def __post_init__(self) -> None:
        if not self.name or self.hidden < 1 or self.objective not in {"binary", "regression"}:
            raise ValueError("invalid Light Head configuration")


class LightHeadRanker(nn.Module):
    """Shared ranker with a conventional main head and configurable Light Heads."""

    def __init__(self, users: int, items: int, genres: int, dimensions: int = 24):
        super().__init__()
        self.user = nn.Embedding(users, dimensions)
        self.item = nn.Embedding(items, dimensions)
        self.genre = nn.Linear(genres, dimensions, bias=False)
        self.shared = nn.Sequential(nn.Linear(dimensions * 3, dimensions), nn.ReLU())
        self.main = nn.Linear(dimensions, 1)
        self.light_heads = nn.ModuleDict()
        self.specs: dict[str, HeadSpec] = {}

    def inject(self, spec: HeadSpec) -> None:
        """Apply centrally supplied task configuration without rebuilding the backbone."""
        if spec.name in self.light_heads:
            raise ValueError(f"Light Head already exists: {spec.name}")
        width = self.main.in_features
        self.light_heads[spec.name] = nn.Sequential(
            nn.Linear(width, spec.hidden), nn.ReLU(), nn.Linear(spec.hidden, 1),
        )
        self.specs[spec.name] = spec

    def reset_run(self) -> None:
        """Discard only stateless heads marked for daily/run reset."""
        for name, head in self.light_heads.items():
            if self.specs[name].reset_each_run:
                for module in head.modules():
                    if module is not head and hasattr(module, "reset_parameters"):
                        module.reset_parameters()

    def representation(self, users: torch.Tensor, items: torch.Tensor,
                       genres: torch.Tensor) -> torch.Tensor:
        return self.shared(torch.cat((
            self.user(users), self.item(items), self.genre(genres),
        ), dim=-1))

    def forward(self, users: torch.Tensor, items: torch.Tensor,
                genres: torch.Tensor, *, stop_gradient: bool = True) -> dict[str, torch.Tensor]:
        shared = self.representation(users, items, genres)
        output = {"main": self.main(shared).squeeze(-1)}
        for name, head in self.light_heads.items():
            output[name] = head(shared.detach() if stop_gradient else shared).squeeze(-1)
        return output


def head_loss(logits: torch.Tensor, targets: torch.Tensor, spec: HeadSpec) -> torch.Tensor:
    if spec.objective == "binary":
        return nn.functional.binary_cross_entropy_with_logits(logits, targets)
    return nn.functional.mse_loss(logits, targets)
