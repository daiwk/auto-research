from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from ..industrial_ranking import evaluate_model
from ..rec_utils import load_movielens_sequences
from .model import RankMixerConfig, train_model


def reproduce_rankmixer(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    config = RankMixerConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_RANKMIXER_STEPS", "240"))
    )
    results, training = {}, {}
    for kind in ("shared_ffn", "rankmixer_dense", "rankmixer_smoe"):
        model, metrics = train_model(kind, data, config, seed)
        training[kind] = metrics
        results[kind] = evaluate_model(model, data, config)
    baseline = results["shared_ffn"]
    proposed = results["rankmixer_smoe"]
    return {
        "paper": {"arxiv_id": "2507.15551", "title": "RankMixer: Scaling Up Ranking Models in Industrial Recommenders", "url": "https://arxiv.org/abs/2507.15551", "track": "recommendation"},
        "dataset": "MovieLens 100K (genres/history replace private Douyin fields)",
        "setup": {"users": len(data.train), "items": data.item_count, "tokens": config.tokens, "dimensions": config.dimensions, "layers": config.layers, "experts": config.experts, "steps": config.steps, "seed": seed},
        "training": training,
        "results": results,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"active_days_percent": 0.3, "duration_percent": 1.08},
        "scope": "Trains parameter-free multi-head token mixing, isolated per-token FFNs, and dense-training/sparse-inference ReLU-routed MoE. Four public feature groups replace 300+ private Douyin fields; kernel-level MFU and quantized serving are not reproduced.",
    }
