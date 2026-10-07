from __future__ import annotations


def configure(commands):

    stats = commands.add_parser("stats", help="make a paired, sequential experiment decision")
    stats.add_argument("action", choices=["decide"])
    stats.add_argument("--baseline", required=True)
    stats.add_argument("--candidate", required=True)
    stats.add_argument("--minimum-effect", type=float, default=0.0)
    stats.add_argument("--alpha", type=float, default=0.05)
    stats.add_argument("--maximum-seeds", type=int, default=9)
    stats.add_argument("--estimated-cost", type=float, default=0.0)
    stats.add_argument("--maximum-cost", type=float)
    stats.add_argument("--minimize", action="store_true")


def run(args):
    from auto_research.evolution.statistics import decide_experiment
    import json

    values = lambda text: tuple(float(value) for value in text.split(",") if value.strip())
    decision = decide_experiment(
        values(args.baseline),
        values(args.candidate),
        minimum_effect=args.minimum_effect,
        alpha=args.alpha,
        maximum_seeds=args.maximum_seeds,
        estimated_cost=args.estimated_cost,
        maximum_cost=args.maximum_cost,
        maximize=not args.minimize,
    )
    print(json.dumps(decision.to_dict(), ensure_ascii=False, indent=2))
    return 0
