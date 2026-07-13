from __future__ import annotations

from pathlib import Path
from typing import Any

from ..rec_utils import load_movielens_sequences, ranking_metrics
from .model import G2RecScorer, build_graph_tokens


def reproduce_g2rec(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    del seed  # Graph construction is deterministic for reproducible comparison.
    data = load_movielens_sequences(dataset_dir)
    graph, membership = build_graph_tokens(data)
    baseline = G2RecScorer(graph, membership, beta=0.0)
    candidates = []
    for beta in (0.15, 0.3, 0.45, 0.6, 0.75):
        scorer = G2RecScorer(graph, membership, beta)
        metric = ranking_metrics(data, scorer.interest_token_scores, target="validation")
        candidates.append((metric["ndcg_at_10"], beta))
    beta = max(candidates)[1]
    proposed = G2RecScorer(graph, membership, beta)
    results = {
        "item_tokens_only": ranking_metrics(data, baseline.item_only_scores),
        "g2rec_item_plus_interest_tokens": ranking_metrics(data, proposed.interest_token_scores),
    }
    return {
        "paper": {"arxiv_id": "2606.20554", "title": "Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation", "url": "https://arxiv.org/abs/2606.20554", "track": "recommendation"},
        "dataset": "MovieLens 100K (ratings >= 4; item-item co-engagement graph)",
        "setup": {"users": len(data.train), "items": data.item_count, "soft_interest_tokens": membership.shape[1], "validation_selected_beta": beta},
        "results": results,
        "ndcg_gain_percent": 100 * (results["g2rec_item_plus_interest_tokens"]["ndcg_at_10"] - results["item_tokens_only"]["ndcg_at_10"]) / max(results["item_tokens_only"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"in_session_lift_lower_bound_percent": 0.03, "engagement_lift_range_percent": [0.06, 0.19]},
        "scope": "Reproduces item-item co-engagement graph construction, soft interest prototypes, alternating item/interest representation, and validation-selected fusion. A compact graph next-token scorer replaces Meta's private generative backbone.",
    }
