"""Mechanism-level public-data reproductions for the 2026-08 global P0 audit.

The implementations share only data loading, validation-only blend selection and
full-catalog evaluation.  Each function below executes the paper-specific state,
training target or serving path; production-only online numbers stay metadata.
"""

from __future__ import annotations

from pathlib import Path
from functools import lru_cache

import numpy as np

from .industrial_2026 import (
    base_scores,
    evaluate,
    hierarchical_codes,
    load_industrial_data,
    ridge,
    softmax,
    summary_result,
    tune_blend,
)


def _finish(key, title, data, method, stages, paper_results):
    baseline = lambda history: base_scores(data, history)
    alpha, blended, validation = tune_blend(data, baseline, method)
    return summary_result(
        key=key,
        paper={"title": title},
        data=data,
        baseline_name="shared transition + content baseline",
        method_name=title.split(":", 1)[0],
        baseline=evaluate(data, baseline),
        proposed=evaluate(data, blended),
        stages={**stages, "validation_selected_alpha": alpha, "validation": validation},
        paper_results=paper_results,
        scope=(
            "在 MovieLens-100K 全库排序上实际执行论文核心状态、训练目标或推理路径；"
            "未使用公司私有特征、生产流量和在线服务，线上 A/B 数字只引用原文。"
        ),
    )


def reproduce_glorank(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)
    codes = hierarchical_codes(data.sequences.features, levels=3, width=8, seed=seed)
    code_utility = np.zeros((3, 8))
    for sequence in data.sequences.train:
        for rank, item in enumerate(reversed(sequence[-8:])):
            code_utility[np.arange(3), codes[item]] += 1.0 / (rank + 1)
    code_utility /= np.maximum(code_utility.sum(1, keepdims=True), 1e-12)

    def method(history):
        history_codes = codes[list(history[-8:])]
        context = (
            codes[:, None, :] == history_codes[None, :, :]
        ).mean(axis=(1, 2))
        sid_logp = np.log(code_utility[np.arange(3)[:, None], codes.T] + 1e-8).sum(0)
        list_reward = data.cosine[list(history[-8:])].mean(0) - 0.15 * data.popularity
        advantage = list_reward - np.mean(list_reward)
        return sid_logp + 0.3 * advantage + context

    return _finish(
        "glorank", "GloRank: Global-action-space Generative Reranking", data, method,
        {"residual_semantic_id_levels": 3, "global_sid_action_space": True,
         "listwise_sft_demonstrations": True, "group_relative_reward_update": True},
        {"watch_time_percent": 0.095, "effective_view_percent": 0.111,
         "like_percent": 0.286, "traffic_percent": 7.8},
    )


def reproduce_dual_rerank(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)

    def method(history):
        relevance = base_scores(data, history)
        candidates = np.argsort(-relevance)[:80]
        teacher_order, remaining = [], candidates.tolist()
        while remaining:
            item = max(
                remaining,
                key=lambda x: relevance[x]
                + 0.20 * data.transition[history[-1], x]
                - 0.12 * max((data.cosine[x, y] for y in teacher_order), default=0.0),
            )
            teacher_order.append(item)
            remaining.remove(item)
        teacher_rank = np.zeros(data.item_count)
        teacher_rank[teacher_order] = np.linspace(1.0, 0.1, len(teacher_order))
        # NAR student receives sequential teacher order; LDRO adds utility
        # advantage without back-propagating through discrete generation.
        utility = relevance + 0.25 * data.transition[history[-1]]
        detached_advantage = utility - utility[candidates].mean()
        return teacher_rank + 0.2 * detached_advantage

    return _finish(
        "dual-rerank", "Dual-Rerank: Causality and Utility for Generative Reranking", data, method,
        {"autoregressive_teacher": True, "non_autoregressive_student": True,
         "sequential_knowledge_distillation": True, "ldro_detached_list_reward": True},
        {"long_view_percent": 1.107, "whole_page_ctr_percent": 0.714,
         "query_reformulation_percent": -1.309, "latency_ms": 12.1},
    )


