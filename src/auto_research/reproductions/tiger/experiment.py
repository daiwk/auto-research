from __future__ import annotations

import os
from pathlib import Path

from ..rec_utils import load_movielens_sequences, ranking_metrics, summarize_runs
from .model import TIGERConfig, random_ids, score_all, train_model, train_semantic_ids


def reproduce_tiger(dataset_dir: Path, seed: int = 42):
    data = load_movielens_sequences(dataset_dir)
    config = TIGERConfig(
        rqvae_steps=int(os.environ.get("AUTO_RESEARCH_TIGER_RQVAE_STEPS", "240")),
        training_steps=int(os.environ.get("AUTO_RESEARCH_TIGER_STEPS", "240")),
    )
    semantic_ids, rqvae = train_semantic_ids(data.item_features, config, seed)
    random_semantic_ids = random_ids(
        data.item_count, config, seed, int(semantic_ids[:, -1].max()) + 1
    )
    seeds = (seed, seed + 1, seed + 2)
    results = {"random_id": [], "tiger": []}
    training = {"random_id": [], "tiger": []}
    for run_seed in seeds:
        for kind, ids in (("random_id", random_semantic_ids), ("tiger", semantic_ids)):
            model, metrics = train_model(ids, data, config, run_seed)
            training[kind].append(metrics)
            results[kind].append(ranking_metrics(
                data, lambda history, model=model: score_all(model, history, data.item_count, config)
            ))
    aggregate = {name: summarize_runs(runs) for name, runs in results.items()}
    baseline, proposed = aggregate["random_id"], aggregate["tiger"]
    return {
        "paper": {"arxiv_id": "2305.05065", "title": "Recommender Systems with Generative Retrieval", "url": "https://arxiv.org/abs/2305.05065", "track": "recommendation"},
        "dataset": "MovieLens 100K genre content, leave-two-out, constrained full-catalog generative ranking",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": list(seeds), "rqvae_steps": config.rqvae_steps, "decoder_steps_per_seed": config.training_steps, "codebooks": config.codebooks, "codebook_size": config.codebook_size},
        "rqvae": rqvae,
        "training": training,
        "results": aggregate,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": None,
        "scope": "Trains an RQ-VAE over public item content, residual semantic codebooks, collision tokens, and a Transformer encoder-decoder that autoregressively scores only valid item Semantic IDs. MovieLens genres replace Sentence-T5 Amazon text embeddings; user-ID hashing, cold-start epsilon mixing and production serving are omitted.",
    }
