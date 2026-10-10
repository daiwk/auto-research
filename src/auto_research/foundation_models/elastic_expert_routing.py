"""Elastic Expert Routing (2610.11575), discrete Gaussian token budgets.

This changes training dispatch only. Inference always uses target_k. It does not
claim wall-clock parity: expected expert count, not launch overhead, is matched.
"""

from __future__ import annotations

import torch
from torch import nn


class ElasticExpertRouting(nn.Module):
    def __init__(self, dim, hidden_dim, num_experts, target_k, radius=1, sigma=1.5):
        super().__init__()
        if not (1 <= target_k - radius <= target_k + radius <= num_experts):
            raise ValueError("budget neighborhood must be symmetric and within expert bounds")
        if sigma <= 0 or radius < 0:
            raise ValueError("positive sigma and nonnegative radius required")
        self.target_k, self.num_experts = target_k, num_experts
        budgets = torch.arange(target_k - radius, target_k + radius + 1)
        probability = (-((budgets.float() - target_k) ** 2) / (2 * sigma**2)).softmax(0)
        self.register_buffer("budgets", budgets)
        self.register_buffer("budget_probability", probability)
        self.router = nn.Linear(dim, num_experts, bias=False)
        self.experts = nn.ModuleList([
            nn.Sequential(nn.Linear(dim, hidden_dim), nn.GELU(), nn.Linear(hidden_dim, dim))
            for _ in range(num_experts)
        ])

    def forward(self, inputs, *, generator=None, return_statistics=False):
        shape = inputs.shape
        tokens = inputs.reshape(-1, shape[-1])
        router_probability = self.router(tokens).float().softmax(-1)
        if self.training:
            indices = torch.multinomial(self.budget_probability, len(tokens), replacement=True,
                                        generator=generator)
            realized = self.budgets[indices]
        else:
            realized = torch.full((len(tokens),), self.target_k, device=tokens.device)
        top_probability, top_expert = router_probability.topk(int(self.budgets[-1]), dim=-1)
        rank = torch.arange(top_expert.shape[-1], device=tokens.device)
        selected = rank[None, :] < realized[:, None]
        weights = top_probability * selected
        weights = weights / weights.sum(-1, keepdim=True)
        output = torch.zeros_like(tokens)
        dispatch_counts = torch.zeros(self.num_experts, device=tokens.device, dtype=torch.long)
        # Dispatch only selected tokens, rather than evaluate every expert and
        # multiply unselected outputs by zero (which would defeat sparse compute).
        for expert_id, expert in enumerate(self.experts):
            token_index, slot = torch.where((top_expert == expert_id) & selected)
            if token_index.numel():
                transformed = expert(tokens[token_index])
                output.index_add_(0, token_index,
                                  transformed * weights[token_index, slot, None].to(tokens.dtype))
                dispatch_counts[expert_id] = token_index.numel()
        output = output.reshape(shape)
        if not return_statistics:
            return output
        # Auxiliary balancing measures actual assignments, including variable K.
        dispatch_fraction = dispatch_counts.float() / dispatch_counts.sum().clamp_min(1)
        balance_loss = self.num_experts * (dispatch_fraction * router_probability.mean(0)).sum()
        return output, {"budgets": realized, "dispatch_counts": dispatch_counts,
                        "balance_loss": balance_loss,
                        "expected_budget": (self.budgets * self.budget_probability).sum()}


class ElasticMoELanguageModel(nn.Module):
    """Trainable causal scratch LM; fixed-K and EER share parameter shapes."""

    def __init__(self, vocabulary, dimensions=64, layers=2, heads=4,
                 num_experts=6, target_k=3, radius=1, context=128):
        super().__init__()
        self.embedding = nn.Embedding(vocabulary, dimensions)
        self.position = nn.Embedding(context, dimensions)
        self.attention = nn.ModuleList([
            nn.MultiheadAttention(dimensions, heads, dropout=0., batch_first=True)
            for _ in range(layers)])
        self.moe = nn.ModuleList([
            ElasticExpertRouting(dimensions, dimensions * 2, num_experts, target_k, radius)
            for _ in range(layers)])
        self.norm1 = nn.ModuleList([nn.LayerNorm(dimensions) for _ in range(layers)])
        self.norm2 = nn.ModuleList([nn.LayerNorm(dimensions) for _ in range(layers)])
        self.final_norm = nn.LayerNorm(dimensions)
        self.head = nn.Linear(dimensions, vocabulary, bias=False)

    def forward(self, tokens):
        length = tokens.shape[1]
        if length > self.position.num_embeddings:
            raise ValueError("sequence exceeds positional context")
        hidden = self.embedding(tokens) + self.position(torch.arange(length, device=tokens.device))
        mask = torch.ones(length, length, dtype=torch.bool, device=tokens.device).triu(1)
        balance, dispatched = [], []
        for attention, moe, norm1, norm2 in zip(
                self.attention, self.moe, self.norm1, self.norm2, strict=True):
            normalized = norm1(hidden)
            attended, _ = attention(normalized, normalized, normalized,
                                     attn_mask=mask, need_weights=False)
            hidden = hidden + attended
            transformed, stats = moe(norm2(hidden), return_statistics=True)
            hidden = hidden + transformed
            balance.append(stats["balance_loss"])
            dispatched.append(stats["budgets"].float().mean())
        return self.head(self.final_norm(hidden)), torch.stack(balance).mean(), torch.stack(dispatched).mean()
