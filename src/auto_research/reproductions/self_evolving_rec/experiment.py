from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from ..rec_utils import load_movielens_sequences, ranking_metrics, summarize_runs
from .model import CANDIDATES, train_candidate


def reproduce_self_evolving_rec(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    all_items = np.arange(data.item_count)
    baseline_runs, selected_runs, selected_names, journals = [], [], [], []
    for offset in range(3):
        run_seed = seed + offset
        trials = []
        trained = {}
        for candidate in CANDIDATES:
            model = train_candidate(data, candidate, run_seed)
            trained[candidate.name] = model
            metric = ranking_metrics(data, lambda history, model=model: model.scores(history[-1], all_items), target="validation")
            trials.append({"candidate": candidate.name, "validation_ndcg_at_10": metric["ndcg_at_10"]})
        selected = max(trials, key=lambda trial: trial["validation_ndcg_at_10"])["candidate"]
        selected_names.append(selected)
        journals.append({"seed": run_seed, "trials": trials, "promoted": selected})
        baseline_model = trained["human_adagrad"]
        selected_model = trained[selected]
        baseline_runs.append(ranking_metrics(data, lambda history, model=baseline_model: model.scores(history[-1], all_items)))
        selected_runs.append(ranking_metrics(data, lambda history, model=selected_model: model.scores(history[-1], all_items)))
    results = {"human_baseline": summarize_runs(baseline_runs), "self_evolving_promoted": summarize_runs(selected_runs)}
    return {
        "paper": {"arxiv_id": "2602.10226", "title": "Self-Evolving Recommendation System: End-To-End Autonomous Model Optimization With LLM Agents", "url": "https://arxiv.org/abs/2602.10226", "track": "recommendation"},
        "dataset": "MovieLens 100K (offline inner loop plus untouched test holdout)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "promoted_candidates": selected_names},
        "experiment_journal": journals,
        "results": results,
        "ndcg_gain_percent": 100 * (results["self_evolving_promoted"]["ndcg_at_10"] - results["human_baseline"]["ndcg_at_10"]) / max(results["human_baseline"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"rmsprop_youtube_percent": 0.06, "rmsprop_surface_percent": 0.12, "glu_youtube_percent": 0.06, "glu_surface_percent": 0.14, "reward_youtube_percent": 0.03, "reward_surface_percent": 0.13},
        "scope": "Concept demo only: the journal and holdout funnel run, but fixed candidates replace the LLM agent and no production A/B feedback enters the loop. These metrics do not reproduce the autonomous system.",
    }
