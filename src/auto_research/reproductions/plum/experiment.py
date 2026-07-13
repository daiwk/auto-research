from pathlib import Path
from typing import Any

import numpy as np

from ..cluster_goobs.model import train_retriever
from ..rec_utils import load_movielens_1m_sequences, ranking_metrics
from .model import PLUMScorer, build_semantic_ids


def reproduce_plum(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_1m_sequences(dataset_dir)
    backbone = train_retriever(data, "random_oob", seed, epochs=3, training_cap=100000)
    item_codes, semantic_prior = build_semantic_ids(data)
    baseline = PLUMScorer(backbone, semantic_prior, item_codes, data.item_features, 0.0)
    choices = []
    for weight in (0.02, 0.05, 0.1, 0.2, 0.35):
        scorer = PLUMScorer(backbone, semantic_prior, item_codes, data.item_features, weight)
        metric = ranking_metrics(data, scorer.generative_semantic_id_scores, target="validation")
        choices.append((metric["ndcg_at_10"], weight))
    weight = max(choices)[1]
    proposed = PLUMScorer(backbone, semantic_prior, item_codes, data.item_features, weight)
    results = {
        "large_embedding_retrieval": ranking_metrics(data, baseline.large_embedding_scores),
        "plum_semantic_id_generation": ranking_metrics(data, proposed.generative_semantic_id_scores),
    }
    base, new = results.values()
    return {
        "paper": {"arxiv_id": "2510.07784", "title": "PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations", "url": "https://arxiv.org/abs/2510.07784", "track": "recommendation"},
        "dataset": "MovieLens 1M (public semantic-ID proxy; YouTube corpus is private)",
        "setup": {"users": len(data.train), "items": data.item_count, "semantic_codes": int(len(np.unique(item_codes))), "seed": seed, "training_transition_cap": 100000, "validation_selected_semantic_weight": weight},
        "results": results,
        "ndcg_gain_percent": 100 * (new["ndcg_at_10"] - base["ndcg_at_10"]) / max(base["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"lfv_engaged_users_percent": 0.07, "lfv_panel_ctr_percent": 0.76, "shorts_engaged_users_percent": 0.28, "shorts_panel_ctr_percent": 4.96},
        "scope": "Reproduces semantic IDs, domain co-occurrence pretraining, and generative semantic-code scoring on a compact retrieval backbone. Gemini MoE CPT, text tokens, beam search, and billion-video serving are out of scope.",
    }
