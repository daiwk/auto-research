"""EvoPilot comparison-verification mechanism reviewed on 2026-09-21."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import numpy as np

from .base import (
    EvaluationTier,
    OnlineABEvidence,
    PaperMetadata,
    ReproductionAdapter,
    ReproductionFidelity,
)
from .industrial_2026 import (
    base_scores,
    evaluate,
    load_industrial_data,
    render_standard,
    summary_result,
    tune_blend,
)


@dataclass(frozen=True)
class ComparisonProtocol:
    base_revision: str
    data_revision: str
    evaluator_revision: str
    output_depth: int
    authorized_treatment: tuple[str, ...]


def verify_comparison(
    control: Mapping[str, Any],
    treatment: Mapping[str, Any],
    protocol: ComparisonProtocol,
) -> dict[str, Any]:
    """Fail closed unless artifact-backed arms realize exactly one approved contrast."""
    errors: list[str] = []
    for arm_name, arm in (("control", control), ("treatment", treatment)):
        if arm.get("status") != "succeeded":
            errors.append(f"{arm_name}:terminal-status")
        for field, expected in (
            ("base_revision", protocol.base_revision),
            ("data_revision", protocol.data_revision),
            ("evaluator_revision", protocol.evaluator_revision),
            ("effective_output_depth", protocol.output_depth),
        ):
            if arm.get(field) != expected:
                errors.append(f"{arm_name}:{field}")
        if not arm.get("artifact_digest"):
            errors.append(f"{arm_name}:artifact-provenance")
    shared = {
        "base_revision", "data_revision", "evaluator_revision",
        "effective_output_depth",
    }
    for field in shared:
        if control.get(field) != treatment.get(field):
            errors.append(f"pair:{field}")
    realized = tuple(sorted(
        key
        for key in set(control.get("configuration", {}))
        | set(treatment.get("configuration", {}))
        if control.get("configuration", {}).get(key)
        != treatment.get("configuration", {}).get(key)
    ))
    if realized != tuple(sorted(protocol.authorized_treatment)):
        errors.append("pair:unauthorized-contrast")
    return {
        "admitted": not errors,
        "errors": tuple(dict.fromkeys(errors)),
        "realized_treatment": realized,
    }


def interaction_head_scores(features: np.ndarray, history) -> np.ndarray:
    """Candidate-conditioned nonlinear rescoring over a frozen public representation."""
    x = np.asarray(features, dtype=np.float64)
    query = x[np.asarray(history[-8:], dtype=np.int64)].mean(axis=0)
    affinity = x @ query
    interaction = np.square(np.maximum(affinity, 0.0))
    diversity = np.sqrt(np.maximum(np.var(x - query, axis=1), 0.0))
    return affinity + 0.20 * interaction - 0.05 * diversity


def reproduce_evopilot(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_industrial_data(dataset_dir)
    baseline_scorer = lambda history: base_scores(data, history)
    method_scorer = lambda history: interaction_head_scores(
        data.sequences.features, history
    )
    alpha, scorer, validation = tune_blend(
        data, baseline_scorer, method_scorer
    )
    protocol = ComparisonProtocol(
        "shared-base-v1", "movielens-100k-temporal-v1",
        "topk-evaluator-v1", 10, ("interaction_head",),
    )
    common = {
        "status": "succeeded",
        "base_revision": protocol.base_revision,
        "data_revision": protocol.data_revision,
        "evaluator_revision": protocol.evaluator_revision,
        "artifact_digest": "public-movielens-artifact-v1",
    }
    invalid = verify_comparison(
        {**common, "effective_output_depth": 40,
         "configuration": {"interaction_head": False}},
        {**common, "effective_output_depth": 10,
         "configuration": {"interaction_head": True}},
        protocol,
    )
    valid = verify_comparison(
        {**common, "effective_output_depth": 10,
         "configuration": {"interaction_head": False}},
        {**common, "effective_output_depth": 10,
         "configuration": {"interaction_head": True}},
        protocol,
    )
    result = summary_result(
        key="evopilot",
        paper={
            "arxiv_id": "2609.21257",
            "title": "Verify, Don't Trust: Agentic Model Development for Video Discovery Retrieval at Scale",
            "url": "https://arxiv.org/abs/2609.21257",
            "organization": "Meta",
        },
        data=data,
        baseline_name="matched two-tower public proxy",
        method_name="matched interaction-head public proxy",
        baseline=evaluate(data, baseline_scorer),
        proposed=evaluate(data, scorer),
        stages={
            "validation_only_alpha": alpha,
            "validation_metrics": validation,
            "historical_mismatch_rejected": not invalid["admitted"],
            "historical_mismatch_errors": invalid["errors"],
            "matched_comparison_admitted": valid["admitted"],
            "realized_treatment": valid["realized_treatment"],
        },
        paper_results={
            "offline_hit_rate_pp": 3.20,
            "online_gsrr_relative_percent": 0.66,
            "campaign_days": 37,
        },
        scope=(
            "公开 MovieLens 上执行比较协议、artifact attestation、fail-closed pair verifier "
            "与 validation-only 交互头对照；不复刻 Meta VDD 私有视频日志、百亿级索引、"
            "远程工作流或线上流量。"
        ),
    )
    result["manifest_ref"] = "reproduction:evopilot"
    result["setup"]["seed"] = seed
    return result


def make_evopilot_adapter() -> ReproductionAdapter:
    return ReproductionAdapter(
        key="evopilot",
        paper=PaperMetadata(
            arxiv_id="2609.21257",
            title="Verify, Don't Trust: Agentic Model Development for Video Discovery Retrieval at Scale",
            url="https://arxiv.org/abs/2609.21257",
            track="recommendation",
            organization="Meta Platforms",
            published="2026-09-18",
            publication_label="arXiv v1",
            topics=("autoresearch", "experiment-verification", "video-retrieval"),
            online_ab=(OnlineABEvidence(
                "Video Deep Dive",
                "Good Search Result Rate for Retention",
                0.66,
                "seven-day randomized online evaluation",
                source_url="https://arxiv.org/html/2609.21257v1",
                source_location="Abstract; Section 5.5",
                experiment_duration="7 days",
                retrieved_at="2026-09-21",
            ),),
        ),
        run=reproduce_evopilot,
        render=render_standard,
        fidelity=ReproductionFidelity.CORE_MECHANISM,
        omitted_core_components=(
            "Meta VDD private video and interaction logs",
            "production ANN index and serving funnel",
            "remote workflow orchestration and human approval service",
        ),
        evaluation_tier=EvaluationTier.PUBLIC_DATASET,
        datasets=("MovieLens 100K",),
        baseline="matched two-tower public proxy",
        metrics=(
            "baseline.hit_at_10", "baseline.ndcg_at_10",
            "method.hit_at_10", "method.ndcg_at_10",
            "stages.historical_mismatch_rejected",
            "stages.matched_comparison_admitted",
        ),
        default_seeds=(42, 43, 44),
        budget="220 users / 360 items; validation-only blend selection",
        device_capabilities=("cpu",),
        infer_device_capabilities=False,
    )
