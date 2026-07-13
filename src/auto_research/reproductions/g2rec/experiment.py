from __future__ import annotations

from pathlib import Path
from typing import Any

import math

import numpy as np

from ..rec_utils import load_amazon_beauty_sequences
from .model import G2RecScorer, build_graph_tokens


def reproduce_g2rec(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    del seed  # Graph construction is deterministic for reproducible comparison.
    data = load_amazon_beauty_sequences(dataset_dir)
    graph, membership = build_graph_tokens(data)
    baseline = G2RecScorer(graph, membership, beta=0.0)
    candidates = []
    for beta in (0.15, 0.3, 0.45, 0.6, 0.75):
        scorer = G2RecScorer(graph, membership, beta)
        metric = sampled_ranking_metrics(
            data, scorer.interest_token_scores, seed=2606, target="validation"
        )
        candidates.append((metric["ndcg_at_10"], beta))
    beta = max(candidates)[1]
    proposed = G2RecScorer(graph, membership, beta)
    results = {
        "item_tokens_only": sampled_ranking_metrics(
            data, baseline.item_only_scores, seed=2607
        ),
        "g2rec_item_plus_interest_tokens": sampled_ranking_metrics(
            data, proposed.interest_token_scores, seed=2607
        ),
    }
    return {
        "paper": {"arxiv_id": "2606.20554", "title": "Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation", "url": "https://arxiv.org/abs/2606.20554", "track": "recommendation"},
        "dataset": "Amazon Beauty 5-core (paper public dataset; item-item co-engagement graph)",
        "setup": {"users": len(data.train), "items": data.item_count, "soft_interest_tokens": membership.shape[1], "validation_selected_beta": beta, "evaluation": "one positive + 99 sampled negatives per user (paper protocol)"},
        "results": results,
        "ndcg_gain_percent": 100 * (results["g2rec_item_plus_interest_tokens"]["ndcg_at_10"] - results["item_tokens_only"]["ndcg_at_10"]) / max(results["item_tokens_only"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"in_session_lift_lower_bound_percent": 0.03, "engagement_lift_range_percent": [0.06, 0.19]},
        "scope": "Reproduces item-item co-engagement graph construction, soft interest prototypes, alternating item/interest representation, and validation-selected fusion. A compact graph next-token scorer replaces Meta's private generative backbone.",
    }


def sampled_ranking_metrics(data, scorer, seed: int, target: str = "test"):
    rng = np.random.default_rng(seed)
    targets = data.test if target == "test" else data.validation
    hits = ndcg = 0.0
    recommended: list[int] = []
    for index, (history, expected) in enumerate(zip(data.train, targets, strict=True)):
        context = history + ((data.validation[index],) if target == "test" else ())
        excluded = set(context) | {expected}
        negatives_set: set[int] = set()
        wanted = min(99, data.item_count - len(excluded))
        while len(negatives_set) < wanted:
            draws = rng.integers(0, data.item_count, 2 * (wanted - len(negatives_set)))
            negatives_set.update(int(item) for item in draws if int(item) not in excluded)
        negatives = np.fromiter(list(negatives_set)[:wanted], dtype=np.int64)
        candidates = np.concatenate(([expected], negatives))
        scores = scorer(context, candidates)
        order = np.argsort(scores)[::-1]
        recommended.extend(int(candidates[position]) for position in order[:10])
        position = int(np.flatnonzero(order == 0)[0])
        if position < 10:
            hits += 1.0
            ndcg += 1.0 / math.log2(position + 2)
    count = len(targets)
    head = set(np.argsort(data.popularity)[-max(1, data.item_count // 10):])
    popularity = data.popularity / max(data.popularity.sum(), 1.0)
    return {
        "hit_at_10": hits / count,
        "ndcg_at_10": ndcg / count,
        "head_share_at_10": sum(item in head for item in recommended) / len(recommended),
        "mean_popularity_at_10": float(np.mean(popularity[recommended])),
    }
