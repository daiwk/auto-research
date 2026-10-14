"""Repaired five-arm ledger tests are CPU-only, not independent seeds or GPU runs."""
import copy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT=Path(__file__).resolve().parents[1]
MODULE=runpy.run_path(str(ROOT/"scripts/curate_oct14_curriculum_repaired.py"))


def fixture(variant="unfiltered"):
    rate=.75 if variant=="staged" else .25 if variant=="too-hard" else .5
    history=[[rate]*8 for _ in range(4)]
    schedule=MODULE["PlateauSchedule"]()
    training=[]
    for step in range(4):
        band=MODULE["BANDS"][schedule.stage] if variant=="staged" else MODULE["BANDS"][4] if variant=="too-hard" else MODULE["BANDS"][2]
        groups=[]
        for row in range(8):
            eligible=variant!="static" or step*2<=row<(step+1)*2
            g={"training_row":row,"eligible":eligible,"current_success":rate}
            if eligible:
                correctness=[1.]*int(rate*8)+[0.]*(8-int(rate*8))
                rewards=[x+.2 for x in correctness]
                mean=sum(rewards)/8
                std=(sum((x-mean)**2 for x in rewards)/8)**.5
                g.update(correctness_rewards=correctness,rewards=rewards,advantages=[(x-mean)/(std+1e-6) for x in rewards],
                    optimizer_update_executed=True,zero_advantage_group=False,gradient_l2_norm=.1)
            groups.append(g)
        transition=schedule.observe(.5) if variant=="staged" else "not-staged"
        training.append({"step":step+1,"band":band,"groups":groups,"effective_updates":sum(g["eligible"] for g in groups),
            "validation_diagnostic":{"accuracy":.5,"examples":4},"transition":transition})
    return {"variant":variant,"difficulty_history":history,"training":training,
        "initial_static_easy_to_hard_order":list(range(8)) if variant=="static" else None,
        "difficulty_dynamics":MODULE["difficulty_dynamics"](history)}


@pytest.mark.parametrize("variant",sorted(MODULE["VARIANTS"]))
def test_cpu_all_five_arms_replay_original_gate_and_schedule(variant):
    result=MODULE["audit_training"](fixture(variant))
    assert result["all_groups_audited"]==32
    assert result["actual_optimizer_updates"]==(8 if variant=="static" else 32)


def test_actual_five42_stage_keeps_zero_groups_negative_staged_and_incomplete_default_plan():
    path=ROOT/"docs/reproductions/2610.13669-grpo-difficulty-curriculum/metrics/public-a30-complete-five-arms-seed42-b9086275.json"
    a=json.loads(path.read_text())
    assert a["seeds"]==[42] and a["actual_cuda_run_count"]==5
    assert a["not_gpu_receipt"] is True and a["whole_method_gpu_validation_passed"] is False
    assert a["default_three_seed_plan_completed"] is False
    assert a["evaluation_protocol"]["variants_are_independent_seeds"] is False
    assert a["evaluation_protocol"]["formal_comparison"] is False
    rows=a["seed_results"][0]["variants"]
    checks=a["execution_checks"]["42"]
    assert [checks[v]["actual_optimizer_updates"] for v in ("unfiltered","static","fixed-medium","staged","too-hard")]==[19,4,7,10,10]
    assert checks["unfiltered"]["mathematically_equal_reward_groups_skipped"]==13
    assert checks["static"]["mathematically_equal_reward_groups_skipped"]==4
    assert rows["staged"]["method_metrics"]["accuracy"]==0.
    assert all(checks[v]["equal_reward_optimizer_updates"]==0 for v in MODULE["VARIANTS"])
    assert len(a["provenance"]["raw_results_sha256"])==5
    assert a["provenance"]["artifact_path"]==str(path.relative_to(ROOT))
    assert all(MODULE["audit_training"](r)["actual_optimizer_updates"]==checks[v]["actual_optimizer_updates"] for v,r in rows.items())


