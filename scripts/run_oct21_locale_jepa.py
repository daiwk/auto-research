#!/usr/bin/env python3
"""Bounded LocaLeJEPA mechanism/gradient diagnostic; no downloads or image claims."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

import torch

from auto_research.foundation_models.locale_jepa import ballreg_loss, locale_jepa_loss

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("src/auto_research/foundation_models/locale_jepa.py", "scripts/run_oct21_locale_jepa.py")
UPSTREAM_REVISION = "771361c18d37e65df3dc188761ffb26751ce4e37"


def run(device: str, seed: int, steps: int) -> dict:
    torch.manual_seed(seed)
    generator = torch.Generator(device=device).manual_seed(seed)
    samples, dimension, views = 64, 8, 2
    centers = torch.eye(dimension, device=device)[:4].repeat_interleave(samples // 4, 0) * 3
    base = centers + torch.randn(samples, dimension, device=device) * 0.3
    inputs = base.unsqueeze(0) + torch.randn(views, samples, dimension, device=device) * 0.1
    projector = torch.nn.Linear(dimension, dimension, device=device)
    optimizer = torch.optim.AdamW(projector.parameters(), lr=1e-3)
    trajectory = []
    stats = {}
    gradient_norm = 0.0
    for _ in range(steps):
        optimizer.zero_grad()
        terms = locale_jepa_loss(projector(inputs), generator=generator, stats=stats)
        terms["loss"].backward()
        gradient_norm = float(projector.weight.grad.norm())
        optimizer.step()
        trajectory.append({key: float(value.detach()) for key, value in terms.items()})
    collapsed = torch.zeros(views, samples, dimension, device=device)
    collapsed_regularizer = ballreg_loss(collapsed, generator=generator)
    return {"seed": seed, "fixture_only": True, "trajectory": trajectory,
            "cluster_diagnostics": stats, "metrics": {
                "final_loss": trajectory[-1]["loss"],
                "prediction_loss": trajectory[-1]["prediction"],
                "local_uniform_ball_regularizer": trajectory[-1]["regularizer"],
                "projector_gradient_norm": gradient_norm,
                "collapsed_uniform_ball_penalty": float(collapsed_regularizer),
                "effective_clusters": stats["effective_clusters"],
                "fallback": stats["fallback"], "steps": steps},
            "data_sha256": hashlib.sha256(inputs.detach().cpu().numpy().tobytes()).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--source-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    seeds = [int(value) for value in args.seeds.split(",")]
    if not 1 <= args.steps <= 32 or not 1 <= len(seeds) <= 3 or len(set(seeds)) != len(seeds):
        raise SystemExit("cost gate: 1-32 steps and 1-3 distinct seeds")
    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA requested but unavailable; CPU fallback forbidden")
    if args.output.exists():
        raise SystemExit("immutable output already exists")
    commit = args.source_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise SystemExit("full source commit required")
    torch.set_num_threads(1)
    started = time.monotonic()
    rows = [run(args.device, seed, args.steps) for seed in seeds]
    result = {"schema_version": 2, "protocol": "locale-jepa-uniform-ball-l1-v1",
              "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
              "promotion_eligible": False, "evolve_integrated": False,
              "formal_comparison": False, "fixture_only": True,
              "full_experiment_status": "not_reproduced_high_cost",
              "code_commit": commit, "device": args.device,
              "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
              "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCES},
              "public_source": {"repository": "https://github.com/alessioborgi/LocaLeJEPA",
                                "revision": UPSTREAM_REVISION},
              "dataset": "generated_multiview_vector_mechanism_fixture_v1",
              "checkpoint": None, "seeds": seeds, "results": rows,
              "elapsed_seconds": time.monotonic() - started}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "seeds": seeds,
                      "elapsed_seconds": result["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
