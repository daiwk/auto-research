from pathlib import Path

from ..recent_20260728_common import full_catalog_metrics, load_recent_movielens, relative
from .model import build_item_graph, score_candidates


def reproduce_friend_gnn(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_recent_movielens(dataset_dir, maximum_users=320, maximum_items=480)
    baseline = full_catalog_metrics(data, lambda history: score_candidates(data, history, use_temporal_hash=False))
    method = full_catalog_metrics(data, lambda history: score_candidates(data, history, use_temporal_hash=True))
    temporal, _ = build_item_graph(data.train)
    edge_count = sum(map(len, temporal.values()))
    return {
        "paper": {"arxiv_id": "2608.27413", "title": "Scaling GNNs for Friend Recommendation"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "full_catalog": True, "temporal_edges": edge_count, "hash_functions": 3},
        "variants": {"popularity ranker": baseline, "multi-hash temporal GNN proxy": method},
        "relative": relative(method, baseline),
        "diagnostics": {
            "hash_table_rows": max(32, data.item_count // 4),
            "nominal_full_table_rows": data.item_count,
            "temporal_lookup": "bisect_left over timestamp-sorted adjacency",
        },
        "paper_results": {
            "friend_additions_lift_percent": 16.0,
            "unique_friend_adders_lift_percent": 11.5,
            "embedding_table_reduction_percent": 98.0,
        },
        "scope": "在 MovieLens-1M 顺序交互上验证多哈希表示、按时间排序邻接表与二分 cutoff；未复刻 VK 的 194M 用户图、GATv2 分布式训练和线上排序器。",
    }
