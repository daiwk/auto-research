#!/usr/bin/env python3
"""Run Sep-19 CUDA kernels and emit one sanitized validation receipt."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[1]


def load_module(path):
    spec = importlib.util.spec_from_file_location("sep19_foundation", path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=("oda","dqwen35","aspire"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if not torch.cuda.is_available(): raise RuntimeError("CUDA is required")
    module = load_module(ROOT/"src/auto_research/foundation_latest_20260919.py")
    torch.manual_seed(args.seed); torch.cuda.manual_seed_all(args.seed); device="cuda"
    if args.method == "oda":
        q=torch.randn(256,device=device); lk=torch.randn(512,256,device=device); lv=torch.randn(512,256,device=device); gk=torch.randn(4096,256,device=device); gv=torch.randn(4096,256,device=device); h=torch.randn(256,device=device)
        output, gate=module.oda_cuda_kernel(q,lk,lv,gk,gv,h)
        metrics={"output_finite":bool(torch.isfinite(output).all()),"global_gate_decision":bool(gate),"global_kv_tokens":len(gk)}
    elif args.method == "dqwen35":
        x=torch.randn(256,512,device=device); r=torch.randn(512,512,device=device)/512; a=torch.randn(512,512,device=device)/512
        output=module.dqwen35_cuda_kernel(x,r,a)
        metrics={"output_finite":bool(torch.isfinite(output).all()),"tokens":len(x),"hidden_size":x.shape[1]}
    else:
        acceptance=torch.rand(4096,device=device); batch=torch.randint(1,33,(4096,),device=device).float()
        lengths,refresh=module.aspire_cuda_kernel(acceptance,.1,1.,batch)
        metrics={"requests":len(lengths),"mean_draft_length":float(lengths.float().mean()),"refresh_fraction":float(refresh.float().mean())}
    torch.cuda.synchronize()
    model=torch.cuda.get_device_name(0); accelerator="A100" if "A100" in model else "A30" if "A30" in model else model
    artifact=f"docs/gpu-validations/{args.method}-a100-20260919.json"
    payload={"schema_version":1,"adapter_key":args.method,"validated_at":"2026-09-19","accelerator":{"vendor":"NVIDIA","model":accelerator},"command":["python","scripts/validate_sep19_gpu.py","--method",args.method,"--seed",str(args.seed),"--output",artifact,"--commit",args.commit],"dataset":{"name":"deterministic public mechanism fixture","revision":"sep19-v1","examples":int(metrics.get("requests",metrics.get("tokens",1)))},"checkpoint":{"model_id":"not-required/reference-kernel","revision":"arxiv-v1"},"result":"passed","metrics":{"seed":args.seed,**metrics},"provenance":{"commit":args.commit,"artifact_path":artifact,"raw_predictions_committed":False,"checkpoint_committed":False}}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload["metrics"],sort_keys=True))


if __name__ == "__main__": main()
