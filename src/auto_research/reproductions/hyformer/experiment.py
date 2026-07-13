from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from ..industrial_ranking import evaluate_model, require_backend, train_supervised
from ..rec_utils import load_movielens_sequences, summarize_runs
from .model import HyFormerConfig, build_model


def reproduce_hyformer(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    config = HyFormerConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_HYFORMER_STEPS", "240"))
    )
    runs = {"late_fusion": [], "hyformer": []}
    training = {"late_fusion": [], "hyformer": []}
    torch, _ = require_backend()
    for offset in range(3):
        for kind in runs:
            torch.manual_seed(seed + offset)
            model = build_model(kind, data, config)
            model, train_metrics = train_supervised(
                model, data, config, seed + offset
            )
            training[kind].append(train_metrics)
            runs[kind].append(evaluate_model(model, data, config))
    results = {kind: summarize_runs(values) for kind, values in runs.items()}
    baseline, proposed = results["late_fusion"], results["hyformer"]
    return {
        "paper": {"arxiv_id": "2601.12681", "title": "HyFormer: Revisiting the Roles of Sequence Modeling and Feature Interaction in CTR Prediction", "url": "https://arxiv.org/abs/2601.12681", "track": "recommendation"},
        "dataset": "MovieLens 100K (single public sequence and genre fields)",
        "setup": {"users": len(data.train), "items": data.item_count, "queries": config.queries, "layers": config.layers, "steps": config.steps, "seeds": [seed, seed + 1, seed + 2]},
        "training": training,
        "results": results,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"watch_time_percent": 0.293, "finish_count_percent": 1.111, "query_change_percent": -0.236},
        "scope": "Trains semantic global-query generation, layer-wise query decoding over sequence K/V, and RankMixer-style query boosting in every layer. MovieLens provides one behavior stream rather than Douyin Search's private multi-sequence fields.",
    }
