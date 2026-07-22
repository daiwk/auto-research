from __future__ import annotations

from pathlib import Path

from auto_research.evolution.llm_data import load_llm_evolution_data

from ..llm_training import evaluate_language_model, require_torch, train_language_model
from .model import build_variant


def reproduce_conv_llm(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_llm_evolution_data(
        dataset_dir, True, vocab_size=1024,
        maximum_train_tokens=240_000, maximum_eval_tokens=32_000,
    )
    rows = {}
    for name in ("Transformer", "QKV-Conv"):
        torch.manual_seed(seed)
        model, config = build_variant(name, data.vocab_size)
        training = train_language_model(
            model, data.train, steps=60, batch_size=6,
            length=config.sequence_length, learning_rate=7e-4,
            seed=seed, torch=torch,
        )
        metrics = evaluate_language_model(
            model, data.test, length=config.sequence_length,
            batches=32, torch=torch,
        )
        rows[name] = {**training, **metrics}
    baseline, method = rows["Transformer"], rows["QKV-Conv"]
    return {
        "paper": {"arxiv_id": "2607.18413", "title": "Convolution for Large Language Models", "url": "https://arxiv.org/abs/2607.18413", "track": "llm"},
        "dataset": {"name": "WikiText-2", "train_tokens": len(data.train), "test_tokens": len(data.test)},
        "setup": {"seed": seed, "steps": 60, "sequence_length": config.sequence_length, "same_tokens_optimizer_and_parameter_budget": True},
        "variants": rows,
        "relative": {"perplexity_reduction_percent": 100.0 * (baseline["perplexity"] - method["perplexity"]) / baseline["perplexity"]},
        "paper_results": {"qwen3_1_7b_baseline_perplexity": 13.42, "qkv_conv_perplexity": 12.79, "extra_parameters_percent": "<0.01"},
        "stages": {"post_qkv_location": True, "depthwise_groups_equal_channels": True, "kernel_size": 3, "residual_shortcut": True, "activation": None, "causal_left_padding": True},
        "scope": "实际预训练同预算 Transformer 与 post-QKV residual depthwise Conv1D；卷积为 k=3、逐通道、线性且随机初始化。WikiText-2 上的 96-d/3-layer 小模型替代论文 Qwen3-0.6B/1.7B/4B 与大规模预训练语料。",
    }
