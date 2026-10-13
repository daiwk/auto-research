#!/usr/bin/env python3
"""Validate and sanitize one actual full-definition seed42 post-training run."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from auto_research.gpu_validation import validate_gpu_receipt
from auto_research.reproductions.progressive_contraction.algorithm import contract_teacher_pool, route_student

IDENTIFIERS={"synthself":"2610.13113","upturn":"2610.13672","progressive-contraction":"2610.12933"}
COMMITS={"synthself":"51b4718a76da286b4111c6fc7d8e003d436def72",
         "upturn":"51b4718a76da286b4111c6fc7d8e003d436def72",
         "progressive-contraction":"32f873e7a81fa90e6508d5eaad5bf9b830b04139"}


def finite_tree(value):
    if isinstance(value,float) and not math.isfinite(value):
        raise ValueError("non-finite evidence cannot pass")
    if isinstance(value,dict):
        for child in value.values():
            finite_tree(child)
    if isinstance(value,list):
        for child in value:
            finite_tree(child)


def updates(training,expected):
    if len(training)!=expected or not training:
        raise ValueError("complete configured update history required")
    for step in training:
        if (step.get("optimizer_update_executed") is not True or step.get("gradient_l2_norm",0)<=0
                or not math.isfinite(step.get("gradient_l2_norm",0))):
            raise ValueError("every advertised update requires actual nonzero finite gradient")
    return len(training)


def validate_mechanism(r,c):
    key=r["method"]
    checks={"parameters_changed":True,"measured_cost":r["cost"]}
    if key=="synthself":
        eq=r["empirical_aligner_constraints"]
        if (r.get("execution_status")!="passed" or not eq.get("satisfied")
                or not eq.get("all_aligner_responses_naturally_complete")
                or eq.get("selection_blocked_by_incomplete_outputs") is not False
                or not eq["rewrite_sequence_nll"]<eq["gold_sequence_nll"]
                or not eq["aligner_quality"]>eq["self_quality"]
                or eq.get("nll_reduction")!="full-response sequence sum including exactly one EOS"
                or len(r["rewrites"])!=c["train_examples"]):
            raise ValueError("complete-response strict sequence-SUM Eq6 required")
        for rewrite in r["rewrites"]:
            if (rewrite.get("truncated") is not False or not rewrite.get("rewrite_natural_completion")
                    or rewrite.get("rewrite_canonical_eos_appended") is not False
                    or rewrite.get("rewrite_nll_scope")!="complete_sequence"
                    or rewrite.get("gold_scored_eos_count")!=1 or rewrite.get("rewrite_scored_eos_count")!=1):
                raise ValueError("partial rewrite or fabricated termination cannot pass")
        if r["control"]["method"]!=c["control"] or c["control"]!="gold-sft":
            raise ValueError("actual independent gold-SFT control required")
        checks.update(method_updates=updates(r["training"],c["epochs"]),
            control_updates=updates(r["control"]["training"],c["epochs"]),eq6=eq,
            construction_gold_access={"offline_aligner":"TRAIN demonstration explicitly supplied",
                "construction_self_rewrite":"independent frozen self-builder at student checkpoint sees TRAIN demonstration",
                "gold_sft_control":"TRAIN response supervision target",
                "evaluated_student_inference":"question only; no current validation gold"},
            gold_in_student_generation_false_scope="evaluated student inference, NOT all construction model generations")
        accepted=sum(bool(x["verified"]) for x in r["rewrites"])
        if any(x.get("supervised_instances")!=accepted or x.get("supervised_tokens",0)<=0 for x in r["training"]):
            raise ValueError("SFT must use the actual verified rewrite corpus")
        for metric in (r["baseline"],r["method_metrics"],r["control"]["metrics"]):
            if sum(metric[s]["examples"] for s in ("acquisition","retention"))!=c["validation_examples"]:
                raise ValueError("both predeclared validation slices required")
    elif key=="upturn":
        if (r.get("execution_status")!="passed" or not r.get("encoder_frozen") or not r.get("reasoner_frozen")
                or r.get("paragraph_boundary_protocol")!="decoded-character-boundaries-to-original-token-prefix-v1"
                or len(r["gate"]["training_bce"])!=c["gate_epochs"]
                or len(r["training_rollout_audits"])!=c["train_examples"]*c["group"]):
            raise ValueError("actual frozen backbones, gate and decoded paragraph rollout evidence required")
        checks.update(position_updates=updates(r["training"],c["steps"]),gate_epochs=c["gate_epochs"],
            assessment_semantics="one shared assessment AFTER head training: frozen reasoner control versus trained intervention",
            assessment_is_training_before_after=False,matched_maximum_response_allowance=True,matched_actual_compute=False)
        informative=0
        for step in r["training"]:
            rewards=step["rescue_rewards"]
            advantages=step["advantages"]
            if len(rewards)!=len(advantages) or len(rewards)!=len(step["cuts"]) or len(rewards)>c["cuts"]:
                raise ValueError("actual sampled cuts/rewards/advantages must match")
            mean=sum(rewards)/len(rewards)
            if (any(not 0<=x<=1 for x in rewards)
                    or any(not math.isclose(a,x-mean,abs_tol=1e-6) for a,x in zip(advantages,rewards,strict=True))):
                raise ValueError("position advantages must derive from actual rescue rewards")
            signal=any(abs(a)>0 for a in advantages)
            if signal!=step["nonzero_rescue_advantage"]:
                raise ValueError("rescue signal cannot be fabricated")
            informative+=signal
        if not informative or informative!=r["position_informative_groups"]:
            raise ValueError("nonzero actual rescue signal required")
        checks["position_informative_groups"]=informative
        for a in r["training_rollout_audits"]:
            cuts=a["paragraph_cut_indices"]
            if (a["paragraph_cut_count"]!=len(cuts) or cuts!=sorted(set(cuts))
                    or any(not 0<x<min(a["response_tokens"],c["max_tokens"]) for x in cuts)
                    or a["eligible_for_position"]!=(not a["correctness"] and len(cuts)>=2)):
                raise ValueError("actual token-prefix eligibility audit mismatch")
        if len(r["generation_budget_controls"])!=c["validation_examples"]:
            raise ValueError("actual assessment budget audit required")
        if any(m.get("examples")!=c["validation_examples"] for m in (r["baseline"],r["method_metrics"])):
            raise ValueError("both actual assessment example counts must match validation_examples")
        for a in r["generation_budget_controls"]:
            n=c["evaluation_group"]
            if not (n<=a["method_generations"]<=2*n and a["base_generations"]==2*n
                    and a["maximum_response_token_allowance"]==2*n*c["max_tokens"]):
                raise ValueError("matched maximum allowance required, not invented identical realized cost")
    else:
        if r.get("paragraph_boundary_protocol")!="decoded-character-boundaries-to-original-token-prefix-v1":
            raise ValueError("corrected original-token paragraph mechanism required")
        profiled=[a for a in r["teacher_audits"] if a.get("profiled")]
        if not profiled or any(not a.get("verified_backbone") for a in profiled):
            raise ValueError("real verified and MC-profiled teacher corpus required")
        for a in profiled:
            p=a["profile"]
            if (not 0<len(p)<=c["prefix_states"] or a["paragraph_cut_indices"]!=[x["prefix_tokens"] for x in p]
                    or any(not 0<x["prefix_tokens"]<a["response_tokens"] or x["samples"]!=c["branches"]
                           or not 0<=x["reachability"]<=1
                           or not math.isclose(x["uncertainty"],4*x["reachability"]*(1-x["reachability"]),abs_tol=1e-8) for x in p)):
                raise ValueError("actual prefix MC reachability/uncertainty mismatch")
        pool,scores=contract_teacher_pool([a["profile"] for a in profiled],c["pool_ratio"])
        if pool!=r["teacher_pool_indices"] or scores!=r["teacher_uncertainty_scores"]:
            raise ValueError("teacher contraction must derive from actual MC profiles")
        if len(r["learner_routes"])!=c["epochs"]-1:
            raise ValueError("complete learner-routing history required")
        for index,route in enumerate(r["learner_routes"]):
            losses=route["normalized_response_nll"]
            if (len(losses)!=len(pool) or route["epoch"]!=index+2
                    or route["active_indices"]!=[pool[i] for i in route_student(losses,c["active_size"])]):
                raise ValueError("active routes must derive from actual student response NLL")
        exposure=len(pool)+(c["epochs"]-1)*c["active_size"]
        if (r["exposure"]["method"]!=exposure or r["exposure"]["full_sft_control"]!=c["epochs"]*len(profiled)
                or not math.isclose(r["exposure"]["relative_to_verified_full_sft"],exposure/(c["epochs"]*len(profiled)))
                or r["exposure"]["teacher_profiling_cost_excluded_from_ratio_but_reported"] is not True
                or r["control"]["method"]!="verified-full-sft"):
            raise ValueError("paired full-corpus control/exposure scope required")
        checks.update(method_updates=updates(r["training"],c["epochs"]),
            control_updates=updates(r["control"]["training"],c["epochs"]),verified_profiled_corpus=len(profiled),
            teacher_uncertainty_scores=scores,teacher_pool_indices=pool,exposure=r["exposure"],
            exposure_ratio_is_total_compute_saving=False)
    return checks


def curate(directory,contract,audit,config,*,accelerator,validated_at):
    r=json.loads((directory/"evidence/result.json").read_text())
    launch=json.loads((directory/"launch.json").read_text())
    exit_record=json.loads((directory/"exit.json").read_text())
    key=r["method"]
    if key not in IDENTIFIERS:
        raise ValueError("unsupported full-chain method")
    canonical=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    if (contract["source_commit"]!=COMMITS[key] or audit.get("source_commit")!=contract["source_commit"]
            or audit.get("source_file_sha256")!=contract["source_file_sha256"]
            or launch.get("source_file_sha256")!=contract["source_file_sha256"]
            or launch.get("source_commit")!=contract["source_commit"]
            or not audit.get("source_hashes_verified") or audit.get("cuda_initialized") is not False
            or audit.get("model_instantiated") is not False or audit.get("execution_config_sha256")!=canonical
            or launch.get("execution_config_sha256")!=canonical):
        raise ValueError("actual frozen core/source/config CPU audit and launch must agree")
    timeout={"synthself":600,"upturn":900,"progressive-contraction":1800}[key]
    if (launch["job"].get("timeout_seconds")!=timeout or exit_record.get("elapsed_seconds",0)>timeout):
        raise ValueError("actual invocation must respect the unchanged granted per-job wall cap")
    if (exit_record.get("exit_code")!=0 or exit_record.get("elapsed_seconds",0)<=0
            or launch.get("seed")!=42 or r.get("seed")!=42 or r.get("device")!="cuda"
            or r.get("parameters_changed") is not True or r.get("diagnostic_only") is not True
            or r.get("promotion_eligible") is not False or r["dataset"].get("verified") is not True
            or r["dataset"].get("test_read") is not False or r["protocol"].get("test_opened") is not False
            or r["protocol"].get("gold_in_student_generation") is not False):
        raise ValueError("actual successful seed42 CUDA/gold/test isolation evidence required")
    c={**config["shared"],**config["methods"][key],**launch["job"]["overrides"]}
    if c!=launch["effective_config"] or launch["job"]["method"]!=key:
        raise ValueError("full effective launch budget must match exact config and overrides")
    for field in ("train_examples","validation_examples","max_tokens"):
        if c[field]!=r["protocol"][field]:
            raise ValueError("measured protocol must match effective budget")
    for flag,value in {"--method":key,"--seed":"42"}.items():
        command=launch["command"]
        if flag not in command or command[command.index(flag)+1]!=value:
            raise ValueError("actual argv does not match measured method/seed")
    for role,resource in (("teacher" if key=="upturn" else "student",r["checkpoint"]),
                          ("student" if key=="upturn" else "teacher",r["encoder"] if key=="upturn" else r["teacher"])):
        verified=audit["resources"][role]
        if (resource["public_id"]!=verified["public_id"] or resource["revision"]!=verified["revision"]
                or resource["verified_mirror"]["file_sha256"]!=verified["file_sha256"] or not verified["verified"]):
            raise ValueError("actual checkpoint must match independently byte-verified public resource")
    finite_tree(r);finite_tree(exit_record)
    checks=validate_mechanism(r,c)
    checks["invocation_elapsed_seconds"]=exit_record["elapsed_seconds"]
    checks["configured_wall_cap_seconds"]=timeout
    metrics={}
    def flatten(value,prefix):
        for name,child in value.items():
            if isinstance(child,dict):
                flatten(child,prefix+"."+name)
            elif name in ("accuracy","avg_accuracy","pass_rate"):
                metrics[prefix+"."+name]={"mean":child,"std":0.,"n":1}
    flatten(r["baseline"],"frozen_reasoner_control" if key=="upturn" else "initial")
    flatten(r["method_metrics"],"trained_intervention" if key=="upturn" else "method_validation")
    if key!="upturn":
        flatten(r["control"]["metrics"],r["control"]["method"])
    metric_path=f"docs/reproductions/{IDENTIFIERS[key]}-{key}/metrics/public-a100-complete-seed42.json"
    receipt_path=f"docs/gpu-validations/{key}-a100-20261014.json"
    limitations=["One seed42 full-definition L1 mechanism smoke, not a formal capability comparison or stable gain.",
        "Original default seeds43/44 remain unfinished; this receipt does not complete the accepted full batch plan.",
        "Only four validation cases; official test content was not opened or used for selection.",
        "Actual token cost is retained; matched configured caps do not imply identical realized compute."]+r["limitations"]
    if key=="upturn":
        limitations.append("Control/intervention are assessed together after head training, NOT training-before/after; pass_rate degradation is retained.")
    elif key=="synthself":
        limitations.append("TRAIN gold is visible to offline aligner and construction self-builder, but never evaluated student inference.")
    artifact={"schema_version":2,"adapter_key":key,"manifest_ref":"reproduction:"+key,"method":key,
        "measured_locally":True,"diagnostic_only":True,"promotion_eligible":False,"seeds":[42],
        "whole_method_gpu_validation_passed":True,"default_three_seed_plan_completed":False,
        "seed_results":[{"seed":42,"diagnostic_only":True,"device":"cuda","result":r}],
        "aggregate_metrics":metrics,"execution_checks":checks,"actual_cuda_run_count":1,
        "dataset":r["dataset"],"checkpoint":r["checkpoint"],
        "evaluation_protocol":{"tier":"l1_mechanism","seeds":[42],"formal_comparison":False,"promotion_eligible":False,
            "test_used_for_selection":False,"default_three_seed_plan_completed":False,"pending_seeds":[43,44],
            "claim_policy":"single-seed mechanism smoke; no stable relative capability or production claim"},
        "provenance":{"code_commit":contract["source_commit"],"artifact_path":metric_path,
            "dataset_fingerprint":hashlib.sha256(json.dumps(r["dataset"],sort_keys=True).encode()).hexdigest(),
            "execution_config_sha256":canonical,"raw_result_sha256":hashlib.sha256((directory/"evidence/result.json").read_bytes()).hexdigest()},
        "limitations":limitations}
    command=["python","scripts/run_oct13_post_training.py","--method",key,"--config","data/oct13_execution.json",
             "--seed","42","--output","runs/complete-"+key+"-s42"]
    receipt={"schema_version":1,"adapter_key":key,"validated_at":validated_at,"seeds":[42],
        "accelerator":{"vendor":"NVIDIA","model":accelerator},"command":command,"command_path_relocations_only":True,
        "dataset":r["dataset"],"checkpoint":{"policy":r["checkpoint"],
            "encoder" if key=="upturn" else "teacher":r["encoder"] if key=="upturn" else r["teacher"]},
        "result":"passed","metrics":metrics,"execution_checks":checks,"limitations":limitations,
        "executed_source_sha256":contract["source_file_sha256"],
        "provenance":{"commit":contract["source_commit"],"artifact_path":receipt_path,"metrics_artifact":metric_path,
            "execution_config_sha256":canonical,"raw_result_sha256":artifact["provenance"]["raw_result_sha256"],"checkpoint_committed":False}}
    errors=validate_gpu_receipt(receipt)
    if errors:
        raise ValueError(errors)
    return artifact,receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for field in ("run-directory","contract","audit","config","output"):
        parser.add_argument("--"+field,type=Path,required=True)
    parser.add_argument("--accelerator",required=True)
    parser.add_argument("--validated-at",required=True)
    args=parser.parse_args()
    artifact,receipt=curate(args.run_directory,json.loads(args.contract.read_text()),json.loads(args.audit.read_text()),
        json.loads(args.config.read_text()),accelerator=args.accelerator,validated_at=args.validated_at)
    args.output.mkdir(parents=True,exist_ok=False)
    for name,value in (("result.json",artifact),("receipt.json",receipt)):
        with (args.output/name).open("x") as stream:
            stream.write(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"method":artifact["method"],"completed_seed":42,"default_three_seed_plan_completed":False}))


if __name__=="__main__":
    main()
