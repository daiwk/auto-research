"""Synthetic curation-contract fixtures; never GPU execution evidence."""
import copy
import json
from pathlib import Path
import runpy

import pytest

ROOT=Path(__file__).resolve().parents[1]


def runs():
    rows=[]
    for variant in ("state","state-no-expansion","full-history-opd"):
        for seed in (42,43,44):
            full=variant=="full-history-opd"
            audit={"root_turns":2 if full else 1,"root_actions_executed":2 if full else 1,
                "additional_actions_executed":0,"response_pool_size":2 if full or variant=="state" else 1,
                "teacher_prior_reasoning_removed_responses":0,
                "same_current_response_prefix":True,"environment_reward_in_loss":False}
            if full:
                audit.update(root_trajectories=2,independent_root_audits=[
                    {"root_turns":1,"root_actions_executed":1,"additional_actions_executed":0},
                    {"root_turns":1,"root_actions_executed":1,"additional_actions_executed":0}])
            rows.append({"method":"state-opd","variant":variant,"seed":seed,"device":"cuda",
                "diagnostic_only":True,"parameters_changed":True,"execution_status":"passed",
                "dataset":{"verified":True,"test_read":False,"source_revision":"public-fixture"},
                "student":{"public_id":"fixture-student","revision":"fixture-v1"},
                "teacher":{"public_id":"fixture-teacher","revision":"fixture-v1"},
                "baseline":{"accuracy":0.,"submission_rate":0.,"mean_executed_actions":1.,"examples":2},
                "method_metrics":{"accuracy":0.,"submission_rate":0.,"mean_executed_actions":1.,"examples":2},
                "training":[{"gradient_l2_norm":1.,"optimizer_update_executed":True,"supervised_tokens":2}],
                "trajectory_audits":[audit],"protocol":{"steps":1,"max_turns":2,"response_cap":4,
                    "transcript_cap":20,"multiplicity":2,"concentration":2,"test_opened":False,
                    "teacher_and_policy_receive_gold":False,"effective_multiplicity":1 if variant=="state-no-expansion" else 2,
                    "teacher_preceding_context":"full-history" if full else "executed-state",
                    "reference_independent_root_trajectories":2 if full else 1}})
    return rows


def summarize(rows):
    return runpy.run_path(str(ROOT/"scripts/curate_oct14_state_opd.py"))["summarize_state_arms"](rows)


def test_three_arms_keep_zero_metrics_and_derive_reasoning_removal():
    result=summarize(runs())
    assert [row["seed"] for row in result["seed_results"]]==[42,43,44]
    assert all(len(row["variants"])==3 for row in result["seed_results"])
    assert result["metrics"]["state.validation.accuracy"]["mean"]==0.
    for variant in ("state","state-no-expansion","full-history-opd"):
        assert result["checks"][variant]["teacher_prior_reasoning_removed_observed"] is False
        assert result["checks"][variant]["teacher_prior_reasoning_removed_responses_per_seed"]==[0,0,0]
    rows=runs()
    rows[0]["trajectory_audits"][0]["teacher_prior_reasoning_removed_responses"]=1
    assert summarize(rows)["checks"]["state"]["teacher_prior_reasoning_removed_observed"] is True


@pytest.mark.parametrize("case",["missing-arm","duplicate-seed","gold","no-update","bad-context",
    "full-history-removes","fake-roots","expanded-actions","wrong-budget","mismatched-data","unverified-data"])
def test_invalid_or_incomplete_evidence_never_passes(case):
    rows=copy.deepcopy(runs())
    if case=="missing-arm": rows.pop()
    elif case=="duplicate-seed": rows[-1]["seed"]=43
    elif case=="gold": rows[0]["protocol"]["teacher_and_policy_receive_gold"]=True
    elif case=="no-update": rows[0]["training"][0]["gradient_l2_norm"]=0.
    elif case=="bad-context": rows[0]["protocol"]["teacher_preceding_context"]="full-history"
    elif case=="full-history-removes": rows[-1]["trajectory_audits"][0]["teacher_prior_reasoning_removed_responses"]=1
    elif case=="fake-roots": rows[-1]["trajectory_audits"][0]["independent_root_audits"].pop()
    elif case=="expanded-actions": rows[0]["trajectory_audits"][0]["additional_actions_executed"]=1
    elif case=="wrong-budget": rows[3]["protocol"]["response_cap"]=8
    elif case=="mismatched-data": rows[3]["dataset"]["source_revision"]="other"
    else: rows[0]["dataset"]["verified"]=False
    with pytest.raises(ValueError): summarize(rows)


@pytest.mark.parametrize("case",["source","exit","argv","config"])
def test_curation_binds_actual_launcher_and_never_upgrades_mismatches(tmp_path,case):
    rows=runs()
    directories=[]
    contract={"source_commit":"a"*40,"source_file_sha256":{"fixture.py":"b"*64}}
    for index,row in enumerate(rows):
        directory=tmp_path/str(index)
        (directory/"evidence").mkdir(parents=True)
        directories.append(directory)
        protocol=row["protocol"]
        config={"steps":protocol["steps"],"max_turns":protocol["max_turns"],
            "max_tokens":protocol["response_cap"],"context_limit":protocol["transcript_cap"],
            "multiplicity":protocol["multiplicity"],"concentration":protocol["concentration"],
            "validation_examples":2,"variant":row["variant"]}
        launch={"source_commit":contract["source_commit"],"source_file_sha256":contract["source_file_sha256"],
            "execution_config_sha256":"c"*64,"effective_config":config,"seed":row["seed"],
            "job":{"overrides":{"variant":row["variant"]}},
            "command":["python","scripts/run_oct13_post_training.py","--method","state-opd",
                "--seed",str(row["seed"]),"--variant",row["variant"]]}
        exit_record={"exit_code":0,"elapsed_seconds":1.}
        if index==0:
            if case=="source": launch["source_commit"]="d"*40
            elif case=="exit": exit_record["exit_code"]=1
            elif case=="argv": launch["command"][launch["command"].index("--seed")+1]="99"
            else: launch["effective_config"]["max_tokens"]=128
        (directory/"evidence/result.json").write_text(json.dumps(row))
        (directory/"launch.json").write_text(json.dumps(launch))
        (directory/"exit.json").write_text(json.dumps(exit_record))
    curate=runpy.run_path(str(ROOT/"scripts/curate_oct14_state_opd.py"))["curate"]
    with pytest.raises(ValueError):
        curate(directories,contract,accelerator="fixture-not-real-GPU",validated_at="fixture")
