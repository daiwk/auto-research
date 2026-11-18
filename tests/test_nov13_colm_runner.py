import copy
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from curate_nov13_colm_evidence import validate_admission
from run_nov13_colm_components import COMPONENTS, CUDA_KEYS, preflight, tier, validate_diagnostic


def test_exact_budget_and_tiers():
    assert len(COMPONENTS) == 23
    assert len(CUDA_KEYS) == 7
    assert preflight()["maximum_run_seconds"] == 180
    assert preflight()["maximum_cuda_devices"] == 1
    assert preflight()["pretrained_model_calls"] == preflight()["api_calls"] == 0
    assert tier("policybank") == tier("mmeb-v3") == tier("avmeme-exam") == "l0_interface"


def test_rejects_changed_evidence_tier_failed_checks_or_nonfinite_metrics():
    row = {"seed": 42, "diagnostic_only": True, "evaluation_tier": "l0_interface",
           "checks": {"explicit": True}, "metrics": {"count": 2}}
    validate_diagnostic(row, 42, "policybank")
    for field, value in [("evaluation_tier", "l1_mechanism"), ("checks", {"explicit": False}),
                         ("checks", {"explicit": 1}), ("metrics", {"count": float("nan")}),
                         ("metrics", {"count": True}), ("diagnostic_only", False)]:
        wrong = copy.deepcopy(row)
        wrong[field] = value
        with pytest.raises(ValueError):
            validate_diagnostic(wrong, 42, "policybank")


def test_admission_rejects_conflicting_labels_and_component_device():
    import json
    audit = Path(__file__).resolve().parents[1] / "docs/research-audits/nov13-colm-remaining"
    raw = json.loads((audit / "raw-cuda.json").read_text())
    frozen = json.loads((audit / "frozen-sources.json").read_text())
    validate_admission(raw, frozen)
    for field, value in [("diagnostic_only", False), ("pretrained_model_calls", 1),
                         ("evolve_integrated", True), ("automatic_retry", True),
                         ("full_experiments_executed", True)]:
        wrong = copy.deepcopy(raw)
        wrong[field] = value
        with pytest.raises(ValueError):
            validate_admission(wrong, frozen)
    wrong = copy.deepcopy(raw)
    wrong["components"]["lidas"]["per_seed"][0]["device"] = "cpu"
    with pytest.raises(ValueError, match="device"):
        validate_admission(wrong, frozen)
