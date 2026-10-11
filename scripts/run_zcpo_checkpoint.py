#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from auto_research.post_training.oct11_checkpoint import run_zcpo


def main():
    p = argparse.ArgumentParser(description="Real checkpoint ZCPO; equal reward groups are skipped")
    for name in ("checkpoint-path", "train-path", "validation-path", "output"):
        p.add_argument("--" + name, required=True, type=Path)
    for name in ("checkpoint-id", "checkpoint-revision", "dataset-revision"):
        p.add_argument("--" + name, required=True)
    p.add_argument("--steps", type=int, default=8)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-tokens", type=int, default=128)
    p.add_argument("--group", type=int, default=4)
    p.add_argument("--validation-examples", type=int, default=8)
    p.add_argument("--device", default="cuda")
    p.add_argument("--split-manifest", type=Path)
    run_zcpo(**vars(p.parse_args()))


if __name__ == "__main__":
    main()
