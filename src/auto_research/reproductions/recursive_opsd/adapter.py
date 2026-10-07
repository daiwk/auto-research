"""Paper metadata and explicit fidelity boundary for Meta DCE+SRCL."""

from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

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


ADAPTER = register(adapter_from_spec(key="recursive-opsd", run=reproduce, render=render))
