from __future__ import annotations

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm


def build_variant(name: str, vocab_size: int):
    architecture = {"Transformer": "llama_modern", "QKV-Conv": "qkv_depthwise_conv"}[name]
    config = MicroLMConfig(
        vocab_size=vocab_size,
        dimensions=96,
        layers=3,
        heads=4,
        sequence_length=64,
        expansion=3,
    )
    return build_micro_lm(architecture, config), config
