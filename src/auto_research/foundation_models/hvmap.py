"""Independent HVMap formula implementation, not the full retrieval campaign.

Fixed source: arXiv:2611.01514v2, Sections 3.3--3.5. Public upstream
1fe819a0369b5a2a00bfb535c5755daa15a5d035 has no declared license; no code
is copied. Exact small tensors test operators, not semantic retrieval quality.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Mapping

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


def _vectors(value: Tensor, name: str) -> Tensor:
    if (value.ndim != 2 or min(value.shape) < 1 or not value.is_floating_point()
            or not torch.isfinite(value).all() or not torch.isfinite(value.norm(dim=-1)).all()
            or (value.norm(dim=-1) <= 1e-12).any()):
        raise ValueError(name + " requires finite, nonzero rows in a floating matrix")
    return value


class HVMap(nn.Module):
    """Four affine layers; three SELUs; width 5 x target dim; L2 output."""

    def __init__(self, input_dim: int, output_dim: int):
        super().__init__()
        if any(isinstance(x, bool) or not isinstance(x, int) or x < 1 for x in (input_dim, output_dim)):
            raise ValueError("positive integral dimensions required")
        width = 5 * output_dim
        dimensions = (input_dim, width, width, width, output_dim)
        self.layers = nn.ModuleList(nn.Linear(a, b) for a, b in zip(dimensions[:-1], dimensions[1:], strict=True))

    def forward(self, value: Tensor) -> Tensor:
        _vectors(value, "mapping input")
        if value.shape[1] != self.layers[0].in_features:
            raise ValueError("wrong source dimension")
        for layer in self.layers[:-1]:
            value = F.selu(layer(value))
        value = self.layers[-1](value)
        _vectors(value, "unnormalized mapping output")
        return F.normalize(value, p=2, dim=-1)


def fuzzy_contrastive_loss(mapped: Tensor, target: Tensor, *, metric: str = "cosine", reduction: str = "sum") -> Tensor:
    """Eq. 3: target-target distances versus mapped-to-ORIGINAL-target.

    The diagonal anchors absolute alignment. Mapped-to-mapped RKD, InfoNCE,
    and a margin hinge are not interchangeable with this squared objective.
    """
    _vectors(mapped, "mapped")
    _vectors(target, "target")
    if mapped.shape != target.shape or mapped.device != target.device or mapped.dtype != target.dtype:
        raise ValueError("paired same-shape, same-device and same-dtype matrices required")
    if metric == "cosine":
        y, z = F.normalize(target, dim=-1), F.normalize(mapped, dim=-1)
        expected, observed = 1 - y @ y.T, 1 - z @ y.T
    elif metric == "l2":
        expected, observed = torch.cdist(target, target), torch.cdist(mapped, target)
    else:
        raise ValueError("unsupported target-space metric")
    squared = (observed - expected).square()
    if reduction == "sum":
        return squared.sum()
    if reduction == "mean":
        return squared.mean()
    raise ValueError("reduction must be sum or mean")


def score2(query_native: Tensor, candidates_native: Tensor, query_mapped: Tensor,
           candidates_mapped: Tensor, *, native_weight: float = .7) -> Tensor:
    """Section 3.3: native weight belongs to each DB's OWN embedding space."""
    if isinstance(native_weight, bool) or not math.isfinite(native_weight) or not 0 <= native_weight <= 1:
        raise ValueError("native weight must lie in [0, 1]")
    for value, name in ((query_native, "query"), (candidates_native, "candidates"),
                        (query_mapped, "mapped query"), (candidates_mapped, "mapped candidates")):
        _vectors(value, name)
    if (query_native.shape[0] != 1 or query_mapped.shape[0] != 1
            or query_native.shape[1] != candidates_native.shape[1]
            or query_mapped.shape[1] != candidates_mapped.shape[1]
            or candidates_native.shape[0] != candidates_mapped.shape[0]):
        raise ValueError("one query and aligned candidate sets required")
    native = F.cosine_similarity(query_native, candidates_native, dim=-1)
    mapped = F.cosine_similarity(query_mapped, candidates_mapped, dim=-1)
    return native_weight * native + (1 - native_weight) * mapped


def federated_topk(scores: Mapping[str, Tensor], k: int) -> list[tuple[str, int, float]]:
    """Merge up to K already retrieved candidates PER database; no final quota."""
    if isinstance(k, bool) or not isinstance(k, int) or k < 1 or not scores:
        raise ValueError("positive K and nonempty database mapping required")
    rows = []
    for database, values in scores.items():
        if not database or values.ndim != 1 or not torch.isfinite(values).all() or values.numel() > k:
            raise ValueError("each DB supplies at most K finite SCORE2 values")
        rows.extend((database, i, float(value)) for i, value in enumerate(values.detach().cpu()))
    return sorted(rows, key=lambda row: (-row[2], row[0], row[1]))[:k]


def map_via_hub(value: Tensor, source: str, target: str, hub: str,
                maps: Mapping[tuple[str, str], Callable[[Tensor], Tensor]]) -> Tensor:
    """Section 3.5 spoke-to-spoke uses two maps, never all-pair training.

    The returned copy is for cross-space scoring; keep the caller's native
    embedding for its native SCORE2 term instead of mapping it back in place.
    """
    _vectors(value, "native embedding")
    if not all(isinstance(name, str) and name for name in (source, target, hub)):
        raise ValueError("named source, target and hub required")
    path = [] if source == target else ([(source, target)] if hub in {source, target}
                                       else [(source, hub), (hub, target)])
    result = value.clone()
    for edge in path:
        if edge not in maps:
            raise ValueError("missing hub/spoke map")
        result = maps[edge](result)
        _vectors(result, "mapped embedding")
    return result


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device not in {"cpu", "cuda"}:
        raise ValueError("cpu/cuda only")
    torch.manual_seed(seed)
    model = HVMap(4, 3).to(device)
    source = torch.randn(8, 4, device=device)
    target = F.normalize(torch.randn(8, 3, device=device), dim=-1)
    mapped = model(source)
    loss = fuzzy_contrastive_loss(mapped, target)
    loss.backward()
    with torch.no_grad():
        identity = fuzzy_contrastive_loss(target, target)
        rotated = -target
        anchored = fuzzy_contrastive_loss(rotated, target)
        rkd = ((1 - rotated @ rotated.T) - (1 - target @ target.T)).square().sum()
        q = torch.tensor([[1., 0.]], device=device)
        candidates = torch.tensor([[1., 0.], [0., 1.]], device=device)
        scores = score2(q, candidates, q, candidates.flip(0))
        winners = federated_topk({"source": torch.tensor([.9, .8], device=device),
                                 "hub": torch.tensor([.2, .1], device=device)}, 2)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"finite_gradients": all(p.grad is not None and bool(torch.isfinite(p.grad).all()) for p in model.parameters()),
                       "unit_outputs": bool(torch.allclose(mapped.norm(dim=-1), torch.ones(8, device=device), atol=1e-6)),
                       "identity_zero": float(identity) < 1e-10,
                       "rkd_cannot_anchor": float(anchored) > 1 and float(rkd) < 1e-8,
                       "native_weight_preserved": bool(torch.allclose(scores, torch.tensor([.7, .3], device=device))),
                       "no_database_quota": all(row[0] == "source" for row in winners)},
            "metrics": {"fuzzy_loss": float(loss.detach()), "identity_loss": float(identity),
                        "unaligned_rkd_loss": float(rkd), "unaligned_fuzzy_loss": float(anchored),
                        "same_database_winners": len(winners)}}
