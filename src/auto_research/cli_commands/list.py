from __future__ import annotations


def configure(commands):

    commands.add_parser("list", help="list installed paper/idea plugins")


def run(args):
    from auto_research.reproductions.registry import list_adapters

    for adapter in list_adapters():
        print(
            f"{adapter.key:20} {adapter.fidelity.value:16} "
            f"{adapter.paper.arxiv_id:12} {adapter.paper.title}"
        )
    return 0
