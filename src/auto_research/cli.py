from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import ResearchConfig
from .evolution import EvolutionConfig, ModelEvolutionEngine
from .publish import publish_report
from .reproductions.base import ReproductionFidelity
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
    run.add_argument("--force-rerun", action="store_true")

    commands.add_parser("list", help="list installed paper/idea plugins")

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
    reproduce.add_argument(
        "--include-concept-demos",
        action="store_true",
        help="include adapters whose core paper model/training is still a proxy",
    )

    evolve = commands.add_parser(
        "evolve", help="evolve an existing model with paper-inspired structures and hyperparameters"
    )
    evolve.add_argument("--model", choices=["rankmixer", "hyformer", "micro-llm"], required=True)
    evolve.add_argument("--dataset", choices=["movielens-100k", "movielens-1m", "wikitext-2"], required=True)
    evolve.add_argument("--direction", required=True, help="natural-language research direction")
    evolve.add_argument("--dataset-dir", type=Path, default=Path("data"))
    evolve.add_argument("--output-dir", type=Path, default=Path("runs/evolution"))
    evolve.add_argument("--query")
    evolve.add_argument("--generations", type=int, default=3)
    evolve.add_argument("--population", type=int, default=4)
    evolve.add_argument("--papers", type=int, default=8)
    evolve.add_argument("--steps", type=int, default=100)
    evolve.add_argument("--seeds", default="42", help="comma-separated integer seeds")
    evolve.add_argument("--offline", action="store_true")
    evolve.add_argument("--workers", type=int, default=1, help="parallel experiments per generation")
    evolve.add_argument("--maximum-users", type=int, help="explicit smoke-test user limit")
    evolve.add_argument("--maximum-items", type=int, help="explicit smoke-test item limit")
    evolve.add_argument("--evaluation-users", type=int, default=1000, help="fixed validation/test cohort; 0 means all users")
    evolve.add_argument("--maximum-train-tokens", type=int, help="optional LLM smoke-test token limit")
    evolve.add_argument("--maximum-eval-tokens", type=int, default=100000, help="LLM validation/test token limit")
    evolve.add_argument("--vocab-size", type=int, default=4096, help="local BPE vocabulary for micro-llm")
    evolve.add_argument("--llm-dimensions", type=int, default=384, help="initial micro-llm hidden width")
    evolve.add_argument("--llm-layers", type=int, default=6, help="initial micro-llm layer count")
    evolve.add_argument("--llm-batch-size", type=int, default=4, help="initial micro-llm batch size")
    evolve.add_argument("--llm-sequence-length", type=int, default=128, help="micro-llm context length")
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
        if args.command == "list":
            for adapter in list_adapters():
                print(
                    f"{adapter.key:20} {adapter.fidelity.value:16} "
                    f"{adapter.paper.arxiv_id:12} {adapter.paper.title}"
                )
            return 0
        if args.command == "reproduce":
            adapters = (
                [
                    adapter
                    for adapter in list_adapters()
                    if args.include_concept_demos
                    or adapter.fidelity is not ReproductionFidelity.CONCEPT_DEMO
                ]
                if args.paper == "all"
                else [get_adapter(args.paper)]
            )
            for adapter in adapters:
                if adapter.fidelity is ReproductionFidelity.CONCEPT_DEMO:
                    print(
                        f"warning: {adapter.key} is a concept demo, not a paper reproduction; "
                        "its result must not be compared with the paper's reported lift.",
                        file=sys.stderr,
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
        if args.command == "evolve":
            seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
            config = EvolutionConfig(
                model=args.model,
                dataset=args.dataset,
                direction=args.direction,
                dataset_dir=args.dataset_dir,
                output_dir=args.output_dir,
                query=args.query,
                generations=args.generations,
                population=args.population,
                max_papers=args.papers,
                steps=args.steps,
                seeds=seeds,
                allow_network=not args.offline,
                workers=args.workers,
                maximum_users=args.maximum_users,
                maximum_items=args.maximum_items,
                evaluation_users=args.evaluation_users or None,
                maximum_train_tokens=args.maximum_train_tokens,
                maximum_eval_tokens=args.maximum_eval_tokens,
                vocab_size=args.vocab_size,
                llm_dimensions=args.llm_dimensions,
                llm_layers=args.llm_layers,
                llm_batch_size=args.llm_batch_size,
                llm_sequence_length=args.llm_sequence_length,
            )
            result, run_dir = ModelEvolutionEngine(config).run()
            champion = next(trial for trial in result.trials if trial.trial_id == result.champion_id)
            print(f"Champion: {champion.trial_id} ({champion.genome.architecture})")
            if args.model == "micro-llm":
                print(f"Validation perplexity: {champion.validation['perplexity']:.4f}")
                print(f"Instruction loss: {champion.validation['instruction_loss']:.4f}")
            else:
                print(f"Validation NDCG@10: {champion.validation['ndcg_at_10']:.6f}")
            print(f"Report: {run_dir / 'report.md'}")
            print(f"Dashboard: {run_dir / 'index.html'}")
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
        force_rerun=args.force_rerun,
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
        "proposal_command": None,
        "proposal_timeout_seconds": 300,
        "cache_dir": ".auto-research/cache",
        "force_rerun": False,
        "experiment_revision": None,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
