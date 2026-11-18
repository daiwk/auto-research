"""Admit source-bound tiny-model CUDA compatibility, not a new9B benchmark."""
import argparse
import hashlib
import json
import math

from oct18_frozen_sources import verify_sources
from run_nov15_vcola_compat import AUDIT, ROOT, SEEDS, source_hashes

ARTIFACT = "docs/gpu-validations/vcola-gva-compat-a100-20261115.json"


def load(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    frozen = load(AUDIT / "frozen-sources.json")
    if source_hashes() != frozen["source_sha256"]:
        raise ValueError("V-CoLA execution sources changed")
    verify_sources(ROOT, frozen["commit"], source_hashes(), frozen["proof"])
    runs = {device: load(AUDIT / f"raw-{device}.json") for device in ("cpu", "cuda")}
    for device, raw in runs.items():
        if (raw["source_sha256"] != source_hashes() or raw["code_commit"] != frozen["commit"]
                or raw["device"] != device or raw["seeds"] != SEEDS
                or raw["transformers_version"] != "5.23.0" or not 0 <= raw["elapsed_seconds"] <= 180):
            raise ValueError("wrong source/dependency/device/seed/budget provenance")
        expected = {"diagnostic_only": True, "formal_comparison": False, "promotion_eligible": False,
                    "evolve_integrated": False, "pretrained_model_calls": 0, "model_and_dataset_downloads": 0,
                    "api_calls": 0, "full_experiments_executed": False, "automatic_retry": False}
        if any(type(raw.get(k)) is not type(v) or raw.get(k) != v for k, v in expected.items()):
            raise ValueError("compatibility evidence cannot be promoted to capability")
        if len(raw["per_seed"]) != 3:
            raise ValueError("exactly three actual seed records required")
        for seed, row in zip(SEEDS, raw["per_seed"], strict=True):
            if (row["seed"] != seed or row["execution_device"] != device
                    or not row["checks"] or any(v is not True for v in row["checks"].values())
                    or any(type(v) not in (int, float) or not math.isfinite(v) for v in row["metrics"].values())):
                raise ValueError("actual compatibility checks or finite metrics failed")
    cuda = runs["cuda"]
    if not cuda["accelerator"].startswith(("NVIDIA A100", "NVIDIA A30")):
        raise ValueError("real A100/A30 evidence required")
    metrics = {name: math.fsum(row["metrics"][name] for row in cuda["per_seed"]) / 3
               for name in cuda["per_seed"][0]["metrics"]}
    receipt = {"schema_version": 1, "adapter_key": "vcola", "validated_at": "2026-11-15",
               "accelerator": {"vendor": "NVIDIA", "model": cuda["accelerator"], "count": 1},
               "command": ["timeout", "180", "python3", "scripts/run_nov15_vcola_compat.py", "--device", "cuda",
                           "--source-commit", frozen["commit"], "--output", "raw-cuda.json"],
               "dataset": {"id": "synthetic:tiny-qwen35-gva-vision-compat-v1",
                           "revision": "sha256:" + source_hashes()["tests/multimodal/test_vcola.py"],
                           "public_capability_benchmark": False, "recipe": cuda["input_scope"]},
               "checkpoint": {"public_id": "none-random-tiny-Qwen3.5",
                              "revision": frozen["commit"], "pretrained": False,
                              "configuration": cuda["model_configuration"]},
               "seeds": SEEDS, "result": "passed", "metrics": metrics,
               "diagnostic_only": True, "evaluation_tier": "l1_mechanism", "promotion_eligible": False,
               "evolve_integrated": False, "full_checkpoint_campaign_reexecuted": False,
               "runtime_library": {"transformers": "5.23.0"},
               "historical_9b_receipt": "docs/gpu-validations/vcola-a100-20261011.json",
               "claim_boundary": "Compact-GVA interface and tiny real vision/hybrid forward only; not a new9B checkpoint quality measurement",
               "provenance": {"commit": frozen["commit"], "artifact_path": ARTIFACT,
                              "executed_source_sha256": source_hashes(),
                              "raw_artifact": "docs/research-audits/nov15-refresh/vcola-compat/raw-cuda.json",
                              "raw_artifact_sha256": hashlib.sha256((AUDIT / "raw-cuda.json").read_bytes()).hexdigest()}}
    path = ROOT / ARTIFACT
    if args.check:
        if load(path) != receipt:
            raise ValueError("accepted receipt differs from actual execution")
    else:
        if path.exists():
            raise ValueError("refusing to overwrite GPU compatibility evidence")
        path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print("V-CoLA compact-GVA CPU and real A100 compatibility accepted; no9B quality claim")


if __name__ == "__main__":
    main()
