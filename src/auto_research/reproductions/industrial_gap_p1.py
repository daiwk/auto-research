"""Mechanism-level implementations for the recommendation P1 gap queue."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .industrial_2026 import (
    base_scores,
    evaluate,
    load_industrial_data,
    ridge,
    softmax,
    summary_result,
    tune_blend,
)


def _finish(key, title, data, method, stages, paper_results, baseline_name="shared transition + content baseline"):
    baseline = lambda history: base_scores(data, history)
    alpha, blended, validation = tune_blend(data, baseline, method)
    return summary_result(
        key=key,
        paper={"title": title},
        data=data,
        baseline_name=baseline_name,
        method_name=title.split(":", 1)[0],
        baseline=evaluate(data, baseline),
        proposed=evaluate(data, blended),
        stages={**stages, "validation_selected_alpha": alpha, "validation": validation},
        paper_results=paper_results,
        scope=(
            "在 MovieLens-100K 全库排序上执行论文的候选相关检索、层级压缩或蒸馏目标；"
            "未使用公司私有日志与线上 serving，线上 A/B 只引用原文。"
        ),
    )


def reproduce_twin_v2(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)
    rng = np.random.default_rng(seed)
    features = data.sequences.features
    # Offline divide-and-conquer compression: balanced hierarchical clusters.
    projection = features @ rng.normal(size=(features.shape[1], 6))
    coarse = np.argmax(projection[:, :3], axis=1)
    fine = np.argmax(projection[:, 3:], axis=1)
    cluster = coarse * 3 + fine
    centroids = np.stack([
        features[cluster == index].mean(0) if np.any(cluster == index) else features.mean(0)
        for index in range(9)
    ])
    cluster_size = np.bincount(cluster, minlength=9).astype(float)

    def method(history):
        target = features[history[-1]]
        # GSU retrieves target-relevant compressed interests; ESU expands only
        # those clusters and applies exact target attention to raw behaviours.
        cluster_score = centroids @ target / np.sqrt(cluster_size + 1.0)
        selected = np.argsort(-cluster_score)[:3]
        relevant = [item for item in history if cluster[item] in selected]
        relevant = relevant[-32:] or list(history[-8:])
        attention = softmax(features[relevant] @ target)
        interest = attention @ features[relevant]
        diversity = 1.0 - np.max(centroids @ features.T, axis=0)
        return features @ interest + 0.20 * diversity

    return _finish(
        "twin-v2", "TWIN-V2: Life-cycle User Behavior Compression", data, method,
        {"offline_hierarchical_clusters": 9, "cluster_size_reweighting": True,
         "candidate_aware_gsu": True, "exact_search_unit": True,
         "maximum_paper_history": 1_000_000},
        {"featured_watch_time_percent": 0.672, "discovery_watch_time_percent": 0.800,
         "slide_watch_time_percent": 0.728, "main_traffic_dau_million": 400},
    )


def reproduce_sim(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)
    features = data.sequences.features

    def method(history):
        target = features[history[-1]]
        history_items = np.asarray(history[:-1] or history)
        # Soft-search GSU is used because public MovieLens has no Alibaba item
        # category service. It still executes candidate-conditioned retrieval.
        gsu_score = features[history_items] @ target
        selected = history_items[np.argsort(-gsu_score)[: min(24, len(history_items))]]
        exact = softmax((features[selected] @ target) / 0.2)
        interest = exact @ features[selected]
        return features @ interest + 0.25 * data.transition[history[-1]]

    return _finish(
        "sim", "SIM: Search-based Interest Model", data, method,
        {"candidate_conditioned_gsu": True, "retrieved_behaviours": 24,
         "exact_search_attention": True, "paper_maximum_history": 54_000},
        {"ctr_percent": 7.1, "rpm_percent": 4.4, "deployment": "main traffic"},
    )


def reproduce_crsd(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)
    features = data.sequences.features
    teacher_targets, standard_rows, reasoning_rows = [], [], []
    for sequence in data.sequences.train:
        if len(sequence) < 3:
            continue
        history, target = sequence[:-1], sequence[-1]
        standard = features[history[-1]]
        reasoning = features[list(history[-min(8, len(history)) :])].mean(0)
        teacher = 0.65 * reasoning + 0.35 * features[target]
        standard_rows.append(standard)
        reasoning_rows.append(reasoning)
        teacher_targets.append(teacher)
    standard = np.asarray(standard_rows)
    reasoning = np.asarray(reasoning_rows)
    teacher = np.asarray(teacher_targets)
    # Stage 1 teacher supplies labels/reasoning; stage 2 uses the same student
    # with standard and reasoning-augmented inputs, plus a contrastive alignment.
    student_standard = ridge(standard, teacher)
    student_reasoning = ridge(reasoning, teacher)
    shared = 0.5 * (student_standard + student_reasoning)
    alignment = float(np.mean(np.sum((standard @ shared) * (reasoning @ shared), axis=1)))

    def method(history):
        standard_view = features[history[-1]]
        reasoning_view = features[list(history[-min(8, len(history)) :])].mean(0)
        distilled = 0.5 * (standard_view @ shared + reasoning_view @ shared)
        return features @ distilled

    return _finish(
        "crsd", "CRSD: Contrastive Reasoning Self-Distillation", data, method,
        {"domain_teacher_cpt_sft_preference_stages": 3,
         "teacher_reasoning_annotation": True, "shared_student_two_views": True,
         "contrastive_alignment": alignment, "reasoning_free_serving": True},
        {"adctr_percent": 0.91, "adcvr_percent": 1.06, "gtv_percent": 0.40,
         "bad_case_reduction_points": 30.5, "traffic_percent": 30.0},
    )
