from __future__ import annotations

import os
from pathlib import Path

from ..industrial_ranking import evaluate_model
from ..rec_utils import load_movielens_sequences
from .model import RankMixerConfig, train_model


def reproduce_tokenmixer_large(dataset_dir: Path, seed: int = 42):
    data = load_movielens_sequences(dataset_dir)
    config = RankMixerConfig(
        dimensions=32, tokens=4, layers=3, batch_size=24, negatives=15,
        steps=int(os.environ.get("AUTO_RESEARCH_TOKENMIXER_LARGE_STEPS", "80")),
        interval_residual=2, auxiliary_weight=0.15,
    )
    models, training, metrics = {}, {}, {}
    for kind in ("rankmixer_dense", "tokenmixer_large"):
        models[kind], training[kind] = train_model(kind, data, config, seed)
        metrics[kind] = evaluate_model(models[kind], data, config)
    baseline, method = metrics["rankmixer_dense"], metrics["tokenmixer_large"]
    return {
        "paper": {"arxiv_id": "2602.06563", "title": "TokenMixer-Large: Scaling Token Mixing for Industrial Recommendation", "url": "https://arxiv.org/abs/2602.06563", "organization": "ByteDance"},
        "dataset": {"name": "MovieLens 100K", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "steps": config.steps, "same_hyperparameters": True},
        "baseline": {"name": "RankMixer dense", **baseline},
        "method": {"name": "TokenMixer-Large", **method},
        "relative": {
            "hit_at_10_percent": 100 * (method["hit_at_10"] - baseline["hit_at_10"]) / max(baseline["hit_at_10"], 1e-12),
            "ndcg_at_10_percent": 100 * (method["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        },
        "training": training,
        "stages": {"mixing_reverting": True, "head_swiglu": True, "token_swiglu": True, "interval_residual": config.interval_residual, "auxiliary_head": True},
        "paper_results": {"online_orders_percent": 1.66, "online_payment_gmv_percent": 2.98, "ads_adss_percent": 2.0, "live_revenue_percent": 1.4},
        "scope": "实际训练 mixing→per-head SwiGLU→reverting→per-token SwiGLU、interval residual 和中层辅助损失；仅缩小维度、层数和公开特征，未复刻字节万亿级样本与生产 kernel。",
    }
