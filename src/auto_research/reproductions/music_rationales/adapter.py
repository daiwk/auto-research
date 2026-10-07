"""Google Music discovery: offline LLM profiles with safe cached serving."""

from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

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


ADAPTER = register(adapter_from_spec(key="music-rationales", run=reproduce, render=render))
