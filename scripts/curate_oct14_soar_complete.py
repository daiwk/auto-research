"""Sanitize actual complete SOAR arms; no probe substitution or multi-seed claim."""
import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path

from auto_research.gpu_validation import validate_gpu_receipt

COMMIT="b90862754bf51b1beeb5add3f7dc2a51ca00ace4"
VARIANTS={"source-consistent","without-source-reward"}
METRIC="docs/reproductions/2610.13157-soar/metrics/public-a100-complete-seed42-b9086275.json"
RECEIPT="docs/gpu-validations/soar-a100-20261014-seed42.json"


def finite(v):
    if isinstance(v,float) and not math.isfinite(v):raise ValueError("nonfinite measured evidence")
    if isinstance(v,dict):
        for x in v.values():finite(x)
    elif isinstance(v,list):
        for x in v:finite(x)


def training_check(r):
    alpha=.1 if r["variant"]=="source-consistent" else 0.
    if len(r["training"])!=4:raise ValueError("original four training groups required")
    updates=zero=0
    ledgers=[]
    for i,step in enumerate(r["training"]):
        components=step["components"]
        if step["step"]!=i+1 or len(components)!=4:raise ValueError("original four trajectory group required")
        for c in components:
            if (any(c[k] not in (0,1) for k in ("answer","format","source_match"))
                or c["source_match"]>c["format"] or type(c["searches"]) is not int or not 0<=c["searches"]<=3):
                raise ValueError("real bounded trajectory reward component audit required")
        rewards=[(c["answer"]+.2*c["format"]+alpha*c["source_match"])/(1.2+alpha) for c in components]
        equal=len(set(rewards))==1
        if equal:
            if step["optimizer_update_executed"] is not False or step["zero_advantage_group"] is not True:
                raise ValueError("equal trajectory reward must have exact zero optimizer updates")
            if "trajectory_advantages" in step and any(step["trajectory_advantages"]):
                raise ValueError("equal reward pseudo advantages are not valid")
            if "trajectory_rewards" in step and step["trajectory_rewards"]!=rewards:
                raise ValueError("actual reward must retain original Appendix D coefficients")
            zero+=1
        else:
            centered=[x-rewards[0] for x in rewards]
            mean=sum(centered)/4
            centered=[x-mean for x in centered]
            std=(sum(x*x for x in centered)/4)**.5
            advantages=[x/(std+1e-6) for x in centered]
            if (step["trajectory_rewards"]!=rewards or len(step["trajectory_advantages"])!=4
                or any(not math.isclose(x,y,abs_tol=1e-5) for x,y in zip(step["trajectory_advantages"],advantages,strict=True))
                or step["optimizer_update_executed"] is not True or step["zero_advantage_group"] is not False
                or not math.isfinite(step["gradient_l2_norm"]) or step["gradient_l2_norm"]<=0):
                raise ValueError("real reward-varying normalized trajectory gradient required")
            updates+=1
        ledgers.append({"step":i+1,"derived_rewards":rewards,"mathematically_equal":equal,
            "optimizer_update_executed":step["optimizer_update_executed"]})
    if not updates or r["parameters_changed"] is not True:raise ValueError("complete SOAR needs real nonzero policy updates")
    return {"actual_optimizer_updates":updates,"equal_reward_groups_skipped":zero,
        "all_four_groups_audited":True,"reward_derivation_audits":ledgers}


