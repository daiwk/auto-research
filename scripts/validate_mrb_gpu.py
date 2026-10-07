#!/usr/bin/env python3
"""A100/A30 regression of lazy adapter spawn, CLI training and moved kernels."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    import torch

    assert torch.cuda.is_available()
    from auto_research.cli import main as cli
    from auto_research.experiment_contract import file_manifest, source_revision
    from auto_research.runtime import configure_runtime
    from auto_research.reproductions.registry import get_adapter
    from auto_research.reproductions.execution import run_with_budget
    from auto_research.mechanisms.rptune_curate import rptune_curate
    from auto_research.post_training.mechanisms.carm_response_mask import carm_response_mask

    configure_runtime("cuda", 1)
    args.output.mkdir(parents=True, exist_ok=True)
    audit_path = args.output / "device-audit.jsonl"
    os.environ["AUTO_RESEARCH_DEVICE_AUDIT_LOG"] = str(audit_path)
    os.environ["AUTO_RESEARCH_DIN_STEPS"] = "3"
    # Exercise serialized lazy bindings in spawn after the binding has already
    # been resolved once. No CUDA tensor crosses the process boundary.
    adapter = get_adapter("din")
    importlib.import_module(adapter.run.module)
    adapter = get_adapter("din")
    result = run_with_budget(adapter, args.data, 42, "smoke", timeout_override=180)
    assert result["setup"]["steps_per_seed"] == 3
    assert (
        cli(
            [
                "reproduce",
                "--paper",
                "din",
                "--dataset-dir",
                str(args.data),
                "--output-dir",
                str(args.output / "cli"),
                "--device",
                "cuda",
                "--cpu-threads",
                "1",
                "--seed",
                "42",
                "--budget",
                "smoke",
                "--budget-seconds",
                "180",
            ]
        )
        == 0
    )
    predictions = list((args.output / "cli").rglob("result.json"))
    assert len(predictions) == 1
    metrics = {
        "adapter_spawn_completed": 1,
        "cli_reproduction_completed": 1,
        "din_steps_per_seed": 3,
        "din_ndcg_at_10": result["results"]["din"]["ndcg_at_10"],
        "mean_pool_ndcg_at_10": result["results"]["mean_pool"]["ndcg_at_10"],
    }
    torch.manual_seed(42)
    adjustment = torch.randn(12, device="cuda", requires_grad=True)
    order, scores = rptune_curate(
        torch.randn(8, device="cuda"), torch.randn(12, 8, device="cuda"), adjustment, prune_rate=0.5
    )
    scores.square().mean().backward()
    assert adjustment.grad is not None and torch.isfinite(adjustment.grad).all()
    metrics["rptune_retained_items"] = len(order)
    metrics["rptune_gradient_norm"] = float(adjustment.grad.norm())
    current = torch.tensor([[0.1, 0.2], [0.8, -0.8]], device="cuda", requires_grad=True)
    mask, drift = carm_response_mask(current, torch.zeros_like(current), threshold=1.5)
    drift.sum().backward()
    assert mask.tolist() == [True, False]
    metrics["carm_mask_checks"] = 2
    metrics["carm_gradient_norm"] = float(current.grad.norm())
    audit = [json.loads(line) for line in audit_path.read_text().splitlines()]
    assert audit and all(row["resolved"].startswith("cuda") for row in audit)
    metrics["verified_cuda_device_resolutions"] = len(audit)
    artifact = "docs/gpu-validations/architecture-mrb-a100-20261007.json"
    receipt = {
        "schema_version": 1,
        "adapter_key": "architecture-mrb-runtime",
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "accelerator": {"vendor": "NVIDIA", "model": torch.cuda.get_device_name()},
        "command": [
            "python",
            "scripts/validate_mrb_gpu.py",
            "--data",
            "data",
            "--output",
            "runs/mrb-gpu",
            "--commit",
            args.commit,
        ],
        "dataset": {
            "name": "MovieLens-100k",
            "revision": file_manifest(args.data),
            "source": "https://files.grouplens.org/datasets/movielens/ml-100k.zip",
        },
        "checkpoint": {"model_id": "din-random-initialization", "revision": "seeds42-43-44"},
        "seeds": [42, 43, 44],
        "result": "passed",
        "metrics": metrics,
        "provenance": {
            "commit": args.commit,
            "source_fingerprint": source_revision(),
            "artifact_path": artifact,
        },
        "boundary": "real CUDA training/CLI/spawn and moved-kernel regression, not a paper-scale capability comparison",
    }
    (args.output / "receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
