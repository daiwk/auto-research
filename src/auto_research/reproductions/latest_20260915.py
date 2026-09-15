"""Executable mechanisms for industrial papers reviewed through 2026-09-15."""

from __future__ import annotations

import itertools
from pathlib import Path

import numpy as np

from .base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from .industrial_2026 import base_scores, evaluate, load_industrial_data, ridge, softmax, summary_result, tune_blend
from .industrial_2026 import render_standard


PAPERS = {
    "pindco": {
        "arxiv_id": "2609.11943",
        "title": "PinDCO: Whole-Page Aware Dynamic Creative Optimization at Scale",
        "organization": "Pinterest",
        "published": "2026-07-21",
        "topics": ("advertising", "creative-optimization", "whole-page-optimization", "multi-tower"),
        "paper_results": {"ad_ctr_lift_percent": 3.09},
        "evidence": ("Pinterest Ads", "ad CTR", 3.09, "production A/B followed by platform launch", "Abstract; Section 4.2"),
        "omitted": ("Pinterest private creative and traffic logs", "production feature store/cache", "online bandit traffic allocation"),
    },
    "mima": {
        "arxiv_id": "2609.12842",
        "title": "MIMA: Multi-Interest Recommendation via Multi-Positive Exclusive Assignment",
        "organization": "Alibaba International Digital Commerce Group",
        "published": "2026-09-11",
        "topics": ("retrieval", "multi-interest", "exclusive-assignment", "industrial-recommendation"),
        "paper_results": {"transaction_count_lift_percent": 5.60, "transaction_amount_lift_percent": 5.44},
        "evidence": ("large-scale e-commerce homepage retrieval", "transaction count", 5.60, "seven-day production A/B", "Section 5.5.2, Table 6"),
        "omitted": ("Alibaba private request groups and catalog", "production causal Transformer checkpoint", "online retrieval serving graph"),
    },
    "chronicle-rec": {
        "arxiv_id": "2609.12375",
        "title": "ChronicleRec: Pre-training Temporally Anchored Tokens for Lifelong User Modeling",
        "organization": "Tencent",
        "published": "2026-09-11",
        "topics": ("ranking", "long-sequence", "sequence-compression", "pretraining"),
        "paper_results": {"gmv_lift_percent": 1.61, "gmv_ci95_low_percent": 0.678, "gmv_ci95_high_percent": 2.547},
        "evidence": ("Weixin Moments Ads pCVR", "GMV", 1.61, "seven-day production A/B", "Section 4.9"),
        "omitted": ("Tencent private AdLive logs", "production MixFormer checkpoint", "asynchronous KV-cache serving"),
    },
}


