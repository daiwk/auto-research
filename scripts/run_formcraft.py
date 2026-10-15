#!/usr/bin/env python3
"""Execute the independent, bounded CPU FormCraft sequence-mechanism study."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

from auto_research.agent_research.formcraft import run_sequence_study


def run(*, seeds: list[int], output: Path) -> dict:
    """Reserve fresh output and nearby snapshots; retain partial failures."""
    if not seeds or len(seeds) != len(set(seeds)):
        raise ValueError("seeds must be nonempty and distinct")
    library_dir = output.parent / f"{output.stem}.libraries"
    if output.exists() or output.is_symlink() or library_dir.exists() or library_dir.is_symlink():
        raise FileExistsError("output and adjacent library directory must be new immutable paths")
    output.parent.mkdir(parents=True, exist_ok=True)
    started, reports = time.monotonic(), []
    # Exclusive creation reserves this attempt before any synthesis. Even an
    # exception leaves a failure JSON and any already-written library snapshots.
    with output.open("x", encoding="utf-8") as handle:
        try:
            library_dir.mkdir()
            for seed in seeds:
                reports.append(run_sequence_study(seed=seed,
                               snapshot_path=library_dir / f"seed{seed}.json"))
            result = {"schema_version": 1, "status": "completed", "reports": reports,
                      "elapsed_seconds": time.monotonic() - started,
                      "library_directory": library_dir.name,
                      "diagnostic_only": True, "promotion_eligible": False, "model_calls": 0}
        except Exception as error:
            result = {"schema_version": 1, "status": "failed", "reports": reports,
                      "elapsed_seconds": time.monotonic() - started,
                      "library_directory": library_dir.name,
                      "failure": {"error_type": type(error).__name__, "reason": str(error)},
                      "diagnostic_only": True, "promotion_eligible": False, "model_calls": 0}
            json.dump(result, handle, indent=2, allow_nan=False)
            handle.write("\n")
            raise
        json.dump(result, handle, indent=2, allow_nan=False)
        handle.write("\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    seeds = [int(value) for value in args.seeds.split(",")]
    if not seeds or len(seeds) != len(set(seeds)):
        parser.error("seeds must be nonempty and distinct")
    try:
        result = run(seeds=seeds, output=args.output)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps({"elapsed_seconds": result["elapsed_seconds"],
                      "reports": [{"seed": row["seed"], **row["metrics"]}
                                  for row in result["reports"]]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
