"""KuaFu item-level semantic compression, with explicit public-data limits."""

from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

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


ADAPTER = register(adapter_from_spec(key="kuafu", run=reproduce, render=render))
