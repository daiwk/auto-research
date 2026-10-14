"""Actual failed44 is not silently accepted by a descriptive three-seed cohort."""
import copy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT=Path(__file__).resolve().parents[1]
DOC=ROOT/"docs/reproductions/2610.13672-upturn/metrics"


def module(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT/"scripts"))
    return runpy.run_path(str(ROOT/"scripts/curate_oct14_upturn_cohort.py"))


def failed():
    a=json.loads((DOC/"public-a100-complete-failed-seed44.json").read_text())
    return a,a["seed_results"][0]["result"]


def config():
    return {"train_examples":8,"validation_examples":4,"max_tokens":768,"group":4,
            "steps":2,"cuts":4,"gate_epochs":20,"evaluation_group":2}


def test_actual_failed44_keeps_zero_rescue_and_negative_assessment():
    a,r=failed()
    assert a["not_gpu_receipt"] is True and a["whole_method_gpu_validation_passed"] is False
    assert a["execution_complete"] is True and a["all_seed_mechanism_passed"] is False
    assert a["seeds"]==[44] and r["execution_status"]=="failed-no-rescue-signal"
    assert r["position_informative_groups"]==0
    assert all(not any(s["advantages"]) and not any(s["rescue_rewards"]) for s in r["training"])
    assert a["execution_checks"]["actual_position_optimizer_calls"]==a["execution_checks"]["entropy_only_position_updates"]==2
    assert r["baseline"]["avg_accuracy"]==.6875 and r["method_metrics"]["avg_accuracy"]==.625
    assert r["baseline"]["pass_rate"]==1. and r["method_metrics"]["pass_rate"]==.75
    assert a["provenance"]["raw_result_sha256"]=="cdf14bdcf8e8dd49653a7714fbca0d9e9e61fa857f73316d6faa42e5289d454e"
    assert a["provenance"]["dataset_fingerprint"]==hashlib.sha256(json.dumps(a["dataset"],sort_keys=True).encode()).hexdigest()


def test_three_execution_cohort_is_not_three_seed_passed_receipt():
    a=json.loads((DOC/"public-a100-complete-three-seed-execution-cohort.json").read_text())
    assert a["seeds"]==[42,43,44] and a["execution_complete"] is True
    assert a["seed_execution_status"]=={"42":"passed","43":"passed","44":"failed-no-rescue-signal"}
    assert a["all_seed_mechanism_passed"] is False and a["accepted_mechanism_aggregate"] is False
    assert a["three_seed_passed_gpu_receipt_issued"] is False and a["accepted_mechanism_seed_count"]==2
    assert a["not_gpu_receipt"] is True and a["whole_method_gpu_validation_passed"] is False
    assert a["evaluation_protocol"]["formal_comparison"] is False and a["evaluation_protocol"]["promotion_eligible"] is False
    assert all(k.startswith("descriptive_all_executed_seeds.") and m["n"]==3 for k,m in a["aggregate_metrics"].items())
    assert a["provenance"]["raw_results_sha256"]["44"]==failed()[0]["provenance"]["raw_result_sha256"]
    old=json.loads((ROOT/"docs/gpu-validations/upturn-a100-20261014.json").read_text())
    assert old["seeds"]==[42] and old["provenance"]["commit"]==a["provenance"]["code_commit"]


@pytest.mark.parametrize("case",["diagnostic","promotion","train-cap","val-cap","response-cap","zero-gradient","negative-gradient","nonfinite-gradient","fake-rescue","fake-advantage"])
def test_failed44_guard_cannot_fabricate_or_relabel_execution(monkeypatch,case):
    r=copy.deepcopy(failed()[1])
    if case=="diagnostic":r["diagnostic_only"]=False
    elif case=="promotion":r["promotion_eligible"]=True
    elif case=="train-cap":r["protocol"]["train_examples"]=16
    elif case=="val-cap":r["protocol"]["validation_examples"]=8
    elif case=="response-cap":r["protocol"]["max_tokens"]=1024
    elif case=="zero-gradient":r["training"][0]["gradient_l2_norm"]=0.
    elif case=="negative-gradient":r["training"][0]["gradient_l2_norm"]=-1.
    elif case=="nonfinite-gradient":r["training"][0]["gradient_l2_norm"]=float("nan")
    elif case=="fake-rescue":r["training"][0]["rescue_rewards"][0]=.5
    else:r["training"][0]["advantages"][0]=.5
    with pytest.raises(ValueError):module(monkeypatch)["validate_failed"](r,config())


def test_resource_false_audit_rejected_without_reading_or_loading_models(tmp_path,monkeypatch):
    a=json.loads((DOC/"public-a100-complete-three-seed-execution-cohort.json").read_text())
    c=config()
    execution={"shared":{},"methods":{"upturn":c}}
    canonical=hashlib.sha256(json.dumps(execution,sort_keys=True).encode()).hexdigest()
    contract={"source_commit":a["provenance"]["code_commit"],"source_file_sha256":a["provenance"]["executed_source_sha256"]}
    r0=a["seed_results"][0]["result"]
    resources={role:{"public_id":r["public_id"],"revision":r["revision"],
                    "file_sha256":r["verified_mirror"]["file_sha256"],"verified":False}
               for role,r in (("teacher",r0["checkpoint"]),("student",r0["encoder"]))}
    audit={**contract,"source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
           "execution_config_sha256":canonical,"resources":resources,"public_train_only_holdout":a["dataset"]}
    dirs=[]
    for row in a["seed_results"]:
        seed=row["seed"]
        d=tmp_path/str(seed)
        (d/"evidence").mkdir(parents=True)
        (d/"evidence/result.json").write_text(json.dumps(row["result"]))
        (d/"launch.json").write_text(json.dumps({**contract,"seed":seed,"job":{"method":"upturn","overrides":{},"timeout_seconds":900},
            "effective_config":c,"execution_config_sha256":canonical,"command":["python","fixture.py","--method","upturn","--seed",str(seed)]}))
        (d/"exit.json").write_text(json.dumps({"exit_code":1 if seed==44 else 0,"elapsed_seconds":1.}))
        dirs.append(d)
    with pytest.raises(ValueError,match="checkpoint|resource"):
        module(monkeypatch)["make"](dirs,contract,audit,execution)
