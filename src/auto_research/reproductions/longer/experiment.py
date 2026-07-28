from pathlib import Path
from typing import Any

from ..rec_utils import load_movielens_sequences, summarize_runs
from ..trainable_sequence_core import SequenceTrainConfig, evaluate_pairwise, train_pairwise
from .model import build_longer_model


def reproduce_longer(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    config = SequenceTrainConfig()
    baseline_runs, longer_runs, training = [], [], []
    for run_seed in (seed, seed + 1, seed + 2):
        baseline, baseline_trace = train_pairwise(
            build_longer_model(data.item_count, config.dimensions, method="recent"),
            data, config, run_seed,
        )
        longer, longer_trace = train_pairwise(
            build_longer_model(data.item_count, config.dimensions, method="longer"),
            data, config, run_seed,
        )
        baseline_runs.append(evaluate_pairwise(baseline, data, config))
        longer_runs.append(evaluate_pairwise(longer, data, config))
        training.append({"seed": run_seed, "baseline": baseline_trace, "longer": longer_trace})
    results = {
        "recent_sequence_transformer": summarize_runs(baseline_runs),
        "longer_hybrid_attention": summarize_runs(longer_runs),
    }
    baseline, proposed = results.values()
    return {
        "paper": {"arxiv_id": "2505.04421", "title": "LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders", "url": "https://arxiv.org/abs/2505.04421", "track": "recommendation"},
        "dataset": "MovieLens 100K (full public interactions; ByteDance data is private)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "group_size": 4, "history_length": config.history_length, "training": training},
        "results": results,
        "ndcg_gain_percent": 100 * (proposed["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"douyin_ads_adss_range_percent": [1.063, 2.097], "douyin_ecommerce_order_per_user_range_percent": [4.6125, 7.9222]},
        "scope": "Core-mechanism reproduction: trains InnerTrans group compression, a global interest token and hybrid attention end to end. Private Douyin features, distributed kernels and production serving are not reproduced.",
    }
