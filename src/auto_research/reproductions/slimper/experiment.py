from __future__ import annotations

from pathlib import Path

from ..industrial_batch import evaluate_scores
from ..llm_training import require_torch
from .model import SlimPerConfig, build_models, complexity, score_catalog, train


def reproduce_slimper(dataset_dir: Path, seed: int = 42) -> dict:
    from ..industrial_batch import compact_movielens
    torch = require_torch(); data = compact_movielens(dataset_dir, maximum_users=220, maximum_items=360)
    config = SlimPerConfig(item_count=data.item_count)
    baseline_model, slimmer_model = build_models(config, data.features, torch)
    baseline_training = train(baseline_model, data, config, seed, torch)
    slimmer_training = train(slimmer_model, data, config, seed, torch)
    baseline = evaluate_scores(data, lambda history: score_catalog(baseline_model, history, config, torch))
    method = evaluate_scores(data, lambda history: score_catalog(slimmer_model, history, config, torch))
    relative = {key + "_percent": 100 * (method[key] - baseline[key]) / max(abs(baseline[key]), 1e-12) for key in ("hit_at_10", "ndcg_at_10", "head_share_at_10")}
    costs = complexity(config)
    relative["attention_score_reduction_percent"] = 100 * (1 - costs["slimper_attention_score_elements"] / costs["baseline_attention_score_elements"])
    relative["intermediate_reduction_percent"] = 100 * (1 - costs["slimper_intermediate_elements"] / costs["baseline_intermediate_elements"])
    return {
        "paper": {"arxiv_id": "2607.12281", "title": "SlimPer: Make Personalization Model Slim and Smart", "url": "https://arxiv.org/abs/2607.12281", "organization": "Meta"},
        "dataset": {"name": "MovieLens 100K", "users": len(data.train), "items": data.item_count},
        "setup": {"seed": seed, "same_rows_features_optimizer_and_steps": True, "history_length": config.maximum_length, "slimper_layers": config.layers, "baseline_layers": config.baseline_layers, "knowledge_slots": config.knowledge_slots, "query_slots": config.query_slots, "template_slots": config.template_slots},
        "baseline": {"name": "full-sequence Transformer ranker", **baseline},
        "method": {"name": "SlimPer Select-Match-Refine", **method},
        "relative": relative, "training": {"baseline": baseline_training, "slimper": slimmer_training}, "complexity": costs,
        "paper_results": {"Reels_2k_reshare_NE_percent": -0.51, "Reels_2k_QPS_percent": 11.0, "Reels_2k_memory_percent": -9.32, "Feed_1k_memory_percent": -18.12, "FLOPs_reduction_range": "8x–25x", "online": "full-traffic statistically significant engagement gains; aggregate topline about 10x a typical significant launch; exact lift not disclosed"},
        "scope": "实际训练逐层 Select–Match–Refine：candidate/user 初始化固定 knowledge slots，segment-wise Q/T projection 对每层原始历史 token 做选择，显式 q×t relevance matching，MLP residual refinement 和跨层 task-logit 累加；full-catalog 推理只编码一次 user tokens 并跨候选共享。MovieLens 单目标与 32-event 历史替代 Instagram 多模态 1k–10k+ events。",
    }
