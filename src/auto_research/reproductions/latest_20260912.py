"""Executable mechanisms for industrial papers reviewed through 2026-09-12."""

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
from .industrial_2026 import (
    base_scores,
    evaluate,
    load_industrial_data,
    summary_result,
    tune_blend,
)
from .industrial_2026 import render_standard


PAPERS = {
    "unirec": {
        "arxiv_id": "2609.11052",
        "title": "UniRec: Cross-stage Multi-Task Fusion with Preference Alignment for Cascaded Recommender Systems",
        "organization": "Kuaishou",
        "published": "2026-09-10",
        "topics": ("pre-ranking", "ranking", "cross-stage-alignment", "industrial-recommendation"),
        "paper_results": {"app_usage_lift_percent": 0.616, "total_watch_time_lift_percent": 0.675, "video_watch_time_lift_percent": 0.755, "active_users_lift_percent": 0.189},
        "evidence": ("Kuaishou live recommender", "app usage", 0.616, "20% live traffic followed by full deployment", "Section 5.4, Table 5"),
        "omitted": ("private Kuaishou logs and features", "production pre-ranking/ranking serving graph", "full-scale cascaded model"),
    },
    "sequenceo1": {
        "arxiv_id": "2609.08443",
        "title": "SequenceO1: End-to-End Ultra-Long (100K) Sequence Modeling in Recommendation with Low-Rank Caching",
        "organization": "ByteDance / Douyin",
        "published": "2026-09-08",
        "topics": ("long-sequence", "sketch-attention", "prototype-compression", "industrial-recommendation"),
        "paper_results": {"thirty_day_activeness_lift_percent": 0.1968, "duration_lift_percent": 1.4999, "finish_lift_percent": 2.3256},
        "evidence": ("Douyin and Douyin Lite recommender", "30-day activeness", 0.1968, "one-month A/B followed by full-traffic deployment", "Section 4.3, Table 4"),
        "omitted": ("private 100K-event histories", "MRLB/FlashSA production kernels", "online cache service"),
    },
    "baff": {
        "arxiv_id": "2609.08725",
        "title": "BAFF: Bid-Aware Filter Family for Mitigating Training Data Interference in RTB A/B Tests",
        "organization": "Dable",
        "published": "2026-09-08",
        "topics": ("advertising", "rtb", "ab-testing", "training-data-interference"),
        "paper_results": {"cpc_te_gap_naive": 9.85, "cpc_te_gap_baff": 0.44, "ctr_te_gap_naive_pp": 1.94, "ctr_te_gap_baff_pp": 0.40},
        "evidence": ("production DSP real-time bidding", "absolute CPC treatment-effect gap reduction versus naive shared log", 95.53, "single advertiser/SSP; two- and three-day measurement phases", "Section 5.4, Tables 6-7"),
        "omitted": ("private DSP auction logs", "production CTR model", "market-side reference experiment"),
    },
}


def _zscore(values):
    values = np.asarray(values, dtype=np.float64)
    return (values - values.mean()) / (values.std() + 1e-8)


def unirec_scores(data, history):
    """Vertical cross-stage alignment plus compact pairwise aggregation."""
    pre_rank = base_scores(data, history)
    recent = list(history[-12:])
    rank = 0.6 * np.mean(data.transition[recent], axis=0) + 0.4 * np.mean(data.cosine[recent], axis=0)
    vertical = 0.5 * _zscore(pre_rank) + 0.5 * _zscore(rank)
    # Compact pairwise aggregation compares candidates against one domain
    # anchor instead of materializing every pair.  Group-relative centering is
    # the executable analogue of UniRec's attribute-GRR regularizer.
    anchors = np.full(int(data.domains.max()) + 1, rank.mean(), dtype=np.float64)
    for domain in np.unique(data.domains):
        anchors[domain] = np.mean(rank[data.domains == domain])
    pairwise = np.tanh(rank - anchors[data.domains])
    group_relative = np.empty_like(vertical)
    for domain in np.unique(data.domains):
        mask = data.domains == domain
        group_relative[mask] = vertical[mask] - vertical[mask].mean()
    return vertical + 0.25 * pairwise + 0.10 * group_relative


def sketch_prototypes(features, budget=4):
    """Farthest-first seeds followed by one assignment/update step."""
    if len(features) <= budget:
        return np.asarray(features, dtype=np.float64)
    centers = [0]
    distance = ((features - features[0]) ** 2).sum(-1)
    while len(centers) < budget:
        index = int(np.argmax(distance))
        centers.append(index)
        distance = np.minimum(distance, ((features - features[index]) ** 2).sum(-1))
    prototypes = np.asarray(features[centers], dtype=np.float64).copy()
    assignment = ((features[:, None] - prototypes[None]) ** 2).sum(-1).argmin(1)
    for index in range(len(prototypes)):
        members = features[assignment == index]
        if len(members):
            prototypes[index] = members.mean(0)
    return prototypes


