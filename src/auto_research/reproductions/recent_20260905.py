"""Executable public-data proxies for the 2026-08-31--09-05 P0 scan.

The implementations preserve each paper's central ranking/retrieval operation
on the shared MovieLens protocol.  Production traffic, private labels and
serving systems are deliberately outside the reproduction boundary.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from .industrial_2026 import base_scores, evaluate, hierarchical_codes, load_industrial_data, summary_result, tune_blend
from .industrial_2026 import render_standard as render


PAPERS = {
    "rest": {
        "key": "rest",
        "arxiv_id": "2609.01240",
        "title": "From Language to Behavior: Scaling Sequence Transformers for Industrial Recommendation Ranking with Rec-Native Designs",
        "organization": "ByteDance",
        "published": "2026-09-01",
        "topics": ("ranking-network", "long-sequence", "shared-prefix-serving"),
        "operator": "context:rest-dual-gate",
        "evidence": ("production advertising platform", "core revenue metric", 11.93, "one-week online A/B; fully deployed", "Abstract; Section 3.5"),
        "paper_results": {"online_auc_lift_percent": 1.31, "revenue_lift_percent": 11.93, "p99_latency_ms": 50.0},
        "omitted": ("private behavior logs", "production sequence checkpoint", "shared-prefix serving kernel"),
    },
    "tgr": {
        "key": "tgr",
        "arxiv_id": "2609.00986",
        "title": "TGR: Advancing Industrial Recommendation from Generative-Paradigm Ranking toward Unified Generation and Reasoning",
        "organization": "Tencent",
        "published": "2026-09-01",
        "topics": ("generative-recommendation", "ranking-network", "reason-token"),
        "operator": "head:tgr-generation-reasoning",
        "evidence": ("Tencent production surfaces", "advertising revenue", 1.71, "five A/B-tested scenarios; full launches", "Abstract and online results"),
        "paper_results": {"ctr_lift_percent": 3.57, "advertising_revenue_lift_percent": 1.71, "new_user_conversion_lift_percent": 13.09},
        "omitted": ("private semantic-ID catalog", "production CCFormer checkpoint", "online generative serving"),
    },
    "camie": {
        "key": "camie",
        "arxiv_id": "2608.30255",
        "title": "CAMIE: Co-Engagement-Aware Multimodal Item Embeddings for Snap Dynamic Product Ads Retrieval",
        "organization": "Snap Inc.",
        "published": "2026-08-31",
        "topics": ("multimodal-retrieval", "co-engagement", "advertising"),
        "operator": "context:coengagement-embedding",
        "evidence": ("Snap Dynamic Product Ads", "overall CVR", 1.911, "production deployment on overall DPA traffic", "Abstract"),
        "paper_results": {"overall_ctr_lift_percent": 0.211, "overall_cvr_lift_percent": 1.911, "multimodal_control_cvr_lift_percent": 10.832},
        "omitted": ("private co-engagement journeys", "production MLLM checkpoint", "DPA ANN service"),
    },
    "setmir": {
        "key": "setmir",
        "arxiv_id": "2608.30251",
        "title": "SetMIR: Multi-Interest Retrieval as Set Prediction",
        "organization": "Snap Inc.",
        "published": "2026-08-31",
        "topics": ("multi-interest-retrieval", "set-prediction", "dynamic-dispatch"),
        "operator": "context:setmir-query-set",
        "evidence": ("Snap Dynamic Product Ads", "overall CVR", 3.1, "deployed production retrieval source", "Abstract"),
        "paper_results": {"overall_cvr_lift_percent": 3.1, "source_ctr_lift_percent": 44.0, "ann_query_reduction_percent": 33.0},
        "omitted": ("private DPA histories", "production transformer checkpoint", "ANN dispatch service"),
    },
}


def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)
    y = np.exp(x)
    return y / np.maximum(y.sum(axis=axis, keepdims=True), 1e-12)


def score_rest(data, history):
    recent = np.asarray(history[-24:])
    age = np.linspace(-2.2, 0.0, len(recent))
    temporal = _softmax(age) @ data.cosine[recent]
    semantic = data.cosine[recent].mean(0)
    transition = data.transition[recent[-1]]
    signal_gate = 1.0 / (1.0 + np.exp(-4.0 * (semantic - semantic.mean())))
    reusable_encoder = signal_gate * temporal + (1.0 - signal_gate) * semantic
    candidate_cross = reusable_encoder * (0.65 + 0.35 * transition)
    return candidate_cross + 0.25 * transition


def score_tgr(data, history):
    recent = np.asarray(history[-16:])
    codes = hierarchical_codes(data.sequences.features, levels=3, width=8, seed=986)
    path = np.ones(data.item_count)
    score = np.zeros(data.item_count)
    for level in range(3):
        counts = np.bincount(codes[recent, level], minlength=8).astype(float) + 0.1
        reason = counts[codes[:, level]] / counts.sum()
        path *= 0.6 + reason
        score += path / (level + 1)
    listwise = 0.6 * data.transition[recent[-1]] + 0.4 * data.cosine[recent].mean(0)
    return score + 0.35 * listwise


def score_camie(data, history):
    recent = np.asarray(history[-20:])
    content = data.sequences.features.astype(float)
    coengaged = data.transition[recent].mean(0)
    query = content[recent].T @ _softmax(coengaged[recent])
    query /= max(np.linalg.norm(query), 1e-12)
    symmetric_infonce = content @ query + data.cosine[recent].mean(0)
    return symmetric_infonce + 0.35 * coengaged


def score_setmir(data, history):
    recent = np.asarray(history[-24:])
    domains = np.unique(data.domains[recent])
    interests = []
    presence = []
    for domain in domains:
        members = recent[data.domains[recent] == domain]
        interests.append(data.cosine[members].mean(0))
        presence.append(len(members) / len(recent))
    interests = np.asarray(interests)
    presence = np.asarray(presence)
    active = presence >= max(1.0 / len(recent), np.median(presence) * 0.5)
    selected = interests[active]
    # Query-level NMS proxy: discard near-duplicate interest score vectors.
    kept = []
    for vector in selected:
        if not kept or max(np.corrcoef(vector, prior)[0, 1] for prior in kept) < 0.95:
            kept.append(vector)
    return np.max(np.asarray(kept), axis=0) + 0.2 * data.transition[recent[-1]]


SCORERS = {"rest": score_rest, "tgr": score_tgr, "camie": score_camie, "setmir": score_setmir}


def reproduce(key: str, dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline_scorer = lambda history: base_scores(data, history)
    alpha, blended, _ = tune_blend(data, baseline_scorer, lambda history: SCORERS[key](data, history))
    baseline = evaluate(data, baseline_scorer)
    proposed = evaluate(data, blended)
    row = PAPERS[key]
    result = summary_result(
        key=row["key"],
        paper={"arxiv_id": row["arxiv_id"], "title": row["title"], "url": f"https://arxiv.org/abs/{row['arxiv_id']}", "organization": row["organization"]},
        data=data,
        baseline_name="transition + content + popularity",
        method_name=f"{row['key']} core mechanism (validation blend={alpha:.1f})",
        baseline=baseline,
        proposed=proposed,
        stages={"finite_scores": int(np.isfinite(SCORERS[key](data, data.sequences.train[0])).sum()), "mechanism_paths": 3},
        paper_results=row["paper_results"],
        scope="公开 MovieLens 上的核心机制验证；不复刻私有日志、生产 checkpoint 或线上服务。",
    )
    result["manifest_ref"] = f"reproduction:{row['key']}"
    return result


def make_adapter(key: str) -> ReproductionAdapter:
    row = PAPERS[key]
    product, metric, lift, traffic, location = row["evidence"]
    return ReproductionAdapter(
        key=row["key"],
        paper=PaperMetadata(
            arxiv_id=row["arxiv_id"], title=row["title"], url=f"https://arxiv.org/abs/{row['arxiv_id']}",
            track="recommendation", organization=row["organization"], published=row["published"], topics=row["topics"],
            online_ab=(OnlineABEvidence(product, metric, lift, traffic, source_url=f"https://arxiv.org/html/{row['arxiv_id']}v1", source_location=location, retrieved_at="2026-09-05"),),
        ),
        run=lambda dataset_dir, seed=42: reproduce(key, dataset_dir, seed), render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=row["omitted"],
        evaluation_tier=EvaluationTier.PUBLIC_DATASET, datasets=("MovieLens 100K",),
        baseline="transition + content + popularity", metrics=("hit_at_10", "ndcg_at_10", "fresh_hit_at_10", "head_share_at_10"),
        evolve_operators=(row["operator"],), default_seeds=(42, 43, 44),
        budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
    )
