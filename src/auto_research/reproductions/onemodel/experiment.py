from __future__ import annotations

from pathlib import Path

from ..recent_20260728_common import full_catalog_metrics, load_recent_movielens, relative
from .model import fit_onemodel, score_global, score_onemodel


def reproduce_onemodel(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_recent_movielens(dataset_dir, maximum_users=320, maximum_items=480)
    state = fit_onemodel(data)
    baseline = full_catalog_metrics(data, lambda history: score_global(state, history))
    method = full_catalog_metrics(data, lambda history: score_onemodel(state, history))
    return {
        "paper": {"arxiv_id": "2608.18606", "title": "OneModel"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "scenarios": 3, "full_catalog": True},
        "variants": {"shared global ranker": baseline, "OneModel scenario-aware": method},
        "relative": relative(method, baseline),
        "paper_results": {
            "explore_time_spent_percent": 0.33,
            "explore_engagement_percent": 1.25,
            "ads_value_percent": 3.43,
            "ads_ctr_percent": 8.18,
            "merchant_dgmv_percent": 1.1867,
            "merchant_gpm_percent": 2.1585,
        },
        "scope": "在 MovieLens-1M 上真实执行共享转移 backbone、由公开 genre 派生的三场景 projection、SAIM 式 sigmoid gate 以及 global-pool/local-state 分层表征；未复刻小红书私有多流日志、统一 Transformer decoder、梯度隔离和生产 serving。",
    }
