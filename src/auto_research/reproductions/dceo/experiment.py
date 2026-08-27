from pathlib import Path

from ..recent_20260728_common import full_catalog_metrics, load_recent_movielens, relative
from .model import causal_diagnostics, score_dceo, score_fixed


def reproduce_dceo(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_recent_movielens(dataset_dir, maximum_users=320, maximum_items=480)
    baseline = full_catalog_metrics(data, lambda history: score_fixed(data, history))
    method = full_catalog_metrics(data, lambda history: score_dceo(data, history))
    return {
        "paper": {"arxiv_id": "2608.25635", "title": "DCEO"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "full_catalog": True, "proxy_objectives": 4},
        "variants": {"fixed multi-objective fusion": baseline, "DCEO core": method},
        "relative": relative(method, baseline),
        "diagnostics": causal_diagnostics(data),
        "paper_results": {"online_gmv_lift_percent": 0.36, "ab_test_days": 41},
        "scope": "在 MovieLens-1M 上执行上下文相关 simplex actor、用户级 proxy 聚合与相对干预诊断；线上只运行 actor。未复刻淘宝私有搜索日志、长期 GMV critic 或生产流量。",
    }
