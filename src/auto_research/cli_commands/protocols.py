from __future__ import annotations


def configure(commands):
    from pathlib import Path

    protocols = commands.add_parser("protocols", help="inspect fair-evaluation protocols")
    protocols.add_argument("action", choices=["list", "show", "compare"])
    protocols.add_argument("--id")
    protocols.add_argument("--left", type=Path)
    protocols.add_argument("--right", type=Path)


def run(args):
    from auto_research.protocols import comparability_errors
    from auto_research.protocols import get_protocol
    import json
    from auto_research.protocols import list_protocols

    if args.action == "list":
        for protocol in list_protocols():
            print(f"{protocol.protocol_id:36} {protocol.dataset:20} {protocol.primary_metric}")
        return 0
    if args.action == "show":
        if not args.id:
            raise ValueError("protocols show requires --id")
        print(json.dumps(get_protocol(args.id).to_dict(), ensure_ascii=False, indent=2))
        return 0
    if not args.left or not args.right:
        raise ValueError("protocols compare requires --left and --right")
    errors = comparability_errors(
        json.loads(args.left.read_text()), json.loads(args.right.read_text())
    )
    if errors:
        raise ValueError("not comparable: " + "; ".join(errors))
    print("comparable")
    return 0
