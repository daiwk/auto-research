from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from ..industrial_ranking import evaluate_model
from ..rec_utils import load_movielens_sequences, summarize_runs
from .model import OneTransConfig, train_model


def reproduce_onetrans(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    config = OneTransConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_ONETRANS_STEPS", "240"))
    )
    runs = {"encode_then_interact": [], "onetrans": []}
    training = {"encode_then_interact": [], "onetrans": []}
    for offset in range(3):
        for kind in runs:
            model, metrics = train_model(kind, data, config, seed + offset)
            training[kind].append(metrics)
            runs[kind].append(evaluate_model(model, data, config))
    results = {kind: summarize_runs(values) for kind, values in runs.items()}
    baseline, proposed = results["encode_then_interact"], results["onetrans"]
    return {
        "paper": {"arxiv_id": "2510.26104", "title": "OneTrans: Unified Feature Interaction and Sequence Modeling with One Transformer in Industrial Recommender", "url": "https://arxiv.org/abs/2510.26104", "track": "recommendation"},
        "dataset": "MovieLens 100K (public replacement for private commerce logs)",
        "setup": {"users": len(data.train), "items": data.item_count, "layers": config.layers, "dimensions": config.dimensions, "sequence_length": config.sequence_length, "steps": config.steps, "seeds": [seed, seed + 1, seed + 2]},
        "training": training,
        "results": results,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"feeds_order_percent": 4.3510, "feeds_gmv_percent": 5.6848, "mall_order_percent": 2.5772, "mall_gmv_percent": 3.6696, "feeds_latency_percent": -3.91},
        "scope": "Trains unified S/NS tokenization, token-specific NS versus shared sequence QKV/FFNs, causal attention, and pyramid tail pruning. Local vectorization replaces persistent cross-request KV infrastructure and private CTR/CVR fields.",
    }
