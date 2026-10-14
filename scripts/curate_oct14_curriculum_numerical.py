#!/usr/bin/env python3
"""Recompute the old curriculum numerical audit; never salvage passed status."""
import argparse
import hashlib
import json
import math
from pathlib import Path

LEGACY_COMMON_SHA="739f276633d74a85ba790e4d6df25504bce89950c40867ed57302cde03f1ada9"
COMMITS={"6aabe57a97ec3a586aac7aeea66128750f9441da":"A100",
         "51b4718a76da286b4111c6fc7d8e003d436def72":"A30"}
KEY="grpo-difficulty-curriculum"
ARTIFACT="docs/reproductions/2610.13669-grpo-difficulty-curriculum/metrics/public-legacy-curriculum-numerical-negative.json"


def audit_training(training):
    reported=0
    equal=[]
    for step in training:
        actual=0
        for group in step["groups"]:
            if not group.get("optimizer_update_executed"):
                continue
            rewards=group["rewards"]
            advantages=group["advantages"]
            gradient=group["gradient_l2_norm"]
            if (not rewards or len(rewards)!=len(advantages) or not math.isfinite(gradient) or gradient<=0
                    or any(not math.isfinite(x) for x in rewards+advantages)):
                raise ValueError("reported optimizer call must retain finite actual rewards/advantages/gradient")
            actual+=1
            if len(set(rewards))==1:
                equal.append({"step":step["step"],"training_row":group["training_row"],"equal_reward":rewards[0],
                              "actual_advantages":advantages,"gradient_l2_norm":gradient})
        if actual!=step["effective_updates"]:
            raise ValueError("raw reported optimizer-call totals cannot be rewritten")
        reported+=actual
    return reported,equal


