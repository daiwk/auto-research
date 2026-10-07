from __future__ import annotations


def configure(commands):
    from pathlib import Path

    publish = commands.add_parser("publish", help="commit a report and open a GitHub PR")
    publish.add_argument("report", type=Path)
    publish.add_argument("--title", required=True)
    publish.add_argument("--base")
    publish.add_argument("--ready", action="store_true")


def run(args):
    from auto_research.publish import publish_report

    print(publish_report(args.report, args.title, args.base, args.ready))
    return 0
