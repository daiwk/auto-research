from __future__ import annotations

import os
from pathlib import Path

from ..rec_utils import load_movielens_sequences, ranking_metrics, summarize_runs
from .model import DINConfig, score_all, train_model


def reproduce_din(dataset_dir: Path, seed: int = 42):
    data = load_movielens_sequences(dataset_dir)
    config = DINConfig(steps=int(os.environ.get("AUTO_RESEARCH_DIN_STEPS", "240")))
    seeds = (seed, seed + 1, seed + 2)
    results = {"mean_pool": [], "din": []}
    training = {"mean_pool": [], "din": []}
    for run_seed in seeds:
        for kind in results:
            model, metrics = train_model(kind, data, config, run_seed)
            training[kind].append(metrics)
            results[kind].append(ranking_metrics(
                data, lambda history, model=model: score_all(model, history, data.item_count, config)
            ))
    aggregate = {name: summarize_runs(runs) for name, runs in results.items()}
    baseline, proposed = aggregate["mean_pool"], aggregate["din"]
    return {
        "paper": {"arxiv_id": "1706.06978", "title": "Deep Interest Network for Click-Through Rate Prediction", "url": "https://arxiv.org/abs/1706.06978", "track": "recommendation"},
        "dataset": "MovieLens 100K genres and histories, leave-two-out, full-catalog ranking",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": list(seeds), "steps_per_seed": config.steps, "dimensions": config.dimensions},
        "training": training,
        "results": aggregate,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"ctr_percent": 10.0, "rpm_percent": 3.8, "period": "2017-05 to 2017-06"},
        "scope": "Runs candidate-conditioned local activation over item+genre behavior embeddings, weighted interest pooling, interaction MLP, Dice activations and negative-sampled CTR training. MBA regularization and Alibaba's private billion-scale sparse features/serving kernels are omitted.",
    }
