from __future__ import annotations

from pathlib import Path

from ..recent_20260728_common import full_catalog_metrics, load_recent_movielens, relative
from .model import fit_tagr, score_production_baseline, score_tagr


def reproduce_tagr(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_recent_movielens(dataset_dir, maximum_users=320, maximum_items=480)
    state = fit_tagr(data)
    baseline = full_catalog_metrics(data, lambda history: score_production_baseline(state, history))
    method = full_catalog_metrics(data, lambda history: score_tagr(state, history))
    return {
        "paper": {"arxiv_id": "2608.24034", "title": "TAGR"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "full_catalog": True, "lsid_levels": 2, "intent_scales": 3},
        "variants": {"production-style transition baseline": baseline, "TAGR core": method},
        "relative": relative(method, baseline),
        "paper_results": {
            "live_room_entry_rate_lift_percent": 8.5,
            "shopping_cart_click_rate_lift_percent": 7.4,
            "revenue_lift_percent": 16.1,
        },
        "scope": "在 MovieLens-1M 上真实执行可刷新但词表稳定的两级 LSID、多尺度 intent 聚合，以及行为/价值双分支的有界 IOPO 推理 analogue；未复刻快手实时广告日志、在线 RM/GRPO 更新和生产 serving。",
    }
