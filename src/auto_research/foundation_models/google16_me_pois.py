"""ME-POIs Eq.9–17 loss core, not a trajectory/Maps capability reproduction.

The visit Transformer, Space2Vec and upstream private data are deliberately not
replaced by a proxy encoder. Callers supply contextual visit vectors and text
features; the runner's generated tensors are formula/gradient diagnostics only.
"""
from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def _finite(value: Tensor, name: str) -> None:
    if not torch.isfinite(value).all():
        raise ValueError(f"{name} must be finite")


def transferred_visit_distribution(
    sparse_xy: Tensor, anchor_xy: Tensor, anchor_histograms: Tensor, bandwidths: Tensor
) -> Tensor:
    """Eq.10–11: separately normalize each Gaussian scale, then average.

    Coordinates and bandwidths must use the same projected-distance unit.
    Histogram counts are normalized here; zero-count anchors are rejected.
    """
    if sparse_xy.ndim != 2 or sparse_xy.shape[1] != 2 or anchor_xy.ndim != 2 or anchor_xy.shape[1] != 2:
        raise ValueError("coordinates must have shape [POI, 2]")
    if anchor_histograms.ndim != 2 or anchor_histograms.shape[0] != len(anchor_xy) or not len(anchor_xy):
        raise ValueError("nonempty anchor histograms must align with coordinates")
    if bandwidths.ndim != 1 or not bandwidths.numel() or (bandwidths <= 0).any():
        raise ValueError("bandwidths must be a positive nonempty vector")
    for value, name in ((sparse_xy, "coordinates"), (anchor_xy, "coordinates"),
                        (anchor_histograms, "histograms"), (bandwidths, "bandwidths")):
        _finite(value, name)
    if (anchor_histograms < 0).any() or (anchor_histograms.sum(-1) <= 0).any():
        raise ValueError("anchor histograms must have nonnegative positive total counts")
    hist = anchor_histograms / anchor_histograms.sum(-1, keepdim=True)
    distances = (sparse_xy[:, None] - anchor_xy[None]).square().sum(-1)
    weights = (-distances[None] / (2 * bandwidths[:, None, None].square())).softmax(-1)
    return (weights @ hist).mean(0)


def prototype_contrastive_loss(visits: Tensor, prototypes: Tensor, poi_ids: Tensor, temperature: float = .1) -> Tensor:
    """Eq.9 with unique minibatch POI prototypes, not duplicate visit negatives."""
    if visits.ndim != 2 or prototypes.ndim != 2 or visits.shape[1] != prototypes.shape[1]:
        raise ValueError("visit/prototype dimensions must agree")
    if poi_ids.shape != (len(visits),) or poi_ids.dtype != torch.long or not len(visits):
        raise ValueError("one integer POI identity required per nonempty visit")
    if temperature <= 0 or not torch.isfinite(torch.tensor(temperature)):
        raise ValueError("temperature must be positive finite")
    if (poi_ids < 0).any() or (poi_ids >= len(prototypes)).any():
        raise ValueError("POI identity outside prototype table")
    _finite(visits, "visits")
    _finite(prototypes, "prototypes")
    unique, target = torch.unique(poi_ids, sorted=True, return_inverse=True)
    logits = F.normalize(visits, dim=-1) @ F.normalize(prototypes[unique], dim=-1).T / temperature
    return F.cross_entropy(logits, target)


def distribution_kl_sum(logits: Tensor, target: Tensor) -> Tensor:
    """Eq.13/15 sum over POIs, including zero-probability target bins."""
    if logits.shape != target.shape or logits.ndim != 2:
        raise ValueError("logits and target must align as [POI, time-bin]")
    _finite(logits, "logits")
    _finite(target, "target")
    if (target < 0).any() or not torch.allclose(target.sum(-1), torch.ones_like(target.sum(-1)), atol=1e-5):
        raise ValueError("target rows must be distributions")
    return F.kl_div(logits.log_softmax(-1), target, reduction="sum")


class MobilityPrototypeLoss(nn.Module):
    """Trainable prototypes, shared temporal MLP and projected-text alignment."""

    def __init__(self, pois: int, dim: int, text_dim: int, bins: int):
        super().__init__()
        if min(pois, dim, text_dim, bins) <= 0:
            raise ValueError("all dimensions must be positive")
        self.prototypes = nn.Parameter(torch.empty(pois, dim))
        nn.init.normal_(self.prototypes, std=.02)
        self.temporal = nn.Sequential(nn.Linear(dim, dim), nn.ReLU(), nn.Linear(dim, bins))
        self.text_projection = nn.Linear(text_dim, dim, bias=False)

    def forward(self, visits: Tensor, poi_ids: Tensor, text_features: Tensor,
                anchor_ids: Tensor, anchor_distribution: Tensor, sparse_ids: Tensor,
                sparse_prior: Tensor, weights: tuple[float, float, float] = (1., 1., 1.)) -> dict[str, Tensor]:
        if text_features.ndim != 2 or len(text_features) != len(self.prototypes):
            raise ValueError("text features must cover every prototype")
        if any(weight < 0 or not torch.isfinite(torch.tensor(weight)) for weight in weights):
            raise ValueError("loss weights must be nonnegative finite")
        ids = torch.cat((anchor_ids, sparse_ids))
        if ids.dtype != torch.long or (ids < 0).any() or (ids >= len(self.prototypes)).any():
            raise ValueError("anchor/sparse identity outside prototype table")
        if len(torch.unique(ids)) != len(ids):
            raise ValueError("anchor and sparse identities must be disjoint and unique")
        _finite(text_features, "text")
        contrastive = prototype_contrastive_loss(visits, self.prototypes, poi_ids)
        logits = self.temporal(self.prototypes)
        anchor = distribution_kl_sum(logits[anchor_ids], anchor_distribution)
        sparse = distribution_kl_sum(logits[sparse_ids], sparse_prior.detach())
        text = (1 - F.cosine_similarity(self.prototypes, self.text_projection(text_features.detach()), dim=-1)).sum()
        total = contrastive + weights[0] * anchor + weights[1] * sparse + weights[2] * text
        return {"loss": total, "contrastive": contrastive, "anchor_kl": anchor,
                "sparse_kl": sparse, "text_alignment": text}
