#!/usr/bin/env python3
"""Produce a review queue from the repository's auditable query matrix."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from auto_research.discovery import (
    build_discovery_payload,
    discover_candidates,
    queries_for_track,
    render_discovery_summary,
    repository_paper_statuses,
    triage_candidates,
)
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
    parser.add_argument("--summary-output")
    parser.add_argument("--github-actions", action="store_true")
    parser.add_argument("--manifest", default="docs/research-manifest.json")
    parser.add_argument("--ledger", default="docs/paper-discovery-ledger.json")
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
    statuses = repository_paper_statuses(Path(args.manifest), Path(args.ledger))
    candidates = triage_candidates(papers, statuses)
    payload = build_discovery_payload(
        track=args.track,
        start_date=start_date,
        end_date=args.end_date,
        query_names=(query.name for query in queries),
        candidates=candidates,
    )
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    if args.summary_output:
        Path(args.summary_output).write_text(render_discovery_summary(payload), encoding="utf-8")
    priority_count = payload["triage_counts"]["google_meta_priority_review"]
    if args.github_actions and priority_count:
        print(
            f"::warning title=Google/Meta paper review::"
            f"{priority_count} new priority candidate(s) require full-text review"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
