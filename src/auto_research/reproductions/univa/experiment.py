from __future__ import annotations

import math
import os
import time
from pathlib import Path

import numpy as np

from ..rec_utils import summarize_runs
from .data import load_univa_data, path_bid_dispersion
from .model import UniVAConfig, beam_search, score_items, train_model


def reproduce_univa(dataset_dir: Path, seed: int = 42) -> dict:
    steps = int(os.environ.get("AUTO_RESEARCH_UNIVA_STEPS", "80"))
    train_rows = int(os.environ.get("AUTO_RESEARCH_UNIVA_TRAIN_ROWS", "12000"))
    evaluation_users = int(os.environ.get("AUTO_RESEARCH_UNIVA_EVAL_USERS", "32"))
    seeds = tuple(
        seed + offset
        for offset in range(int(os.environ.get("AUTO_RESEARCH_UNIVA_SEEDS", "3")))
    )
    data = load_univa_data(dataset_dir, train_rows, evaluation_users, 64, seed)
    config = UniVAConfig(steps=steps)
    run_results = {"semantic_sid_sl": [], "commercial_sid_sl": [], "univa_full": []}
    run_test_results = {name: [] for name in run_results}
    training = {name: [] for name in run_results}
    serving = []
    for run_seed in seeds:
        semantic, metrics = train_model(
            data.semantic_codes, data.ecpm, data.item_count, data.train, config, run_seed, False
        )
        training["semantic_sid_sl"].append(metrics)
        run_results["semantic_sid_sl"].append(
            evaluate(semantic, data.validation, data.semantic_codes, data, False, config)
        )
        run_test_results["semantic_sid_sl"].append(
            evaluate(semantic, data.test, data.semantic_codes, data, False, config)
        )
        commercial, metrics = train_model(
            data.commercial_codes, data.ecpm, data.item_count, data.train, config, run_seed, False
        )
        training["commercial_sid_sl"].append(metrics)
        run_results["commercial_sid_sl"].append(
            evaluate(commercial, data.validation, data.commercial_codes, data, False, config)
        )
        run_test_results["commercial_sid_sl"].append(
            evaluate(commercial, data.test, data.commercial_codes, data, False, config)
        )
        full, metrics = train_model(
            data.commercial_codes, data.ecpm, data.item_count, data.train, config, run_seed, True
        )
        training["univa_full"].append(metrics)
        run_results["univa_full"].append(
            evaluate(full, data.validation, data.commercial_codes, data, True, config)
        )
        run_test_results["univa_full"].append(
            evaluate(full, data.test, data.commercial_codes, data, True, config)
        )
        serving.append(evaluate_serving(full, data, config))
    validation = {name: summarize_runs(values) for name, values in run_results.items()}
    selected = max(
        validation,
        key=lambda name: (
            validation[name]["value_hr_at_100"],
            validation[name]["hr_at_100"],
        ),
    )
    test = summarize_runs(run_test_results[selected])
    baseline_test = summarize_runs(run_test_results["semantic_sid_sl"])
    # The commercial token refines the first two semantic levels. Compare the
    # bid dispersion before and after that refinement instead of grouping by
    # the already-nearly-unique three-level semantic identifier.
    semantic_dispersion = path_bid_dispersion(data.semantic_codes[:, :2], data.bids)
    commercial_dispersion = path_bid_dispersion(data.commercial_codes, data.bids)
    return {
        "paper": {
            "arxiv_id": "2605.05803",
            "title": "Unified Value Alignment for Generative Recommendation in Industrial Advertising",
            "url": "https://arxiv.org/abs/2605.05803",
            "organization": "Tencent / WeChat Channels",
        },
        "dataset": {
            "name": "MiniOneRec Amazon Office_Products",
            "source": str(data.source),
            "train_rows": len(data.train),
            "validation_users": len(data.validation),
            "test_users": len(data.test),
            "items": data.item_count,
        },
        "setup": {
            "seeds": list(seeds),
            "steps_per_model": steps,
            "commercial_vocabulary_budget": 64,
            "semantic_code_sizes": [256, 256, 256],
            "scaled_decoder": {
                "dimensions": config.dimensions,
                "experts": config.experts,
                "top_experts": config.top_experts,
                "recursive_rounds": config.recursive_rounds,
            },
            "selection": "validation ValueHR@100, then HR@100",
        },
        "commercial_sid": {
            **data.commercial_stats,
            "semantic_path_bid_dispersion": semantic_dispersion,
            "commercial_path_bid_dispersion": commercial_dispersion,
        },
        "training": training,
        "validation": validation,
        "selected_variant": selected,
        "test_by_variant": {
            name: summarize_runs(values) for name, values in run_test_results.items()
        },
        "test": test,
        "semantic_sid_test_baseline": baseline_test,
        "serving": summarize_runs(serving),
        "paper_results": {
            "offline_hr_at_100_relative_percent": 37.04,
            "offline_value_hr_at_100_relative_percent": 37.01,
            "offline_wndcg_at_100_relative_percent": 26.20,
            "online_v1_gmv_percent": 1.03,
            "online_v2_gmv_percent": 1.50,
            "online_v2_gmv_normal_percent": 1.42,
            "online_traffic_percent": 5.0,
            "online_dates": "2026-03-07 to 2026-03-11",
        },
        "scope": (
            "Runs semantic-vs-commercial SID construction, equi-frequency classify-then-bin, "
            "HSTU encoding, cross/self-attentive MoR+Sparse-MoE decoding, dual generation/value "
            "heads, alternating supervised and clipped PPO/value updates, full-catalog value metrics, "
            "and request-valid trie beam search. Amazon brand/popularity/embedding-derived attributes "
            "and a deterministic interaction-value simulator replace Tencent's private optimization "
            "goal, ROI, industry, bid, pCTR/pCVR snapshots, inventory, and live traffic."
        ),
    }


