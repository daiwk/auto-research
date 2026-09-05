"""Executable public-data proxies for the H05 industrial-paper batch.

Each scorer isolates one paper's central computation on the same audited
MovieLens protocol.  Private traffic, production LLMs and serving systems are
explicitly outside the local reproduction boundary.
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
    "marc": {
        "key": "marc", "arxiv_id": "2604.18146",
        "title": "Modular Representation Compression: Adapting LLMs for Efficient and Effective Recommendations",
        "organization": "Shanghai Jiao Tong University", "published": "2026-04-20",
        "topics": ("llm-recommendation", "representation-compression", "modular-learning"),
        "operator": "head:modular-compression",
        "evidence": ("Commercial search advertising", "eCPM", 2.82, "production online A/B", "Abstract and experiments"),
        "paper_results": {"ecpm_lift_percent": 2.82},
        "omitted": ("production LLM hidden states", "private advertising logs", "online serving stack"),
    },
    "rankup": {
        "key": "rankup", "arxiv_id": "2604.17878",
        "title": "RankUp: Towards High-rank Representations for Large Scale Advertising Recommender Systems",
        "organization": "Tencent", "published": "2026-04-20",
        "topics": ("advertising", "representation-collapse", "feature-interaction"),
        "operator": "head:high-rank-representation",
        "evidence": ("Weixin advertising", "GMV", 4.81, "fully deployed across three products", "Abstract and Section 1"),
        "paper_results": {"video_accounts_gmv_lift_percent": 3.41, "official_accounts_gmv_lift_percent": 4.81, "moments_gmv_lift_percent": 2.12},
        "omitted": ("production sparse features", "cross-pretrained embeddings", "Tencent advertising serving"),
    },
    "sid_coord": {
        "key": "sid-coord", "arxiv_id": "2604.10471",
        "title": "SID-Coord: Coordinating Semantic IDs for ID-based Ranking in Short-Video Search",
        "organization": "Kuaishou Technology", "published": "2026-04-12",
        "topics": ("short-video-search", "semantic-id", "long-tail-ranking"),
        "operator": "head:sid-coordination",
        "evidence": ("Kuaishou short-video search", "Long-play rate", 0.664, "production online A/B", "Abstract"),
        "paper_results": {"long_play_rate_lift_percent": 0.664, "playback_duration_lift_percent": 0.369},
        "omitted": ("production SID tokenizer", "private short-video logs", "online ranking backbone"),
    },
    "rclrec": {
        "key": "rclrec", "arxiv_id": "2603.28124",
        "title": "RCLRec: Reverse Curriculum Learning for Modeling Sparse Conversions in Generative Recommendation",
        "organization": "Alibaba International Digital Commerce Group", "published": "2026-03-30",
        "topics": ("generative-recommendation", "conversion-modeling", "curriculum-learning"),
        "operator": "context:reverse-curriculum",
        "evidence": ("Alibaba advertising recommendation", "Advertising revenue", 2.09, "production online A/B", "Abstract"),
        "paper_results": {"advertising_revenue_lift_percent": 2.09, "orders_lift_percent": 1.86},
        "omitted": ("production semantic tokenizer", "private conversion histories", "autoregressive serving"),
    },
    "tagllm": {
        "key": "tagllm", "arxiv_id": "2603.21481",
        "title": "TagLLM: A Fine-Grained Tag Generation Approach for Note Recommendation",
        "organization": "Tongji University", "published": "2026-03-23",
        "topics": ("content-understanding", "tag-generation", "knowledge-distillation"),
        "operator": "head:fine-grained-tags",
        "evidence": ("Note recommendation", "Cold-start page-view CTR", 32.37, "production online A/B", "Abstract"),
        "paper_results": {"view_duration_lift_percent": 0.31, "interaction_lift_percent": 0.96, "cold_start_ctr_lift_percent": 32.37},
        "omitted": ("multimodal teacher LLM", "private note corpus", "production distillation pipeline"),
    },
    "genfacet": {
        "key": "genfacet", "arxiv_id": "2603.19665",
        "title": "GenFacet: End-to-End Generative Faceted Search via Multi-Task Preference Alignment in E-Commerce",
        "organization": "JD.com", "published": "2026-03-20",
        "topics": ("e-commerce-search", "facet-generation", "preference-alignment"),
        "operator": "reward:facet-preference",
        "evidence": ("JD.com e-commerce search", "Facet CTR", 42.0, "production online A/B", "Abstract"),
        "paper_results": {"facet_ctr_lift_percent": 42.0, "user_conversion_lift_percent": 2.0},
        "omitted": ("production LLM", "private query/facet logs", "GRPO training and retrieval service"),
    },
    "cgr": {
        "key": "cgr", "arxiv_id": "2603.04227",
        "title": "Constraint-Aware Generative Re-ranking for Multi-Objective Optimization in Advertising Feeds",
        "organization": "Bilibili", "published": "2026-03-04",
        "topics": ("advertising", "generative-reranking", "constraint-optimization"),
        "operator": "reward:constraint-aware",
        "evidence": ("Bilibili advertising feeds", "Inference latency reduction", 85.0, "millions of daily requests; production online A/B", "Conclusion"),
        "paper_results": {"inference_latency_reduction_percent": 85.0, "business_constraint_satisfaction": 1.0},
        "omitted": ("production generator/evaluator network", "private ad-feed logs", "real-time serving constraints"),
    },
    "hpgr": {
        "key": "hpgr", "arxiv_id": "2603.00980",
        "title": "Beyond the Flat Sequence: Hierarchical and Preference-Aware Generative Recommendations",
        "organization": "Harbin Institute of Technology", "published": "2026-03-01",
        "topics": ("generative-recommendation", "hierarchical-sequence", "sparse-attention"),
        "operator": "context:hierarchical-preference",
        "evidence": ("Huawei AppGallery recommendation", "eCPM", 1.99, "production online A/B", "Section 1 and online experiments"),
        "paper_results": {"ecpm_lift_percent": 1.99},
        "omitted": ("industrial pretraining corpus", "production HSTU backbone", "AppGallery serving stack"),
    },
    "climber_pilot": {
        "key": "climber-pilot", "arxiv_id": "2602.13581",
        "title": "Climber-Pilot: A Non-Myopic Generative Recommendation Model Towards Better Instruction-Following",
        "organization": "NetEase Cloud Music", "published": "2026-02-14",
        "topics": ("generative-retrieval", "long-horizon", "instruction-following"),
        "operator": "context:instruction-foresight",
        "evidence": ("NetEase Cloud Music", "Core business metric", 4.24, "production online A/B", "Abstract"),
        "paper_results": {"core_business_metric_lift_percent": 4.24},
        "omitted": ("production generative retriever", "private music sequences", "business instruction service"),
    },
    "rolegen": {
        "key": "rolegen", "arxiv_id": "2602.13134",
        "title": "Awakening Dormant Users: Generative Recommendation with Counterfactual Functional Role Reasoning",
        "organization": "Beihang University", "published": "2026-02-13",
        "topics": ("generative-recommendation", "counterfactual-reasoning", "dormant-users"),
        "operator": "reward:counterfactual-role",
        "evidence": ("Kuaishou e-commerce", "Order volume", 7.3, "production online A/B", "Abstract"),
        "paper_results": {"recall_at_1_lift_percent": 6.2, "order_volume_lift_percent": 7.3},
        "omitted": ("LLM trajectory reasoner", "private dormant-user logs", "reasoning-feedback serving loop"),
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


def score_marc(data, history):
    def modular_features():
        features = data.sequences.features.astype(np.float64)
        nuisance = np.column_stack((np.ones(data.item_count), data.popularity))
        task_module = features - nuisance @ np.linalg.lstsq(nuisance, features, rcond=None)[0]
        _, _, right = np.linalg.svd(task_module, full_matrices=False)
        width = max(2, min(6, right.shape[0]))
        compressed = task_module @ right[:width].T
        return compressed / np.maximum(np.linalg.norm(compressed, axis=1, keepdims=True), 1e-12)
    compressed = _cached("marc", data, modular_features)
    query = compressed[np.asarray(history[-12:])].mean(0)
    return compressed @ query + 0.20 * data.transition[history[-1]]


def score_rankup(data, history):
    def high_rank():
        features = data.sequences.features.astype(np.float64)
        rng = np.random.default_rng(17878)
        views = []
        for _ in range(3):
            permuted = features[:, rng.permutation(features.shape[1])]
            views.append(np.tanh(permuted @ rng.normal(0.0, 0.3, (features.shape[1], 8))))
        output = np.concatenate(views, axis=1)
        return output - output.mean(0, keepdims=True)
    representations = _cached("rankup", data, high_rank)
    query = representations[np.asarray(history[-16:])].mean(0)
    global_token = representations.mean(0)
    return representations @ (query + 0.15 * global_token) + 0.10 * data.popularity


def score_sid_coord(data, history):
    codes = _cached("sid-coord", data, lambda: hierarchical_codes(data.sequences.features, levels=3, width=8, seed=14))
    recent = np.asarray(history[-12:])
    sid_match = sum((codes[:, None, level] == codes[recent][None, :, level]).mean(1) / (level + 1) for level in range(3))
    hid = data.transition[recent[-1]]
    tail_gate = 1.0 - _rank01(data.popularity)
    interest = data.cosine[recent].mean(0)
    return (1.0 - 0.65 * tail_gate) * hid + 0.65 * tail_gate * sid_match + 0.25 * interest


def score_rclrec(data, history):
    values = np.asarray(history[-24:])
    target_proxy = data.transition[values[-1]]
    relevance = target_proxy[values] + data.popularity[values]
    curriculum = values[np.argsort(-relevance)[: min(8, len(values))]][::-1]
    weights = np.linspace(1.0, 0.35, len(curriculum))
    weights /= weights.sum()
    intermediate = (data.cosine[curriculum] * weights[:, None]).sum(0)
    return intermediate + 0.35 * target_proxy


def score_tagllm(data, history):
    recent = np.asarray(history[-12:])
    codes = _cached("tagllm", data, lambda: hierarchical_codes(data.sequences.features, levels=4, width=12, seed=23))
    handbook = np.zeros((4, 12), dtype=np.float64)
    for level in range(4):
        np.add.at(handbook[level], codes[recent, level], np.linspace(0.5, 1.0, len(recent)))
    tag_score = sum(handbook[level][codes[:, level]] / (level + 1) for level in range(4))
    fine_grained = data.cosine[recent[-4:]].mean(0)
    return tag_score + 0.40 * fine_grained + 0.10 * data.transition[recent[-1]]


def score_genfacet(data, history):
    recent = np.asarray(history[-10:])
    facet_counts = np.bincount(data.domains[recent], minlength=int(data.domains.max()) + 1)
    facet = np.log1p(facet_counts[data.domains])
    rewritten_intent = 0.55 * data.cosine[recent].mean(0) + 0.45 * data.transition[recent[-1]]
    satisfaction = 1.0 + 0.25 * _rank01(rewritten_intent)
    return satisfaction * rewritten_intent + 0.30 * facet


def score_cgr(data, history):
    relevance = _rank01(base_scores(data, history))
    remaining = np.ones(data.item_count, dtype=bool)
    output = np.full(data.item_count, -2.0)
    domain_count = np.zeros(int(data.domains.max()) + 1, dtype=np.int64)
    slate = min(20, data.item_count)
    for position in range(slate):
        penalty = 0.22 * domain_count[data.domains] / max(position, 1)
        reward = relevance - penalty
        reward[~remaining] = -np.inf
        chosen = int(np.argmax(reward))
        output[chosen] = slate - position + reward[chosen] * 0.01
        remaining[chosen] = False
        domain_count[data.domains[chosen]] += 1
    output[remaining] += relevance[remaining]
    return output


def score_hpgr(data, history):
    values = np.asarray(history[-24:])
    sessions = np.array_split(values, min(4, len(values)))
    query = data.sequences.features[values[-1]]
    session_vectors = np.stack([data.sequences.features[session].mean(0) for session in sessions])
    session_weight = np.exp(session_vectors @ query)
    session_weight /= session_weight.sum()
    hierarchy = (session_vectors * session_weight[:, None]).sum(0)
    sparse = data.sequences.features @ hierarchy
    threshold = np.quantile(sparse, 0.70)
    return np.where(sparse >= threshold, sparse, 0.15 * sparse) + 0.20 * data.transition[values[-1]]


def score_climber_pilot(data, history):
    recent = np.asarray(history[-12:])
    one_step = data.transition[recent[-1]]
    two_step = one_step @ data.transition
    three_step = two_step @ data.transition
    preferred = np.bincount(data.domains[recent[-6:]], minlength=int(data.domains.max()) + 1)
    instruction = preferred[data.domains] / max(preferred.max(), 1)
    return 0.45 * one_step + 0.35 * two_step + 0.20 * three_step + 0.25 * instruction


def score_rolegen(data, history):
    recent = np.asarray(history[-16:])
    direct = data.transition[recent[-1]]
    instrumental = direct @ data.transition
    counterfactual = data.transition[recent[-4:]].mean(0)
    role_gain = instrumental - counterfactual
    dormant_novelty = 1.0 - _rank01(data.popularity)
    return direct + 0.55 * role_gain + 0.20 * dormant_novelty + 0.15 * data.cosine[recent].mean(0)


SCORERS = {
    "marc": score_marc,
    "rankup": score_rankup,
    "sid_coord": score_sid_coord,
    "rclrec": score_rclrec,
    "tagllm": score_tagllm,
    "genfacet": score_genfacet,
    "cgr": score_cgr,
    "hpgr": score_hpgr,
    "climber_pilot": score_climber_pilot,
    "rolegen": score_rolegen,
}


def diagnostics(key: str, data, history) -> dict[str, float]:
    scores = SCORERS[key](data, history)
    result: dict[str, float] = {"finite_scores": int(np.isfinite(scores).sum()), "score_std": float(np.std(scores))}
    details = {
        "marc": {"compressed_modules": 2, "task_decoupling_constraints": 1},
        "rankup": {"permuted_embedding_views": 3, "global_tokens": 1},
        "sid_coord": {"semantic_id_levels": 3, "coordination_paths": 3},
        "rclrec": {"reverse_curriculum_items": min(8, len(history)), "intermediate_supervision": 1},
        "tagllm": {"tag_levels": 4, "interest_handbooks": 1},
        "genfacet": {"generative_tasks": 2, "preference_alignment_heads": 1},
        "cgr": {"bounded_decoder_steps": min(20, data.item_count), "constraint_channels": int(data.domains.max()) + 1},
        "hpgr": {"hierarchical_sessions": min(4, len(history)), "sparse_attention_keep_ratio": 0.3},
        "climber_pilot": {"foresight_horizons": 3, "instruction_channels": int(data.domains.max()) + 1},
        "rolegen": {"functional_roles": 2, "counterfactual_paths": 1},
    }
    return result | details[key]


def reproduce_h05(key: str, dataset_dir: Path, seed: int = 42) -> dict:
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
            online_ab=(OnlineABEvidence(product, metric, lift, traffic, source_url=f"https://arxiv.org/html/{paper['arxiv_id']}v1", source_location=location, retrieved_at="2026-09-05"),),
        ),
        run=lambda dataset_dir, seed=42: reproduce_h05(key, dataset_dir, seed),
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
