from __future__ import annotations


def configure(commands):
    from auto_research.scaling_law import DEFAULT_SCALING_POINTS
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    scaling = commands.add_parser(
        "scaling-law",
        help="run an auditable multi-budget empirical scaling curve for micro-llm",
    )
    scaling.add_argument("--dataset-dir", type=Path, default=Path("data"))
    scaling.add_argument("--output-dir", type=Path, default=Path("runs/scaling-law"))
    scaling.add_argument(
        "--points",
        default=DEFAULT_SCALING_POINTS,
        help="comma-separated DIMxLAYERS:TRAIN_TOKENS:STEPS points (minimum three)",
    )
    scaling.add_argument("--seeds", default="42")
    scaling.add_argument("--architecture", default="gpt_baseline")
    scaling.add_argument("--vocab-size", type=int, default=1024)
    scaling.add_argument("--batch-size", type=int, default=2)
    scaling.add_argument("--sequence-length", type=int, default=64)
    scaling.add_argument("--maximum-eval-tokens", type=int, default=8192)
    scaling.add_argument("--learning-rate", type=float, default=3e-4)
    scaling.add_argument("--optimizer", choices=["adamw", "adam", "adagrad"], default="adamw")
    scaling.add_argument("--resume", action="store_true")
    scaling.add_argument("--offline", action="store_true")
    _add_runtime_arguments(scaling)


def run(args):
    from auto_research.scaling_law import ScalingLawConfig
    from auto_research.scaling_law import ScalingLawRunner
    from auto_research.scaling_law import parse_scaling_points

    seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
    payload, run_dir = ScalingLawRunner(
        ScalingLawConfig(
            dataset_dir=args.dataset_dir,
            output_dir=args.output_dir,
            points=parse_scaling_points(args.points),
            seeds=seeds,
            architecture=args.architecture,
            vocab_size=args.vocab_size,
            batch_size=args.batch_size,
            sequence_length=args.sequence_length,
            maximum_eval_tokens=args.maximum_eval_tokens,
            learning_rate=args.learning_rate,
            beta=args.beta,
            optimizer=args.optimizer,
            allow_network=not args.offline,
            resume=args.resume,
        )
    ).run()
    fit = payload["fit"]["compute_power_law"]
    print(
        f"Points: {len(payload['points'])}; log RMSE: {fit['log_rmse']:.6f}; "
        f"R^2: {fit['r_squared']:.6f}"
    )
    print(f"Report: {run_dir / 'report.md'}")
    return 0
