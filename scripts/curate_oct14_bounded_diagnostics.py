#!/usr/bin/env python3
"""Retain bounded MBS failure and SOAR train-only probe, never sign receipts."""
import argparse
import hashlib
import json
from pathlib import Path

from curate_oct14_post_complete import finite_tree
from auto_research.reproductions.magicbeanstalk.algorithm import verified_hard_seed


def curate(directory,contract,audit,config,*,method):
    launch=json.loads((directory/"launch.json").read_text())
    exit_record=json.loads((directory/"exit.json").read_text())
    canonical=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    if (launch["source_commit"]!=contract["source_commit"] or audit["source_commit"]!=contract["source_commit"]
            or launch["source_file_sha256"]!=contract["source_file_sha256"]
            or audit["source_file_sha256"]!=contract["source_file_sha256"]
            or not audit["source_hashes_verified"] or audit["cuda_initialized"] is not False
            or audit["model_instantiated"] is not False or launch["execution_config_sha256"]!=canonical
            or audit["execution_config_sha256"]!=canonical or launch["seed"]!=42):
        raise ValueError("actual source/resource/config/seed binding required")
    if exit_record["elapsed_seconds"]<=0:
        raise ValueError("actual elapsed evidence required")
    wall=1800 if method=="magicbeanstalk" else 300
    if exit_record["elapsed_seconds"]>wall:
        raise ValueError("actual invocation exceeded the granted wall cap")
    for role in ("student","teacher"):
        resource=audit["resources"][role]
        if (resource["verified"] is not True or resource["public_id"]!=config["shared"][role+"_id"]
                or resource["revision"]!=config["shared"][role+"_revision"]):
            raise ValueError("fixed source-bound public resources required")
    finite_tree(exit_record)
    if method=="magicbeanstalk":
        if contract["source_commit"]!="0f5dca9f7f0319c6e3bb57aa578cfe26499a6e7e" or exit_record["exit_code"]!=1:
            raise ValueError("this curator preserves only the actual bounded0f failure")
        raw_path=directory/"evidence/failure.json"
        raw=json.loads(raw_path.read_text())
        c={**config["shared"],**config["methods"][method],**launch["job"]["overrides"]}
        if (c!=launch["effective_config"] or c["train_examples"]!=16 or c["hard_root_limit"]!=4
                or c["max_tokens"]!=1024 or c["depth"]!=1 or c["group"]!=4 or c["steps"]!=2
                or c["teacher_attempts"]!=2 or c["decomposition_retries"]!=2 or c["synthesis_retries"]!=2):
            raise ValueError("original bounded budget required")
        selection=raw["hard_root_selection"]
        calibrations=selection["calibration_audits"]
        eligible=[]
        for index,row in enumerate(calibrations):
            accepted=verified_hard_seed(row["rewards"],row["truncated"])
            if row["training_index"]!=index or accepted!=row["accepted"]:
                raise ValueError("hardness must derive from actual original-order outcomes/truncation")
            if accepted:
                eligible.append(index)
        if (len(calibrations)!=selection["calibrated_training_candidates"] or len(calibrations)>16
                or selection["selected_training_root_indices"]!=eligible[:4]
                or selection["verified_hard_roots_selected"]!=len(eligible[:4])
                or selection["tree_construction_attempts"]!=len(eligible[:4])
                or selection["paired_rl_root_indices"]!=[]
                or raw["status"]!="failed" or "no actual effectivity-validated" not in raw["error"]):
            raise ValueError("bounded failed descendant evidence mismatch")
        if any(role in raw["cost"]["generation_calls"] for role in ("mbs_rlvr","seed_rlvr_control")):
            raise ValueError("this failure must not claim any RL updates")
        dataset=audit["public_train_only_holdout"]
        checkpoint={role:{"public_id":v["public_id"],"revision":v["revision"],"file_sha256":v["file_sha256"]}
                    for role,v in audit["resources"].items()}
        checks={"hard_root_selection":selection,"method_rl_updates":0,"control_rl_updates":0,
            "construction_failed_without_complete_gate_trace":True,
            "failure_interpretation":"hard roots found, but no surviving descendant; raw trace does not isolate every internal rejection"}
        path="docs/reproductions/2610.12659-magicbeanstalk/metrics/public-a100-bounded-failed-seed42-0f5dca9f.json"
    else:
        if contract["source_commit"]!="57b2314db1d5b8a8ebeb0aa7fbb6b7fee523df55" or exit_record["exit_code"]!=0:
            raise ValueError("actual frozen57b completed SOAR probe required")
        raw_path=directory/"evidence/diagnosis.json"
        raw=json.loads(raw_path.read_text())
        if (raw["core_source_sha256"]!=contract["source_file_sha256"] or raw["source_commit"]!=contract["source_commit"]
                or raw["whole_method_gpu_validation_passed"] is not False or raw["validation_content_read"] is not False
                or raw["test_content_read"] is not False or raw["assessment_executed"] is not False
                or raw["lora_updates"]!=0 or raw["optimizer_updates"]!=0
                or len(raw["training_episode_audits"])!=8
                or raw["configured_caps"]!={"training_prefix":4,"episodes_per_question":2,"max_turns":3,
                    "response_cap":256,"generated_response_tokens_upper":12288,"wall_cap_seconds":300,"optimizer_updates":0}):
            raise ValueError("train-only original-cap no-update/no-evaluation SOAR probe required")
        if sum(raw["cost"]["generated_tokens"].values())>12288:
            raise ValueError("SOAR generated-token cap exceeded")
        dataset=raw["dataset"]
        checkpoint=raw["checkpoint"]
        actual=checkpoint["policy"]
        teacher=audit["resources"]["teacher"]
        if (actual["public_id"]!=teacher["public_id"] or actual["revision"]!=teacher["revision"]
                or actual["verified_mirror"]["file_sha256"]!=teacher["file_sha256"]):
            raise ValueError("actual 7B policy must match preverified public bytes")
        checks={"diagnosis_status":raw["diagnosis_status"],"valid_format_episodes":raw["valid_format_episodes"],
            "source_match_episodes":raw["source_match_episodes"],"total_searches":raw["total_searches"],
            "lora_updates":0,"assessment_executed":False,"validation_content_read":False,"test_content_read":False}
        path="docs/reproductions/2610.13157-soar/metrics/public-a100-train-format-probe-seed42-57b2314d.json"
    finite_tree(raw)
    checks.update(invocation_elapsed_seconds=exit_record["elapsed_seconds"],return_code=exit_record["exit_code"],
        configured_wall_cap_seconds=wall,measured_cost=raw["cost"])
    metrics={"generated_response_tokens":{"mean":sum(raw["cost"]["generated_tokens"].values()),"std":0.,"n":1},
        "invocation_elapsed_seconds":{"mean":exit_record["elapsed_seconds"],"std":0.,"n":1}}
    return {"schema_version":2,"adapter_key":method,"manifest_ref":"reproduction:"+method,"method":method,
        "measured_locally":True,"diagnostic_only":True,"promotion_eligible":False,"not_gpu_receipt":True,
        "whole_method_gpu_validation_passed":False,"seeds":[42],"accelerator":{"vendor":"NVIDIA","model":"NVIDIA A100-SXM4-80GB"},
        "seed_results":[{"seed":42,"device":"cuda","diagnostic_only":True,"stage_result":raw}],
        "aggregate_metrics":metrics,"execution_checks":checks,"dataset":dataset,"checkpoint":checkpoint,
        "evaluation_protocol":{"tier":"l1_mechanism","seeds":[42],"formal_comparison":False,"promotion_eligible":False,
            "test_used_for_selection":False,"claim_policy":"retained failed construction or no-update training diagnostic, not full-method GPU acceptance"},
        "provenance":{"code_commit":contract["source_commit"],"artifact_path":path,"executed_source_sha256":contract["source_file_sha256"],
            "dataset_fingerprint":hashlib.sha256(json.dumps(dataset,sort_keys=True).encode()).hexdigest(),
            "execution_config_sha256":canonical,"raw_result_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
            "raw_launch_sha256":hashlib.sha256((directory/"launch.json").read_bytes()).hexdigest()},
        "limitations":["No passed GPU receipt: complete defining mechanism with nonzero policy updates remains unvalidated.",
            "One seed tiny public training/validation diagnostic, not original benchmark or formal capability evidence.",
            "Original failure traces retained; no gates lowered, no forced advantage, no retries or test-selected budget."]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("run-directory","contract","audit","config","output"):
        p.add_argument("--"+name,type=Path,required=True)
    p.add_argument("--method",choices=("magicbeanstalk","soar"),required=True)
    args=p.parse_args()
    artifact=curate(args.run_directory,json.loads(args.contract.read_text()),json.loads(args.audit.read_text()),
        json.loads(args.config.read_text()),method=args.method)
    with args.output.open("x") as stream:
        stream.write(json.dumps(artifact,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
