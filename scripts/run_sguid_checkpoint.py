#!/usr/bin/env python3
"""Run two real SGUID curation/probe/restart/internalization cycles."""
import argparse
from pathlib import Path

from auto_research.post_training.sguid_checkpoint import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("checkpoint-path", "train-path", "validation-path", "split-manifest", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    for name in ("checkpoint-id", "checkpoint-revision", "dataset-revision"):
        parser.add_argument("--" + name, required=True)
    for name, default in (("seed", 42), ("training-examples", 8), ("validation-examples", 8),
                          ("rounds", 2), ("probe-steps", 8), ("internalization-steps", 8),
                          ("max-tokens", 512), ("skill-tokens", 256), ("candidate-count", 8),
                          ("retrieve-count", 6), ("late-minimum", 2)):
        parser.add_argument("--" + name, type=int, default=default)
    parser.add_argument("--device", default="cuda")
    result = run(**vars(parser.parse_args()))
    if result["status"] != "completed":
        raise SystemExit("SGUID failed persistence selection; retained artifact, no fallback")


if __name__ == "__main__":
    main()
