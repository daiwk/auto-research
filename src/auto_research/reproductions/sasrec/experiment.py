from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from ..rec_utils import load_movielens_sequences, ranking_metrics, summarize_runs
from ..sequence_training import evaluate_sequence_model
from .model import SASRecConfig, train_model


def reproduce_sasrec(dataset_dir: Path, seed: int = 42):
    data = load_movielens_sequences(dataset_dir)
    config = SASRecConfig(steps=int(os.environ.get("AUTO_RESEARCH_SASREC_STEPS", "240")))
    seeds = (seed, seed + 1, seed + 2)
    runs, training = [], []
    for run_seed in seeds:
        model, train_metrics = train_model(data, config, run_seed)
        runs.append(evaluate_sequence_model(model, data, config))
        training.append(train_metrics)
    popularity = ranking_metrics(data, lambda _history: data.popularity)
    result = summarize_runs(runs)
    return {
        "paper": {"arxiv_id": "1808.09781", "title": "Self-Attentive Sequential Recommendation", "url": "https://arxiv.org/abs/1808.09781", "track": "recommendation"},
        "dataset": "MovieLens 100K, per-user chronological leave-two-out, full-catalog ranking",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": list(seeds), "steps_per_seed": config.steps, "dimensions": config.dimensions, "layers": config.layers},
        "training": training,
        "results": {"popularity": popularity, "sasrec": result},
        "ndcg_gain_percent": 100 * (result["ndcg_at_10"] - popularity["ndcg_at_10"]) / max(popularity["ndcg_at_10"], 1e-12),
        "paper_online_ab": None,
        "scope": "Runs the paper's tied item embeddings, learned positions, causal self-attention, point-wise FFN, residual/layer normalization, and pairwise BCE objective. Full-catalog evaluation is stricter than the paper's 100 sampled negatives; MovieLens-100K replaces ML-1M for fast Mac iteration.",
    }
