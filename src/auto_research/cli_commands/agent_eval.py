from __future__ import annotations


def configure(commands):
    from auto_research.agent_research.models import METHODS as AGENT_METHODS
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    agent_eval = commands.add_parser(
        "agent-eval",
        help="evaluate paper-inspired agent memory, planning and tool-use methods",
    )
    agent_eval.add_argument(
        "--method",
        choices=AGENT_METHODS,
        required=True,
    )
    agent_eval.add_argument(
        "--benchmark",
        choices=[
            "evomem-mini",
            "planbench-mini",
            "scalemcp-mini",
            "swebench-local",
            "osreward-mini",
        ],
        default="evomem-mini",
    )
    agent_eval.add_argument("--episodes", type=int, default=120)
    agent_eval.add_argument("--memory-size", type=int, default=24)
    agent_eval.add_argument("--seed", type=int, default=42)
    agent_eval.add_argument("--output-dir", type=Path, default=Path("runs/agent-research"))
    _add_runtime_arguments(agent_eval)


def run(args):
    from auto_research.agent_research import AgentResearchConfig
    from auto_research.agent_research import AgentResearchRunner

    result, run_dir = AgentResearchRunner(
        AgentResearchConfig(
            method=args.method,
            benchmark=args.benchmark,
            episodes=args.episodes,
            memory_size=args.memory_size,
            seed=args.seed,
            output_dir=args.output_dir,
        )
    ).run()
    print(f"Joint success: {result.metrics['joint_success']:.4f}")
    print(f"Average cost: {result.metrics['average_cost']:.4f}")
    print(f"Report: {run_dir / 'report.md'}")
    return 0
