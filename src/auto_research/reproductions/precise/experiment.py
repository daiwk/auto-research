from __future__ import annotations

import os
from pathlib import Path

from ..industrial_ranking import require_backend
from .data import load_precise_data
from .model import PreciseConfig, build_precise, evaluate, initialize_llm_tokens, targeted_train, universal_train


def reproduce_precise(dataset_dir: Path, seed: int = 42):
    config = PreciseConfig(
        maximum_users=int(os.environ.get("AUTO_RESEARCH_PRECISE_USERS", "300")),
        universal_steps=int(os.environ.get("AUTO_RESEARCH_PRECISE_UT_STEPS", "120")),
        targeted_steps=int(os.environ.get("AUTO_RESEARCH_PRECISE_TT_STEPS", "240")),
    )
    data = load_precise_data(dataset_dir, config.maximum_users)
    tokens, mask, initialization = initialize_llm_tokens(data, dataset_dir, config)

    torch, _ = require_backend()
    torch.manual_seed(seed)
    target_only = build_precise(len(data.item_texts), tokens, mask, config)
    target_training = targeted_train(target_only, data.targeted, config, seed)
    target_metrics = evaluate(target_only, data, config)

    torch.manual_seed(seed)
    precise = build_precise(len(data.item_texts), tokens, mask, config)
    universal_training = universal_train(precise, data.universal, config, seed)
    progressive_training = targeted_train(precise, data.targeted, config, seed)
    precise_metrics = evaluate(precise, data, config)

    return {
        "paper": {"arxiv_id": "2412.06308", "title": "PRECISE: Pre-training Sequential Recommenders with Collaborative and Semantic Information", "url": "https://arxiv.org/abs/2412.06308", "track": "recommendation"},
        "dataset": "MovieLens-1M chronological positive feedback; ratings >=4 are the sparse target task",
        "setup": {"seed": seed, "users": len(data.targeted), "items": len(data.item_texts), "llm": config.model_name, "text_tokens": config.text_tokens, "universal_steps": config.universal_steps, "targeted_steps": config.targeted_steps, "initialization": initialization},
        "training": {"target_only": target_training, "universal": universal_training, "progressive_targeted": progressive_training},
        "results": {"precise_tt_only": target_metrics, "precise_ut_plus_tt": precise_metrics},
        "paper_online_ab": {"ranking_clicks_percent": 1.961, "ranking_shares_percent": 1.433, "participants": "180M"},
        "scope": "Executes contextual LLM token initialization, trainable token states, top-k MoE attention experts, ID/text alternate training, causal all-position next-item pre-training, no-mask target training, concatenated user MLP, and cross-user BPR. Public MovieLens feedback substitutes private WeChat scenes.",
    }
