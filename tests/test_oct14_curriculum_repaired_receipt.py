"""Fifteen-run receipt guards; CPU fixtures are not CUDA evidence."""
import copy
import json
from pathlib import Path
import runpy

import pytest

ROOT=Path(__file__).resolve().parents[1]
CURRENT=runpy.run_path(str(ROOT/"tests/test_oct14_curriculum_repaired_curation.py"))
MODULE=runpy.run_path(str(ROOT/"scripts/curate_oct14_curriculum_repaired.py"))


def inputs(tmp_path):
    ds=[]
    for seed in (42,43,44):
        for variant in sorted(MODULE["VARIANTS"]):
            d=tmp_path/f"{variant}-{seed}"
            d.mkdir()
            contract,audit,config=CURRENT["run_fixture"](d)
            r=json.loads((d/"evidence/result.json").read_text())
            r.update(CURRENT["fixture"](variant),seed=seed)
            (d/"evidence/result.json").write_text(json.dumps(r))
            l=json.loads((d/"launch.json").read_text());l["seed"]=seed;l["effective_config"]["variant"]=variant
            for flag,value in (("--seed",str(seed)),("--variant",variant)):
                l["command"][l["command"].index(flag)+1]=value
            (d/"launch.json").write_text(json.dumps(l))
            m=json.loads((d/"gpu-memory.json").read_text());m.update(seed=seed,variant=variant)
            (d/"gpu-memory.json").write_text(json.dumps(m))
            ds.append(d)
    observer={"source_commit":MODULE["OBSERVER"],"source_file_sha256":{"scripts/observe_oct14_cuda_memory.py":MODULE["OBSERVER_SHA"]}}
    return ds,contract,audit,config,observer


def test_fifteen_cpu_fixtures_only_verify_schema_and_all_scope_guard(tmp_path):
    a,r=MODULE["curate_with_receipt"](*inputs(tmp_path))
    assert a["actual_cuda_run_count"]==15 and a["seeds"]==r["seeds"]==[42,43,44]
    assert len(r["all_sanitized_commands"])==15
    assert a["evaluation_protocol"]["claim_policy"]=="single/few-seed smoke result; do not claim a stable improvement"
    assert a["evaluation_protocol"]["formal_comparison"] is False
    assert r["observer_binding"]["commit"]==MODULE["OBSERVER"]
    assert all(x["n"]==3 for x in r["metrics"].values())


@pytest.mark.parametrize("case",["five42","missing","duplicate","observer","old-core","one-zero","one-exit","one-budget","pseudo"])
def test_partial_failed_or_unbound_arm_cannot_get_receipt(tmp_path,case):
    ds,contract,audit,config,observer=inputs(tmp_path)
    if case=="five42":ds=ds[:5]
    elif case=="missing":ds.pop()
    elif case=="duplicate":ds[-1]=ds[0]
    elif case=="observer":observer["source_commit"]="0"*40
    elif case=="old-core":contract["source_commit"]="51b4718a76da286b4111c6fc7d8e003d436def72"
    else:
        d=ds[-1]
        name="exit.json" if case=="one-exit" else "launch.json" if case=="one-budget" else "evidence/result.json"
        p=d/name;data=json.loads(p.read_text())
        if case=="one-exit":data["exit_code"]=124
        elif case=="one-budget":data["effective_config"]["group"]=16
        elif case=="one-zero":data["parameters_changed"]=False
        else:
            group=data["training"][0]["groups"][0]
            group.update(rewards=[.2]*8,advantages=[-.014901161193847656]*8,correctness_rewards=[0.]*8,current_success=0.)
            data["difficulty_history"][0][0]=0.
            data["difficulty_dynamics"]=MODULE["difficulty_dynamics"](data["difficulty_history"])
        p.write_text(json.dumps(data))
    with pytest.raises(ValueError):MODULE["curate_with_receipt"](ds,contract,audit,config,copy.deepcopy(observer))


def zeroize(directory,*,negative_control):
    raw=directory/"evidence/result.json"
    r=json.loads(raw.read_text())
    history=[[0.]*8 for _ in range(4)]
    r.update(difficulty_history=history,difficulty_dynamics=MODULE["difficulty_dynamics"](history),parameters_changed=False,
        execution_status="passed-negative-control" if negative_control else "failed-no-effective-updates",
        method_metrics=copy.deepcopy(r["baseline"]))
    for index,step in enumerate(r["training"]):
        step["groups"]=[{"training_row":i,"eligible":not negative_control,"current_success":0.,
            **({"correctness_rewards":[0.]*8,"rewards":[.2]*8,"optimizer_update_executed":False,"zero_advantage_group":True}
               if not negative_control else {})} for i in range(8)]
        step["effective_updates"]=0
    raw.write_text(json.dumps(r))
    for name,key in (("exit.json","exit_code"),("gpu-memory.json","core_exit_code")):
        p=directory/name;v=json.loads(p.read_text());v[key]=0 if negative_control else 1;p.write_text(json.dumps(v))


def test_completed_true_zero_negative_control_remains_zero_in_cpu_schema_fixture(tmp_path):
    args=inputs(tmp_path)
    d=next(d for d in args[0] if d.name=="too-hard-44")
    zeroize(d,negative_control=True)
    a,r=MODULE["curate_with_receipt"](*args)
    check=a["execution_checks"]["44"]["too-hard"]
    assert check["actual_optimizer_updates"]==0 and check["negative_control_completed"] is True
    assert r["execution_checks"]["44"]["too-hard"]["actual_optimizer_updates"]==0


def test_complete_but_legit_zero_method_arm_cannot_get_passed_receipt(tmp_path):
    args=inputs(tmp_path)
    d=next(d for d in args[0] if d.name=="unfiltered-44")
    zeroize(d,negative_control=False)
    with pytest.raises(ValueError):MODULE["curate_with_receipt"](*args)


@pytest.mark.parametrize("case",["native-exists","receipt-exists","same-path"])
def test_cli_output_collisions_reject_before_either_output_write(tmp_path,monkeypatch,case):
    output=tmp_path/"native.json"
    receipt=tmp_path/"receipt.json"
    if case=="native-exists":output.write_text("preserved native")
    elif case=="receipt-exists":receipt.write_text("preserved receipt")
    else:receipt=output
    inputs=[]
    for name in ("contract","audit","config","observer-contract"):
        path=tmp_path/(name+".json");path.write_text("{}");inputs.extend(["--"+name,str(path)])
    before={p:p.read_bytes() for p in (output,receipt) if p.exists()}
    monkeypatch.setitem(MODULE["main"].__globals__,"curate_with_receipt",lambda *args:({"fixture":True},{"fixture":True}))
    monkeypatch.setattr("sys.argv",["curator","--run-directory",str(tmp_path),*inputs,
        "--output",str(output),"--receipt-output",str(receipt)])
    with pytest.raises(ValueError if case=="same-path" else FileExistsError):MODULE["main"]()
    assert {p:p.read_bytes() for p in (output,receipt) if p.exists()}==before
