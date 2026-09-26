"""Register the scaled public-data UNIQUE mechanism experiment."""

from __future__ import annotations

from ..base import (
    EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce


def render(result: dict) -> str:
    lines = ["# UNIQUE 本地公开数据实验", "",
             "KuaiRand-Pure 曝光时间留末两条；CTR-AUC 仅对真实曝光计算。", "",
             "| 配置 | Validation CTR-AUC | Test CTR-AUC | Test Code Recall@4 |",
             "|---|---:|---:|---:|"]
    for name, value in result["variants"].items():
        recall = value["test"].get("candidate_recall_at_4_codes")
        recall_text = f"{recall:.4f}" if recall is not None else "不适用"
        lines.append(f"| {name} | {value['validation']['ctr_auc']:.4f} | "
                     f"{value['test']['ctr_auc']:.4f} | {recall_text} |")
    return "\n".join(lines + ["", "## 边界", "", result["scope"], ""])


ADAPTER = register(ReproductionAdapter(
    key="unique",
    paper=PaperMetadata(
        arxiv_id="2609.23718",
        title="UNIQUE: A Unified Retrieval and Ranking System for Large-Scale Feed Recommendation",
        url="https://arxiv.org/abs/2609.23718",
        track="recommendation",
        organization="Beihang University",
        published="2026-09-20",
        publication_label="arXiv v1",
        topics=("retrieval", "ranking", "generative-recommendation"),
        online_ab=(OnlineABEvidence(
            "Mobile Baidu", "total watch duration", 0.96, "full-traffic online A/B",
            source_url="https://arxiv.org/html/2609.23718v1",
            source_location="Abstract and Section 4.4", retrieved_at="2026-09-26",
        ),),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=(
        "production heterogeneous features and task-specific multi-head feedback objectives",
        "full Mobile Baidu traffic, infrastructure and online A/B",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("KuaiRand-Pure",),
    baseline="same early-fusion ranker without joint code generation",
    metrics=("variants.unique_scaled.test.ctr_auc",
             "variants.unique_scaled.test.candidate_recall_at_4_codes"),
    default_seeds=(42, 43, 44),
    budget="300 steps per variant; 500k raw exposures; chronological holdout",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
