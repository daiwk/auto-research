from pathlib import Path

from ..industrial_2026 import evaluate, gain, load_industrial_data
from .model import fit_oneshot, oneshot_scores, two_tower_scores


def reproduce_oneshot(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir)
    state = fit_oneshot(data, seed)
    baseline = evaluate(data, lambda history: two_tower_scores(data, state, history))
    method = evaluate(data, lambda history: oneshot_scores(data, state, history))
    return {
        "paper": {"arxiv_id": "2607.27475", "title": "OneShot"},
        "dataset": {"name": "MovieLens 100K", "users": len(data.sequences.train), "items": data.item_count},
        "variants": {"two-tower dot-product retrieval": baseline, "OneShot index-in-ranking": method},
        "relative": gain(method, baseline),
        "mechanism": {"index_levels": 2, "branching": 8, "neural_scoring": True, "straight_through_proxy": "ranking-shaped deterministic assignments"},
        "paper_results": {"recall_percent": 20.0, "efficiency_multiple": 10.0, "sessions_percent": 0.035, "watch_time_percent": 0.136, "source_rate_percent": 61.58},
        "scope": "在公开数据上执行 ranking-shaped 两层索引、路径级候选探测和非点积 neural scoring；小规模 NumPy 版本以确定性 assignment 代理 STE/SCO，未复刻十亿级 Instagram 索引和分布式 serving。",
    }
