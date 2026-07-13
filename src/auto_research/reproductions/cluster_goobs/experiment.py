from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from ..rec_utils import load_movielens_1m_sequences, ranking_metrics, summarize_runs
from .model import train_retriever


def reproduce_cluster_goobs(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_1m_sequences(dataset_dir)
    runs: dict[str, list[dict[str, float]]] = {"random_oob": [], "cluster_goobs": []}
    for offset in range(3):
        for method in runs:
            model = train_retriever(data, method, seed + offset)
            runs[method].append(
                ranking_metrics(
                    data,
                    lambda history, model=model: model.scores(
                        history[-1], np.arange(data.item_count)
                    ),
                )
            )
    results = {method: summarize_runs(values) for method, values in runs.items()}
    baseline = results["random_oob"]
    proposed = results["cluster_goobs"]
    return {
        "paper": {
            "arxiv_id": "2607.00448",
            "title": "Real-Time Hard Negative Sampling via LLM-based Clustering for Large-Scale Two-Tower Retrieval",
            "url": "https://arxiv.org/abs/2607.00448",
            "track": "recommendation",
        },
        "dataset": "MovieLens 1M (paper public dataset; ratings >= 3; genres form paper's public clusters)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "epochs": 3, "training_transition_cap_per_seed": 100000},
        "results": results,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "head_share_change_percent": 100 * (proposed["head_share_at_10"] - baseline["head_share_at_10"]) / max(baseline["head_share_at_10"], 1e-12),
        "paper_online_ab": {"ctr_lift_percent": 53.0, "top_100_impression_share_control_percent": 50.0, "top_100_impression_share_treatment_percent": 32.0},
        "scope": "The cluster-conditioned real-time sampler is reproduced. Public MovieLens genres replace Meta's private LLM media embeddings; GOOBS distributed serving infrastructure is out of scope.",
    }
