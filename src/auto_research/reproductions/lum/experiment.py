from __future__ import annotations

import os
from pathlib import Path

from .model import LUMConfig, build_ranker, load_lum_data, pretrain_lum, query_knowledge, train_ranker


def reproduce_lum(dataset_dir: Path, seed: int = 42):
    config = LUMConfig(
        maximum_users=int(os.environ.get("AUTO_RESEARCH_LUM_USERS", "1000")),
        pretrain_steps=int(os.environ.get("AUTO_RESEARCH_LUM_PRETRAIN_STEPS", "200")),
        ranker_steps=int(os.environ.get("AUTO_RESEARCH_LUM_STEPS", "160")),
        maximum_train=int(os.environ.get("AUTO_RESEARCH_LUM_TRAIN", "6000")),
        maximum_test=int(os.environ.get("AUTO_RESEARCH_LUM_TEST", "1500")),
    )
    data = load_lum_data(dataset_dir, config.maximum_users)
    lum, pretraining = pretrain_lum(data, config, seed)
    train, test = data.train[: config.maximum_train], data.test[: config.maximum_test]
    knowledge, item_knowledge = query_knowledge(lum, (*train, *test), data, config)
    baseline = train_ranker(build_ranker(data, knowledge, item_knowledge, config, False), train, test, config, seed)
    method = train_ranker(build_ranker(data, knowledge, item_knowledge, config, True), train, test, config, seed)
    return {
        "paper": {"arxiv_id": "2502.08309", "title": "Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm based Large User Model", "url": "https://arxiv.org/abs/2502.08309", "track": "recommendation"},
        "dataset": "MovieLens-1M ratings, genres, and chronological user behavior",
        "setup": {"seed": seed, "users": data.users, "items": data.items, "conditions": data.conditions, "pretrain_examples": len(data.pretrain), "train": len(train), "test": len(test), "pretrain_steps": config.pretrain_steps, "ranker_steps": config.ranker_steps, "group_queries": data.conditions},
        "pretraining": pretraining,
        "results": {"dlrm": baseline, "lum_augmented_dlrm": method},
        "paper_online_ab": {"ctr_percent": 2.9, "rpm_percent": 1.2, "product": "Taobao sponsored search"},
        "scope": "Executes heterogeneous condition/item token encoding, causal next-condition-item InfoNCE pre-training, masked group querying, offline knowledge caching, direct feature incorporation, target-interest similarity, and downstream discriminative CTR training. MovieLens rating conditions replace proprietary Taobao scenario/query conditions.",
    }
