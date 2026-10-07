"""Register the public HELIX architecture mechanism."""

from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce


def render(result: dict) -> str:
    metrics = result["metrics"]
    return (
        "# HELIX 架构诊断\n\n"
        f"- 候选条件分支差异：{metrics['candidate_conditioned_delta']:.6f}\n"
        f"- 用户缓存保持不变：{metrics['user_cache_unchanged']}\n\n"
        f"> {result['scope']}\n"
    )


ADAPTER = register(adapter_from_spec(key="helix", run=reproduce, render=render))
