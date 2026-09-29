"""KuaFu item-level semantic compression, with explicit public-data limits."""

from __future__ import annotations

from .experiment import reproduce
from ..base import (
    EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register


def render(result: dict) -> str:
    metrics = result["dev_metrics"]
    return "\n".join([
        "# KuaFu 公开 MRQA 诊断", "",
        "> 这是 32 题公开数据的小规模诊断，不是腾讯工业系统或论文效果复现。", "",
        "| 输入路径 | Dev EM | Dev F1 |", "|---|---:|---:|",
        *(
            f"| {name} | {values['em']:.4f} | {values['f1']:.4f} |"
            for name, values in metrics.items()
        ),
        "", result["control_caveat"], "",
    ])


ADAPTER = register(ReproductionAdapter(
    key="kuafu",
    paper=PaperMetadata(
        arxiv_id="2609.31045",
        title="KuaFu: Compressing Long User Behavior into Understanding at Billion Scale",
        url="https://arxiv.org/abs/2609.31045",
        track="recommendation",
        organization="Tencent",
        published="2026-09-25",
        publication_label="arXiv v1",
        topics=("long-behavior", "item-compression", "hallucination-aware-rl"),
        online_ab=(OnlineABEvidence(
            product="Tencent advertising and recommendation",
            metric="overall GMV", lift_percent=1.37,
            traffic="visitor-randomized; retained 5% holdout after full rollout",
            source_url="https://arxiv.org/html/2609.31045v1",
            source_location="Section 4.8",
            experiment_duration="four-week ramp plus ten-month holdout",
            significance="95% CI [0.71%, 2.03%]",
            retrieved_at="2026-09-29",
        ),),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=(
        "private two-year behavior log and four production profiling tasks",
        "industrial-scale curriculum/data volume and RecBench comparison",
        "effective hallucination RL update and Tencent online A/B",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("MRQA 2019 SQuAD train/dev",),
    baseline="same-decoder raw head/tail token-budget input ablations, not separately trained baselines",
    metrics=("dev_metrics.compressed.em", "dev_metrics.compressed.f1",
             "dev_metrics.raw_head_equal_tokens.f1",
             "dev_metrics.raw_tail_equal_tokens.f1"),
    default_seeds=(42,),
    budget="default 32 train contexts, 32 dev contexts; 4 items x 24 tokens; 2 cache tokens/item",
    device_capabilities=("cuda",),
    infer_device_capabilities=False,
    requires_gpu_validation=True,
    gpu_validation_artifact="docs/gpu-validations/kuafu-a100-independent-control-20260929.json",
))
