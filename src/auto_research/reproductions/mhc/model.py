from __future__ import annotations

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm


def build_variant(name: str, vocab_size: int):
    architecture = {
        "Transformer": "llama_modern",
        "HC": "hyper_connections",
        "mHC": "mhc",
    }[name]
    config = MicroLMConfig(
        vocab_size=vocab_size,
        dimensions=64,
        layers=3,
        heads=4,
        sequence_length=48,
        expansion=3,
        residual_streams=2,
        sinkhorn_iterations=20,
    )
    return build_micro_lm(architecture, config), config
