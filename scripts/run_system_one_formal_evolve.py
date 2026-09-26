#!/usr/bin/env python3
"""Run a reproducible multi-generation System One checkpoint comparison."""

from __future__ import annotations

import argparse
from pathlib import Path

from auto_research.evolution.engine import ModelEvolutionEngine
from auto_research.evolution.models import EvolutionConfig


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--nimble", type=Path)
    parser.add_argument("--nimble-base", type=Path)
    parser.add_argument("--laya", type=Path)
    parser.add_argument("--nanojev", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("runs/system-one-formal-evolve"))
    parser.add_argument("--resume", type=Path, help="Continue an interrupted run from result.json")
    parser.add_argument("--generations", type=int, default=2)
    parser.add_argument("--population", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default="cuda:0")
    args = parser.parse_args()
    config = EvolutionConfig(
        model="system-one", dataset="system-one-public",
        direction="比较开放 checkpoint、校准温度与选择性阈值",
        output_dir=args.output_dir, generations=args.generations,
        resume_dir=args.resume,
        population=args.population, seeds=(args.seed,), workers=1,
        allow_network=False, device=args.device,
        system_one_public_data=args.data,
        system_one_nanojev_checkpoint=args.nanojev,
        system_one_nimble_checkpoint=args.nimble,
        system_one_nimble_base=args.nimble_base,
        system_one_laya_checkpoint=args.laya,
    )
    result, run_dir = ModelEvolutionEngine(config).run()
    print(f"run_dir={run_dir}")
    print(f"champion_id={result.champion_id}")
    print(f"rounds={len(result.rounds)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
