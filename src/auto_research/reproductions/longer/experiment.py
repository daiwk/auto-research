from pathlib import Path
from typing import Any

from ..rec_utils import load_movielens_sequences, ranking_metrics, summarize_runs
from .model import LONGERScorer, train_backbone


def reproduce_longer(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    baseline_runs, longer_runs, selected = [], [], []
    for offset in range(3):
        model = train_backbone(data, seed + offset)
        baseline = LONGERScorer(model, 0.0)
        baseline_runs.append(ranking_metrics(data, baseline.recent_transformer_scores))
        choices = []
        for weight in (0.1, 0.25, 0.5, 0.75, 1.0):
            scorer = LONGERScorer(model, weight)
            metric = ranking_metrics(data, scorer.longer_scores, target="validation")
            choices.append((metric["ndcg_at_10"], weight))
        weight = max(choices)[1]
        selected.append(weight)
        longer_runs.append(ranking_metrics(data, LONGERScorer(model, weight).longer_scores))
    results = {
        "recent_sequence_transformer": summarize_runs(baseline_runs),
        "longer_token_merge": summarize_runs(longer_runs),
    }
    baseline, proposed = results.values()
    return {
        "paper": {"arxiv_id": "2505.04421", "title": "LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders", "url": "https://arxiv.org/abs/2505.04421", "track": "recommendation"},
        "dataset": "MovieLens 100K (public proxy; ByteDance data is private)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "group_size": 4, "validation_selected_merge_weights": selected},
        "results": results,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"douyin_ads_adss_range_percent": [1.063, 2.097], "douyin_ecommerce_order_per_user_range_percent": [4.6125, 7.9222]},
        "scope": "Concept demo only: fixed score aggregation sketches global/local history use, but no trainable hybrid-attention or InnerTrans module is run. These metrics do not reproduce LONGER.",
    }
