#!/usr/bin/env python3
"""Three-seed CPU L1 receipt for LESSER's forward-only feature identity.

No held-out benchmark, full-gradient data-selection baseline, or LLM training
is claimed by this receipt. Run with PYTHONPATH=src python scripts/run_lesser_20261005.py.
"""

import json
from pathlib import Path

import torch

from auto_research.post_training.lesser import (
    output_gradient_feature,
    rademacher_projection,
    round_robin_select,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/post-training/2610.03702-lesser/metrics/mechanism-seeds42-44.json"


def run(seed: int) -> dict:
    torch.manual_seed(seed)
    hidden = torch.randn(8, 6, dtype=torch.float64)
    readout = torch.randn(11, 6, dtype=torch.float64, requires_grad=True)
    target = torch.randint(0, 11, (8,))
    weights = torch.rand(8, dtype=torch.float64)
    weights[0] = 0
    logits = hidden @ readout.T
    forward = output_gradient_feature(hidden, logits.detach(), target, weights, normalize=False).reshape(11, 6)
    loss = -(weights * logits.log_softmax(-1).gather(1, target[:, None]).squeeze(1)).sum()
    reference = torch.autograd.grad(loss, readout)[0]
    left, right = rademacher_projection(11, 6, 4, 5, seed=seed)
    projected = output_gradient_feature(
        hidden, logits.detach(), target, weights, projection=(left, right), normalize=False
    ).reshape(4, 5)
    pool = torch.randn(10, 20, dtype=torch.float64)
    query = torch.randn(3, 20, dtype=torch.float64)
    chosen = round_robin_select(pool, query, 4)
    return {
        "seed": seed,
        "readout_gradient_max_abs_error": float((forward - reference).abs().max()),
        "projection_max_abs_error": float((projected - left @ forward @ right).abs().max()),
        "selected_unique": len(chosen) == len(set(chosen)),
        "selected_count": len(chosen),
    }


def main() -> None:
    results = [run(seed) for seed in (42, 43, 44)]
    assert all(item["readout_gradient_max_abs_error"] < 1e-12 for item in results)
    assert all(item["projection_max_abs_error"] < 1e-12 for item in results)
    payload = {
        "schema_version": 2,
        "paper": "2610.03702",
        "tier": "L1",
        "diagnostic_only": True,
        "device": "cpu",
        "dataset": "synthetic fixed readout tensors (formula diagnostic)",
        "manifest_ref": "post-training:lesser",
        "protocol": "Random fixed hidden states/readout; exact autograd parity and tokenwise projection parity; no model training",
        "seeds": [42, 43, 44],
        "evaluation_protocol": {
            "tier": "l1_mechanism",
            "seeds": [42, 43, 44],
            "formal_comparison": False,
            "claim_policy": "three-seed formula/selector diagnostic only; no capability or speedup claim",
        },
        "provenance": {
            "artifact_path": str(OUTPUT.relative_to(ROOT)),
            "dataset_fingerprint": "synthetic-fixed-rng-torch-seeds42-44; no public dataset",
        },
        "metrics": {
            "gradient_identity_max_abs_error": max(item["readout_gradient_max_abs_error"] for item in results),
            "projection_identity_max_abs_error": max(item["projection_max_abs_error"] for item in results),
        },
        "results": results,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
