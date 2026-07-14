from __future__ import annotations

import os
from pathlib import Path

from ..rec_utils import load_movielens_sequences, summarize_runs
from ..sasrec.model import SASRecConfig, train_model as train_sasrec
from ..sequence_training import evaluate_sequence_model
from .model import HSTUConfig, train_model


def reproduce_hstu(dataset_dir: Path, seed: int = 42):
    data = load_movielens_sequences(dataset_dir)
    steps = int(os.environ.get("AUTO_RESEARCH_HSTU_STEPS", "240"))
    hstu_config = HSTUConfig(steps=steps)
    sasrec_config = SASRecConfig(steps=steps)
    seeds = (seed, seed + 1, seed + 2)
    results = {"sasrec": [], "hstu": []}
    training = {"sasrec": [], "hstu": []}
    for run_seed in seeds:
        sasrec, metrics = train_sasrec(
            data, sasrec_config, run_seed, loss_kind="sampled_softmax"
        )
        training["sasrec"].append(metrics)
        results["sasrec"].append(evaluate_sequence_model(sasrec, data, sasrec_config))
        hstu, metrics = train_model(data, hstu_config, run_seed)
        training["hstu"].append(metrics)
        results["hstu"].append(evaluate_sequence_model(hstu, data, hstu_config))
    aggregate = {name: summarize_runs(runs) for name, runs in results.items()}
    baseline, proposed = aggregate["sasrec"], aggregate["hstu"]
    return {
        "paper": {"arxiv_id": "2402.17152", "title": "Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations", "url": "https://arxiv.org/abs/2402.17152", "track": "recommendation"},
        "dataset": "MovieLens 100K, per-user chronological leave-two-out, full-catalog ranking",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": list(seeds), "steps_per_seed": steps, "matched_dimensions": hstu_config.dimensions, "matched_layers": hstu_config.layers, "matched_heads": hstu_config.heads},
        "training": training,
        "results": aggregate,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"ranking_engagement_percent": 12.4, "ranking_consumption_percent": 4.4},
        "scope": "Runs matched-budget SASRec and HSTU with UVQK SiLU projections, causal non-softmax pointwise aggregated attention, learned relative-position bias, post-pooling normalization, U-gating, residuals, and generative all-position training. Private action types, timestamps, stochastic-length kernels, M-FALCON and trillion-parameter serving are omitted.",
    }
