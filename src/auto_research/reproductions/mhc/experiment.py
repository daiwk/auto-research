from __future__ import annotations

from pathlib import Path

import numpy as np

from auto_research.evolution.llm_data import load_llm_evolution_data

from ..llm_training import evaluate_language_model, require_torch, train_language_model
from .model import build_variant


def reproduce_mhc(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_llm_evolution_data(
        dataset_dir, True, vocab_size=1024,
        maximum_train_tokens=180_000, maximum_eval_tokens=24_000,
    )
    rows = {}
    for name in ("Transformer", "HC", "mHC"):
        torch.manual_seed(seed)
        model, config = build_variant(name, data.vocab_size)
        training = train_language_model(
            model, data.train, steps=45, batch_size=4,
            length=config.sequence_length, learning_rate=8e-4,
            seed=seed, torch=torch,
        )
        metrics = evaluate_language_model(
            model, data.validation, length=config.sequence_length,
            batches=24, torch=torch,
        )
        probe = torch.tensor(
            data.validation[: config.sequence_length], dtype=torch.long,
            device=next(model.parameters()).device,
        )[None]
        stability = model.connection_stats(probe)
        rows[name] = {**metrics, **training, "stability": stability}
    baseline, method = rows["Transformer"], rows["mHC"]
    return {
        "paper": {
            "arxiv_id": "2512.24880",
            "title": "mHC: Manifold-Constrained Hyper-Connections",
            "url": "https://arxiv.org/abs/2512.24880",
            "track": "llm",
        },
        "dataset": {"name": "WikiText-2", "train_tokens": len(data.train), "validation_tokens": len(data.validation)},
        "setup": {"seed": seed, "steps": 45, "sequence_length": config.sequence_length, "same_tokens_and_optimizer": True},
        "variants": rows,
        "relative": {
            "perplexity_reduction_percent": 100.0 * (baseline["perplexity"] - method["perplexity"]) / baseline["perplexity"],
            "vs_hc_percent": 100.0 * (rows["HC"]["perplexity"] - method["perplexity"]) / rows["HC"]["perplexity"],
        },
        "paper_results": {"benchmark_gain_percent": "2.1–2.3", "training_overhead_percent": 6.7},
        "stability": {
            "mhc_doubly_stochastic": rows["mHC"]["stability"],
            "hc_unconstrained": rows["HC"]["stability"],
        },
        "scope": "实际训练 2-stream 动态 HC 与 mHC；mHC 对 H_res 做 20 次 Sinkhorn-Knopp，并对 H_pre/H_post 做非负约束。WikiText-2 小模型替代 DeepSeek 私有语料与 3B/9B/27B MoE；未复刻 TileLang 融合核、重计算和 DualPipe。",
    }
