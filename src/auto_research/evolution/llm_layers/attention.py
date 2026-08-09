from __future__ import annotations

import math

from .common import _correlation, _rotary, _sinkhorn


def build_attention_layers(torch, nn, config, architecture, modern, parallel, kv_heads, head_dim):
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
            self.width_router = (
                nn.Linear(config.dimensions, config.heads, bias=False)
                if architecture == "wide_dynamic_width" else None
            )
            self.retoken = (
                nn.Parameter(torch.zeros(config.heads, head_dim))
                if architecture == "retoken" else None
            )
            self.retoken_projection = (
                nn.Linear(head_dim, head_dim, bias=False)
                if architecture == "retoken" else None
            )
            self.last_retoken_keep_rate = 1.0
            self.last_active_head_fraction = 1.0
            qkv_width = config.heads * head_dim + 2 * kv_heads * head_dim
            self.qkv_conv = (
                nn.Conv1d(qkv_width, qkv_width, kernel_size=3, groups=qkv_width, bias=True)
                if architecture == "qkv_depthwise_conv" else None
            )
            self.hybrid_ssm = (
                nn.Conv1d(
                    config.dimensions,
                    config.dimensions,
                    kernel_size=5,
                    groups=config.dimensions,
                )
                if architecture == "hymba" else None
            )
            self.hybrid_gate = (
                nn.Linear(config.dimensions, config.dimensions)
                if architecture == "hymba" else None
            )
            self.last_selected_block_fraction = 1.0

        def forward(self, values, value_values=None):
            batch, length, _ = values.shape
            value_values = values if value_values is None else value_values
            q, k, v = self.q(values), self.k(values), self.v(value_values)
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
            if modern and architecture != "alibi":
                q, k = _rotary(
                    q, k, torch,
                    mode="mobius" if architecture == "mobius_rope" else "standard",
                    context_length=config.sequence_length,
                )
            if kv_heads != config.heads:
                repeats = config.heads // kv_heads
                k = k.repeat_interleave(repeats, dim=1)
                v = v.repeat_interleave(repeats, dim=1)
            if architecture == "alibi":
                positions = torch.arange(length, device=values.device)
                distance = positions[:, None] - positions[None, :]
                slopes = torch.pow(
                    2.0,
                    -torch.linspace(1.0, 8.0, config.heads, device=values.device),
                )
                bias = -slopes[:, None, None] * distance.clamp_min(0)[None]
                bias = bias.masked_fill(
                    distance[None] < 0, float("-inf")
                )
                mixed = torch.nn.functional.scaled_dot_product_attention(
                    q, k, v, attn_mask=bias[None], is_causal=False
                )
            elif architecture == "moba":
                block = 8
                block_count = (length + block - 1) // block
                padded = block_count * block - length
                key_blocks = torch.nn.functional.pad(k, (0, 0, 0, padded)).view(
                    batch, config.heads, block_count, block, head_dim
                ).mean(3)
                route_scores = torch.einsum("bhld,bhkd->bhlk", q, key_blocks)
                query_positions = torch.arange(length, device=values.device)
                block_positions = torch.arange(block_count, device=values.device) * block
                causal_blocks = block_positions[None, :] <= query_positions[:, None]
                route_scores = route_scores.masked_fill(
                    ~causal_blocks[None, None], float("-inf")
                )
                keep = min(2, block_count)
                selected = route_scores.topk(keep, dim=-1).indices
                block_mask = torch.zeros_like(route_scores, dtype=torch.bool)
                block_mask.scatter_(-1, selected, True)
                token_blocks = torch.arange(length, device=values.device) // block
                token_mask = block_mask.gather(
                    -1,
                    token_blocks[None, None, None, :].expand(
                        batch, config.heads, length, length
                    ),
                )
                causal = torch.ones(length, length, device=values.device, dtype=torch.bool).tril()
                token_mask &= causal[None, None]
                attention_bias = torch.zeros_like(token_mask, dtype=q.dtype).masked_fill(
                    ~token_mask, float("-inf")
                )
                mixed = torch.nn.functional.scaled_dot_product_attention(
                    q, k, v, attn_mask=attention_bias, is_causal=False
                )
                self.last_selected_block_fraction = float(
                    block_mask.float().mean().detach().cpu()
                )
            elif self.retoken is not None:
                # RETOKEN scores the cached value vectors rather than the keys.
                # Here every causal query receives the same learned retrieval
                # target offset, and keeps up to half the maximum context (all
                # visible values for shorter prefixes). The straight-through mask lets
                # the one-token target and its projection learn from LM loss.
                retrieval_query = self.retoken_projection(
                    q + self.retoken[None, :, None, :]
                )
                relevance = torch.einsum(
                    "bhid,bhjd->bhij",
                    torch.nn.functional.normalize(retrieval_query, dim=-1),
                    torch.nn.functional.normalize(v, dim=-1),
                )
                causal = torch.ones(
                    length, length, device=values.device, dtype=torch.bool
                ).tril()
                relevance = relevance.masked_fill(~causal[None, None], -1e4)
                keep = max(1, length // 2)
                threshold = relevance.topk(keep, dim=-1).values[..., -1:]
                hard = (relevance >= threshold) & causal[None, None]
                soft = torch.sigmoid(relevance - threshold)
                retrieval_mask = hard.to(soft.dtype) + soft - soft.detach()
                attention_bias = torch.log(retrieval_mask.clamp_min(1e-6))
                attention_bias = attention_bias.masked_fill(
                    ~causal[None, None], float("-inf")
                )
                mixed = torch.nn.functional.scaled_dot_product_attention(
                    q, k, v, attn_mask=attention_bias, is_causal=False
                )
                self.last_retoken_keep_rate = float(
                    hard.float().sum().detach().cpu()
                    / causal.sum().clamp_min(1).detach().cpu()
                    / config.heads
                    / batch
                )
            else:
                mixed = torch.nn.functional.scaled_dot_product_attention(
                    q, k, v, is_causal=True
                )
            if self.width_router is not None:
                scores = self.width_router(values)
                keep = max(1, config.heads // 2)
                threshold = scores.topk(keep, dim=-1).values[..., -1:]
                hard = (scores >= threshold).to(scores.dtype)
                soft = torch.sigmoid(scores)
                mask = hard + soft - soft.detach()
                mixed = mixed * mask.transpose(1, 2).unsqueeze(-1)
                self.last_active_head_fraction = float(hard.mean().detach().cpu())
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
            mixed = self.output(
                mixed.transpose(1, 2).reshape(batch, length, config.dimensions)
            )
            if self.hybrid_ssm is not None:
                state = self.hybrid_ssm(
                    torch.nn.functional.pad(values.transpose(1, 2), (4, 0))
                ).transpose(1, 2)
                gate = torch.sigmoid(self.hybrid_gate(values))
                mixed = gate * mixed + (1.0 - gate) * state
                self.last_hybrid_gate = float(gate.detach().mean().cpu())
            return mixed

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
                self.width_router = (
                    nn.Linear(config.dimensions, 8, bias=False)
                    if architecture == "wide_dynamic_width" else None
                )
                self.last_active_channel_fraction = 1.0
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
            hidden = torch.nn.functional.silu(self.gate(values)) * self.up(values)
            if self.width_router is not None:
                scores = self.width_router(values)
                threshold = scores.topk(4, dim=-1).values[..., -1:]
                hard = (scores >= threshold).to(scores.dtype)
                soft = torch.sigmoid(scores)
                group_mask = hard + soft - soft.detach()
                channel_mask = group_mask.repeat_interleave(
                    hidden.shape[-1] // group_mask.shape[-1], dim=-1
                )
                hidden = hidden * channel_mask
                self.last_active_channel_fraction = float(hard.mean().detach().cpu())
            return self.down(hidden)
    return RMSNorm, norm, Attention, LoopedLatentAttention, GaugeQuantizer, ConditionalMemory, FFN
