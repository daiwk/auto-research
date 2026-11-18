"""Portable SensorWM arithmetic evidence, not forecasting or clinical capability."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

import pytest

from auto_research.multimodal import sensorwm_planning

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_sensorwm_planning as runner  # noqa: E402
from oct18_frozen_sources import verify_sources  # noqa: E402


def read(name):
    return json.loads((runner.AUDIT / name).read_text())


@pytest.fixture
def frozen():
    return read("frozen-sources.json")


def check_cli(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["run_sensorwm_planning.py", "--check"])
    runner.main()


def test_actual_three_seed_cpu_artifact_and_frozen_commit_membership(frozen):
    raw = read("raw-cpu.json")
    runner.validate(raw, frozen)
    assert raw["seeds"] == [42, 43, 44]
    assert [row["seed"] for row in raw["per_seed"]] == [42, 43, 44]
    assert raw["device"] == "cpu" and raw["accelerator"] == "CPU"
    assert set(frozen["source_sha256"]) == set(runner.SOURCES)
    assert re.fullmatch(r"[0-9a-f]{40}", frozen["commit"])
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for relative, expected in frozen["source_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected
    assert runner.load(runner.METRIC) == runner.metric(raw, frozen)


@pytest.mark.parametrize("field,value", [
    ("device", "cuda"), ("accelerator", "NVIDIA A100"), ("seeds", [42, 43]),
    ("code_commit", "0" * 40), ("component", "sensorwm"), ("batch", "other"),
    ("diagnostic_only", False), ("evaluation_tier", "l3_capability"),
    ("formal_comparison", True), ("promotion_eligible", True), ("evolve_integrated", True),
    ("pretrained_model_calls", 1), ("api_calls", 1), ("full_experiments_executed", True),
    ("automatic_retry", True), ("elapsed_seconds", 11), ("elapsed_seconds", float("nan")),
])
def test_raw_scope_seed_device_and_capability_tampering_rejected(field, value, frozen):
    raw = read("raw-cpu.json")
    raw[field] = value
    with pytest.raises(ValueError):
        runner.validate(raw, frozen)


@pytest.mark.parametrize("change", [
    "missing-seed", "seed", "device", "accelerator", "failed-check", "empty-checks",
    "nan-metric", "boolean-metric", "missing-metric", "promoted-tier",
])
def test_per_seed_tampering_rejected(change, frozen):
    raw = read("raw-cpu.json")
    rows = raw["per_seed"]
    if change == "missing-seed":
        rows.pop()
    elif change == "seed":
        rows[0]["seed"] = 99
    elif change == "device":
        rows[0]["execution_device"] = "cuda"
    elif change == "accelerator":
        rows[0]["execution_accelerator"] = "NVIDIA A100"
    elif change == "failed-check":
        rows[0]["checks"][next(iter(rows[0]["checks"]))] = False
    elif change == "empty-checks":
        rows[0]["checks"] = {}
    elif change == "nan-metric":
        rows[0]["metrics"]["best_fixture_score"] = float("nan")
    elif change == "boolean-metric":
        rows[0]["metrics"]["best_fixture_score"] = True
    elif change == "missing-metric":
        rows[0]["metrics"].pop("best_fixture_score")
    else:
        rows[0]["evaluation_tier"] = "l3_capability"
    with pytest.raises(ValueError):
        runner.validate(raw, frozen)


@pytest.mark.parametrize("change_both", [False, True])
def test_raw_and_frozen_source_hash_drift_rejected(change_both, frozen):
    raw = read("raw-cpu.json")
    raw["source_sha256"][runner.MODULE] = "0" * 64
    changed = deepcopy(frozen)
    if change_both:
        changed["source_sha256"][runner.MODULE] = "0" * 64
    with pytest.raises(ValueError, match="source identity"):
        runner.validate(raw, changed)


def test_forged_commit_cannot_bypass_portable_tree_proof(frozen):
    raw = read("raw-cpu.json")
    changed = deepcopy(frozen)
    raw["code_commit"] = changed["commit"] = changed["proof"]["commit"] = "0" * 40
    with pytest.raises(ValueError, match="commit|object"):
        runner.validate(raw, changed)


def test_portable_check_does_not_read_cache_use_git_or_write_files(monkeypatch):
    original_bytes, original_text = Path.read_bytes, Path.read_text

    def guarded_bytes(path, *args, **kwargs):
        if "/.cache/nov12-refresh/" in str(path.resolve()):
            raise AssertionError("portable --check cannot require source web captures")
        return original_bytes(path, *args, **kwargs)

    def guarded_text(path, *args, **kwargs):
        if "/.cache/nov12-refresh/" in str(path.resolve()):
            raise AssertionError("portable --check cannot require source web captures")
        return original_text(path, *args, **kwargs)

    def forbidden(*_args, **_kwargs):
        raise AssertionError("portable --check cannot write files or invoke Git")

    monkeypatch.setattr(Path, "read_bytes", guarded_bytes)
    monkeypatch.setattr(Path, "read_text", guarded_text)
    monkeypatch.setattr(Path, "write_bytes", forbidden)
    monkeypatch.setattr(Path, "write_text", forbidden)
    monkeypatch.setattr(runner.subprocess, "check_output", forbidden)
    check_cli(monkeypatch)


@pytest.mark.parametrize("target", ["metric-artifact", "raw-numeric-result"])
def test_check_rejects_changed_metric_or_raw_result(monkeypatch, target):
    original = runner.load

    def changed_load(path):
        payload = original(path)
        if target == "metric-artifact" and path == runner.METRIC:
            payload = deepcopy(payload)
            payload["metrics"]["best_fixture_score"] += .01
        elif target == "raw-numeric-result" and path == runner.AUDIT / "raw-cpu.json":
            payload = deepcopy(payload)
            payload["per_seed"][0]["metrics"]["best_fixture_score"] += .01
        return payload

    monkeypatch.setattr(runner, "load", changed_load)
    with pytest.raises(ValueError, match="metric artifact differs"):
        check_cli(monkeypatch)


def test_catalog_and_metric_do_not_advertise_gpu_evolve_or_capability():
    path = ROOT / "src/auto_research/paper_specs/catalog/multimodal-models/sensorwm-planning.json"
    spec, metric = json.loads(path.read_text()), runner.load(runner.METRIC)
    assert sensorwm_planning.REQUIRES_GPU_VALIDATION is False
    assert spec["key"] == "sensorwm-planning"
    assert spec["requires_gpu_validation"] is False
    assert spec.get("gpu_validation_artifact") in (None, "")
    assert spec.get("gpu_validation_passed") is not True
    assert spec["adapter"] is None and spec["implementation_status"] == "component_only"
    for row in (spec, metric):
        assert row["diagnostic_only"] is True
        assert row["evaluation_tier"] == "l1_mechanism"
        assert row["promotion_eligible"] is False and row["evolve_integrated"] is False
        assert row["automatic_retry"] is False and row["automatic_implementation_queue"] is False
        assert row["full_experiment_status"] == "not_reproduced_high_cost"
    assert metric["formal_comparison"] is False
    assert metric["dataset"]["kind"] == "nonclinical_formula_fixtures"
    assert metric["dataset"]["public_capability_benchmark"] is False
    with pytest.raises(ValueError, match="CPU"):
        sensorwm_planning.diagnostic(42, device="cuda")


def test_bilingual_paper_has_original_figure_metadata_and_current_source_hash():
    folder = ROOT / "docs/multimodal-models/2611.08568-sensorwm-planning"
    cn, en = folder / "README.md", folder / "README-en.md"
    chinese, english = cn.read_text(), en.read_text()
    for text in (chinese, english):
        assert text.count("<!-- paper-figure:start -->") == 1
        assert text.count("<!-- paper-figure:end -->") == 1
        start, end = text.index("<!-- paper-figure:start -->"), text.index("<!-- paper-figure:end -->")
        assert start < end
        assert "assets/paper-figure-01.png" in text[start:end]
        assert text.endswith("\n") and not text.endswith("\n\n")
    assert "## 论文信息" in chinese and "## 本地复现" in chinese
    assert "`sensorwm-planning`" in chinese and "版权归原作者所有" in chinese
    assert "[简体中文](README.md)" in english
    assert re.findall(r"<!-- source-sha256: ([0-9a-f]{64}) -->", english) == [
        hashlib.sha256(cn.read_bytes()).hexdigest()]
    assert (folder / "assets/paper-figure-01.png").is_file()


def test_bounded_scope_ledger_and_committed_artifact_hashes_agree():
    scope = read("task-scope.json")
    ledger = json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())
    batches = [row for row in ledger["batches"] if row["batch"] == runner.BATCH]
    assert len(batches) == 1
    batch = batches[0]
    assert scope["batch"] == runner.BATCH
    for record in (scope, batch):
        assert record["counts"]["selected_papers"] == 1
        assert record["counts"]["component_implementations"] == 1
        assert record["counts"]["cpu_validated_components"] == 1
        assert record["counts"]["cuda_validated_components"] == 0
        assert record["counts"]["new_first_publications"] == 0
        assert record["counts"]["full_capability_reproductions"] == 0
        assert record["review_watermark_advanced"] is False
        assert record["review_watermark"] == {"before": "2026-11-09", "after": "2026-11-09"}
        assert record["all_sources_exhaustive"] is False
        assert record["full_window_review_complete"] is False
    assert batch["counts"] == scope["counts"]
    assert batch["artifacts"] == scope["artifacts"]
    assert scope["artifacts"]
    for receipt in scope["artifacts"]:
        relative = Path(receipt["path"])
        assert not relative.is_absolute() and not {"..", ".cache"}.intersection(relative.parts)
        path = ROOT / "docs" / relative
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == receipt["sha256"]
    assert [(row["id"], row["key"]) for row in scope["papers"]] == [
        ("2611.08568", "sensorwm-planning")]
    candidates = {row["id"]: row for row in batch["candidates"]}
    assert set(candidates) == {"2611.08568", "2603.27787"}
    sensorwm, ckm = candidates["2611.08568"], candidates["2603.27787"]
    assert sensorwm == scope["papers"][0]
    assert sensorwm["key"] == "sensorwm-planning" and sensorwm["status"] == "implemented"
    assert sensorwm["implementation_status"] == "component_only"
    assert sensorwm["diagnostic_only"] is True and sensorwm["evaluation_tier"] == "l1_mechanism"
    assert sensorwm["full_capability_reproduced"] is False
    assert ckm["status"] == "rejected" and ckm["resolution"] == "out_of_scope_specialized_application"
    assert isinstance(ckm["reason"], str) and ckm["reason"].strip()
    assert ckm.get("key") is None and scope["excluded"] == [ckm]
