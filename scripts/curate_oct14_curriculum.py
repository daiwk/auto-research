#!/usr/bin/env python3
"""Curate the three actual seed-42 curriculum arms; not a three-seed claim."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from auto_research.gpu_validation import validate_gpu_receipt
from auto_research.reproductions.grpo_difficulty_curriculum.algorithm import BANDS, PlateauSchedule

KEY="grpo-difficulty-curriculum"
VARIANTS=("fixed-medium","staged","too-hard")
METRICS="docs/reproductions/2610.13669-grpo-difficulty-curriculum/metrics/public-a100-three-arms-seed42.json"
RECEIPT="docs/gpu-validations/grpo-difficulty-curriculum-a100-20261014.json"
MATCHED=("steps","group","train_examples","validation_examples","max_tokens","learning_rate","context_limit")


def curate(directories,contract,audit,*,accelerator,validated_at):
    if (audit.get("source_commit")!=contract["source_commit"]
            or audit.get("source_file_sha256")!=contract["source_file_sha256"]
            or not audit.get("source_hashes_verified") or audit.get("cuda_initialized") is not False
            or audit.get("model_instantiated") is not False):
        raise ValueError("matching actual CPU source audit required")
    rows={}
    for directory in directories:
        r=json.loads((directory/"evidence/result.json").read_text())
        l=json.loads((directory/"launch.json").read_text())
        e=json.loads((directory/"exit.json").read_text())
        v=r.get("variant")
        if v not in VARIANTS or v in rows or r.get("seed")!=42 or l.get("seed")!=42:
            raise ValueError("exactly three distinct actual seed-42 arms required")
        if (l.get("source_commit")!=contract["source_commit"]
                or l.get("source_file_sha256")!=contract["source_file_sha256"]
                or l.get("execution_config_sha256")!=audit.get("execution_config_sha256")
                or e.get("exit_code")!=0 or not math.isfinite(e.get("elapsed_seconds",0)) or e["elapsed_seconds"]<=0):
            raise ValueError("immutable source/config/successful exit evidence mismatch")
        c=l["effective_config"]
        command=l["command"]
        for flag,value in {"--method":KEY,"--seed":"42","--variant":v}.items():
            if flag not in command or command[command.index(flag)+1]!=value:
                raise ValueError("actual argv mismatch")
        if (r.get("method")!=KEY or r.get("device")!="cuda" or r.get("execution_status")!="passed"
                or not r.get("parameters_changed") or r.get("diagnostic_only") is not True
                or not r["dataset"].get("verified") or r["dataset"].get("test_read") is not False
                or r["protocol"].get("test_opened") is not False
                or r["protocol"].get("gold_in_student_generation") is not False
                or c.get("variant")!=v or l["job"]["overrides"].get("variant")!=v):
            raise ValueError("actual CUDA updates and gold/test isolation required")
        for field in ("train_examples","validation_examples","max_tokens"):
            if r["protocol"].get(field)!=c[field]:
                raise ValueError("actual protocol does not match launch budget")
        history=r["training"]
        if len(history)!=c["steps"] or len(r["difficulty_history"])!=len(history):
            raise ValueError("actual complete difficulty recalibration history required")
        schedule=PlateauSchedule()
        updates=0
        for index,step in enumerate(history):
            expected=BANDS[schedule.stage] if v=="staged" else BANDS[4 if v=="too-hard" else 2]
            if tuple(step["band"])!=expected or step["step"]!=index+1 or len(step["groups"])!=c["train_examples"]:
                raise ValueError("paper band or actual step/group budget mismatch")
            actual=0
            for group_index,g in enumerate(step["groups"]):
                rate=g["current_success"]
                if (not math.isfinite(rate) or not 0<=rate<=1
                        or g["training_row"]!=group_index or rate!=r["difficulty_history"][index][group_index]
                        or g["eligible"]!=(expected[0]<=rate<=expected[1])):
                    raise ValueError("difficulty gate must use actual current-policy correctness")
                if not g["eligible"]:
                    if g.get("optimizer_update_executed"):
                        raise ValueError("rejected group cannot update")
                    continue
                correctness=g["correctness_rewards"]
                if (len(correctness)!=c["group"] or any(x not in (0,1) for x in correctness)
                        or sum(correctness)/len(correctness)!=rate):
                    raise ValueError("correctness rollout group mismatch")
                if g.get("optimizer_update_executed"):
                    if (g.get("zero_advantage_group") is not False
                            or not math.isfinite(g.get("gradient_l2_norm",0)) or g["gradient_l2_norm"]<=0
                            or not g.get("advantages") or not any(abs(a)>0 for a in g["advantages"])
                            or any(not math.isfinite(a) for a in g["advantages"])
                            or len(g["advantages"])!=c["group"]):
                        raise ValueError("effective update requires real nonzero advantage/gradient")
                    rewards=g.get("rewards",[])
                    if (len(rewards)!=c["group"] or any(not math.isfinite(x) for x in rewards)
                            or any(not (math.isclose(x-y,0.,abs_tol=1e-6) or math.isclose(x-y,.2,abs_tol=1e-6))
                                   for x,y in zip(rewards,correctness,strict=True))):
                        raise ValueError("length shaping cannot replace correctness reward")
                    mean=sum(rewards)/len(rewards)
                    std=(sum((x-mean)**2 for x in rewards)/len(rewards))**.5
                    if any(not math.isclose(a,(x-mean)/(std+1e-6),abs_tol=1e-5)
                           for a,x in zip(g["advantages"],rewards,strict=True)):
                        raise ValueError("advantages must derive from actual group rewards")
                    actual+=1
            if actual!=step["effective_updates"]:
                raise ValueError("reported effective-update count mismatch")
            expected_transition=(schedule.observe(step["validation_diagnostic"]["accuracy"]) if actual else "no-effective-updates") if v=="staged" else "not-staged"
            if step["transition"]!=expected_transition:
                raise ValueError("staged transition must follow actual validation and updates")
            updates+=actual
        if not updates:
            raise ValueError("zero actual updates cannot sign passed")
        rows[v]=(r,l,e,updates,directory)
    if set(rows)!=set(VARIANTS):
        raise ValueError("all three measured arms required")
    first=rows[VARIANTS[0]]
    for r,l,_,_,_ in rows.values():
        if (any(r[k]!=first[0][k] for k in ("checkpoint","dataset","baseline"))
                or any(l["effective_config"][k]!=first[1]["effective_config"][k] for k in MATCHED)):
            raise ValueError("paired initial checkpoint/data and configured budgets required")
    checks={v:{"actual_optimizer_updates":n,"invocation_elapsed_seconds":e["elapsed_seconds"],
        "validation_examples":r["method_metrics"]["examples"],"difficulty_recalibration_steps":len(r["difficulty_history"]),
        "actual_bands":[s["band"] for s in r["training"]],"actual_stage_transitions":[s["transition"] for s in r["training"]],
        "measured_cost":r["cost"]} for v,(r,_,e,n,_) in rows.items()}
    metrics={f"{v}.{phase}.accuracy":{"mean":r[key]["accuracy"],"std":0.,"n":1}
        for v,(r,_,_,_,_) in rows.items() for phase,key in (("initial","baseline"),("validation","method_metrics"))}
    limitations=["One seed and three variants are NOT three independent seeds; L1 mechanism smoke only.",
        "Four validation examples cannot establish stable gains or original B5 degradation; test stayed isolated.",
        "Matched configured rollout caps do not imply equal effective updates, realized token cost or runtime.",
        "Only fixed-medium/staged/B5-too-hard were executed; static and unfiltered controls are not claimed.",
        "Original default seeds 43/44 remain unfinished; passing this CUDA smoke does not complete the batch plan.",
        "Staged reached B2, not the full original B1-to-B5 curriculum; validation cadence is reduced-scale."]
    artifact={"schema_version":2,"adapter_key":KEY,"manifest_ref":"reproduction:"+KEY,"method":KEY,
        "measured_locally":True,"diagnostic_only":True,"promotion_eligible":False,"seeds":[42],
        "seed_results":[{"seed":42,"diagnostic_only":True,"device":"cuda","variants":{v:rows[v][0] for v in VARIANTS}}],
        "aggregate_metrics":metrics,"execution_checks":checks,"actual_cuda_run_count":3,
        "dataset":first[0]["dataset"],"checkpoint":first[0]["checkpoint"],
        "evaluation_protocol":{"tier":"l1_mechanism","seeds":[42],"formal_comparison":False,"promotion_eligible":False,
            "test_used_for_selection":False,"matched_configured_budget":True,"matched_actual_compute":False,
            "claim_policy":"single-seed mechanism smoke, not stable capability or production improvement"},
        "provenance":{"code_commit":contract["source_commit"],"artifact_path":METRICS,
            "dataset_fingerprint":hashlib.sha256(json.dumps(first[0]["dataset"],sort_keys=True).encode()).hexdigest(),
            "execution_config_sha256":audit["execution_config_sha256"],
            "raw_results_sha256":{v:hashlib.sha256((rows[v][4]/"evidence/result.json").read_bytes()).hexdigest() for v in VARIANTS}},
        "limitations":limitations}
    commands=[["python","scripts/run_oct13_post_training.py","--method",KEY,"--config","data/oct13_execution.json",
        "--seed","42","--output","runs/curriculum-"+v+"-s42","--variant",v] for v in VARIANTS]
    receipt={"schema_version":1,"adapter_key":KEY,"validated_at":validated_at,"seeds":[42],"variants":list(VARIANTS),
        "accelerator":{"vendor":"NVIDIA","model":accelerator},"command":commands[0],"all_sanitized_commands":commands,
        "command_path_relocations_only":True,"dataset":artifact["dataset"],"checkpoint":artifact["checkpoint"],
        "result":"passed","metrics":metrics,"execution_checks":checks,"limitations":limitations,
        "executed_source_sha256":contract["source_file_sha256"],
        "provenance":{"commit":contract["source_commit"],"artifact_path":RECEIPT,"metrics_artifact":METRICS,
            "execution_config_sha256":audit["execution_config_sha256"],"checkpoint_committed":False}}
    errors=validate_gpu_receipt(receipt)
    if errors:
        raise ValueError(errors)
    return artifact,receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-directory",type=Path,action="append",required=True)
    parser.add_argument("--contract",type=Path,required=True)
    parser.add_argument("--audit",type=Path,required=True)
    parser.add_argument("--accelerator",required=True)
    parser.add_argument("--validated-at",required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        raise FileExistsError("curation output is immutable")
    artifact,receipt=curate(args.run_directory,json.loads(args.contract.read_text()),json.loads(args.audit.read_text()),
        accelerator=args.accelerator,validated_at=args.validated_at)
    args.output.mkdir(parents=True,exist_ok=False)
    for name,value in (("result.json",artifact),("receipt.json",receipt)):
        with (args.output/name).open("x") as stream:
            stream.write(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"actual_cuda_runs":3,"independent_seeds":1,"diagnostic_only":True}))


if __name__=="__main__":
    main()
