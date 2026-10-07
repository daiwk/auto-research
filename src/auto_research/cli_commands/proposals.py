from __future__ import annotations


def configure(commands):
    from pathlib import Path

    proposals = commands.add_parser("proposals", help="create auditable paper-to-experiment plans")
    proposals.add_argument("action", choices=["create"])
    proposals.add_argument("--paper")
    proposals.add_argument("--spec", type=Path, help="paper.yaml for a newly retrieved paper")
    proposals.add_argument("--model", required=True)
    proposals.add_argument("--protocol", required=True)
    proposals.add_argument("--direction", default="")
    proposals.add_argument("--source", default="installed-paper-component")
    proposals.add_argument("--operators", default="")
    proposals.add_argument("--output", type=Path, default=Path("runs/proposal.json"))


def run(args):
    from pathlib import Path
    from auto_research.experiment_proposals import find_paper_spec
    from auto_research.experiment_proposals import propose_from_paper
    from auto_research.experiment_proposals import write_proposal

    if not args.paper and not args.spec:
        raise ValueError("proposals create requires --paper or --spec")
    from auto_research.paper_specs import load_spec

    spec = load_spec(args.spec) if args.spec else find_paper_spec(Path.cwd(), args.paper)
    operators = tuple(value.strip() for value in args.operators.split(",") if value.strip())
    proposal = propose_from_paper(
        spec,
        model=args.model,
        protocol_id=args.protocol,
        direction=args.direction,
        source_kind=args.source,
        operators=operators or None,
    )
    print(write_proposal(proposal, args.output).resolve())
    return 0
