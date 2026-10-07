"""Register the public Snap GRP v0.1 mechanisms."""

from __future__ import annotations

from auto_research.paper_specs.runtime import adapter_from_spec

from ..base import EvaluationTier, OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce


def render(result: dict) -> str:
    metrics = result["metrics"]
    return "# GRP v0.1 机制诊断\n\n" + "\n".join(f"- {key}: {value}" for key, value in metrics.items()) + f"\n\n> {result['scope']}\n"


ADAPTER = register(adapter_from_spec(key="grp", run=reproduce, render=render))
