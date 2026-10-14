"""Actual42/43 passed and44 failed: completed execution, not accepted three-seed mechanism."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from curate_oct14_post_complete import curate,finite_tree  # noqa: E402

KEY="upturn"
COMMIT="51b4718a76da286b4111c6fc7d8e003d436def72"
FAILED_PATH="docs/reproductions/2610.13672-upturn/metrics/public-a100-complete-failed-seed44.json"
COHORT_PATH="docs/reproductions/2610.13672-upturn/metrics/public-a100-complete-three-seed-execution-cohort.json"


def validate_failed(r,c):
    finite_tree(r)
    if (r["method"]!=KEY or r["seed"]!=44 or r["execution_status"]!="failed-no-rescue-signal"
            or r["position_informative_groups"]!=0 or not r["encoder_frozen"] or not r["reasoner_frozen"]
            or r["protocol"]["test_opened"] is not False or r["protocol"]["gold_in_student_generation"] is not False
            or r["dataset"]["test_read"] is not False or r["device"]!="cuda"
            or r.get("diagnostic_only") is not True or r.get("promotion_eligible") is not False
            or any(r["protocol"].get(k)!=c[k] for k in ("train_examples","validation_examples","max_tokens"))
            or len(r["gate"]["training_bce"])!=c["gate_epochs"] or len(r["training"])!=c["steps"]
            or len(r["training_rollout_audits"])!=c["train_examples"]*c["group"]
            or any(m["examples"]!=c["validation_examples"] for m in (r["baseline"],r["method_metrics"]))):
        raise ValueError("complete actual44 frozen-head failed-rescue execution required")
    for step in r["training"]:
        if (step["nonzero_rescue_advantage"] is not False or any(step["rescue_rewards"])
                or any(step["advantages"]) or not 1<=len(step["cuts"])<=c["cuts"]
                or len(step["cuts"])!=len(step["advantages"]) or len(step["cuts"])!=len(step["rescue_rewards"])):
            raise ValueError("the negative record must retain actual zero rescue rewards and advantages")
        gradient=step.get("gradient_l2_norm",0)
        if step.get("optimizer_update_executed") and (not isinstance(gradient,(float,int))
                or not math.isfinite(gradient) or gradient<=0):
            raise ValueError("reported entropy-only optimizer call still needs a real finite positive gradient")
    return {"mechanism_passed":False,"execution_complete":True,"execution_status":r["execution_status"],
        "gate_epochs":len(r["gate"]["training_bce"]),"nonzero_rescue_groups":0,
        "actual_position_optimizer_calls":sum(bool(x["optimizer_update_executed"]) for x in r["training"]),
        "entropy_only_position_updates":sum(bool(x["optimizer_update_executed"]) for x in r["training"]),
        "assessment_semantics":"single shared assessment AFTER head training, frozen reasoner control vs intervention",
        "parameters_changed_is_not_rescue_validation":True,"measured_cost":r["cost"]}


def make(directories,contract,audit,config):
    indexed={json.loads((d/"launch.json").read_text())["seed"]:d for d in directories}
    if len(directories)!=3 or set(indexed)!={42,43,44}:
        raise ValueError("all three distinct actual seed execution directories required")
    pairs={s:curate(indexed[s],contract,audit,config,accelerator="NVIDIA A100-SXM4-80GB",
                    validated_at="2026-10-14",expected_seed=s) for s in (42,43)}
    d=indexed[44]
    r=json.loads((d/"evidence/result.json").read_text())
    l=json.loads((d/"launch.json").read_text())
    e=json.loads((d/"exit.json").read_text())
    c={**config["shared"],**config["methods"][KEY],**l["job"]["overrides"]}
    canonical=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    if (contract["source_commit"]!=COMMIT or audit["source_commit"]!=COMMIT or l["source_commit"]!=COMMIT
            or l["source_file_sha256"]!=contract["source_file_sha256"]
            or audit["source_file_sha256"]!=contract["source_file_sha256"]
            or not audit["source_hashes_verified"] or audit["cuda_initialized"] is not False
            or audit["model_instantiated"] is not False or l["execution_config_sha256"]!=canonical
            or audit["execution_config_sha256"]!=canonical or c!=l["effective_config"]
            or l["seed"]!=44 or l["job"]["timeout_seconds"]!=900 or e["exit_code"]!=1
            or not 0<e["elapsed_seconds"]<=900 or r["dataset"]!=audit["public_train_only_holdout"]):
        raise ValueError("exact immutable source/config/resource and actual failed44 exit required")
    finite_tree(e)
    for flag,value in {"--method":KEY,"--seed":"44"}.items():
        if flag not in l["command"] or l["command"][l["command"].index(flag)+1]!=value:
            raise ValueError("actual failed44 argv mismatch")
    for role,value in (("teacher",r["checkpoint"]),("student",r["encoder"])):
        resource=audit["resources"][role]
        if (resource.get("verified") is not True or value["public_id"]!=resource["public_id"] or value["revision"]!=resource["revision"]
                or value["verified_mirror"]["file_sha256"]!=resource["file_sha256"]):
            raise ValueError("actual frozen checkpoint must match preverified public resource")
    checks=validate_failed(r,c)
    checks.update(invocation_elapsed_seconds=e["elapsed_seconds"],configured_wall_cap_seconds=900,return_code=1)
    hashes={str(s):hashlib.sha256((indexed[s]/"evidence/result.json").read_bytes()).hexdigest() for s in (42,43,44)}
    fingerprint=hashlib.sha256(json.dumps(r["dataset"],sort_keys=True).encode()).hexdigest()
    common={"schema_version":2,"adapter_key":KEY,"manifest_ref":"reproduction:"+KEY,"method":KEY,
        "measured_locally":True,"diagnostic_only":True,"promotion_eligible":False,"not_gpu_receipt":True,
        "whole_method_gpu_validation_passed":False,"execution_complete":True,"all_seed_mechanism_passed":False,
        "dataset":r["dataset"],"checkpoint":r["checkpoint"],
        "evaluation_protocol":{"tier":"l1_mechanism","formal_comparison":False,"promotion_eligible":False,
            "test_used_for_selection":False,"assessment_is_training_before_after":False,"matched_actual_compute":False,
            "claim_policy":"execution-complete cohort including failed44, not accepted three-seed mechanism or stable gain"},
        "provenance":{"code_commit":COMMIT,"executed_source_sha256":contract["source_file_sha256"],
            "execution_config_sha256":canonical,"dataset_fingerprint":fingerprint},
        "limitations":["44 has only entropy-driven parameter updates and no rescue signal; it cannot pass mechanism validation.",
            "42/43 passed individually; existing seed42 GPU receipt remains source-bound, but no three-seed passed receipt is issued.",
            "Four validation cases and matched maximum allowances are not equal realized generation pools or formal capability evidence.",
            "All negative metrics are retained; no retry, sample expansion, threshold change or forced advantage."]}
    metrics={phase+"."+name:{"mean":m[name],"std":0.,"n":1} for phase,m in
        (("frozen_reasoner_control",r["baseline"]),("trained_intervention",r["method_metrics"])) for name in ("avg_accuracy","pass_rate")}
    failed={**common,"seeds":[44],"seed_results":[{"seed":44,"diagnostic_only":True,"device":"cuda","mechanism_passed":False,"result":r}],
        "execution_checks":checks,"aggregate_metrics":metrics,
        "evaluation_protocol":{**common["evaluation_protocol"],"seeds":[44]},
        "provenance":{**common["provenance"],"artifact_path":FAILED_PATH,"raw_result_sha256":hashes["44"]}}
    raw_rows={s:pairs[s][0]["seed_results"][0]["result"] for s in (42,43)}
    raw_rows[44]=r
    metrics={}
    for phase,key in (("frozen_reasoner_control","baseline"),("trained_intervention","method_metrics")):
        for name in ("avg_accuracy","pass_rate"):
            values=[raw_rows[s][key][name] for s in (42,43,44)]
            metrics["descriptive_all_executed_seeds."+phase+"."+name]={"mean":statistics.mean(values),"std":statistics.stdev(values),"n":3}
    cohort={**common,"seeds":[42,43,44],"actual_cuda_run_count":3,"accepted_mechanism_aggregate":False,
        "accepted_mechanism_seed_count":2,"three_seed_passed_gpu_receipt_issued":False,
        "seed_execution_status":{"42":"passed","43":"passed","44":"failed-no-rescue-signal"},
        "seed_results":[{"seed":s,"diagnostic_only":True,"device":"cuda","execution_complete":True,
            "mechanism_passed":s!=44,"result":raw_rows[s]} for s in (42,43,44)],"aggregate_metrics":metrics,
        "execution_checks":{"per_seed":{**{str(s):pairs[s][0]["execution_checks"] for s in (42,43)},"44":checks}},
        "evaluation_protocol":{**common["evaluation_protocol"],"seeds":[42,43,44],
            "execution_complete":True,"all_seed_mechanism_passed":False,"accepted_mechanism_aggregate":False},
        "provenance":{**common["provenance"],"artifact_path":COHORT_PATH,"raw_results_sha256":hashes}}
    return failed,cohort


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run-directory",type=Path,action="append",required=True)
    for name in ("contract","audit","config","output"):
        p.add_argument("--"+name,type=Path,required=True)
    args=p.parse_args()
    failed,cohort=make(args.run_directory,json.loads(args.contract.read_text()),json.loads(args.audit.read_text()),json.loads(args.config.read_text()))
    args.output.mkdir(parents=True,exist_ok=False)
    for name,value in (("failed44.json",failed),("cohort.json",cohort)):
        with (args.output/name).open("x") as stream:
            stream.write(json.dumps(value,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
