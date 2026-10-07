from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.cli_commands.common import _add_runtime_arguments

    run = commands.add_parser("run", help="search papers and run iterative experiments")
    run.add_argument("--topic", help="research topic (or provide --config)")
    run.add_argument("--track", choices=["llm", "recommendation"])
    run.add_argument("--config", type=Path)
    run.add_argument("--trials", type=int, default=8)
    run.add_argument("--papers", type=int, default=8)
    run.add_argument("--offline", action="store_true")
    run.add_argument("--output-dir", type=Path, default=Path("runs"))
    run.add_argument("--force-rerun", action="store_true")
    _add_runtime_arguments(run)


def run(args):
    from auto_research.runner import ResearchRunner
    from auto_research.cli_commands.common import _run_config
    import sys

    config = _run_config(args)
    result, run_dir = ResearchRunner(config).run()
    if not result.best_trial:
        print(f"Run failed; inspect {run_dir / 'report.md'}", file=sys.stderr)
        return 2
    print(f"Best {result.metric_name}: {result.best_trial.metric:.6f}")
    print(f"Report: {run_dir / 'report.md'}")
    return 0
