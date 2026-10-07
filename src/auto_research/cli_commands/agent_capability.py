from __future__ import annotations


def configure(commands):
    from auto_research.agent_research.capability_methods import CAPABILITY_METHODS
    from pathlib import Path

    agent_capability = commands.add_parser(
        "agent-capability",
        help="compare Agent policies on held-out L2.1 tasks without guide/oracle labels",
    )
    agent_capability.add_argument("--methods", default=",".join(CAPABILITY_METHODS))
    agent_capability.add_argument("--seeds", default="42,43,44")
    agent_capability.add_argument("--episodes", type=int, default=60)
    agent_capability.add_argument("--train-episodes", type=int, default=36)
    agent_capability.add_argument(
        "--output-dir",
        type=Path,
        default=Path("runs/agent-capability"),
    )


def run(args):
    from auto_research.agent_research import CapabilitySuiteConfig
    from auto_research.agent_research import run_capability_suite

    methods = tuple(value.strip() for value in args.methods.split(",") if value.strip())
    seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
    results = run_capability_suite(
        CapabilitySuiteConfig(
            methods=methods,
            seeds=seeds,
            episodes=args.episodes,
            train_episodes=args.train_episodes,
            output_dir=args.output_dir,
        )
    )
    for method, payload in results.items():
        print(
            f"{method}: joint={payload['metrics']['joint_success']:.4f}, "
            f"plan_f1={payload['metrics']['plan_step_f1']:.4f}, "
            f"cost={payload['metrics']['average_cost']:.4f}"
        )
    print(f"Summary: {args.output_dir / 'summary.json'}")
    return 0
