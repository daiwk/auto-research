from __future__ import annotations

import os
from pathlib import Path

from ..industrial_batch import FAIR_DIN_STEPS, compact_movielens, evaluate_scores, run_din_baseline
from ..rec_utils import summarize_runs
from .model import scorer, train_caption_tokens, train_ranker


def reproduce_mm_llm(dataset_dir: Path, seed: int = 42):
    data = compact_movielens(dataset_dir, 180, 280)
    steps = int(os.environ.get("AUTO_RESEARCH_MM_LLM_STEPS", "100"))
    caption_tokens, caption_training = train_caption_tokens(data, seed, steps)
    results = {"visual_id_baseline": [], "mm_llm_features": []}
    training = []
    for run_seed in (seed, seed + 1, seed + 2):
        baseline, base_train = train_ranker(data, caption_tokens, run_seed, steps, False)
        method, method_train = train_ranker(data, caption_tokens, run_seed, steps, True)
        results["visual_id_baseline"].append(evaluate_scores(data, scorer(baseline, data)))
        results["mm_llm_features"].append(evaluate_scores(data, scorer(method, data)))
        training.append({"baseline": base_train, "method": method_train})
    aggregate = {name: summarize_runs(values) for name, values in results.items()}
    base, method = aggregate["visual_id_baseline"], aggregate["mm_llm_features"]
    seeds = (seed, seed + 1, seed + 2)
    din_steps = FAIR_DIN_STEPS
    aggregate["din"], din_training = run_din_baseline(data, seeds, din_steps)
    return {
        "paper": {"arxiv_id": "2605.09338", "title": "A General Framework for Multimodal LLM-Based Multimedia Understanding in Large-Scale Recommendation Systems", "url": "https://arxiv.org/abs/2605.09338", "track": "recommendation"},
        "dataset": "MovieLens-100K public content vectors and feedback",
        "setup": {"users": len(data.train), "items": data.item_count, "steps": steps, "din_steps": din_steps, "seeds": list(seeds)},
        "caption_training": caption_training, "training": training, "din_training": din_training, "results": aggregate,
        "ndcg_gain_percent": 100 * (method["ndcg_at_10"] / max(base["ndcg_at_10"], 1e-12) - 1),
        "ndcg_vs_din_percent": 100 * (method["ndcg_at_10"] / max(aggregate["din"]["ndcg_at_10"], 1e-12) - 1),
        "paper_online_ab": {"engagement_percent": 0.02, "offline_auc_percent": 0.35},
        "scope": "Trains a visual-encoder/query-cross-attention caption-token generator, tokenizes its discrete semantic outputs, builds user semantic-interest profiles, and injects both into an ID+visual ranker. MovieLens content vectors replace raw private multimedia and a compact decoder replaces BLIP-2/LLaMA2-1.5B.",
    }
