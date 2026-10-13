"""Recorded full SOAR evidence guards; CPU fixtures are not new GPU runs."""
import copy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT=Path(__file__).resolve().parents[1]
MODULE=runpy.run_path(str(ROOT/"scripts/curate_oct14_soar_complete.py"))
PUBLIC=json.loads((ROOT/MODULE["METRIC"]).read_text())
RECEIPT=json.loads((ROOT/MODULE["RECEIPT"]).read_text())


def fixture(tmp_path):
    rows=copy.deepcopy(PUBLIC["seed_results"][0]["variants"])
    policy=rows["source-consistent"]["checkpoint"]
    shared={"student_path":"fixture-public","student_id":policy["public_id"],"student_revision":policy["revision"],
        "validation_examples":4,"context_limit":4096,"learning_rate":1e-5}
    settings={"train_examples":8,"steps":4,"group":4,"max_turns":3,"max_tokens":256,"verifier":"normalized-em"}
    config={"shared":shared,"methods":{"soar":settings}}
    canonical=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    contract={"source_commit":MODULE["COMMIT"],"source_file_sha256":RECEIPT["executed_source_sha256"]}
    corpus=rows["source-consistent"]["corpus"]
    audit={**contract,"source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
        "execution_config_sha256":canonical,"resources":{"student":{"verified":True,"public_id":policy["public_id"],
            "revision":policy["revision"],"file_sha256":policy["verified_mirror"]["file_sha256"]}},
        "method_specific_holdouts":{"soar":{"status":"verified","tool_groups_disjoint":True,"holdout":PUBLIC["dataset"]}},
        "soar_corpus":{**corpus,"status":"verified","generation_inputs_do_not_include_qa_answers":True}}
    directories=[]
    for variant,r in rows.items():
        d=tmp_path/variant
        (d/"evidence").mkdir(parents=True)
        launch={**contract,"seed":42,"execution_config_sha256":canonical,"effective_config":{**shared,**settings,"variant":variant},
            "job":{"timeout_seconds":1800},"gpu_slot_grant":"A100-post-training-explicit-slot",
            "command":["python","fixture-not-new-GPU","--method","soar","--seed","42","--variant",variant]}
        for p,value in (("evidence/result.json",r),("launch.json",launch),("exit.json",{"exit_code":0,"elapsed_seconds":1.})):
            (d/p).write_text(json.dumps(value))
        directories.append(d)
    return directories,contract,audit,config


def test_actual_complete_soar_record_has_two_arms_one_seed_and_real_updates():
    assert PUBLIC["seeds"]==RECEIPT["seeds"]==[42]
    assert PUBLIC["default_three_seed_plan_completed"] is False and PUBLIC["actual_cuda_run_count"]==2
    assert PUBLIC["evaluation_protocol"]["pending_seeds"]==[43,44]
    assert PUBLIC["evaluation_protocol"]["formal_comparison"] is False
    assert PUBLIC["evaluation_protocol"]["variants_are_independent_seeds"] is False
    checks=PUBLIC["execution_checks"]
    assert checks["source-consistent"]["actual_optimizer_updates"]==4
    assert checks["without-source-reward"]["actual_optimizer_updates"]==3
    assert checks["without-source-reward"]["equal_reward_groups_skipped"]==1
    assert PUBLIC["provenance"]["raw_results_sha256"]=={
        "source-consistent":"f0597403b4e7f02ff5e9e5c70def793f5c4c8c38ea406efbcbd86e9bd8267d9b",
        "without-source-reward":"3e8f9a849a9e9aa2557b0ee0d15fc270dce73406b2d7a650c03980f08ccd5409"}
    for variant,row in PUBLIC["seed_results"][0]["variants"].items():
        assert row["baseline"]["accuracy"]==0. and row["method_metrics"]["accuracy"]==.25
        assert row["method_metrics"]["format_compliance"]==.5
        assert MODULE["training_check"](row)["actual_optimizer_updates"]==checks[variant]["actual_optimizer_updates"]
    assert PUBLIC["aggregate_metrics"]["source-consistent.validation.source_consistency"]["mean"]==.5
    assert PUBLIC["aggregate_metrics"]["without-source-reward.validation.source_consistency"]["mean"]==.25


def test_complete_cpu_fixture_is_source_bound_but_not_additional_cuda(tmp_path):
    a,r=MODULE["curate"](*fixture(tmp_path))
    assert a["seeds"]==r["seeds"]==[42] and a["default_three_seed_plan_completed"] is False


@pytest.mark.parametrize("case",["source","source-files","audit","cuda","resource","corpus","holdout","config",
    "budget","exit","wall","seed","gold","validation-count","zero-update","reward","advantage","zero-pseudo","gradient","nonfinite","duplicate"])
def test_complete_soar_rejects_mismatched_or_fabricated_evidence(tmp_path,case):
    directories,contract,audit,config=fixture(tmp_path)
    d=directories[0]
    raw=d/"evidence/result.json"
    r=json.loads(raw.read_text())
    l=json.loads((d/"launch.json").read_text())
    e=json.loads((d/"exit.json").read_text())
    if case=="source":contract["source_commit"]="0"*40
    elif case=="source-files":l["source_file_sha256"]={}
    elif case=="audit":audit["source_hashes_verified"]=False
    elif case=="cuda":audit["cuda_initialized"]=True
    elif case=="resource":audit["resources"]["student"]["verified"]=False
    elif case=="corpus":audit["soar_corpus"]["generation_inputs_do_not_include_qa_answers"]=False
    elif case=="holdout":audit["method_specific_holdouts"]["soar"]["tool_groups_disjoint"]=False
    elif case=="config":l["execution_config_sha256"]="0"*64
    elif case=="budget":l["effective_config"]["max_tokens"]=512
    elif case=="exit":e["exit_code"]=1
    elif case=="wall":e["elapsed_seconds"]=1801.
    elif case=="seed":r["seed"]=43
    elif case=="gold":r["protocol"]["gold_in_student_generation"]=True
    elif case=="validation-count":r["method_metrics"]["examples"]=3
    elif case=="zero-update":r["parameters_changed"]=False
    elif case=="duplicate":directories[1]=directories[0]
    elif case=="zero-pseudo":
        zero=PUBLIC["seed_results"][0]["variants"]["without-source-reward"]["training"][0]
        r["training"][0]=copy.deepcopy(zero)
        r["variant"]="without-source-reward"
        r["training"][0].update(optimizer_update_executed=True,trajectory_advantages=[.01]*4)
    else:
        step=next(s for s in r["training"] if s["optimizer_update_executed"])
        if case=="reward":step["trajectory_rewards"][0]+=1.
        elif case=="advantage":step["trajectory_advantages"][0]=10.
        elif case=="gradient":step["gradient_l2_norm"]=0.
        else:step["loss"]=float("nan")
    raw.write_text(json.dumps(r))
    (d/"launch.json").write_text(json.dumps(l))
    (d/"exit.json").write_text(json.dumps(e))
    with pytest.raises(ValueError):MODULE["curate"](directories,contract,audit,config)
