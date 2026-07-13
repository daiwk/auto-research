from __future__ import annotations

from pathlib import Path
from typing import Any

from ..rec_utils import load_movielens_sequences, ranking_metrics, summarize_runs
from .model import CMSLScorer, semantic_assignments, train_backbone


def reproduce_cmsl(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    baseline_runs, cmsl_runs, selected = [], [], []
    for offset in range(3):
        run_seed = seed + offset
        model = train_backbone(data, run_seed)
        assignments = semantic_assignments(data.item_features, clusters=6, seed=run_seed)
        baseline_scorer = CMSLScorer(model, assignments, alpha=0.0)
        baseline_runs.append(ranking_metrics(data, baseline_scorer.single_sequence_scores))
        candidates = []
        for alpha in (0.25, 0.5, 0.75, 1.0):
            scorer = CMSLScorer(model, assignments, alpha)
            metric = ranking_metrics(data, scorer.multi_sequence_scores, target="validation")
            candidates.append((metric["ndcg_at_10"], alpha))
        alpha = max(candidates)[1]
        selected.append(alpha)
        cmsl_runs.append(ranking_metrics(data, CMSLScorer(model, assignments, alpha).multi_sequence_scores))
    results = {"single_sequence": summarize_runs(baseline_runs), "cmsl": summarize_runs(cmsl_runs)}
    return {
        "paper": {"arxiv_id": "2606.28533", "title": "CMSL: Constructive Multi-Sequence Learning for Recommendation Systems", "url": "https://arxiv.org/abs/2606.28533", "track": "recommendation"},
        "dataset": "MovieLens 100K (ratings >= 4; genres initialize latent sequence construction)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "validation_selected_alpha": selected, "latent_sequences": 6},
        "results": results,
        "ndcg_gain_percent": 100 * (results["cmsl"]["ndcg_at_10"] - results["single_sequence"]["ndcg_at_10"]) / max(results["single_sequence"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"metric_1": 0.116, "metric_2": 0.158, "metric_3": 0.171, "metric_4": 0.092},
        "scope": "Reproduces multi-sequence construction, isolated strand modeling, and degree-two linear-attention approximation on a compact sequential backbone. It does not reproduce Meta's HSTU kernels, private features, or 128-H100 training stack.",
    }
