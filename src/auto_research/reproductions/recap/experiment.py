from __future__ import annotations

import copy
from pathlib import Path

import numpy as np

from ..industrial_2026 import base_scores, evaluate, gain, load_industrial_data, tune_blend
from ..llm_training import require_torch
from .model import bounded_profile, train_evaluator, train_grpo, train_sft


def reproduce_recap(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch(); data = load_industrial_data(dataset_dir)
    sft, (rows, targets), sft_stats = train_sft(data, seed, torch)
    reference = copy.deepcopy(sft).eval(); categories = int(data.domains.max()) + 1
    evaluator = train_evaluator(rows, targets, categories, seed, torch)
    grpo_stats = train_grpo(sft, reference, evaluator, rows, targets, categories, seed, torch)

    def profile_score(policy, history):
        profile = bounded_profile(policy, data, history, torch)
        return profile[data.domains]
    baseline_fn = lambda history: base_scores(data, history)
    sft_alpha, sft_scorer, _ = tune_blend(data, baseline_fn, lambda h: profile_score(reference, h))
    recap_alpha, recap_scorer, validation = tune_blend(data, baseline_fn, lambda h: profile_score(sft, h))
    baseline = evaluate(data, sft_scorer); method = evaluate(data, recap_scorer)
    return {
        "paper": {"arxiv_id": "2607.15730", "title": "RECAP: Feedback-Driven Streaming Semantic User Profiles for Short-Video Recommendation", "url": "https://arxiv.org/abs/2607.15730", "organization": "Kuaishou"},
        "dataset": {"name": "MovieLens 100K", "users": len(data.sequences.train), "items": data.item_count},
        "setup": {"seed": seed, "same_base_ranker_and_split": True, "profile_capacity": 4},
        "baseline": {"name": "open-loop SFT streaming profile", **baseline},
        "method": {"name": "RECAP feedback-optimized profile", **method}, "relative": gain(method, baseline),
        "training": {"sft": sft_stats, "grpo": grpo_stats},
        "validation": {"sft_blend": sft_alpha, "recap_blend": recap_alpha, **validation},
        "stages": {"causal_transformer_updater": True, "bounded_structured_memory": True, "deterministic_decay_merge_evict": True, "dual_tower_evaluator": True, "label_consistent_reward": True, "clipped_grpo": True},
        "paper_results": {"uAUC_absolute": 0.0084, "Recall_at_2000_percent": 4.9, "AppStayTime_per_user_percent": 0.139},
        "scope": "实际训练 causal Transformer 流式 profile updater（SFT），训练双塔反馈 evaluator，再进行 group-size=4 的 clipped GRPO；推理执行固定容量 profile 的 decay/refresh/merge/evict 状态机。MovieLens genre token 与隐式 next-item feedback 替代快手自然语言 profile、生产日志和大参数 LLM。",
    }
