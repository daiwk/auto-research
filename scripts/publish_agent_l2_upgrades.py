#!/usr/bin/env python3
"""Publish selected ToolRoute L2.1 runs into paper pages and the shared summary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_DIRS = {
    "jit-agent": "2608.25593-jit-agent",
    "traceml": "2608.26086-traceml",
    "adavdr": "2608.25559-adavdr",
    "topas": "2608.25523-topas",
    "caskg": "2608.25500-caskg",
    "progrouter": "2608.25992-progrouter",
}


def publish(source: Path) -> None:
    summary_path = ROOT / "docs/experiments/agent-toolroute-l2-seeds42-44.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    for method, paper_dir in PAPER_DIRS.items():
        source_path = source / f"{method}-toolroute-l21-seeds42-43-44/metrics.json"
        payload = json.loads(source_path.read_text(encoding="utf-8"))
        relative = Path("docs/agent-research") / paper_dir / "metrics/toolroute-l2-seeds42-44.json"
        payload["provenance"]["artifact_path"] = relative.as_posix()
        destination = ROOT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        summary["results"][method] = {
            "metrics": payload["metrics"],
            "aggregate_metrics": payload["aggregate_metrics"],
            "artifact_path": relative.as_posix(),
        }
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    publish(args.source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
