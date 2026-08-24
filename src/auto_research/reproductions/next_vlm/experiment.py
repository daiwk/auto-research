from pathlib import Path

import numpy as np

from ..genrec_netflix.data import load_genrec_data
from ..recent_20260728_common import full_catalog_metrics, relative
from .model import fit_next, next_scores, production_baseline


def reproduce_next(dataset_dir: Path, seed: int = 42):
    del seed
    data = load_genrec_data(dataset_dir)
    state = fit_next(data)
    baseline = full_catalog_metrics(data, lambda history: production_baseline(state, history))
    method = full_catalog_metrics(data, lambda history: next_scores(state, history))
    edge_count = int(np.count_nonzero(state["verified_nkg"]))
    return {
        "paper": {"arxiv_id": "2607.24789", "title": "NEXT"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": len(data.item_texts)},
        "variants": {"optimized multi-path baseline": baseline, "NEXT verified intent edges": method},
        "relative": relative(method, baseline),
        "mechanism": {"verified_nkg_edges": edge_count, "offline_reasoning": True, "online_direct_injection": True},
        "paper_results": {"watch_time_percent": 0.53, "distinct_video_exposure_percent": 0.51, "users_approx": 100_000_000},
        "scope": "用公开标题/genre 与协同转移执行 item→intent→item、离线边生成/验证和在线加性注入；未训练论文 8B VLM，也没有 Meta 私有短视频、安全或实时 serving 信号。",
    }
