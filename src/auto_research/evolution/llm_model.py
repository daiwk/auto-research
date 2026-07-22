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
    residual_streams: int = 2
    sinkhorn_iterations: int = 10


def build_micro_lm(architecture: str, config: MicroLMConfig):
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError("LLM evolution requires pip install -e '.[llm-evolution]'") from exc
    supported = {
        "gpt_baseline", "gpt_gqa", "llama_modern", "llama_gqa",
        "parallel_gelu", "parallel_swiglu", "llama_gqa_parallel",
        "hyper_connections", "mhc", "qkv_depthwise_conv",
    }
    if architecture not in supported:
        raise ValueError(f"unknown micro LLM architecture: {architecture}")
    modern = architecture.startswith("llama") or architecture in {
        "hyper_connections", "mhc", "qkv_depthwise_conv",
    }
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
            qkv_width = config.heads * head_dim + 2 * kv_heads * head_dim
            self.qkv_conv = (
                nn.Conv1d(qkv_width, qkv_width, kernel_size=3, groups=qkv_width, bias=True)
                if architecture == "qkv_depthwise_conv" else None
            )

        def forward(self, values):
            batch, length, _ = values.shape
            q, k, v = self.q(values), self.k(values), self.v(values)
            if self.qkv_conv is not None:
                projected = torch.cat((q, k, v), dim=-1)
                # Left padding keeps the augmentation autoregressive.  The paper's
                # best P5 block is a linear residual depthwise Conv1D with k=3.
                local = self.qkv_conv(torch.nn.functional.pad(projected.transpose(1, 2), (2, 0)))
                q, k, v = torch.split(
                    projected + local.transpose(1, 2),
                    (config.heads * head_dim, kv_heads * head_dim, kv_heads * head_dim),
                    dim=-1,
                )
            q = q.view(batch, length, config.heads, head_dim).transpose(1, 2)
            k = k.view(batch, length, kv_heads, head_dim).transpose(1, 2)
            v = v.view(batch, length, kv_heads, head_dim).transpose(1, 2)
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

    class HyperLayer(nn.Module):
        """Paper-faithful dynamic HC/mHC wrapper around one Transformer sublayer."""

        def __init__(self, function):
            super().__init__()
            streams = config.residual_streams
            self.function = function
            self.function_norm = norm()
            self.mapping_norm = nn.RMSNorm(streams * config.dimensions)
            self.dynamic = nn.Linear(
                streams * config.dimensions, streams * streams + 2 * streams,
                bias=False,
            )
            self.pre_bias = nn.Parameter(torch.zeros(streams))
            self.post_bias = nn.Parameter(torch.zeros(streams))
            self.residual_bias = nn.Parameter(torch.eye(streams))
            self.dynamic_scale = nn.Parameter(torch.tensor(0.01))

        def mappings(self, values):
            streams = config.residual_streams
            flat = self.mapping_norm(values.flatten(-2))
            raw = self.dynamic_scale * self.dynamic(flat)
            pre_raw, post_raw, residual_raw = torch.split(
                raw, (streams, streams, streams * streams), dim=-1
            )
            residual_raw = residual_raw.view(*values.shape[:-2], streams, streams)
            if architecture == "mhc":
                pre = torch.sigmoid(pre_raw + self.pre_bias)
                post = 2.0 * torch.sigmoid(post_raw + self.post_bias)
                residual = _sinkhorn(
                    residual_raw + self.residual_bias,
                    config.sinkhorn_iterations,
                    torch,
                )
            else:
                pre = pre_raw + torch.softmax(self.pre_bias, dim=-1)
                post = post_raw + torch.ones_like(self.post_bias)
                residual = residual_raw + self.residual_bias
            return pre, post, residual

        def forward(self, values):
            pre, post, residual = self.mappings(values)
            function_input = torch.einsum("...s,...sd->...d", pre, values)
            update = self.function(self.function_norm(function_input))
            carried = torch.einsum("...ij,...jd->...id", residual, values)
            return carried + post.unsqueeze(-1) * update.unsqueeze(-2)

    class HyperBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.attention = HyperLayer(Attention())
            self.ffn = HyperLayer(FFN())

        def forward(self, values):
            return self.ffn(self.attention(values))

    class MicroLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.token = nn.Embedding(config.vocab_size, config.dimensions)
            self.position = None if modern else nn.Embedding(config.sequence_length, config.dimensions)
            hyper = architecture in {"hyper_connections", "mhc"}
            self.blocks = nn.ModuleList([
                HyperBlock() if hyper else Block() for _ in range(config.layers)
            ])
            self.final_norm = norm()
            self.output = nn.Linear(config.dimensions, config.vocab_size, bias=False)
            self.output.weight = self.token.weight
            self.memory = None
            self.memory_layer = 0
            self.apply(self._initialize)

        @staticmethod
        def _initialize(module):
            if isinstance(module, (nn.Linear, nn.Embedding, nn.Conv1d)):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)
                if getattr(module, "bias", None) is not None:
                    nn.init.zeros_(module.bias)

        def attach_memory(self, module, layer: int = 0):
            self.memory = module
            self.memory_layer = layer

        def hidden(self, tokens, embedding_noise_alpha: float = 0.0):
            values = self.token(tokens)
            if self.position is not None:
                positions = torch.arange(tokens.shape[1], device=tokens.device)
                values = values + self.position(positions)[None]
            if embedding_noise_alpha and self.training:
                scale = embedding_noise_alpha / math.sqrt(values.shape[1] * values.shape[2])
                values = values + torch.empty_like(values).uniform_(-scale, scale)
            hyper = architecture in {"hyper_connections", "mhc"}
            if hyper:
                values = values.unsqueeze(-2).expand(
                    *values.shape[:-1], config.residual_streams, values.shape[-1]
                ).contiguous()
            for index, block in enumerate(self.blocks):
                values = block(values)
                if self.memory is not None and index == self.memory_layer:
                    values = self.memory(tokens, values)
            if hyper:
                values = values.mean(dim=-2)
            return self.final_norm(values)

        def forward(self, tokens, embedding_noise_alpha: float = 0.0):
            return self.output(self.hidden(tokens, embedding_noise_alpha))

        def connection_stats(self, tokens):
            if architecture not in {"hyper_connections", "mhc"}:
                return {}
            values = self.token(tokens).unsqueeze(-2).expand(
                *tokens.shape, config.residual_streams, config.dimensions
            ).contiguous()
            residuals = []
            for block in self.blocks:
                for layer in (block.attention, block.ffn):
                    _, _, residual = layer.mappings(values)
                    residuals.append(residual)
                    values = layer(values)
            matrices = torch.cat([row.reshape(-1, config.residual_streams, config.residual_streams) for row in residuals])
            matrices_cpu = matrices.detach().float().cpu()
            return {
                "row_sum_error": float((matrices_cpu.sum(-1) - 1).abs().max()),
                "column_sum_error": float((matrices_cpu.sum(-2) - 1).abs().max()),
                "spectral_norm_max": float(torch.linalg.matrix_norm(matrices_cpu, ord=2).max()),
            }

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


def _sinkhorn(logits, iterations, torch):
    values = torch.exp(logits - logits.amax(dim=(-2, -1), keepdim=True))
    for _ in range(iterations):
        values = values / values.sum(dim=-1, keepdim=True).clamp_min(1e-8)
        values = values / values.sum(dim=-2, keepdim=True).clamp_min(1e-8)
    return values
