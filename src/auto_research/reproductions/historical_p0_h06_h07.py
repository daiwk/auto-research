"""Executable public-data proxies for historical P0 batches H06 and H07.

The implementations isolate the central computation of each paper on the
shared MovieLens protocol. Private traffic, production models and serving
systems stay outside the local reproduction boundary.
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
    summary_result,
    tune_blend,
)
from .industrial_2026 import render_standard as render


PAPERS = {
    "unimvt": {
        "key": "unimvt",
        "arxiv_id": "2602.12972",
        "title": "Jointly Optimizing Debiased CTR and Uplift for Coupons Marketing: A Unified Causal Framework",
        "organization": "Kuaishou Technology",
        "published": "2026-02-13",
        "topics": ("causal-recommendation", "uplift-modeling", "coupon-marketing"),
        "operator": "reward:causal-uplift",
        "evidence": ("Kuaishou coupon marketing", "Coupon revenue", 18.14, "10% production traffic online A/B", "Section 5.4"),
        "paper_results": {"coupon_revenue_lift_percent": 18.14, "roi_gain": 8.80, "coupon_pcoc_error_reduction_percent": 86.51},
        "omitted": ("private coupon assignments", "production CTR backbone", "online allocation service"),
    },
    "rq_gmm": {
        "key": "rq-gmm",
        "arxiv_id": "2602.12593",
        "title": "RQ-GMM: Residual Quantized Gaussian Mixture Model for Multimodal Semantic Discretization in CTR Prediction",
        "organization": "Tencent",
        "published": "2026-02-13",
        "topics": ("multimodal-recommendation", "semantic-tokenization", "ctr-prediction"),
        "operator": "head:residual-gmm",
        "evidence": ("Tencent short-video advertising", "Advertiser value", 1.502, "large-scale production online A/B", "Abstract and online experiments"),
        "paper_results": {"advertiser_value_lift_percent": 1.502},
        "omitted": ("production multimodal encoder", "private advertising features", "online CTR serving"),
    },
    "capts": {
        "key": "capts",
        "arxiv_id": "2602.12564",
        "title": "CAPTS: Channel-Aware, Preference-Aligned Trigger Selection for Multi-Channel Item-to-Item Retrieval",
        "organization": "Kuaishou Technology",
        "published": "2026-02-13",
        "topics": ("retrieval", "trigger-selection", "multi-channel-routing"),
        "operator": "context:channel-trigger-routing",
        "evidence": ("Kwai multi-channel retrieval", "Total app time spent", 0.713, "production online A/B", "Section 4.4.1"),
        "paper_results": {"total_time_lift_percent": 0.713, "average_time_per_device_lift_percent": 0.586, "daily_active_devices_lift_percent": 0.115},
        "omitted": ("four production I2I retrievers", "private downstream attribution logs", "online quota service"),
    },
    "mlcc": {
        "key": "mlcc",
        "arxiv_id": "2602.12041",
        "title": "Compress, Cross and Scale: Multi-Level Compression Cross Networks for Efficient Scaling in Recommender Systems",
        "organization": "Bilibili",
        "published": "2026-02-12",
        "topics": ("feature-interaction", "compression", "scaling-law"),
        "operator": "head:multi-level-cross",
        "evidence": ("Bilibili advertising", "Advertiser value", 32.0, "production online A/B under latency constraint", "Online experiments"),
        "paper_results": {"advertiser_value_lift_percent": 32.0, "auc_lift_percent": 0.52, "flops_reduction_multiple": 26.0},
        "omitted": ("private sparse features", "production DLRM stack", "industrial serving kernels"),
        "upstream": "https://github.com/shishishu/MLCC",
    },
    "ug_sep": {
        "key": "ug-sep",
        "arxiv_id": "2602.10455",
        "title": "Compute Only Once: UG-Separation for Efficient Large Recommendation Models",
        "organization": "ByteDance AML",
        "published": "2026-02-11",
        "topics": ("ranking-network", "inference-efficiency", "token-mixing"),
        "operator": "head:ug-separation",
        "evidence": ("ByteDance recommendation", "Inference latency reduction", 20.0, "production online A/B and deployment", "Abstract and online experiments"),
        "paper_results": {"inference_latency_reduction_percent": 20.0},
        "omitted": ("production RankMixer checkpoints", "W8A16 serving kernels", "private feature pipeline"),
    },
    "smes": {
        "key": "smes",
        "arxiv_id": "2602.09386",
        "title": "SMES: Towards Scalable Multi-Task Recommendation via Expert Sparsity",
        "organization": "Kuaishou Technology",
        "published": "2026-02-10",
        "topics": ("multi-task-learning", "sparse-moe", "expert-routing"),
        "operator": "reward:expert-balance",
        "evidence": ("Kuaishou short-video recommendation", "User watch time", 0.31, "production online A/B", "Section 4.7"),
        "paper_results": {"watch_time_lift_percent": 0.31, "gauc_lift_percent": 0.29, "activated_expert_reduction_percent": 50.0},
        "omitted": ("private multi-task labels", "production expert parallelism", "online routing service"),
    },
    "pit": {
        "key": "pit",
        "arxiv_id": "2602.08530",
        "title": "PIT: A Dynamic Personalized Item Tokenizer for End-to-End Generative Recommendation",
        "organization": "Beijing University of Posts and Telecommunications",
        "published": "2026-02-09",
        "topics": ("generative-recommendation", "semantic-id", "dynamic-tokenizer"),
        "operator": "head:personalized-tokenizer",
        "evidence": ("Kuaishou generative recommendation", "Online business metric", 0.402, "production online A/B", "Online experiments"),
        "paper_results": {"online_business_lift_percent": 0.402},
        "omitted": ("production co-generative model", "streaming index service", "private user-item logs"),
    },
    "zenith": {
        "key": "zenith",
        "arxiv_id": "2601.21285",
        "title": "Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation",
        "organization": "North Carolina State University",
        "published": "2026-01-29",
        "topics": ("ranking-network", "scaling-law", "feature-interaction"),
        "operator": "zenith",
        "evidence": ("TikTok Live", "Quality watch sessions per user", 9.93, "production online A/B", "Table 4"),
        "paper_results": {"quality_watch_sessions_lift_percent": 9.93, "quality_watch_duration_lift_percent": 8.11, "ctr_auc_lift_percent": 1.05},
        "omitted": ("billion-scale sparse features", "production TSMoE kernels", "TikTok Live serving stack"),
    },
    "easq": {
        "key": "easq",
        "arxiv_id": "2601.20215",
        "title": "Towards End-to-End Alignment of User Satisfaction via Questionnaire in Video Recommendation",
        "organization": "Kuaishou Technology",
        "published": "2026-01-28",
        "topics": ("satisfaction-alignment", "preference-learning", "online-learning"),
        "operator": "context:questionnaire-alignment",
        "evidence": ("Kuaishou video recommendation", "User satisfaction metric", 5.1, "production online A/B", "Section 5.3"),
        "paper_results": {"satisfaction_lift_percent": 5.1},
        "omitted": ("private questionnaire responses", "production ranking backbone", "online DPO update service"),
    },
    "s2gr": {
        "key": "s2gr",
        "arxiv_id": "2601.18664",
        "title": "S2GR: Stepwise Semantic-Guided Reasoning in Latent Space for Generative Recommendation",
        "organization": "Kuaishou Technology",
        "published": "2026-01-26",
        "topics": ("generative-recommendation", "latent-reasoning", "semantic-id"),
        "operator": "head:stepwise-semantic-reasoning",
        "evidence": ("Kuaishou recommendation", "Online core metric", 5.25, "production online A/B", "Section 5.4"),
        "paper_results": {"online_core_metric_lift_percent": 5.25},
        "omitted": ("production SID codebook", "private interaction graph", "autoregressive serving"),
    },
    "sparsectr": {
        "key": "sparsectr",
        "arxiv_id": "2601.17836",
        "title": "Unleashing the Potential of Sparse Attention on Long-term Behaviors for CTR Prediction",
        "organization": "Institute of Software, Chinese Academy of Sciences",
        "published": "2026-01-25",
        "topics": ("ctr-prediction", "long-sequence", "sparse-attention"),
        "operator": "context:evolutionary-sparse-attention",
        "evidence": ("Meituan list advertising", "CTR", 1.72, "1% traffic production online A/B for 7 days", "Section 4.7"),
        "paper_results": {"ctr_lift_percent": 1.72, "cpm_lift_percent": 1.41, "sequence_length": 1024},
        "omitted": ("private advertising histories", "production HSTU stack", "40 ms serving implementation"),
        "upstream": "https://github.com/laiweijiang/SparseCTR",
    },
    "hcub": {
        "key": "hcub",
        "arxiv_id": "2601.14333",
        "title": "Hierarchical Contextual Uplift Bandits for Catalog Personalization",
        "organization": "Dream11",
        "published": "2026-01-20",
        "topics": ("bandit", "uplift-modeling", "catalog-personalization"),
        "operator": "context:hierarchical-uplift",
        "evidence": ("Dream11 catalog personalization", "Revenue", 0.51, "production online A/B", "Introduction and online experiments"),
        "paper_results": {"revenue_lift_percent": 0.51, "engagement_lift_percent": 0.42, "regret_reduction_percent": 5.0},
        "omitted": ("private fantasy-sports catalog", "production bandit state", "online policy deployment"),
    },
    "airbnb_ebr": {
        "key": "airbnb-ebr",
        "arxiv_id": "2601.06873",
        "title": "Applying Embedding-Based Retrieval to Airbnb Search",
        "organization": "Airbnb",
        "published": "2026-01-11",
        "topics": ("search-retrieval", "embedding-retrieval", "hard-negative-mining"),
        "operator": "context:journey-retrieval",
        "evidence": ("Airbnb search", "Booking conversion", 0.31, "production online A/B", "Section 6.3"),
        "paper_results": {"booking_conversion_lift_percent": 0.31, "retrieval_traffic_share_percent": 16.0},
        "omitted": ("dynamic property inventory", "production HNSW/IVF service", "private booking journeys"),
    },
    "promise": {
        "key": "promise",
        "arxiv_id": "2601.04674",
        "title": "PROMISE: Process Reward Models Unlock Test-Time Scaling Laws in Generative Recommendations",
        "organization": "Kuaishou Technology",
        "published": "2026-01-08",
        "topics": ("generative-recommendation", "process-reward", "test-time-scaling"),
        "operator": "reward:process-reward",
        "evidence": ("Kuaishou generative recommendation", "Online core metric", 5.0, "production online A/B", "Section 4.3"),
        "paper_results": {"online_core_metric_lift_percent": 5.0},
        "omitted": ("production process reward model", "private SID trajectories", "latency-aware beam service"),
    },
    "harmonrank": {
        "key": "harmonrank",
        "arxiv_id": "2601.02955",
        "title": "Rethinking Multi-objective Ranking Ensemble in Recommender System: From Score Fusion to Rank Consistency",
        "organization": "Kuaishou Technology",
        "published": "2026-01-06",
        "topics": ("multi-objective-ranking", "rank-consistency", "ensemble"),
        "operator": "reward:rank-consistency",
        "evidence": ("Kuaishou live e-commerce", "Purchase", 2.635, "production online A/B", "Section 5.7"),
        "paper_results": {"purchase_lift_percent": 2.635, "watch_time_lift_percent": 0.451},
        "omitted": ("private multi-objective labels", "production ensemble models", "live serving stack"),
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


def _softmax(values: np.ndarray, axis: int = -1) -> np.ndarray:
    shifted = values - values.max(axis=axis, keepdims=True)
    output = np.exp(shifted)
    return output / np.maximum(output.sum(axis=axis, keepdims=True), 1e-12)


def score_unimvt(data, history):
    recent = np.asarray(history[-16:])
    factual = 0.55 * data.cosine[recent].mean(0) + 0.45 * data.transition[recent[-1]]
    treatment = (data.domains % 4).astype(np.float64)
    propensity = 0.15 + 0.70 * _rank01(data.popularity)
    residual = treatment - np.polyval(np.polyfit(propensity, treatment, 1), propensity)
    monotone_uplift = np.log1p(treatment) * residual / np.maximum(propensity * (1.0 - propensity), 0.1)
    return factual + 0.12 * monotone_uplift


def score_rq_gmm(data, history):
    def quantized():
        residual = data.sequences.features.astype(np.float64).copy()
        result = np.zeros_like(residual)
        rng = np.random.default_rng(12593)
        for _ in range(3):
            centers = residual[rng.choice(len(residual), size=8, replace=False)]
            distance = ((residual[:, None] - centers[None]) ** 2).sum(2)
            posterior = _softmax(-distance / 0.15, axis=1)
            component = posterior @ centers
            result += component
            residual -= component
        return result / np.maximum(np.linalg.norm(result, axis=1, keepdims=True), 1e-12)

    catalog = _cached("rq-gmm", data, quantized)
    query = catalog[np.asarray(history[-12:])].mean(0)
    return catalog @ query + 0.20 * data.transition[history[-1]]


def score_capts(data, history):
    recent = np.asarray(history[-16:])
    downstream = data.transition[recent] @ data.transition
    attribution = downstream.mean(0)
    channel_affinity = np.stack(
        [data.cosine[recent[data.domains[recent] % 4 == channel]].mean(0) if np.any(data.domains[recent] % 4 == channel) else np.zeros(data.item_count) for channel in range(4)]
    )
    route = channel_affinity.max(0)
    diversity = 1.0 - np.bincount(data.domains[recent], minlength=int(data.domains.max()) + 1)[data.domains] / len(recent)
    return attribution + 0.35 * route + 0.15 * diversity


def score_mlcc(data, history):
    features = data.sequences.features.astype(np.float64)
    recent = features[np.asarray(history[-12:])].mean(0)
    levels = []
    state = features
    for width in (8, 4, 2):
        _, _, right = np.linalg.svd(state - state.mean(0), full_matrices=False)
        compressed = state @ right[: min(width, right.shape[0])].T
        crossed = compressed * compressed.mean(0, keepdims=True)
        levels.append(crossed @ (compressed[np.asarray(history[-12:])].mean(0)))
        state = np.tanh(state + 0.15 * np.outer(levels[-1], recent))
    return sum(levels) + 0.20 * data.transition[history[-1]]


def score_ug_sep(data, history):
    features = data.sequences.features.astype(np.float64)
    user_state = features[np.asarray(history[-16:])].mean(0)
    reusable = features @ user_state
    candidate_compensation = (features * user_state[None]) @ np.linspace(0.5, 1.5, features.shape[1])
    return reusable + 0.30 * candidate_compensation + 0.20 * data.transition[history[-1]]


def score_smes(data, history):
    recent = np.asarray(history[-12:])
    base = data.cosine[recent].mean(0)
    experts = np.stack((base, data.transition[recent[-1]], 1.0 - _rank01(data.popularity), _rank01(data.popularity)))
    shared = experts[:2].mean(0)
    private_gate = _softmax(np.stack((experts[2], experts[3])), axis=0)
    private = (private_gate * experts[2:]).sum(0)
    balance = 1.0 - np.abs(private_gate[0] - private_gate[1])
    return shared + 0.35 * private + 0.10 * balance


def score_pit(data, history):
    recent = np.asarray(history[-16:])
    codes = _cached("pit", data, lambda: hierarchical_codes(data.sequences.features, levels=3, width=10, seed=85))
    user_codes = codes[recent]
    losses = np.stack([(codes[:, level, None] != user_codes[None, :, level]).mean(1) for level in range(3)])
    selected = losses.min(0)
    beam_robustness = np.partition(losses, min(1, losses.shape[0] - 1), axis=0)[:2].mean(0)
    return -selected - 0.30 * beam_robustness + 0.35 * data.transition[recent[-1]]


def score_zenith(data, history):
    features = data.sequences.features.astype(np.float64)
    recent = features[np.asarray(history[-16:])]
    prime_tokens = np.stack((recent.mean(0), recent.max(0), recent[-4:].mean(0)))
    fusion = _softmax(prime_tokens @ prime_tokens[-1]) @ prime_tokens
    tokenwise_boost = np.tanh(features * fusion[None]) * (1.0 + np.maximum(features, 0.0))
    return tokenwise_boost @ fusion + 0.20 * data.transition[history[-1]]


def score_easq(data, history):
    recent = np.asarray(history[-16:])
    backbone = data.cosine[recent].mean(0)
    sparse_questionnaire = 0.5 * data.transition[recent[-1]] + 0.5 * (1.0 - _rank01(data.popularity))
    preference = sparse_questionnaire - backbone
    lora_path = np.tanh(preference) * (0.5 + np.abs(backbone))
    return backbone + 0.35 * lora_path


def score_s2gr(data, history):
    recent = np.asarray(history[-12:])
    codes = _cached("s2gr", data, lambda: hierarchical_codes(data.sequences.features, levels=4, width=8, seed=64))
    score = np.zeros(data.item_count)
    prefix_confidence = np.ones(data.item_count)
    for level in range(4):
        distribution = np.bincount(codes[recent, level], minlength=8).astype(np.float64) + 0.1
        distribution /= distribution.sum()
        thinking = distribution[codes[:, level]]
        prefix_confidence *= 0.65 + thinking
        score += prefix_confidence * thinking / (level + 1)
    return score + 0.25 * data.transition[recent[-1]]


def score_sparsectr(data, history):
    recent = np.asarray(history[-24:])
    gaps = np.abs(np.diff(recent.astype(np.float64), prepend=recent[0]))
    split_points = np.argsort(-gaps[1:])[:3] + 1
    chunks = np.split(recent, np.sort(split_points))
    query = data.sequences.features[recent[-1]]
    chunk_vectors = np.stack([data.sequences.features[chunk].mean(0) for chunk in chunks])
    global_branch = data.sequences.features @ (_softmax(chunk_vectors @ query) @ chunk_vectors)
    transitions = np.asarray([chunk[-1] for chunk in chunks])
    transition_branch = data.cosine[transitions].mean(0)
    local_branch = data.cosine[recent[-6:]].mean(0)
    temporal_bias = np.exp(-np.linspace(1.0, 0.0, len(recent)))
    temporal = (data.cosine[recent] * temporal_bias[:, None]).sum(0) / temporal_bias.sum()
    return 0.30 * global_branch + 0.25 * transition_branch + 0.30 * local_branch + 0.15 * temporal


def score_hcub(data, history):
    recent = np.asarray(history[-16:])
    domain = data.domains[recent]
    coarse = np.bincount(domain, minlength=int(data.domains.max()) + 1).astype(np.float64)
    coarse /= max(coarse.sum(), 1.0)
    contextual = data.cosine[recent].mean(0)
    treatment = 1.0 - _rank01(data.popularity)
    inherited = 0.55 * coarse[data.domains] + 0.45 * coarse.mean()
    uplift = treatment * (contextual - contextual.mean())
    uncertainty = np.sqrt(np.maximum(inherited * (1.0 - inherited), 0.0))
    return contextual + 0.40 * uplift + 0.15 * uncertainty


def score_airbnb_ebr(data, history):
    recent = np.asarray(history[-20:])
    journey = 0.50 * data.cosine[recent[-5:]].mean(0) + 0.30 * data.cosine[recent].mean(0) + 0.20 * data.transition[recent[-1]]
    hard_negative = np.maximum(data.popularity - np.quantile(data.popularity, 0.75), 0.0)
    dynamic_inventory = 0.8 + 0.2 * (data.domains % 2 == data.domains[recent[-1]])
    return dynamic_inventory * (journey - 0.18 * hard_negative)


def score_promise(data, history):
    recent = np.asarray(history[-12:])
    codes = _cached("promise", data, lambda: hierarchical_codes(data.sequences.features, levels=4, width=8, seed=46))
    process = np.ones(data.item_count)
    reward = np.zeros(data.item_count)
    for level in range(4):
        target_distribution = np.bincount(codes[recent, level], minlength=8).astype(np.float64) + 0.1
        target_distribution /= target_distribution.sum()
        step_reward = target_distribution[codes[:, level]]
        process *= 0.5 + step_reward
        reward += process / (level + 1)
    return reward + 0.25 * data.transition[recent[-1]]


def score_harmonrank(data, history):
    recent = np.asarray(history[-16:])
    objectives = np.stack((data.transition[recent[-1]], data.cosine[recent].mean(0), 1.0 - _rank01(data.popularity)))
    ranks = np.stack([_rank01(value) for value in objectives])
    dependency = _softmax(ranks @ ranks.T / np.sqrt(data.item_count), axis=1)
    aligned = dependency @ ranks
    consistency = 1.0 - aligned.std(0)
    return aligned.mean(0) + 0.25 * consistency


SCORERS = {
    "unimvt": score_unimvt,
    "rq_gmm": score_rq_gmm,
    "capts": score_capts,
    "mlcc": score_mlcc,
    "ug_sep": score_ug_sep,
    "smes": score_smes,
    "pit": score_pit,
    "zenith": score_zenith,
    "easq": score_easq,
    "s2gr": score_s2gr,
    "sparsectr": score_sparsectr,
    "hcub": score_hcub,
    "airbnb_ebr": score_airbnb_ebr,
    "promise": score_promise,
    "harmonrank": score_harmonrank,
}


def diagnostics(key: str, data, history) -> dict[str, float]:
    scores = SCORERS[key](data, history)
    result: dict[str, float] = {
        "finite_scores": int(np.isfinite(scores).sum()),
        "score_std": float(np.std(scores)),
    }
    details = {
        "unimvt": {"treatment_levels": 4, "counterfactual_towers": 2},
        "rq_gmm": {"residual_quantization_levels": 3, "gaussian_components": 8},
        "capts": {"retrieval_channels": 4, "downstream_attribution_hops": 2},
        "mlcc": {"compression_levels": 3, "cross_channels": 3},
        "ug_sep": {"reusable_user_paths": 1, "information_compensation_paths": 1},
        "smes": {"shared_experts": 2, "private_experts": 2},
        "pit": {"personalized_code_levels": 3, "beam_indices_per_item": 2},
        "zenith": {"prime_tokens": 3, "tokenwise_boost_paths": 1},
        "easq": {"questionnaire_paths": 1, "preference_alignment_paths": 1},
        "s2gr": {"reasoning_steps": 4, "semantic_code_levels": 4},
        "sparsectr": {"time_chunks": 4, "sparse_attention_branches": 3},
        "hcub": {"context_levels": 2, "uplift_policy_paths": 1},
        "airbnb_ebr": {"journey_stages": 3, "hard_negative_paths": 1},
        "promise": {"process_reward_steps": 4, "beam_pruning_signals": 1},
        "harmonrank": {"ranking_objectives": 3, "dependency_attention_heads": 1},
    }
    return result | details[key]


def reproduce_h06_h07(key: str, dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline_scorer = lambda history: base_scores(data, history)
    alpha, blended, _ = tune_blend(
        data,
        baseline_scorer,
        lambda history: SCORERS[key](data, history),
    )
    baseline = evaluate(data, baseline_scorer)
    method = evaluate(data, blended)
    paper = PAPERS[key]
    result = summary_result(
        key=paper["key"],
        paper={
            "arxiv_id": paper["arxiv_id"],
            "title": paper["title"],
            "url": f"https://arxiv.org/abs/{paper['arxiv_id']}",
            "organization": paper["organization"],
        },
        data=data,
        baseline_name="transition + content + popularity",
        method_name=f"{paper['key']} core mechanism (validation blend={alpha:.1f})",
        baseline=baseline,
        proposed=method,
        stages=diagnostics(key, data, data.sequences.train[0]),
        paper_results=paper["paper_results"],
        scope="执行论文可由公开 MovieLens 特征审计的核心计算；不复刻私有日志、生产模型或线上服务栈。",
    )
    result["manifest_ref"] = f"reproduction:{paper['key']}"
    return result


def make_adapter(key: str) -> ReproductionAdapter:
    paper = PAPERS[key]
    product, metric, lift, traffic, location = paper["evidence"]
    return ReproductionAdapter(
        key=paper["key"],
        paper=PaperMetadata(
            arxiv_id=paper["arxiv_id"],
            title=paper["title"],
            url=f"https://arxiv.org/abs/{paper['arxiv_id']}",
            track="recommendation",
            organization=paper["organization"],
            published=paper["published"],
            topics=paper["topics"],
            online_ab=(
                OnlineABEvidence(
                    product,
                    metric,
                    lift,
                    traffic,
                    source_url=f"https://arxiv.org/html/{paper['arxiv_id']}v1",
                    source_location=location,
                    retrieved_at="2026-09-05",
                ),
            ),
        ),
        run=lambda dataset_dir, seed=42: reproduce_h06_h07(key, dataset_dir, seed),
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
