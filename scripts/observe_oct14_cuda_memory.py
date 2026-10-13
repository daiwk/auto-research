#!/usr/bin/env python3
"""Observe a frozen 51b curriculum invocation without modifying its algorithm."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy
import sys
import time

import torch

CORE_COMMIT="51b4718a76da286b4111c6fc7d8e003d436def72"
ALLOWED_VARIANTS={"unfiltered","static","fixed-medium","staged","too-hard"}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_core(root,contract,audit,arguments):
    if (contract["source_commit"]!=CORE_COMMIT or audit["source_commit"]!=CORE_COMMIT
            or contract["source_file_sha256"]!=audit["source_file_sha256"]
            or not audit["source_hashes_verified"] or audit["cuda_initialized"] is not False
            or audit["model_instantiated"] is not False):
        raise ValueError("exact frozen 51b source/CPU audit required")
    for relative,expected in contract["source_file_sha256"].items():
        if digest(root/relative)!=expected:
            raise ValueError("frozen core source mismatch")
    if len(arguments)!=10 or set(arguments[::2])!={"--method","--config","--seed","--output","--variant"}:
        raise ValueError("forward only the original five argument pairs; no added training overrides")
    flags=dict(zip(arguments[::2],arguments[1::2],strict=True))
    if (flags["--method"]!="grpo-difficulty-curriculum" or flags["--seed"] not in {"43","44"}
            or flags["--variant"] not in ALLOWED_VARIANTS):
        raise ValueError("only the ten approved curriculum arm/seed jobs may be observed")
    config=json.loads(Path(flags["--config"]).read_text())
    canonical=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()
    c={**config["shared"],**config["methods"]["grpo-difficulty-curriculum"]}
    if (canonical!=audit["execution_config_sha256"] or any(c.get(k)!=v for k,v in {
            "train_examples":8,"steps":4,"group":8,"max_tokens":512,"validation_examples":4,
            "context_limit":4096,"learning_rate":1e-5}.items())):
        raise ValueError("original configured training budget and exact CPU config binding required")
    return flags,canonical


def observe(target,arguments,output,metadata,*,cuda=None,entry_runner=None):
    """Read actual per-process allocator maxima in finally, including failed exits."""
    cuda=torch.cuda if cuda is None else cuda
    entry_runner=runpy.run_path if entry_runner is None else entry_runner
    if output.exists():
        raise FileExistsError("memory observation is immutable")
    previous=list(sys.argv)
    code=1
    started=time.monotonic()
    cuda.reset_peak_memory_stats()
    try:
        sys.argv=[str(target),*arguments]
        entry_runner(str(target),run_name="__main__")
        code=0
    except SystemExit as exc:
        code=exc.code if isinstance(exc.code,int) else 0 if exc.code is None else 1
    finally:
        sys.argv=previous
        record={**metadata,"artifact_kind":"observational_cuda_memory_not_gpu_receipt",
            "not_gpu_receipt":True,"core_exit_code":code,"actual_elapsed_seconds":time.monotonic()-started,
            "no_monkeypatch":True,"training_arguments_forwarded_unchanged":True,
            "measurement_scope":"whole frozen-core invocation after reset; per-process Torch allocator, not device-global NVML peak",
            "peak_memory_available":False}
        try:
            cuda.synchronize()
            record.update(peak_memory_available=True,
                actual_max_memory_allocated_bytes=int(cuda.max_memory_allocated()),
                actual_max_memory_reserved_bytes=int(cuda.max_memory_reserved()),
                accelerator={"vendor":"NVIDIA","model":cuda.get_device_name()})
        except Exception as exc:
            record["memory_measurement_error_type"]=type(exc).__name__
        with output.open("x") as stream:
            stream.write(json.dumps(record,indent=2,allow_nan=False)+"\n")
    return code


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("core-root","core-contract","core-audit","observer-root","observer-contract","memory-output"):
        parser.add_argument("--"+name,type=Path,required=True)
    parser.add_argument("--execute",action="store_true")
    parser.add_argument("--gpu-grant")
    parser.add_argument("core_arguments",nargs=argparse.REMAINDER)
    args=parser.parse_args()
    arguments=args.core_arguments[1:] if args.core_arguments[:1]==["--"] else args.core_arguments
    if not args.execute:
        print(json.dumps({"planned_only":True,"observational_only":True,"core_commit":CORE_COMMIT,
            "allowed_seeds":[43,44],"training_definition_changes":False,"not_gpu_receipt":True}))
        return 0
    if args.gpu_grant!="A30-post-training-explicit-slot":
        parser.error("fresh approved A30 curriculum slot required")
    observer=json.loads(args.observer_contract.read_text())
    relative="scripts/observe_oct14_cuda_memory.py"
    actual=Path(__file__).resolve()
    if actual!=(args.observer_root/relative).resolve() or observer["source_file_sha256"].get(relative)!=digest(actual):
        raise ValueError("observer entrypoint must be independently frozen and hash-bound")
    contract=json.loads(args.core_contract.read_text())
    audit=json.loads(args.core_audit.read_text())
    flags,canonical=validate_core(args.core_root,contract,audit,arguments)
    # Import routing only: never replace modules, training functions or symbols.
    sys.path.insert(0,str(args.core_root/"src"))
    package=importlib.util.find_spec("auto_research")
    if package is None or Path(package.origin).resolve()!=(args.core_root/"src/auto_research/__init__.py").resolve():
        raise ValueError("original core imports must resolve inside the frozen 51b root")
    if "A30" not in torch.cuda.get_device_name():
        raise ValueError("observer grant is limited to the actual NVIDIA A30")
    target=args.core_root/"scripts/run_oct13_post_training.py"
    metadata={"core_commit":CORE_COMMIT,"core_runner_sha256":contract["source_file_sha256"]["scripts/run_oct13_post_training.py"],
        "observer_commit":observer["source_commit"],"observer_source_sha256":digest(__file__),
        "core_import_binding":"prepend frozen core root/src; refuse mismatched preloaded package",
        "seed":int(flags["--seed"]),"variant":flags["--variant"],"execution_config_canonical_sha256":canonical}
    return observe(target,arguments,args.memory_output,metadata)


if __name__=="__main__":
    raise SystemExit(main())
