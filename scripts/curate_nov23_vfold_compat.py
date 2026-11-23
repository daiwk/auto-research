"""Supplemental hook-level evidence, never a replacement VFold benchmark."""

import argparse
import hashlib
import json
from pathlib import Path

from oct18_frozen_sources import verify_sources

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs/research-audits/nov23-latest"
TARGET="docs/gpu-validations/vfold-cache-keyword-compat-a100-20261123.json"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    frozen=json.loads((AUDIT/"frozen-vfold-compat-sources.json").read_text())
    verify_sources(ROOT,frozen["commit"],frozen["source_sha256"],frozen["proof"])
    for device in ("cpu","cuda"):
        raw=json.loads((AUDIT/f"raw-vfold-compat-{device}.json").read_text())
        assert raw["code_commit"]==frozen["commit"] and raw["source_sha256"]==frozen["source_sha256"]
        assert raw["device"]==device and raw["seeds"]==[42,43,44] and raw["elapsed_seconds"]<=30
        assert raw["diagnostic_only"] is True and raw["formal_comparison"] is False
        assert raw["full_experiments_executed"] is False and raw["pretrained_model_calls"]==raw["api_calls"]==0
        assert [r["seed"] for r in raw["per_seed"]]==[42,43,44]
        assert all(all(v is True for v in r["checks"].values()) and r["metrics"]["max_attention_error"]<=1e-6 for r in raw["per_seed"])
    assert raw["accelerator"].startswith(("NVIDIA A100","NVIDIA A30"))
    value={"schema_version":1,"adapter_key":"vfold-cache-keyword-compat","validated_at":"2026-11-23",
        "accelerator":{"vendor":"NVIDIA","model":raw["accelerator"],"count":1},
        "command":["python3","scripts/run_nov23_vfold_compat.py","--device","cuda","--source-commit",frozen["commit"],"--output","raw-vfold-compat-cuda.json"],
        "dataset":{"id":"synthetic:vfold-hook-cache-keywords-v1","revision":"sha256:"+frozen["source_sha256"]["scripts/run_nov23_vfold_compat.py"],"capability_benchmark":False},
        "checkpoint":{"public_id":"none-small-tensor-regression","revision":frozen["commit"],"pretrained":False},
        "seeds":[42,43,44],"result":"passed","diagnostic_only":True,"evaluation_tier":"l1_mechanism",
        "metrics":{"max_attention_error":max(r["metrics"]["max_attention_error"] for r in raw["per_seed"]),"completed_cache_pairs":sum(r["metrics"]["completed_pairs"] for r in raw["per_seed"])},
        "scope":"Actual finish hook and value banks on CUDA tensors, both keyword lifecycles; not HF/Qwen model inference or full VFold results. Original VFold paper receipt remains unchanged.",
        "provenance":{"commit":frozen["commit"],"artifact_path":TARGET,"executed_source_sha256":frozen["source_sha256"],
                      "raw_artifact_path":"docs/research-audits/nov23-latest/raw-vfold-compat-cuda.json",
                      "raw_sha256":hashlib.sha256((AUDIT/"raw-vfold-compat-cuda.json").read_bytes()).hexdigest()}}
    target=ROOT/TARGET
    if args.check:
        assert json.loads(target.read_text())==value
    else:
        target.write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"vfold_hook_compat":"passed","full_vfold_experiment":False}))


if __name__=="__main__":
    main()
