from __future__ import annotations


def configure(commands):
    from pathlib import Path

    agent_matrix = commands.add_parser(
        "agent-matrix",
        help="compare agent policies on the same real local executor tasks and budget",
    )
    agent_matrix.add_argument(
        "--methods", default="direct,critic,agent-lightning,swe-agent,openhands"
    )
    agent_matrix.add_argument("--seeds", default="42,43,44")
    agent_matrix.add_argument("--episodes", type=int, default=12)
    agent_matrix.add_argument("--memory-size", type=int, default=8)
    agent_matrix.add_argument("--output-dir", type=Path, default=Path("runs/agent-executor-matrix"))


def run(args):
    import json
    from auto_research.agent_research import run_executor_matrix

    payload, path = run_executor_matrix(
        output_dir=args.output_dir,
        methods=tuple(value.strip() for value in args.methods.split(",") if value.strip()),
        seeds=tuple(int(value) for value in args.seeds.split(",") if value.strip()),
        episodes=args.episodes,
        memory_size=args.memory_size,
    )
    print(json.dumps({"summary": payload["summary"], "metrics": str(path)}))
    return 0
