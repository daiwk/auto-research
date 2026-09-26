"""Flat feedback-aware codes and shared early-fusion retrieval/ranking.

This is intentionally a small public-data implementation, not Baidu's serving model.
"""

from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn import functional as F


class Unique(nn.Module):
    def __init__(self, items: int, users: int, item_tags: torch.Tensor, *,
                 tags: int, dim: int = 32, codes: int = 64,
                 balance: float = 0.5, joint: bool = True) -> None:
        super().__init__()
        self.items = items
        self.codes = codes
        self.balance = balance
        self.joint = joint
        self.register_buffer("item_tags", item_tags.long())
        self.item_id = nn.Embedding(items, dim)
        self.tag = nn.Embedding(tags, dim)
        self.user = nn.Embedding(users, dim)
        self.item_tower = nn.Linear(dim, dim)
        self.user_tower = nn.Linear(dim, dim)
        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(dim, 4, 2 * dim, dropout=0,
                                       batch_first=True), 1, enable_nested_tensor=False,
        )
        self.query = nn.Linear(dim, dim)
        self.key = nn.Linear(dim, dim)
        self.value = nn.Linear(dim, dim)
        self.code_head = nn.Linear(dim, 1)
        self.rank_head = nn.Linear(dim, 1)
        initial = F.normalize(torch.randn(codes, dim), dim=-1)
        self.register_buffer("codebook", initial)
        self.register_buffer("usage", torch.ones(codes) / codes)

    def item_vector(self, ids: torch.Tensor) -> torch.Tensor:
        return F.normalize(self.item_tower(self.item_id(ids) +
                                           self.tag(self.item_tags[ids])), dim=-1)

    @torch.no_grad()
    def assign(self, vectors: torch.Tensor) -> torch.Tensor:
        distance = torch.cdist(vectors.reshape(-1, vectors.shape[-1]), self.codebook).square()
        if self.balance:
            multiplier = (self.usage.clamp_min(1e-4) * self.codes).pow(self.balance)
            distance *= multiplier
        return distance.argmin(-1).reshape(vectors.shape[:-1])

    @torch.no_grad()
    def update_codebook(self, vectors: torch.Tensor, *, decay: float = 0.95) -> None:
        flat = vectors.detach().reshape(-1, vectors.shape[-1])
        assignment = self.assign(flat)
        counts = torch.bincount(assignment, minlength=self.codes).float()
        sums = torch.zeros_like(self.codebook)
        sums.index_add_(0, assignment, flat)
        used = counts > 0
        self.codebook[used] = F.normalize(
            decay * self.codebook[used] + (1 - decay) * (sums[used] / counts[used, None]),
            dim=-1,
        )
        self.usage.mul_(decay).add_((1 - decay) * counts / counts.sum().clamp_min(1))

    def prefix(self, users: torch.Tensor, history: torch.Tensor) -> torch.Tensor:
        """Static + recent + pooled medium + pooled long tokens, all train-only history."""
        embedded = self.item_id(history) + self.tag(self.item_tags[history])
        recent = embedded[:, -8:]
        medium = embedded[:, -16:-8].reshape(len(users), 2, 4, -1).mean(2)
        long_term = embedded[:, :-16].mean(1, keepdim=True)
        tokens = torch.cat((self.user(users)[:, None], recent, medium, long_term), dim=1)
        return self.encoder(tokens)

    def cross(self, prefix: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """Each target attends only to prefix; targets cannot read one another."""
        query = self.query(targets)
        key = self.key(prefix)
        value = self.value(prefix)
        weight = torch.softmax(query @ key.transpose(-1, -2) / math.sqrt(query.shape[-1]), -1)
        return torch.tanh(targets + weight @ value)

    def forward(self, users: torch.Tensor, history: torch.Tensor,
                items: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        prefix = self.prefix(users, history)
        vectors = self.item_vector(items)
        codes = self.assign(vectors)
        quantized = vectors + (self.codebook[codes] - vectors).detach()
        target = self.item_id(items) + self.tag(self.item_tags[items]) + quantized
        rank = self.rank_head(self.cross(prefix, target)).squeeze(-1)
        if self.joint:
            code_targets = self.codebook[None].expand(len(users), -1, -1)
            logits = self.code_head(self.cross(prefix, code_targets)).squeeze(-1)
        else:
            logits = torch.empty(len(users), 0, device=users.device)
        return rank, logits, vectors

    def code_perplexity(self) -> float:
        probs = self.usage.clamp_min(1e-9)
        return float(torch.exp(-(probs * probs.log()).sum()))
