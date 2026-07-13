from pathlib import Path
from typing import Any

from ..cluster_goobs.model import train_retriever
from ..rec_utils import load_movielens_1m_sequences, ranking_metrics
from .model import OneRecScorer


def reproduce_onerec(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_1m_sequences(dataset_dir)
    backbone = train_retriever(data, "random_oob", seed, epochs=3, training_cap=100000)
    baseline = OneRecScorer(backbone, data.item_features, data.popularity, 0.0, 0.0)
    session_choices = []
    for weight in (0.1, 0.25, 0.5, 0.75, 1.0):
        scorer = OneRecScorer(backbone, data.item_features, data.popularity, weight, 0.0)
        metric = ranking_metrics(data, scorer.session_scores, target="validation")
        session_choices.append((metric["ndcg_at_10"], weight))
    session_weight = max(session_choices)[1]
    preference_choices = []
    for weight in (0.01, 0.02, 0.05, 0.1, 0.2):
        scorer = OneRecScorer(backbone, data.item_features, data.popularity, session_weight, weight)
        metric = ranking_metrics(data, scorer.aligned_scores, target="validation")
        preference_choices.append((metric["ndcg_at_10"], weight))
    preference_weight = max(preference_choices)[1]
    session = OneRecScorer(backbone, data.item_features, data.popularity, session_weight, 0.0)
    aligned = OneRecScorer(backbone, data.item_features, data.popularity, session_weight, preference_weight)
    results = {
        "pointwise_retrieval": ranking_metrics(data, baseline.pointwise_scores),
        "session_wise_generation": ranking_metrics(data, session.session_scores),
        "onerec_plus_preference_alignment": ranking_metrics(data, aligned.aligned_scores),
    }
    base, _, proposed = results.values()
    return {
        "paper": {"arxiv_id": "2502.18965", "title": "OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment", "url": "https://arxiv.org/abs/2502.18965", "track": "recommendation"},
        "dataset": "MovieLens 1M (public proxy; Kuaishou production logs are private)",
        "setup": {"users": len(data.train), "items": data.item_count, "seed": seed, "training_transition_cap": 100000, "validation_selected_session_weight": session_weight, "validation_selected_preference_weight": preference_weight},
        "results": results,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - base["ndcg_at_10"]) / max(base["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"traffic_percent": 1.0, "total_watch_time_percent": 1.68, "average_view_duration_percent": 6.56},
        "scope": "Reproduces session-wise generation and reward-margin preference alignment over a shared retrieval backbone. MoE generation, RQ semantic IDs, the production reward model, and iterative DPO sampling are compact proxies.",
    }
