#!/usr/bin/env python3
"""CPU-only AutoformBench inventory, execution planning and result import."""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path

from auto_research.agent_research.autoformbench import (
    OFFICIAL_MODELS, ProtocolError, fetch_release, harbor_plan,
    import_official_results, load_release, read_verifier_verdict,
    select_tasks, task_view, validate_comparison,
)


def _selection_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task", action="append", default=[])
    parser.add_argument("--book", action="append", default=[])
    parser.add_argument("--limit", type=int)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    fetch = actions.add_parser("fetch", help="download only pinned small CSVs")
    fetch.add_argument("--release-dir", type=Path, required=True)
    fetch.add_argument("--model", choices=OFFICIAL_MODELS, action="append", default=[])
    fetch.add_argument("--all-models", action="store_true")
    for name in ("tasks", "plan", "import-results"):
        command = actions.add_parser(name)
        command.add_argument("--release-dir", type=Path, required=True)
        command.add_argument("--output", type=Path, required=True)
        if name in {"tasks", "plan"}:
            _selection_arguments(command)
        if name == "plan":
            command.add_argument("--repository-dir", type=Path, required=True)
            command.add_argument("--agent", default="nop")
            command.add_argument("--model")
        if name == "import-results":
            command.add_argument("--model", choices=OFFICIAL_MODELS, action="append", default=[])
            command.add_argument("--all-models", action="store_true")
            command.add_argument("--source-condition", required=True, choices=("source-present", "source-free"))
            command.add_argument("--budget-usd", default="200")
            command.add_argument("--strict-budget", action="store_true")
    verdict = actions.add_parser("verdict", help="parse an existing real verifier verdict; do not execute Lean")
    verdict.add_argument("--path", type=Path, required=True)
    verdict.add_argument("--task", required=True)
    verdict.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == "fetch":
            if args.all_models and args.model:
                raise ProtocolError("choose --all-models or individual --model flags")
            result = fetch_release(args.release_dir, models=OFFICIAL_MODELS if args.all_models else args.model)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.output.exists():
            raise ProtocolError("choose a new immutable output path")
        if args.action == "verdict":
            result = read_verifier_verdict(args.path, expected_problem_id=args.task)
        else:
            release = load_release(args.release_dir)
            if args.action == "import-results":
                if args.all_models and args.model:
                    raise ProtocolError("choose --all-models or individual --model flags")
                models = OFFICIAL_MODELS if args.all_models else args.model
                if not models:
                    raise ProtocolError("select at least one --model or --all-models")
                budget = Decimal(args.budget_usd)
                reports = [import_official_results(
                    release, args.release_dir / f"leaderboard_data/{model}.csv", model=model,
                    source_condition=args.source_condition, budget_usd=budget,
                ) for model in models]
                validate_comparison(reports, source_condition=args.source_condition,
                                    budget_usd=budget, strict_budget=args.strict_budget)
                result = {"kind": "official_reference_import", "reports": reports,
                          "strict_budget_requested": args.strict_budget,
                          "local_execution_performed": False, "local_capability_score": None,
                          "diagnostic_only": True, "promotion_eligible": False}
            else:
                limit = args.limit
                if args.action == "plan" and not args.task and not args.book and limit is None:
                    limit = 1
                tasks = select_tasks(release, task_ids=args.task, books=args.book, limit=limit)
                result = task_view(release, tasks) if args.action == "tasks" else harbor_plan(
                    release, tasks, repository_dir=args.repository_dir, agent=args.agent, model=args.model,
                )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        if args.action == "import-results":
            summary = [{"model": row["model"], **row["metrics"],
                        "source_condition": row["source_condition"],
                        "over_budget_rows": row["budget_audit"]["observed_rows_above_nominal_cap"]}
                       for row in result["reports"]]
        else:
            summary = {"action": args.action, "output": str(args.output),
                       "execution_performed": False, "task_count": len(result.get("tasks", result.get("commands", [])))}
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    except (ProtocolError, OSError, ValueError, InvalidOperation) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