def evaluate(model, rows, codes, data, fused, config):
    hits = {10: 0.0, 50: 0.0, 100: 0.0}
    value_hits = {10: 0.0, 50: 0.0, 100: 0.0}
    weighted_ndcg = {10: 0.0, 50: 0.0, 100: 0.0}
    total_value = sum(float(data.ecpm[target]) for _, target in rows)
    total_weight = sum(math.log10(1 + float(data.ecpm[target])) for _, target in rows)
    started = time.perf_counter()
    for history, target in rows:
        scores = score_items(model, history, codes, fused, config)
        scores[list(set(history))] = -np.inf
        order = np.argsort(scores)[::-1][:100]
        positions = np.flatnonzero(order == target)
        rank = int(positions[0]) + 1 if len(positions) else None
        value = float(data.ecpm[target])
        weight = math.log10(1 + value)
        for k in hits:
            if rank is not None and rank <= k:
                hits[k] += 1
                value_hits[k] += value
                weighted_ndcg[k] += weight / math.log2(rank + 1)
    count = len(rows)
    result = {"users": count, "seconds": time.perf_counter() - started}
    for k in hits:
        result[f"hr_at_{k}"] = hits[k] / count
        result[f"value_hr_at_{k}"] = value_hits[k] / max(total_value, 1e-12)
        result[f"wndcg_at_{k}"] = weighted_ndcg[k] / max(total_weight, 1e-12)
    return result


def evaluate_serving(model, data, config):
    rows = data.validation[: min(8, len(data.validation))]
    unconstrained_valid = constrained_valid = 0
    semantic_value = fused_value = 0.0
    started = time.perf_counter()
    for history, _ in rows:
        unconstrained = beam_search(
            model, history, data.commercial_codes, 50, True, False, config
        )
        constrained = beam_search(
            model, history, data.commercial_codes, 50, True, True, config
        )
        semantic = beam_search(
            model, history, data.commercial_codes, 50, False, True, config
        )
        unconstrained_valid += unconstrained["valid_paths"]
        constrained_valid += constrained["valid_paths"]
        if semantic["items"]:
            semantic_value += float(np.mean(data.ecpm[semantic["items"]]))
        if constrained["items"]:
            fused_value += float(np.mean(data.ecpm[constrained["items"]]))
    count = len(rows)
    return {
        "requests": count,
        "unconstrained_valid_paths": unconstrained_valid / count,
        "personalized_trie_valid_paths": constrained_valid / count,
        "semantic_beam_mean_value": semantic_value / count,
        "value_guided_beam_mean_value": fused_value / count,
        "seconds": time.perf_counter() - started,
    }
