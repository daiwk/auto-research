from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import runpy
import sys

import pytest

from auto_research.agent_research import clasharness as c


def test_solver_view_is_allowlisted_and_detached():
    task = {"task_id": "task1", "instruction": "read the visible file", "ground_truth": {"answer": "SECRET"},
            "hidden_constraints": ["SECRET"], "data": {"private": {"answer": "SECRET"},
            "public": {"file": "public.txt", "nested": {"text": "VISIBLE"}}}}
    view = c.solver_view(task)
    assert "SECRET" not in str(view) and view["solver_reference_access"] is None
    assert not view["reference_isolation_verified"]
    assert view["public_input_trust_boundary"] == "caller_declared_public_not_content_audited"
    assert view["public_data"]["nested"]["text"] == "VISIBLE"
    view["public_data"]["file"] = "changed"
    assert task["data"]["public"]["file"] == "public.txt"


def test_demotion_uses_original_check_index_not_list_position():
    audit = {"checks": [{"task_id": "task1", "check_index": 7, "in_sets": ["value_conflict"]}]}
    checks = [{"check_index": 2, "role": "required", "passed": True},
              {"check_index": 7, "role": "required", "passed": False}]
    inventory = [{"check_index": 2, "role": "required"}, {"check_index": 7, "role": "required"}]
    original = c.score_checks("task1", checks, audit=audit, policy="as_published", expected_checks=inventory)
    adjusted = c.score_checks("task1", checks, audit=audit, policy="conservative", expected_checks=inventory)
    assert original["all_pass"] is False and adjusted["all_pass"] is True
    assert adjusted["coverage_verified"]
    assert adjusted["demoted_indices"] == [7] and adjusted["local_capability_score"] is None
    assert c.score_checks("other", checks, audit=audit, expected_checks=inventory)["all_pass"] is False


@pytest.mark.parametrize("checks", [[], [{"check_index": 0, "role": "diagnostic", "passed": True}]])
def test_zero_required_checks_is_unscorable_not_free_success(checks):
    result = c.score_checks("task1", checks, audit={"checks": []})
    assert result["all_pass"] is None and result["required_pass_fraction"] is None


def test_truthy_strings_duplicate_indices_and_unregistered_policy_rejected():
    valid = {"check_index": 0, "role": "required", "passed": True}
    for checks in ([{**valid, "passed": "false"}], [valid, valid], [{**valid, "check_index": True}]):
        with pytest.raises(c.ProtocolError):
            c.score_checks("task1", checks, audit={"checks": []})
    with pytest.raises(c.ProtocolError):
        c.score_checks("task1", [valid], audit={"checks": []}, policy="whatever_wins")


def test_curated_import_is_not_full_leaderboard_and_retains_unscorable_rows():
    row = {"success": True, "score": 1., "n_required": 1, "n_required_passed": 1,
           "checks": [{"role": "required", "passed": True}], "verb_trace": ["rm -rf /"]}
    unknown = {"success": False, "score": 0., "n_required": 0, "n_required_passed": 0, "checks": []}
    fixture = {"rounds": {"round1": {"model1": row}, "round2": {"model1": unknown}}}
    result = c.summarize_curated(fixture)
    assert result["selected_rounds"] == 2 and result["models"]["model1"]["published_successes"] == 1
    assert len(result["unscorable_required_checks"]) == 1
    assert not result["fairness_recomputed_from_curated"]
    changed = deepcopy(fixture)
    changed["rounds"]["round1"]["model1"]["n_required_passed"] = 0
    with pytest.raises(c.ProtocolError):
        c.summarize_curated(changed)


def test_pinned_import_rejects_missing_or_changed_release(tmp_path):
    with pytest.raises(c.ProtocolError):
        c.load_release(tmp_path)
    path = tmp_path / "analysis/dead_rounds_exclusion.json"
    path.parent.mkdir()
    path.write_text("{}")
    with pytest.raises(c.ProtocolError, match="pinned source mismatch"):
        c.load_release(tmp_path)


@pytest.mark.parametrize("field", ["reference_solution", "referenceAnswer", "gold", "Ground-Truth",
                                    "private_state", "expected_answer", "solution_commands", "reference"])
