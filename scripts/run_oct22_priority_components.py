"""Run CPU-only DeepSEA scorer and LogAct durability contracts, never an LLM."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from oct18_frozen_sources import capture_sources  # noqa: E402

MODULES = {"deepsea": "src/auto_research/foundation_models/deepsea.py",
           "logact": "src/auto_research/agent_research/logact.py"}
RUNNER = "scripts/run_oct22_priority_components.py"
SEEDS = [42, 43, 44]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit")
    parser.add_argument("--mgsm-archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("a new output path is required")
    commit = args.source_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    paths = [RUNNER, *MODULES.values()]
    # Reject an asserted but nonexistent or stale commit BEFORE execution.
    capture_sources(ROOT, commit, paths)
    from auto_research.foundation_models.deepsea import diagnostic as deepsea, inspect_fixed_mgsm_archive
    from auto_research.agent_research.logact import diagnostic as logact
    components = {key: {"per_seed": [function(seed) for seed in SEEDS]}
                  for key, function in (("deepsea", deepsea), ("logact", logact))}
    for component in components.values():
        if any(not row["checks"] or not all(v is True for v in row["checks"].values())
               for row in component["per_seed"]):
            raise AssertionError("component contracts failed")
    inspection = inspect_fixed_mgsm_archive(args.mgsm_archive) if args.mgsm_archive else None
    payload = {"schema_version": 2, "device": "cpu", "accelerator": "CPU", "seeds": SEEDS,
        "code_commit": commit,
        "source_sha256": {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in paths},
        "components": components, "official_data_schema_inspection": inspection,
        "diagnostic_only": True, "formal_comparison": False, "promotion_eligible": False,
        "evolve_integrated": False, "pretrained_model_calls": 0,
        "full_experiment_status": "not_reproduced_high_cost"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"components": list(components), "device": "cpu", "model_calls": 0,
                      "official_schema_checked": inspection is not None}))


if __name__ == "__main__":
    main()
