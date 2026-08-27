from __future__ import annotations

from dataclasses import asdict, fields
import json
from pathlib import Path

from auto_research.agent_research.capability_benchmark import build_capability_tasks
from auto_research.agent_research.capability_models import CapabilityObservation
from auto_research.agent_research.capability_runner import (
    CapabilitySuiteConfig,
    run_capability_suite,
)


def test_l2_observation_excludes_evaluator_labels():
    task = build_capability_tasks(12, 42)[0]
    public_fields = {field.name for field in fields(CapabilityObservation)}
    serialized = json.dumps(asdict(task.observation), sort_keys=True)

    assert "answer" not in public_fields
    assert "plan" not in public_fields
    assert "route" not in public_fields
    assert task.answer not in serialized


def test_l2_suite_is_discriminative_and_writes_formal_three_seed_evidence(
    tmp_path: Path,
):
    results = run_capability_suite(CapabilitySuiteConfig(
        seeds=(42, 43, 44), episodes=24, output_dir=tmp_path,
    ))

    assert results["long-context"]["metrics"]["joint_success"] < results["react"]["metrics"]["joint_success"]
    assert results["react"]["metrics"]["joint_success"] < results["ahead"]["metrics"]["joint_success"]
    assert len({
        row["metrics"]["joint_success"]
        for row in results["react"]["seed_results"]
    }) > 1
    for method, payload in results.items():
        assert payload["manifest_ref"] == (
            f"agent-research:{method}:toolroute-l2-v1"
        )
        assert payload["evaluation_protocol"] == {
            "tier": "l2_capability",
            "seeds": [42, 43, 44],
            "formal_comparison": True,
            "claim_policy": (
                "shared no-oracle benchmark; compare only within toolroute-l2-v1"
            ),
        }
        assert payload["diagnostics"]["oracle_fields_exposed"] is False
        assert payload["aggregate_metrics"]["joint_success"]["ci95_radius"] >= 0
        run_dir = tmp_path / f"{method}-toolroute-l2-seeds42-43-44"
        assert (run_dir / "metrics.json").exists()
        assert "oracle labels" in (run_dir / "report.md").read_text(encoding="utf-8")


def test_single_seed_l2_run_is_not_marked_as_formal(tmp_path: Path):
    payload = run_capability_suite(CapabilitySuiteConfig(
        methods=("react",), seeds=(42,), episodes=12, output_dir=tmp_path,
    ))["react"]

    assert payload["evaluation_protocol"]["formal_comparison"] is False
    assert payload["evaluation_protocol"]["tier"] == "l2_capability"


def test_committed_l2_evidence_is_complete_and_not_saturated():
    root = Path(__file__).resolve().parents[1]
    summary = json.loads(
        (root / "docs/experiments/agent-toolroute-l2-seeds42-44.json").read_text(
            encoding="utf-8"
        )
    )

    assert summary["oracle_fields_exposed"] is False
    assert summary["manifest_ref"] == "experiments:agent-toolroute-l2-seeds42-44"
    assert summary["seeds"] == [42, 43, 44]
    assert len(summary["results"]) == 6
    assert summary["evaluation_protocol"]["formal_comparison"] is True
    assert summary["provenance"]["dataset_fingerprint"]
    assert len({
        round(result["metrics"]["joint_success"], 6)
        for result in summary["results"].values()
    }) > 1
    for result in summary["results"].values():
        artifact = json.loads(
            (root / result["artifact_path"]).read_text(encoding="utf-8")
        )
        assert artifact["evaluation_protocol"]["tier"] == "l2_capability"
        assert artifact["evaluation_protocol"]["formal_comparison"] is True
        assert artifact["diagnostics"]["oracle_fields_exposed"] is False
        assert artifact["provenance"]["dataset_fingerprint"]
