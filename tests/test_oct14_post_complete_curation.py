"""Curation guards use recorded data; fixtures never claim an additional GPU run."""
import copy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT=Path(__file__).resolve().parents[1]
MODULE=runpy.run_path(str(ROOT/"scripts/curate_oct14_post_complete.py"))
HASHES={"synthself":"8fa5c2d74188eae798a9f590c38a2917ebe64f45e93cb832e0cfbb9f9844579c",
        "upturn":"52780127310d86eb17356c0968d113910b96f659d9997ecd87607bf75f13b10e",
        "progressive-contraction":"179bf4d73896074908a445f9e20e87ceba1e1c34c24927349fd19da312706e2d"}
CONFIGS={"synthself":{"epochs":2,"control":"gold-sft","max_tokens":512},
         "upturn":{"steps":2,"gate_epochs":20,"group":4,"cuts":4,"evaluation_group":2,"max_tokens":768},
         "progressive-contraction":{"epochs":3,"prefix_states":2,"branches":4,"pool_ratio":.5,"active_size":1,"max_tokens":512}}


def recorded(key):
    identifier=MODULE["IDENTIFIERS"][key]
    artifact=json.loads((ROOT/f"docs/reproductions/{identifier}-{key}/metrics/public-a100-complete-seed42.json").read_text())
    receipt=json.loads((ROOT/f"docs/gpu-validations/{key}-a100-20261014.json").read_text())
    return artifact,receipt


def fixture(tmp_path,key):
    a,receipt=recorded(key)
    r=copy.deepcopy(a["seed_results"][0]["result"])
    c={"train_examples":8,"validation_examples":4,**CONFIGS[key]}
    config={"shared":{},"methods":{key:c}}
    sha=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    contract={"source_commit":MODULE["COMMITS"][key],"source_file_sha256":receipt["executed_source_sha256"]}
    resources={}
    for role,value in (("teacher" if key=="upturn" else "student",r["checkpoint"]),
                       ("student" if key=="upturn" else "teacher",r["encoder"] if key=="upturn" else r["teacher"])):
        resources[role]={"verified":True,"public_id":value["public_id"],"revision":value["revision"],
                         "file_sha256":value["verified_mirror"]["file_sha256"]}
    audit={**contract,"source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
           "execution_config_sha256":sha,"resources":resources}
    launch={**contract,"seed":42,"job":{"method":key,"overrides":{},
            "timeout_seconds":{"synthself":600,"upturn":900,"progressive-contraction":1800}[key]},"execution_config_sha256":sha,
            "effective_config":c,"command":["python","fixture.py","--method",key,"--seed","42"]}
    exit_record={"exit_code":0,"elapsed_seconds":1.}
    return r,launch,exit_record,contract,audit,config


def invoke(tmp_path,data):
    r,l,e,contract,audit,config=data
    (tmp_path/"evidence").mkdir()
    for path,value in (("evidence/result.json",r),("launch.json",l),("exit.json",e)):
        (tmp_path/path).write_text(json.dumps(value))
    return MODULE["curate"](tmp_path,contract,audit,config,accelerator="fixture-not-additional-CUDA",validated_at="fixture")


@pytest.mark.parametrize("key",HASHES)
def test_actual_complete_record_stays_single_seed_and_source_bound(key):
    a,receipt=recorded(key)
    assert a["seeds"]==a["evaluation_protocol"]["seeds"]==receipt["seeds"]==[42]
    assert a["whole_method_gpu_validation_passed"] is True
    assert a["default_three_seed_plan_completed"] is False
    assert a["evaluation_protocol"]["pending_seeds"]==[43,44]
    assert a["evaluation_protocol"]["formal_comparison"] is False
    assert a["evaluation_protocol"]["promotion_eligible"] is False
    assert all(x["n"]==1 for x in a["aggregate_metrics"].values())
    assert a["provenance"]["code_commit"]==receipt["provenance"]["commit"]==MODULE["COMMITS"][key]
    assert a["provenance"]["raw_result_sha256"]==receipt["provenance"]["raw_result_sha256"]==HASHES[key]
    assert a["provenance"]["dataset_fingerprint"]==hashlib.sha256(json.dumps(a["dataset"],sort_keys=True).encode()).hexdigest()
    assert len(receipt["executed_source_sha256"])==(52 if key=="progressive-contraction" else 53)
    assert MODULE["validate_gpu_receipt"](receipt)==[]
    r=a["seed_results"][0]["result"]
    if key=="upturn":
        assert a["execution_checks"]["assessment_is_training_before_after"] is False
        assert r["baseline"]["pass_rate"]==1. and r["method_metrics"]["pass_rate"]==.75
        assert r["baseline"]["avg_accuracy"]==r["method_metrics"]["avg_accuracy"]==.625
    elif key=="synthself":
        roles=a["execution_checks"]["construction_gold_access"]
        assert "TRAIN" in roles["offline_aligner"] and "TRAIN" in roles["construction_self_rewrite"]
        assert "no current validation gold" in roles["evaluated_student_inference"]
    else:
        assert r["teacher_uncertainty_scores"]==[0.,0.,0.,0.]
        assert r["method_metrics"]["accuracy"]==r["control"]["metrics"]["accuracy"]==.75
        assert a["execution_checks"]["exposure_ratio_is_total_compute_saving"] is False