def test_declared_public_data_rejects_hidden_aliases_at_any_depth(field):
    task = {"task_id": "t", "instruction": "public instruction",
            "data": {"public": {"nested": [{field: "SECRET"}]}}}
    with pytest.raises(c.ProtocolError, match="hidden/scorer field"):
        c.solver_view(task)
    task["data"]["public"] = {}
    task["visible_constraints"] = [{field: "SECRET"}]
    with pytest.raises(c.ProtocolError, match="hidden/scorer field"):
        c.solver_view(task)


def test_partial_verdicts_cannot_claim_complete_success():
    checks = [{"check_index": 2, "role": "required", "passed": True}]
    result = c.score_checks("t", checks, audit={"checks": []})
    assert result["observed_checks_all_pass"] is True
    assert not result["coverage_verified"] and result["all_pass"] is None
    assert result["required_pass_fraction"] is None
    assert result["observed_required_pass_fraction"] == 1.
    for inventory in ([{"check_index": 2, "role": "required"}, {"check_index": 3, "role": "required"}],
                      [], [{"check_index": 2, "role": "diagnostic"}],
                      [{"check_index": 2, "role": "required"}] * 2,
                      [{"check_index": True, "role": "required"}]):
        with pytest.raises(c.ProtocolError):
            c.score_checks("t", checks, audit={"checks": []}, expected_checks=inventory)


def test_complete_diagnostic_only_inventory_is_not_vacuous_success():
    checks = [{"check_index": 0, "role": "diagnostic", "passed": True}]
    result = c.score_checks("t", checks, audit={"checks": []},
                            expected_checks=[{"check_index": 0, "role": "diagnostic"}])
    assert result["coverage_verified"] and not result["official_task_inventory_verified"]
    assert result["all_pass"] is None and result["observed_checks_all_pass"] is None


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_declared_public_json_rejects_nonfinite_numbers(value):
    with pytest.raises(c.ProtocolError, match="finite"):
        c.solver_view({"task_id": "t", "instruction": "public", "data": {"public": {"value": value}}})


def test_fetch_rejects_oversized_cache_before_reading(tmp_path, monkeypatch):
    path = tmp_path / next(iter(c.FILE_HASHES))
    path.parent.mkdir(parents=True)
    with path.open("wb") as handle:
        handle.truncate(c.MAX_BYTES + 1)
    def forbidden_read(*args, **kwargs):
        raise AssertionError("oversized cache must be rejected before reading")
    monkeypatch.setattr(Path, "read_bytes", forbidden_read)
    with pytest.raises(c.ProtocolError, match="bounded"):
        c.fetch_release(tmp_path)


@pytest.mark.parametrize("inventory_source", [None, "embedded", "file"])
def test_score_cli_only_reports_complete_success_with_explicit_inventory(tmp_path, monkeypatch, inventory_source):
    module = runpy.run_path(str(Path(__file__).resolve().parents[1] / "scripts/run_clasharness.py"))
    monkeypatch.setitem(module["main"].__globals__, "load_release", lambda path: {"analysis/v8_check_fairness_audit.json": {"checks": []}})
    verdicts, output = tmp_path / "verdicts.json", tmp_path / "result.json"
    row = {"task_id": "t", "checks": [{"check_index": 0, "role": "required", "passed": True}]}
    inventory = [{"check_index": 0, "role": "required"}]
    argv = ["run_clasharness.py", "score-checks", "--release-dir", str(tmp_path),
            "--verdicts", str(verdicts), "--output", str(output)]
    if inventory_source == "embedded":
        row["expected_checks"] = inventory
    elif inventory_source == "file":
        expected = tmp_path / "expected.json"
        expected.write_text(json.dumps(inventory))
        argv += ["--expected-checks", str(expected)]
    verdicts.write_text(json.dumps(row))
    monkeypatch.setattr(sys, "argv", argv)
    assert module["main"]() == 0
    result = json.loads(output.read_text())
    assert result["coverage_verified"] is (inventory_source is not None)
    assert result["all_pass"] is (None if inventory_source is None else True)
