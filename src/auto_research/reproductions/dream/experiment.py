from __future__ import annotations

from pathlib import Path

import numpy as np

from ..industrial_2026 import base_scores, evaluate, gain, load_industrial_data
from .model import StrategyBundle, StrategyMemory, candidate_bundles, compile_strategy, infer_intent


def _objective(metrics: dict[str, float]) -> float:
    return metrics["ndcg_at_10"] + 0.25 * metrics["hit_at_10"] - 0.02 * metrics["head_share_at_10"]


def _replay_metrics(data, scorer, indices):
    hits = ndcg = 0.0; catalog = []
    for user in indices:
        history, target = data.sequences.train[user], data.sequences.validation[user]
        scores = np.asarray(scorer(history), dtype=np.float64).copy()
        scores[list(set(history))] = -np.inf
        top = np.argsort(-scores)[:10]; catalog.extend(top.tolist())
        positions = np.flatnonzero(top == target)
        hits += float(bool(positions.size))
        if positions.size:
            ndcg += 1.0 / np.log2(int(positions[0]) + 2)
    head = set(np.argsort(-data.popularity)[: max(1, data.item_count // 10)])
    return {
        "hit_at_10": hits / len(indices), "ndcg_at_10": ndcg / len(indices),
        "head_share_at_10": sum(item in head for item in catalog) / len(catalog),
    }


def reproduce_dream(dataset_dir: Path, seed: int = 42) -> dict:
    del seed  # The compiler and replay are deterministic by design.
    data = load_industrial_data(dataset_dir, maximum_users=260, maximum_items=420)
    baseline_scorer = lambda history: base_scores(data, history)
    baseline = evaluate(data, baseline_scorer)
    memory = StrategyMemory()
    center = StrategyBundle()
    replay_log = []
    offline_users = tuple(range(0, len(data.sequences.train), 2))
    online_shadow_users = tuple(range(1, len(data.sequences.train), 2))
    offline_control = _replay_metrics(data, baseline_scorer, offline_users)
    online_control = _replay_metrics(data, baseline_scorer, online_shadow_users)

    # Offline reward loop: three generations, validation only, frozen before test.
    for generation in range(3):
        trials = []
        for bundle in candidate_bundles(center):
            def scorer(history, bundle=bundle):
                intent = infer_intent(data, history)
                return compile_strategy(data, history, intent, bundle)[0]
            metrics = _replay_metrics(data, scorer, offline_users)
            trials.append((metrics, bundle))
            replay_log.append({"generation": generation, "bundle": bundle.__dict__, "objective": float(_objective(metrics))})
        best_metrics, best_bundle = max(trials, key=lambda row: _objective(row[0]))
        def shadow_scorer(history):
            intent = infer_intent(data, history)
            return compile_strategy(data, history, intent, best_bundle)[0]
        shadow_metrics = _replay_metrics(data, shadow_scorer, online_shadow_users)
        delta = _objective(shadow_metrics) - _objective(online_control)
        memory.deposit("global", best_bundle, delta)
        if delta > 0:
            center = best_bundle
        replay_log.append({"generation": generation, "online_shadow_outcome_delta": float(delta), "accepted": bool(delta > 0)})

    cloud_calls = schema_valid = 0
    def dream_scorer(history):
        nonlocal cloud_calls, schema_valid
        intent = infer_intent(data, history)
        bundle = memory.retrieve(intent.signature)
        scores, trace = compile_strategy(data, history, intent, bundle)
        cloud_calls += int(trace["cloud_triggered"]); schema_valid += int(trace["schema_valid"])
        return scores

    method = evaluate(data, dream_scorer)
    total_calls = len(data.sequences.test)
    selected = memory.retrieve("global")
    return {
        "paper": {"arxiv_id": "2608.09408", "title": "DREAM", "url": "https://arxiv.org/abs/2608.09408", "organization": "Taobao & Tmall Group / Alibaba"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.sequences.train), "items": data.item_count},
        "setup": {"seed": 42, "offline_generations": 3, "evaluated_strategy_bundles": len(replay_log), "offline_replay_users": len(offline_users), "online_shadow_users": len(online_shadow_users), "test_frozen_after_validation": True},
        "baseline": {"name": "retrieval/ranking backbone without DREAM overlay", **baseline},
        "method": {"name": "DREAM intent + meta strategy overlay", **method},
        "relative": gain(method, baseline),
        "stages": {
            "l0_l1_l2_intent_engine": True, "edge_cloud_traffic_funnel": True,
            "m1_intent_summary": True, "m2_strategy_memory_planning": True,
            "m3_schema_guarded_compiler": True, "offline_online_reward_dual_loop": True,
            "selected_strategy": selected.__dict__, "memory_positive_conclusions": memory.accepted,
            "memory_rejected_conclusions": memory.rejected,
            "cloud_trigger_share": cloud_calls / max(total_calls, 1),
            "schema_valid_rate": schema_valid / max(total_calls, 1),
            "replay_tail": replay_log[-3:],
        },
        "paper_results": {
            "intent_model_overall_baseline": 71.32, "intent_model_overall_dream": 84.74,
            "rerank_ipv_percent": 2.06, "fine_rank_rerank_ipv_percent": 2.71,
            "fine_rank_rerank_core_ipv_percent": 3.06, "fine_rank_rerank_gmv_percent": 1.31,
            "cognitive_recall_ipv_percent": 0.80, "strategy_adaptation_ipv_percent": 0.52,
        },
        "scope": "在公开 MovieLens-1M 上保留原排序 backbone，实际执行 L0/L1/L2 意图抽取、流量漏斗、策略记忆、三轮离线 replay、typed bundle 安全校验、有界乘法编译与类目打散，并在验证集冻结策略后评估测试集；未复刻淘宝私有多源信号、Qwen3 Meta Engine 和线上结论回流。",
    }
