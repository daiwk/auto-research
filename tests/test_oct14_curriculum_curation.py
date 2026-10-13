"""Synthetic fixtures for curation integrity, never CUDA evidence."""
import copy
import json
from pathlib import Path
import runpy

import pytest

ROOT=Path(__file__).resolve().parents[1]


def fixtures():
    contract={"source_commit":"a"*40,"source_file_sha256":{"fixture.py":"b"*64}}
    audit={"source_commit":contract["source_commit"],"source_file_sha256":contract["source_file_sha256"],
        "source_hashes_verified":True,"cuda_initialized":False,"model_instantiated":False,"execution_config_sha256":"c"*64}
    rows=[]
    for variant,band,correctness in (("fixed-medium",[.375,.625],[1,1,0,0]),
            ("staged",[.625,.875],[1,1,1,0]),("too-hard",[.125,.375],[1,0,0,0])):
        rate=sum(correctness)/4
        r={"method":"grpo-difficulty-curriculum","variant":variant,"seed":42,"device":"cuda",
            "diagnostic_only":True,"parameters_changed":True,"execution_status":"passed",
            "dataset":{"verified":True,"test_read":False,"source_revision":"fixture-v1"},
            "checkpoint":{"public_id":"fixture","revision":"fixture-v1"},
            "baseline":{"accuracy":.5,"examples":4},"method_metrics":{"accuracy":.5,"examples":4},
            "protocol":{"test_opened":False,"gold_in_student_generation":False,
                "train_examples":2,"validation_examples":4,"max_tokens":512},
            "cost":{"generated_tokens":{"fixture":4}},"difficulty_history":[[rate,rate]],
            "training":[{"step":1,"band":band,"effective_updates":2,
                "validation_diagnostic":{"accuracy":.5},"transition":"new-best" if variant=="staged" else "not-staged",
                "groups":[{"training_row":i,"eligible":True,"current_success":rate,"correctness_rewards":correctness,
                    "optimizer_update_executed":True,"zero_advantage_group":False,"gradient_l2_norm":1.,
                    "rewards":correctness,
                    "advantages":[(x-rate)/((rate*(1-rate))**.5+1e-6) for x in correctness]} for i in range(2)]}]}
        config={"variant":variant,"steps":1,"group":4,"train_examples":2,"validation_examples":4,
            "max_tokens":512,"learning_rate":1e-5,"context_limit":4096}
        l={"source_commit":contract["source_commit"],"source_file_sha256":contract["source_file_sha256"],
            "execution_config_sha256":audit["execution_config_sha256"],"seed":42,"effective_config":config,
            "job":{"overrides":{"variant":variant}},"command":["python","runner.py","--method",
                "grpo-difficulty-curriculum","--seed","42","--variant",variant]}
        rows.append((r,l,{"exit_code":0,"elapsed_seconds":1.}))
    return contract,audit,rows


def invoke(tmp_path,contract,audit,rows):
    directories=[]
    for i,(r,l,e) in enumerate(rows):
        d=tmp_path/str(i)
        (d/"evidence").mkdir(parents=True)
        (d/"evidence/result.json").write_text(json.dumps(r))
        (d/"launch.json").write_text(json.dumps(l))
        (d/"exit.json").write_text(json.dumps(e))
        directories.append(d)
    return runpy.run_path(str(ROOT/"scripts/curate_oct14_curriculum.py"))["curate"](
        directories,contract,audit,accelerator="fixture-not-real-GPU",validated_at="fixture")


def test_one_seed_three_variants_never_becomes_three_seeds(tmp_path):
    artifact,receipt=invoke(tmp_path,*fixtures())
    assert artifact["seeds"]==[42] and len(artifact["seed_results"])==1
    assert len(artifact["seed_results"][0]["variants"])==3
    assert artifact["evaluation_protocol"]["formal_comparison"] is False
    assert artifact["evaluation_protocol"]["promotion_eligible"] is False
    assert all(v["n"]==1 for v in artifact["aggregate_metrics"].values())
    assert receipt["seeds"]==[42]


@pytest.mark.parametrize("case",["missing","duplicate","seed","source","audit","config","argv","exit",
    "gold","test","checkpoint","baseline","band","gate","correctness","zero-advantage",
    "zero-gradient","count","transition","budget","reward","advantage-not-from-reward"])
def test_mismatched_or_fabricated_evidence_rejected(tmp_path,case):
    contract,audit,rows=copy.deepcopy(fixtures())
    r,l,e=rows[0]
    g=r["training"][0]["groups"][0]
    if case=="missing":rows.pop()
    elif case=="duplicate":rows[1][0]["variant"]="fixed-medium"
    elif case=="seed":r["seed"]=43
    elif case=="source":l["source_commit"]="d"*40
    elif case=="audit":audit["cuda_initialized"]=True
    elif case=="config":l["execution_config_sha256"]="d"*64
    elif case=="argv":l["command"][l["command"].index("--seed")+1]="43"
    elif case=="exit":e["exit_code"]=1
    elif case=="gold":r["protocol"]["gold_in_student_generation"]=True
    elif case=="test":r["dataset"]["test_read"]=True
    elif case=="checkpoint":r["checkpoint"]["revision"]="other"
    elif case=="baseline":r["baseline"]["accuracy"]=0.
    elif case=="band":r["training"][0]["band"]=[0.,1.]
    elif case=="gate":g["eligible"]=False
    elif case=="correctness":g["correctness_rewards"]=[1,1,1,0]
    elif case=="zero-advantage":g["advantages"]=[0.,0.,0.,0.]
    elif case=="zero-gradient":g["gradient_l2_norm"]=0.
    elif case=="count":r["training"][0]["effective_updates"]=1
    elif case=="transition":rows[1][0]["training"][0]["transition"]="advance"
    elif case=="reward":g["rewards"][0]=10.
    elif case=="advantage-not-from-reward":g["advantages"][0]=10.
    else:l["effective_config"]["max_tokens"]=1024
    with pytest.raises(ValueError):invoke(tmp_path,contract,audit,rows)
