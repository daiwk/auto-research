from __future__ import annotations

import os
from pathlib import Path

from ..llm_rec_data import load_text_ctr_data
from .model import KARConfig, build_knowledge, build_ranker, require_backend, train_and_evaluate


def reproduce_kar(dataset_dir: Path, seed: int = 42):
    torch, _, _, _ = require_backend()
    config = KARConfig(
        maximum_users=int(os.environ.get("AUTO_RESEARCH_KAR_USERS", "80")),
        steps=int(os.environ.get("AUTO_RESEARCH_KAR_STEPS", "120")),
        maximum_train=int(os.environ.get("AUTO_RESEARCH_KAR_TRAIN", "5000")),
        maximum_test=int(os.environ.get("AUTO_RESEARCH_KAR_TEST", "1000")),
    )
    data = load_text_ctr_data(dataset_dir, maximum_users=config.maximum_users)
    train, test = data.train[:config.maximum_train], data.test[:config.maximum_test]
    user_knowledge, item_knowledge, knowledge_metrics = build_knowledge(data, dataset_dir, config)
    torch.manual_seed(seed)
    baseline = train_and_evaluate(build_ranker(data, user_knowledge, item_knowledge, config, False), train, test, config, seed)
    torch.manual_seed(seed)
    method = train_and_evaluate(build_ranker(data, user_knowledge, item_knowledge, config, True), train, test, config, seed)
    return {
        "paper": {"arxiv_id": "2306.10933", "title": "Towards Open-World Recommendation with Knowledge Augmentation from Large Language Models", "url": "https://arxiv.org/abs/2306.10933", "track": "recommendation"},
        "dataset": "MovieLens 100K title/genre text",
        "setup": {"seed": seed, "llm": config.model_name, "users": data.users, "train_examples": len(train), "test_examples": len(test), "steps": config.steps, **knowledge_metrics},
        "results": {"id_ranker": baseline, "kar_hybrid_expert": method},
        "paper_online_ab": {"news_recall_percent": 7.0, "music_traffic": "10% treatment / 10% control, 7 days", "song_play_count_percent": 1.7, "play_duration_percent": 1.57},
        "scope": "Executes LLM factorization prompts, generated user-preference and item-factual knowledge, offline knowledge storage, hybrid-expert adaptation, and downstream CTR training. SmolLM2-135M-Instruct and MovieLens replace PanGu and proprietary Huawei logs.",
    }
