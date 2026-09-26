"""Scaled MuSeR retrieval mechanisms: temporal pooling, multi-query, semantic fusion."""

from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn import functional as F


class MuSeR(nn.Module):
    def __init__(self, items: int, tags: int, item_tags: torch.Tensor, *,
                 dimensions: int = 32, interests: int = 4,
                 use_compression: bool = True, use_semantics: bool = True):
        super().__init__()
        self.items = items
        self.use_compression = use_compression
        self.use_semantics = use_semantics
        self.register_buffer("item_tags", item_tags.long())
        self.item_embedding = nn.Embedding(items + 1, dimensions, padding_idx=items)
        self.tag_embedding = nn.Embedding(tags + 1, dimensions, padding_idx=tags)
        self.id_projection = nn.Linear(dimensions, dimensions, bias=False)
        self.semantic_projection = nn.Linear(dimensions, dimensions, bias=False)
        self.positions = nn.Embedding(64, dimensions)
        layer = nn.TransformerEncoderLayer(dimensions, 4, 2 * dimensions,
                                           dropout=0.0, batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, 1, enable_nested_tensor=False)
        self.queries = nn.Parameter(torch.randn(interests, dimensions) * 0.02)
        self.temperature = 0.07

    def item_vectors(self, ids: torch.Tensor) -> torch.Tensor:
        values = self.id_projection(self.item_embedding(ids))
        if self.use_semantics:
            safe_ids = ids.clamp_max(self.items - 1)
            semantic = self.tag_embedding(self.item_tags[safe_ids])
            values = values + self.semantic_projection(semantic)
        return F.normalize(values, dim=-1)

    def _compress_one(self, ids: torch.Tensor) -> torch.Tensor:
        if not self.use_compression:
            return self.item_vectors(ids[-64:])
        recent = ids[-8:]
        mid = ids[-40:-8]
        old = ids[:-40]
        blocks = []
        for section, width in ((old, 16), (mid, 4)):
            for start in range(0, len(section), width):
                blocks.append(self.item_vectors(section[start:start + width]).mean(0))
        blocks.extend(self.item_vectors(recent).unbind(0))
        return torch.stack(blocks[-64:])

    def encode(self, histories: list[torch.Tensor]) -> torch.Tensor:
        compressed = [self._compress_one(history) for history in histories]
        width = max(len(row) for row in compressed)
        padded = torch.zeros(len(compressed), width, self.queries.shape[-1],
                             device=compressed[0].device)
        mask = torch.ones(len(compressed), width, dtype=torch.bool,
                          device=compressed[0].device)
        for index, row in enumerate(compressed):
            padded[index, :len(row)] = row
            mask[index, :len(row)] = False
        positions = torch.arange(width, device=padded.device)
        hidden = self.encoder(padded + self.positions(positions),
                              src_key_padding_mask=mask)
        attention = torch.einsum("md,bld->bml", self.queries, hidden)
        attention = attention / math.sqrt(hidden.shape[-1])
        attention = attention.masked_fill(mask[:, None, :], -1e4).softmax(-1)
        return F.normalize(torch.einsum("bml,bld->bmd", attention, hidden), dim=-1)

    def score(self, interests: torch.Tensor, candidates: torch.Tensor) -> torch.Tensor:
        items = self.item_vectors(candidates)
        similarity = torch.einsum("bmd,bkd->bkm", interests, items)
        routing = (similarity / self.temperature).softmax(-1)
        return (routing * similarity).sum(-1) / self.temperature

    @staticmethod
    def orthogonality(interests: torch.Tensor) -> torch.Tensor:
        gram = interests @ interests.transpose(-1, -2)
        identity = torch.eye(gram.shape[-1], device=gram.device)
        return ((gram - identity) ** 2).mean()