def curate(directories,contract,audit,config,*,expected_seed=42):
    if expected_seed not in (42,43,44):raise ValueError("fixed default seeds required")
    metric_path=METRIC.replace("seed42",f"seed{expected_seed}")
    receipt_path=RECEIPT.replace("seed42",f"seed{expected_seed}")
    canonical=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    if (contract["source_commit"]!=COMMIT or audit["source_commit"]!=COMMIT
        or len(contract["source_file_sha256"])!=54
        or contract["source_file_sha256"].get("src/auto_research/post_training/oct13_common.py")!="d19401266a420afdc64867f145f8384fd649dc1991e4b74ea1f7ee8b8d91bde5"
        or audit["source_file_sha256"]!=contract["source_file_sha256"] or audit["source_hashes_verified"] is not True
        or audit["execution_config_sha256"]!=canonical or audit["cuda_initialized"] is not False
        or audit["model_instantiated"] is not False):raise ValueError("actual frozen source and CPU audit required")
    rows={};checks={};hashes={}
    for d in directories:
        path=d/"evidence/result.json"
        r=json.loads(path.read_text());l=json.loads((d/"launch.json").read_text());e=json.loads((d/"exit.json").read_text())
        v=r["variant"]
        c={**config["shared"],**config["methods"]["soar"],"variant":v}
        if (v not in VARIANTS or v in rows or r["seed"]!=expected_seed or l["seed"]!=expected_seed or r["method"]!="soar"
            or l["source_commit"]!=COMMIT or l["source_file_sha256"]!=contract["source_file_sha256"]
            or l["execution_config_sha256"]!=canonical or l["effective_config"]!=c
            or l["job"]["timeout_seconds"]!=1800 or e["exit_code"]!=0 or not 0<e["elapsed_seconds"]<=1800
            or l["gpu_slot_grant"]!="A100-post-training-explicit-slot" or r["device"]!="cuda"
            or r["diagnostic_only"] is not True or r["promotion_eligible"] is not False):
            raise ValueError("two actual fixed default-seed complete CUDA arms required")
        if (c["steps"]!=4 or c["group"]!=4 or c["max_turns"]!=3 or c["max_tokens"]!=256
            or c["train_examples"]!=8 or c["validation_examples"]!=4 or c["context_limit"]!=4096
            or c["verifier"]!="normalized-em" or r["protocol"]["max_tokens"]!=256
            or r["protocol"]["train_examples"]!=8 or r["protocol"]["validation_examples"]!=4
            or r["protocol"]["gold_in_student_generation"] is not False or r["protocol"]["test_opened"] is not False
            or any(r[k]["examples"]!=4 for k in ("baseline","method_metrics"))):
            raise ValueError("original method budget and evaluated-policy gold isolation required")
        holdout=audit["method_specific_holdouts"]["soar"]
        if (holdout["status"]!="verified" or holdout["tool_groups_disjoint"] is not True
            or r["dataset"]!=holdout["holdout"] or r["dataset"]["test_read"] is not False):
            raise ValueError("actual independent tool-disjoint public holdout required")
        resource=audit["resources"]["student"]
        checkpoint=r["checkpoint"]
        if (resource["verified"] is not True or resource["public_id"]!=c["student_id"]
            or resource["revision"]!=c["student_revision"] or checkpoint["public_id"]!=resource["public_id"]
            or checkpoint["revision"]!=resource["revision"]
            or checkpoint["verified_mirror"]["file_sha256"]!=resource["file_sha256"]
            or checkpoint["public_id"]!="Qwen/Qwen2.5-7B-Instruct"
            or checkpoint["revision"]!="bb46c15ee4bb56c5b63245ef50fd7637234d6f75"):
            raise ValueError("actual already-cached fixed public 7B policy bytes required")
        corpus=audit["soar_corpus"]
        if (corpus["status"]!="verified" or corpus["generation_inputs_do_not_include_qa_answers"] is not True
            or r["corpus"]!={"public_id":corpus["public_id"],"revision":corpus["revision"],"file_sha256":corpus["file_sha256"]}):
            raise ValueError("sealed independent catalog must not be gold-generated")
        for flag,value in {"--method":"soar","--seed":str(expected_seed),"--variant":v}.items():
            if flag not in l["command"] or l["command"][l["command"].index(flag)+1]!=value:raise ValueError("actual argv mismatch")
        finite(r);finite(e)
        check=training_check(r)
        if (sum(r["cost"]["generated_tokens"].values())>36864
            or r["cost"]["scored_response_tokens"]["reference"]>12288):raise ValueError("original generated/scored safety bounds exceeded")
        check.update(invocation_elapsed_seconds=e["elapsed_seconds"],configured_wall_cap_seconds=1800,measured_cost=r["cost"])
        rows[v]=r;checks[v]=check;hashes[v]=hashlib.sha256(path.read_bytes()).hexdigest()
    if set(rows)!=VARIANTS:raise ValueError("both complete original reward arms required")
    first=rows["source-consistent"]
    if any(rows[v][k]!=first[k] for v in VARIANTS for k in ("dataset","checkpoint","corpus","baseline")):
        raise ValueError("same-device/source/resource/seed initial baseline pairing required")
    if rows["source-consistent"]["training"][0]["components"]!=rows["without-source-reward"]["training"][0]["components"]:
        raise ValueError("first unchanged-policy trajectories must expose the source-reward contrast")
    metrics={v+"."+phase+"."+name:{"mean":r[key][name],"std":0.,"n":1}
        for v,r in rows.items() for phase,key in (("initial","baseline"),("validation","method_metrics"))
        for name in ("accuracy","source_consistency","format_compliance","mean_searches")}
    limitations=[("One seed42 and two reward arms are not two seeds; default43/44 remain pending." if expected_seed==42 else
        "One actual seed and two reward arms are not two seeds; the other default seeds remain pending."),
        "Independent public tool-catalog attribute QA is not the original RATED or seven-QA benchmark; tiny4validation is L1 only.",
        "Real LoRA policy, isolated same-policy internal recall, lexical retrieval and frozen-reference trajectory GRPO are executed.",
        "Raw zero groups and all actual generation/scoring costs are retained; matched configured budget is not identical realized compute.",
        "The measured source-match difference is not a stable capability or production improvement claim."]
    artifact={"schema_version":2,"adapter_key":"soar","manifest_ref":"reproduction:soar","method":"soar",
        "measured_locally":True,"diagnostic_only":True,"promotion_eligible":False,"seeds":[expected_seed],
        "whole_method_gpu_validation_passed":True,"default_three_seed_plan_completed":False,"actual_cuda_run_count":2,
        "seed_results":[{"seed":expected_seed,"device":"cuda","diagnostic_only":True,"variants":rows}],
        "aggregate_metrics":metrics,"execution_checks":checks,"dataset":first["dataset"],"checkpoint":first["checkpoint"],
        "evaluation_protocol":{"tier":"l1_mechanism","seeds":[expected_seed],"formal_comparison":False,"promotion_eligible":False,
            "claim_policy":"single/few-seed smoke result; do not claim a stable improvement",
            "test_used_for_selection":False,"pending_seeds":[s for s in (42,43,44) if s!=expected_seed],"variants_are_independent_seeds":False},
        "provenance":{"code_commit":COMMIT,"artifact_path":metric_path,"executed_source_sha256":contract["source_file_sha256"],
            "execution_config_sha256":canonical,"raw_results_sha256":hashes,
            "dataset_fingerprint":hashlib.sha256(json.dumps(first["dataset"],sort_keys=True).encode()).hexdigest()},"limitations":limitations}
    commands=[["python","scripts/run_oct13_post_training.py","--method","soar","--config","data/oct14_execution-soar7b-full-v1.json",
        "--seed",str(expected_seed),"--output","runs/soar-"+v+"-s"+str(expected_seed),"--variant",v] for v in sorted(VARIANTS)]
    receipt={"schema_version":1,"adapter_key":"soar","validated_at":"2026-10-14","seeds":[expected_seed],
        "accelerator":{"vendor":"NVIDIA","model":"NVIDIA-A100-SXM4-80GB"},"command":commands[0],
        "all_sanitized_commands":commands,"command_path_relocations_only":True,"dataset":first["dataset"],
        "checkpoint":{"policy":first["checkpoint"],"frozen_reference":first["checkpoint"]},"result":"passed",
        "metrics":metrics,"execution_checks":checks,"executed_source_sha256":contract["source_file_sha256"],"limitations":limitations,
        "provenance":{"commit":COMMIT,"artifact_path":receipt_path,"metrics_artifact":metric_path,
            "execution_config_sha256":canonical,"raw_results_sha256":hashes,"checkpoint_committed":False}}
    errors=validate_gpu_receipt(receipt)
    if errors:raise ValueError(errors)
    return artifact,receipt



