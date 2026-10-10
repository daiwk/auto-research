"""Public thirteen-task capability protocol; never substitutes open NanoJev for Jev."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.system_one.capability_bench import evaluate_capability
from auto_research.system_one.capability_data import DATASETS, export_dataset, load_capability_data
from auto_research.system_one.nanojev import NanoJevProvider, NANOJEV_REVISION
from auto_research.system_one.providers import TypeSafeHTTPProvider


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare", help="download an immutable official labeled split")
    prepare.add_argument("--benchmark", choices=tuple(DATASETS), required=True)
    prepare.add_argument("--config", required=True)
    prepare.add_argument("--language", required=True)
    prepare.add_argument("--revision", required=True)
    prepare.add_argument("--split", choices=("test", "validation"), default="test")
    prepare.add_argument("--limit", type=int)
    prepare.add_argument("--output", type=Path, required=True)
    run = commands.add_parser("evaluate")
    run.add_argument("--data", type=Path, nargs="+", required=True)
    run.add_argument("--backend", choices=("nanojev", "typesafe"), required=True)
    run.add_argument("--checkpoint-dir", type=Path)
    run.add_argument("--device", default="cuda:0")
    run.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        report = export_dataset(args.benchmark, args.config, args.language, args.revision,
                                args.output, split=args.split, limit=args.limit)
    else:
        items, sources = load_capability_data(args.data)
        if args.backend == "nanojev":
            if args.checkpoint_dir is None:
                parser.error("NanoJev requires --checkpoint-dir; no implicit checkpoint download")
            provider = NanoJevProvider.from_checkpoint(args.checkpoint_dir, allow_download=False,
                                                      device=args.device)
        else:
            provider = TypeSafeHTTPProvider()
        report = evaluate_capability(provider, items)
        report.update(domain="system-one", method="jev-capability", dataset_sources=sources,
                      backend=args.backend, checkpoint_revision=NANOJEV_REVISION
                      if args.backend == "nanojev" else "provider-managed",
                      closed_jev_reproduction=args.backend == "typesafe",
                      diagnostic_only=any(source.get("limit") for source in sources),
                      selection="fixed backend; no evaluation-based tuning")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "predictions"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
