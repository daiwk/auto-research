"""ANGLE public-data mechanism reviewed on 2026-09-19."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from .industrial_2026 import base_scores, evaluate, load_industrial_data, render_standard, summary_result, tune_blend


def hierarchical_identifiers(features, intents: int = 8, abstracts: int = 4):
    """Build deterministic intent×abstract identifiers from public item features."""
    x = np.asarray(features, dtype=np.float64)
    intent = np.argmax(x[:, :intents], axis=1) % intents
    abstract = np.argmax(np.abs(x[:, intents:intents + abstracts]), axis=1) % abstracts
    return np.stack([intent, abstract], axis=1)


def angle_joint_scores(features, history, identifiers):
    """Execute generation, discrimination and ranking signals jointly."""
    x = np.asarray(features, dtype=np.float64)
    hist = np.asarray(history[-12:], dtype=np.int64)
    query = x[hist].mean(0)
    generation = x @ query
    intent_hist = np.bincount(identifiers[hist, 0], minlength=int(identifiers[:, 0].max()) + 1)
    abstract_hist = np.bincount(identifiers[hist, 1], minlength=int(identifiers[:, 1].max()) + 1)
    discrimination = intent_hist[identifiers[:, 0]] + 0.5 * abstract_hist[identifiers[:, 1]]
    ranking = generation + 0.15 * discrimination
    return ranking, {"generation_loss_proxy": float(-generation[hist].mean()), "discrimination_margin": float(discrimination.max() - discrimination.mean()), "ranking_score_std": float(ranking.std())}


def dynamic_constrained_beam(scores, identifiers, allowed_pairs, beam_size=20):
    allowed = {tuple(pair) for pair in allowed_pairs}
    order = np.argsort(-np.asarray(scores))
    selected = [int(index) for index in order if tuple(identifiers[index]) in allowed][:beam_size]
    return selected, {"valid_pair_count": len(allowed), "beam_size": len(selected), "invalid_pruned": int(len(order) - sum(tuple(identifiers[index]) in allowed for index in order))}


def reproduce(dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir)
    ids = hierarchical_identifiers(data.sequences.features)
    baseline_scorer = lambda history: base_scores(data, history)
    audit = {}

    def raw_method(history):
        scores, joint = angle_joint_scores(data.sequences.features, history, ids)
        history_pairs = {tuple(pair) for pair in ids[np.asarray(history[-12:], dtype=np.int64)]}
        # Keep observed intent plus every abstract child as the public-data
        # counterpart of the paper's request-dependent constrained trie.
        allowed = {(intent, abstract) for intent, _ in history_pairs for abstract in np.unique(ids[:, 1])}
        chosen, beam = dynamic_constrained_beam(scores, ids, allowed, beam_size=min(40, len(scores)))
        constrained = np.full(len(scores), scores.min() - 1.0)
        constrained[chosen] = scores[chosen]
        audit.update(joint, **beam)
        return constrained

    alpha, scorer, validation = tune_blend(data, baseline_scorer, raw_method)
    sample = data.sequences.train[0]; raw_method(sample)
    result = summary_result(
        key="angle", paper={"arxiv_id":"2609.18296", "title":"One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations", "url":"https://arxiv.org/abs/2609.18296", "organization":"Tencent"},
        data=data, baseline_name="transition + content + popularity", method_name="ANGLE hierarchical identifier retrieval",
        baseline=evaluate(data, baseline_scorer), proposed=evaluate(data, scorer),
        stages={**audit, "validation_only_alpha": alpha, "validation_metrics": validation, "joint_objectives": ("generation", "discrimination", "ranking")},
        paper_results={"wts_consumption_lift_percent":1.81,"wts_gmv_lift_percent":2.16,"qbs_consumption_lift_percent":6.57},
        scope="公开 MovieLens 特征执行层次标识、三目标打分和动态约束 beam；不复刻腾讯广告语料、生产索引或线上流量。",
    )
    result["manifest_ref"] = "reproduction:angle"; result["setup"]["seed"] = seed
    return result


def make_adapter() -> ReproductionAdapter:
    metrics = (("consumption",1.81),("GMV",2.16),("clicks",1.50),("conversions",1.44),("exposure",2.49))
    evidence = tuple(OnlineABEvidence("Weixin Top Stories sponsored search", metric, lift, "production online A/B", source_url="https://arxiv.org/html/2609.18296v1", source_location="online experiment table", retrieved_at="2026-09-19") for metric, lift in metrics)
    return ReproductionAdapter(
        key="angle", paper=PaperMetadata(arxiv_id="2609.18296", title="One-Step Retrieval Framework for Real-Time Sponsored Search Ads Using Hierarchical Text Representations", url="https://arxiv.org/abs/2609.18296", track="recommendation", organization="Tencent", published="2026-09-16", publication_label="arXiv v1", topics=("sponsored-search","generative-retrieval","hierarchical-identifiers"), online_ab=evidence),
        run=reproduce, render=render_standard, fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=("Tencent private sponsored-search logs","production hierarchical index","online serving stack"), evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K",), baseline="transition + content + popularity", metrics=("hit_at_10","ndcg_at_10","fresh_hit_at_10","head_share_at_10"),
        default_seeds=(42,43,44), budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
    )
