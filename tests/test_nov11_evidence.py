"""Reject evidence promotion, device drift and missing seed rows in this batch."""
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from curate_nov11_components import validate_raw  # noqa: E402
from run_nov11_components import AUDIT, COMPONENTS, CUDA_KEYS  # noqa: E402


@pytest.fixture
def frozen():
    return json.loads((AUDIT / "frozen-sources.json").read_text())


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_actual_frozen_evidence_and_fixed_scope(device, frozen):
    raw = json.loads((AUDIT / f"raw-{device}.json").read_text())
    validate_raw(raw, device, frozen)
    assert set(raw["components"]) == (set(COMPONENTS) if device == "cpu" else CUDA_KEYS)


@pytest.mark.parametrize("field,value", [
    ("promotion_eligible", True), ("formal_comparison", True),
    ("evolve_integrated", True), ("pretrained_model_calls", 1),
    ("full_experiments_executed", True), ("automatic_retry", True),
    ("elapsed_seconds", 181), ("elapsed_seconds", float("nan")),
    ("accelerator", "CPU"), ("code_commit", "0" * 40),
])
def test_tampered_cuda_provenance_is_rejected(field, value, frozen):
    raw = json.loads((AUDIT / "raw-cuda.json").read_text())
    raw[field] = value
    with pytest.raises(ValueError):
        validate_raw(raw, "cuda", frozen)


def test_missing_or_relabelled_seed_rows_are_rejected(frozen):
    raw = json.loads((AUDIT / "raw-cuda.json").read_text())
    broken = deepcopy(raw)
    broken["components"]["adindex"]["per_seed"].pop()
    with pytest.raises(ValueError):
        validate_raw(broken, "cuda", frozen)
    broken = deepcopy(raw)
    broken["components"]["adindex"]["per_seed"][0]["execution_device"] = "cpu"
    with pytest.raises(ValueError):
        validate_raw(broken, "cuda", frozen)


def test_high_cost_reference_has_no_fake_capability_or_receipt():
    spec = json.loads((ROOT / "src/auto_research/paper_specs/catalog/agent-research/alphaproof-code.json").read_text())
    assert spec["adapter"] is None
    assert not spec["requires_gpu_validation"]
    assert spec["full_experiment_status"] == "not_reproduced_high_cost"
    assert spec["full_experiment_review_done"] is True
    assert spec["promotion_eligible"] is False
    assert spec["evolve_integrated"] is False
