from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    matrix = commands.add_parser(
        "multimodal-matrix",
        help="run a resumable, budget-matched matrix across public checkpoints",
    )
    matrix.add_argument("--config", type=Path, required=True)
    matrix.add_argument("--output-dir", type=Path, required=True)
    matrix.add_argument("--seed", type=int, default=42)
    matrix.add_argument("--offline", action="store_true")
    _add_runtime_arguments(matrix)


def run(args):
    from auto_research.multimodal import run_checkpoint_matrix

    run_dir = run_checkpoint_matrix(
        args.config, args.output_dir, seed=args.seed, offline=args.offline
    )
    print(f"Matrix: {run_dir / 'matrix.json'}")
    print(f"Report: {run_dir / 'report.md'}")
    return 0
