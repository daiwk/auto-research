from __future__ import annotations

from pathlib import Path
from typing import Any

from ..rec_utils import load_movielens_sequences, ranking_metrics
from .model import MementoScorer, collaborative_embeddings


def reproduce_memento(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    del seed
    data = load_movielens_sequences(dataset_dir)
    embeddings = collaborative_embeddings(data)
    validation = []
    for weight in (0.3, 0.5, 0.7, 0.9):
        scorer = MementoScorer(embeddings, weight)
        metric = ranking_metrics(data, scorer.rag_scores, target="validation")
        validation.append((metric["ndcg_at_10"], weight))
    weight = max(validation)[1]
    scorer = MementoScorer(embeddings, weight)
    results = {
        "last_n": ranking_metrics(data, scorer.last_n_scores),
        "memento_mmr": ranking_metrics(data, scorer.rag_scores),
    }
    return {
        "paper": {"arxiv_id": "2605.24051", "title": "Memento: Personalized RAG-Style Long-Retention Data Scaling for Online Ads Recommendation", "url": "https://arxiv.org/abs/2605.24051", "track": "recommendation"},
        "dataset": "MovieLens 100K (long-history retrieval over positive interactions)",
        "setup": {"users": len(data.train), "items": data.item_count, "retrieved_memories": 8, "validation_selected_relevance_weight": weight},
        "results": results,
        "ndcg_gain_percent": 100 * (results["memento_mmr"]["ndcg_at_10"] - results["last_n"]["ndcg_at_10"]) / max(results["last_n"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"ctr_lift_percent": 1.0, "cvr_lift_percent": 1.2},
        "scope": "Reproduces query-conditioned MMR retrieval balancing relevance and diversity over retained histories. MovieLens interactions replace Meta's 365-day embedding corpus; distributed INT8 serving, Ember, and data replay are out of scope.",
    }
