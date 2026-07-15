from __future__ import annotations

import os
from pathlib import Path

import numpy as np

from ..rec_utils import batched_ranking_metrics, load_movielens_sequences, summarize_runs
from .model import NONTPConfig, score_batch, train_model


def reproduce_nontp(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_movielens_sequences(dataset_dir)
    config = NONTPConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_NONTP_STEPS", "80")),
        batch_size=int(os.environ.get("AUTO_RESEARCH_NONTP_BATCH_SIZE", "32")),
    )
    seed_count = int(os.environ.get("AUTO_RESEARCH_NONTP_SEEDS", "3"))
    seeds = tuple(seed + index for index in range(seed_count))
    domains = np.asarray(data.item_features).argmax(axis=1)
    results = {name: [] for name in ("ntp", "tcl", "tdl", "nontp")}
    training = {name: [] for name in results}
    for run_seed in seeds:
        for name in results:
            model, metrics = train_model(name, data, domains, config, run_seed)
            training[name].append(metrics)
            results[name].append(
                batched_ranking_metrics(
                    data,
                    lambda histories, model=model: score_batch(model, histories, config),
                    batch_size=128,
                )
            )
    aggregate = {name: summarize_runs(values) for name, values in results.items()}
    baseline, proposed = aggregate["ntp"], aggregate["nontp"]
    return {
        "paper": {
            "arxiv_id": "2607.12277",
            "title": "Not Only NTP: Extending Training Signal Coverage for Generative Recommendation",
            "url": "https://arxiv.org/abs/2607.12277",
            "organization": "Meituan",
        },
        "dataset": "MovieLens 100K chronological sequences; primary genre is the public domain label",
        "setup": {
            "users": len(data.train),
            "items": data.item_count,
            "domains": int(domains.max()) + 1,
            "seeds": list(seeds),
            "steps_per_variant_seed": config.steps,
            "future_steps": config.future_steps,
            "temperature": config.temperature,
            "ema_momentum": config.ema_momentum,
            "lambda_tcl": config.auxiliary_weight,
            "lambda_tdl": config.auxiliary_weight,
        },
        "training": training,
        "results": aggregate,
        "relative": {
            "hit_at_10_percent": _gain(proposed["hit_at_10"], baseline["hit_at_10"]),
            "ndcg_at_10_percent": _gain(proposed["ndcg_at_10"], baseline["ndcg_at_10"]),
        },
        "paper_results": {
            "amazon_hr_at_10_ntp": 0.3455,
            "amazon_hr_at_10_nontp": 0.3553,
            "amazon_ndcg_at_10_ntp": 0.2371,
            "amazon_ndcg_at_10_nontp": 0.2459,
            "online_ctr_percent": 1.8,
            "online_gmv_percent": 2.1,
        },
        "scope": (
            "Executes joint NTP+TCL+TDL training, a full EMA teacher, three offset-specific "
            "predictors, InfoNCE negatives restricted to other sequences, cross-domain mean "
            "pooling through the shared item head, and zero-overhead inference. A compact causal "
            "Transformer and MovieLens genre domains replace HSTU and the 3.2M-item Amazon "
            "Movie-Book-CDs benchmark."
        ),
    }


def _gain(value: float, baseline: float) -> float:
    return 100.0 * (value - baseline) / max(abs(baseline), 1e-12)
