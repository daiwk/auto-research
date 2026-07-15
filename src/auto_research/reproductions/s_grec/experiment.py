from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np

from .data import load_sgrec_data
from .model import GeneratorConfig, score_catalog, train_policy, train_sft
from .psj import train_psj


def reproduce_s_grec(dataset_dir: Path, seed: int = 42) -> dict:
    model_name = os.environ.get(
        "AUTO_RESEARCH_SGREC_JUDGE_MODEL", "HuggingFaceTB/SmolLM2-135M-Instruct"
    )
    train_rows = int(os.environ.get("AUTO_RESEARCH_SGREC_TRAIN_ROWS", "12000"))
    eval_users = int(os.environ.get("AUTO_RESEARCH_SGREC_EVAL_USERS", "96"))
    psj_sft_steps = int(os.environ.get("AUTO_RESEARCH_SGREC_PSJ_SFT_STEPS", "64"))
    aspect_grpo_steps = int(os.environ.get("AUTO_RESEARCH_SGREC_ASPECT_GRPO_STEPS", "24"))
    pair_grpo_steps = int(os.environ.get("AUTO_RESEARCH_SGREC_PAIR_GRPO_STEPS", "24"))
    sft_steps = int(os.environ.get("AUTO_RESEARCH_SGREC_GENERATOR_SFT_STEPS", "600"))
    policy_steps = int(os.environ.get("AUTO_RESEARCH_SGREC_POLICY_STEPS", "240"))
    data = load_sgrec_data(dataset_dir, train_rows, eval_users, seed)
    config = GeneratorConfig(
        semantic_sampling_ratio=float(
            os.environ.get("AUTO_RESEARCH_SGREC_SEMANTIC_RATIO", "0.05")
        )
    )
    judge, psj_training = train_psj(
        data,
        model_name,
        psj_sft_steps,
        aspect_grpo_steps,
        pair_grpo_steps,
        seed,
    )
    sft_model, sft_training = train_sft(data, sft_steps, config, seed + 1)
    modes = ("business", "reward_sum", "adv_sum", "a2po")
    models, policy_training = {}, {}
    for mode in modes:
        models[mode], policy_training[mode] = train_policy(
            sft_model, data, judge, policy_steps, mode, config, seed + 10
        )
    validation = {
        mode: evaluate(models[mode], data, data.validation, config) for mode in modes
    }
    selected = max(
        ("business", "a2po"),
        key=lambda mode: (
            validation[mode]["hr_at_10"],
            validation[mode]["ndcg_at_10"],
        ),
    )
    test = {mode: evaluate(models[mode], data, data.test, config) for mode in modes}
    return {
        "paper": {
            "arxiv_id": "2602.10606",
            "title": "S-GRec: Personalized Semantic-Aware Generative Recommendation with Asymmetric Advantage",
            "url": "https://arxiv.org/abs/2602.10606",
            "organization": "Tencent / WeChat Channels",
        },
        "dataset": {
            "name": "MiniOneRec Amazon Office_Products",
            "source": str(data.source),
            "train_rows": len(data.train),
            "aspect_samples": len(data.aspects),
            "pairwise_samples": len(data.pairs),
            "validation_users": len(data.validation),
            "test_users": len(data.test),
            "items": len(data.codes),
            "context_aspect": "dropped, matching the paper's Amazon setup",
        },
        "setup": {
            "judge_model": model_name,
            "seed": seed,
            "group_size": config.group_size,
            "semantic_sampling_ratio": config.semantic_sampling_ratio,
            "selection": "validation HR@10, then NDCG@10; business vs A2PO only",
            "selected_variant": selected,
        },
        "training": {
            "psj": psj_training,
            "generator_sft": sft_training,
            "policy": policy_training,
        },
        "validation": validation,
        "test": test,
        "paper_results": {
            "office_minionerec_hr_at_10": 0.1634,
            "office_minionerec_ndcg_at_10": 0.1242,
            "office_sgrec_hr_at_10": 0.1689,
            "office_sgrec_ndcg_at_10": 0.1308,
            "industrial_minionerec_hr_at_10": 0.1586,
            "industrial_sgrec_hr_at_10": 0.1632,
            "psj_sft_grpo_pair_auc": 0.8116,
            "psj_sft_grpo_point_accuracy": 0.8687,
            "online_gmv_percent": 1.19,
            "online_gmv_normal_percent": 1.55,
            "online_ctr_percent": 1.16,
            "online_dislike_percent": -2.02,
            "online_traffic_percent": 20.0,
        },
        "scope": (
            "Executes a real causal-LM LoRA judge, discrete profile/future/novelty aspect "
            "SFT and KL-regularized group-relative policy updates, user-conditional sampled "
            "importance levels with pairwise GRPO, SID autoregressive generator SFT, and four "
            "fairly initialized policy variants including the exact A2PO sign gate and magnitude "
            "bound. Public Office next-item feedback and Qwen embeddings replace proprietary "
            "DeepSeek-R1 plus human ad annotations and eCPM; PSJ is queried only during training."
        ),
    }


def evaluate(model, data, rows, config):
    hits = {3: 0.0, 5: 0.0, 10: 0.0}
    ndcg = {3: 0.0, 5: 0.0, 10: 0.0}
    novelty_hits = {level: [] for level in range(4)}
    for row in rows:
        scores = score_catalog(model, data, row, config)
        scores[list(set(row.history))] = -np.inf
        order = np.argsort(scores)[::-1][:10]
        positions = np.flatnonzero(order == row.target)
        rank = int(positions[0]) + 1 if len(positions) else None
        for k in hits:
            hit = float(rank is not None and rank <= k)
            hits[k] += hit
            if k == 5:
                novelty_hits[_novelty_level(row, data)].append(hit)
        for k in ndcg:
            if rank is not None and rank <= k:
                ndcg[k] += 1 / math.log2(rank + 1)
    count = len(rows)
    return {
        "users": count,
        **{f"hr_at_{k}": value / count for k, value in hits.items()},
        **{f"ndcg_at_{k}": value / count for k, value in ndcg.items()},
        "novelty_hr_at_5": {
            str(level): float(np.mean(values)) if values else None
            for level, values in novelty_hits.items()
        },
    }


def _novelty_level(row, data):
    if row.target in row.history:
        return 0
    target = data.codes[row.target]
    history = data.codes[list(row.history)]
    if np.any(np.all(history[:, :2] == target[:2], axis=1)):
        return 1
    if np.any(history[:, 0] == target[0]):
        return 2
    return 3
