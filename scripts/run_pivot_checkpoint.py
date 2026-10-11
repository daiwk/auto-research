#!/usr/bin/env python3
import argparse
from pathlib import Path

from auto_research.post_training.pivot_checkpoint import run


def main():
    p = argparse.ArgumentParser(description="Real PIVOT intent distillation with shared SFT/OPD warmup and isolated holdout")
    for name in ("student-path", "teacher-path", "train-path", "validation-path", "split-manifest", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    for name in ("student-id", "student-revision", "teacher-id", "teacher-revision", "dataset-revision"):
        p.add_argument("--" + name, required=True)
    for name, default in (("seed", 42), ("training-examples", 8), ("validation-examples", 8), ("steps", 8),
                          ("warmup-steps", 2), ("sft-epochs", 2), ("batch-size", 2), ("group", 2), ("max-tokens", 256)):
        p.add_argument("--" + name, type=int, default=default)
    p.add_argument("--device", default="cuda")
    run(**vars(p.parse_args()))


if __name__ == "__main__":
    main()
