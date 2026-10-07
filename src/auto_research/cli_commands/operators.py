from __future__ import annotations


def configure(commands):
    from pathlib import Path

    operators = commands.add_parser(
        "operators", help="inspect and validate paper-derived Evolve operator combinations"
    )
    operators.add_argument("action", choices=["list", "check", "export"])
    operators.add_argument("--model")
    operators.add_argument("--operators", default="")
    operators.add_argument("--max-compute", type=int)
    operators.add_argument("--max-memory", type=int)
    operators.add_argument("--max-latency", type=int)
    operators.add_argument("--output", type=Path, default=Path("runs/operator-graph.json"))


def run(args):
    from auto_research.evolution.compatibility import operator_registry
    from auto_research.evolution.compatibility import validate_operator_set
    from auto_research.evolution.compatibility import write_compatibility_graph

    if args.action == "export":
        print(write_compatibility_graph(args.output).resolve())
        return 0
    if args.action == "list":
        for key, spec in sorted(operator_registry().items()):
            print(f"{key:32} {spec.domain:18} {spec.slot:14} {','.join(spec.compatible_models)}")
        return 0
    if not args.model:
        raise ValueError("operators check requires --model")
    values = [value.strip() for value in args.operators.split(",") if value.strip()]
    if not values:
        raise ValueError("operators check requires --operators")
    errors = validate_operator_set(
        args.model,
        values,
        max_compute=args.max_compute,
        max_memory=args.max_memory,
        max_latency=args.max_latency,
    )
    if errors:
        raise ValueError("; ".join(errors))
    print("compatible")
    return 0
