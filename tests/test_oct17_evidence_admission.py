"""Pure admission tests: never fabricate or write a GPU receipt."""
from copy import deepcopy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("oct17_admission", ROOT / "scripts/curate_oct17_component_evidence.py")
CURATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CURATOR)


def test_admission_rejects_cpu_fallback_and_incomplete_seed_coverage():
    with pytest.raises(ValueError, match="CPU fallback"):
        CURATOR.validate({"device": "cpu"}, "foundation")
    payload = {"device": "cuda", "accelerator": "NVIDIA A100", "diagnostic_only": True,
               "promotion_eligible": False, "seeds": [42]}
    with pytest.raises(ValueError, match="three fixed seeds"):
        CURATOR.validate(payload, "foundation")


def test_nonfinite_metrics_are_not_accepted():
    with pytest.raises(ValueError, match="nonfinite"):
        CURATOR.finite_tree({"nested": [{"metric": float("nan")}]})


@pytest.mark.parametrize("failure", [{"status": "failed"}, {"result": "partial"},
                                    {"error": "failed after final metric snapshot"}])
def test_explicit_failure_cannot_be_rewritten_as_passed(failure):
    with pytest.raises(ValueError):
        CURATOR.reject_explicit_failure(failure)


def test_partial_or_failed_bit_roundtrip_cannot_be_passed_by_runner_label():
    metrics = {"all_bf16_exponents_bitwise_roundtrip": True, "roomy_buffer_roundtrip": True,
               "autograd_matches_dense": True, "overflow_raw_tail_bytes": 8}
    CURATOR.validate_measurement("lct", metrics)
    broken = deepcopy(metrics)
    broken["all_bf16_exponents_bitwise_roundtrip"] = False
    with pytest.raises(ValueError, match="roundtrip failed"):
        CURATOR.validate_measurement("lct", broken)
    broken = deepcopy(metrics)
    broken["overflow_raw_tail_bytes"] = 0
    with pytest.raises(ValueError, match="must be positive"):
        CURATOR.validate_measurement("lct", broken)


def test_sample_statistics_are_recomputed_and_preserve_negative_results():
    rows = [{"seed": s, "metrics": {"signed_loss": v, "checks": True}}
            for s, v in zip((42, 43, 44), (-3., -2., -1.), strict=True)]
    assert CURATOR.average(rows) == {"checks": True, "signed_loss": {"mean": -2., "std": 1., "n": 3}}
    rows[-1]["metrics"].pop("checks")
    with pytest.raises(ValueError, match="fields differ"):
        CURATOR.average(rows)
