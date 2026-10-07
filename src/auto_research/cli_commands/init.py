from __future__ import annotations


def configure(commands):
    from pathlib import Path

    init = commands.add_parser("init", help="write an editable example configuration")
    init.add_argument("path", type=Path, nargs="?", default=Path("research.json"))
    init.add_argument("--track", choices=["llm", "recommendation"], default="llm")


def run(args):
    from auto_research.cli_commands.common import _init_config

    _init_config(args.path, args.track)
    print(f"Created {args.path}")
    return 0
