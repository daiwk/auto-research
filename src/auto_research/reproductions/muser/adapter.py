"""Register the public-data MuSeR mechanism experiment."""

from __future__ import annotations

from ..base import (
    EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce


def render(result: dict) -> str:
    lines = [
        "# MuSeR 本地公开数据实验", "",
        "KuaiRand-Pure 逐用户留末两次正反馈；每组同训练步数、相同负采样与切分。", "",
        "| 配置 | Validation Recall@10 | Test Recall@10 | Test NDCG@10 |",
        "|---|---:|---:|---:|",
    ]
    for name, value in result["variants"].items():
        lines.append(
            f"| {name} | {value['validation']['recall_at_10']:.4f} | "
            f"{value['test']['recall_at_10']:.4f} | "
            f"{value['test']['ndcg_at_10']:.4f} |"
        )
    return "\n".join(lines + ["", "## 边界", "", result["scope"], ""])


ADAPTER = register(ReproductionAdapter(
    key="muser",
    paper=PaperMetadata(
        arxiv_id="2609.23677",
        title="MuSeR: Scalable Long-sequence Recommendation with Multi-interest Modeling",
        url="https://arxiv.org/abs/2609.23677",
        track="recommendation",
        organization="Baidu",
        published="2026-09-20",
        publication_label="arXiv v1",
        topics=("retrieval", "long-sequence", "multi-interest"),
        online_ab=(OnlineABEvidence(
            "Baidu APP", "daily active users", 0.26,
            "online A/B", source_url="https://arxiv.org/html/2609.23677v1",
            source_location="Abstract and Introduction", significance="p<0.05",
            retrieved_at="2026-09-26",
        ),),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=(
        "ERNIE-generated summaries, ERNIE-Speed distillation, and BGE multimodal embeddings",
        "asynchronous representation refresh, HNSW retrieval, and Baidu online traffic",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("KuaiRand-Pure",),
    baseline="recent-only single-interest ID retrieval",
    metrics=(
        "variants.muser.test.recall_at_10",
        "variants.recent_single_id.test.recall_at_10",
    ),
    default_seeds=(42, 43, 44),
    budget="800 steps each; full catalog; per-user last-two holdout",
    device_capabilities=("cpu",),
    infer_device_capabilities=False,
))
