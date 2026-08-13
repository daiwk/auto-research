#!/usr/bin/env python3
"""Produce a review queue from the repository's auditable query matrix."""

from __future__ import annotations

import argparse
import datetime as dt
import json

from auto_research.discovery import discover_candidates, queries_for_track
from auto_research.papers import ArxivClient


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--track",
        choices=("recommendation", "foundation-model", "post-training", "agent"),
        default="recommendation",
    )
    window = parser.add_mutually_exclusive_group()
    window.add_argument("--start-date", type=dt.date.fromisoformat)
    window.add_argument("--lookback-days", type=int, default=14)
    parser.add_argument("--end-date", type=dt.date.fromisoformat, default=dt.date.today())
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--maximum-results-per-query", type=int, default=200)
    parser.add_argument("--output")
    args = parser.parse_args()
    start_date = args.start_date or args.end_date - dt.timedelta(days=args.lookback_days)
    queries = queries_for_track(args.track)
    papers = discover_candidates(
        ArxivClient(minimum_interval_seconds=3.0),
        queries,
        start_date=start_date,
        end_date=args.end_date,
        page_size=args.page_size,
        maximum_results_per_query=args.maximum_results_per_query,
    )
    payload = {
        "schema_version": 1,
        "track": args.track,
        "window": {"start": str(start_date), "end": str(args.end_date)},
        "query_matrix": [query.name for query in queries],
        "candidate_count": len(papers),
        "candidates": [paper.to_dict() for paper in papers],
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
