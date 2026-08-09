from __future__ import annotations

import math

from .common import _correlation, _rotary, _sinkhorn


def build_model_class(torch, nn, config, architecture, modern, parallel, kv_heads, head_dim, RMSNorm, norm, Attention, LoopedLatentAttention, GaugeQuantizer, ConditionalMemory, FFN, Block, AttentionResidualBlock, HyperLayer, HyperBlock, LocalizedLatentRecurrence, NajuBlock, MambaBlock):
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
            elif architecture in {"block_attnres", "rd_attnres"}:
                self.blocks = nn.ModuleList([
                    AttentionResidualBlock(index + 1)
                    for index in range(config.layers)
                ])
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
            self.localized_recurrence = (
                LocalizedLatentRecurrence(steps=2)
                if architecture == "penelope" else None
            )
            self.byte_patch_gate = (
                nn.Linear(config.dimensions, 1)
                if architecture == "blt" else None
            )
            self.last_patch_rate = 1.0
            self.recurrence_layer = max(0, config.layers // 2 - 1)
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
            if self.byte_patch_gate is not None:
                # BLT's entropy patching is represented by a differentiable
                # boundary gate over byte/token surprisal. Adjacent low-entropy
                # positions share a latent patch, which is expanded back before
                # the byte decoder so the causal LM target stays unchanged.
                novelty = torch.ones_like(tokens, dtype=values.dtype)
                novelty[:, 1:] = (tokens[:, 1:] != tokens[:, :-1]).to(values.dtype)
                learned = torch.sigmoid(self.byte_patch_gate(values)).squeeze(-1)
                boundary = (0.65 * novelty + 0.35 * learned).clamp(0.0, 1.0)
                previous = torch.nn.functional.pad(values[:, :-1], (0, 0, 1, 0))
                values = boundary.unsqueeze(-1) * values + (
                    1.0 - boundary.unsqueeze(-1)
                ) * previous
                self.last_patch_rate = float(boundary.detach().mean().cpu())
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
            sources = [values]
            for index, block in enumerate(self.blocks):
                if self.gauge_quantizer is not None:
                    values = self.gauge_quantizer(values)
                values = (
                    block(sources)
                    if architecture in {"block_attnres", "rd_attnres"}
                    else block(values)
                )
                if architecture in {"block_attnres", "rd_attnres"}:
                    sources.append(values)
                if (
                    self.localized_recurrence is not None
                    and index == self.recurrence_layer
                ):
                    values = self.localized_recurrence(values)
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
            if architecture == "rope":
                return {"position_encoding": "rotary", "relative_phase": True}
            if architecture == "alibi":
                return {"position_encoding": "linear-attention-bias", "train_short_test_long": True}
            if architecture == "gqa":
                return {
                    "query_heads": config.heads,
                    "kv_heads": config.kv_heads,
                    "kv_cache_reduction_x": config.heads / config.kv_heads,
                }
            if architecture == "hymba":
                return {
                    "parallel_attention_ssm": True,
                    "hybrid_gate_mean": sum(
                        block.attention.last_hybrid_gate for block in self.blocks
                    ) / len(self.blocks),
                }
            if architecture == "moba":
                return {
                    "block_size": 8,
                    "selected_block_fraction": sum(
                        block.attention.last_selected_block_fraction for block in self.blocks
                    ) / len(self.blocks),
                }
            if architecture == "blt":
                return {
                    "tokenizer_free_reference": "dynamic byte patches",
                    "observed_patch_boundary_rate": self.last_patch_rate,
                    "expanded_back_to_byte_targets": True,
                }
            if architecture == "olm_composable":
                return {
                    "ordinary_pytorch_modules": True,
                    "composable_operators": ["Block", "Residual", "Repeat", "Parallel"],
                    "runtime_portability": ["cpu", "mps", "cuda"],
                    "preset_family": "decoder-only transformer",
                }
            if architecture in {"block_attnres", "rd_attnres"}:
                return {
                    "residual_sources_last_layer": len(self.blocks),
                    "qk_v_role_decoupled": architecture == "rd_attnres",
                    "qk_v_route_js_divergence": sum(
                        block.last_route_js for block in self.blocks
                    ) / len(self.blocks),
                    "extra_route_vectors_per_layer": (
                        2 if architecture == "rd_attnres" else 1
                    ),
                }
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
            if architecture == "penelope":
                return {
                    "localized_decoder_interval": [
                        self.recurrence_layer,
                        self.recurrence_layer + 1,
                    ],
                    "latent_recurrence_steps": (
                        self.localized_recurrence.last_latent_steps
                    ),
                    "full_decoder_reexecution": False,
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
            if architecture == "wide_dynamic_width":
                return {
                    "routing_granularity": "token-head-and-ffn-group",
                    "active_attention_head_fraction": sum(
                        block.attention.last_active_head_fraction for block in self.blocks
                    ) / len(self.blocks),
                    "active_ffn_channel_fraction": sum(
                        block.ffn.last_active_channel_fraction for block in self.blocks
                    ) / len(self.blocks),
                    "target_sparsity": 0.5,
                }
            if architecture == "retoken":
                return {
                    "retrieval_target_tokens": 1,
                    "score_space": "final-value-projection",
                    "causal_cache_keep_rate": sum(
                        block.attention.last_retoken_keep_rate
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
    return MicroLM,
