#!/usr/bin/env python3
"""Freeze explicitly reviewed static official lists for future daily deltas."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from auto_research.discovery_sources import (
    DiscoverySource, fetch_text, page_url, publication_records,
)


def build_snapshot(artifact: dict, config: dict, *, checked_at: str) -> dict:
    policies = {
        source["name"]: source.get("review_policy", "incremental")
        for source in config.get("sources", [])
    }
    sources = {}
    for stat in artifact.get("cross_source", {}).get("source_stats", []):
        name = stat["source"]
        if policies.get(name) != "snapshot":
            continue
        titles = set(stat.get("snapshot_publication_titles", [])) or {
            item["title"] for item in stat.get("unresolved_publications", [])
        }
        sources[name] = sorted(titles, key=str.casefold)
    return _snapshot_payload(sources, checked_at=checked_at)


def _snapshot_payload(sources: dict[str, list[str]], *, checked_at: str) -> dict:
    return {
        "schema_version": 1,
        "checked_at": checked_at,
        "note": (
            "Static conference inventory baseline only. A title in this file is not an "
            "acceptance or reproduction decision; subsequent additions remain reviewable."
        ),
        "sources": dict(sorted(sources.items())),
    }


def fetch_static_snapshot(config: dict, *, checked_at: str) -> dict:
    sources = {}
    for raw in config.get("sources", []):
        source = DiscoverySource(**raw)
        if source.review_policy != "snapshot":
            continue
        titles = set()
        for page in range(1, source.max_pages + 1):
            url = source.url if page == 1 else page_url(source.url, page)
            titles.update(
                title for title, _, _ in publication_records(source, fetch_text(url))
            )
        sources[source.name] = sorted(titles, key=str.casefold)
    return _snapshot_payload(sources, checked_at=checked_at)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--fetch-static", action="store_true")
    parser.add_argument(
        "--config", type=Path, default=Path("configs/paper-discovery-sources.json")
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--checked-at", default=dt.date.today().isoformat())
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.fetch_static:
        payload = fetch_static_snapshot(config, checked_at=args.checked_at)
    elif args.artifact:
        payload = build_snapshot(
            json.loads(args.artifact.read_text(encoding="utf-8")),
            config,
            checked_at=args.checked_at,
        )
    else:
        parser.error("provide --artifact or --fetch-static")
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
