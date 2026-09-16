"""Industrial recommendation mechanisms reviewed through 2026-09-16."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from .industrial_2026 import base_scores, evaluate, load_industrial_data, ridge, softmax, summary_result, tune_blend
from .industrial_2026 import render_standard


PAPERS = {
    "gese": {
        "arxiv_id": "2609.15094", "title": "Generate to Explore, Select to Exploit: Aligning LLM-based Headline Generation with Personalized Recommendation",
        "organization": "Baidu", "published": "2026-09-14",
        "topics": ("presentation-layer", "headline-generation", "gspo", "bandit-selection"),
        "paper_results": {"ctr_lift_percent": 2.57, "dwell_time_lift_percent": 0.87},
        "evidence": ("commercial information feed with 100M+ DAU", "CTR", 2.57, "production online A/B", "Section 4.2; Table 2"),
        "omitted": ("Baidu private headline logs", "Qwen3-14B SFT/GSPO checkpoint", "production feedback selector"),
        # Presentation-layer generation is not an executable RankMixer axis.
        # Keep the adapter runnable without advertising a registry-only evolve operator.
        "operators": (),
    },
    "lazformer": {
        "arxiv_id": "2609.14978", "title": "LazFormer: Scaling Transformers for Industrial Recommendation via Transferable Generative Pre-training",
        "organization": "Alibaba International Digital Commerce Group", "published": "2026-09-14",
        "topics": ("ranking", "generative-pretraining", "residual-adapter", "hybrid-sparse-attention"),
        "paper_results": {"ipv_lift_percent": 5.21, "orders_lift_percent": 3.38, "buyers_lift_percent": 3.70, "gmv_lift_percent": 9.85},
        "evidence": ("large-scale e-commerce homepage ranking", "IPV", 5.21, "two-week production A/B", "Section 4.7; Table 7"),
        "omitted": ("Alibaba private homepage logs", "production five-layer Transformer checkpoint", "A10 serving stack"),
        # The public-data adapter executes the transferable pretrain/residual
        # mechanism, but it is not wired into the RankMixer trainer yet.
        "operators": (),
    },
}


def gese_candidate_scores(data, history, candidates: int = 5):
    """Diversity-aware exploration followed by contextual exploitation."""
    features = data.sequences.features.astype(np.float64)
    query = features[np.asarray(history[-12:], dtype=np.int64)].mean(0)
    relevance = features @ query
    selected = [int(np.argmax(relevance))]
    while len(selected) < candidates:
        diversity = 1.0 - np.max(features @ features[selected].T, axis=1)
        fidelity = np.clip(features @ query, -1.0, 1.0)
        reward = 0.55 * relevance + 0.30 * diversity + 0.15 * fidelity
        reward[selected] = -np.inf
        selected.append(int(np.argmax(reward)))
    # Public sequence recency is the auditable substitute for instantaneous
    # production context used by the online selector.
    recent = features[np.asarray(history[-3:], dtype=np.int64)].mean(0)
    selector = features[selected] @ recent
    scores = np.full(len(features), relevance.min() - 1.0)
    scores[selected] = relevance[selected] + 0.35 * selector
    return scores, selected


def coarse_to_fine_tokens(features, history, recent: int = 8):
    sequence = np.asarray(history, dtype=np.int64)
    old, tail = sequence[:-recent], sequence[-recent:]
    coarse = [features[group].mean(0) for group in np.array_split(old, max(1, min(4, len(old)))) if len(group)]
    return np.stack(coarse + [features[index] for index in tail])


def lazformer_alignment(data):
    """Generative pretraining map plus ranking-specific residual adapter."""
    features = data.sequences.features.astype(np.float64)
    source, target = [], []
    for history, positive in zip(data.sequences.train, data.sequences.validation):
        source.append(coarse_to_fine_tokens(features, history).mean(0))
        target.append(features[positive])
    pretrained = ridge(np.asarray(source), np.asarray(target), regularization=0.2)
    residual = ridge(np.asarray(source), np.asarray(target) - np.asarray(source) @ pretrained, regularization=0.5)
    return pretrained, residual


def lazformer_scores(data, history, pretrained, residual):
    tokens = coarse_to_fine_tokens(data.sequences.features.astype(np.float64), history)
    request = data.sequences.features[np.asarray(history[-3:], dtype=np.int64)].mean(0)
    hybrid = tokens @ pretrained + 0.5 * tokens @ residual
    attention = softmax(hybrid @ request)
    representation = attention @ hybrid
    return data.sequences.features @ representation


def reproduce(key: str, dataset_dir: Path, seed: int = 42):
    data = load_industrial_data(dataset_dir)
    baseline_scorer = lambda history: base_scores(data, history)
    if key == "gese":
        raw_method = lambda history: gese_candidate_scores(data, history)[0]
        _, selected = gese_candidate_scores(data, data.sequences.train[0])
        stages = {"candidate_set_size": len(selected), "setwise_diversity_reward": True, "contextual_selector": True}
        scope = "公开内容向量执行集合级多样性探索、faithfulness 约束和上下文选择；不把候选标题向量冒充 Qwen3-14B 生成或线上反馈。"
    else:
        pretrained, residual = lazformer_alignment(data)
        raw_method = lambda history: lazformer_scores(data, history, pretrained, residual)
        sample = coarse_to_fine_tokens(data.sequences.features, data.sequences.train[0])
        stages = {"compressed_tokens": len(sample), "generative_pretraining_map": True, "residual_adapter": True, "hybrid_sparse_attention": True}
        scope = "公开序列执行生成式预训练映射、ranking residual adapter、近密远疏压缩和 request-aware pooling；不复刻生产 Transformer 与 A10 serving。"
    alpha, method_scorer, validation = tune_blend(data, baseline_scorer, raw_method)
    stages.update(validation_only_alpha=alpha, validation_metrics=validation)
    row = PAPERS[key]
    result = summary_result(key=key, paper={"arxiv_id": row["arxiv_id"], "title": row["title"], "url": f"https://arxiv.org/abs/{row['arxiv_id']}", "organization": row["organization"]}, data=data, baseline_name="transition + content + popularity", method_name=f"{key} executable mechanism", baseline=evaluate(data, baseline_scorer), proposed=evaluate(data, method_scorer), stages=stages, paper_results=row["paper_results"], scope=scope)
    result["manifest_ref"] = f"reproduction:{key}"
    result["setup"]["seed"] = seed
    return result


def make_adapter(key: str) -> ReproductionAdapter:
    row = PAPERS[key]
    product, metric, lift, traffic, location = row["evidence"]
    online = [OnlineABEvidence(product, metric, lift, traffic, source_url=f"https://arxiv.org/html/{row['arxiv_id']}v1", source_location=location, experiment_duration="two weeks" if key == "lazformer" else None, retrieved_at="2026-09-16")]
    if key == "gese":
        online.append(OnlineABEvidence(product, "dwell time", 0.87, traffic, source_url="https://arxiv.org/html/2609.15094v1", source_location=location, retrieved_at="2026-09-16"))
    if key == "lazformer":
        for metric2, lift2 in (("orders", 3.38), ("buyers", 3.70), ("GMV", 9.85)):
            online.append(OnlineABEvidence(product, metric2, lift2, traffic, source_url="https://arxiv.org/html/2609.14978v1", source_location=location, experiment_duration="two weeks", retrieved_at="2026-09-16"))
    return ReproductionAdapter(
        key=key,
        paper=PaperMetadata(arxiv_id=row["arxiv_id"], title=row["title"], url=f"https://arxiv.org/abs/{row['arxiv_id']}", track="recommendation", organization=row["organization"], published=row["published"], publication_label="arXiv v1", topics=row["topics"], online_ab=tuple(online)),
        run=lambda dataset_dir, seed=42: reproduce(key, dataset_dir, seed), render=render_standard,
        fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=row["omitted"], evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K",), baseline="transition + content + popularity", metrics=("hit_at_10", "ndcg_at_10", "fresh_hit_at_10", "head_share_at_10"),
        evolve_operators=row["operators"], default_seeds=(42, 43, 44), budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
    )