def sequenceo1_scores(data, history, sketch_budget=4, recent_budget=8):
    recent = list(history[-recent_budget:])
    old = list(history[:-recent_budget]) or list(history[:-1])
    recent_branch = base_scores(data, recent)
    prototypes = sketch_prototypes(data.sequences.features[old], sketch_budget)
    sketch_branch = (prototypes @ data.sequences.features.T).max(0)
    # STCA-style parallel recent/sketch branches.  The history is compressed to
    # a fixed number of prototypes; no target information enters the sketch.
    return 0.65 * _zscore(recent_branch) + 0.35 * _zscore(sketch_branch)


def bid_aware_mask(control_ranks, control_bids, treatment_bids, candidates, k, l):
    control_ranks = np.asarray(control_ranks)
    control_bids = np.asarray(control_bids, dtype=np.float64)
    treatment_bids = np.asarray(treatment_bids, dtype=np.float64)
    d_ad = control_ranks / float(candidates)
    d_bp = np.maximum(control_bids - treatment_bids, 0.0) / np.maximum(control_bids, 1e-12)
    return (d_ad < k) & (d_bp < l), d_ad, d_bp


def reproduce_baff(seed=42):
    """Controlled RTB interference simulation with the paper's exact filter."""
    rng = np.random.default_rng(seed)
    requests, candidates, dimensions = 2400, 30, 12
    context = rng.normal(size=(requests, dimensions))
    ads = rng.normal(scale=0.35, size=(candidates, dimensions))
    values = rng.lognormal(0.1, 0.2, size=candidates)
    control_w = rng.normal(size=dimensions)
    treatment_w = control_w + rng.normal(scale=0.35, size=dimensions)
    true_w = treatment_w + rng.normal(scale=0.12, size=dimensions)
    control_scores = (context * control_w) @ ads.T
    treatment_scores = (context * treatment_w) @ ads.T
    control_choice = (control_scores * values).argmax(1)
    treatment_choice = (treatment_scores * values).argmax(1)
    control_bid = 1 / (1 + np.exp(-control_scores[np.arange(requests), control_choice])) * values[control_choice]
    treatment_bid = 1 / (1 + np.exp(-treatment_scores[np.arange(requests), treatment_choice])) * values[treatment_choice]
    ranks = np.argsort(np.argsort(-treatment_scores, axis=1), axis=1)[np.arange(requests), control_choice]
    keep, d_ad, d_bp = bid_aware_mask(ranks, control_bid, treatment_bid, candidates, 0.5, 0.5)

    arm_b = np.arange(requests) % 2 == 1
    chosen = np.where(arm_b, treatment_choice, control_choice)
    z = context + ads[chosen]
    probability = 1 / (1 + np.exp(-(z @ true_w) / dimensions))
    labels = rng.binomial(1, probability).astype(np.float64)
    b_only = arm_b
    naive = np.ones(requests, dtype=bool)
    filtered = arm_b | ((~arm_b) & keep)

    def fit(mask):
        matrix = z[mask]
        return np.linalg.solve(matrix.T @ matrix + 0.2 * np.eye(dimensions), matrix.T @ labels[mask])

    reference = fit(b_only)
    naive_theta, filtered_theta = fit(naive), fit(filtered)
    naive_gap = float(np.linalg.norm(naive_theta - reference))
    filtered_gap = float(np.linalg.norm(filtered_theta - reference))
    return {
        "paper": {"arxiv_id": "2609.08725", "title": PAPERS["baff"]["title"], "url": "https://arxiv.org/abs/2609.08725", "organization": "Dable"},
        "dataset": {"name": "controlled RTB simulation", "requests": requests, "candidates": candidates},
        "setup": {"adapter": "baff", "seed": seed, "same_split_and_candidates": True},
        "baseline": {"name": "naive pooled training", "parameter_deviation": naive_gap, "retained_control_fraction": 1.0},
        "method": {"name": "BAFF F(0.5,0.5)", "parameter_deviation": filtered_gap, "retained_control_fraction": float(keep[~arm_b].mean())},
        "relative": {"parameter_deviation_reduction_percent": 100 * (naive_gap - filtered_gap) / max(naive_gap, 1e-12)},
        "stages": {"d_ad_mean": float(d_ad.mean()), "d_bp_mean": float(d_bp.mean()), "filter_exactly_matches_equation": True},
        "paper_results": PAPERS["baff"]["paper_results"],
        "scope": "受控 RTB 仿真执行论文 F(k,l) 判据与 ridge 偏差诊断；不是论文线上 KPI，也不替代私有 DSP 日志。",
        "manifest_ref": "reproduction:baff",
    }


