"""CPU-only five-arm repaired cohort audit; failed/zero groups remain explicit."""
import hashlib
import argparse
import json
import math
from pathlib import Path
import statistics

from auto_research.reproductions.grpo_difficulty_curriculum.algorithm import BANDS,PlateauSchedule,difficulty_dynamics

COMMIT="b90862754bf51b1beeb5add3f7dc2a51ca00ace4"
PRECISION_SHA="d19401266a420afdc64867f145f8384fd649dc1991e4b74ea1f7ee8b8d91bde5"
OBSERVER="92c2081869dcfbcec89b85580721d9bdb0dd136c"
OBSERVER_SHA="e106b23ff74d4d7ffc4572fddd77780ef1811eb2f33cb1967d8f86776874d36c"
VARIANTS={"unfiltered","static","fixed-medium","staged","too-hard"}
KEY="grpo-difficulty-curriculum"


def finite(value):
    if isinstance(value,float) and not math.isfinite(value):
        raise ValueError("nonfinite evidence cannot be accepted")
    if isinstance(value,dict):
        for item in value.values():finite(item)
    elif isinstance(value,list):
        for item in value:finite(item)


def audit_training(r):
    v=r["variant"]
    history=r["difficulty_history"]
    if len(history)!=4 or any(len(row)!=8 or any(not 0<=x<=1 for x in row) for row in history):
        raise ValueError("four actual current-policy calibration rounds of eight rows required")
    order=sorted(range(8),key=lambda i:(-history[0][i],i))
    if r["initial_static_easy_to_hard_order"]!=(order if v=="static" else None):
        raise ValueError("static order must derive from initial current-policy success rates")
    if r["difficulty_dynamics"]!=difficulty_dynamics(history) or len(r["training"])!=4:
        raise ValueError("difficulty dynamics must derive from all four rounds")
    schedule=PlateauSchedule()
    updates=equal=eligible_count=0
    zero_ledgers=[]
    for index,step in enumerate(r["training"]):
        band=BANDS[schedule.stage] if v=="staged" else BANDS[4] if v=="too-hard" else BANDS[2]
        groups=step["groups"]
        if (step["step"]!=index+1 or tuple(step["band"])!=band or len(groups)!=8
            or {g["training_row"] for g in groups}!=set(range(8)) or step["validation_diagnostic"]["examples"]!=4):
            raise ValueError("original step, band, complete group ledger and validation cadence required")
        static_indices=set(order[index*2:(index+1)*2])
        actual=0
        for g in groups:
            row=g["training_row"]
            rate=history[index][row]
            expected=(v=="unfiltered" or (row in static_indices if v=="static" else band[0]<=rate<=band[1]))
            if g["current_success"]!=rate or g["eligible"] is not expected:
                raise ValueError("eligibility must derive from actual current-policy correctness, not shaped rewards")
            if not expected:
                if g.get("optimizer_update_executed") or "advantages" in g:
                    raise ValueError("rejected group cannot carry an optimizer update or invented advantages")
                continue
            eligible_count+=1
            correctness,rewards=g["correctness_rewards"],g["rewards"]
            if (len(correctness)!=8 or len(rewards)!=8 or any(x not in (0,1) for x in correctness)
                or sum(correctness)/8!=rate or any(not (math.isclose(x-y,0.,abs_tol=1e-6)
                    or math.isclose(x-y,.2,abs_tol=1e-6)) for x,y in zip(rewards,correctness,strict=True))):
                raise ValueError("actual binary correctness and unchanged auxiliary length reward required")
            if len(set(rewards))==1:
                equal+=1
                if (g["optimizer_update_executed"] is not False or g["zero_advantage_group"] is not True
                    or ("advantages" in g and (len(g["advantages"])!=8 or any(g["advantages"])))):
                    raise ValueError("equal rewards must have exact zero advantage and skip all optimizer work")
                zero_ledgers.append({"step":index+1,"training_row":row,"rewards":rewards,
                    "optimizer_update_executed":False,"zero_advantage_group":True,
                    "advantages_recorded":g.get("advantages"),"advantages_field_present":"advantages" in g})
                continue
            advantages=g["advantages"]
            centered=[x-rewards[0] for x in rewards]
            mean=sum(centered)/8
            centered=[x-mean for x in centered]
            std=(sum(x*x for x in centered)/8)**.5
            expected_adv=[x/(std+1e-6) for x in centered]
            if (len(advantages)!=8 or any(not math.isclose(a,b,abs_tol=1e-5) for a,b in zip(advantages,expected_adv,strict=True))
                or g["optimizer_update_executed"] is not True or g["zero_advantage_group"] is not False
                or not math.isfinite(g["gradient_l2_norm"]) or g["gradient_l2_norm"]<=0):
                raise ValueError("reward-varying update must have actual normalized advantages and finite positive gradient")
            actual+=1
        if step["effective_updates"]!=actual:
            raise ValueError("actual optimizer calls must match every eligible group ledger")
        transition=(schedule.observe(step["validation_diagnostic"]["accuracy"]) if actual else "no-effective-updates") if v=="staged" else "not-staged"
        if step["transition"]!=transition:
            raise ValueError("staged transition must replay original plateau schedule, including no-update rounds")
        updates+=actual
    return {"actual_optimizer_updates":updates,"eligible_groups":eligible_count,
        "mathematically_equal_reward_groups_skipped":equal,"equal_reward_optimizer_updates":0,
        "actual_zero_group_ledgers":zero_ledgers,"all_groups_audited":32}