@pytest.mark.parametrize("key",HASHES)
def test_curation_fixture_accepts_complete_mechanism_without_multi_seed_claim(tmp_path,key):
    a,receipt=invoke(tmp_path,fixture(tmp_path,key))
    assert a["actual_cuda_run_count"]==1 and receipt["result"]=="passed"
    assert a["default_three_seed_plan_completed"] is False


@pytest.mark.parametrize("case",["source","source-files","audit","cuda-audit","config","budget","seed","exit","gold","test","zero-update","zero-gradient","nonfinite","checkpoint","wall","wall-cap"])
def test_source_or_measured_evidence_mismatch_rejected(tmp_path,case):
    data=fixture(tmp_path,"synthself")
    r,l,e,_,audit,_=data
    if case=="source":l["source_commit"]="d"*40
    elif case=="source-files":l["source_file_sha256"]={}
    elif case=="audit":audit["source_hashes_verified"]=False
    elif case=="cuda-audit":audit["cuda_initialized"]=True
    elif case=="config":l["execution_config_sha256"]="d"*64
    elif case=="budget":l["effective_config"]={**l["effective_config"],"max_tokens":1024}
    elif case=="seed":r["seed"]=43
    elif case=="exit":e["exit_code"]=1
    elif case=="gold":r["protocol"]["gold_in_student_generation"]=True
    elif case=="test":r["dataset"]["test_read"]=True
    elif case=="zero-update":r["training"][0]["optimizer_update_executed"]=False
    elif case=="zero-gradient":r["training"][0]["gradient_l2_norm"]=0.
    elif case=="nonfinite":r["training"][0]["loss"]=float("nan")
    elif case=="wall":e["elapsed_seconds"]=601.
    elif case=="wall-cap":l["job"]["timeout_seconds"]=900
    else:r["checkpoint"]["revision"]="other"
    with pytest.raises(ValueError):invoke(tmp_path,data)


@pytest.mark.parametrize("key,case",[("synthself","eq6"),("synthself","partial"),("synthself","fabricated-eos"),
    ("synthself","control"),("upturn","zero-rescue"),("upturn","invented-advantage"),
    ("upturn","cut"),("upturn","generation-budget"),("upturn","baseline-examples"),("upturn","method-examples"),("progressive-contraction","profile"),
    ("progressive-contraction","pool"),("progressive-contraction","route"),("progressive-contraction","exposure")])
def test_defining_mechanism_corruption_rejected(tmp_path,key,case):
    data=fixture(tmp_path,key)
    r=data[0]
    if case=="eq6":r["empirical_aligner_constraints"]["rewrite_sequence_nll"]=1000.
    elif case=="partial":r["rewrites"][0]["truncated"]=True
    elif case=="fabricated-eos":r["rewrites"][0]["rewrite_canonical_eos_appended"]=True
    elif case=="control":r["control"]["method"]="other"
    elif case=="zero-rescue":r["training"][0]["rescue_rewards"]=[0.]*4
    elif case=="invented-advantage":r["training"][0]["advantages"][0]=10.
    elif case=="cut":r["training_rollout_audits"][0]["paragraph_cut_indices"]=[9999]
    elif case=="generation-budget":r["generation_budget_controls"][0]["base_generations"]=8
    elif case=="baseline-examples":r["baseline"]["examples"]=3
    elif case=="method-examples":r["method_metrics"]["examples"]=3
    elif case=="profile":r["teacher_audits"][0]["profile"][0]["uncertainty"]=.5
    elif case=="pool":r["teacher_pool_indices"]=[2,3]
    elif case=="route":r["learner_routes"][0]["active_indices"]=[0]
    else:r["exposure"]["full_sft_control"]=4
    with pytest.raises(ValueError):invoke(tmp_path,data)
