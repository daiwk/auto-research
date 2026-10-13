#!/usr/bin/env python3
"""Run actual GPPO/TAPO/GRPO-control training with complete public provenance."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from auto_research.post_training.proximal_checkpoint import ProximalExecutionFailure, run_proximal_checkpoint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method", choices=("gppo-framework", "tapo-trajectory", "grpo-control"), required=True)
    for name in ("student-path", "train-path", "validation-path", "split-manifest"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    for name in ("student-id", "student-revision", "dataset-revision"):
        parser.add_argument(f"--{name}", required=True)
    for name, default in (("seed", 42), ("steps", 3), ("group", 4), ("max-tokens", 512),
                          ("inner-updates", 2), ("validation-examples", 8), ("max-task-attempts", 16),
                          ("context-limit", 4096)):
        parser.add_argument(f"--{name}", type=int, default=default)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--geometry", choices=("tv", "chi2", "hellinger", "kl", "two_sided_log"), default="chi2")
    parser.add_argument("--topology", choices=("mc", "atomic", "binary"), default="atomic")
    parser.add_argument("--delta", type=float, default=.04)
    parser.add_argument("--learning-rate", type=float, default=1e-5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output
    if output.exists():
        raise FileExistsError("previous evidence is immutable; use a fresh directory")
    kwargs = vars(args)
    kwargs.pop("output")
    try:
        result = run_proximal_checkpoint(**kwargs)
    except ProximalExecutionFailure as exc:
        output.mkdir(parents=True)
        (output / "failure.json").write_text(json.dumps(exc.evidence, ensure_ascii=False, indent=2) + "\n")
        print(str(exc), file=sys.stderr)
        return 1
    output.mkdir(parents=True)
    (output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"method": result["method"], "baseline": result["baseline"],
                      "after": result["method_metrics"], "sampling": result["sampling"],
                      "parameters_changed": result["parameters_changed"], "diagnostic_only": True}))


if __name__ == "__main__":
    raise SystemExit(main())
