from __future__ import annotations

import copy
import os
from pathlib import Path

from .model import (
    BEQUEConfig, build_model, build_rewrite_data, evaluate,
    sample_preference_lists, train_pro, train_sft,
)


def reproduce_beque(dataset_dir: Path, seed: int = 42):
    config = BEQUEConfig(
        sft_steps=int(os.environ.get("AUTO_RESEARCH_BEQUE_SFT_STEPS", "60")),
        pro_steps=int(os.environ.get("AUTO_RESEARCH_BEQUE_PRO_STEPS", "20")),
        maximum_train=int(os.environ.get("AUTO_RESEARCH_BEQUE_TRAIN", "600")),
        maximum_test=int(os.environ.get("AUTO_RESEARCH_BEQUE_TEST", "100")),
    )
    data = build_rewrite_data(dataset_dir)
    train, test = data.train[:config.maximum_train], data.test[:config.maximum_test]
    model, tokenizer = build_model(config)
    sft_training = train_sft(model, tokenizer, train, config, seed)
    sft_model = copy.deepcopy(model)
    sft_result = evaluate(sft_model, tokenizer, test, data, config)
    preferences = sample_preference_lists(model, tokenizer, train, data, config)
    pro_training = train_pro(model, tokenizer, preferences, config, seed + 1)
    pro_result = evaluate(model, tokenizer, test, data, config)
    return {
        "paper": {"arxiv_id": "2311.03758", "title": "Large Language Model based Long-tail Query Rewriting in Taobao Search", "url": "https://arxiv.org/abs/2311.03758", "track": "recommendation"},
        "dataset": "MovieLens 100K public catalog text (query-rewrite proxy for private Taobao logs)",
        "setup": {"seed": seed, "model": config.model_name, "train_examples": len(train), "test_examples": len(test), "sft_steps": config.sft_steps, "pro_steps": config.pro_steps, "beams": config.beams},
        "training": {"sft": sft_training, "pro": pro_training},
        "results": {"sft": sft_result, "sft_plus_pro": pro_result},
        "paper_online_ab": {"duration": "14 days", "all_query_gmv_percent": 0.40, "transactions_percent": 0.34, "uv_percent": 0.33, "covered_query_gmv_percent": 2.96},
        "scope": "Executes seq2seq SFT, model beam self-sampling, offline retrieval feedback, partial-order construction, and rank-aware PRO. T5-small and a MovieLens catalog replace Qwen-7B and private Taobao queries/search infrastructure.",
    }
