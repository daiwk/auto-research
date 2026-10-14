"""Actual stage evidence stays explicitly below whole-method GPU acceptance."""
import hashlib
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
RAW_HASHES={"synthself":"5943fd24eb44f23ff6c18cab4f0ec20cc15f74777bf1a8137407b887cd712c3f",
            "upturn":"558f2b3996a954a3f79be94d8cae17997af6692dc901f5605834dbb792c7f31e"}


@pytest.mark.parametrize("key,identifier",[("synthself","2610.13113"),("upturn","2610.13672")])
def test_actual_train_stage_not_receipt_and_no_lora_validation_or_test(key,identifier):
    p=ROOT/f"docs/reproductions/{identifier}-{key}/metrics/public-a100-train-diagnosis-seed42-51b4718a.json"
    x=json.loads(p.read_text())
    assert x["schema_version"]==2 and x["not_gpu_receipt"] is True and x["whole_method_gpu_validation_passed"] is False
    assert x["seeds"]==x["evaluation_protocol"]["seeds"]==[42]
    assert x["provenance"]["code_commit"]=="51b4718a76da286b4111c6fc7d8e003d436def72"
    assert x["provenance"]["dataset_fingerprint"]==hashlib.sha256(json.dumps(x["dataset"],sort_keys=True).encode()).hexdigest()
    r=x["seed_results"][0]["stage_result"]
    assert r["whole_method_gpu_validation_passed"] is False and r["lora_updates"]==0
    assert r["assessment_executed"] is False and r["validation_content_read"] is False and r["test_content_read"] is False
    assert len(r["core_source_sha256"])==53
    assert r["core_source_sha256"]["scripts/diagnose_oct14_post_training.py"]==r["diagnostic_runner_sha256"]
    assert r["diagnostic_outputs_usable"] is True
    if key=="synthself":
        c=r["empirical_aligner_constraints"]
        assert c["all_naturally_complete"] and c["strict_eq6_satisfied"]
        assert c["rewrite_sequence_nll"]<c["gold_sequence_nll"] and c["aligner_quality"]>c["self_quality"]
        assert len(r["training_rewrite_audits"])==8
    else:
        assert len(r["training_rollout_audits"])==32 and r["eligible_failed_rollouts"]==16
        assert r["position_informative_groups"]==2
        assert all(s["nonzero_rescue_advantage"] and s["gradient_l2_norm"]>0 and s["optimizer_update_executed"]
                   for s in r["position_training"])
    assert x["provenance"]["raw_result_sha256"]==RAW_HASHES[key]
