from __future__ import annotations


def configure(commands):
    from pathlib import Path

    candidate = commands.add_parser(
        "candidate", help="stage, verify or explicitly promote a generated evolve plugin"
    )
    candidate.add_argument("action", choices=["stage", "verify", "promote"])
    candidate.add_argument("--spec", type=Path)
    candidate.add_argument("--id")
    candidate.add_argument("--destination", type=Path)
    candidate.add_argument("--timeout", type=int, default=300)
    candidate.add_argument("--approve", action="store_true")


def run(args):
    from auto_research.evolution.promotion import CandidatePluginSpec
    from auto_research.evolution.promotion import CandidatePromotionPipeline
    from pathlib import Path
    import json

    pipeline = CandidatePromotionPipeline(Path.cwd())
    if args.action == "stage":
        if not args.spec:
            raise ValueError("candidate stage requires --spec")
        print(pipeline.stage(CandidatePluginSpec.from_file(args.spec)))
    elif args.action == "verify":
        if not args.id:
            raise ValueError("candidate verify requires --id")
        print(json.dumps(pipeline.verify(args.id, args.timeout), ensure_ascii=False))
    else:
        if not args.id or not args.destination:
            raise ValueError("candidate promote requires --id and --destination")
        print(pipeline.promote(args.id, args.destination, approved=args.approve))
    return 0
