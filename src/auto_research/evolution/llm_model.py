from __future__ import annotations

from dataclasses import dataclass

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
        "looped_latent_attention", "gaugequant", "penelope",
        "switch_transformer", "mamba", "switch_attention",
        "native_sparse_attention", "gated_attention",
        "nsa_gated_attention", "wide_dynamic_width", "retoken",
        "block_attnres", "rd_attnres",
        "olm_composable",
        "macro", "hilp",
        "rope", "alibi", "gqa", "hymba", "moba", "blt",
    }
    if architecture not in supported:
        raise ValueError(f"unknown micro LLM architecture: {architecture}")
    modern = architecture.startswith("llama") or architecture in {
        "hyper_connections", "mhc", "qkv_depthwise_conv", "mobius_rope", "naju",
        "adadsf", "engram", "looped_latent_attention", "gaugequant", "penelope",
        "switch_transformer", "mamba", "switch_attention",
        "native_sparse_attention", "gated_attention",
        "nsa_gated_attention", "wide_dynamic_width", "retoken",
        "block_attnres", "rd_attnres",
        "olm_composable",
        "macro", "hilp",
        "rope", "alibi", "gqa", "hymba", "moba", "blt",
    }
    parallel = "parallel" in architecture
    kv_heads = config.kv_heads if architecture == "gqa" else config.heads
    if config.dimensions % config.heads or config.heads % kv_heads:
        raise ValueError("dimensions/heads and heads/kv_heads must be divisible")
    head_dim = config.dimensions // config.heads
    from .llm_layers.attention import build_attention_layers
    from .llm_layers.blocks import build_blocks
    from .llm_layers.model import build_model_class
    attention = build_attention_layers(torch, nn, config, architecture, modern, parallel, kv_heads, head_dim)
    blocks = build_blocks(torch, nn, config, architecture, modern, parallel, kv_heads, head_dim, *attention)
    (MicroLM,) = build_model_class(torch, nn, config, architecture, modern, parallel, kv_heads, head_dim, *attention, *blocks)
    return MicroLM()