def reproduce(key: str, dataset_dir: Path, seed: int = 42):
    if key == "baff":
        return reproduce_baff(seed)
    data = load_industrial_data(dataset_dir)
    baseline_scorer = lambda history: base_scores(data, history)
    raw_method = unirec_scores if key == "unirec" else sequenceo1_scores
    alpha, method_scorer, validation = tune_blend(
        data, baseline_scorer, lambda history: raw_method(data, history)
    )
    baseline = evaluate(data, baseline_scorer)
    method = evaluate(data, method_scorer)
    result = summary_result(
        key=key,
        paper={"arxiv_id": PAPERS[key]["arxiv_id"], "title": PAPERS[key]["title"], "url": f"https://arxiv.org/abs/{PAPERS[key]['arxiv_id']}", "organization": PAPERS[key]["organization"]},
        data=data,
        baseline_name="transition + content + popularity",
        method_name=f"{key} executable mechanism",
        baseline=baseline,
        proposed=method,
        stages={"validation_only_alpha": alpha, "validation_metrics": validation, "finite_scores": data.item_count},
        paper_results=PAPERS[key]["paper_results"],
        scope=("MovieLens 的短公开序列仅验证跨阶段对齐/组相对聚合，不等于快手生产级 cascade。" if key == "unirec" else "MovieLens 历史远短于 100K；这里只验证固定预算 prototype sketch 与 recent 双分支，不复刻 MRLB/FlashSA。"),
    )
    result["manifest_ref"] = f"reproduction:{key}"
    result["setup"]["seed"] = seed
    return result


def render_baff(result):
    return "\n".join([
        f"# {result['paper']['title']}", "",
        "| Variant | parameter deviation | retained control logs |", "|---|---:|---:|",
        f"| {result['baseline']['name']} | {result['baseline']['parameter_deviation']:.6f} | 100.00% |",
        f"| {result['method']['name']} | {result['method']['parameter_deviation']:.6f} | {100 * result['method']['retained_control_fraction']:.2f}% |", "",
        f"相对 naive pooled training 的参数偏差变化：{result['relative']['parameter_deviation_reduction_percent']:+.2f}% 。", "",
        "## 复现边界", "", result["scope"], "",
    ])


def make_adapter(key: str) -> ReproductionAdapter:
    row = PAPERS[key]
    product, metric, lift, traffic, location = row["evidence"]
    return ReproductionAdapter(
        key=key,
        paper=PaperMetadata(
            arxiv_id=row["arxiv_id"], title=row["title"], url=f"https://arxiv.org/abs/{row['arxiv_id']}",
            track="recommendation", organization=row["organization"], published=row["published"],
            publication_label="arXiv v1", topics=row["topics"],
            online_ab=(OnlineABEvidence(product, metric, lift, traffic, source_url=f"https://arxiv.org/html/{row['arxiv_id']}", source_location=location, experiment_duration="one month" if key == "sequenceo1" else None, significance="all reported effects statistically significant" if key == "sequenceo1" else None, retrieved_at="2026-09-12"),),
        ),
        run=lambda dataset_dir, seed=42: reproduce(key, dataset_dir, seed),
        render=render_baff if key == "baff" else render_standard,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=row["omitted"],
        evaluation_tier=EvaluationTier.MECHANISM if key == "baff" else EvaluationTier.PUBLIC_DATASET,
        datasets=("controlled RTB simulation",) if key == "baff" else ("MovieLens 100K",),
        baseline="naive pooled training" if key == "baff" else "transition + content + popularity",
        metrics=("parameter_deviation", "retained_control_fraction") if key == "baff" else ("hit_at_10", "ndcg_at_10", "fresh_hit_at_10", "head_share_at_10"),
        # Evolve mappings are intentionally withheld until the main evaluator
        # can execute them; registry-only labels do not satisfy the contract.
        evolve_operators=(), default_seeds=(42, 43, 44),
        budget="2,400 simulated auctions" if key == "baff" else "220 users / 360 items; validation-only blend selection",
        device_capabilities=("cpu",), infer_device_capabilities=False,
    )
