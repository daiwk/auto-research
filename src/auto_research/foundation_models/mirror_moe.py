"""MirrorMoE Eqs. 3-6, independent dense-reference dispatch (no Megatron dependency)."""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor, nn


@dataclass(frozen=True)
class MirrorRouting:
    selected: Tensor
    aggregation_weights: Tensor
    original_probabilities: Tensor
    selection_probabilities: Tensor
    balancing_loss: Tensor


def cosine_mirror_ratio(progress: float, initial: float = .4) -> float:
    if not 0 <= progress <= 1 or not 0 <= initial <= 1:
        raise ValueError("progress and initial ratio must be in [0,1]")
    return initial * .5 * (1 + math.cos(math.pi * progress))


def mirror_routing(logits: Tensor, *, top_k: int, ratio: float) -> MirrorRouting:
    if (logits.ndim < 2 or not logits.is_floating_point() or not bool(torch.isfinite(logits).all()) or
            not isinstance(top_k, int) or isinstance(top_k, bool) or
            not 1 <= top_k <= logits.shape[-1] or not 0 <= ratio <= 1 or logits.numel() == 0):
        raise ValueError("finite nonempty token/expert logits, valid top_k and ratio required")
    dtype = torch.float64 if logits.dtype == torch.float64 else torch.float32
    original = logits.to(dtype).softmax(-1)
    mirrored = (-logits.to(dtype)).softmax(-1)
    selection = (1 - ratio) * original + ratio * mirrored
    selected = selection.topk(top_k, dim=-1).indices
    # Eq. 5: original probabilities, NOT mixed probabilities and NOT normalized
    # over the selected experts. Shared experts are added independently.
    weights = original.gather(-1, selected)
    experts = logits.shape[-1]
    count = _expert_counts(selected, experts)
    fractions = count / (selected.numel())
    balancing = experts * (fractions * original.reshape(-1, experts).mean(0)).sum()
    return MirrorRouting(selected, weights, original, selection, balancing)


def _expert_counts(selected: Tensor, experts: int) -> Tensor:
    return torch.bincount(selected.reshape(-1), minlength=experts).to(torch.float32)


class MirrorMoELayer(nn.Module):
    """Actual trainable experts; dense evaluation used only for bounded reference tests."""

    def __init__(self, dimension: int, hidden: int, routed_experts: int = 6,
                 shared_experts: int = 2, top_k: int = 3):
        super().__init__()
        if min(dimension, hidden, routed_experts) < 1 or not 0 <= shared_experts or not 1 <= top_k <= routed_experts:
            raise ValueError("invalid expert dimensions/counts")
        self.router = nn.Linear(dimension, routed_experts, bias=False)
        self.routed = nn.ModuleList(nn.Sequential(nn.Linear(dimension, hidden), nn.SiLU(),
                                   nn.Linear(hidden, dimension)) for _ in range(routed_experts))
        self.shared = nn.ModuleList(nn.Sequential(nn.Linear(dimension, hidden), nn.SiLU(),
                                   nn.Linear(hidden, dimension)) for _ in range(shared_experts))
        self.top_k = top_k

    def forward(self, hidden: Tensor, *, ratio: float) -> tuple[Tensor, MirrorRouting]:
        routing = mirror_routing(self.router(hidden), top_k=self.top_k, ratio=ratio)
        all_outputs = torch.stack([expert(hidden) for expert in self.routed], -2)
        selected = all_outputs.gather(-2, routing.selected.unsqueeze(-1).expand(*routing.selected.shape, hidden.shape[-1]))
        output = (selected * routing.aggregation_weights.unsqueeze(-1)).sum(-2)
        for expert in self.shared:
            output = output + expert(hidden)
        return output, routing
