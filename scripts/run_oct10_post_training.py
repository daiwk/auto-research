"""Train exact October OPD/RL operators on user-provided public checkpoints."""

import argparse
from pathlib import Path

from auto_research.post_training.oct10_checkpoint import OBJECTIVES, run_checkpoint


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objective", choices=OBJECTIVES, required=True)
    for field in ("student", "teacher"):
        parser.add_argument(f"--{field}-path", type=Path, required=True)
        parser.add_argument(f"--{field}-id", required=True)
        parser.add_argument(f"--{field}-revision", required=True)
    parser.add_argument("--train-path", type=Path, required=True)
    parser.add_argument("--validation-path", type=Path, required=True)
    parser.add_argument("--dataset-revision", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=3)
    parser.add_argument("--max-tokens", type=int, default=32)
    parser.add_argument("--group", type=int, default=4)
    parser.add_argument("--learning-rate", type=float, default=1e-5)
    parser.add_argument("--validation-examples", type=int, default=4)
    parser.add_argument("--device", default="cuda")
    run_checkpoint(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
