"""Register Google Lightweight Ranking Heads as an executable public-data adapter."""

from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

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


ADAPTER = register(adapter_from_spec(key="light-heads", run=reproduce, render=render))
