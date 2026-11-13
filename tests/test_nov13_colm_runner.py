import copy

import pytest

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
