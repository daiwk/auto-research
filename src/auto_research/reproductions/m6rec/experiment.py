from __future__ import annotations

import os
from pathlib import Path

from .model import M6RecConfig, movielens_text_examples, train_and_evaluate


def reproduce_m6rec(dataset_dir: Path, seed: int = 42):
    config = M6RecConfig(
        model_name=os.environ.get("AUTO_RESEARCH_M6REC_MODEL", "prajjwal1/bert-tiny"),
        steps=int(os.environ.get("AUTO_RESEARCH_M6REC_STEPS", "100")),
        maximum_examples=int(os.environ.get("AUTO_RESEARCH_M6REC_EXAMPLES", "5000")),
    )
    train, test = movielens_text_examples(dataset_dir, config)
    option = train_and_evaluate(train, test, config, seed, use_adapters=False)
    adapter = train_and_evaluate(train, test, config, seed, use_adapters=True)
    return {
        "paper": {"arxiv_id": "2205.08084", "title": "M6-Rec: Generative Pretrained Language Models are Open-Ended Recommender Systems", "url": "https://arxiv.org/abs/2205.08084", "track": "recommendation"},
        "dataset": "MovieLens 100K with official title and genre text",
        "setup": {"seed": seed, "model": config.model_name, "train_examples": len(train), "test_examples": len(test), "steps": config.steps, "adapter_width": config.adapter_width},
        "results": {"option_tuning": option, "option_adapter_tuning": adapter},
        "auc_gain_percent": 100 * (adapter["auc"] - option["auc"]) / max(option["auc"], 1e-12),
        "paper_online_ab": {"product": "Alipay mini-app retrieval", "relative_ctr_percent": 1.0, "deployment": "fully deployed since July 2021"},
        "scope": "Executes M6-Rec's plain-text behavior/candidate formulation, frozen pretrained Transformer, option tuning, and per-layer bottleneck option-adapter tuning. BERT-tiny and MovieLens replace proprietary M6 and Alipay/Taobao logs; production early-exit and pruning are not benchmarked.",
    }
