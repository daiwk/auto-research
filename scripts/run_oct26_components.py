"""Run the fixed Oct26 L1 scope against a frozen source proof, without models."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_google_emnlp25_components import validate_row  # noqa: E402

RUNNER = "scripts/run_oct26_components.py"
SPEC = "docs/research-audits/oct26-components/execution-spec.json"
SEEDS = [42, 43, 44]


def execution_spec():
    spec = json.loads((ROOT / SPEC).read_text())
    if spec.get("schema_version") != 1 or spec.get("seeds") != SEEDS or not spec.get("components"):
        raise ValueError("fixed nonempty three-seed spec required")
    rows = spec["components"]
    if len({r["key"] for r in rows}) != len(rows):
        raise ValueError("duplicate component")
    for row in rows:
        path = Path(row["source"])
        if (path.is_absolute() or ".." in path.parts or not row["source"].startswith("src/auto_research/")
                or path.suffix != ".py" or row["device"] != "cuda"
                or not row["checks"] or not row["metrics"] or not row["gates"]):
            raise ValueError("bounded source and explicit defining schemas/gates required")
    return spec


def sources(spec):
    package_inits = ["src/auto_research/__init__.py", *[
        f"src/auto_research/{package}/__init__.py" for package in (
            "foundation_models", "system_one", "multimodal", "post_training", "agent_research", "reproductions")]]
    return [RUNNER, SPEC, "scripts/oct18_frozen_sources.py", "scripts/run_google_emnlp25_components.py",
            *package_inits, *sorted({r["source"] for r in spec["components"]})]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--source-commit")
    parser.add_argument("--frozen-proof", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("immutable new output required")
    spec = execution_spec()
    paths = sources(spec)
    commit = args.source_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
    proof = json.loads(args.frozen_proof.read_text()) if args.frozen_proof else capture_sources(ROOT, commit, paths)
    verify_sources(ROOT, commit, hashes, proof)
    import torch

    torch.set_num_threads(1)
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("real CUDA required; CPU fallback forbidden")
    accelerator = torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU"
    if args.device == "cuda" and not any(n in accelerator for n in ("A100", "A30")):
        parser.error("real NVIDIA A100 or A30 required")
    started = time.monotonic()
    components = {}
    for expected in spec["components"]:
        module = importlib.import_module(expected["source"].removeprefix("src/").removesuffix(".py").replace("/", "."))
        if Path(module.__file__).resolve() != (ROOT / expected["source"]).resolve():
            raise RuntimeError("imported module is not the frozen source; installed-package shadowing forbidden")
        rows = []
        for seed in SEEDS:
            row = module.diagnostic(seed, device=args.device)
            validate_row(row, expected, seed)
            row.update(execution_device=args.device, execution_accelerator=accelerator)
            rows.append(row)
        components[expected["key"]] = {"per_seed": rows}
    if args.device == "cuda":
        torch.cuda.synchronize()
    result = {"schema_version": 2, "device": args.device, "accelerator": accelerator, "seeds": SEEDS,
              "code_commit": commit, "source_sha256": hashes, "components": components,
              "elapsed_seconds": time.monotonic() - started, "evaluation_tier": "l1_mechanism",
              "diagnostic_only": True, "formal_comparison": False, "promotion_eligible": False,
              "evolve_integrated": False, "pretrained_model_calls": 0, "full_experiments_executed": False}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"device": args.device, "components": list(components), "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
