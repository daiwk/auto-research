"""Register the public-data MuSeR mechanism experiment."""

from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

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


ADAPTER = register(adapter_from_spec(key="muser", run=reproduce, render=render))
