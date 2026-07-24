from __future__ import annotations

from pathlib import Path

from ..industrial_batch import compact_movielens, evaluate_scores
from ..llm_training import require_torch
from ..tiger.model import (
    TIGERConfig, score_all as score_tiger, train_model as train_tiger,
    train_semantic_ids,
)
from .model import BARGEConfig, build_barge, score_catalog, train_barge, train_osq_ids


def reproduce_barge(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = compact_movielens(dataset_dir, maximum_users=180, maximum_items=300)
    config = BARGEConfig()
    tiger_config = TIGERConfig(
        dimensions=config.dimensions,
        heads=config.heads,
        layers=config.layers,
        sequence_length=config.sequence_length,
        codebooks=config.codebooks,
        codebook_size=config.codebook_size,
        rqvae_steps=config.osq_steps,
        training_steps=config.training_steps,
        batch_size=config.batch_size,
        learning_rate=config.learning_rate,
    )
    single_ids, rq_diagnostics = train_semantic_ids(data.features, tiger_config, seed)
    baseline_model, baseline_training = train_tiger(
        single_ids, data, tiger_config, seed
    )
    dual_ids, osq_diagnostics = train_osq_ids(data.features, config, seed)
    method_model = build_barge(*dual_ids, config)
    method_model, method_training = train_barge(
        method_model, data, config, seed
    )
    baseline = evaluate_scores(
        data,
        lambda history: score_tiger(
            baseline_model, history, data.item_count, tiger_config
        ),
    )
    method = evaluate_scores(
        data,
        lambda history: score_catalog(method_model, history, config, torch),
    )
    relative = {
        key + "_percent": 100 * (method[key] - baseline[key]) / max(abs(baseline[key]), 1e-12)
        for key in ("hit_at_10", "ndcg_at_10", "head_share_at_10")
    }
    return {
        "paper": {
            "arxiv_id": "2607.21028",
            "title": "Bridging the Structural Gap",
            "url": "https://arxiv.org/abs/2607.21028",
            "organization": "Tencent",
        },
        "dataset": {
            "name": "MovieLens 100K",
            "users": len(data.train),
            "items": data.item_count,
        },
        "setup": {
            "seed": seed,
            "same_rows_optimizer_steps_and_model_width": True,
            "steps": config.training_steps,
            "semantic_levels": config.codebooks + 1,
            "beam_fusion": "item-space OR fusion via best channel rank",
        },
        "baseline": {"name": "single-path TIGER-style GR", **baseline},
        "method": {"name": "BARGE ICA + HPR + DPD", **method},
        "relative": relative,
        "training": {
            "baseline": baseline_training,
            "barge": method_training,
        },
        "tokenizers": {
            "rqvae": rq_diagnostics,
            "osqvae": osq_diagnostics,
        },
        "paper_results": {
            "online_ctr_percent": 0.60,
            "online_click_uv_percent": 1.34,
            "online_total_reading_time_percent": 1.70,
        },
        "scope": (
            "实际训练 single-path RQ-VAE/TIGER 对照，以及 BARGE 的 Householder 正交旋转、"
            "双 residual codebooks、逐 item ICA、双 decoder、逐层 symmetric InfoNCE HPR 和"
            "item-id 空间 OR-fusion。MovieLens genre 替代腾讯 item embeddings；"
            "全库 teacher-forced path scoring 替代生产 beam kernel，未使用私有曝光负例。"
        ),
    }
