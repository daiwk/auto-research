#!/usr/bin/env python3
"""Curate actual State-OPD three-arm runs without inventing audit outcomes."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics

from auto_research.gpu_validation import validate_gpu_receipt

SEEDS=(42,43,44)
VARIANTS=("state","full-history-opd","state-no-expansion")
MATCHED_FIELDS=("steps","max_turns","response_cap","transcript_cap","multiplicity","concentration")
METRICS_ARTIFACT="docs/reproductions/2610.13238-state-opd/metrics/public-a100-three-arms-seeds42-44.json"
RECEIPT_ARTIFACT="docs/gpu-validations/state-opd-a100-20261014.json"


def statistic(values):
    if not values or any(not math.isfinite(v) for v in values):
        raise ValueError("finite measured scalar metrics required")
    return {"mean":statistics.mean(values),"std":statistics.stdev(values) if len(values)>1 else 0.,"n":len(values)}


def summarize_state_arms(runs):
    indexed={}
    for run in runs:
        key=(run.get("variant"),run.get("seed"))
        if key in indexed or key[0] not in VARIANTS or key[1] not in SEEDS:
            raise ValueError("unexpected or duplicate arm/seed")
        indexed[key]=run
    if set(indexed)!={(variant,seed) for variant in VARIANTS for seed in SEEDS}:
        raise ValueError("all three actual arms and all three seeds required")
    first=indexed[("state",42)]
    checks={}
    metrics={}
    for variant in VARIANTS:
        per_seed=[]
        for seed in SEEDS:
            run=indexed[(variant,seed)]
            protocol=run.get("protocol",{})
            full=variant=="full-history-opd"
            if (run.get("method")!="state-opd" or run.get("device")!="cuda"
                    or run.get("diagnostic_only") is not True or not run.get("parameters_changed")
                    or run.get("execution_status")!="passed"):
                raise ValueError("successful actual CUDA parameter updates required")
            if (not run.get("dataset",{}).get("verified") or run["dataset"].get("test_read") is not False
                    or protocol.get("test_opened") is not False
                    or protocol.get("teacher_and_policy_receive_gold") is not False):
                raise ValueError("verified train-only input and gold isolation required")
            if any(run.get(k)!=first.get(k) for k in ("dataset","student","teacher")):
                raise ValueError("identical verified public resources required")
            if any(protocol.get(k)!=first["protocol"].get(k) for k in MATCHED_FIELDS):
                raise ValueError("matched configured training budgets required")
            if run["baseline"]!=indexed[("state",seed)]["baseline"]:
                raise ValueError("paired controls must start at the same measured initial policy")
            if protocol.get("teacher_preceding_context")!=("full-history" if full else "executed-state"):
                raise ValueError("teacher context does not match actual variant")
            if (protocol.get("effective_multiplicity")!=(1 if variant=="state-no-expansion" else protocol["multiplicity"])
                    or protocol.get("reference_independent_root_trajectories")!=(protocol["multiplicity"] if full else 1)):
                raise ValueError("variant-specific response allocation mismatch")
            training=run.get("training",[])
            audits=run.get("trajectory_audits",[])
            if len(training)!=protocol["steps"] or len(audits)!=len(training) or not training:
                raise ValueError("complete actual training/audit steps required")
            updates=0
            for step in training:
                gradient=step.get("gradient_l2_norm",0)
                executed=step.get("optimizer_update_executed")
                if not math.isfinite(gradient) or gradient<0 or bool(gradient>0)!=bool(executed) or step.get("supervised_tokens",0)<=0:
                    raise ValueError("gradient/update/token audit mismatch")
                updates+=int(bool(executed))
            if not updates:
                raise ValueError("zero actual updates cannot pass GPU validation")
            removed=0
            roots=0
            pools=0
            for audit in audits:
                amount=audit.get("teacher_prior_reasoning_removed_responses",-1)
                if (not isinstance(amount,int) or amount<0 or amount>audit.get("response_pool_size",0)
                        or audit.get("additional_actions_executed")!=0
                        or audit.get("same_current_response_prefix") is not True
                        or audit.get("environment_reward_in_loss") is not False):
                    raise ValueError("invalid response/context/environment audit")
                if full:
                    independent=audit.get("independent_root_audits",[])
                    if (amount!=0 or audit.get("root_trajectories")!=protocol["multiplicity"]
                            or len(independent)!=protocol["multiplicity"]
                            or any(a.get("additional_actions_executed")!=0 for a in independent)
                            or sum(a["root_turns"] for a in independent)!=audit["root_turns"]
                            or sum(a["root_actions_executed"] for a in independent)!=audit["root_actions_executed"]):
                        raise ValueError("full-history requires actual independent roots and no context removal")
                elif variant=="state-no-expansion" and audit["response_pool_size"]!=audit["root_turns"]:
                    raise ValueError("no-expansion arm must contain only executed root responses")
                removed+=amount
                roots+=audit["root_actions_executed"]
                pools+=audit["response_pool_size"]
            per_seed.append({"seed":seed,"actual_optimizer_updates":updates,
                "teacher_prior_reasoning_removed_responses":removed,"executed_root_actions":roots,
                "response_pool_size":pools,"supervised_tokens":sum(s["supervised_tokens"] for s in training)})
        checks[variant]={"per_seed":per_seed,"completed_seeds":3,
            "teacher_context_from_actual_protocol":"full-history" if variant=="full-history-opd" else "executed-state",
            "teacher_prior_reasoning_removed_responses_per_seed":[p["teacher_prior_reasoning_removed_responses"] for p in per_seed],
            "teacher_prior_reasoning_removed_observed":any(p["teacher_prior_reasoning_removed_responses"]>0 for p in per_seed),
            "expanded_actions_executed":0}
        for arm,label in (("baseline","initial"),("method_metrics","validation")):
            for metric in ("accuracy","submission_rate","mean_executed_actions"):
                metrics[f"{variant}.{label}.{metric}"]=statistic([indexed[(variant,s)][arm][metric] for s in SEEDS])
    for control in ("full-history-opd","state-no-expansion"):
        metrics[f"state.paired_accuracy_difference_vs_{control}"]=statistic([
            indexed[("state",s)]["method_metrics"]["accuracy"]-indexed[(control,s)]["method_metrics"]["accuracy"] for s in SEEDS])
    return {"metrics":metrics,"checks":checks,"dataset":first["dataset"],
        "checkpoint":{"student":first["student"],"teacher":first["teacher"]},
        "seed_results":[{"seed":s,"diagnostic_only":True,"device":"cuda",
            "variants":{v:indexed[(v,s)] for v in VARIANTS}} for s in SEEDS]}


def curate(directories,contract,*,accelerator,validated_at):
    runs=[]
    launches=[]
    exits=[]
    for directory in directories:
        run=json.loads((directory/"evidence/result.json").read_text())
        launch=json.loads((directory/"launch.json").read_text())
        exit_record=json.loads((directory/"exit.json").read_text())
        if (exit_record["exit_code"]!=0 or launch["source_commit"]!=contract["source_commit"]
                or launch["source_file_sha256"]!=contract["source_file_sha256"]
                or launch["seed"]!=run["seed"] or launch["job"]["overrides"]["variant"]!=run["variant"]):
            raise ValueError("actual successful immutable launcher/source evidence required")
        configured=launch["effective_config"]
        aliases={"steps":"steps","max_turns":"max_turns","max_tokens":"response_cap",
            "context_limit":"transcript_cap","multiplicity":"multiplicity","concentration":"concentration"}
        if (any(configured.get(c)!=run["protocol"].get(p) for c,p in aliases.items())
                or configured.get("validation_examples")!=run["baseline"].get("examples")
                or configured.get("variant")!=run["variant"]):
            raise ValueError("actual protocol must match the immutable effective launch configuration")
        runs.append(run)
        launches.append(launch)
        exits.append(exit_record)
    if len({l["execution_config_sha256"] for l in launches})!=1:
        raise ValueError("all arms must use the same frozen configuration")
    summary=summarize_state_arms(runs)
    for run,exit_record in zip(runs,exits,strict=True):
        elapsed=exit_record.get("elapsed_seconds")
        if elapsed is None or not math.isfinite(elapsed) or elapsed<=0:
            raise ValueError("actual positive wall-clock duration required")
        for row in summary["checks"][run["variant"]]["per_seed"]:
            if row["seed"]==run["seed"]:
                row["invocation_elapsed_seconds"]=elapsed
    ordered=sorted(zip(runs,launches,directories,strict=True),key=lambda item:(VARIANTS.index(item[0]["variant"]),item[0]["seed"]))
    limitations=["Three-seed L1 public calculator mechanism diagnostic, not original environment or formal capability evaluation.",
        "Negative/zero validation metrics are retained; optimizer updates alone do not prove task improvement.",
        "Configured response/step budgets match; realized response pools/tokens differ and full prompt/FLOP costs are not measured.",
        "Measured token cost here is training supervised response tokens; validation generation tokens are not recorded by the State runner."]
    artifact={"schema_version":2,"adapter_key":"state-opd","manifest_ref":"reproduction:state-opd",
        "method":"state-opd","diagnostic_only":True,"measured_locally":True,"seeds":list(SEEDS),
        "dataset":summary["dataset"],"checkpoint":summary["checkpoint"],"seed_results":summary["seed_results"],
        "aggregate_metrics":summary["metrics"],"execution_checks":summary["checks"],
        "actual_cuda_run_count":len(runs),
        "evaluation_protocol":{"tier":"l1_mechanism","seeds":list(SEEDS),"formal_comparison":False,"promotion_eligible":False,
            "test_used_for_selection":False,"matched_configured_budget":True,"matched_actual_compute":False,
            "claim_policy":"three-seed L1 mechanism diagnostic; no stable capability or production improvement claimed"},
        "provenance":{"code_commit":contract["source_commit"],"artifact_path":METRICS_ARTIFACT,
            "dataset_fingerprint":hashlib.sha256(json.dumps(summary["dataset"],sort_keys=True).encode()).hexdigest(),
            "execution_config_sha256":launches[0]["execution_config_sha256"],
            "raw_results_sha256":{f"{r['variant']}-s{r['seed']}":hashlib.sha256((d/"evidence/result.json").read_bytes()).hexdigest()
                for r,_,d in ordered}},
        "limitations":limitations}
    commands=[]
    for _,launch,_ in ordered:
        command=launch["command"]
        expected_flags={"--method":"state-opd","--seed":str(launch["seed"]),
            "--variant":launch["job"]["overrides"]["variant"]}
        if any(flag not in command or command[command.index(flag)+1]!=value for flag,value in expected_flags.items()):
            raise ValueError("launcher argv must match actual method/seed/variant")
        commands.append(["python","scripts/run_oct13_post_training.py","--method","state-opd",
            "--config","data/oct13_execution.json","--seed",str(launch["seed"]),
            "--output",f"runs/state-{launch['job']['overrides']['variant']}-s{launch['seed']}",
            "--variant",launch["job"]["overrides"]["variant"]])
    receipt={"schema_version":1,"adapter_key":"state-opd","validated_at":validated_at,
        "seeds":list(SEEDS),"variants":list(VARIANTS),
        "accelerator":{"vendor":"NVIDIA","model":accelerator},"command":commands[0],
        "all_sanitized_commands":commands,"command_path_relocations_only":True,
        "dataset":summary["dataset"],"checkpoint":summary["checkpoint"],"result":"passed",
        "metrics":summary["metrics"],"execution_checks":summary["checks"],"limitations":limitations,
        "executed_source_sha256":contract["source_file_sha256"],
        "provenance":{"commit":contract["source_commit"],"artifact_path":RECEIPT_ARTIFACT,
            "metrics_artifact":METRICS_ARTIFACT,"checkpoint_committed":False,
            "execution_config_sha256":launches[0]["execution_config_sha256"]}}
    errors=validate_gpu_receipt(receipt)
    if errors:
        raise ValueError(errors)
    return artifact,receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-directory",type=Path,action="append",required=True)
    parser.add_argument("--contract",type=Path,required=True)
    parser.add_argument("--accelerator",required=True)
    parser.add_argument("--validated-at",required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        raise FileExistsError("curation output is immutable; use a fresh directory")
    artifact,receipt=curate(args.run_directory,json.loads(args.contract.read_text()),
        accelerator=args.accelerator,validated_at=args.validated_at)
    args.output.mkdir(parents=True,exist_ok=False)
    for name,value in (("result.json",artifact),("receipt.json",receipt)):
        with (args.output/name).open("x") as stream:
            stream.write(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"output":str(args.output),"actual_runs":artifact["actual_cuda_run_count"],"diagnostic_only":True}))


if __name__=="__main__":
    main()
