"""Executable public-data proxies for the H04 industrial-paper batch.

The implementations intentionally share the audited MovieLens protocol while
keeping nine paper-specific operators.  Production LLMs, private traffic and
serving systems remain explicit reproduction boundaries.
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
from .industrial_2026 import (
    base_scores,
    evaluate,
    hierarchical_codes,
    load_industrial_data,
    softmax,
    summary_result,
    tune_blend,
)
from .industrial_2026 import render_standard as render


PAPERS = {
    "atomic_intent": {
        "key": "atomic-intent", "arxiv_id": "2606.10357",
        "title": "Atomic Intent Reasoning: Bringing LLM Semantics to Industrial Cross-Domain Recommendations",
        "organization": "The Hong Kong Polytechnic University", "published": "2026-06-09",
        "topics": ("cross-domain", "llm-recommendation", "intent-retrieval"),
        "operator": "context:atomic-intent-tree",
        "evidence": ("Kuaishou E-commerce", "GMV", 3.446, "5.08% production traffic", "Section 5.6"),
        "paper_results": {"gmv_lift_percent": 3.446, "throughput_gain_x": 400.0},
        "omitted": ("offline production LLM", "Kuaishou intent store", "online serving stack"),
    },
    "toolrec": {
        "key": "toolrec", "arxiv_id": "2606.08466",
        "title": "ToolRec: Calibrated Preference Alignment for Query Recommendation in On-Device Assistants",
        "organization": "Huazhong University of Science and Technology", "published": "2026-06-07",
        "topics": ("query-recommendation", "preference-alignment", "tool-use"),
        "operator": "reward:tool-calibration",
        "evidence": ("OPPO Xiaobu", "CTR", 3.32, "7 days; 5% traffic per model", "Section 5.2, Table 1"),
        "paper_results": {"click_lift_percent": 4.74, "ctr_lift_percent": 3.32, "relevance_change_percent": -1.44},
        "omitted": ("Qwen3-14B LoRA", "private assistant logs", "online tool service"),
    },
    "ssrlive": {
        "key": "ssrlive", "arxiv_id": "2606.06970",
        "title": "SSRLive: Live Streaming Recommendation with Dynamic Semantic ID",
        "organization": "Taobao & Tmall Group, Alibaba", "published": "2026-06-05",
        "topics": ("live-streaming", "semantic-id", "multitask-ranking"),
        "operator": "head:dynamic-sid",
        "evidence": ("Alibaba live streaming", "Watch time", 3.38, "production A/B; statistically significant", "Section 6, Table 4"),
        "paper_results": {"watch_time_lift_percent": 3.38, "gmv_lift_percent": 0.72, "follower_lift_percent": 3.12, "interaction_lift_percent": 2.92},
        "omitted": ("production multimodal encoder", "0.04B industrial model", "partial-run serving"),
    },
    "taiji": {
        "key": "taiji", "arxiv_id": "2606.03866",
        "title": "Taiji: Pareto Optimal Policy Optimization with Semantics-IDs Trade-off for Industrial LLM-Enhanced Recommendation",
        "organization": "Kuaishou Technology", "published": "2026-06-02",
        "topics": ("advertising", "reinforcement-alignment", "pareto-optimization"),
        "operator": "reward:pareto-semantic-id",
        "evidence": ("Kuaishou advertising", "Revenue", 3.30, "7 days; 10% control and 10% treatment", "Section 3.4, Table 2"),
        "paper_results": {"advertiser_value_lift_percent": 2.83, "revenue_lift_percent": 3.30},
        "omitted": ("DeepSeek-R1-7B training", "teacher CoT generation", "Kuaishou ad platform"),
    },
    "primal_dual_decoding": {
        "key": "primal-dual-decoding", "arxiv_id": "2607.19357",
        "title": "Stochastic Primal-Dual Decoding for Multiobjective Generative Recommender Systems",
        "organization": "Spotify", "published": "2026-05-26",
        "topics": ("generative-recommendation", "multiobjective", "constrained-decoding"),
        "operator": "reward:primal-dual",
        "evidence": ("Spotify recommender", "Auxiliary objective", 1.8, "large-scale online A/B; zero user-satisfaction cost", "Section 5.2"),
        "paper_results": {"auxiliary_objective_lift_percent": 1.8, "user_satisfaction_cost_percent": 0.0},
        "omitted": ("production autoregressive ranker", "private objective attributes", "capacity management"),
    },
    "muchator": {
        "key": "muchator", "arxiv_id": "2605.27103",
        "title": "MuChator: Enabling Active Music Discovery via Conversational Music LLMs in Douyin Music",
        "organization": "ByteDance", "published": "2026-05-26",
        "topics": ("music-recommendation", "conversational-llm", "active-discovery"),
        "operator": "context:conversational-intent",
        "evidence": ("Douyin Music", "Active days", 46.49, "approximately one month; >0.1B daily users", "Section 4.2, Table 2"),
        "paper_results": {"active_day_lift_percent": 46.49, "duration_lift_percent": 77.36, "ctr_lift_percent": 11.26},
        "omitted": ("Qwen3-8B pretraining/SFT/RL", "private music corpus", "conversational serving"),
    },
    "causal_representation": {
        "key": "causal-representation", "arxiv_id": "2605.27043",
        "title": "Causal Representation Learning for Generalisable Recommendation",
        "organization": "University of Warwick", "published": "2026-05-26",
        "topics": ("causal-recommendation", "distribution-shift", "representation-learning"),
        "operator": "head:causal-bottleneck",
        "evidence": ("Spotify playlist generation", "Track streams", 0.75, "2 weeks; millions of users; 95% CI [+0.54%, +0.96%]", "Section 4.3, Table 2"),
        "paper_results": {"track_stream_lift_percent": 0.75, "skip_reduction_percent": 0.61, "minutes_played_lift_percent": 0.50},
        "omitted": ("production session ranker", "private random-exposure logs", "live policy distribution"),
    },
    "policy_facet": {
        "key": "policy-facet", "arxiv_id": "2605.16479",
        "title": "Policy-Grounded Dynamic Facet Suggestions for Job Search",
        "organization": "LinkedIn", "published": "2026-05-15",
        "topics": ("job-search", "facet-retrieval", "policy-ranking"),
        "operator": "head:policy-facet",
        "evidence": ("LinkedIn Job Search", "Facet CTR", 34.8, "production A/B; p<0.0001", "Section 4.2, Table 5"),
        "paper_results": {"facet_ctr_lift_percent": 34.8, "apply_ratio_lift_percent": 2.6, "successful_session_lift_percent": 1.6},
        "omitted": ("LLM-curated production taxonomy", "fine-tuned SLMs", "LinkedIn serving cache"),
    },
    "pa_bridge": {
        "key": "pa-bridge", "arxiv_id": "2605.05855",
        "title": "Bridging Passive and Active: Enhancing Conversation Starter Recommendation via Active Expression Modeling",
        "organization": "ByteDance", "published": "2026-05-07",
        "topics": ("conversation-starter", "distribution-alignment", "debiasing"),
        "operator": "context:active-expression",
        "evidence": ("ByteDance conversation starter", "Feature penetration", 0.54, "production online A/B", "Section 3.3, Table 2"),
        "paper_results": {"feature_penetration_lift_percent": 0.54, "active_day_lift_percent": 0.04, "unique_clicked_lift_percent": 56.50},
        "omitted": ("private active-expression logs", "production base model", "online feedback loop"),
    },
}

_CACHE: dict[tuple[object, ...], object] = {}


def _cached(key: str, data, factory):
    features = data.sequences.features
    cache_key = (key, features.shape, float(features.sum()), float(features[:3].sum()))
    if cache_key not in _CACHE:
        _CACHE[cache_key] = factory()
    return _CACHE[cache_key]


def _rank01(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values)
    ranks = np.empty_like(order, dtype=np.float64)
    ranks[order] = np.linspace(0.0, 1.0, len(values))
    return ranks


def score_atomic_intent(data, history):
    codes = _cached("air-codes", data, lambda: hierarchical_codes(data.sequences.features, levels=3, width=8, seed=31))
    recent = np.asarray(history[-16:])
    recency = np.exp(np.linspace(-2.0, 0.0, len(recent)))
    recency /= recency.sum()
    intent_weight = np.zeros((3, 8), dtype=np.float64)
    for level in range(3):
        np.add.at(intent_weight[level], codes[recent, level], recency)
    tree = sum(intent_weight[level][codes[:, level]] / (level + 1) for level in range(3))
    target_semantics = data.cosine[recent].mean(0)
    return tree * (0.5 + _rank01(target_semantics)) + 0.15 * base_scores(data, history)


def score_toolrec(data, history):
    recent = np.asarray(history[-12:])
    preference = data.cosine[recent].mean(0)
    tool_frequency = np.bincount(data.domains[recent], minlength=int(data.domains.max()) + 1)
    dynamic_system = np.log1p(tool_frequency[data.domains])
    user_calibration = 0.75 + 0.5 * _rank01(preference)
    return user_calibration * preference + 0.35 * dynamic_system + 0.10 * data.popularity


def score_ssrlive(data, history):
    codes = _cached("ssrlive-codes", data, lambda: hierarchical_codes(data.sequences.features, levels=3, width=8, seed=7))
    recent = np.asarray(history[-10:])
    static_sid = (codes[:, None, :] == codes[recent][None, :, :]).mean(axis=(1, 2))
    dynamic_sid = data.transition[recent[-1]] + 0.5 * data.cosine[recent[-3:]].mean(0)
    interaction = np.sqrt(np.maximum(data.popularity * (1.0 + dynamic_sid), 0.0))
    return 0.45 * static_sid + 0.40 * dynamic_sid + 0.15 * interaction


def score_taiji(data, history):
    semantic = _rank01(data.cosine[np.asarray(history[-8:])].mean(0))
    collaborative = _rank01(data.transition[history[-1]])
    disagreement = np.abs(semantic - collaborative)
    semantic_weight = 0.5 + 0.35 * (disagreement - disagreement.mean())
    semantic_weight = np.clip(semantic_weight, 0.15, 0.85)
    return semantic_weight * semantic + (1.0 - semantic_weight) * collaborative


def score_primal_dual_decoding(data, history):
    relevance = _rank01(base_scores(data, history))
    auxiliary = 1.0 - _rank01(data.popularity)
    remaining = np.ones(data.item_count, dtype=bool)
    output = np.full(data.item_count, -1.0)
    lagrange, target, slate = 1.0, 0.55, min(20, data.item_count)
    for position in range(slate):
        combined = relevance + lagrange * auxiliary
        combined[~remaining] = -np.inf
        chosen = int(np.argmax(combined))
        output[chosen] = slate - position + 0.01 * combined[chosen]
        remaining[chosen] = False
        lagrange *= np.exp(-0.35 * (auxiliary[chosen] - target))
    output[remaining] = relevance[remaining] - 2.0
    return output


def score_muchator(data, history):
    recent = np.asarray(history[-8:])
    immediate_intent = data.sequences.features[recent[-3:]].mean(0)
    conversational = data.sequences.features @ immediate_intent
    discovery = 1.0 - data.popularity
    genre_gap = 1.0 - np.isin(data.domains, np.unique(data.domains[recent])).astype(float)
    return 0.65 * conversational + 0.20 * discovery + 0.15 * genre_gap


def _causal_features(data):
    features = data.sequences.features.astype(np.float64)
    confounder = np.column_stack((data.popularity, np.eye(int(data.domains.max()) + 1)[data.domains]))
    projection = np.linalg.lstsq(confounder, features, rcond=None)[0]
    residual = features - confounder @ projection
    return residual / np.maximum(np.linalg.norm(residual, axis=1, keepdims=True), 1e-12)


def score_causal_representation(data, history):
    causal = _cached("causal-features", data, lambda: _causal_features(data))
    query = causal[np.asarray(history[-12:])].mean(0)
    return causal @ query + 0.15 * data.transition[history[-1]]


def score_policy_facet(data, history):
    recent = np.asarray(history[-8:])
    query = data.sequences.features[recent].mean(0)
    retrieval = data.sequences.features @ query
    preferred = np.bincount(data.domains[recent], minlength=int(data.domains.max()) + 1)
    policy = np.log1p(preferred[data.domains])
    top_facets = np.argsort(-preferred)[: min(3, len(preferred))]
    allowed = np.isin(data.domains, top_facets).astype(float)
    return 0.65 * retrieval + 0.25 * policy + 0.10 * allowed


def score_pa_bridge(data, history):
    values = np.asarray(history[-16:])
    split = max(1, len(values) - 4)
    passive = data.sequences.features[values[:split]].mean(0)
    active = data.sequences.features[values[split:]].mean(0)
    aligned = 0.45 * passive + 0.55 * active
    semantic = data.sequences.features @ aligned
    propensity = np.maximum(data.popularity, 0.05)
    discrete = (data.domains[:, None] == data.domains[values[split:]][None]).mean(1)
    return semantic + 0.25 * discrete / np.sqrt(propensity)


SCORERS = {
    "atomic_intent": score_atomic_intent,
    "toolrec": score_toolrec,
    "ssrlive": score_ssrlive,
    "taiji": score_taiji,
    "primal_dual_decoding": score_primal_dual_decoding,
    "muchator": score_muchator,
    "causal_representation": score_causal_representation,
    "policy_facet": score_policy_facet,
    "pa_bridge": score_pa_bridge,
}


def diagnostics(key: str, data, history) -> dict[str, float]:
    scores = SCORERS[key](data, history)
    result: dict[str, float] = {
        "finite_scores": int(np.isfinite(scores).sum()),
        "score_std": float(np.std(scores)),
    }
    if key == "atomic_intent":
        result |= {"intent_tree_levels": 3, "cached_atomic_intents": data.item_count}
    elif key == "toolrec":
        result |= {"calibration_sides": 2, "dynamic_system_weight": 1}
    elif key == "ssrlive":
        result |= {"semantic_id_levels": 3, "dynamic_sid_channels": 2}
    elif key == "taiji":
        result |= {"pareto_objectives": 2, "adaptive_item_weights": data.item_count}
    elif key == "primal_dual_decoding":
        result |= {"decoder_steps": min(20, data.item_count), "constraint_multipliers": 1}
    elif key == "muchator":
        result |= {"intent_turns": min(3, len(history)), "active_discovery_channels": 2}
    elif key == "causal_representation":
        result |= {"confounder_channels": int(data.domains.max()) + 2, "inference_overhead_parameters": 0}
    elif key == "policy_facet":
        result |= {"retrieval_stages": 1, "pointwise_policy_ranker": 1}
    else:
        result |= {"distribution_domains": 2, "semantic_discretizer": 1}
    return result


def reproduce_h04(key: str, dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline_scorer = lambda history: base_scores(data, history)
    alpha, blended, _ = tune_blend(data, baseline_scorer, lambda history: SCORERS[key](data, history))
    baseline = evaluate(data, baseline_scorer)
    method = evaluate(data, blended)
    paper = PAPERS[key]
    result = summary_result(
        key=paper["key"],
        paper={"arxiv_id": paper["arxiv_id"], "title": paper["title"], "url": f"https://arxiv.org/abs/{paper['arxiv_id']}", "organization": paper["organization"]},
        data=data,
        baseline_name="transition + content + popularity",
        method_name=f"{paper['key']} core mechanism (validation blend={alpha:.1f})",
        baseline=baseline,
        proposed=method,
        stages=diagnostics(key, data, data.sequences.train[0]),
        paper_results=paper["paper_results"],
        scope="执行论文可由公开 MovieLens 特征审计的核心计算；不复刻私有日志、生产大模型或线上服务栈。",
    )
    result["manifest_ref"] = f"reproduction:{paper['key']}"
    return result


def make_adapter(key: str) -> ReproductionAdapter:
    paper = PAPERS[key]
    product, metric, lift, traffic, location = paper["evidence"]
    return ReproductionAdapter(
        key=paper["key"],
        paper=PaperMetadata(
            arxiv_id=paper["arxiv_id"], title=paper["title"], url=f"https://arxiv.org/abs/{paper['arxiv_id']}",
            track="recommendation", organization=paper["organization"], published=paper["published"], topics=paper["topics"],
            online_ab=(OnlineABEvidence(product, metric, lift, traffic, source_url=f"https://arxiv.org/html/{paper['arxiv_id']}v1", source_location=location, retrieved_at="2026-09-02"),),
        ),
        run=lambda dataset_dir, seed=42: reproduce_h04(key, dataset_dir, seed),
        render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=paper["omitted"],
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K",),
        baseline="transition + content + popularity",
        metrics=("hit_at_10", "ndcg_at_10", "fresh_hit_at_10", "head_share_at_10"),
        evolve_operators=(paper["operator"],),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; validation-only blend selection",
        device_capabilities=("cpu",),
        infer_device_capabilities=False,
    )
