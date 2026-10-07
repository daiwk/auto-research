from __future__ import annotations


def configure(commands):
    from pathlib import Path
    from auto_research.reproductions.base import ReproductionFidelity
    from auto_research.cli_commands.common import _add_runtime_arguments
    import argparse
    from auto_research.reproductions.registry import list_adapters

    reproduce = commands.add_parser("reproduce", help="run paper-specific baseline comparisons")
    adapter_keys = [adapter.key for adapter in list_adapters()]
    reproduce.add_argument("--paper", choices=[*adapter_keys, "all"], default="all")
    reproduce.add_argument("--dataset-dir", type=Path, default=Path("data"))
    reproduce.add_argument("--output-dir", type=Path, default=Path("runs/reproductions"))
    _add_runtime_arguments(reproduce)
    reproduce.add_argument("--output", type=Path, help=argparse.SUPPRESS)
    reproduce.add_argument(
        "--seed",
        type=int,
        help="single-seed override; otherwise each adapter's audited default seeds are used",
    )
    reproduce.add_argument(
        "--seeds",
        default="",
        help="comma-separated seeds; standard/formal runs should use at least three",
    )
    reproduce.add_argument("--workers", type=int, default=1)
    reproduce.add_argument("--track", help="filter adapters by track")
    reproduce.add_argument("--topic", help="filter adapters by topic substring")
    reproduce.add_argument("--organization", help="filter first-author organization substring")
    reproduce.add_argument(
        "--fidelity",
        choices=[level.value for level in ReproductionFidelity],
        help="filter by reproduction fidelity",
    )
    reproduce.add_argument(
        "--budget",
        choices=["smoke", "standard", "paper-specific"],
        default="paper-specific",
    )
    reproduce.add_argument(
        "--budget-seconds",
        type=int,
        help="override the hard wall-clock limit for smoke/standard runs",
    )
    reproduce.add_argument(
        "--state-file",
        type=Path,
        help="persistent batch state; completed adapter/seed pairs are resumed",
    )
    reproduce.add_argument(
        "--write-manifest",
        type=Path,
        help="write the canonical normalized paper manifest and exit",
    )
    reproduce.add_argument(
        "--include-concept-demos",
        action="store_true",
        help="include adapters whose core paper model/training is still a proxy",
    )


def run(args):
    from auto_research.reproductions.base import ReproductionFidelity
    from concurrent.futures import ThreadPoolExecutor
    from auto_research.cli_commands.common import _load_batch_state
    from auto_research.cli_commands.common import _run_reproduction
    from auto_research.cli_commands.common import _write_batch_state
    from auto_research.cli_commands.common import _write_reproduction_batch_summary
    from concurrent.futures import as_completed
    import datetime as dt
    from auto_research.reproductions.registry import get_adapter
    from auto_research.reproductions.registry import list_adapters
    import sys
    from auto_research.reproductions.reporting import write_legacy_combined_report
    from auto_research.reproductions.manifest import write_manifest
    from auto_research.reproductions.reporting import write_reproduction_result

    all_adapters = list(list_adapters())
    if args.write_manifest:
        print(write_manifest(args.write_manifest, all_adapters).resolve())
        return 0
    adapters = (
        [
            adapter
            for adapter in all_adapters
            if args.include_concept_demos
            or adapter.fidelity is not ReproductionFidelity.CONCEPT_DEMO
        ]
        if args.paper == "all"
        else [get_adapter(args.paper)]
    )
    adapters = [
        adapter
        for adapter in adapters
        if (not args.track or adapter.paper.track == args.track)
        and (
            not args.topic
            or any(args.topic.lower() in topic.lower() for topic in adapter.paper.topics)
        )
        and (
            not args.organization
            or args.organization.lower() in (adapter.paper.organization or "").lower()
        )
        and (not args.fidelity or adapter.fidelity.value == args.fidelity)
    ]
    if not adapters:
        raise ValueError("no reproduction adapters match the requested filters")
    for adapter in adapters:
        if adapter.fidelity is ReproductionFidelity.CONCEPT_DEMO:
            print(
                f"warning: {adapter.key} is a concept demo, not a paper reproduction; "
                "its result must not be compared with the paper's reported lift.",
                file=sys.stderr,
            )
    explicit_seeds = tuple(int(value.strip()) for value in args.seeds.split(",") if value.strip())
    seeds_by_adapter = {
        adapter.key: (
            explicit_seeds or ((args.seed,) if args.seed is not None else adapter.default_seeds)
        )
        for adapter in adapters
    }
    state = _load_batch_state(args.state_file)
    adapters_by_key = {adapter.key: adapter for adapter in adapters}
    prior_entries = [
        (adapters_by_key[key.split(":", 1)[0]], completed["result"])
        for key, completed in state["completed"].items()
        if key.split(":", 1)[0] in adapters_by_key and isinstance(completed.get("result"), dict)
    ]
    pending = [
        (adapter, seed)
        for adapter in adapters
        for seed in seeds_by_adapter[adapter.key]
        if f"{adapter.key}:{seed}" not in state["completed"]
    ]
    if not pending:
        print("All requested adapter/seed pairs are already completed in the state file.")
        return 0
    entries = []
    workers = max(1, min(args.workers, len(pending) or 1))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(
                _run_reproduction,
                adapter,
                args.dataset_dir,
                seed,
                (seed,),
                args.budget,
                args.budget_seconds,
            ): (adapter, seed)
            for adapter, seed in pending
        }
        for future in as_completed(futures):
            adapter, seed = futures[future]
            result = future.result()
            entries.append((adapter, result))
    entries.sort(key=lambda item: (item[0].key, item[1].get("seed", 0)))
    if args.output:
        report = write_legacy_combined_report(entries, args.output)
        print(f"Report: {report.resolve()}")
    else:
        for adapter, result in entries:
            report = write_reproduction_result(
                adapter,
                result,
                args.output_dir,
                seeds=(result["seed"],),
                dataset_dir=args.dataset_dir,
                budget=args.budget,
            )
            print(f"{adapter.key}: {report.resolve()}")
        if any(len(values) > 1 for values in seeds_by_adapter.values()):
            summary = _write_reproduction_batch_summary(
                [*prior_entries, *entries],
                args.output_dir,
                seeds_by_adapter,
                args.budget,
            )
            print(f"Batch summary: {summary.resolve()}")
    for adapter, result in entries:
        state["completed"][f"{adapter.key}:{result['seed']}"] = {
            "completed_at": dt.datetime.now().isoformat(),
            "result": result,
        }
    _write_batch_state(args.state_file, state)
    return 0
