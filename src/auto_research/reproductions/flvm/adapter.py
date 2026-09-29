"""Register Google's FLVM as a public-data concept diagnostic."""

from __future__ import annotations

from ..base import (
    EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce


def render(result: dict) -> str:
    lines = ["# FLVM 公开数据诊断", "", "KuaiRand-Pure 的时间切分和真实曝光反馈。", "",
             "| 模型 | Validation Like AP | Test Like AP | Test Hate AP |",
             "|---|---:|---:|---:|"]
    for name, variant in result["variants"].items():
        validation = variant["validation"]["signals"]["is_like"]["average_precision"]
        like = variant["test"]["signals"]["is_like"]["average_precision"]
        hate = variant["test"]["signals"]["is_hate"]["average_precision"]
        lines.append(f"| {name} | {validation:.5f} | {like:.5f} | {hate:.5f} |")
    return "\n".join(lines + ["", "## 边界", "", result["scope"], ""])


ADAPTER = register(ReproductionAdapter(
    key="flvm",
    paper=PaperMetadata(
        arxiv_id="2609.32839",
        title="Mend the Measurement Gap: Latent User Preference Modeling for Short-Form Video Recommendation",
        url="https://arxiv.org/abs/2609.32839",
        track="recommendation",
        organization="Google / YouTube",
        published="2026-09-26",
        publication_label="arXiv v1",
        topics=("ranking", "multi-task", "feedback-debiasing"),
        online_ab=(OnlineABEvidence(
            "YouTube Shorts", "primary viewer enjoyment", 2.67,
            "14-day online A/B", source_url="https://arxiv.org/html/2609.32839",
            source_location="Section 4, online A/B paragraph", retrieved_at="2026-09-29",
        ),),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=(
        "private YouTube satisfaction surveys, serving features and production ranker",
        "production prescoring integration, traffic and online A/B",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("KuaiRand-Pure",),
    baseline="independently trained shared-trunk multitask control on identical public signals",
    metrics=("variants.flvm.test.signals.is_like.average_precision",
             "variants.flvm.test.signals.is_hate.average_precision"),
    default_seeds=(42, 43, 44),
    budget="300 updates/model/seed; all KuaiRand-Pure impressions; chronological 70/15/15",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
