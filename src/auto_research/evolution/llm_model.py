from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class MicroLMConfig:
    vocab_size: int
    dimensions: int = 128
    layers: int = 2
    heads: int = 4
    kv_heads: int = 4
    sequence_length: int = 128
    expansion: int = 4


def build_micro_lm(architecture: str, config: MicroLMConfig):
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError("LLM evolution requires pip install -e '.[llm-evolution]'") from exc
    supported = {
        "gpt_baseline", "gpt_gqa", "llama_modern", "llama_gqa",
        "parallel_gelu", "parallel_swiglu", "llama_gqa_parallel",
    }
    if architecture not in supported:
        raise ValueError(f"unknown micro LLM architecture: {architecture}")
    modern = architecture.startswith("llama")
    parallel = "parallel" in architecture
    kv_heads = 2 if "gqa" in architecture else config.heads
    if config.dimensions % config.heads or config.heads % kv_heads:
        raise ValueError("dimensions/heads and heads/kv_heads must be divisible")
    head_dim = config.dimensions // config.heads

    class RMSNorm(nn.Module):
        def __init__(self):
            super().__init__()
            self.weight = nn.Parameter(torch.ones(config.dimensions))

        def forward(self, values):
            return values * torch.rsqrt(values.pow(2).mean(-1, keepdim=True) + 1e-6) * self.weight

    def norm():
        return RMSNorm() if modern else nn.LayerNorm(config.dimensions)

    class Attention(nn.Module):
        def __init__(self):
            super().__init__()
            self.q = nn.Linear(config.dimensions, config.heads * head_dim, bias=not modern)
            self.k = nn.Linear(config.dimensions, kv_heads * head_dim, bias=not modern)
            self.v = nn.Linear(config.dimensions, kv_heads * head_dim, bias=not modern)
            self.output = nn.Linear(config.dimensions, config.dimensions, bias=not modern)

        def forward(self, values):
            batch, length, _ = values.shape
            q = self.q(values).view(batch, length, config.heads, head_dim).transpose(1, 2)
            k = self.k(values).view(batch, length, kv_heads, head_dim).transpose(1, 2)
            v = self.v(values).view(batch, length, kv_heads, head_dim).transpose(1, 2)
            if modern:
                q, k = _rotary(q, k, torch)
            if kv_heads != config.heads:
                repeats = config.heads // kv_heads
                k = k.repeat_interleave(repeats, dim=1)
                v = v.repeat_interleave(repeats, dim=1)
            mixed = torch.nn.functional.scaled_dot_product_attention(q, k, v, is_causal=True)
            return self.output(mixed.transpose(1, 2).reshape(batch, length, config.dimensions))

    class FFN(nn.Module):
        def __init__(self):
            super().__init__()
            width = config.expansion * config.dimensions
            if modern or architecture == "parallel_swiglu":
                self.up = nn.Linear(config.dimensions, width, bias=False)
                self.gate = nn.Linear(config.dimensions, width, bias=False)
                self.down = nn.Linear(width, config.dimensions, bias=False)
            else:
                self.network = nn.Sequential(
                    nn.Linear(config.dimensions, width), nn.GELU(),
                    nn.Linear(width, config.dimensions),
                )

        def forward(self, values):
            if hasattr(self, "network"):
                return self.network(values)
            return self.down(torch.nn.functional.silu(self.gate(values)) * self.up(values))

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.first_norm, self.second_norm = norm(), norm()
            self.attention, self.ffn = Attention(), FFN()

        def forward(self, values):
            if parallel:
                normalized = self.first_norm(values)
                return values + self.attention(normalized) + self.ffn(normalized)
            values = values + self.attention(self.first_norm(values))
            return values + self.ffn(self.second_norm(values))

    class MicroLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.token = nn.Embedding(config.vocab_size, config.dimensions)
            self.position = None if modern else nn.Embedding(config.sequence_length, config.dimensions)
            self.blocks = nn.ModuleList([Block() for _ in range(config.layers)])
            self.final_norm = norm()
            self.output = nn.Linear(config.dimensions, config.vocab_size, bias=False)
            self.output.weight = self.token.weight
            self.apply(self._initialize)

        @staticmethod
        def _initialize(module):
            if isinstance(module, (nn.Linear, nn.Embedding)):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if getattr(module, "bias", None) is not None:
                    nn.init.zeros_(module.bias)

        def forward(self, tokens, embedding_noise_alpha: float = 0.0):
            values = self.token(tokens)
            if self.position is not None:
                positions = torch.arange(tokens.shape[1], device=tokens.device)
                values = values + self.position(positions)[None]
            if embedding_noise_alpha and self.training:
                scale = embedding_noise_alpha / math.sqrt(values.shape[1] * values.shape[2])
                values = values + torch.empty_like(values).uniform_(-scale, scale)
            for block in self.blocks:
                values = block(values)
            return self.output(self.final_norm(values))

    return MicroLM()


def _rotary(q, k, torch):
    length, width = q.shape[-2], q.shape[-1]
    half = width // 2
    frequencies = 1.0 / (10000 ** (torch.arange(half, device=q.device, dtype=q.dtype) / half))
    angles = torch.arange(length, device=q.device, dtype=q.dtype)[:, None] * frequencies[None]
    cos, sin = angles.cos()[None, None], angles.sin()[None, None]

    def rotate(values):
        left, right = values[..., :half], values[..., half:half * 2]
        return torch.cat((left * cos - right * sin, left * sin + right * cos, values[..., half * 2:]), dim=-1)

    return rotate(q), rotate(k)