def curate(read_only_audit,interruption_root):
    records=read_only_audit["completed_raw_records"]
    if len(records)!=8:
        raise ValueError("all eight recorded old completed runs required")
    rows=[]
    dataset=checkpoint=None
    identities=set()
    for record in records:
        path=Path(record["raw_path"])
        content=path.read_bytes()
        if hashlib.sha256(content).hexdigest()!=record["raw_sha256"]:
            raise ValueError("old immutable raw bytes must match the prior audit")
        r=json.loads(content)
        l=json.loads((path.parent.parent/"launch.json").read_text())
        e=json.loads((path.parent.parent/"exit.json").read_text())
        if (l["source_commit"] not in COMMITS or l["source_commit"]!=record["source_commit"]
                or l["source_file_sha256"]["src/auto_research/post_training/oct13_common.py"]!=LEGACY_COMMON_SHA
                or r["method"]!=KEY or r["seed"]!=record["seed"] or r["variant"]!=record["variant"]
                or r["device"]!="cuda" or e["exit_code"]!=0 or not 0<e["elapsed_seconds"]
                or not math.isfinite(e["elapsed_seconds"]) or r["dataset"]["test_read"] is not False):
            raise ValueError("actual legacy source/run identity/exit/test isolation required")
        identity=(COMMITS[l["source_commit"]],r["variant"],r["seed"])
        if identity in identities:
            raise ValueError("duplicate variants are not independent recorded runs")
        identities.add(identity)
        dataset=r["dataset"] if dataset is None else dataset
        checkpoint=r["checkpoint"] if checkpoint is None else checkpoint
        if dataset!=r["dataset"]:
            raise ValueError("all old runs must use the same verified public dataset")
        reported,equal=audit_training(r["training"])
        if (reported!=record["raw_reported_optimizer_updates"]
                or len(equal)!=record["mathematically_equal_reward_optimizer_updates"]
                or equal!=record["equal_reward_group_audits"]):
            raise ValueError("prior counts cannot substitute for recomputation from actual raw")
        rows.append({k:v for k,v in record.items() if k not in ("raw_path","old_cuda_validation_pending_corrected_source")}
                    |{"accelerator_model":identity[0],"invocation_elapsed_seconds":e["elapsed_seconds"],
                      "raw_execution_status":r["execution_status"],"genuine_reward_varying_optimizer_calls":reported-len(equal),
                      "corrected_source_validation_still_required":True})
    expected={("A100",v,42) for v in ("fixed-medium","staged","too-hard")}
    expected|={("A30",v,s) for v,s in (("unfiltered",42),("static",42),("unfiltered",43),("static",43),("fixed-medium",43))}
    if identities!=expected:
        raise ValueError("exact old execution cohorts, not mixed new-source runs, required")
    interrupted=[]
    for variant in ("staged","too-hard"):
        d=interruption_root/("curriculum-"+variant+"-s43")
        e=json.loads((d/"exit.json").read_text())
        marker=json.loads((d/"interrupted-by-main.json").read_text())
        if e["exit_code"]!=-15 or marker["status"]!="interrupted-at-explicit-main-request":
            raise ValueError("actual directed interruption must be preserved")
        interrupted.append({"variant":variant,"seed":43,"exit_code":-15,"elapsed_seconds":e["elapsed_seconds"]})
    index=json.loads((interruption_root/"queue-interrupted-by-main.json").read_text())
    if (set(index["seed44_jobs_not_launched"])!={"unfiltered","static","fixed-medium","staged","too-hard"}
            or list(interruption_root.glob("*-s44"))):
        raise ValueError("never claim unlaunched seed44 jobs completed")
    seeds=[42,43]
    metrics={x["accelerator_model"]+"."+x["variant"]+".s"+str(x["seed"])+".mathematically_equal_reward_optimizer_calls":
             {"mean":x["mathematically_equal_reward_optimizer_updates"],"std":0.,"n":1} for x in rows}
    return {"schema_version":2,"adapter_key":KEY,"manifest_ref":"reproduction:"+KEY,"method":KEY,
        "measured_locally":True,"diagnostic_only":True,"promotion_eligible":False,"not_gpu_receipt":True,
        "whole_method_gpu_validation_passed":False,"seeds":seeds,
        "seed_results":[{"seed":s,"diagnostic_only":True,"variants":{x["accelerator_model"]+"."+x["variant"]:x for x in rows if x["seed"]==s}} for s in seeds],
        "aggregate_metrics":metrics,"dataset":dataset,"checkpoint":checkpoint,
        "issue":"float32 centering residual for mathematically equal shaped rewards was divided by std+1e-6 and wrongly admitted as a nonzero update",
        "execution_checks":{"old_completed_runs_reviewed":8,"no_old_raw_bytes_modified":True,
            "posthoc_filtering_cannot_salvage_passed_status":True,"old_controls_positive_evidence_withdrawn":True,
            "interrupted_old_a30_jobs":interrupted,"seed44_old_five_arms_not_launched":True,
            "new_corrected_core_commit":"b90862754bf51b1beeb5add3f7dc2a51ca00ace4","new_core_gpu_validation_pending":True},
        "evaluation_protocol":{"tier":"l1_mechanism","seeds":seeds,"formal_comparison":False,"promotion_eligible":False,
            "test_used_for_selection":False,"claim_policy":"numerical-integrity negative audit, not accepted corrected-source mechanism evidence"},
        "provenance":{"code_commit":"51b4718a76da286b4111c6fc7d8e003d436def72",
            "source_commit_scope":"primary affected A30 cohort51b; separately tagged historical6a A100 rows retained",
            "artifact_path":ARTIFACT,"dataset_fingerprint":hashlib.sha256(json.dumps(dataset,sort_keys=True).encode()).hexdigest(),
            "raw_results_sha256":{x["accelerator_model"]+"."+x["variant"]+".s"+str(x["seed"]):x["raw_sha256"] for x in rows}},
        "limitations":["Reported optimizer calls and original metrics are not rewritten; mathematically equal-reward calls are numerical artifacts, not genuine reward signal.",
            "Historical A10042 three arms and A30fixed43 had no equal-reward admitted groups, but do not validate the newly repaired full five-arm path.",
            "No old passed status is salvaged by subtracting pseudo updates; corrected-source same-budget GPU runs are required.",
            "A100 and A30/framework cohorts are not paired capability baselines; variants are not independent seeds."]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("read-only-audit","interruption-root","output"):
        p.add_argument("--"+name,type=Path,required=True)
    args=p.parse_args()
    artifact=curate(json.loads(args.read_only_audit.read_text()),args.interruption_root)
    with args.output.open("x") as stream:
        stream.write(json.dumps(artifact,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
