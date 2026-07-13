from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from ..rec_utils import load_movielens_sequences, summarize_runs
from .model import MixFormerConfig, evaluate_model, train_model


def reproduce_mixformer(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    config = MixFormerConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_MIXFORMER_STEPS", "240"))
    )
    baseline_runs, proposed_runs = [], []
    training = {"stacked": [], "unified": []}
    for offset in range(3):
        baseline, baseline_training = train_model("stacked", data, seed + offset, config)
        proposed, proposed_training = train_model("unified", data, seed + offset, config)
        baseline_runs.append(evaluate_model(baseline, data, config))
        proposed_runs.append(evaluate_model(proposed, data, config))
        training["stacked"].append(baseline_training)
        training["unified"].append(proposed_training)
    results = {
        "stacked_dense_plus_sequence": summarize_runs(baseline_runs),
        "unified_mixformer": summarize_runs(proposed_runs),
    }
    baseline, proposed = results.values()
    return {
        "paper": {"arxiv_id": "2602.14110", "title": "MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders", "url": "https://arxiv.org/abs/2602.14110", "track": "recommendation"},
        "dataset": "MovieLens 100K (genres proxy 300+ private Douyin features)",
        "setup": {
            "users": len(data.train), "items": data.item_count,
            "seeds": [seed, seed + 1, seed + 2], "steps": config.steps,
            "dimensions": config.dimensions, "layers": config.layers,
            "sequence_length": config.sequence_length,
        },
        "training": training,
        "results": results,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"douyin_duration_percent": 0.2799, "douyin_lite_duration_percent": 0.4105, "douyin_comment_percent": 0.7035, "douyin_lite_comment_percent": 1.9097},
        "scope": "Trains the paper's stacked baseline and unified dense/sequence Transformer under a matched local budget. Dense feature splits and behavior tokens share every proposed block, and user encoding is reused across all item scores. Private trillion-scale labels, 1B+ scaling, and production latency infrastructure remain out of scope.",
    }
