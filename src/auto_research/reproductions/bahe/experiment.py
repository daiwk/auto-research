from __future__ import annotations

import os
from pathlib import Path

from ..llm_rec_data import load_text_ctr_data
from .model import (
    BAHEConfig, atomic_behavior_embeddings, build_bahe, build_full_text,
    evaluate, require_backend, train_model,
)


def reproduce_bahe(dataset_dir: Path, seed: int = 42):
    torch, _, _, _ = require_backend()
    config = BAHEConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_BAHE_STEPS", "100")),
        maximum_train=int(os.environ.get("AUTO_RESEARCH_BAHE_TRAIN", "5000")),
        maximum_test=int(os.environ.get("AUTO_RESEARCH_BAHE_TEST", "1000")),
    )
    data = load_text_ctr_data(dataset_dir)
    train, test = data.train[:config.maximum_train], data.test[:config.maximum_test]
    atomic = atomic_behavior_embeddings(data, dataset_dir, config)
    torch.manual_seed(seed)
    full, tokenizer = build_full_text(config)
    full_training = train_model(full, tokenizer, data, train, config, seed, False)
    full_result = evaluate(full, tokenizer, data, test, config, False)
    torch.manual_seed(seed)
    bahe = build_bahe(atomic, config)
    bahe_training = train_model(bahe, None, data, train, config, seed, True)
    bahe_result = evaluate(bahe, None, data, test, config, True)
    return {
        "paper": {"arxiv_id": "2403.19347", "title": "Breaking the Length Barrier: LLM-Enhanced CTR Prediction in Long Textual User Behaviors", "url": "https://arxiv.org/abs/2403.19347", "track": "recommendation"},
        "dataset": "MovieLens 100K title text",
        "setup": {"seed": seed, "model": config.model_name, "train_examples": len(train), "test_examples": len(test), "steps": config.steps, "history_items": config.history_items},
        "training": {"full_text": full_training, "bahe": bahe_training},
        "results": {"full_text_upper_tuning": full_result, "bahe_atomic_hierarchical": bahe_result},
        "paper_online_ab": {"duration": "two weeks", "ctr_percent": 9.65, "advertising_cpm_percent": 2.41},
        "scope": "Executes shallow frozen LLM encoding of reusable atomic behaviors, offline representation storage, trainable upper-layer hierarchical behavior aggregation, and CTR training. BERT-tiny and MovieLens replace the production LLM and ad logs.",
    }
