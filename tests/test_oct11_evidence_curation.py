import importlib.util
from copy import deepcopy
import json
from pathlib import Path

import pytest


def module():
    spec = importlib.util.spec_from_file_location("oct11_curation", "scripts/curate_oct11_checkpoint_evidence.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_vfold_memory_summary_excludes_different_cache_lengths():
    report = {"adapter_key": "vfold", "seed": 42, "diagnostic_only": True,
              "exact_fold_relative_logit_error": .01, "rows": [
                  {"example": 0, "recipe": "full", "cache_tokens": 100, "persistent_cache_bytes": 1000},
                  {"example": 0, "recipe": "vfold", "cache_tokens": 90, "persistent_cache_bytes": 500},
                  {"example": 1, "recipe": "full", "cache_tokens": 100, "persistent_cache_bytes": 1000},
                  {"example": 1, "recipe": "vfold", "cache_tokens": 100, "persistent_cache_bytes": 850}]}
    metrics, pairs = module().summarize("vfold", report)
    assert [p["example"] for p in pairs] == [1]
    assert metrics["matched_length_cache_reduction_mean"] == pytest.approx(.15)
    report["exact_fold_relative_logit_error"] = .03
    with pytest.raises(ValueError, match="function check"):
        module().summarize("vfold", report)


def test_zcpo_skip_only_run_cannot_be_archived_as_actual_training():
    report = {"adapter_key": "zcpo", "seed": 42, "diagnostic_only": True,
              "metrics": {"active_groups": 0, "adapter_parameter_delta_l2": 0.},
              "history": [{"active": False}]}
    with pytest.raises(ValueError, match="active updates"):
        module().summarize("zcpo", report)


def test_committed_opd_features_are_all_layers_and_receipt_source_is_exact():
    report = json.loads(Path("docs/post-training/2610.11247-opd-learning-signals/metrics/checkpoint-a100-seed42.json").read_text())
    runtime = report["runtime_details"]
    assert len(runtime["layerwise_prompt_cka"]) == len(runtime["representation_positions"]) == 37
    assert runtime["parameter_scope"].startswith("LoRA adapter")
    receipt = json.loads(Path("docs/gpu-validations/opd-learning-signals-a100-20261011.json").read_text())
    assert receipt["provenance"]["commit"] == report["provenance"]["original_code_commit"]
    assert "scripts/run_opd_learning_signals.py" in receipt["executed_source_sha256"]


def sparse_module():
    spec = importlib.util.spec_from_file_location("sparse_curation", "scripts/curate_sparse_decoding_evidence.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def sparse_report():
    path = Path("docs/foundation-models/2610.12327-sparse-decoding/metrics/checkpoint-a100-seed42.json")
    return deepcopy(json.loads(path.read_text())["runtime_details"])


def test_sparse_curation_preserves_quality_loss_and_truncations():
    metrics = sparse_module().summarize(sparse_report())
    assert metrics["dense"]["bounded_exact_match"] == 1
    assert metrics["decode-wanda-bitmask"]["bounded_exact_match"] == .25
    assert metrics["decode-wanda-bitmask"]["truncated_examples"] == 3
    assert metrics["fixed-text-wanda-bitmask"]["eos_completion_fraction"] == .25


@pytest.mark.parametrize("corruption", ["calls", "eos", "calibration", "test"])
def test_sparse_curation_rejects_corrupted_execution_accounting(corruption):
    report = sparse_report()
    if corruption == "calls":
        report["sparse_calls"] += 1
    elif corruption == "eos":
        report["rows"][0]["truncated"] = report["rows"][0]["ended_with_eos"]
    elif corruption == "calibration":
        key = next(iter(report["calibration"]["counts"]))
        report["calibration"]["counts"][key] += 1
    else:
        report["test_read"] = True
    with pytest.raises(ValueError):
        sparse_module().summarize(report)
