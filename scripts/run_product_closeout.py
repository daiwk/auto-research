"""Run matched category-adapter ablations on real public product interactions."""
import argparse
import json
from pathlib import Path
import subprocess

import torch

from auto_research.reproductions.industrial_2026 import evaluate
from auto_research.reproductions.product_data import load_product_data
from auto_research.reproductions.sep7_models import train_two_tower


def run(root, steps=200, seeds=(42, 43, 44)):
    torch.set_num_threads(4)
    data, evidence = load_product_data(root)
    rows = []
    for seed in seeds:
        methods = {}
        for adapter in (False, True):
            table, training = train_two_tower(data, seed, adapter=adapter, steps=steps)
            scorer = lambda history: table[history[-1]]
            methods["category_adapter" if adapter else "shared_two_tower"] = {
                "training": training,
                "validation": evaluate(data, scorer, target_split="validation"),
                "test": evaluate(data, scorer, target_split="test"),
            }
        rows.append({"seed": seed, "methods": methods})
        print(json.dumps(rows[-1]), flush=True)
    return {"schema_version": 2, "dataset": evidence, "runs": rows,
            "provenance": {"commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], text=True).strip()},
            "evaluation_protocol": {"formal_comparison": False,
                                    "scope": "matched public next-product mechanism experiment; not a semantic complementarity benchmark"}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, default=Path("data"))
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.dataset_dir, args.steps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
