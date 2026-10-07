from __future__ import annotations


def configure(commands):
    from pathlib import Path

    experiments = commands.add_parser(
        "experiments", help="index and browse experiment artifacts across all research domains"
    )
    experiments.add_argument("action", choices=["sync", "list", "dashboard", "pareto"])
    experiments.add_argument("--database", type=Path, default=Path("runs/experiments.sqlite"))
    experiments.add_argument("--roots", default="docs,runs")
    experiments.add_argument("--output", type=Path, default=Path("runs/experiment-dashboard.html"))
    experiments.add_argument("--domain")
    experiments.add_argument("--method")
    experiments.add_argument("--dataset")
    experiments.add_argument("--metric")
    experiments.add_argument("--x-metric")
    experiments.add_argument("--y-metric")
    experiments.add_argument("--maximize-x", action="store_true")
    experiments.add_argument("--minimize-y", action="store_true")


def run(args):
    from auto_research.experiment_store.store import ExperimentStore
    from pathlib import Path
    import json
    from auto_research.experiment_store.store import sync_experiments
    from auto_research.experiment_store.dashboard import write_dashboard

    roots = [Path(value.strip()) for value in args.roots.split(",") if value.strip()]
    if args.action == "sync":
        imported, failed = sync_experiments(args.database, roots)
        print(f"Indexed {imported} artifacts; skipped {failed} invalid artifacts")
        return 0 if not failed else 2
    if args.action == "dashboard":
        imported, failed = sync_experiments(args.database, roots)
        print(f"Indexed {imported} artifacts; skipped {failed} invalid artifacts")
        print(write_dashboard(args.database, args.output).resolve())
        return 0
    with ExperimentStore(args.database) as store:
        if args.action == "pareto":
            if not args.x_metric or not args.y_metric:
                raise ValueError("pareto requires --x-metric and --y-metric")
            rows = store.pareto_frontier(
                args.x_metric,
                args.y_metric,
                minimize_x=not args.maximize_x,
                minimize_y=args.minimize_y,
            )
        else:
            rows = store.rows(
                domain=args.domain,
                method=args.method,
                dataset=args.dataset,
                metric=args.metric,
            )
    for row in rows:
        print(
            json.dumps(
                {
                    "domain": row.domain,
                    "method": row.method,
                    "dataset": row.dataset,
                    "seed": row.seed,
                    "metrics": row.metrics,
                    "path": row.path,
                },
                ensure_ascii=False,
            )
        )
    return 0
