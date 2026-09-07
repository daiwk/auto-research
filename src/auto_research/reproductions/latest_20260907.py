"""Executable public-data proxies for the 2026-09-07 discovery batch."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from .industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .industrial_2026 import render_standard as render


PAPERS = {
    "allecompanion": {
        "arxiv_id": "2609.05063",
        "title": "Beyond Co-purchase Relation: Evolution of Complementary Recommendations at Allegro",
        "organization": "Allegro.com",
        "published": "2026-09-04",
        "publication_label": "RecSys 2026",
        "topics": ("complementary-recommendation", "two-tower", "category-adapter", "e-commerce"),
        "operator": "context:complementary-category-adapter",
        "paper_results": {"web_organic_gmv_lift_percent": 8.05, "app_organic_gmv_lift_percent": 9.35, "web_cart_gmv_lift_percent": 21.25, "app_cart_gmv_lift_percent": 15.73},
        "evidence": ("Allegro product and cart placements", "attributed GMV", 21.25, "two-week tests routed over 100% platform traffic", "Section 4.4, Table 5"),
        "omitted": ("private 90-day Allegro transaction log", "production Faiss index", "ComCat expert rules"),
    },
    "autolr": {
        "arxiv_id": "2609.04871",
        "title": "AutoLR: Automating the Path from Research to Launch Review in Industrial Recommender Systems",
        "organization": "NetEase, Inc.",
        "published": "2026-09-04",
        "publication_label": "NetEase technical report",
        "topics": ("auto-research", "experiment-controller", "launch-review", "industrial-recommendation"),
        "operator": "controller:autolr-evidence-council",
        "paper_results": {"completed_offline_evaluations": 1586, "canonical_ledger_records": 3289, "launch_reviews": 9, "content_time_lift_sum_percent": 10.83},
        "evidence": ("NetEase DASHEN feed and immersive-video feed", "content-consumption time", 10.83, "nine Launch Review records with online A/B and production decisions", "Section 5.2, Table 1"),
        "omitted": ("private DASHEN repository", "production experiment ledger", "online admission and Launch Review authority"),
    },
}


def _softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - values.max()
    exp = np.exp(shifted)
    return exp / np.maximum(exp.sum(), 1e-12)


def score_allecompanion(data, history):
    recent = np.asarray(history[-24:])
    query = data.sequences.features[recent].mean(axis=0)
    content = data.sequences.features @ query
    category_signal = np.bincount(data.domains[recent], minlength=int(data.domains.max()) + 1).astype(float)
    category_signal = _softmax(category_signal)
    category_adapter = category_signal[data.domains]
    # Category reconstruction is represented by agreement between the projected
    # query and the candidate's category-conditioned content score.
    reconstruction = category_adapter * (content - content.min() + 1e-6)
    return 0.55 * data.cosine[recent].mean(0) + 0.30 * reconstruction + 0.15 * data.transition[recent[-1]]


def score_autolr(data, history):
    recent = np.asarray(history[-24:])
    proposals = np.stack((
        data.transition[recent[-1]],
        data.cosine[recent].mean(0),
        data.popularity,
    ))
    normalized = (proposals - proposals.mean(axis=1, keepdims=True)) / (proposals.std(axis=1, keepdims=True) + 1e-6)
    council = normalized.mean(axis=0)
    disagreement = normalized.std(axis=0)
    evidence = np.asarray((0.45, 0.40, 0.15)) @ normalized
    # Deterministic exploration/exploitation allocation: evidence is the
    # exploitation score and disagreement supplies a bounded exploration bonus.
    return 0.65 * evidence + 0.25 * council + 0.10 * disagreement


SCORERS = {"allecompanion": score_allecompanion, "autolr": score_autolr}


def reproduce(key: str, dataset_dir: Path, seed: int = 42) -> dict:
    del seed
    data = load_industrial_data(dataset_dir)
    baseline_scorer = lambda history: base_scores(data, history)
    method_scorer = lambda history: SCORERS[key](data, history)
    alpha, blended, _ = tune_blend(data, baseline_scorer, method_scorer)
    baseline = evaluate(data, baseline_scorer)
    proposed = evaluate(data, blended)
    row = PAPERS[key]
    result = summary_result(
        key=key,
        paper={"arxiv_id": row["arxiv_id"], "title": row["title"], "url": f"https://arxiv.org/abs/{row['arxiv_id']}", "organization": row["organization"]},
        data=data,
        baseline_name="transition + content + popularity",
        method_name=f"{key} core mechanism (validation blend={alpha:.1f})",
        baseline=baseline,
        proposed=proposed,
        stages={"finite_scores": int(np.isfinite(method_scorer(data.sequences.train[0])).sum()), "mechanism_paths": 3},
        paper_results=row["paper_results"],
        scope="公开 MovieLens 上的核心机制验证；不复刻私有日志、生产 checkpoint 或线上系统。",
    )
    result["manifest_ref"] = f"reproduction:{key}"
    return result


def make_adapter(key: str) -> ReproductionAdapter:
    row = PAPERS[key]
    product, metric, lift, traffic, location = row["evidence"]
    return ReproductionAdapter(
        key=key,
        paper=PaperMetadata(
            arxiv_id=row["arxiv_id"], title=row["title"], url=f"https://arxiv.org/abs/{row['arxiv_id']}",
            track="recommendation", organization=row["organization"], published=row["published"],
            publication_label=row["publication_label"], topics=row["topics"],
            online_ab=(OnlineABEvidence(product, metric, lift, traffic, source_url=f"https://arxiv.org/html/{row['arxiv_id']}", source_location=location, experiment_duration="two weeks" if key == "allecompanion" else None, retrieved_at="2026-09-07"),),
        ),
        run=lambda dataset_dir, seed=42: reproduce(key, dataset_dir, seed), render=render,
        fidelity=ReproductionFidelity.CORE_MECHANISM, omitted_core_components=row["omitted"],
        evaluation_tier=EvaluationTier.PUBLIC_DATASET, datasets=("MovieLens 100K",),
        baseline="transition + content + popularity", metrics=("hit_at_10", "ndcg_at_10", "fresh_hit_at_10", "head_share_at_10"),
        evolve_operators=(row["operator"],), default_seeds=(42, 43, 44),
        budget="220 users / 360 items; validation-only blend selection", device_capabilities=("cpu",), infer_device_capabilities=False,
    )