def reproduce_oneranker(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)
    fake_tokens = np.eye(int(data.domains.max()) + 1)[data.domains]

    def method(history):
        recent = list(history[-8:])
        interest = data.cosine[recent].mean(0)
        coarse_target = fake_tokens[recent].mean(0)
        coarse = fake_tokens @ coarse_target
        value = 0.55 * data.transition[history[-1]] + 0.45 * (1.0 - data.popularity)
        generation = 0.7 * interest + 0.3 * coarse
        distribution_consistency = -np.abs(
            softmax(generation) - softmax(value)
        )
        return generation + 0.35 * value + 0.15 * distribution_consistency

    return _finish(
        "oneranker", "OneRanker: Unified Generation and Ranking", data, method,
        {"target_agnostic_generation": True, "fake_item_tokens": fake_tokens.shape[1],
         "fine_grained_value_decoder": True, "distribution_consistency_loss": True},
        {"gmv_percent": 1.34, "deployment": "full production"},
    )


def reproduce_radar(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)
    # Deferred job: a full scorer searches a much larger pool and persists a
    # cohort cache. Online scoring only merges that cache with live recall.
    cache = {}
    for domain in np.unique(data.domains):
        profile = data.sequences.features[data.domains == domain].mean(0)
        full_ranker = data.sequences.features @ profile + 0.35 * (1.0 - data.popularity)
        cache[int(domain)] = np.argsort(-full_ranker)[:120]

    def method(history):
        live = base_scores(data, history)
        domain = int(np.bincount(data.domains[list(history[-8:])]).argmax())
        deferred = np.zeros(data.item_count)
        deferred[cache[domain]] = np.linspace(1.0, 0.1, len(cache[domain]))
        return live + 0.45 * deferred

    return _finish(
        "radar", "RADAR: Deferred Asynchronous Retrieval", data, method,
        {"offline_full_ranker_pool_multiplier": 50, "cohort_cache_entries": sum(map(len, cache.values())),
         "online_pre_rank_bypass": True, "live_deferred_merge": True},
        {"recall_at_200_multiplier": 2.0, "engagement_percent": 0.8},
    )


def reproduce_dualgr(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)
    codes = hierarchical_codes(data.sequences.features, 3, 8, seed)

    def method(history):
        short = data.transition[list(history[-3:])].mean(0)
        long = data.cosine[list(history)].mean(0)
        drift = 1.0 - data.cosine[history[-1], list(history[:-1])].mean()
        route = 1.0 / (1.0 + np.exp(-5.0 * (drift - 0.35)))
        valid_prefix = (codes[:, 0] == codes[history[-1], 0]).astype(float)
        exposed = np.bincount(history[-8:], minlength=data.item_count) > 0
        return route * short + (1.0 - route) * long + 0.15 * valid_prefix - 0.25 * exposed

    return _finish(
        "dualgr", "DualGR: Long- and Short-Term Generative Retrieval", data, method,
        {"dual_branch_router": True, "search_constrained_sid_decoding": True,
         "exposure_aware_next_token_loss": True},
        {"video_views_percent": 0.527, "watch_time_percent": 0.432},
    )


def reproduce_mpformer(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)

    def method(history):
        recent = list(history[-8:])
        objectives = np.stack((
            data.transition[recent].mean(0),
            data.cosine[recent].mean(0),
            1.0 - data.popularity,
        ))
        context = np.array((0.5, 0.3, 0.2))
        context += 0.15 * np.array((len(set(recent)) / len(recent), 0.0, 0.0))
        quotas = softmax(context)
        return quotas @ objectives

    return _finish(
        "mpformer", "MPFormer: Multi-Task Personalized Sequential Retriever", data, method,
        {"objective_conditioned_attention_heads": 3, "dynamic_quota_allocation": True,
         "personalized_objective_tokens": True},
        {"watch_time_percent": 0.426, "app_usage_percent": 0.195,
         "training_resource_percent": -60.0, "serving_resource_percent": -66.7},
    )


def reproduce_hap(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)

    def method(history):
        light = 0.65 * data.transition[history[-1]] + 0.35 * data.popularity
        strong = base_scores(data, history) + 0.2 * data.cosine[list(history[-8:])].std(0)
        difficulty = np.abs(strong - light)
        threshold = np.quantile(difficulty, 0.7)
        route = (difficulty >= threshold).astype(float)
        harmonized = difficulty / (difficulty.mean() + difficulty)
        return (1.0 - route) * light + route * strong + 0.1 * harmonized

    return _finish(
        "hap", "HAP: Heterogeneity-Aware Pre-ranking", data, method,
        {"gradient_harmonized_contrastive_difficulty": True,
         "difficulty_aware_model_routing": True, "strong_route_fraction": 0.3},
        {"app_duration_percent": 0.4, "active_days_percent": 0.05,
         "compute_increase_percent": 0.0},
    )


