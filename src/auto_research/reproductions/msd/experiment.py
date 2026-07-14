from __future__ import annotations

import os
from pathlib import Path

from ..llm_rec_data import load_text_ctr_data
from .model import MSDConfig, build_rankers, distill_student, train_and_evaluate


def reproduce_msd(dataset_dir: Path, seed: int = 42):
    config = MSDConfig(
        maximum_users=int(os.environ.get("AUTO_RESEARCH_MSD_USERS", "30")),
        teacher_items=int(os.environ.get("AUTO_RESEARCH_MSD_TEACHER_ITEMS", "160")),
        distill_steps=int(os.environ.get("AUTO_RESEARCH_MSD_DISTILL_STEPS", "32")),
        ranker_steps=int(os.environ.get("AUTO_RESEARCH_MSD_STEPS", "100")),
    )
    data = load_text_ctr_data(dataset_dir, maximum_users=config.maximum_users)
    student, tokenizer, user_prompts, item_prompts, frequency, distillation = distill_student(data, dataset_dir, config, seed)
    baseline, method = build_rankers(data, student, tokenizer, user_prompts, item_prompts, frequency, config, seed)
    baseline_result = train_and_evaluate(baseline, data.train, data.test, config, seed)
    method_result = train_and_evaluate(method, data.train, data.test, config, seed)
    return {
        "paper": {"arxiv_id": "2412.06860", "title": "Balancing Efficiency and Effectiveness: An LLM-Infused Approach for Optimized CTR Prediction", "url": "https://arxiv.org/abs/2412.06860", "track": "recommendation"},
        "dataset": "MovieLens-100K title/genre CTR",
        "setup": {"seed": seed, "users": data.users, "items": len(data.titles), "train": min(len(data.train), config.maximum_train), "test": min(len(data.test), config.maximum_test), "teacher_items": config.teacher_items, "distill_steps": config.distill_steps, "ranker_steps": config.ranker_steps, **distillation},
        "results": {"id_ctr": baseline_result, "msd": method_result},
        "paper_online_ab": {"ctr_percent": 2.12, "cpm_percent": 2.59, "traffic": "Meituan sponsored search, 2024-10-20 to 2024-10-30"},
        "scope": "Executes teacher knowledge generation, autoregressive T5 student distillation, q/v LoRA CTR alignment, user/item/history adapters, frequency-adaptive cached/online embeddings and top-k relevant-history fusion. MovieLens replaces proprietary Meituan ad logs.",
    }