def curate_three(directories,contract,audit,config):
    if len(directories)!=6:raise ValueError("all three seeds times two real arms required")
    indexed={}
    for d in directories:
        l=json.loads((d/"launch.json").read_text())
        identity=(l["seed"],l["effective_config"]["variant"])
        if identity in indexed:raise ValueError("duplicate arm is not an independent seed")
        indexed[identity]=d
    if set(indexed)!={(s,v) for s in (42,43,44) for v in VARIANTS}:raise ValueError("exact default three-seed two-arm cohort required")
    pairs={s:curate([indexed[s,v] for v in sorted(VARIANTS)],contract,audit,config,expected_seed=s) for s in (42,43,44)}
    first,receipt=pairs[42]
    if any(a[k]!=first[k] for a,_ in pairs.values() for k in ("dataset","checkpoint")):
        raise ValueError("all seeds must use identical fixed public checkpoint/dataset")
    metrics={name:{"mean":statistics.mean(pairs[s][0]["aggregate_metrics"][name]["mean"] for s in (42,43,44)),
        "std":statistics.stdev(pairs[s][0]["aggregate_metrics"][name]["mean"] for s in (42,43,44)),"n":3}
        for name in first["aggregate_metrics"]}
    limitations=["Three actual seeds42/43/44 and two arms complete this reduced-scale mechanism plan, not the multi-method batch.",
        "Three seeds remain L1 public tool-catalog diagnostics, not original RATED/seven-QA benchmarks or stable capability evidence."]+first["limitations"][1:]
    metric_path=METRIC.replace("seed42","seeds42-44")
    receipt_path=RECEIPT.replace("seed42","seeds42-44")
    hashes={str(s)+"."+v:h for s in (42,43,44) for v,h in pairs[s][0]["provenance"]["raw_results_sha256"].items()}
    checks={str(s):pairs[s][0]["execution_checks"] for s in (42,43,44)}
    artifact={**first,"seeds":[42,43,44],"actual_cuda_run_count":6,"default_three_seed_plan_completed":True,
        "seed_results":[pairs[s][0]["seed_results"][0] for s in (42,43,44)],"aggregate_metrics":metrics,
        "execution_checks":{"per_seed":checks},"evaluation_protocol":{**first["evaluation_protocol"],"seeds":[42,43,44],"pending_seeds":[]},
        "provenance":{**first["provenance"],"artifact_path":metric_path,"raw_results_sha256":hashes},"limitations":limitations}
    receipt={**receipt,"seeds":[42,43,44],"metrics":metrics,"execution_checks":artifact["execution_checks"],
        "all_sanitized_commands":[c for s in (42,43,44) for c in pairs[s][1]["all_sanitized_commands"]],
        "provenance":{**receipt["provenance"],"artifact_path":receipt_path,"metrics_artifact":metric_path,"raw_results_sha256":hashes},
        "limitations":limitations}
    errors=validate_gpu_receipt(receipt)
    if errors:raise ValueError(errors)
    return artifact,receipt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-directory",type=Path,action="append",required=True)
    for n in ("contract","audit","config","output"):p.add_argument("--"+n,type=Path,required=True)
    a=p.parse_args()
    operation=curate_three if len(a.run_directory)==6 else curate
    artifact,receipt=operation(a.run_directory,*[json.loads(getattr(a,n).read_text()) for n in ("contract","audit","config")])
    a.output.mkdir(parents=True,exist_ok=False)
    for name,data in (("result.json",artifact),("receipt.json",receipt)):
        with (a.output/name).open("x") as s:s.write(json.dumps(data,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":main()
