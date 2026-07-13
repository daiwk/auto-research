from pathlib import Path
from typing import Any

from ..longer.model import train_backbone
from ..rec_utils import load_movielens_sequences, ranking_metrics, summarize_runs
from .model import MixFormerScorer


def reproduce_mixformer(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    baseline_runs, proposed_runs, selected = [], [], []
    for offset in range(3):
        model = train_backbone(data, seed + offset)
        baseline = MixFormerScorer(model, data.item_features, 0.0)
        baseline_runs.append(ranking_metrics(data, baseline.stacked_scores))
        choices = []
        for weight in (0.05, 0.1, 0.2, 0.35, 0.5):
            scorer = MixFormerScorer(model, data.item_features, weight)
            metric = ranking_metrics(data, scorer.unified_scores, target="validation")
            choices.append((metric["ndcg_at_10"], weight))
        weight = max(choices)[1]
        selected.append(weight)
        proposed_runs.append(ranking_metrics(data, MixFormerScorer(model, data.item_features, weight).unified_scores))
    results = {"stacked_dense_plus_sequence": summarize_runs(baseline_runs), "unified_mixformer": summarize_runs(proposed_runs)}
    baseline, proposed = results.values()
    return {
        "paper": {"arxiv_id": "2602.14110", "title": "MixFormer: Co-Scaling Up Dense and Sequence in Industrial Recommenders", "url": "https://arxiv.org/abs/2602.14110", "track": "recommendation"},
        "dataset": "MovieLens 100K (genres proxy 300+ private Douyin features)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "validation_selected_cross_weights": selected},
        "results": results,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"douyin_duration_percent": 0.2799, "douyin_lite_duration_percent": 0.4105, "douyin_comment_percent": 0.7035, "douyin_lite_comment_percent": 1.9097},
        "scope": "Concept demo only: a fixed semantic gate sketches dense/sequence interaction, but no MixFormer block or decoupled train/serve path is trained. These metrics do not reproduce MixFormer.",
    }
