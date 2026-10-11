#!/usr/bin/env python3
"""Archive a completed instance-disjoint CPU replay without upgrading claims."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    a = p.parse_args()
    report = json.loads(a.input.read_text())
    protocol = report["evaluation_protocol"]
    if protocol["tier"] != "l2_public_dataset" or protocol["formal_comparison"] or report["checkpoint"]["device"] != "cpu":
        raise ValueError("bounded CPU public replay required")
    partitions = {k: set(v) for k, v in report["partition_ids"].items()}
    if any(partitions[a] & partitions[b] for a, b in (("calibration", "reference_pool"),
                                                     ("calibration", "evaluation"), ("reference_pool", "evaluation"))):
        raise ValueError("instance leakage across partitions")
    if not set(report["reference_ids"]) <= partitions["reference_pool"]:
        raise ValueError("references outside dedicated pool")
    if {r["instance_id"] for r in report["rows"]} != partitions["evaluation"]:
        raise ValueError("evaluation rows differ from frozen partition")
    commit = report["provenance"]["original_code_commit"]
    for source, digest in report["provenance"]["executed_source_sha256"].items():
        if hashlib.sha256(subprocess.check_output(["git", "show", f"{commit}:{source}"], cwd=ROOT)).hexdigest() != digest:
            raise ValueError("source evidence mismatch")
    target = ROOT / "docs/agent-research/2610.12375-ontrack/metrics/public-replay-cpu-seed42.json"
    report["provenance"]["artifact_path"] = str(target.relative_to(ROOT))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
