#!/usr/bin/env python3
"""Run FORTE on chronological MovieLens-100K, with real CPU/CUDA training."""

import argparse
import json
from pathlib import Path

from auto_research.reproductions.forte.experiment import run_forte


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dataset-dir", type=Path, required=True)
    p.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--epochs", type=int, default=6)
    p.add_argument("--batch-size", type=int, default=512)
    p.add_argument("--limit", type=int)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    result = run_forte(
        a.dataset_dir,
        a.seed,
        device=a.device,
        epochs=a.epochs,
        batch_size=a.batch_size,
        limit=a.limit,
    )
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"selected_removed": result["selected_removed"], "test": result["test"]}))


if __name__ == "__main__":
    main()
