from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    mad_rl = commands.add_parser(
        "mad-rl",
        help="run the MaD-RL five-category synthetic-choice mechanism audit",
    )
    mad_rl.add_argument("--divergences", default="correctness,l2,forward-kl,reverse-kl,jsd")
    mad_rl.add_argument(
        "--target", default="0,0,0.3333333333333333,0.3333333333333333,0.3333333333333333"
    )
    mad_rl.add_argument("--seeds", default="42,43,44")
    mad_rl.add_argument("--steps", type=int, default=60)
    mad_rl.add_argument("--group-size", type=int, default=16)
    mad_rl.add_argument("--output-dir", type=Path, default=Path("runs/post-training/mad-rl"))
    _add_runtime_arguments(mad_rl)


def run(args):

    from auto_research.post_training.mad_rl import run_choice_experiment

    payload, run_dir = run_choice_experiment(
        seeds=tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip()),
        divergences=tuple(value.strip() for value in args.divergences.split(",") if value.strip()),
        target=tuple(float(value.strip()) for value in args.target.split(",")),
        steps=args.steps,
        group_size=args.group_size,
        output_dir=args.output_dir,
    )
    print(f"MaD-RL mechanism runs: {len(payload['runs'])}")
    print(f"Report: {run_dir / 'report.md'}")
    return 0
