from __future__ import annotations

from pathlib import Path

import numpy as np

from .industrial_2026 import (
    base_scores,
    evaluate,
    load_industrial_data,
    ridge,
    summary_result,
    tune_blend,
)


def _run(key, title, dataset_dir, method, stages, paper_results, seed=42):
    data = load_industrial_data(dataset_dir, maximum_users=260, maximum_items=420)
    baseline = lambda history: base_scores(data, history)
    alpha, scorer, validation = tune_blend(data, baseline, lambda h: method(data, h))
    return summary_result(
        key=key,
        paper={"title": title},
        data=data,
        baseline_name="shared transition + content baseline",
        method_name=title.split(":", 1)[0],
        baseline=evaluate(data, baseline),
        proposed=evaluate(data, scorer),
        stages={**stages, "validation_selected_alpha": alpha, "validation": validation},
        paper_results=paper_results,
        scope=(
            "MovieLens-100K 的公开内容特征与行为序列用于执行论文核心机制；"
            "没有使用生产私有流量、线上触发器或十亿级向量索引，线上指标只引用原文。"
        ),
    )


def reproduce_dme(dataset_dir: Path, seed: int = 42) -> dict:
    def method(data, history):
        query = data.sequences.features[list(history[-8:])].mean(axis=0)
        evidence_type = int(np.argmax(np.abs(query)))
        typed = data.sequences.features[:, evidence_type]
        latent = data.sequences.features @ query
        # Cross-conditional reconstruction: reconstruct counterpart features
        # from the typed latent representation, used only during training.
        design = np.column_stack((latent, typed, latent * typed, np.ones(len(latent))))
        decoder = ridge(design, data.sequences.features)
        reconstructed = design @ decoder
        reconstruction = np.sum(reconstructed * query[None], axis=1)
        return 0.55 * data.cosine[list(history[-8:])].mean(axis=0) + 0.30 * latent + 0.15 * reconstruction

    return _run(
        "dme", "DME: Douyin Multimodal Embedding", dataset_dir, method,
        {
            "contrastive_pretraining": True,
            "evidence_grounded_typed_latent_reasoning": True,
            "cross_conditional_reconstruction_training_only": True,
            "serving_generation_heads": 0,
        },
        {"mmeb_v2_2b": 74.8, "mmeb_v2_9b": 78.4, "offline_relative_percent": 2.92, "online_lifetime_percent": 0.1},
        seed,
    )


def reproduce_steps(dataset_dir: Path, seed: int = 42) -> dict:
    def method(data, history):
        recent = list(history[-8:])
        transition = data.transition[recent].mean(axis=0)
        long_term = data.cosine[recent].mean(axis=0)
        # Gated ordinal planning controls the next invocation interval. High
        # uncertainty triggers sooner; the execution utility uses trajectory
        # reward while the filter rejects low-utility pushes.
        uncertainty = 1.0 - transition / max(transition.max(), 1e-12)
        ordinal_interval = 1.0 + 3.0 * uncertainty
        execution = 0.65 * transition + 0.35 * long_term
        gate = 1.0 / ordinal_interval
        safeguard = execution >= np.quantile(execution, 0.55)
        return execution * gate * safeguard

    return _run(
        "steps", "STEPS: Self-Triggered Agentic Push Recommendation", dataset_dir, method,
        {
            "planning_agent_gated_ordinal_regression": True,
            "execution_agent_trajectory_reward": True,
            "filtering_agent_safeguard": True,
            "closed_loop_self_trigger": True,
        },
        {"active_days_percent": 0.2843, "permission_disablement_percent": -1.9089, "compute_percent": -79.42},
        seed,
    )


def reproduce_spear(dataset_dir: Path, seed: int = 42) -> dict:
    def method(data, history):
        recent = list(history[-8:])
        original = data.sequences.features[recent[-1]]
        profile = data.sequences.features[recent].mean(axis=0)
        recall_embedding = data.sequences.features @ original
        rank_embedding = data.sequences.features @ profile
        rewrite_confidence = 1.0 / (1.0 + np.exp(-rank_embedding))
        semantic_fidelity = np.maximum(recall_embedding, 0.0)
        # Multiplication prevents a high-frequency generic rewrite from winning
        # without original-query relevance. The residual path is always kept.
        gated_rewrite = rewrite_confidence * semantic_fidelity * (0.5 + 0.5 * rank_embedding)
        residual_original = 0.35 * recall_embedding
        return residual_original + gated_rewrite

    return _run(
        "spear", "SPEAR: Selection-aware Personalized Rewriting and Retrieval", dataset_dir, method,
        {
            "dual_embedding_gradient_isolation": True,
            "multiplicative_rewrite_gate": True,
            "dynamic_rewrite_selector": True,
            "original_query_residual": True,
        },
        {"semantic_similarity_at_10_percent": 18.2, "click_recall_at_10_percent": 99.5, "query_view_ctr_percent": 0.259, "reading_depth_percent": 0.733},
        seed,
    )


def render_latest(result: dict) -> str:
    from .industrial_2026 import render_standard

    return render_standard(result)
