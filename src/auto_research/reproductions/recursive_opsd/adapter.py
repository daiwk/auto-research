"""Paper metadata and explicit fidelity boundary for Meta DCE+SRCL."""

from __future__ import annotations

from .experiment import reproduce
from ..base import EvaluationTier, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register


def render(result: dict) -> str:
    before = result["baseline_validation"]
    after = result["final_validation"]
    return "\n".join([
        "# Recursive OPSD 公开数学题诊断", "",
        "> Qwen3-4B + 极小 GSM8K 样本仅验证 DCE/SRCL 可执行；不是论文性能复现。", "",
        "| 指标 | 训练前验证 | 训练后验证 |", "|---|---:|---:|",
        f"| Accuracy | {before['accuracy']:.4f} | {after['accuracy']:.4f} |",
        f"| 平均输出 token | {before['mean_generated_tokens']:.1f} | {after['mean_generated_tokens']:.1f} |",
        "", f"真实参数变化 L2：{result['adapter_parameter_delta_l2']:.6f}。", "",
    ])


ADAPTER = register(ReproductionAdapter(
    key="recursive-opsd",
    paper=PaperMetadata(
        arxiv_id="2609.30652",
        title="Recursive Self-Improvement via On-Policy Distillation for Reasoning",
        url="https://arxiv.org/abs/2609.30652",
        track="llm",
        organization="Meta AI / University of California, Riverside",
        published="2026-09-25",
        publication_label="arXiv v1",
        topics=("On-policy self-distillation", "DCE", "SRCL", "reasoning"),
    ),
    run=reproduce,
    render=render,
    fidelity=ReproductionFidelity.CONCEPT_DEMO,
    omitted_core_components=(
        "14,717 OpenThoughts training problems and 200-step rank-128 LoRA protocol",
        "AIME24/25/26 and HMMT25 Average@12 with 32K generation budget",
        "paper-matched SFT, GRPO, OPSD and test-time scaling baselines",
    ),
    evaluation_tier=EvaluationTier.PUBLIC_DATASET,
    datasets=("official GSM8K train/test",),
    baseline="pre-update same checkpoint plus two-step fixed-teacher and DCE-only controls",
    metrics=("baseline_validation.accuracy", "final_validation.accuracy",
             "final_test.accuracy", "adapter_parameter_delta_l2"),
    default_seeds=(42,),
    budget="2 updates; 4 train + 2 validation + 2 test problems; 192 tokens",
    device_capabilities=("cuda",),
    infer_device_capabilities=False,
    requires_gpu_validation=True,
    gpu_validation_artifact="docs/gpu-validations/recursive-opsd-a100-20260929.json",
))
