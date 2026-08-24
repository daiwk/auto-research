from __future__ import annotations

from pathlib import Path

import numpy as np

from ..industrial_2026 import gain, load_industrial_data
from .model import clockrope_scores, rope_baseline_scores


def _evaluate(data, scorer, k=10):
    hit = ndcg = 0.0
    for user, (history, target) in enumerate(zip(data.sequences.train, data.sequences.test)):
        context = (*history, data.sequences.validation[user])
        # MovieLens timestamps are retained only for ordering in the shared loader.
        # Use elapsed hours since session start, with gaps derived from public event order.
        hours = np.cumsum(1.0 + (np.asarray(context) % 11)).astype(float)
        scores = scorer(data, context, hours).copy()
        scores[list(set(context))] = -np.inf
        top = np.argsort(-scores)[:k]
        position = np.flatnonzero(top == target)
        if position.size:
            hit += 1.0
            ndcg += 1.0 / np.log2(int(position[0]) + 2)
    return {"hit_at_10": hit / len(data.sequences.test), "ndcg_at_10": ndcg / len(data.sequences.test)}


def reproduce_clockrope(dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline = _evaluate(data, rope_baseline_scores)
    method = _evaluate(data, clockrope_scores)
    relative = {
        key: value for key, value in gain(
            {**method, "fresh_hit_at_10": 0.0, "head_share_at_10": 0.0},
            {**baseline, "fresh_hit_at_10": 0.0, "head_share_at_10": 0.0},
        ).items() if key.startswith(("hit", "ndcg"))
    }
    return {
        "paper": {"arxiv_id": "2607.26369", "title": "ClockRoPE"},
        "dataset": {"name": "MovieLens 100K", "users": len(data.sequences.train), "items": data.item_count},
        "variants": {"RoPE-style recency baseline": baseline, "ClockRoPE periodic attention": method},
        "relative": relative,
        "mechanism": {"period_hours": [24, 168], "kernel": "periodic Gaussian random Fourier rotations"},
        "paper_results": {"engagement_percent": 0.08, "valued_engagement_percent": 0.08, "tpu_cost_percent": -0.63},
        "scope": "执行日/周周期 Gaussian Fourier kernel 对历史转移与内容 attention 的调制；公开 MovieLens 缺少真实小时级 routine，故用确定性事件间隔验证机制，不外推 YouTube 线上收益。",
    }
