from pathlib import Path

from ..recent_20260728_common import full_catalog_metrics, load_recent_movielens, relative
from .model import diagnostics, score_transretrieval, score_two_tower


def reproduce_transretrieval(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_recent_movielens(dataset_dir, maximum_users=320, maximum_items=480)
    baseline = full_catalog_metrics(data, lambda h: score_two_tower(data, h))
    method = full_catalog_metrics(data, lambda h: score_transretrieval(data, h))
    return {
        "paper": {"arxiv_id": "2608.25528", "title": "TransRetrieval"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "full_catalog": True, "history_length": 20},
        "variants": {"Transformer two-tower": baseline, "TransRetrieval core": method},
        "relative": relative(method, baseline),
        "diagnostics": diagnostics(data),
        "paper_results": {"revenue_lift_percent": 2.53, "rpm_lift_percent": 1.28},
        "scope": "在 MovieLens-1M 上执行 norm-aware weighted aggregation、8→1 target token compression 与 position-style domain embedding；未复刻 400 亿交互、52M 广告库和生产 ANN serving。",
    }
