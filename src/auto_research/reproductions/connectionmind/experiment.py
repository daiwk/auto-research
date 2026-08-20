from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from .model import distill_student, load_delicious_graph, train_path_policy, typed_path_features


def _evaluate(data, scorer, target_split="test", k=10):
    targets = data.test if target_split == "test" else data.validation
    hits = ndcg = precision = 0.0
    surfaced_relations = np.zeros(4, dtype=np.float64)
    for user, (history, target) in enumerate(zip(data.train, targets)):
        context = (*history, data.validation[user]) if target_split == "test" else history
        scores, relation = scorer(user, context)
        scores = np.asarray(scores).copy(); scores[list(set(context))] = -np.inf
        top = np.argsort(-scores)[:k]
        positions = np.flatnonzero(top == target)
        hits += float(bool(positions.size)); precision += float(bool(positions.size)) / k
        ndcg += 0.0 if not positions.size else 1.0 / math.log2(int(positions[0]) + 2)
        surfaced_relations += np.bincount(relation[top], minlength=4)
    count = len(targets)
    return {
        "recall_at_10": hits / count, "precision_at_10": precision / count,
        "ndcg_at_10": ndcg / count,
        "surfaced_relation_distribution": (surfaced_relations / surfaced_relations.sum()).tolist(),
    }


def _relative(method, baseline):
    return {
        f"{metric}_percent": 100.0 * (method[metric] - baseline[metric]) / max(abs(baseline[metric]), 1e-12)
        for metric in ("recall_at_10", "precision_at_10", "ndcg_at_10")
    }


def reproduce_connectionmind(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_delicious_graph(dataset_dir)
    policy, training = train_path_policy(data, seed=seed)
    student_weights = distill_student(data, policy)

    def graph_baseline(user, history):
        features = typed_path_features(data, user, history)
        weights = np.asarray((0.40, 0.20, 0.25, 0.15))
        return features @ weights, np.argmax(features * weights[None], axis=1)

    activity = np.asarray([len(row) for row in data.train])
    heavy = set(np.argsort(-activity)[: max(1, math.ceil(0.10 * len(activity)))].tolist())

    def hybrid_raw(user, history):
        features = typed_path_features(data, user, history)
        if user in heavy:
            logits = policy.action_logits(features)
            return policy.item_scores(features), np.argmax(logits, axis=1)
        contributions = features * student_weights[None]
        return contributions.sum(1), np.argmax(contributions, axis=1)

    baseline = _evaluate(data, graph_baseline)
    best = None
    for alpha in np.linspace(0.1, 1.0, 10):
        def blended(user, history, alpha=alpha):
            base, _ = graph_baseline(user, history)
            path, relation = hybrid_raw(user, history)
            base = (base - base.min()) / max(float(np.ptp(base)), 1e-12)
            path = (path - path.min()) / max(float(np.ptp(path)), 1e-12)
            return (1.0 - alpha) * base + alpha * path, relation
        validation = _evaluate(data, blended, target_split="validation")
        objective = validation["ndcg_at_10"] + 0.25 * validation["recall_at_10"]
        if best is None or objective > best[0]:
            best = (objective, float(alpha), blended)
    alpha, hybrid = best[1], best[2]
    method = _evaluate(data, hybrid)
    return {
        "paper": {"arxiv_id": "2608.10187", "title": "ConnectionMind", "url": "https://arxiv.org/abs/2608.10187", "organization": "Michigan State University / Meta"},
        "dataset": {"name": "HetRec 2011 Delicious-2K", "users": len(data.train), "items": data.item_count, "social_edges": sum(map(len, data.friends)), "tag_dimensions": data.item_tags.shape[1]},
        "setup": {"seed": seed, "split": "chronological leave-two-out", "heavy_user_share": len(heavy) / len(data.train), "validation_selected_path_blend": alpha},
        "baseline": {"name": "fixed heterogeneous graph aggregation", **baseline},
        "method": {"name": "ConnectionMind SFT+GRPO hybrid", **method},
        "relative": _relative(method, baseline),
        "stages": {"typed_heterogeneous_graph": True, "shortest_path_sft": True, "rule_reward_grpo": True, "teacher_path_distillation": True, "hybrid_heavy_user_inference": True, **training},
        "paper_results": {
            "delicious_8b_recall_at_5": 0.0631, "delicious_8b_recall_at_20": 0.1374,
            "meta_offline_recall_at_10_percent": 88.0,
            "online_exposure_percent": 0.33, "online_watch_time_percent": 0.43,
            "online_video_sessions_percent": 0.22,
        },
        "scope": "使用论文同款公开 Delicious 数据真实构造 user-item-tag-social 异构图，实际执行最短正路径 SFT、格式/推荐/步数规则奖励的组相对策略更新、路径教师蒸馏与重用户混合推理；未复刻 Meta 私有视频日志、Llama-3 3B/8B 与生产服务。",
    }
