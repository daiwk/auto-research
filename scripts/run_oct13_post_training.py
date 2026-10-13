#!/usr/bin/env python3
"""Run one of the nine Oct13 papers on verified public checkpoint/holdout inputs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from auto_research.post_training.oct13_common import ExecutionFailure,execute,render_result
from auto_research.post_training.proximal_checkpoint import ProximalExecutionFailure

METHODS=("state-opd","magicbeanstalk","gppo-framework","tapo-trajectory","synthself","upturn",
         "soar","grpo-difficulty-curriculum","progressive-contraction")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method",choices=METHODS,required=True)
    parser.add_argument("--config",type=Path)
    for name in ("student-path","teacher-path","train-path","validation-path","split-manifest","corpus-path"):
        parser.add_argument("--"+name,type=Path)
    for name in ("student-id","student-revision","teacher-id","teacher-revision","dataset-revision",
                 "corpus-id","corpus-revision","variant","control","verifier","geometry","topology"):
        parser.add_argument("--"+name)
    for name in ("steps","group","max-tokens","train-examples","validation-examples","context-limit","epochs",
                 "teacher-attempts","branches","prefix-states","active-size","cuts","suffixes","gate-epochs",
                 "max-cuts","evaluation-group","depth","decomposition-retries","synthesis-retries","max-turns",
                 "multiplicity","concentration","inner-updates","max-task-attempts","hard-root-limit"):
        parser.add_argument("--"+name,type=int)
    for name in ("learning-rate","pool-ratio","kl-beta","delta"):
        parser.add_argument("--"+name,type=float)
    parser.add_argument("--device",choices=("cpu","cuda"))
    parser.add_argument("--seed",type=int,default=42)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        raise FileExistsError("previous evidence is immutable; choose a new output directory")
    config={}
    if args.config:
        raw=json.loads(args.config.read_text())
        config={**raw.get("shared",raw),**raw.get("methods",{}).get(args.method,{})}
    config.update({k:v for k,v in vars(args).items() if v is not None and k not in {"method","config","seed","output"}})
    required=("student_path","student_id","student_revision","train_path","validation_path","split_manifest","dataset_revision")
    missing=[k for k in required if not config.get(k)]
    if missing:
        parser.error("verified execution resources missing: "+", ".join(missing))
    try:
        result=execute(args.method,config,seed=args.seed)
    except (ExecutionFailure,ProximalExecutionFailure) as exc:
        args.output.mkdir(parents=True)
        (args.output/"failure.json").write_text(json.dumps(exc.evidence,ensure_ascii=False,indent=2)+"\n")
        print(str(exc),file=sys.stderr)
        return 1
    except Exception as exc:
        # Preserve unexpected runtime failures without putting machine paths,
        # prompts, labels or unverified provenance into a sanitizable receipt.
        args.output.mkdir(parents=True)
        failure={"status":"failed","diagnostic_only":True,"method":args.method,"seed":args.seed,
                 "error_type":type(exc).__name__,"error":"execution terminated; inspect the separate local runtime log",
                 "requested_sources":{k:str(v) for k,v in config.items() if k.endswith("_id") or k.endswith("_revision")},
                 "resource_verification_completed":None}
        (args.output/"failure.json").write_text(json.dumps(failure,ensure_ascii=False,indent=2)+"\n")
        print(str(exc),file=sys.stderr)
        return 1
    args.output.mkdir(parents=True)
    (args.output/"result.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    (args.output/"report.md").write_text(render_result(result))
    print(json.dumps({"method":args.method,"parameters_changed":result.get("parameters_changed"),
                      "baseline":result["baseline"],"after":result["method_metrics"],
                      "diagnostic_only":True},ensure_ascii=False))
    if str(result.get("execution_status","")).startswith("failed"):
        return 1
    if args.method=="upturn" and not result.get("position_informative_groups"):
        return 1  # an entropy-only position update is not rescue-learning validation
    return 0 if result.get("parameters_changed") or config.get("variant")=="too-hard" else 1


if __name__=="__main__":
    raise SystemExit(main())
