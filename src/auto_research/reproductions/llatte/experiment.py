from __future__ import annotations

from pathlib import Path
from typing import Any

from ..rec_utils import load_movielens_sequences, ranking_metrics, summarize_runs
from .model import LLaTTEScorer, train_sequence_backbone


def reproduce_llatte(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    baseline_runs, llatte_runs, selected = [], [], []
    for offset in range(3):
        model = train_sequence_backbone(data, seed + offset)
        baseline = LLaTTEScorer(model, 0.0)
        baseline_runs.append(ranking_metrics(data, baseline.short_sequence_scores))
        candidates = []
        for target_weight in (0.1, 0.25, 0.5, 0.75):
            for upstream_weight in (0.1, 0.25, 0.5, 0.75):
                scorer = LLaTTEScorer(model, upstream_weight, target_weight)
                metric = ranking_metrics(
                    data, scorer.two_stage_scores, target="validation"
                )
                candidates.append(
                    (metric["ndcg_at_10"], target_weight, upstream_weight)
                )
        _, target_weight, upstream_weight = max(candidates)
        selected.append(
            {"target_aware": target_weight, "upstream": upstream_weight}
        )
        llatte_runs.append(
            ranking_metrics(
                data,
                LLaTTEScorer(
                    model, upstream_weight, target_weight
                ).two_stage_scores,
            )
        )
    results = {"short_online_sequence": summarize_runs(baseline_runs), "llatte_two_stage": summarize_runs(llatte_runs)}
    return {
        "paper": {"arxiv_id": "2601.20083", "title": "LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation", "url": "https://arxiv.org/abs/2601.20083", "track": "recommendation"},
        "dataset": "MovieLens 100K (positive sequential interactions)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "validation_selected_weights": selected, "online_window": 12},
        "results": results,
        "ndcg_gain_percent": 100 * (results["llatte_two_stage"]["ndcg_at_10"] - results["short_online_sequence"]["ndcg_at_10"]) / max(results["short_online_sequence"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"conversion_lift_percent": 4.3, "normalized_entropy_reduction_percent": 0.25},
        "scope": "Reproduces the target-aware online sequence stage, pyramidal recent-token reduction, and cached full-history upstream representation. NumPy embeddings replace MLA, DHEN, semantic LLaMA features, and asynchronous H100 serving.",
    }