def _zscore(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    return (values - values.mean()) / (values.std() + 1e-8)


def pixel_penalty(relative_aspect_ratio, strength: float) -> np.ndarray:
    """PinDCO Eq. (1): monotone whole-page pixel penalty."""
    ratio = np.asarray(relative_aspect_ratio, dtype=np.float64)
    return np.clip(1.0 - np.tanh(strength * (ratio - 1.0)), 0.0, 1.0)


def component_fusion_scores(data, history, strength: float = 0.45) -> np.ndarray:
    """Component-specialized towers, ad-conditioned delta fusion, and PAM."""
    features = data.sequences.features.astype(np.float64)
    split = max(1, features.shape[1] // 2)
    image, text = features[:, :split], features[:, split:]
    recent = np.asarray(history[-10:], dtype=np.int64)
    image_query = image[recent].mean(0)
    text_query = text[recent].mean(0) if text.shape[1] else np.zeros(0)
    image_tower = image @ image_query
    text_tower = text @ text_query if text.shape[1] else np.zeros(len(features))
    component_delta = 0.65 * _zscore(image_tower) + 0.35 * _zscore(text_tower)
    ad_logit = _zscore(base_scores(data, history))
    fused_logit = ad_logit + 0.35 * np.tanh(component_delta)
    # Public data has no creative aspect ratio.  A deterministic content-norm
    # proxy keeps the exact PAM equation executable without claiming pixel data.
    norm = np.linalg.norm(features, axis=1)
    relative_ratio = norm / max(np.median(norm), 1e-8)
    return fused_logit * pixel_penalty(relative_ratio, strength)


def exclusive_assignment(cost: np.ndarray) -> tuple[np.ndarray, float]:
    """Exact one-to-one Hungarian objective for the small public mini-suite."""
    cost = np.asarray(cost, dtype=np.float64)
    rows, columns = cost.shape
    size = min(rows, columns)
    best_perm, best_cost = None, float("inf")
    for chosen in itertools.permutations(range(columns), size):
        value = float(sum(cost[row, column] for row, column in enumerate(chosen)))
        if value < best_cost:
            best_perm, best_cost = chosen, value
    return np.asarray(best_perm, dtype=np.int64), best_cost


def mima_interests(features: np.ndarray, history, interests: int = 4) -> tuple[np.ndarray, np.ndarray, int]:
    """Multi-positive exclusive updates plus activation calibration."""
    sequence = np.asarray(history, dtype=np.int64)
    groups = [group for group in np.array_split(sequence, interests) if len(group)]
    centers = np.stack([features[group].mean(0) for group in groups])
    assignments = 0
    # Adjacent positives emulate same-request positive sets on public sequences.
    for positive_ids in np.array_split(sequence[-min(len(sequence), 2 * len(centers)):], len(centers)):
        if not len(positive_ids):
            continue
        positives = features[positive_ids]
        cost = -centers @ positives.T
        matched, _ = exclusive_assignment(cost)
        for row, column in enumerate(matched):
            centers[row] = 0.7 * centers[row] + 0.3 * positives[column]
            assignments += 1
    activation = softmax(np.asarray([len(group) for group in groups], dtype=np.float64))
    return centers, activation, assignments


def mima_scores(data, history) -> np.ndarray:
    features = data.sequences.features.astype(np.float64)
    centers, activation, _ = mima_interests(features, history)
    channels = centers @ features.T
    return np.max(channels + np.log(activation[:, None] + 1e-12), axis=0)


def recency_merge(features: np.ndarray, history, near_keep: int = 8) -> np.ndarray:
    """ChronicleRec non-uniform merge: coarse far, medium mid, exact near."""
    sequence = np.asarray(history, dtype=np.int64)
    near = sequence[-near_keep:]
    older = sequence[:-near_keep]
    cut = max(0, len(older) // 2)
    far, mid = older[:cut], older[cut:]

    def pool(ids: np.ndarray, stride: int) -> list[np.ndarray]:
        return [features[ids[start:start + stride]].mean(0) for start in range(0, len(ids), stride)]

    tokens = pool(far, 4) + pool(mid, 2) + [features[index] for index in near]
    return np.stack(tokens) if tokens else features[sequence[-1:]]


def chronicle_tokens(features: np.ndarray, history, horizons=(0, 3, 6)) -> np.ndarray:
    """Causal, temporally anchored summaries over complementary horizons."""
    branches = []
    for dropped in horizons:
        visible = history[:-dropped] if dropped and len(history) > dropped else history
        merged = recency_merge(features, visible)
        anchors = np.unique(np.linspace(0, len(merged) - 1, min(4, len(merged)), dtype=int))
        for anchor in anchors:
            causal_prefix = merged[: anchor + 1]
            weights = np.linspace(0.5, 1.0, len(causal_prefix))
            branches.append(np.average(causal_prefix, axis=0, weights=weights))
    return np.stack(branches)


def _chronicle_alignment(data) -> np.ndarray:
    source, target = [], []
    features = data.sequences.features.astype(np.float64)
    for history, positive in zip(data.sequences.train, data.sequences.validation):
        source.append(chronicle_tokens(features, history).mean(0))
        target.append(features[positive])
    return ridge(np.asarray(source), np.asarray(target), regularization=0.1)


def chronicle_scores(data, history, alignment: np.ndarray) -> np.ndarray:
    tokens = chronicle_tokens(data.sequences.features.astype(np.float64), history)
    aligned = tokens @ alignment
    return np.max(aligned @ data.sequences.features.T, axis=0)


def reproduce(key: str, dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir)
    baseline_scorer = lambda history: base_scores(data, history)
    stages: dict[str, object] = {}
    if key == "pindco":
        raw_method = lambda history: component_fusion_scores(data, history)
        stages = {"component_towers": 2, "ad_conditioned_delta": True, "pixel_penalty_exact": True}
    elif key == "mima":
        raw_method = lambda history: mima_scores(data, history)
        _, activation, assignments = mima_interests(data.sequences.features, data.sequences.train[0])
        stages = {"exclusive_assignments": assignments, "activation_sum": float(activation.sum()), "one_to_one": True}
    else:
        alignment = _chronicle_alignment(data)
        raw_method = lambda history: chronicle_scores(data, history, alignment)
        sample = chronicle_tokens(data.sequences.features, data.sequences.train[0])
        stages = {"chronicle_tokens": len(sample), "multi_horizon": True, "causal_anchors": True, "alignment_fitted_on_validation": True}

    alpha, method_scorer, validation = tune_blend(data, baseline_scorer, raw_method)
    stages.update({"validation_only_alpha": alpha, "validation_metrics": validation})
    baseline = evaluate(data, baseline_scorer)
    method = evaluate(data, method_scorer)
    row = PAPERS[key]
    result = summary_result(
        key=key,
        paper={"arxiv_id": row["arxiv_id"], "title": row["title"], "url": f"https://arxiv.org/abs/{row['arxiv_id']}", "organization": row["organization"]},
        data=data,
        baseline_name="transition + content + popularity",
        method_name=f"{key} executable mechanism",
        baseline=baseline,
        proposed=method,
        stages=stages,
        paper_results=row["paper_results"],
        scope={
            "pindco": "公开 MovieLens 执行组件专塔、ad-conditioned delta 融合与 PAM 精确公式；内容范数仅替代私有像素尺寸，不等于 Pinterest 创意线上复现。",
            "mima": "公开序列执行多正例一对一匹配、互补兴趣更新与 activation calibration；用分段特征替代生产 causal Transformer 与请求日志。",
            "chronicle-rec": "公开序列执行非均匀合并、因果锚点、多 horizon 与 alignment；不复刻腾讯私有 MixFormer、AdLive 和异步缓存。",
        }[key],
    )
    result["manifest_ref"] = f"reproduction:{key}"
    result["setup"]["seed"] = seed
    return result


def make_adapter(key: str) -> ReproductionAdapter:
    row = PAPERS[key]
    product, metric, lift, traffic, location = row["evidence"]
    second_evidence = ()
    if key == "mima":
        second_evidence = (OnlineABEvidence(product, "transaction amount", 5.44, traffic, source_url="https://arxiv.org/html/2609.12842v1", source_location=location, experiment_duration="seven days", retrieved_at="2026-09-15"),)
    return ReproductionAdapter(
        key=key,
        paper=PaperMetadata(
            arxiv_id=row["arxiv_id"], title=row["title"], url=f"https://arxiv.org/abs/{row['arxiv_id']}",
            track="recommendation", organization=row["organization"], published=row["published"], publication_label="arXiv v1",
            topics=row["topics"], online_ab=(OnlineABEvidence(product, metric, lift, traffic, source_url=f"https://arxiv.org/html/{row['arxiv_id']}v1", source_location=location, experiment_duration="seven days" if key != "pindco" else None, significance="95% CI excludes zero" if key == "chronicle-rec" else None, retrieved_at="2026-09-15"),) + second_evidence,
        ),
        run=lambda dataset_dir, seed=42: reproduce(key, dataset_dir, seed), render=render_standard,
        fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=row["omitted"],
        evaluation_tier=EvaluationTier.PUBLIC_DATASET, datasets=("MovieLens 100K",),
        baseline="transition + content + popularity", metrics=("hit_at_10", "ndcg_at_10", "fresh_hit_at_10", "head_share_at_10"),
        evolve_operators=(), default_seeds=(42, 43, 44), budget="220 users / 360 items; validation-only blend selection",
        device_capabilities=("cpu",), infer_device_capabilities=False,
    )
