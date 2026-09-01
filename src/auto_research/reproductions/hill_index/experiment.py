from pathlib import Path

import numpy as np

from ..industrial_2026 import evaluate, load_industrial_data, summary_result
from .model import build_hill, score_hill


def reproduce_hill_index(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    state = build_hill(data, seed)
    baseline = evaluate(data, lambda history: score_hill(data, state, history, False)[0])
    method = evaluate(data, lambda history: score_hill(data, state, history, True)[0])
    sample_histories = data.sequences.train[: min(64, len(data.sequences.train))]
    flat_counts = [score_hill(data, state, history, False)[1] for history in sample_histories]
    hill_counts = [score_hill(data, state, history, True)[1] for history in sample_histories]
    return summary_result(
        key="hill-index",
        paper={
            "arxiv_id": "2604.12965",
            "title": "Efficient Retrieval Scaling with Hierarchical Indexing for Large Scale Recommendation",
            "url": "https://arxiv.org/abs/2604.12965",
            "organization": "Meta",
        },
        data=data,
        baseline_name="one-layer learned index",
        method_name="HILL residual two-layer index",
        baseline=baseline,
        proposed=method,
        stages={
            "coarse_nodes": len(state["coarse_centers"]),
            "residual_children_per_node": 6,
            "flat_mean_scored_items": float(np.mean(flat_counts)),
            "hill_mean_scored_items": float(np.mean(hill_counts)),
            "hill_candidate_fraction": float(np.mean(hill_counts) / data.item_count),
            "test_time_training_nodes": int(
                sum(len(value) for value in state["fine_centers"].values())
            ),
        },
        paper_results={
            "two_layer_monn_medium_small_online_metric_percent": 2.57,
            "two_layer_monn_small_small_online_metric_percent": 1.22,
        },
        scope=(
            "实际学习 coarse attention assignment、跨层 residual quantization、层级 beam 检索，并与同公开切分的"
            "单层索引比较候选量和质量；未复刻 Meta MoNN、十亿级 Ads 索引和分布式 FAISS EM。"
        ),
    )
