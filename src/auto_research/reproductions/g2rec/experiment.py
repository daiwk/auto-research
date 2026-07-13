from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any

import numpy as np

from ..rec_utils import load_amazon_beauty_sequences
from .model import (
    G2RecConfig,
    next_item_logits,
    train_decoder,
    train_soft_membership,
)


def reproduce_g2rec(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_amazon_beauty_sequences(dataset_dir)
    config = G2RecConfig(
        graph_steps=int(os.environ.get("AUTO_RESEARCH_G2REC_GRAPH_STEPS", "120")),
        training_steps=int(os.environ.get("AUTO_RESEARCH_G2REC_STEPS", "240")),
        evaluation_users=int(os.environ.get("AUTO_RESEARCH_G2REC_EVAL_USERS", "1000")),
    )
    membership, graph_training = train_soft_membership(data, config, seed)
    baseline, baseline_training = train_decoder(
        "item_only", data, membership, config, seed
    )
    proposed, proposed_training = train_decoder(
        "g2rec", data, membership, config, seed
    )
    results = {
        "item_tokens_only": sampled_ranking_metrics(
            data, baseline, "item_only", config, seed + 1
        ),
        "g2rec_item_plus_interest_tokens": sampled_ranking_metrics(
            data, proposed, "g2rec", config, seed + 1
        ),
    }
    return {
        "paper": {"arxiv_id": "2606.20554", "title": "Structuring and Tokenizing Distributed User Interest Context for Generative Recommendation", "url": "https://arxiv.org/abs/2606.20554", "track": "recommendation"},
        "dataset": "Amazon Beauty 5-core (paper public dataset)",
        "setup": {
            "users": len(data.train), "items": data.item_count,
            "soft_interest_tokens": config.interests,
            "training_steps": config.training_steps,
            "profile_loss_weight": config.profile_weight,
            "evaluation_users": min(config.evaluation_users, len(data.train)),
            "evaluation": "one positive + 99 sampled negatives per user",
        },
        "training": {
            "soft_graph_clustering": graph_training,
            "item_only": baseline_training,
            "g2rec": proposed_training,
        },
        "results": results,
        "ndcg_gain_percent": 100 * (results["g2rec_item_plus_interest_tokens"]["ndcg_at_10"] - results["item_tokens_only"]["ndcg_at_10"]) / max(results["item_tokens_only"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"in_session_lift_lower_bound_percent": 0.03, "engagement_lift_range_percent": [0.06, 0.19]},
        "scope": "Trains G2Rec's sparse co-engagement soft-modularity profiles, alternating item/continuous-interest token decoder, next-item loss, and profile-prediction loss on the paper's public Beauty dataset. A 96d two-layer decoder replaces Llama-2-13B and evaluation is capped for local Mac runtime.",
    }


def sampled_ranking_metrics(data, model, kind, config, seed: int):
    rng = np.random.default_rng(seed)
    users = np.arange(len(data.train))
    rng.shuffle(users)
    users = users[: min(config.evaluation_users, len(users))]
    hits = ndcg = 0.0
    recommended: list[int] = []
    for user in users:
        history = data.train[user] + (data.validation[user],)
        expected = data.test[user]
        excluded = set(history) | {expected}
        negatives: set[int] = set()
        while len(negatives) < min(99, data.item_count - len(excluded)):
            negatives.update(
                int(item) for item in rng.integers(0, data.item_count, 256)
                if int(item) not in excluded
            )
        candidates = np.asarray([expected, *list(negatives)[:99]], dtype=np.int64)
        scores = next_item_logits(model, kind, history, config)[candidates]
        order = np.argsort(scores)[::-1]
        recommended.extend(int(candidates[position]) for position in order[:10])
        position = int(np.flatnonzero(order == 0)[0])
        if position < 10:
            hits += 1.0
            ndcg += 1.0 / math.log2(position + 2)
    head = set(np.argsort(data.popularity)[-max(1, data.item_count // 10):])
    count = max(1, len(users))
    return {
        "hit_at_10": hits / count,
        "ndcg_at_10": ndcg / count,
        "head_share_at_10": sum(item in head for item in recommended) / max(1, len(recommended)),
    }
