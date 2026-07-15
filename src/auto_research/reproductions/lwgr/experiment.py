from __future__ import annotations

import gc
import math
import os
from pathlib import Path

import numpy as np

from ..rec_utils import summarize_runs
from .data import load_lwgr_data
from .model import (
    LWGRConfig,
    load_knowledge_llm,
    score_catalog,
    train_policy,
    train_reference,
)


def reproduce_lwgr(dataset_dir: Path, seed: int = 42) -> dict:
    model_name = os.environ.get(
        "AUTO_RESEARCH_LWGR_MODEL", "HuggingFaceTB/SmolLM2-135M"
    )
    reference_steps = int(os.environ.get("AUTO_RESEARCH_LWGR_REFERENCE_STEPS", "180"))
    policy_steps = int(os.environ.get("AUTO_RESEARCH_LWGR_POLICY_STEPS", "100"))
    train_rows = int(os.environ.get("AUTO_RESEARCH_LWGR_TRAIN_ROWS", "12000"))
    eval_users = int(os.environ.get("AUTO_RESEARCH_LWGR_EVAL_USERS", "48"))
    seed_count = int(os.environ.get("AUTO_RESEARCH_LWGR_SEEDS", "3"))
    seeds = tuple(seed + index for index in range(seed_count))
    data = load_lwgr_data(dataset_dir, train_rows, eval_users, seed)
    config = LWGRConfig()
    llm, title_embeddings, device = load_knowledge_llm(model_name, data.titles, config)
    validation = {name: [] for name in ("reference", "unconstrained", "lwgr")}
    test = {name: [] for name in validation}
    training = {name: [] for name in validation}
    for run_seed in seeds:
        reference, metrics = train_reference(
            data.codes, len(data.codes), data.train, config, reference_steps, run_seed, device
        )
        training["reference"].append(metrics)
        validation["reference"].append(evaluate(reference, data.validation, data.codes, config, True))
        test["reference"].append(evaluate(reference, data.test, data.codes, config, True))
        unconstrained, metrics = train_policy(
            reference, llm, title_embeddings, data.codes, data.train, config,
            policy_steps, run_seed, False,
        )
        training["unconstrained"].append(metrics)
        validation["unconstrained"].append(evaluate(unconstrained, data.validation, data.codes, config, False))
        test["unconstrained"].append(evaluate(unconstrained, data.test, data.codes, config, False))
        del unconstrained
        gc.collect()
        lwgr, metrics = train_policy(
            reference, llm, title_embeddings, data.codes, data.train, config,
            policy_steps, run_seed, True,
        )
        training["lwgr"].append(metrics)
        validation["lwgr"].append(evaluate(lwgr, data.validation, data.codes, config, False))
        test["lwgr"].append(evaluate(lwgr, data.test, data.codes, config, False))
        del lwgr, reference
        gc.collect()
    validation_summary = {name: summarize_runs(values) for name, values in validation.items()}
    selected = max(
        validation_summary,
        key=lambda name: (validation_summary[name]["ndcg_at_10"], validation_summary[name]["recall_at_10"]),
    )
    return {
        "paper": {
            "arxiv_id": "2605.18771",
            "title": "LWGR: Lagrangian-Constrained Personalized World Knowledge for Generative Recommendation",
            "url": "https://arxiv.org/abs/2605.18771",
            "organization": "Alibaba International / CAS",
        },
        "dataset": {
            "name": "MiniOneRec Amazon Office_Products",
            "source": str(data.source),
            "train_rows": len(data.train),
            "validation_users": len(data.validation),
            "test_users": len(data.test),
            "items": len(data.codes),
        },
        "setup": {
            "model": model_name,
            "seeds": list(seeds),
            "parallel_codebooks": config.parallel_codebooks,
            "codewords_per_codebook": config.codewords,
            "selection": "validation NDCG@10, then Recall@10",
            "selected_variant": selected,
        },
        "training": training,
        "validation": validation_summary,
        "test": {name: summarize_runs(values) for name, values in test.items()},
        "paper_results": {
            "beauty_recall_at_10": 0.1026,
            "beauty_ndcg_at_10": 0.0701,
            "maximum_offline_relative_percent": 11.23,
            "online_revenue_percent": 1.35,
            "online_gmv_percent": 0.83,
            "online_ctr_percent": 1.17,
            "online_latency_ms": [13.35, 13.55],
        },
        "scope": (
            "Executes IBQ straight-through parallel codebooks, user-conditioned soft tokens "
            "through a real frozen open-source causal LM, BOS cross-attention knowledge fusion, "
            "a frozen generative reference policy, and alternating Lagrangian primal-dual updates "
            "against a confidence-degradation constraint. SmolLM2-135M and public Office titles/SIDs "
            "replace Qwen3-4B, Beauty/Toys full-scale runs, industrial logs, and nearline production storage."
        ),
    }


def evaluate(model, rows, codes, config, reference):
    recalls = {5: 0.0, 10: 0.0}
    ndcgs = {5: 0.0, 10: 0.0}
    for history, target in rows:
        scores = score_catalog(model, history, codes, config, reference)
        scores[list(set(history))] = -np.inf
        order = np.argsort(scores)[::-1][:10]
        position = np.flatnonzero(order == target)
        rank = int(position[0]) + 1 if len(position) else None
        for k in recalls:
            if rank is not None and rank <= k:
                recalls[k] += 1
                ndcgs[k] += 1 / math.log2(rank + 1)
    count = len(rows)
    return {
        "users": count,
        "recall_at_5": recalls[5] / count,
        "ndcg_at_5": ndcgs[5] / count,
        "recall_at_10": recalls[10] / count,
        "ndcg_at_10": ndcgs[10] / count,
    }
