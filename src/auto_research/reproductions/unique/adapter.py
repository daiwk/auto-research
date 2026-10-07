"""Register the scaled public-data UNIQUE mechanism experiment."""

from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

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


ADAPTER = register(adapter_from_spec(key="unique", run=reproduce, render=render))
