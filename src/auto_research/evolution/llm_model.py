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
        "mobius_rope", "naju", "adadsf", "engram",
        "looped_latent_attention", "gaugequant",
        "switch_transformer", "mamba", "switch_attention",
        "native_sparse_attention", "gated_attention",
        "nsa_gated_attention",
    }
    if architecture not in supported:
        raise ValueError(f"unknown micro LLM architecture: {architecture}")
    modern = architecture.startswith("llama") or architecture in {
        "hyper_connections", "mhc", "qkv_depthwise_conv", "mobius_rope", "naju",
        "adadsf", "engram", "looped_latent_attention", "gaugequant",
        "switch_transformer", "mamba", "switch_attention",
        "native_sparse_attention", "gated_attention",
        "nsa_gated_attention",
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
            self.switch_router = (
                nn.Linear(config.dimensions, 1)
                if architecture == "switch_attention" else None
            )
            self.output_gate = (
                nn.Linear(config.dimensions, config.heads)
                if architecture == "gated_attention" else None
            )
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
                q, k = _rotary(
                    q, k, torch,
                    mode="mobius" if architecture == "mobius_rope" else "standard",
                    context_length=config.sequence_length,
                )
            if kv_heads != config.heads:
                repeats = config.heads // kv_heads
                k = k.repeat_interleave(repeats, dim=1)
                v = v.repeat_interleave(repeats, dim=1)
            mixed = torch.nn.functional.scaled_dot_product_attention(
                q, k, v, is_causal=True
            )
            if self.output_gate is not None:
                gate = torch.sigmoid(
                    self.output_gate(values).transpose(1, 2).unsqueeze(-1)
                )
                mixed = mixed * gate
                self.last_gate_mean = float(gate.detach().mean().cpu())
                self.last_gate_below_half = float(
                    (gate.detach() < 0.5).float().mean().cpu()
                )
            if self.switch_router is not None:
                positions = torch.arange(length, device=values.device)
                local_mask = (
                    (positions[None, :] <= positions[:, None])
                    & (positions[None, :] >= positions[:, None] - 15)
                )
                local = torch.nn.functional.scaled_dot_product_attention(
                    q, k, v, attn_mask=local_mask, is_causal=False
                )
                route = torch.sigmoid(self.switch_router(values))
                route = route.transpose(1, 2).unsqueeze(-1)
                mixed = route * mixed + (1.0 - route) * local
                self.last_full_attention_rate = float(route.detach().mean().cpu())
            return self.output(mixed.transpose(1, 2).reshape(batch, length, config.dimensions))

    class LoopedLatentAttention(nn.Module):
        """Weight-tied attention whose K/V cache is stored in a shared latent basis."""

        def __init__(self):
            super().__init__()
            latent = max(4, head_dim // 2)
            self.latent = latent
            self.q = nn.Linear(config.dimensions, config.heads * head_dim, bias=False)
            self.k_down = nn.Linear(config.dimensions, config.kv_heads * latent, bias=False)
            self.v_down = nn.Linear(config.dimensions, config.kv_heads * latent, bias=False)
            self.k_up = nn.Parameter(torch.empty(config.kv_heads, latent, head_dim))
            self.v_up = nn.Parameter(torch.empty(config.kv_heads, latent, head_dim))
            self.output = nn.Linear(config.dimensions, config.dimensions, bias=False)
            nn.init.normal_(self.k_up, std=0.02)
            nn.init.normal_(self.v_up, std=0.02)
            self.last_cache_compression = head_dim / latent

        def forward(self, values):
            batch, length, _ = values.shape
            q = self.q(values).view(
                batch, length, config.heads, head_dim
            ).transpose(1, 2)
            k_latent = self.k_down(values).view(
                batch, length, config.kv_heads, self.latent
            ).transpose(1, 2)
            v_latent = self.v_down(values).view(
                batch, length, config.kv_heads, self.latent
            ).transpose(1, 2)
            k = torch.einsum("bhsl,hld->bhsd", k_latent, self.k_up)
            v = torch.einsum("bhsl,hld->bhsd", v_latent, self.v_up)
            if config.kv_heads != config.heads:
                repeats = config.heads // config.kv_heads
                k = k.repeat_interleave(repeats, dim=1)
                v = v.repeat_interleave(repeats, dim=1)
            q, k = _rotary(
                q, k, torch, mode="standard",
                context_length=config.sequence_length,
            )
            mixed = torch.nn.functional.scaled_dot_product_attention(
                q, k, v, is_causal=True
            )
            return self.output(
                mixed.transpose(1, 2).reshape(batch, length, config.dimensions)
            )

    class GaugeQuantizer(nn.Module):
        """Learn an equivalent channel basis and execute an STE W4/A4 path."""

        def __init__(self):
            super().__init__()
            self.generator = nn.Parameter(
                torch.randn(config.dimensions) * 0.02
            )
            self.last_outlier = 0.0
            self.outlier_loss = None

        def _basis(self):
            vector = self.generator
            unit = vector / vector.norm().clamp_min(1e-6)
            eye = torch.eye(
                config.dimensions, dtype=vector.dtype, device=vector.device
            )
            return eye - 2.0 * unit[:, None] * unit[None, :]

        @staticmethod
        def _fake_quantize(values, bits=4):
            bound = 2 ** (bits - 1) - 1
            scale = values.detach().abs().amax(dim=-1, keepdim=True).clamp_min(1e-6)
            quantized = torch.round(values / scale * bound).clamp(-bound, bound)
            restored = quantized * scale / bound
            return values + (restored - values).detach()

        def forward(self, values):
            basis = self._basis()
            rotated = values @ basis
            self.outlier_loss = torch.logsumexp(
                rotated.abs(), dim=-1
            ).mean()
            self.last_outlier = float(self.outlier_loss.detach().cpu())
            return self._fake_quantize(rotated) @ basis.T

        def regularizer(self):
            if self.outlier_loss is None:
                return self.generator.sum() * 0.0
            # The online objective directly penalizes activation outliers.
            return 1e-3 * self.outlier_loss

    class ConditionalMemory(nn.Module):
        """Engram-style deterministic hashed n-gram lookup with gated fusion."""

        def __init__(self, buckets=4096):
            super().__init__()
            self.buckets = buckets
            self.table = nn.Embedding(buckets, config.dimensions)
            self.norm = RMSNorm()
            self.gate = nn.Linear(2 * config.dimensions, config.dimensions)
            nn.init.normal_(self.table.weight, std=0.02)

        def forward(self, tokens, values):
            previous = torch.nn.functional.pad(tokens[:, :-1], (1, 0))
            previous2 = torch.nn.functional.pad(tokens[:, :-2], (2, 0))
            address = (
                tokens.long() * 1_000_003
                + previous.long() * 9_176
                + previous2.long() * 131
            ) % self.buckets
            memory = self.table(address)
            gate = torch.sigmoid(self.gate(torch.cat((values, memory), dim=-1)))
            return values + gate * self.norm(memory)

    class FFN(nn.Module):
        def __init__(self):
            super().__init__()
            width = config.expansion * config.dimensions
            if architecture == "switch_transformer":
                self.router = nn.Linear(config.dimensions, 4, bias=False)
                self.experts = nn.ModuleList(
                    [
                        nn.Sequential(
                            nn.Linear(config.dimensions, width, bias=False),
                            nn.ReLU(),
                            nn.Linear(width, config.dimensions, bias=False),
                        )
                        for _ in range(4)
                    ]
                )
                self.last_balance_loss = None
            elif modern or architecture == "parallel_swiglu":
                self.up = nn.Linear(config.dimensions, width, bias=False)
                self.gate = nn.Linear(config.dimensions, width, bias=False)
                self.down = nn.Linear(width, config.dimensions, bias=False)
            else:
                self.network = nn.Sequential(
                    nn.Linear(config.dimensions, width), nn.GELU(),
                    nn.Linear(width, config.dimensions),
                )

        def forward(self, values):
            if hasattr(self, "experts"):
                probability = torch.softmax(self.router(values), dim=-1)
                selected = probability.argmax(-1)
                outputs = torch.stack(
                    [expert(values) for expert in self.experts], dim=-2
                )
                dispatch = torch.nn.functional.one_hot(
                    selected, len(self.experts)
                ).to(values.dtype)
                gate = (dispatch * probability).sum(-1, keepdim=True)
                mixed = (dispatch.unsqueeze(-1) * outputs).sum(-2)
                load = dispatch.float().mean(dim=(0, 1))
                importance = probability.float().mean(dim=(0, 1))
                self.last_balance_loss = len(self.experts) * (load * importance).sum()
                return gate * mixed
            if hasattr(self, "network"):
                return self.network(values)
            return self.down(torch.nn.functional.silu(self.gate(values)) * self.up(values))

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.first_norm, self.second_norm = norm(), norm()
            if architecture == "looped_latent_attention":
                self.attention = LoopedLatentAttention()
            elif architecture in {
                "native_sparse_attention", "nsa_gated_attention"
            }:
                from .llm_attention_2025 import build_native_sparse_attention

                self.attention = build_native_sparse_attention(
                    torch=torch,
                    nn=nn,
                    config=config,
                    head_dim=head_dim,
                    rotary=_rotary,
                    gated=architecture == "nsa_gated_attention",
                )
            else:
                self.attention = Attention()
            self.ffn = FFN()

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

    class NajuBlock(nn.Module):
        """Native-discrete selective SSM with independent retain/write gates."""

        def __init__(self):
            super().__init__()
            dimensions = config.dimensions
            self.inner = 2 * dimensions
            self.state_size = max(8, dimensions // config.heads)
            self.norm = RMSNorm()
            self.input = nn.Linear(dimensions, 2 * self.inner, bias=False)
            self.content_conv = nn.Conv1d(
                self.inner, self.inner, kernel_size=3, groups=self.inner, bias=True
            )
            self.forget = nn.Linear(self.inner, self.inner)
            self.write = nn.Linear(self.inner, self.inner)
            self.forget_conv = nn.Conv1d(
                self.inner, self.inner, kernel_size=3, groups=self.inner, bias=False
            )
            self.write_conv = nn.Conv1d(
                self.inner, self.inner, kernel_size=3, groups=self.inner, bias=False
            )
            self.bc = nn.Linear(self.inner, 2 * self.state_size, bias=False)
            self.feedthrough = nn.Parameter(torch.full((self.inner,), 0.01))
            self.output = nn.Linear(self.inner, dimensions, bias=False)
            self.readout_scale = self.state_size ** -0.5
            nn.init.constant_(self.forget.bias, 5.0)
            nn.init.constant_(self.write.bias, -2.0)
            self.last_gate_statistics = {}

        @staticmethod
        def _causal_convolution(module, values):
            width = module.kernel_size[0] - 1
            return module(torch.nn.functional.pad(values.transpose(1, 2), (width, 0))).transpose(1, 2)

        def forward(self, values):
            content, modulation = self.input(self.norm(values)).chunk(2, dim=-1)
            content = torch.nn.functional.silu(
                self._causal_convolution(self.content_conv, content)
            )
            forget = torch.sigmoid(
                self.forget(content)
                + self._causal_convolution(self.forget_conv, content)
            )
            write = torch.sigmoid(
                self.write(content)
                + self._causal_convolution(self.write_conv, content)
            )
            direction_write, direction_read = self.bc(content).chunk(2, dim=-1)
            state = torch.zeros(
                values.shape[0], self.inner, self.state_size,
                dtype=values.dtype, device=values.device,
            )
            outputs = []
            for index in range(values.shape[1]):
                state = (
                    forget[:, index, :, None] * state
                    + write[:, index, :, None]
                    * content[:, index, :, None]
                    * direction_write[:, index, None, :]
                )
                memory = torch.einsum(
                    "bis,bs->bi", state, direction_read[:, index]
                ) * self.readout_scale
                outputs.append(memory + self.feedthrough * content[:, index])
            mixed = torch.stack(outputs, dim=1)
            self.last_gate_statistics = {
                "forget_mean": float(forget.detach().mean().cpu()),
                "write_mean": float(write.detach().mean().cpu()),
                "gate_correlation": float(_correlation(forget, write, torch)),
            }
            return values + self.output(
                mixed * torch.nn.functional.silu(modulation)
            )

    class MambaBlock(nn.Module):
        """Input-dependent selective state-space recurrence (Mamba core)."""

        def __init__(self):
            super().__init__()
            d = config.dimensions
            self.norm = RMSNorm()
            self.input = nn.Linear(d, 2 * d, bias=False)
            self.conv = nn.Conv1d(d, d, 4, groups=d)
            self.delta = nn.Linear(d, d)
            self.b = nn.Linear(d, d)
            self.c = nn.Linear(d, d)
            self.a_log = nn.Parameter(torch.zeros(d))
            self.skip = nn.Parameter(torch.ones(d))
            self.output = nn.Linear(d, d, bias=False)
            self.last_selectivity = 0.0

        def forward(self, values):
            content, gate = self.input(self.norm(values)).chunk(2, dim=-1)
            content = self.conv(
                torch.nn.functional.pad(content.transpose(1, 2), (3, 0))
            ).transpose(1, 2)
            content = torch.nn.functional.silu(content)
            delta = torch.nn.functional.softplus(self.delta(content))
            decay = torch.exp(-delta * torch.exp(self.a_log))
            write = delta * self.b(content) * content
            read = self.c(content)
            state = torch.zeros_like(content[:, 0])
            outputs = []
            for index in range(content.shape[1]):
                state = decay[:, index] * state + write[:, index]
                outputs.append(read[:, index] * state + self.skip * content[:, index])
            self.last_selectivity = float(delta.detach().std().cpu())
            mixed = torch.stack(outputs, dim=1)
            return values + self.output(
                mixed * torch.nn.functional.silu(gate)
            )

    class MicroLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.token = nn.Embedding(config.vocab_size, config.dimensions)
            self.position = None if modern else nn.Embedding(config.sequence_length, config.dimensions)
            hyper = architecture in {"hyper_connections", "mhc"}
            if architecture == "looped_latent_attention":
                shared_loop = Block()
                self.blocks = nn.ModuleList(
                    [shared_loop for _ in range(config.layers)]
                )
            else:
                self.blocks = nn.ModuleList([
                    (
                        HyperBlock()
                        if hyper
                        else NajuBlock()
                        if architecture == "naju"
                        else MambaBlock()
                        if architecture == "mamba"
                        else Block()
                    )
                    for _ in range(config.layers)
                ])
            self.final_norm = norm()
            self.output = nn.Linear(config.dimensions, config.vocab_size, bias=False)
            self.output.weight = self.token.weight
            self.memory = None
            self.memory_layer = 0
            self.conditional_memory = (
                ConditionalMemory() if architecture == "engram" else None
            )
            self.gauge_quantizer = (
                GaugeQuantizer() if architecture == "gaugequant" else None
            )
            self.apply(self._initialize)
            if architecture == "naju":
                for block in self.blocks:
                    nn.init.constant_(block.forget.bias, 5.0)
                    nn.init.constant_(block.write.bias, -2.0)
                    nn.init.constant_(block.feedthrough, 0.01)

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
                if self.gauge_quantizer is not None:
                    values = self.gauge_quantizer(values)
                values = block(values)
                if self.conditional_memory is not None and index == 0:
                    values = self.conditional_memory(tokens, values)
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

        def sequence_mixer_stats(self):
            if architecture != "naju":
                return {}
            rows = [block.last_gate_statistics for block in self.blocks]
            if not rows or not all(rows):
                return {}
            return {
                key: float(sum(row[key] for row in rows) / len(rows))
                for key in rows[0]
            }

        def architecture_stats(self):
            if architecture == "engram":
                return {
                    "lookup_complexity": "O(1)",
                    "memory_buckets": self.conditional_memory.buckets,
                }
            if architecture == "looped_latent_attention":
                return {
                    "weight_tied": True,
                    "kv_cache_compression_x": self.blocks[0].attention.last_cache_compression,
                }
            if architecture == "gaugequant":
                return {
                    "weight_bits": 4,
                    "activation_bits": 4,
                    "logsumexp_outlier": self.gauge_quantizer.last_outlier,
                }
            if architecture == "switch_transformer":
                losses = [
                    block.ffn.last_balance_loss
                    for block in self.blocks
                    if block.ffn.last_balance_loss is not None
                ]
                return {
                    "experts": 4,
                    "active_experts_per_token": 1,
                    "load_balance_loss": (
                        float(torch.stack(losses).mean().detach().cpu())
                        if losses else 0.0
                    ),
                }
            if architecture == "mamba":
                return {
                    "selective_scan": True,
                    "attention_layers": 0,
                    "delta_std": sum(
                        block.last_selectivity for block in self.blocks
                    ) / len(self.blocks),
                }
            if architecture == "switch_attention":
                return {
                    "routing_granularity": "token-layer",
                    "full_attention_rate": sum(
                        block.attention.last_full_attention_rate
                        for block in self.blocks
                    ) / len(self.blocks),
                    "local_window": 16,
                }
            if architecture in {
                "native_sparse_attention", "nsa_gated_attention"
            }:
                rows = [
                    block.attention.last_statistics
                    for block in self.blocks
                    if block.attention.last_statistics
                ]
                if not rows:
                    return {}
                numeric = {
                    key: sum(float(row[key]) for row in rows) / len(rows)
                    for key in rows[0]
                }
                numeric["reference_kernel"] = "pytorch"
                return numeric
            if architecture == "gated_attention":
                return {
                    "gate_position": "after_sdpa_per_head",
                    "output_gate_mean": sum(
                        block.attention.last_gate_mean
                        for block in self.blocks
                    ) / len(self.blocks),
                    "output_gate_below_0_5": sum(
                        block.attention.last_gate_below_half
                        for block in self.blocks
                    ) / len(self.blocks),
                }
            return {}

        def auxiliary_loss(self):
            losses = []
            if self.gauge_quantizer is not None:
                losses.append(self.gauge_quantizer.regularizer())
            if architecture == "switch_transformer":
                losses.extend(
                    1e-2 * block.ffn.last_balance_loss
                    for block in self.blocks
                    if block.ffn.last_balance_loss is not None
                )
            return (
                sum(losses)
                if losses
                else self.token.weight.sum() * 0.0
            )

    return MicroLM()


def _rotary(q, k, torch, *, mode: str = "standard", context_length: int | None = None):
    length, width = q.shape[-2], q.shape[-1]
    half = width // 2
    standard = 1.0 / (
        10000 ** (torch.arange(half, device=q.device, dtype=q.dtype) / half)
    )
    def rotate(values):
        frequencies = standard[None].expand(values.shape[1], -1).clone()
        if mode == "mobius":
            if not context_length:
                raise ValueError("Möbius RoPE requires a fixed training context length")
            special_heads = max(1, values.shape[1] // 4)
            anti_periodic = (
                math.pi
                * (2 * torch.arange(half, device=q.device, dtype=q.dtype) + 1)
                / context_length
            )
            frequencies[:special_heads] = anti_periodic
        angles = (
            torch.arange(length, device=q.device, dtype=q.dtype)[:, None, None]
            * frequencies[None]
        )
        cos = angles.cos().permute(1, 0, 2)[None]
        sin = angles.sin().permute(1, 0, 2)[None]
        left, right = values[..., :half], values[..., half:half * 2]
        return torch.cat((left * cos - right * sin, left * sin + right * cos, values[..., half * 2:]), dim=-1)

    return rotate(q), rotate(k)


def _correlation(left, right, torch):
    left = left.detach().float().flatten()
    right = right.detach().float().flatten()
    left = left - left.mean()
    right = right - right.mean()
    denominator = left.square().sum().sqrt() * right.square().sum().sqrt()
    if float(denominator) == 0.0:
        return torch.tensor(0.0)
    return (left * right).sum() / denominator


def _sinkhorn(logits, iterations, torch):
    values = torch.exp(logits - logits.amax(dim=(-2, -1), keepdim=True))
    for _ in range(iterations):
        values = values / values.sum(dim=-1, keepdim=True).clamp_min(1e-8)
        values = values / values.sum(dim=-2, keepdim=True).clamp_min(1e-8)
    return values
