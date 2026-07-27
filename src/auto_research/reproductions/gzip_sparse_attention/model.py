from __future__ import annotations

import gzip
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class GzipLMConfig:
    dimensions: int = 64
    layers: int = 2
    heads: int = 4
    sequence_length: int = 256
    block_size: int = 32
    local_blocks: int = 1


def compression_ratios(tokens, block_size: int) -> list[list[float]]:
    """Equation 1: compressed bytes divided by original block bytes."""
    rows = tokens.detach().cpu().tolist() if hasattr(tokens, "detach") else tokens
    output = []
    for row in rows:
        values = []
        for start in range(0, len(row), block_size):
            block = bytes(int(value) & 0xFF for value in row[start : start + block_size])
            values.append(len(gzip.compress(block, compresslevel=1)) / len(block))
        output.append(values)
    return output


def build_attention_mask(
    tokens,
    *,
    mode: str,
    heads: int,
    block_size: int,
    local_blocks: int = 1,
    random_edges: int = 2,
):
    """Construct dense, BigBird or paper-faithful gzip block masks."""
    import torch

    batch, length = tokens.shape
    blocks = math.ceil(length / block_size)
    block_positions = torch.arange(length, device=tokens.device) // block_size
    query_blocks = block_positions[:, None]
    key_blocks = block_positions[None, :]
    causal = torch.arange(length, device=tokens.device)[None, :] <= torch.arange(
        length, device=tokens.device
    )[:, None]
    local = (query_blocks - key_blocks).abs() <= local_blocks
    masks = torch.zeros(
        batch, heads, length, length, dtype=torch.bool, device=tokens.device
    )
    if mode == "dense":
        masks[:] = causal
        return masks
    if mode == "bigbird":
        generator = torch.Generator(device="cpu").manual_seed(20260727)
        block_mask = torch.eye(blocks, dtype=torch.bool)
        for query in range(blocks):
            left, right = max(0, query - local_blocks), min(blocks, query + local_blocks + 1)
            block_mask[query, left:right] = True
            block_mask[query, ::8] = True
            choices = torch.randperm(blocks, generator=generator)[:random_edges]
            block_mask[query, choices] = True
        token_mask = block_mask.to(tokens.device)[query_blocks, key_blocks] & causal
        masks[:] = token_mask
        return masks
    if mode != "gzip":
        raise ValueError(f"unsupported attention mode: {mode}")

    ratios = compression_ratios(tokens, block_size)
    local_heads = heads // 2
    long_heads = max(1, heads // 4)
    for row, values in enumerate(ratios):
        ratio_tensor = torch.tensor(values, device=tokens.device)
        literal = ratio_tensor > ratio_tensor.mean()
        literal_tokens = literal[block_positions]
        long_range = literal_tokens[:, None] & literal_tokens[None, :]
        long_range |= query_blocks == key_blocks
        masks[row, :local_heads] = local & causal
        masks[row, local_heads : local_heads + long_heads] = long_range & causal
        masks[row, local_heads + long_heads :] = (local | long_range) & causal
    return masks


def build_model(config: GzipLMConfig, mode: str):
    import torch
    from torch import nn

    class MaskedAttention(nn.Module):
        def __init__(self):
            super().__init__()
            self.qkv = nn.Linear(config.dimensions, 3 * config.dimensions, bias=False)
            self.output = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.head_dim = config.dimensions // config.heads

        def forward(self, values, mask):
            batch, length, _ = values.shape
            qkv = self.qkv(values).view(
                batch, length, 3, config.heads, self.head_dim
            )
            query, key, value = (
                qkv[:, :, index].transpose(1, 2) for index in range(3)
            )
            scores = query @ key.transpose(-2, -1) / math.sqrt(self.head_dim)
            scores = scores.masked_fill(~mask, torch.finfo(scores.dtype).min)
            mixed = torch.softmax(scores, dim=-1) @ value
            return self.output(mixed.transpose(1, 2).reshape(batch, length, -1))

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.attention_norm = nn.RMSNorm(config.dimensions)
            self.attention = MaskedAttention()
            self.mlp_norm = nn.RMSNorm(config.dimensions)
            self.mlp = nn.Sequential(
                nn.Linear(config.dimensions, 4 * config.dimensions),
                nn.GELU(),
                nn.Linear(4 * config.dimensions, config.dimensions),
            )

        def forward(self, values, mask):
            values = values + self.attention(self.attention_norm(values), mask)
            return values + self.mlp(self.mlp_norm(values))

    class ByteLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.mode = mode
            self.token = nn.Embedding(256, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            self.blocks = nn.ModuleList(Block() for _ in range(config.layers))
            self.norm = nn.RMSNorm(config.dimensions)
            self.output = nn.Linear(config.dimensions, 256, bias=False)
            self.output.weight = self.token.weight

        def forward(self, tokens):
            positions = torch.arange(tokens.shape[1], device=tokens.device)
            values = self.token(tokens) + self.position(positions)[None]
            mask = build_attention_mask(
                tokens,
                mode=self.mode,
                heads=config.heads,
                block_size=config.block_size,
                local_blocks=config.local_blocks,
            )
            for block in self.blocks:
                values = block(values, mask)
            return self.output(self.norm(values))

    return ByteLM()
