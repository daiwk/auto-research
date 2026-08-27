from __future__ import annotations

from dataclasses import asdict, fields
import json
from pathlib import Path

from auto_research.agent_research.capability_benchmark import (
    CapabilityEnvironment,
    build_capability_tasks,
)
from auto_research.agent_research.capability_models import CapabilityObservation
from auto_research.agent_research.capability_runner import (
    CapabilitySuiteConfig,
    run_capability_suite,
)


def test_l2_observation_excludes_evaluator_labels():
    task = build_capability_tasks(12, 42, "test")[0]
    public_fields = {field.name for field in fields(CapabilityObservation)}
    serialized = json.dumps(asdict(task.observation), sort_keys=True)

    assert "answer" not in public_fields
    assert "plan" not in public_fields
    assert "route" not in public_fields
    assert task.answer not in serialized
    assert "canonical_route" not in serialized
    feedback = CapabilityEnvironment(task).call("guide")
    assert feedback.status == "unknown_tool"
    assert not feedback.next_tags


def test_l21_splits_have_disjoint_families_and_harder_test_routes():
    train = build_capability_tasks(24, 42, "train")
    validation = build_capability_tasks(24, 42, "validation")
    test = build_capability_tasks(24, 42, "test")

    families = [
        {task.observation.family for task in rows}
        for rows in (train, validation, test)
    ]
    assert families[0].isdisjoint(families[1])
    assert families[0].isdisjoint(families[2])
    assert families[1].isdisjoint(families[2])
    assert max(len(task.canonical_route) for task in train) == 4
    assert min(len(task.canonical_route) for task in test) == 5


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
    assert results["reflexion"]["seed_results"][0]["telemetry"]["reflections"] > 0
    assert results["agent-g2"]["seed_results"][0]["telemetry"]["verifications"] > 0
    assert results["ahead"]["seed_results"][0]["telemetry"]["compressions"] > 0
    assert results["auso"]["seed_results"][0]["telemetry"]["skill_reuses"] > 0
    for method, payload in results.items():
        assert payload["manifest_ref"] == (
            f"agent-research:{method}:toolroute-l2.1-v1"
        )
        assert payload["evaluation_protocol"] == {
            "tier": "l2_capability",
            "seeds": [42, 43, 44],
            "formal_comparison": True,
            "claim_policy": (
                "held-out test, no guide/oracle; compare only within toolroute-l2.1-v1"
            ),
        }
        assert payload["diagnostics"]["oracle_fields_exposed"] is False
        assert payload["aggregate_metrics"]["joint_success"]["ci95_radius"] >= 0
        assert payload["diagnostics"]["guide_endpoint"] == "absent"
        assert payload["metrics"]["joint_success"] < 1.0
        run_dir = tmp_path / f"{method}-toolroute-l21-seeds42-43-44"
        assert (run_dir / "metrics.json").exists()
        report = (run_dir / "report.md").read_text(encoding="utf-8")
        assert "guide endpoint" in report
        assert "train、validation、test" in report


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
    assert summary["manifest_ref"] == "experiments:agent-toolroute-l2.1-seeds42-44"
    assert summary["seeds"] == [42, 43, 44]
    assert len(summary["results"]) == 6
    assert len(summary["ablations"]) == 5
    assert summary["guide_endpoint"] == "absent"
    assert summary["evaluation_protocol"]["formal_comparison"] is True
    assert summary["provenance"]["dataset_fingerprint"]
    assert len({
        round(result["metrics"]["joint_success"], 6)
        for result in summary["results"].values()
    }) > 1
    assert (
        summary["ablations"]["react-no-retry"]["metrics"]["joint_success"]
        < summary["results"]["react"]["metrics"]["joint_success"]
    )
    assert (
        summary["ablations"]["reflexion-no-reflection"]["metrics"]["joint_success"]
        < summary["results"]["reflexion"]["metrics"]["joint_success"]
    )
    assert (
        summary["ablations"]["agent-g2-no-verifier"]["metrics"]["joint_success"]
        < summary["results"]["agent-g2"]["metrics"]["joint_success"]
    )
    assert (
        summary["ablations"]["ahead-no-compression"]["metrics"]["average_cost"]
        > summary["results"]["ahead"]["metrics"]["average_cost"]
    )
    assert (
        summary["ablations"]["auso-no-memory"]["metrics"]["average_cost"]
        > summary["results"]["auso"]["metrics"]["average_cost"]
    )
    for result in summary["results"].values():
        artifact = json.loads(
            (root / result["artifact_path"]).read_text(encoding="utf-8")
        )
        assert artifact["evaluation_protocol"]["tier"] == "l2_capability"
        assert artifact["evaluation_protocol"]["formal_comparison"] is True
        assert artifact["diagnostics"]["oracle_fields_exposed"] is False
        assert artifact["provenance"]["dataset_fingerprint"]

    evolve = json.loads(
        (root / summary["evolve_artifact"]).read_text(encoding="utf-8")
    )
    assert evolve["diagnostics"]["generations"] == 3
    assert evolve["diagnostics"]["population"] == 9
    assert evolve["diagnostics"]["trials"] == 28
    assert len(evolve["diagnostics"]["lineage"]) == 28
    assert evolve["metrics"]["joint_success"] > evolve["baseline_metrics"]["joint_success"]
    assert evolve["metrics"]["plan_step_f1"] > evolve["baseline_metrics"]["plan_step_f1"]
