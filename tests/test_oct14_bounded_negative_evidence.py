"""Actual bounded failures/probes remain negative, never fabricated receipts."""
import hashlib
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("method,identifier,name,commit,count",[
    ("magicbeanstalk","2610.12659","public-a100-bounded-failed-seed42-0f5dca9f.json","0f5dca9f7f0319c6e3bb57aa578cfe26499a6e7e",52),
    ("soar","2610.13157","public-a100-train-format-probe-seed42-57b2314d.json","57b2314db1d5b8a8ebeb0aa7fbb6b7fee523df55",54)])
def test_actual_stage_not_receipt_and_no_fabricated_policy_updates(method,identifier,name,commit,count):
    a=json.loads((ROOT/f"docs/reproductions/{identifier}-{method}/metrics"/name).read_text())
    assert a["schema_version"]==2 and a["not_gpu_receipt"] is True
    assert a["whole_method_gpu_validation_passed"] is False
    assert a["diagnostic_only"] is True and a["promotion_eligible"] is False
    assert a["seeds"]==a["evaluation_protocol"]["seeds"]==[42]
    assert a["evaluation_protocol"]["formal_comparison"] is False
    assert a["provenance"]["code_commit"]==commit
    assert len(a["provenance"]["executed_source_sha256"])==count
    assert a["provenance"]["dataset_fingerprint"]==hashlib.sha256(json.dumps(a["dataset"],sort_keys=True).encode()).hexdigest()
    assert len(a["provenance"]["raw_result_sha256"])==64 and len(a["provenance"]["raw_launch_sha256"])==64
    assert all(x["n"]==1 for x in a["aggregate_metrics"].values())
    r=a["seed_results"][0]["stage_result"]
    if method=="magicbeanstalk":
        selection=r["hard_root_selection"]
        assert selection["calibrated_training_candidates"]==16 and selection["hard_root_limit"]==4
        assert selection["selected_training_root_indices"]==[4,7,8] and selection["tree_construction_attempts"]==3
        assert selection["paired_rl_root_indices"]==[]
        assert a["execution_checks"]["method_rl_updates"]==a["execution_checks"]["control_rl_updates"]==0
        assert a["execution_checks"]["construction_failed_without_complete_gate_trace"] is True
        assert not ({"mbs_rlvr","seed_rlvr_control"}&r["cost"]["generation_calls"].keys())
        assert r["cost"]["generated_tokens"]["effectivity_student"]==1231
        assert r["cost"]["generated_tokens"]["effectivity_teacher"]==1038
    else:
        assert r["whole_method_gpu_validation_passed"] is False
        assert r["lora_updates"]==r["optimizer_updates"]==0
        assert r["assessment_executed"] is False and r["validation_content_read"] is False and r["test_content_read"] is False
        assert r["diagnosis_status"]=="no-format-signal" and len(r["training_episode_audits"])==8
        assert r["total_searches"]==r["valid_format_episodes"]==r["source_match_episodes"]==0
        assert all(x["final_action_kind"]=="invalid" and not x["turns"][0]["truncated"] for x in r["training_episode_audits"])
        assert sum(r["cost"]["generated_tokens"].values())==433
        assert r["checkpoint"]["policy"]["public_id"]=="Qwen/Qwen2.5-7B-Instruct"
