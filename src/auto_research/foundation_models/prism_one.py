"""Prism-1 option-isolated causal scoring, independently implemented from §4.

This tiny reference has no checkpoint, tokenizer or capability benchmark.  The
architectural contract (not a trained model's quality) is what it implements.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import torch
from torch import Tensor, nn


@dataclass(frozen=True)
class PackedOptions:
    token_ids: Tensor
    position_ids: Tensor
    allowed_attention: Tensor
    option_ends: Tensor
    prefix_length: int
    option_lengths: tuple[int, ...]


def pack_options(prefix: Tensor, options: Sequence[Tensor]) -> PackedOptions:
    """Pack one context and nonempty option blocks, resetting each block's positions.

    ``allowed_attention[q,k]`` is true iff q may attend k.  Context tokens
    retain ordinary causal attention; an option sees the whole shared context
    and only the causal prefix of its *own* option.  There are no answer labels
    or cross-option edges.
    """
    if prefix.ndim != 1 or prefix.dtype != torch.long or prefix.numel() == 0:
        raise ValueError("prefix must be a nonempty 1D long tensor")
    if not options:
        raise ValueError("at least one option is required")
    if bool((prefix < 0).any()):
        raise ValueError("token ids cannot be negative")
    for option in options:
        if (option.ndim != 1 or option.numel() == 0 or option.dtype != torch.long
                or option.device != prefix.device or bool((option < 0).any())):
            raise ValueError("options must be nonempty same-device 1D long tensors")
    lengths = tuple(option.numel() for option in options)
    p = prefix.numel()
    n = p + sum(lengths)
    allowed = torch.zeros((n, n), device=prefix.device, dtype=torch.bool)
    allowed[:p, :p] = torch.ones((p, p), device=prefix.device, dtype=torch.bool).tril()
    positions = [torch.arange(p, device=prefix.device)]
    ends, start = [], p
    for length in lengths:
        allowed[start:start + length, :p] = True
        allowed[start:start + length, start:start + length] = torch.ones(
            (length, length), device=prefix.device, dtype=torch.bool).tril()
        positions.append(torch.arange(p, p + length, device=prefix.device))
        ends.append(start + length - 1)
        start += length
    return PackedOptions(
        torch.cat((prefix, *options)), torch.cat(positions), allowed,
        torch.tensor(ends, device=prefix.device, dtype=torch.long), p, lengths,
    )


class _CausalBlock(nn.Module):
    def __init__(self, width: int, heads: int) -> None:
        super().__init__()
        self.heads, self.head_width = heads, width // heads
        self.norm_attention = nn.LayerNorm(width)
        self.norm_mlp = nn.LayerNorm(width)
        self.qkv = nn.Linear(width, 3 * width)
        self.out = nn.Linear(width, width)
        self.mlp = nn.Sequential(nn.Linear(width, 3 * width), nn.GELU(), nn.Linear(3 * width, width))

    def forward(self, hidden: Tensor, allowed: Tensor) -> Tensor:
        n, width = hidden.shape
        qkv = self.qkv(self.norm_attention(hidden)).reshape(n, 3, self.heads, self.head_width)
        q, k, v = qkv.unbind(dim=1)
        scores = torch.einsum("qhd,khd->hqk", q, k) / math.sqrt(self.head_width)
        weights = scores.masked_fill(~allowed.unsqueeze(0), -torch.inf).softmax(dim=-1)
        update = torch.einsum("hqk,khd->qhd", weights, v).reshape(n, width)
        hidden = hidden + self.out(update)
        return hidden + self.mlp(self.norm_mlp(hidden))


class PrismOneScorer(nn.Module):
    """Small trainable causal transformer preserving Prism-1's information boundary.

    Learned absolute positions make the shared-position requirement explicit.
    This is not a Qwen/Gemma implementation or a claim to their decision quality.
    """

    def __init__(self, vocabulary: int = 37, width: int = 24, heads: int = 3,
                 depth: int = 2, max_positions: int = 128, yes_token: int = 1,
                 no_token: int = 2) -> None:
        super().__init__()
        if (min(vocabulary, width, heads, depth, max_positions) <= 0 or width % heads
                or not 0 <= yes_token < vocabulary or not 0 <= no_token < vocabulary
                or yes_token == no_token):
            raise ValueError("invalid transformer dimensions or yes/no token identities")
        self.vocabulary = vocabulary
        self.yes_token, self.no_token = yes_token, no_token
        self.token_embedding = nn.Embedding(vocabulary, width)
        self.position_embedding = nn.Embedding(max_positions, width)
        self.blocks = nn.ModuleList(_CausalBlock(width, heads) for _ in range(depth))
        self.final_norm = nn.LayerNorm(width)
        self.vocabulary_head = nn.Linear(width, vocabulary, bias=False)

    def token_logits(self, packed: PackedOptions) -> Tensor:
        if (bool((packed.token_ids >= self.vocabulary).any())
                or bool((packed.position_ids >= self.position_embedding.num_embeddings).any())):
            raise ValueError("token or position exceeds model capacity")
        hidden = self.token_embedding(packed.token_ids) + self.position_embedding(packed.position_ids)
        for block in self.blocks:
            hidden = block(hidden, packed.allowed_attention)
        return self.vocabulary_head(self.final_norm(hidden))

    def forward(self, packed: PackedOptions) -> Tensor:
        logits = self.token_logits(packed)[packed.option_ends]
        # log P(yes) - log P(no) = logit(yes) - logit(no), no cancellation error.
        return logits[:, self.yes_token] - logits[:, self.no_token]

    def choice_probabilities(self, packed: PackedOptions) -> Tensor:
        return self(packed).softmax(dim=0)


def choice_diagnostics(original_scores: Tensor, extended_scores: Tensor) -> dict[str, float]:
    """Compare the same original options before/after adding unrelated options.

    The extra scores must be appended after the original options.  Accuracy is
    deliberately absent: these invariants do not require, or establish, gold
    decisions.
    """
    if (original_scores.ndim != 1 or extended_scores.ndim != 1 or original_scores.numel() < 1
            or extended_scores.numel() <= original_scores.numel()
            or not bool(torch.isfinite(original_scores).all())
            or not bool(torch.isfinite(extended_scores).all())):
        raise ValueError("finite 1D original and strictly longer extended scores required")
    n = original_scores.numel()
    original = original_scores.softmax(0)
    # Conditional softmax over the retained options is algebraically identical
    # to renormalizing the full distribution, without underflow if an added
    # option has an enormous score.
    retained = extended_scores[:n].softmax(0)
    return {"original_score_max_error": float((original_scores - extended_scores[:n]).abs().max().detach()),
            "renormalized_original_probability_tv": float((original - retained).abs().sum().detach() / 2)}
