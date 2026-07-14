from __future__ import annotations

import os
from pathlib import Path

from ..rec_utils import batched_ranking_metrics, load_movielens_sequences, summarize_runs
from .model import PinFMConfig, finetune_model, pretrain_model, score_batch, train_scratch


def reproduce_pinfm(dataset_dir: Path, seed: int = 42):
    data = load_movielens_sequences(dataset_dir)
    config = PinFMConfig(
        pretrain_steps=int(os.environ.get("AUTO_RESEARCH_PINFM_PRETRAIN_STEPS", "160")),
        finetune_steps=int(os.environ.get("AUTO_RESEARCH_PINFM_FINETUNE_STEPS", "160")),
    )
    seeds = (seed, seed + 1, seed + 2)
    results = {"scratch_dcat": [], "pinfm": []}
    validation_results = {"scratch_dcat": [], "pinfm": []}
    training = {"scratch_dcat": [], "pinfm_pretrain": [], "pinfm_finetune": []}
    for run_seed in seeds:
        scratch, metrics = train_scratch(data, config, run_seed)
        training["scratch_dcat"].append(metrics)
        results["scratch_dcat"].append(batched_ranking_metrics(
            data,
            lambda histories, model=scratch: score_batch(
                model, histories, data.item_count, config
            ),
            batch_size=32,
        ))
        validation_results["scratch_dcat"].append(batched_ranking_metrics(
            data,
            lambda histories, model=scratch: score_batch(
                model, histories, data.item_count, config
            ),
            batch_size=32,
            target="validation",
        ))
        pretrained, metrics = pretrain_model(data, config, run_seed)
        training["pinfm_pretrain"].append(metrics)
        pinfm, metrics = finetune_model(pretrained, "pinfm", data, config, run_seed)
        training["pinfm_finetune"].append(metrics)
        results["pinfm"].append(batched_ranking_metrics(
            data,
            lambda histories, model=pinfm: score_batch(
                model, histories, data.item_count, config
            ),
            batch_size=32,
        ))
        validation_results["pinfm"].append(batched_ranking_metrics(
            data,
            lambda histories, model=pinfm: score_batch(
                model, histories, data.item_count, config
            ),
            batch_size=32,
            target="validation",
        ))
    aggregate = {name: summarize_runs(runs) for name, runs in results.items()}
    validation_aggregate = {
        name: summarize_runs(runs) for name, runs in validation_results.items()
    }
    baseline, proposed = aggregate["scratch_dcat"], aggregate["pinfm"]
    return {
        "paper": {"arxiv_id": "2507.12704", "title": "PinFM: Foundation Model for User Activity Sequences at a Billion-scale Visual Discovery Platform", "url": "https://arxiv.org/abs/2507.12704", "track": "recommendation"},
        "dataset": "MovieLens 100K genres and positive histories, leave-two-out, full-catalog ranking",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": list(seeds), "pretrain_steps": config.pretrain_steps, "finetune_steps": config.finetune_steps, "dimensions": config.dimensions, "layers": config.layers},
        "training": training,
        "results": aggregate,
        "validation_results": validation_aggregate,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"homefeed_sitewide_saves_percent": 1.20, "homefeed_surface_saves_percent": 2.60, "homefeed_fresh_saves_percent": 5.70, "i2i_sitewide_saves_percent": 0.72, "i2i_surface_saves_percent": 2.09},
        "scope": "Runs decoder-only NTL+MTL+FTL contrastive pretraining, downstream early-fusion fine-tuning, candidate-ID randomization, 10x lower backbone fine-tuning LR, and mathematically decomposed DCAT context/candidate attention with context KV reuse. MovieLens replaces Pinterest multi-action data; age dropout, distributed embeddings, int4 quantization and Triton kernels are omitted.",
    }
