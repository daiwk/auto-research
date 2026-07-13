from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import ResearchConfig
from .publish import publish_report
from .reproductions.registry import get_adapter, list_adapters
from .reproductions.reporting import (
    write_legacy_combined_report,
    write_reproduction_result,
)
from .runner import ResearchRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="auto-research")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="search papers and run iterative experiments")
    run.add_argument("--topic", help="research topic (or provide --config)")
    run.add_argument("--track", choices=["llm", "recommendation"])
    run.add_argument("--config", type=Path)
    run.add_argument("--trials", type=int, default=8)
    run.add_argument("--papers", type=int, default=8)
    run.add_argument("--offline", action="store_true")
    run.add_argument("--output-dir", type=Path, default=Path("runs"))

    init = commands.add_parser("init", help="write an editable example configuration")
    init.add_argument("path", type=Path, nargs="?", default=Path("research.json"))
    init.add_argument("--track", choices=["llm", "recommendation"], default="llm")

    publish = commands.add_parser("publish", help="commit a report and open a GitHub PR")
    publish.add_argument("report", type=Path)
    publish.add_argument("--title", required=True)
    publish.add_argument("--base")
    publish.add_argument("--ready", action="store_true")

    reproduce = commands.add_parser(
        "reproduce", help="run paper-specific baseline comparisons"
    )
    adapter_keys = [adapter.key for adapter in list_adapters()]
    reproduce.add_argument("--paper", choices=[*adapter_keys, "all"], default="all")
    reproduce.add_argument("--dataset-dir", type=Path, default=Path("data"))
    reproduce.add_argument(
        "--output-dir", type=Path, default=Path("runs/reproductions")
    )
    reproduce.add_argument("--output", type=Path, help=argparse.SUPPRESS)
    reproduce.add_argument("--seed", type=int, default=42)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "init":
            _init_config(args.path, args.track)
            print(f"Created {args.path}")
            return 0
        if args.command == "publish":
            print(publish_report(args.report, args.title, args.base, args.ready))
            return 0
        if args.command == "reproduce":
            adapters = (
                list(list_adapters())
                if args.paper == "all"
                else [get_adapter(args.paper)]
            )
            entries = [
                (adapter, adapter.run(args.dataset_dir, args.seed))
                for adapter in adapters
            ]
            if args.output:
                report = write_legacy_combined_report(entries, args.output)
                print(f"Report: {report.resolve()}")
            else:
                for adapter, result in entries:
                    report = write_reproduction_result(
                        adapter, result, args.output_dir
                    )
                    print(f"{adapter.key}: {report.resolve()}")
            return 0
        config = _run_config(args)
        result, run_dir = ResearchRunner(config).run()
        if not result.best_trial:
            print(f"Run failed; inspect {run_dir / 'report.md'}", file=sys.stderr)
            return 2
        print(f"Best {result.metric_name}: {result.best_trial.metric:.6f}")
        print(f"Report: {run_dir / 'report.md'}")
        return 0
    except (ValueError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _run_config(args: argparse.Namespace) -> ResearchConfig:
    if args.config:
        return ResearchConfig.from_file(args.config)
    if not args.topic or not args.track:
        raise ValueError("--topic and --track are required without --config")
    return ResearchConfig(
        topic=args.topic,
        track=args.track,
        max_trials=args.trials,
        max_papers=args.papers,
        output_dir=args.output_dir,
        allow_network=not args.offline,
    )


def _init_config(path: Path, track: str) -> None:
    if path.exists():
        raise ValueError(f"refusing to overwrite {path}")
    payload = {
        "topic": "efficient post-training" if track == "llm" else "ranking loss and negative sampling",
        "track": track,
        "max_papers": 8,
        "max_trials": 8,
        "seed": 42,
        "output_dir": "runs",
        "dataset_dir": "data",
        "allow_network": True,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
