from __future__ import annotations

import os
from pathlib import Path

from ..rec_utils import batched_ranking_metrics, load_movielens_sequences, summarize_runs
from .model import TransActV2Config, score_batch, train_model


def reproduce_transact_v2(dataset_dir: Path, seed: int = 42):
    data = load_movielens_sequences(dataset_dir)
    config = TransActV2Config(steps=int(os.environ.get("AUTO_RESEARCH_TRANSACT_V2_STEPS", "160")))
    seeds = (seed, seed + 1, seed + 2)
    results = {"transact": [], "transact_v2": []}
    training = {"transact": [], "transact_v2": []}
    for run_seed in seeds:
        for kind in results:
            model, metrics = train_model(kind, data, config, run_seed)
            training[kind].append(metrics)
            results[kind].append(batched_ranking_metrics(
                data,
                lambda histories, model=model: score_batch(
                    model, histories, data.item_count, config
                ),
                batch_size=2,
            ))
    aggregate = {name: summarize_runs(runs) for name, runs in results.items()}
    baseline, proposed = aggregate["transact"], aggregate["transact_v2"]
    return {
        "paper": {"arxiv_id": "2506.02267", "title": "TransAct V2: Lifelong User Action Sequence Modeling on Pinterest Recommendation", "url": "https://arxiv.org/abs/2506.02267", "track": "recommendation"},
        "dataset": "MovieLens 100K genres and positive histories, leave-two-out, full-catalog ranking",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": list(seeds), "steps_per_seed": config.steps, "lifelong_length": config.lifelong_length, "selected_length": config.selected_length},
        "training": training,
        "results": aggregate,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"traffic_per_arm_percent": 1.5, "repin_volume_percent": 6.35, "hide_volume_percent": -12.80, "impression_diversity_percent": 0.45, "time_spent_percent": 1.41},
        "scope": "Runs candidate-anchored nearest-neighbor selection over lifelong/realtime histories, recent-action retention, early-fusion causal Transformer ranking, and sampled next-action auxiliary loss. MovieLens genres replace PinSage embeddings; private action/surface fields, impression negatives and Triton serving kernels are omitted.",
    }
