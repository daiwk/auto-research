"""Register Google Lightweight Ranking Heads as an executable public-data adapter."""

from __future__ import annotations

from .experiment import reproduce
from ..base import (
    EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register


def render(result: dict) -> str:
    lines = [
        "# Lightweight Ranking Heads 本地实验", "",
        "MovieLens 100K 显式评分，逐用户时间切分；rating≥4 为原任务，rating=5 为新任务。",
        "", "| 配置 | Validation main AUC | Validation light AUC | Test main AUC | Test light AUC |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, metrics in result["variants"].items():
        validation, test = metrics["validation"], metrics["test"]
        lines.append(
            f"| {name} | {validation['main_auc']:.4f} | {validation['light_auc']:.4f} | "
            f"{test['main_auc']:.4f} | {test['light_auc']:.4f} |"
        )
    return "\n".join(lines + ["", "## 复现边界", "", result["scope"], ""])


ADAPTER = register(ReproductionAdapter(
    key="light-heads",
    paper=PaperMetadata(
        arxiv_id="2609.25433",
        title="Lightweight Ranking Heads: Accelerating Multi-Task Experimentation in Production Recommender Systems",
        url="https://arxiv.org/abs/2609.25433",
        track="recommendation",
        organization="Google",
        published="2026-09-21",
        publication_label="arXiv v1",
        topics=("ranking", "multi-task-learning", "lightweight-heads"),
        online_ab=(OnlineABEvidence(
            "YouTube", "top-line engagement", 0.03,
            "production A/B experiment",
            source_url="https://arxiv.org/html/2609.25433v1",
            source_location="Section 5.2", significance="p<0.05",
            retrieved_at="2026-09-26",
        ),),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=(
        "YouTube online continuous-training fleet and shared configuration service",
        "private multi-task labels, downstream reward model and serving dependencies",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MovieLens 100K",),
    baseline="frozen shared ranker with main rating task",
    metrics=(
        "variants.light_head.test.main_auc", "variants.light_head.test.light_auc",
        "variants.no_reset.test.light_auc", "variants.no_stop_gradient.test.main_auc",
    ),
    default_seeds=(42, 43, 44),
    budget="120 shared steps + 80 new-head steps per variant; chronological 70/15/15",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
