"""Short frozen-source diagnostics, no checkpoint/data download or paid API."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402

RUNNER = "scripts/run_oct22_bulletin_components.py"
HELPER = "scripts/oct18_frozen_sources.py"
MODULES = {
    "alps": "src/auto_research/foundation_models/alps.py",
    "asteroid": "src/auto_research/agent_research/asteroid.py",
    "cord": "src/auto_research/post_training/cord.py",
    "csd": "src/auto_research/post_training/csd.py",
    "jev-multicorrect": "src/auto_research/system_one/multicorrect.py",
}
SEEDS = [42, 43, 44]
SOURCES = [RUNNER, HELPER, *MODULES.values()]
CUDA_KEYS = set(MODULES) - {"jev-multicorrect"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--source-commit")
    parser.add_argument("--frozen-proof", type=Path, help="portable proof for a minimal remote source tree")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.seeds != "42,43,44":
        parser.error("new immutable output and fixed three seeds required")
    commit = args.source_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    hashes = {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in SOURCES}
    proof = json.loads(args.frozen_proof.read_text()) if args.frozen_proof else capture_sources(ROOT, commit, SOURCES)
    verify_sources(ROOT, commit, hashes, proof)
    import torch

    torch.set_num_threads(1)
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("requested CUDA unavailable; no CPU fallback")
    accelerator = torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU"
    if args.device == "cuda" and not any(model in accelerator for model in ("A100", "A30")):
        parser.error("this bounded receipt requires a real NVIDIA A100/A30")
    started = time.monotonic()
    components = {}
    for key, source in MODULES.items():
        if args.device == "cuda" and key not in CUDA_KEYS:
            continue
        function = importlib.import_module(source.removeprefix("src/").removesuffix(".py").replace("/", ".")).diagnostic
        rows = [function(seed, device=args.device) if key in CUDA_KEYS else function(seed) for seed in SEEDS]
        for row in rows:
            if not row["checks"] or not all(v is True for v in row["checks"].values()):
                raise RuntimeError(f"{key}: a defining contract failed")
            if not all(type(v) in (float, int, bool) and math.isfinite(v) for v in row["metrics"].values()):
                raise RuntimeError(f"{key}: nonfinite/nonscalar diagnostic")
        components[key] = {"per_seed": rows}
    if args.device == "cuda":
        torch.cuda.synchronize()
    payload = {"schema_version": 2, "device": args.device, "accelerator": accelerator,
        "seeds": SEEDS, "code_commit": commit, "source_sha256": hashes, "components": components,
        "elapsed_seconds": time.monotonic()-started,
        "diagnostic_only": True, "formal_comparison": False, "promotion_eligible": False,
        "evolve_integrated": False, "pretrained_model_calls": 0,
        "full_experiment_status": "not_reproduced_high_cost"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"device": args.device, "components": list(components), "elapsed_seconds": payload["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