def test_equal_group_missing_advantages_is_recorded_not_fabricated_or_dropped():
    r=fixture()
    g=r["training"][0]["groups"][0]
    g.update(correctness_rewards=[0.]*8,rewards=[.2]*8,current_success=0.,optimizer_update_executed=False,zero_advantage_group=True)
    del g["advantages"]
    r["difficulty_history"][0][0]=0.
    r["difficulty_dynamics"]=MODULE["difficulty_dynamics"](r["difficulty_history"])
    r["training"][0]["effective_updates"]-=1
    out=MODULE["audit_training"](r)
    assert out["eligible_groups"]==32 and out["actual_optimizer_updates"]==31
    assert out["mathematically_equal_reward_groups_skipped"]==1
    ledger=out["actual_zero_group_ledgers"][0]
    assert ledger["advantages_recorded"] is None and ledger["advantages_field_present"] is False


@pytest.mark.parametrize("case",["equal-pseudo","rejected-update","count","band","history","dynamics","order","transition","advantage","gradient"])
def test_ledger_cannot_hide_pseudo_updates_or_change_curriculum(case):
    r=fixture("static" if case in ("rejected-update","order") else "staged" if case=="transition" else "unfiltered")
    g=r["training"][0]["groups"][0]
    if case=="equal-pseudo":
        g.update(correctness_rewards=[0.]*8,rewards=[.2]*8,advantages=[-.014901161193847656]*8,current_success=0.)
        r["difficulty_history"][0][0]=0.
        r["difficulty_dynamics"]=MODULE["difficulty_dynamics"](r["difficulty_history"])
    elif case=="rejected-update":r["training"][0]["groups"][7]["optimizer_update_executed"]=True
    elif case=="count":r["training"][0]["effective_updates"]-=1
    elif case=="band":r["training"][0]["band"]=(0.,1.)
    elif case=="history":r["difficulty_history"][0][0]=0.
    elif case=="dynamics":r["difficulty_dynamics"]["span"][0]=1.
    elif case=="order":r["initial_static_easy_to_hard_order"]=list(reversed(range(8)))
    elif case=="transition":r["training"][0]["transition"]="advance"
    elif case=="advantage":g["advantages"][0]=10.
    else:g["gradient_l2_norm"]=0.
    with pytest.raises(ValueError):MODULE["audit_training"](copy.deepcopy(r))


def run_fixture(tmp_path):
    public=json.loads((ROOT/"docs/reproductions/2610.13669-grpo-difficulty-curriculum/metrics/public-legacy-curriculum-numerical-negative.json").read_text())
    soar_receipt=json.loads((ROOT/"docs/gpu-validations/soar-a100-20261014-seed42.json").read_text())
    policy=public["checkpoint"]
    shared={"student_path":"fixture-public","student_id":policy["public_id"],"student_revision":policy["revision"],
        "validation_examples":4,"context_limit":4096,"learning_rate":1e-5}
    settings={"train_examples":8,"steps":4,"group":8,"max_tokens":512}
    config={"shared":shared,"methods":{MODULE["KEY"]:settings}}
    canonical=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    contract={"source_commit":MODULE["COMMIT"],"source_file_sha256":soar_receipt["executed_source_sha256"]}
    audit={**contract,"source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,
        "execution_config_sha256":canonical,"public_train_only_holdout":public["dataset"],
        "resources":{"student":{"verified":True,"public_id":policy["public_id"],"revision":policy["revision"],
            "file_sha256":policy["verified_mirror"]["file_sha256"]}}}
    r={**fixture(),"seed":42,"method":MODULE["KEY"],"device":"cuda","diagnostic_only":True,"promotion_eligible":False,
        "protocol":{"train_examples":8,"validation_examples":4,"max_tokens":512,"gold_in_student_generation":False,"test_opened":False},
        "dataset":public["dataset"],"checkpoint":policy,"baseline":{"accuracy":.25,"examples":4},
        "method_metrics":{"accuracy":.5,"examples":4},"parameters_changed":True,"execution_status":"passed","cost":{"generated_tokens":{"fixture":1}}}
    l={**contract,"seed":42,"execution_config_sha256":canonical,"effective_config":{**shared,**settings,"variant":"unfiltered"},
        "job":{"timeout_seconds":900},"gpu_slot_grant":"A30-post-training-explicit-slot",
        "command":["python","fixture-not-new-GPU","--method",MODULE["KEY"],"--seed","42","--variant","unfiltered"]}
    m={"core_commit":MODULE["COMMIT"],"observer_commit":MODULE["OBSERVER"],"observer_source_sha256":MODULE["OBSERVER_SHA"],
        "core_exit_code":0,"accelerator":{"model":"NVIDIA A30"},"seed":42,"variant":"unfiltered","peak_memory_available":True,
        "no_monkeypatch":True,"training_arguments_forwarded_unchanged":True,"actual_max_memory_allocated_bytes":1,
        "actual_max_memory_reserved_bytes":2}
    binding={"core_commit":MODULE["COMMIT"],"observer_commit":MODULE["OBSERVER"],
        "observer_source_sha256":{"scripts/observe_oct14_cuda_memory.py":MODULE["OBSERVER_SHA"]}}
    (tmp_path/"evidence").mkdir()
    for p,value in (("evidence/result.json",r),("launch.json",l),("exit.json",{"exit_code":0,"elapsed_seconds":1.}),
        ("gpu-memory.json",m),("observer-binding.json",binding)):
        (tmp_path/p).write_text(json.dumps(value))
    return contract,audit,config


