"""Protocol tests use invented CSVs, never fabricated Lean execution success."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
from types import MappingProxyType

import pytest

from auto_research.agent_research import autoformbench as a


ROOT = Path(__file__).resolve().parents[1]


def _csv(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


@pytest.fixture
def inputs():
    manifest = [
        {"problem_id": "task_a", "book": "book_a", "target_count": "2",
         "target_declarations": "A.helper;A.final"},
        {"problem_id": "task_b", "book": "book_b", "target_count": "1",
         "target_declarations": "B.final"},
    ]
    sources = [
        {"book": name, "title": name, "authors": "An author", "url": "https://example.org/book"}
        for name in ("book_a", "book_b")
    ]
    return manifest, sources


@pytest.fixture
def release(inputs):
    manifest, sources = inputs
    return a._parse_release(_csv(a.MANIFEST_FIELDS, manifest), _csv(a.SOURCE_FIELDS, sources))


@pytest.fixture
def rows():
    result = []
    for task, book, target, passed in (("task_a", "book_a", "A.final", "true"),
                                        ("task_b", "book_b", "B.final", "false")):
        result.append({"problem_id": task, "textbook": book, "target_theorem": target,
                       "passed": passed, **{field: "1" for field in a.COUNT_FIELDS},
                       "cost_usd": "2.5000", "end_reason": "success" if passed == "true" else "model_gave_up"})
    return result


def _pin_test_fixture(monkeypatch, tmp_path, inputs, rows):
    """Only unit-test hashes are replaced; this never creates published evidence."""
    manifest, sources = inputs
    files = {"MANIFEST.csv": _csv(a.MANIFEST_FIELDS, manifest),
             "SOURCES.csv": _csv(a.SOURCE_FIELDS, sources),
             "leaderboard_data/gpt-6-astra.csv": _csv(a.RESULT_FIELDS, rows)}
    monkeypatch.setattr(a, "OFFICIAL_TASK_COUNT", 2)
    monkeypatch.setattr(a, "FILE_HASHES", MappingProxyType({
        name: hashlib.sha256(contents).hexdigest() for name, contents in files.items()
    }))
    for relative, contents in files.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(contents)
    return a.load_release(tmp_path), tmp_path / "leaderboard_data/gpt-6-astra.csv"


def test_manifest_inventory_is_immutable_and_not_a_proof(release):
    assert len(release.tasks) == 2 and len(release.sources) == 2
    assert release.tasks[0].target_declarations == ("A.helper", "A.final")
    assert not release.pinned
    with pytest.raises(TypeError):
        release.sources["fake"] = release.sources["book_a"]
    with pytest.raises(FrozenInstanceError):
        release.tasks[0].book = "another"
    view = a.task_view(release, release.tasks)
    assert view["source_condition"] == "source-free"
    assert view["inventory_only"] and not view["execution_performed"]
    assert not view["training_use_allowed"] and not view["contains_gold_proofs"]
    assert len(view["selection_sha256"]) == 64
    assert "proof" not in view["tasks"][0]


@pytest.mark.parametrize("change", ["duplicate_task", "unsafe_id", "unknown_book", "zero_targets",
                                   "count_mismatch", "duplicate_target", "empty_target", "extra_source"])
def test_malformed_manifest_rejected(inputs, change):
    manifest, sources = inputs
    if change == "duplicate_task":
        manifest.append(dict(manifest[0]))
    elif change == "unsafe_id":
        manifest[0]["problem_id"] = "../task"
    elif change == "unknown_book":
        manifest[0]["book"] = "missing"
    elif change == "zero_targets":
        manifest[0]["target_count"] = "0"
    elif change == "count_mismatch":
        manifest[0]["target_count"] = "3"
    elif change == "duplicate_target":
        manifest[0]["target_declarations"] = "A.final;A.final"
    elif change == "empty_target":
        manifest[0]["target_declarations"] = "A.final;"
    else:
        sources.append({**sources[0], "book": "unused"})
    with pytest.raises(a.ProtocolError):
        a._parse_release(_csv(a.MANIFEST_FIELDS, manifest), _csv(a.SOURCE_FIELDS, sources))


def test_pinned_release_rejects_unknown_revision_and_modified_bytes(tmp_path, inputs):
    manifest, sources = inputs
    (tmp_path / "MANIFEST.csv").write_bytes(_csv(a.MANIFEST_FIELDS, manifest))
    (tmp_path / "SOURCES.csv").write_bytes(_csv(a.SOURCE_FIELDS, sources))
    with pytest.raises(a.ProtocolError, match="revision"):
        a.load_release(tmp_path, revision="main")
    with pytest.raises(a.ProtocolError, match="hash mismatch"):
        a.load_release(tmp_path)


def test_filters_are_exact_and_deterministic(release):
    assert [task.problem_id for task in a.select_tasks(release, task_ids=("task_b", "task_a"))] == ["task_a", "task_b"]
    assert a.select_tasks(release, books=("book_b",))[0].problem_id == "task_b"
    assert len(a.select_tasks(release, limit=1)) == 1
    for kwargs in ({"task_ids": ("missing",)}, {"books": ("missing",)},
                   {"task_ids": ("task_a", "task_a")}, {"limit": True}, {"limit": 0},
                   {"task_ids": ("task_a",), "books": ("book_b",)}):
        with pytest.raises(a.ProtocolError):
            a.select_tasks(release, **kwargs)
    assert a.task_view(release, release.tasks)["selection_sha256"] != a.task_view(release, release.tasks[:1])["selection_sha256"]
    with pytest.raises(a.ProtocolError):
        a.task_view(release, [replace(release.tasks[0], target_declarations=("gold",))])


def test_plan_uses_upstream_real_arguments_but_does_not_execute(monkeypatch, tmp_path, inputs, rows):
    release, _ = _pin_test_fixture(monkeypatch, tmp_path, inputs, rows)
    plan = a.harbor_plan(release, release.tasks[:1], repository_dir=tmp_path)
    assert plan["execution_performed"] is False
    assert plan["source_condition"] == "source-free" and plan["agent"] == "nop"
    assert plan["environment"] == {"HARBOR_TELEMETRY": "0", "UV_OFFLINE": "1"}
    steps = plan["commands"][0]["steps"]
    assert steps[0] == ["python3", "harbor/export.py", "--problem", "task_a"]
    assert steps[1][-3:] == ["--check", "--problem", "task_a"]
    assert steps[2][:5] == ["uvx", "--offline", "--from", "harbor==0.22.0", "harbor"]
    assert plan["gpus"] == 0 and plan["network_mode"] == "no-network"
    solver = a.harbor_plan(release, release.tasks[:1], repository_dir=tmp_path,
                          agent="installed-agent", model="provider/model")
    assert solver["commands"][0]["steps"][-1][-2:] == ["--model", "provider/model"]
    for kwargs in ({"agent": "installed-agent"}, {"agent": "--option"}, {"model": "not-used"}):
        with pytest.raises(a.ProtocolError):
            a.harbor_plan(release, release.tasks, repository_dir=tmp_path, **kwargs)


def test_unpinned_inventory_cannot_plan_an_official_run(release, tmp_path):
    with pytest.raises(a.ProtocolError, match="pinned"):
        a.harbor_plan(release, release.tasks, repository_dir=tmp_path)


@pytest.mark.parametrize("change", ["unknown", "duplicate", "missing", "book", "target", "bool",
                                   "negative", "nan", "infinite", "fractional_count", "reason"])
def test_result_rows_reject_identity_and_metric_corruption(release, rows, change):
    if change == "unknown":
        rows[0]["problem_id"] = "not_a_task"
    elif change == "duplicate":
        rows.append(dict(rows[0]))
    elif change == "missing":
        rows.pop()
    elif change == "book":
        rows[0]["textbook"] = "book_b"
    elif change == "target":
        rows[0]["target_theorem"] = "different_statement"
    elif change == "bool":
        rows[0]["passed"] = "1"
    elif change == "negative":
        rows[0]["cost_usd"] = "-0.01"
    elif change == "nan":
        rows[0]["cost_usd"] = "NaN"
    elif change == "infinite":
        rows[0]["cost_usd"] = "Infinity"
    elif change == "fractional_count":
        rows[0]["turns"] = "1.5"
    else:
        rows[0]["end_reason"] = "model_gave_up"
    with pytest.raises(a.ProtocolError):
        a._parse_leaderboard(release, _csv(a.RESULT_FIELDS, rows))


def test_official_import_cannot_masquerade_as_source_free_or_local(monkeypatch, tmp_path, inputs, rows):
    release, path = _pin_test_fixture(monkeypatch, tmp_path, inputs, rows)
    result = a.import_official_results(release, path, model="gpt-6-astra", source_condition="source-present")
    assert result["metrics"]["solved"] == 1 and result["metrics"]["tasks"] == 2
    assert result["metrics"]["observed_cost_usd_total"] == "5.0000"
    assert result["local_capability_score"] is None and not result["local_execution_performed"]
    assert result["diagnostic_only"] and not result["promotion_eligible"]
    assert result["source_condition"] == "source-present"
    assert result["reasoning_effort"] == "max"
    assert not result["reasoning_effort_is_cross_provider_matched_compute"]
    for kwargs in ({"source_condition": "source-free"},
                   {"source_condition": "source-present", "budget_usd": Decimal("20")}):
        with pytest.raises(a.ProtocolError, match="condition"):
            a.import_official_results(release, path, model="gpt-6-astra", **kwargs)
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(a.ProtocolError, match="hash mismatch"):
        a.import_official_results(release, path, model="gpt-6-astra", source_condition="source-present")


def test_budget_overruns_are_preserved_and_strict_comparison_rejects_them(monkeypatch, tmp_path, inputs, rows):
    rows[0]["cost_usd"] = "358.8273"
    release, path = _pin_test_fixture(monkeypatch, tmp_path, inputs, rows)
    report = a.import_official_results(release, path, model="gpt-6-astra", source_condition="source-present")
    assert report["budget_audit"]["observed_rows_above_nominal_cap"] == 1
    assert report["budget_audit"]["task_ids"] == ["task_a"]
    assert report["metrics"]["tasks"] == 2 and report["metrics"]["observed_cost_usd_max"] == "358.8273"
    with pytest.raises(a.ProtocolError, match="strict budget"):
        a.validate_comparison([report], source_condition="source-present", budget_usd=Decimal("200"))
    a.validate_comparison([report], source_condition="source-present", budget_usd=Decimal("200"), strict_budget=False)


@pytest.mark.parametrize("change", ["source", "budget", "manifest", "tasks", "scaffold", "tools", "stopping", "duplicate"])
def test_mixed_condition_comparisons_are_rejected(monkeypatch, tmp_path, inputs, rows, change):
    release, path = _pin_test_fixture(monkeypatch, tmp_path, inputs, rows)
    first = a.import_official_results(release, path, model="gpt-6-astra", source_condition="source-present")
    second = json.loads(json.dumps(first))
    second["model"] = "other"
    if change == "source":
        second["source_condition"] = "source-free"
    elif change == "budget":
        second["nominal_budget_usd_per_task"] = "20"
    elif change == "manifest":
        second["manifest_sha256"] = "0" * 64
    elif change == "tasks":
        second["metrics"]["tasks"] = 1
    elif change == "scaffold":
        second["scaffold"] = "a different system"
    elif change == "tools":
        second["tool_access"] = []
    elif change == "stopping":
        second["stopping_policy"] = "first surrender"
    else:
        second["model"] = first["model"]
    with pytest.raises(a.ProtocolError):
        a.validate_comparison([first, second], source_condition="source-present", budget_usd=Decimal("200"))


@pytest.mark.parametrize("status,accepted,exit_code,reward", [
    ("accepted", True, 0, 1), ("rejected", False, 1, 0), ("error", None, None, None),
])
def test_existing_verdict_parser_preserves_infrastructure_errors(tmp_path, status, accepted, exit_code, reward):
    # This is a parser fixture, not a mocked subprocess or proof of running Lean.
    path = tmp_path / "verdict.json"
    path.write_text(json.dumps({"problem_id": "task_a", "status": status,
                                "accepted": accepted, "reason": "parser fixture",
                                "comparator_exit_code": exit_code}))
    parsed = a.read_verifier_verdict(path, expected_problem_id="task_a")
    assert parsed["reward"] == reward
    assert parsed["local_capability_score"] is None and not parsed["verifier_provenance_attested"]
    with pytest.raises(a.ProtocolError, match="ID"):
        a.read_verifier_verdict(path, expected_problem_id="task_b")


def test_invalid_acceptance_is_not_a_success(tmp_path):
    path = tmp_path / "verdict.json"
    path.write_text(json.dumps({"problem_id": "task_a", "status": "accepted", "accepted": True,
                                "reason": "wrong exit code", "comparator_exit_code": 2}))
    with pytest.raises(a.ProtocolError, match="exit code"):
        a.read_verifier_verdict(path, expected_problem_id="task_a")


@pytest.mark.parametrize("payload", [[], {}, {"problem_id": "task_a", "status": "error"}])
def test_malformed_verdict_is_not_silently_an_infrastructure_error(tmp_path, payload):
    path = tmp_path / "verdict.json"
    path.write_text(json.dumps(payload))
    with pytest.raises(a.ProtocolError, match="upstream verdict fields"):
        a.read_verifier_verdict(path, expected_problem_id="task_a")


def test_comparison_rejects_nonfinite_and_missing_budgets(monkeypatch, tmp_path, inputs, rows):
    release, path = _pin_test_fixture(monkeypatch, tmp_path, inputs, rows)
    report = a.import_official_results(release, path, model="gpt-6-astra", source_condition="source-present")
    with pytest.raises(a.ProtocolError, match="finite"):
        a.validate_comparison([report], source_condition="source-present", budget_usd=Decimal("NaN"))
    report.pop("nominal_budget_usd_per_task")
    with pytest.raises(a.ProtocolError, match="nominal budget"):
        a.validate_comparison([report], source_condition="source-present", budget_usd=Decimal("200"))


def test_cli_help_is_an_actual_cpu_process_without_model_or_verifier_download():
    completed = subprocess.run([sys.executable, str(ROOT / "scripts/run_autoformbench.py"), "--help"],
                               cwd=ROOT, capture_output=True, text=True, timeout=20)
    assert completed.returncode == 0
    assert "import-results" in completed.stdout and "verdict" in completed.stdout


def test_documentation_and_catalog_keep_unknown_date_and_interface_boundary():
    spec = json.loads((ROOT / "src/auto_research/paper_specs/catalog/agent-research/autoformbench.json").read_text())
    text = (ROOT / "docs/agent-research/autoformbench/README.md").read_text()
    assert spec["adapter"] is None and spec["published"] == ""
    assert spec["implementation_status"] == "evaluation_protocol_interface"
    assert not spec["requires_gpu_validation"] and not spec["promotion_eligible"]
    for label in ("| 论文链接 |", "| 公司/机构 |", "| 首次公开日期 |", "| 原文开源代码 |",
                  "| 本地 Adapter |", "| 本地复现代码 |", "source-present", "source-free",
                  a.REVISION, "成本过高，不复现（审查 DONE）"):
        assert label in text