def validate_run(directory,contract,audit,config):
    raw=directory/"evidence/result.json"
    r=json.loads(raw.read_text())
    l=json.loads((directory/"launch.json").read_text())
    e=json.loads((directory/"exit.json").read_text())
    m=json.loads((directory/"gpu-memory.json").read_text())
    binding=json.loads((directory/"observer-binding.json").read_text())
    canonical=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    v,seed=r["variant"],r["seed"]
    c={**config["shared"],**config["methods"][KEY],"variant":v}
    if (v not in VARIANTS or seed not in (42,43,44) or l["seed"]!=seed or r["method"]!=KEY
        or contract["source_commit"]!=COMMIT or l["source_commit"]!=COMMIT or audit["source_commit"]!=COMMIT
        or len(contract["source_file_sha256"])!=54
        or contract["source_file_sha256"].get("src/auto_research/post_training/oct13_common.py")!=PRECISION_SHA
        or any(x["source_file_sha256"]!=contract["source_file_sha256"] for x in (l,audit))
        or audit["source_hashes_verified"] is not True or audit["cuda_initialized"] is not False
        or audit["model_instantiated"] is not False or audit["execution_config_sha256"]!=canonical
        or l["execution_config_sha256"]!=canonical or l["effective_config"]!=c
        or e["exit_code"] not in (0,1) or not 0<e["elapsed_seconds"]<=900
        or l["job"]["timeout_seconds"]!=900 or l["gpu_slot_grant"]!="A30-post-training-explicit-slot"):
        raise ValueError("actual repaired source, config, seed, A30 launch and original wall bound required")
    if (c["train_examples"]!=8 or c["validation_examples"]!=4 or c["steps"]!=4 or c["group"]!=8
        or c["max_tokens"]!=512 or c["context_limit"]!=4096 or c["learning_rate"]!=1e-5
        or r["protocol"]["train_examples"]!=8 or r["protocol"]["validation_examples"]!=4
        or r["protocol"]["max_tokens"]!=512 or r["protocol"]["gold_in_student_generation"] is not False
        or r["protocol"]["test_opened"] is not False or r["device"]!="cuda"
        or r["diagnostic_only"] is not True or r["promotion_eligible"] is not False
        or r["dataset"]["verified"] is not True or r["dataset"]["test_read"] is not False
        or r["dataset"]!=audit["public_train_only_holdout"]
        or any(r[k]["examples"]!=4 for k in ("baseline","method_metrics"))
        or sum(r["cost"]["generated_tokens"].values())>143360):
        raise ValueError("original method budget, real CUDA and gold/test isolation required")
    resource=audit["resources"]["student"]
    if (resource["verified"] is not True or resource["public_id"]!=c["student_id"]
        or resource["revision"]!=c["student_revision"] or r["checkpoint"]["public_id"]!=resource["public_id"]
        or r["checkpoint"]["revision"]!=resource["revision"]
        or r["checkpoint"]["verified_mirror"]["file_sha256"]!=resource["file_sha256"]):
        raise ValueError("actual fixed public checkpoint bytes required")
    if (m["core_commit"]!=COMMIT or m["observer_commit"]!=OBSERVER
        or m["observer_source_sha256"]!=OBSERVER_SHA or m["core_exit_code"]!=e["exit_code"]
        or m["accelerator"]["model"]!="NVIDIA A30" or m["seed"]!=seed or m["variant"]!=v
        or m["peak_memory_available"] is not True or m["no_monkeypatch"] is not True
        or m["training_arguments_forwarded_unchanged"] is not True
        or not 0<m["actual_max_memory_allocated_bytes"]<=m["actual_max_memory_reserved_bytes"]<=20*1024**3
        or binding["core_commit"]!=COMMIT or binding["observer_commit"]!=OBSERVER
        or binding["observer_source_sha256"]!={"scripts/observe_oct14_cuda_memory.py":OBSERVER_SHA}):
        raise ValueError("actual observational peak with unchanged core and observer double binding required")
    for flag,value in {"--method":KEY,"--seed":str(seed),"--variant":v}.items():
        if flag not in l["command"] or l["command"][l["command"].index(flag)+1]!=value:
            raise ValueError("actual argv mismatch")
    finite(r);finite(e);finite(m)
    check=audit_training(r)
    changed=check["actual_optimizer_updates"]>0
    expected_status="passed" if changed else "passed-negative-control" if v=="too-hard" else "failed-no-effective-updates"
    if (r["parameters_changed"] is not changed or r["execution_status"]!=expected_status
        or e["exit_code"]!=(0 if changed or v=="too-hard" else 1)):
        raise ValueError("actual zero-update outcome cannot be reclassified as a positive mechanism")
    check.update(invocation_elapsed_seconds=e["elapsed_seconds"],configured_wall_cap_seconds=900,
        peak_memory=m,measured_cost=r["cost"],execution_complete=True,
        mechanism_passed=changed,negative_control_completed=(v=="too-hard" and not changed))
    return r,check,hashlib.sha256(raw.read_bytes()).hexdigest()


