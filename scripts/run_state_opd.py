#!/usr/bin/env python3
"""Execute State-OPD with verified public checkpoint mirrors and train-only split."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.reproductions.state_opd.checkpoint import run_state_opd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for role in ("student", "teacher"):
        parser.add_argument(f"--{role}-path", type=Path, required=True)
        parser.add_argument(f"--{role}-id", required=True)
        parser.add_argument(f"--{role}-revision", required=True)
    for name in ("train-path", "validation-path", "split-manifest"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--dataset-revision", required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=2)
    parser.add_argument("--max-turns", type=int, default=4)
    parser.add_argument("--max-tokens", type=int, default=256)
    parser.add_argument("--multiplicity", type=int, default=4)
    parser.add_argument("--concentration", type=int, default=2)
    parser.add_argument("--validation-examples", type=int, default=4)
    parser.add_argument("--context-limit", type=int, default=4096)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output
    if output.exists():
        raise FileExistsError("choose a new evidence directory")
    kwargs = vars(args)
    kwargs.pop("output")
    result = run_state_opd(**kwargs)
    output.mkdir(parents=True)
    (output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"method": "state-opd", "parameters_changed": result["parameters_changed"],
                      "baseline": result["baseline"], "after": result["method_metrics"],
                      "diagnostic_only": True}, ensure_ascii=False))
    return 0 if result["execution_status"] == "passed" and result["parameters_changed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
