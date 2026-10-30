"""Execute only the frozen ten-component Oct30 overlap-backfill scope."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_google_emnlp25_components import validate_row  # noqa: E402

RUNNER = "scripts/run_oct30_components.py"
SPEC = "docs/research-audits/oct30-overlap-components/execution-spec.json"
PREFLIGHT = "docs/research-audits/oct30-overlap-components/preflight.json"
SEEDS = [42, 43, 44]
COMPONENTS = {
    "concur": ("post_training/concur.py", "cpu"),
    "merlin": ("foundation_models/merlin.py", "cuda"),
    "crop": ("agent_research/crop.py", "cpu"),
    "pinger": ("reproductions/pinger_components.py", "cuda"),
    "pinterest-rlbp": ("reproductions/pinterest_rlbp.py", "cuda"),
    "fold-bias": ("foundation_models/fold_bias.py", "cuda"),
    "swim": ("foundation_models/swim.py", "cuda"),
    "mpopd": ("post_training/mpopd.py", "cuda"),
    "emma": ("agent_research/emma.py", "cpu"),
    "evalalloc": ("agent_research/evalalloc.py", "cpu"),
}


def execution_spec():
    spec = json.loads((ROOT / SPEC).read_text())
    if spec.get("schema_version") != 1 or spec.get("seeds") != SEEDS:
        raise ValueError("fixed three-seed schema required")
    rows = spec["components"]
    if len(rows) != len(COMPONENTS) or {r["key"] for r in rows} != set(COMPONENTS):
        raise ValueError("exactly the fixed ten component contracts required")
    for row in rows:
        source, device = COMPONENTS[row["key"]]
        if (row["source"] != "src/auto_research/" + source or row["device"] != device
                or not row["checks"] or not row["metrics"] or not row["gates"]):
            raise ValueError("fixed module/device and explicit numerical contracts required")
    return spec


def sources(spec):
    return [RUNNER, SPEC, PREFLIGHT, "scripts/oct18_frozen_sources.py", "scripts/run_google_emnlp25_components.py",
            *sorted({r["source"] for r in spec["components"]})]


def load_component(key, source):
    name = "_oct30_" + key.replace("-", "_")
    loader = importlib.util.spec_from_file_location(name, ROOT / source)
    if loader is None or loader.loader is None:
        raise ValueError("fixed source unavailable")
    module = importlib.util.module_from_spec(loader)
    sys.modules[name] = module
    loader.loader.exec_module(module)
    if Path(module.__file__).resolve() != (ROOT / source).resolve():
        raise ValueError("installed package shadowed the frozen source")
    return module


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
        parser.error("real NVIDIA A100/A30 required")
    started, components = time.monotonic(), {}
    for expected in spec["components"]:
        if args.device == "cuda" and expected["device"] != "cuda":
            continue
        module = load_component(expected["key"], expected["source"])
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