def curate(directories,contract,audit,config):
    rows={}
    checks={}
    hashes={}
    for d in directories:
        r,c,h=validate_run(d,contract,audit,config)
        identity=(r["seed"],r["variant"])
        if identity in rows:raise ValueError("duplicates are not independent seeds")
        rows[identity]=r;checks[identity]=c;hashes[identity]=h
    seeds=sorted({s for s,_ in rows})
    if seeds not in ([42],[42,43,44]) or set(rows)!={(s,v) for s in seeds for v in VARIANTS}:
        raise ValueError("complete exact five-arm seed42 or original fifteen-run cohort required")
    for seed in seeds:
        first=rows[seed,"unfiltered"]
        if any(rows[seed,v][k]!=first[k] for v in VARIANTS for k in ("dataset","checkpoint","baseline")):
            raise ValueError("all same-device/framework seed arms must have identical initial baseline/resources")
    first=rows[42,"unfiltered"]
    if any(r[k]!=first[k] for r in rows.values() for k in ("dataset","checkpoint")):
        raise ValueError("all seeds must have identical fixed public dataset/checkpoint bytes")
    accepted=all(c["mechanism_passed"] or c["negative_control_completed"] for c in checks.values())
    metrics={}
    for v in sorted(VARIANTS):
        for phase,key in (("initial","baseline"),("validation","method_metrics")):
            values=[rows[s,v][key]["accuracy"] for s in seeds]
            metrics[v+"."+phase+".accuracy"]={"mean":statistics.mean(values),"std":statistics.stdev(values) if len(seeds)>1 else 0.,"n":len(seeds)}
    return {"schema_version":2,"adapter_key":KEY,"manifest_ref":"reproduction:"+KEY,"method":KEY,
        "measured_locally":True,"diagnostic_only":True,"promotion_eligible":False,"not_gpu_receipt":True,
        "seeds":seeds,"actual_cuda_run_count":len(rows),"execution_complete":True,
        "all_seed_arm_mechanisms_or_negative_controls_accepted":accepted,
        "whole_method_gpu_validation_passed":False,"default_three_seed_plan_completed":seeds==[42,43,44],
        "seed_results":[{"seed":s,"device":"cuda","diagnostic_only":True,"variants":{v:rows[s,v] for v in sorted(VARIANTS)}} for s in seeds],
        "aggregate_metrics":metrics,"dataset":rows[42,"unfiltered"]["dataset"],"checkpoint":rows[42,"unfiltered"]["checkpoint"],
        "execution_checks":{str(s):{v:checks[s,v] for v in sorted(VARIANTS)} for s in seeds},
        "evaluation_protocol":{"tier":"l1_mechanism","seeds":seeds,"formal_comparison":False,
            "claim_policy":"single/few-seed smoke result; do not claim a stable improvement",
            "promotion_eligible":False,"test_used_for_selection":False,"within_A30_same_seed_arms_paired":True,
            "paired_with_old_A100_or_51b":False,"variants_are_independent_seeds":False,
            "concurrent_latency_comparison_eligible":False},
        "provenance":{"code_commit":COMMIT,"executed_source_sha256":contract["source_file_sha256"],
            "artifact_path":"docs/reproductions/2610.13669-grpo-difficulty-curriculum/metrics/public-a30-complete-five-arms-"+
                ("seed42" if seeds==[42] else "seeds42-44")+"-b9086275.json",
            "execution_config_sha256":hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest(),
            "dataset_fingerprint":hashlib.sha256(json.dumps(rows[42,"unfiltered"]["dataset"],sort_keys=True).encode()).hexdigest(),
            "raw_results_sha256":{str(s)+"."+v:h for (s,v),h in hashes.items()}},
        "limitations":["Zero and rejected groups are fully audited, not dropped from denominators; no old-source pseudo updates are reused.",
            "Five variants are paired method/control arms, not five independent seeds; only actually completed seeds enter descriptive metrics.",
            "This native CPU curation is not itself a GPU receipt; an accepted source-bound receipt requires a separate review.",
            "Matched configured budget is not matched realized updates/token cost; concurrency timing is not a throughput comparison."]}