def test_cpu_full_binding_fixture_does_not_claim_a_new_gpu_run(tmp_path):
    r,c,h=MODULE["validate_run"](tmp_path,*run_fixture(tmp_path))
    assert r["seed"]==42 and c["actual_optimizer_updates"]==32 and len(h)==64


@pytest.mark.parametrize("case",["old-source","old-precision","source-files","cpu-audit","resource","dataset","config","cap","seed",
    "wall","exit","gold","observer","cpu-device","memory","token-cap"])
def test_repaired_run_rejects_wrong_core_resource_config_or_observer(tmp_path,case):
    contract,audit,config=run_fixture(tmp_path)
    if case=="old-source":contract["source_commit"]="51b4718a76da286b4111c6fc7d8e003d436def72"
    elif case=="old-precision":contract["source_file_sha256"]["src/auto_research/post_training/oct13_common.py"]="739f276633d74a85ba790e4d6df25504bce89950c40867ed57302cde03f1ada9"
    elif case=="cpu-audit":audit["cuda_initialized"]=True
    elif case=="resource":audit["resources"]["student"]["verified"]=False
    elif case=="dataset":audit["public_train_only_holdout"]={}
    else:
        name="launch.json" if case in ("source-files","config","cap") else "exit.json" if case in ("wall","exit") else "gpu-memory.json" if case in ("observer","cpu-device","memory") else "evidence/result.json"
        p=tmp_path/name
        data=json.loads(p.read_text())
        if case=="source-files":data["source_file_sha256"]={}
        elif case=="config":data["execution_config_sha256"]="0"*64
        elif case=="cap":data["effective_config"]["max_tokens"]=1024
        elif case=="seed":data["seed"]=45
        elif case=="wall":data["elapsed_seconds"]=901.
        elif case=="exit":data["exit_code"]=124
        elif case=="gold":data["protocol"]["gold_in_student_generation"]=True
        elif case=="observer":data["observer_commit"]="0"*40
        elif case=="cpu-device":data["accelerator"]["model"]="CPU"
        elif case=="token-cap":data["cost"]["generated_tokens"]["fixture"]=143361
        else:data["actual_max_memory_reserved_bytes"]=0
        p.write_text(json.dumps(data))
    with pytest.raises(ValueError):MODULE["validate_run"](tmp_path,contract,audit,config)


@pytest.mark.parametrize("case",["missing","duplicate","cross-seed-dataset","cross-seed-checkpoint"])
def test_cohort_guard_rejects_partial_duplicate_and_cross_seed_resource_mix(monkeypatch,case):
    # Only the CPU aggregate is isolated here; no training operator is patched.
    directories=[(s,v) for s in (42,43,44) for v in sorted(MODULE["VARIANTS"])]
    if case=="missing":directories.pop()
    elif case=="duplicate":directories[-1]=directories[0]
    def ledger(identity,*_):
        s,v=identity
        changed=(s==44 and case.startswith("cross-seed"))
        r={"seed":s,"variant":v,"dataset":{"fixture_dataset":1 if changed and case=="cross-seed-dataset" else 0},
            "checkpoint":{"fixture_checkpoint":1 if changed and case=="cross-seed-checkpoint" else 0},
            "baseline":{"accuracy":.25},"method_metrics":{"accuracy":.5}}
        return r,{"mechanism_passed":True,"negative_control_completed":False},"0"*64
    monkeypatch.setitem(MODULE["curate"].__globals__,"validate_run",ledger)
    with pytest.raises(ValueError):MODULE["curate"](directories,{"source_file_sha256":{}},{},{})
