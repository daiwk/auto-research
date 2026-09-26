"""Google Music discovery: offline LLM profiles with safe cached serving."""

from __future__ import annotations

from .experiment import reproduce
from ..base import (
    EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register


def render(result: dict) -> str:
    setup, metrics = result["setup"], result["results"]
    return "\n".join([
        "# Google Music artist discovery 公开数据实验", "",
        f"HetRec Last.fm 2K，{setup['split']}，{setup['users']} 位用户；"
        f"生成器 {setup['model']}（{setup['device']}）。", "",
        "| 指标 | 结果 |", "|---|---:|",
        f"| CF Hit@5 | {metrics['cf_hit_at_5']:.4f} |",
        f"| LLM 有效提名 Hit@5 | {metrics['generated_hit_at_5']:.4f} |",
        f"| 缓存加回退 Hit@5 | {metrics['served_hit_at_5_with_fallback']:.4f} |",
        f"| 候选目录与理由审核通过率 | {metrics['catalog_grounded_share']:.4f} |",
        f"| 原 CF 候选解释覆盖率 | {metrics['annotation_coverage_at_5']:.4f} |",
        f"| 至少一条有效提名的用户占比 | {metrics['cache_coverage']:.4f} |",
        "", "## 复现边界", "", result["scope"], "",
    ])


ADAPTER = register(ReproductionAdapter(
    key="music-rationales",
    paper=PaperMetadata(
        arxiv_id="2609.23877",
        title="Explainable Recommendations at Scale: LLM Rationales for YouTube Music Artist Discovery",
        url="https://arxiv.org/abs/2609.23877",
        track="recommendation",
        organization="Google",
        published="2026-09-20",
        publication_label="arXiv v1",
        topics=("music-discovery", "llm-rationale", "offline-online-decoupling"),
        online_ab=(OnlineABEvidence(
            "YouTube Music", "YDD shelf-level engagement", 22.43,
            "large-scale online multi-arm holdback A/B",
            source_url="https://arxiv.org/html/2609.23877v1",
            source_location="Section 4.3, Table 1", significance="95% CI [16.93%, 27.93%]",
            retrieved_at="2026-09-27",
        ),),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=(
        "private Gemini model, music knowledge graph and LLM-as-a-Judge",
        "YouTube Music retrieval fleet, event-driven refresh and multi-arm online A/B",
        "public Last.fm has neither music exposure nor rationale engagement labels",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("HetRec Last.fm 2K",),
    baseline="training-only collaborative filtering artist candidates",
    metrics=("results.cf_hit_at_5", "results.generated_hit_at_5",
             "results.served_hit_at_5_with_fallback", "results.catalog_grounded_share",
             "results.annotation_coverage_at_5", "results.cache_coverage"),
    default_seeds=(42,),
    budget="default 20 validation users; published GPU audit 100 validation and 100 test users; at most 5 nominations",
    device_capabilities=("cpu", "cuda"),
    infer_device_capabilities=False,
    requires_gpu_validation=True,
    gpu_validation_artifact="docs/gpu-validations/music-rationales-a100-20260927.json",
))
