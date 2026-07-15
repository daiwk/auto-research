from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np

from .data import load_sigma_data
from .model import (
    build_sigma,
    materialize_semantics,
    score_catalog,
    train_grounder,
    train_sigma,
)


def reproduce_sigma(dataset_dir: Path, seed: int = 42) -> dict:
    model_name = os.environ.get(
        "AUTO_RESEARCH_SIGMA_MODEL", "HuggingFaceTB/SmolLM2-135M-Instruct"
    )
    grounding_steps = int(os.environ.get("AUTO_RESEARCH_SIGMA_GROUNDING_STEPS", "40"))
    sft_steps = int(os.environ.get("AUTO_RESEARCH_SIGMA_SFT_STEPS", "480"))
    train_rows = int(os.environ.get("AUTO_RESEARCH_SIGMA_TRAIN_ROWS", "12000"))
    eval_users = int(os.environ.get("AUTO_RESEARCH_SIGMA_EVAL_USERS", "128"))
    data = load_sigma_data(dataset_dir, train_rows, eval_users, seed)
    grounder, grounding = train_grounder(data, model_name, grounding_steps, seed)
    semantics = materialize_semantics(grounder, data)
    model = build_sigma(grounder, data, semantics)
    sft = train_sigma(model, data, sft_steps, seed + 1)
    modes = ("id_only", "top1_prefix", "apf")
    validation = {mode: evaluate(model, data, data.validation, mode) for mode in modes}
    selected = max(
        modes,
        key=lambda mode: (validation[mode]["hr_at_20"], validation[mode]["ndcg_at_10"]),
    )
    test = {mode: evaluate(model, data, data.test, mode) for mode in modes}
    return {
        "paper": {
            "arxiv_id": "2602.22913",
            "title": "SIGMA: A Semantic-Grounded Instruction-Driven Generative Multi-Task Recommender at AliExpress",
            "url": "https://arxiv.org/abs/2602.22913",
            "organization": "Alibaba / AliExpress",
        },
        "dataset": {
            "name": "MiniOneRec Amazon Office_Products",
            "source": str(data.source),
            "train_rows": len(data.train),
            "validation_users": len(data.validation),
            "test_users": len(data.test),
            "items": len(data.codes),
            "grounding_pairs": len(data.grounding_pairs),
        },
        "setup": {
            "model": model_name,
            "seed": seed,
            "tasks": list(sorted(set(row.task for row in data.train))),
            "selection": "validation HR@20, then NDCG@10",
            "selected_variant": selected,
        },
        "training": {"multi_view_grounding": grounding, "multi_task_sft": sft},
        "validation": validation,
        "test": test,
        "paper_results": {
            "sigma_hr_at_1_percent": 9.61,
            "sigma_hr_at_20_percent": 43.05,
            "without_grounding_hr_at_20_percent": 33.24,
            "without_apf_hr_at_20_percent": 37.73,
            "online_order_percent": 2.80,
            "online_cvr_percent": 3.84,
            "online_gmv_percent": 7.84,
            "online_category_breadth_percent": 2.47,
            "online_traffic_percent": 5.0,
            "online_duration": "2 weeks",
        },
        "scope": (
            "Executes real causal-LM LoRA multi-view grounding with InfoNCE and collaborative "
            "similarity KL distillation, published RQ-based Office SID prefixes, fused semantic/"
            "visual/ID item vectors, all seven instruction task types, prefix NTP plus same-prefix "
            "hard-negative InfoNCE, three-step prefix-to-item generation, and APF. Public Office "
            "brand, embedding, and deterministic task attributes replace AliExpress queries, "
            "images, holidays, online ranking embeddings, 280M samples, and nearline U2I serving."
        ),
    }


def evaluate(model, data, rows, mode):
    hits = {1: 0.0, 5: 0.0, 10: 0.0, 20: 0.0}
    ndcg = {10: 0.0, 20: 0.0}
    task_hits = {task: [] for task in sorted(set(row.task for row in rows))}
    for row in rows:
        scores = score_catalog(model, data, row, mode)
        scores[list(set(row.history))] = -np.inf
        order = np.argsort(scores)[::-1][:20]
        positions = np.flatnonzero(order == row.target)
        rank = int(positions[0]) + 1 if len(positions) else None
        for k in hits:
            hits[k] += float(rank is not None and rank <= k)
        for k in ndcg:
            if rank is not None and rank <= k:
                ndcg[k] += 1 / math.log2(rank + 1)
        task_hits[row.task].append(float(rank is not None and rank <= 20))
    count = len(rows)
    return {
        "users": count,
        **{f"hr_at_{k}": value / count for k, value in hits.items()},
        **{f"ndcg_at_{k}": value / count for k, value in ndcg.items()},
        "task_hr_at_20": {
            task: float(np.mean(values)) if values else 0.0
            for task, values in task_hits.items()
        },
    }
