"""Tiny real-device cache-hook regression; no HF/model/checkpoint download.

Exercises the actual VFold finish hook and value banks with both cache keyword
names. This is not a real Transformers forward pass or a VFold benchmark; the
real tiny-Qwen integration is covered separately by CPU tests/CI.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
from types import SimpleNamespace

from oct18_frozen_sources import capture_sources, verify_sources

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/"docs/research-audits/nov23-latest"
FILES=["scripts/run_nov23_vfold_compat.py","scripts/oct18_frozen_sources.py","src/auto_research/foundation/vfold.py"]


def write_new(path,data):
    if path.exists():
        raise ValueError("refusing to overwrite actual run/proof")
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")


def diagnostic(seed,device):
    import torch

    spec=importlib.util.spec_from_file_location("_vfold_compat_frozen",ROOT/FILES[-1])
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)

    class Cache:
        def __init__(self):
            self.banks=module.ValueBanks(2,sink=4,recent=128)

        def finish_layer(self,index):
            self.banks.finish_layer(index)

    class Attention(torch.nn.Module):
        def __init__(self,index):
            super().__init__()
            self.layer_idx=index

        def forward(self,x,*,cache=None,past_key_values=None):
            bank=cache if cache is not None else past_key_values
            key=x*(self.layer_idx+1)
            value=x.sin()*(self.layer_idx+1)
            keys,values=bank.banks.update(self.layer_idx,key,value)
            # The hook must run only after this real attention consumes values.
            return ((key@keys.transpose(-1,-2))/2).softmax(-1)@values

    generator=torch.Generator().manual_seed(seed)
    errors=[]
    completed=0
    for keyword in ("past_key_values","cache"):
        cache=Cache()
        layers=[SimpleNamespace(self_attn=Attention(i).to(device)) for i in range(2)]
        model=SimpleNamespace(model=SimpleNamespace(layers=layers))
        handles=module.attach_finish_hooks(model)
        history=[[],[]]
        try:
            for length in (8,1,1):
                x=torch.randn(1,2,length,4,generator=generator).to(device)
                for index,layer in enumerate(layers):
                    key=x*(index+1)
                    values=x.sin()*(index+1)
                    history[index].append((key,values))
                    all_keys=torch.cat([r[0] for r in history[index]],-2)
                    all_values=torch.cat([r[1] for r in history[index]],-2)
                    expected=((key@all_keys.transpose(-1,-2))/2).softmax(-1)@all_values
                    actual=layer.self_attn(x,**{keyword:cache})
                    errors.append(float((actual-expected).abs().max().item()))
                if cache.banks.pending or cache.banks.consumed:
                    raise ValueError("cache pair was not completed after attention")
                completed+=1
            if cache.banks.keys[0].shape[-2]!=10:
                raise ValueError("decode cache did not grow")
        finally:
            for handle in handles:
                handle.remove()
    if max(errors)>1e-6:
        raise ValueError("protected values changed")
    return {"seed":seed,"checks":{"both_cache_keyword_lifecycles_complete":completed==6,
                                  "actual_attention_matches_uncompressed":max(errors)<=1e-6},
            "metrics":{"max_attention_error":max(errors),"completed_pairs":completed}}


def main():
    import subprocess

    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze",action="store_true")
    parser.add_argument("--device",choices=("cpu","cuda"),default="cpu")
    parser.add_argument("--source-commit")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in FILES}
    path=AUDIT/"frozen-vfold-compat-sources.json"
    if args.freeze:
        commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
        proof=capture_sources(ROOT,commit,FILES)
        write_new(path,{"schema_version":1,"commit":commit,"source_sha256":hashes,"proof":proof})
        print(json.dumps({"commit":commit,"execution_files":len(FILES)}))
        return
    frozen=json.loads(path.read_text())
    if args.source_commit!=frozen["commit"] or hashes!=frozen["source_sha256"] or args.output is None:
        raise ValueError("source commit/output/frozen source mismatch")
    verify_sources(ROOT,frozen["commit"],hashes,frozen["proof"])
    import torch
    torch.set_num_threads(2)
    accelerator="CPU"
    if args.device=="cuda":
        if not torch.cuda.is_available() or torch.cuda.device_count()!=1:
            raise ValueError("exactly one visible CUDA device required")
        accelerator=torch.cuda.get_device_name(0)
        if not accelerator.startswith(("NVIDIA A100","NVIDIA A30")):
            raise ValueError("real A100/A30 required")
    started=time.monotonic()
    rows=[diagnostic(seed,args.device) for seed in (42,43,44)]
    if args.device=="cuda":
        torch.cuda.synchronize()
    elapsed=time.monotonic()-started
    if elapsed>30:
        raise TimeoutError("compatibility budget exceeded")
    raw={"schema_version":2,"diagnostic_only":True,"evaluation_tier":"l1_mechanism","formal_comparison":False,
         "scope":"Actual VFold finish-hook/value-bank lifecycle on real tiny tensors; no real HF/model forward or benchmark",
         "device":args.device,"accelerator":accelerator,"code_commit":frozen["commit"],"source_sha256":hashes,
         "seeds":[42,43,44],"per_seed":rows,"elapsed_seconds":elapsed,"pretrained_model_calls":0,"api_calls":0,
         "full_experiments_executed":False,"automatic_retry":False}
    write_new(args.output,raw)
    print(json.dumps({"device":args.device,"elapsed_seconds":elapsed,"seeds":3,"result":"passed"}))


if __name__=="__main__":
    main()
