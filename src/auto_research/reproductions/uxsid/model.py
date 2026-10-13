"""Equations 2--11 of UxSID, without item-specific interest compression."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math

import torch
from torch import nn
from torch.nn import functional as F


@dataclass
class QuantizedItems:
    first_ids: torch.Tensor
    residual_ids: tuple[torch.Tensor, ...]
    reconstruction: torch.Tensor
    reconstruction_mse: float


class ResidualKmeansFSQ:
    """Residual vector k-means followed by bounded finite scalar quantization.

    UxSID specifies the residual decomposition and the first-code serving key,
    but not a unique hybrid stage schedule. The schedule is explicit here;
    fitted centers and scalar ranges use training item attributes only.
    """
    def __init__(self, codebook_size=64, kmeans_stages=2, scalar_levels=7, iterations=30):
        if min(codebook_size, kmeans_stages, iterations) < 1 or scalar_levels < 2:
            raise ValueError("positive vector-quantizer budget and >=2 scalar levels required")
        self.size, self.stages = codebook_size, kmeans_stages
        self.levels, self.iterations = scalar_levels, iterations
        self.centers: list[torch.Tensor] = []

    def fit(self, vectors: torch.Tensor, *, seed: int):
        if vectors.ndim != 2 or len(vectors) < self.size or not torch.isfinite(vectors).all():
            raise ValueError("finite training semantic vectors with at least K rows required")
        generator = torch.Generator(device=vectors.device).manual_seed(seed)
        residual = vectors.detach().float()
        self.centers = []
        for _ in range(self.stages):
            centers = residual[torch.randperm(len(residual), generator=generator,
                                             device=residual.device)[:self.size]].clone()
            for _ in range(self.iterations):
                assignments = torch.cdist(residual, centers).argmin(1)
                next_centers = centers.clone()
                for group in range(self.size):
                    members = residual[assignments == group]
                    if len(members):
                        next_centers[group] = members.mean(0)
                if torch.allclose(centers, next_centers, atol=1e-6, rtol=0):
                    centers = next_centers
                    break
                centers = next_centers
            self.centers.append(centers)
            residual = residual - centers[torch.cdist(residual, centers).argmin(1)]
        self.scalar_min = residual.amin(0)
        self.scalar_span = (residual.amax(0) - self.scalar_min).clamp_min(1e-8)
        return self

    def encode(self, vectors: torch.Tensor) -> QuantizedItems:
        if not self.centers:
            raise RuntimeError("fit quantizer on training attributes first")
        original = vectors.detach().float()
        residual = original
        codes = []
        for centers in self.centers:
            code = torch.cdist(residual, centers).argmin(1)
            codes.append(code)
            residual = residual - centers[code]
        scalar = (((residual - self.scalar_min) / self.scalar_span).clamp(0, 1)
                  * (self.levels - 1)).round().long()
        scalar_values = self.scalar_min + scalar.float() * self.scalar_span / (self.levels - 1)
        reconstruction = original - residual + scalar_values
        return QuantizedItems(codes[0], tuple(codes[1:] + [scalar]), reconstruction,
                              float((reconstruction - original).square().mean()))


class ProjectedAttention(nn.Module):
    def __init__(self, dimension):
        super().__init__()
        self.query = nn.Linear(dimension, dimension, bias=False)
        self.key = nn.Linear(dimension, dimension, bias=False)
        self.value = nn.Linear(dimension, dimension, bias=False)
        self.dimension = dimension

    def forward(self, queries, keys, valid=None):
        scores = self.query(queries) @ self.key(keys).transpose(-1, -2) / math.sqrt(self.dimension)
        if valid is not None:
            if not valid.any(-1).all():
                raise ValueError("each sequence must contain at least one real history item")
            scores = scores.masked_fill(~valid[:, None, :], -torch.inf)
        return torch.softmax(scores, -1) @ self.value(keys)


def orthogonality_loss(anchors):
    """Eq.5: global squared L2 denominator, not row-normalized cosine loss."""
    gram = anchors @ anchors.transpose(-1, -2)
    norm = anchors.square().sum((-1, -2), keepdim=True).clamp_min(1e-8)
    identity = torch.eye(anchors.shape[-2], device=anchors.device, dtype=anchors.dtype)
    return torch.linalg.vector_norm((gram / norm - identity).flatten(-2), dim=-1).mean()


class InterestCompressor(nn.Module):
    def __init__(self, dimension=32, anchors=8):
        super().__init__()
        self.anchors = nn.Parameter(torch.randn(anchors, dimension) / math.sqrt(dimension))
        self.attention = ProjectedAttention(dimension)
        self.pffns = nn.ModuleList(nn.Sequential(nn.Linear(dimension, dimension * 4), nn.Sigmoid(),
                                                nn.Linear(dimension * 4, dimension))
                                  for _ in range(anchors))
        self.norms = nn.ModuleList(nn.LayerNorm(dimension) for _ in range(anchors))

    def forward(self, history, valid):
        compressed = self.attention(self.anchors.expand(len(history), -1, -1), history, valid)
        return torch.stack([norm(compressed[:, j] + pffn(compressed[:, j]))
                            for j, (pffn, norm) in enumerate(zip(self.pffns, self.norms))], dim=1)


class UxSID(nn.Module):
    def __init__(self, *, items, users, sid_count, dimension=32, anchors=8, variant="uxsid"):
        super().__init__()
        if variant not in {"uxsid", "global-only", "agnostic", "ungated"}:
            raise ValueError("unsupported paired ablation")
        self.variant, self.dimension = variant, dimension
        self.items = nn.Embedding(items, dimension, padding_idx=0)
        self.users = nn.Embedding(users, dimension)
        self.sids = nn.Embedding(sid_count, dimension)
        self.compressor = InterestCompressor(dimension, anchors)
        self.global_attention = ProjectedAttention(dimension)
        self.local_attention = ProjectedAttention(dimension)
        self.gate = nn.Sequential(nn.Linear(dimension, dimension), nn.ReLU(),
                                  nn.Linear(dimension, dimension), nn.Sigmoid())
        self.context = nn.Linear(1, dimension)
        self.predictor = nn.Sequential(nn.Linear(7 * dimension, 96), nn.ReLU(), nn.Linear(96, 1))

    def memory(self, history_ids, valid, sid_ids):
        history = self.items(history_ids)
        semantic = self.sids(sid_ids)[:, None, :]
        anchors = self.compressor(history, valid)
        global_interest = self.global_attention(semantic, history, valid)
        gated = semantic * self.gate(global_interest) if self.variant == "uxsid" else semantic
        local_interest = self.local_attention(gated, anchors)
        if self.variant == "global-only":
            local_interest = torch.zeros_like(local_interest)
        elif self.variant == "agnostic":
            global_interest = anchors.mean(1, keepdim=True)
            local_interest = global_interest
        return torch.cat((global_interest[:, 0], local_interest[:, 0]), dim=-1), anchors

    def score(self, *, memory, users, targets, history_ids, valid, context, sid_ids):
        short = self.items(history_ids[:, -10:])
        short_valid = valid[:, -10:]
        short_mean = (short * short_valid[..., None]).sum(1) / short_valid.sum(1, keepdim=True)
        features = torch.cat((self.items(targets), self.users(users),
                              self.sids(sid_ids), self.context(context[:, None]), short_mean, memory), dim=-1)
        return self.predictor(features)[:, 0]

    def forward(self, *, users, targets, history_ids, valid, context, sid_ids):
        memory, anchors = self.memory(history_ids, valid, sid_ids)
        return self.score(memory=memory, users=users, targets=targets, history_ids=history_ids,
                          valid=valid, context=context, sid_ids=sid_ids), orthogonality_loss(anchors)


class SemanticMemoryCache:
    """User/SID sharing with history and model-revision invalidation.

    This is an offline-generated in-process KV cache, not a production latency
    benchmark. Each value is computed from precisely the same history as the
    uncached model; target item identity cannot enter the memory computation.
    """
    def __init__(self):
        self.values = {}

    def get(self, model, *, user, sid, history_ids, valid, model_revision):
        if model.training:
            raise ValueError("only a frozen eval-mode model can populate serving memory")
        history_hash = hashlib.sha256(history_ids.detach().cpu().numpy().tobytes()
                                      + valid.detach().cpu().numpy().tobytes()).hexdigest()
        key = (int(user), int(sid), history_hash, model_revision)
        if key not in self.values:
            with torch.no_grad():
                ids = torch.tensor([sid], device=history_ids.device)
                self.values[key] = model.memory(history_ids, valid, ids)[0].detach()
        return self.values[key]


def objective(logits, labels, orthogonal, *, coefficient=1e-3):
    return F.binary_cross_entropy_with_logits(logits, labels) + coefficient * orthogonal
