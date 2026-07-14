from __future__ import annotations

import os
from pathlib import Path

from ..industrial_batch import compact_movielens, evaluate_scores
from ..rec_utils import summarize_runs
from .model import scorer, train


def reproduce_argus(dataset_dir: Path, seed: int = 42):
    data = compact_movielens(dataset_dir, 180, 300)
    steps = int(os.environ.get("AUTO_RESEARCH_ARGUS_STEPS", "110"))
    feedback_weight = float(os.environ.get("AUTO_RESEARCH_ARGUS_FEEDBACK_WEIGHT", "0.35"))
    results = {"next_item_only": [], "feedback_then_item": []}
    training = []
    for run_seed in (seed, seed + 1, seed + 2):
        baseline, base_train = train(data, run_seed, steps, False)
        method, method_train = train(data, run_seed, steps, True, feedback_weight)
        results["next_item_only"].append(evaluate_scores(data, scorer(baseline)))
        results["feedback_then_item"].append(evaluate_scores(data, scorer(method)))
        training.append({"baseline": base_train, "method": method_train})
    aggregate = {name: summarize_runs(values) for name, values in results.items()}
    base, method = aggregate["next_item_only"], aggregate["feedback_then_item"]
    return {"paper": {"arxiv_id": "2507.15994", "title": "Scaling Recommender Transformers to One Billion Parameters", "url": "https://arxiv.org/abs/2507.15994", "track": "recommendation"}, "dataset": "MovieLens-100K long positive sequences", "setup": {"users": len(data.train), "items": data.item_count, "steps": steps, "feedback_weight": feedback_weight, "seeds": [seed, seed + 1, seed + 2], "context": 32}, "training": training, "results": aggregate, "ndcg_gain_percent": 100 * (method["ndcg_at_10"] / max(base["ndcg_at_10"], 1e-12) - 1), "paper_online_ab": {"total_listening_time_percent": 2.26, "likes_percent": 6.37}, "scope": "Trains matched Transformers with the paper's autoregressive decomposition: predict feedback semantics first, project that distribution back into the state, then predict the next item. MovieLens genre feedback and a 48d model replace proprietary music signals and billion-parameter scale."}