def curate_with_receipt(directories,contract,audit,config,observer_contract):
    """Only all fifteen independently validated repaired runs may be signed."""
    from auto_research.gpu_validation import validate_gpu_receipt
    artifact=curate(directories,contract,audit,config)
    if (artifact["seeds"]!=[42,43,44] or artifact["actual_cuda_run_count"]!=15
        or artifact["default_three_seed_plan_completed"] is not True
        or artifact["all_seed_arm_mechanisms_or_negative_controls_accepted"] is not True
        or observer_contract["source_commit"]!=OBSERVER
        or observer_contract["source_file_sha256"]!={"scripts/observe_oct14_cuda_memory.py":OBSERVER_SHA}):
        raise ValueError("all fifteen actual repaired cores and precise independent observer binding required")
    metric_path="docs/reproductions/2610.13669-grpo-difficulty-curriculum/metrics/public-a30-complete-five-arms-seeds42-44-b9086275.json"
    receipt_path="docs/gpu-validations/grpo-difficulty-curriculum-a30-20261014-seeds42-44.json"
    artifact={**artifact,"whole_method_gpu_validation_passed":True,
        "provenance":{**artifact["provenance"],"artifact_path":metric_path,
            "observer_commit":OBSERVER,"observer_source_sha256":observer_contract["source_file_sha256"]}}
    commands=[]
    for seed in (42,43,44):
        for v in sorted(VARIANTS):
            directory="runs/curriculum-"+v+"-s"+str(seed)
            commands.append(["python","-u","scripts/observe_oct14_cuda_memory.py",
                "--core-root","workspace/core","--core-contract","data/source-contract-b9086275.json",
                "--core-audit","data/resource-audit-a30-cpu-b9086275.json",
                "--observer-root","workspace/observer","--observer-contract","data/observer-contract-92c20818.json",
                "--memory-output",directory+"/gpu-memory.json","--execute","--gpu-grant","A30-post-training-explicit-slot",
                "--","--method",KEY,"--config","data/oct14_execution-curriculum-a30-v1.json",
                "--seed",str(seed),"--output",directory+"/evidence","--variant",v])
    limitations=artifact["limitations"][:2]+artifact["limitations"][3:]+[
        "Every first-seed and remaining-seed arm is same-device/source/config; old6a/51b cohorts are not reused or pooled.",
        "Three seed groups remain L1 diagnostics, not a stable gain, original paper benchmark or production A/B.",
        "Negative staged and any other lower validation metrics are preserved; too-hard is not forced to have zero updates."]
    artifact["limitations"]=limitations
    receipt={"schema_version":1,"adapter_key":KEY,"validated_at":"2026-10-14","seeds":[42,43,44],
        "accelerator":{"vendor":"NVIDIA","model":"NVIDIA A30"},"command":commands[0],"all_sanitized_commands":commands,
        "command_path_relocations_only":True,"dataset":artifact["dataset"],"checkpoint":artifact["checkpoint"],
        "variants":sorted(VARIANTS),"result":"passed","metrics":artifact["aggregate_metrics"],
        "execution_checks":artifact["execution_checks"],"executed_source_sha256":contract["source_file_sha256"],
        "observer_binding":{"commit":OBSERVER,"source_file_sha256":observer_contract["source_file_sha256"],
            "training_core_commit":COMMIT,"source_neutral_observation":True},"limitations":limitations,
        "provenance":{"commit":COMMIT,"artifact_path":receipt_path,"metrics_artifact":metric_path,
            "execution_config_sha256":artifact["provenance"]["execution_config_sha256"],
            "raw_results_sha256":artifact["provenance"]["raw_results_sha256"],"checkpoint_committed":False}}
    errors=validate_gpu_receipt(receipt)
    if errors:raise ValueError(errors)
    return artifact,receipt


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-directory",type=Path,action="append",required=True)
    for name in ("contract","audit","config","output"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--observer-contract",type=Path)
    parser.add_argument("--receipt-output",type=Path)
    args=parser.parse_args()
    if bool(args.observer_contract)!=bool(args.receipt_output):
        parser.error("observer contract and receipt output must be provided together")
    if args.receipt_output and args.output.resolve()==args.receipt_output.resolve():
        raise ValueError("native artifact and receipt outputs must be distinct")
    for path in (args.output,args.receipt_output):
        if path is not None and path.exists():
            raise FileExistsError(path)
    inputs=[json.loads(getattr(args,k).read_text()) for k in ("contract","audit","config")]
    if args.receipt_output:
        value,receipt=curate_with_receipt(args.run_directory,*inputs,json.loads(args.observer_contract.read_text()))
        with args.receipt_output.open("x") as stream:
            stream.write(json.dumps(receipt,indent=2,allow_nan=False)+"\n")
    else:
        value=curate(args.run_directory,*inputs)
    with args.output.open("x") as stream:
        stream.write(json.dumps(value,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":main()
