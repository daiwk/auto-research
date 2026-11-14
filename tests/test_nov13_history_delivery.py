"""Portable six-paper intake boundaries and four-component CPU evidence."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import run_nov13_history_components as runner  # noqa: E402


def test_four_actual_seed_sets_and_portable_frozen_commit():
    frozen = runner.load(runner.AUDIT / "frozen-sources.json")
    raw = runner.load(runner.AUDIT / "raw-cpu.json")
    runner.validate(raw, frozen)
    assert set(frozen["source_sha256"]) == set(runner.SOURCES)
    assert set(raw["components"]) == set(runner.COMPONENTS)
    for key in runner.COMPONENTS:
        assert runner.load(runner.metric_path(key)) == runner.metric(key, raw, frozen)
        assert [row["seed"] for row in raw["components"][key]] == [42, 43, 44]


@pytest.mark.parametrize("field,value", [
    ("device", "cuda"), ("accelerator", "NVIDIA A100"), ("seeds", [42]),
    ("code_commit", "0" * 40), ("batch", "other"), ("diagnostic_only", False),
    ("evaluation_tier", "l3_capability"), ("formal_comparison", True),
    ("promotion_eligible", True), ("evolve_integrated", True), ("api_calls", 1),
    ("full_experiments_executed", True), ("elapsed_seconds", float("nan")),
    ("elapsed_seconds", 11), ("automatic_retry", True),
])
def test_raw_claim_or_execution_scope_tampering_rejected(field, value):
    raw = runner.load(runner.AUDIT / "raw-cpu.json")
    raw[field] = value
    with pytest.raises(ValueError):
        runner.validate(raw, runner.load(runner.AUDIT / "frozen-sources.json"))


@pytest.mark.parametrize("change", ["missing-component", "missing-seed", "failed-check", "nan", "gpu", "source"])
def test_component_and_source_tampering_rejected(change):
    raw = runner.load(runner.AUDIT / "raw-cpu.json")
    frozen = runner.load(runner.AUDIT / "frozen-sources.json")
    rows = raw["components"]["scientist-two"]
    if change == "missing-component":
        del raw["components"]["envharness"]
    elif change == "missing-seed":
        rows.pop()
    elif change == "failed-check":
        rows[0]["checks"][next(iter(rows[0]["checks"]))] = False
    elif change == "nan":
        rows[0]["metrics"][next(iter(rows[0]["metrics"]))] = float("nan")
    elif change == "gpu":
        rows[0]["execution_device"] = "cuda"
    else:
        frozen = deepcopy(frozen)
        path = runner.MODULES["scientist-two"]
        raw["source_sha256"][path] = frozen["source_sha256"][path] = "0" * 64
    with pytest.raises(ValueError):
        runner.validate(raw, frozen)


def test_check_needs_neither_cache_network_git_nor_writes(monkeypatch):
    original = Path.read_bytes

    def read_bytes(path):
        if "/.cache/nov13-history-repair/" in str(path.resolve()):
            raise AssertionError("uncommitted research capture cannot be a portable dependency")
        return original(path)

    def forbidden(*args, **kwargs):
        raise AssertionError("portable check must not write or use Git")

    monkeypatch.setattr(Path, "read_bytes", read_bytes)
    monkeypatch.setattr(Path, "write_text", forbidden)
    monkeypatch.setattr(runner.subprocess, "check_output", forbidden)
    monkeypatch.setattr(sys, "argv", ["runner", "--check"])
    runner.main()


def test_six_papers_have_reviewed_english_and_truthful_cost_boundaries():
    keys = set(runner.COMPONENTS) | {"mle-star", "alphaevolve"}
    for key in keys:
        spec = json.loads((ROOT / f"src/auto_research/paper_specs/catalog/agent-research/{key}.json").read_text())
        cn = ROOT / "docs" / spec["detail_path"]
        en = cn.with_name("README-en.md").read_text()
        assert "source-sha256: " + hashlib.sha256(cn.read_bytes()).hexdigest() in en
        assert "(README.md)" in en
        assert spec["review_done"] is True
        expected = runner.FULL_STATUS.get(key, "not_reproduced_high_cost")
        assert spec["full_experiment_status"] == expected
        assert spec["requires_gpu_validation"] is False
        assert spec["promotion_eligible"] is False and spec["evolve_integrated"] is False
        assert spec["automatic_retry"] is False and spec["automatic_implementation_queue"] is False
        assert spec["adapter"] is None
        assert spec["implementation_status"] == ("component_only" if key in runner.COMPONENTS else "deferred_high_cost")
