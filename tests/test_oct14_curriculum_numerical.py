"""Old numerical evidence is preserved, never reclassified into a GPU pass."""
import copy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT=Path(__file__).resolve().parents[1]
MODULE=runpy.run_path(str(ROOT/"scripts/curate_oct14_curriculum_numerical.py"))
PUBLIC=json.loads((ROOT/MODULE["ARTIFACT"]).read_text())


def fixture(tmp_path):
    records=[]
    for cohort in PUBLIC["seed_results"]:
        for index,row in enumerate(cohort["variants"].values()):
            # CPU-only ledger fixture; it does not claim these are new CUDA results.
            record=copy.deepcopy(row)
            groups=[]
            for equal in row["equal_reward_group_audits"]:
                groups.append({"training_row":equal["training_row"],"rewards":[equal["equal_reward"]]*8,
                    "advantages":equal["actual_advantages"],"gradient_l2_norm":equal["gradient_l2_norm"],
                    "optimizer_update_executed":True,"fixture_step":equal["step"]})
            for _ in range(row["genuine_reward_varying_optimizer_calls"]):
                groups.append({"training_row":100,"rewards":[0.,1.],"advantages":[-1.,1.],
                    "gradient_l2_norm":1.,"optimizer_update_executed":True,"fixture_step":99})
            training=[]
            for step in sorted({g["fixture_step"] for g in groups}):
                batch=[{k:v for k,v in g.items() if k!="fixture_step"} for g in groups if g["fixture_step"]==step]
                training.append({"step":step,"groups":batch,"effective_updates":len(batch)})
            r={"method":MODULE["KEY"],"seed":row["seed"],"variant":row["variant"],"device":"cuda",
                "dataset":PUBLIC["dataset"],"checkpoint":PUBLIC["checkpoint"],"training":training,"execution_status":"passed"}
            d=tmp_path/f"{cohort['seed']}-{index}"
            (d/"evidence").mkdir(parents=True)
            raw=d/"evidence/result.json"
            raw.write_text(json.dumps(r))
            (d/"launch.json").write_text(json.dumps({"source_commit":row["source_commit"],
                "source_file_sha256":{"src/auto_research/post_training/oct13_common.py":MODULE["LEGACY_COMMON_SHA"]}}))
            (d/"exit.json").write_text(json.dumps({"exit_code":0,"elapsed_seconds":1.}))
            record.update(raw_path=str(raw),raw_sha256=hashlib.sha256(raw.read_bytes()).hexdigest())
            records.append(record)
    interrupted=tmp_path/"interrupted"
    for variant in ("staged","too-hard"):
        d=interrupted/f"curriculum-{variant}-s43"
        d.mkdir(parents=True)
        (d/"exit.json").write_text(json.dumps({"exit_code":-15,"elapsed_seconds":1.}))
        (d/"interrupted-by-main.json").write_text(json.dumps({"status":"interrupted-at-explicit-main-request"}))
    (interrupted/"queue-interrupted-by-main.json").write_text(json.dumps({"seed44_jobs_not_launched":
        ["unfiltered","static","fixed-medium","staged","too-hard"]}))
    return {"completed_raw_records":records},interrupted


def test_actual_legacy_public_negative_keeps_pseudo_updates_and_incomplete_queue():
    assert PUBLIC["not_gpu_receipt"] is True and PUBLIC["whole_method_gpu_validation_passed"] is False
    assert PUBLIC["diagnostic_only"] is True and PUBLIC["promotion_eligible"] is False
    rows=[v for s in PUBLIC["seed_results"] for v in s["variants"].values()]
    assert len(rows)==8 and PUBLIC["seeds"]==[42,43]
    selected={(x["accelerator_model"],x["variant"],x["seed"]):x for x in rows}
    for v,s,reported,pseudo in [("unfiltered",42,32,12),("static",42,8,3),("unfiltered",43,32,13),("static",43,8,2)]:
        row=selected["A30",v,s]
        assert row["raw_reported_optimizer_updates"]==reported
        assert row["mathematically_equal_reward_optimizer_updates"]==pseudo
    checks=PUBLIC["execution_checks"]
    assert checks["posthoc_filtering_cannot_salvage_passed_status"] is True
    assert checks["seed44_old_five_arms_not_launched"] is True
    assert len(checks["interrupted_old_a30_jobs"])==2
    assert not (ROOT/"scripts/curate_oct14_curriculum_controls.py").exists()


def test_cpu_fixture_curation_never_salvages_genuine_groups_into_pass(tmp_path):
    output=MODULE["curate"](*fixture(tmp_path))
    assert output["not_gpu_receipt"] is True and output["whole_method_gpu_validation_passed"] is False
    assert output["execution_checks"]["old_completed_runs_reviewed"]==8


@pytest.mark.parametrize("case",["dedup","hash","source","source-file","count","pseudo-count","pseudo-ledger","missing","unlaunched"])
def test_old_audit_cannot_hide_identity_hash_or_pseudo_updates(tmp_path,case):
    audit,interrupted=fixture(tmp_path)
    records=audit["completed_raw_records"]
    if case=="dedup":records[-1]=copy.deepcopy(records[-2])
    elif case=="hash":records[0]["raw_sha256"]="0"*64
    elif case=="missing":records.pop()
    elif case=="count":records[0]["raw_reported_optimizer_updates"]-=1
    elif case in ("pseudo-count","pseudo-ledger"):
        record=next(x for x in records if x["equal_reward_group_audits"])
        if case=="pseudo-count":record["mathematically_equal_reward_optimizer_updates"]-=1
        else:record["equal_reward_group_audits"][0]["actual_advantages"][0]=0.
    elif case=="unlaunched":(interrupted/"curriculum-static-s44").mkdir()
    else:
        p=Path(records[0]["raw_path"]).parent.parent/"launch.json"
        data=json.loads(p.read_text())
        if case=="source":data["source_commit"]="b90862754bf51b1beeb5add3f7dc2a51ca00ace4"
        else:data["source_file_sha256"]["src/auto_research/post_training/oct13_common.py"]="0"*64
        p.write_text(json.dumps(data))
    with pytest.raises(ValueError):MODULE["curate"](audit,interrupted)


@pytest.mark.parametrize("case",["count","gradient","nonfinite"])
def test_raw_optimizer_call_is_not_silently_filtered(case):
    group={"training_row":0,"rewards":[1.2]*8,"advantages":[.11920928955078125]*8,
        "gradient_l2_norm":.1,"optimizer_update_executed":True}
    step={"step":1,"groups":[group],"effective_updates":1}
    if case=="count":step["effective_updates"]=0
    elif case=="gradient":group["gradient_l2_norm"]=0.
    else:group["advantages"][0]=float("nan")
    with pytest.raises(ValueError):MODULE["audit_training"]([step])