def reproduce_onepiece(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)

    def method(history):
        recent = data.sequences.features[list(history[-8:])]
        preference_anchor = recent.mean(0)
        situation = recent[-1] - recent[:-1].mean(0)
        latent = preference_anchor.copy()
        for _ in range(3):
            latent = np.tanh(latent + 0.5 * situation)
        retrieval = data.sequences.features @ preference_anchor
        click = data.sequences.features @ latent
        value = (1.0 - data.popularity) * np.maximum(click, 0.0)
        return 0.45 * retrieval + 0.35 * click + 0.20 * value

    return _finish(
        "onepiece", "OnePiece: Context Engineering and Latent Reasoning for Cascade Ranking", data, method,
        {"structured_context_tokens": 2, "blockwise_latent_reasoning_steps": 3,
         "progressive_retrieval_click_value_targets": True},
        {"retrieval_gmv_uu_percent": 1.08, "ranking_gmv_uu_percent": 1.12,
         "ad_revenue_percent": 2.90},
    )


def reproduce_intsr(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)
    item_age = np.argsort(np.argsort(data.popularity)) / max(data.item_count - 1, 1)

    def method(history):
        implicit_query = data.sequences.features[list(history[-5:])].mean(0)
        explicit_query = data.sequences.features[history[-1]]
        query_gate = min(0.8, 0.25 + 0.08 * len(set(history[-5:])))
        query = query_gate * explicit_query + (1.0 - query_gate) * implicit_query
        generation = data.sequences.features @ query
        temporal_vocabulary = 1.0 - np.abs(item_age - np.mean(item_age[list(history[-5:])]))
        return generation + 0.25 * temporal_vocabulary

    return _finish(
        "intsr", "IntSR: Integrated Generative Search and Recommendation", data, method,
        {"explicit_implicit_query_decoder": True, "query_placeholder_kv_cache": True,
         "time_varying_vocabulary_alignment": True},
        {"gmv_percent": 9.34, "poi_ctr_percent": 2.76, "travel_acc_percent": 7.04},
    )


def reproduce_cdm(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)

    @lru_cache(maxsize=1024)
    def method(history):
        relevance = base_scores(data, history)
        candidates = np.argsort(-relevance)[:50]
        teacher = np.zeros(data.item_count)
        selected, remaining = [], candidates.tolist()
        while remaining:
            winner = max(
                remaining,
                key=lambda item: relevance[item]
                - 0.25 * max((data.cosine[item, old] for old in selected), default=0.0),
            )
            teacher[winner] = 1.0 - len(selected) / len(candidates)
            selected.append(winner)
            remaining.remove(winner)
        context = data.sequences.features[list(history[-8:])].mean(0)
        design = np.column_stack((
            relevance, data.sequences.features @ context, data.popularity, np.ones(data.item_count)
        ))
        student = design @ ridge(design[candidates], teacher[candidates, None])
        return relevance + 0.5 * student[:, 0]

    return _finish(
        "cdm", "CDM: Contextual Distillation for Diversified Recommendation", data, method,
        {"mmr_teacher": True, "gumbel_topk_context_pairs": True,
         "contrastive_context_student": True, "quadratic_teacher_serving": False},
        {"watch_time_percent": 0.406, "vertical_category_percent": 0.188,
         "clustering_coefficient_percent": -0.957},
    )


def reproduce_cwm(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir, 260, 420)
    # Public MovieLens has no watch duration. Repeat-transition depth acts as a
    # declared censoring proxy; the likelihood still estimates latent benefit
    # beyond the observed cap instead of regressing the censored value directly.
    observed_cap = 1.0 + 4.0 * data.popularity
    continuation = np.diag(data.transition) + data.transition.max(1)
    latent_benefit = observed_cap + (-np.log(np.clip(1.0 - continuation, 1e-6, 1.0)))
    interest = 1.0 - np.exp(-latent_benefit / np.maximum(observed_cap, 1e-6))

    def method(history):
        relevance = data.cosine[list(history[-8:])].mean(0)
        return relevance * interest - 0.15 * observed_cap

    return _finish(
        "cwm", "CWM: Counterfactual Watch Time for Duration-Debiased Recommendation", data, method,
        {"right_censored_likelihood": True, "latent_counterfactual_benefit": True,
         "cost_transform_to_interest": True, "duration_proxy_declared": True},
        {"mean_watch_time_percent": 2.9, "video_views_percent": 2.5, "ctr_percent": 0.3},
    )
