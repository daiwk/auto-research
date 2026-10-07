"""Register Google's FLVM as a public-data concept diagnostic."""

from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

from ..base import (
    EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter,
    ReproductionFidelity,
)
from ..registry import register
from .experiment import reproduce


def render(result: dict) -> str:
    lines = ["# FLVM 公开数据诊断", "", "KuaiRand-Pure 的时间切分和真实曝光反馈。", "",
             "| 模型 | Validation Like AP | Test Like AP | Test Hate AP |",
             "|---|---:|---:|---:|"]
    for name, variant in result["variants"].items():
        validation = variant["validation"]["signals"]["is_like"]["average_precision"]
        like = variant["test"]["signals"]["is_like"]["average_precision"]
        hate = variant["test"]["signals"]["is_hate"]["average_precision"]
        lines.append(f"| {name} | {validation:.5f} | {like:.5f} | {hate:.5f} |")
    return "\n".join(lines + ["", "## 边界", "", result["scope"], ""])


ADAPTER = register(adapter_from_spec(key="flvm", run=reproduce, render=render))
