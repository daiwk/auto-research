from __future__ import annotations

from pathlib import Path

import numpy as np

from ..industrial_batch import CompactSequences, evaluate_scores
from ..llm_training import require_torch
from ..rec_utils import load_movielens_1m_sequences
from .model import RecGPTV3Config, build_models, diagnostics, score_catalog, semantic_ids, train


def _compact_ml1m(root: Path, maximum_users=360, maximum_items=520):
    raw = load_movielens_1m_sequences(root)
    selected = set(np.argsort(-raw.popularity)[:maximum_items].tolist())
    rows = []
    for history, validation, test in zip(raw.train, raw.validation, raw.test):
        sequence = [item for item in (*history, validation, test) if item in selected]
        if len(sequence) >= 9:
            rows.append(sequence)
        if len(rows) >= maximum_users:
            break
    items = sorted({item for row in rows for item in row})
    mapping = {item: index for index, item in enumerate(items)}
    encoded = [[mapping[item] for item in row] for row in rows]
    return CompactSequences(
        train=tuple(tuple(row[:-2]) for row in encoded), validation=tuple(row[-2] for row in encoded),
        test=tuple(row[-1] for row in encoded), features=raw.item_features[items].astype(np.float32),
        popularity=raw.popularity[items].astype(np.float32),
    )


def reproduce_recgpt_v3(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch(); data = _compact_ml1m(dataset_dir)
    config = RecGPTV3Config()
    ids, rqvae = semantic_ids(data.features, config, seed)
    baseline_model, method_model = build_models(data.features, ids, config)
    baseline_model, baseline_training = train(baseline_model, data, config, seed, method=False)
    method_model, method_training = train(method_model, data, config, seed, method=True)
    baseline = evaluate_scores(data, lambda history: score_catalog(baseline_model, history, config, torch))
    method = evaluate_scores(data, lambda history: score_catalog(method_model, history, config, torch))
    relative = {key + "_percent": 100 * (method[key] - baseline[key]) / max(abs(baseline[key]), 1e-12) for key in ("hit_at_10", "ndcg_at_10", "head_share_at_10")}
    return {
        "paper": {"arxiv_id": "2607.15591", "title": "RecGPT-V3 Technical Report", "url": "https://arxiv.org/abs/2607.15591", "organization": "Alibaba / Taobao"},
        "dataset": {"name": "MovieLens 1M", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "steps_per_model": config.training_steps, "history_length": config.maximum_history, "memory_slots": config.memory_slots, "recent_events": config.recent_events, "latent_tokens": config.latent_tokens, "semantic_id_levels": 2},
        "baseline": {"name": "RecGPT-V2-style stateless full-history hybrid Transformer", **baseline},
        "method": {"name": "RecGPT-V3 memory + hybrid SID/text + latent reasoning", **method},
        "relative": relative, "rqvae": rqvae, "diagnostics": diagnostics(method_model, data, config, torch),
        "training": {"baseline": baseline_training, "recgpt_v3": method_training},
        "paper_results": {"item_IPV_percent": 3.08, "item_CTR_percent": 0.98, "item_GMV_percent": 7.51, "feed_IPV_percent": 1.28, "feed_CTR_percent": 1.00, "feed_GMV_percent": 3.97, "memory_compute_reduction_percent": 55.8, "serving_resource_reduction_percent": 52.4, "reasoning_token_reduction": "200x"},
        "scope": "实际训练两级 RQ-VAE Semantic ID、文本/类型与 SID 的共享 item tower、full-history 显式教师、固定容量可追溯 memory attention、latent-token 多段重建蒸馏和 dense ranking-feedback KL。MovieLens genre 替代淘宝文本/图像/属性，公开 popularity+teacher reward 替代生产 CTR ranker；未执行 14B CPT/SFT、DeepSeek teacher 或线上 GRPO。",
    }
