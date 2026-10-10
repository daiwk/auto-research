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
    merge_external_candidates,
    paper_is_in_window,
)
from auto_research.discovery_sources import (
    DiscoverySource, catalog_papers_from_manifest, discover_external, load_sources,
    load_source_snapshots, official_review_queue,
)
from auto_research.papers import ArxivClient, canonical_arxiv_id
from auto_research.models import Paper
from auto_research.discovery_checkpoint import atomic_json, coverage_summary


def effective_start_date(
    requested_start: dt.date,
    *,
    announcement_overlap_days: int,
) -> dt.date:
    """Include the preceding arXiv submission day in a daily announcement scan.

    arXiv announces papers on the following business day, so a page labelled
    ``27 Aug`` normally contains records whose API ``published`` timestamp is
    ``26 Aug``.  The repository ledger de-duplicates the overlap.
    """
    if announcement_overlap_days < 0:
        raise ValueError("announcement-overlap-days must be non-negative")
    return requested_start - dt.timedelta(days=announcement_overlap_days)


def external_paper_in_window(
    paper: Paper, provenance: dict[str, list[dict]], *,
    start_date: dt.date, end_date: dt.date,
) -> bool:
    if paper_is_in_window(paper, start_date=start_date, end_date=end_date):
        return True
    return any(
        start_date <= dt.date.fromisoformat(item["source_published"]) <= end_date
        for item in provenance.get(canonical_arxiv_id(paper.arxiv_id), ())
        if item.get("source_published")
    )


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
    parser.add_argument(
        "--announcement-overlap-days",
        type=int,
        default=1,
        help=(
            "preceding submission days included to match arXiv announcement dates; "
            "ledger de-duplication keeps repeated records out of the new queue"
        ),
    )
    parser.add_argument("--page-size", type=int, default=50)
    parser.add_argument("--maximum-results-per-query", type=int, default=200)
    parser.add_argument(
        "--recall-mode", choices=("submission-window", "late-index"),
        default="submission-window",
        help="date-bounded primary scan; run late-index separately to retain ID-month backfill",
    )
    parser.add_argument("--output")
    parser.add_argument("--summary-output")
    parser.add_argument("--official-review-output")
    parser.add_argument("--checkpoint-dir", type=Path, help="persist each successful query page; use a separate directory per track/window")
    parser.add_argument("--resume", action="store_true", help="resume the exact saved window/query matrix")
    parser.add_argument("--github-actions", action="store_true")
    parser.add_argument("--manifest", default="docs/research-manifest.json")
    parser.add_argument("--ledger", default="docs/paper-discovery-ledger.json")
    parser.add_argument(
        "--arxiv-cache-dir", type=Path,
        default=Path(".cache/paper-discovery/arxiv"),
        help="successful arXiv pages are checkpointed here and reused only after transient failure",
    )
    parser.add_argument("--cross-source-config", type=Path)
    parser.add_argument(
        "--source-snapshots", type=Path,
        default=Path("configs/paper-discovery-source-snapshots.json"),
        help="approved baselines for static conference lists; only deltas enter daily review",
    )
    parser.add_argument(
        "--snowball-seeds", default="",
        help="comma-separated relevant arXiv IDs used for citation snowball",
    )
    parser.add_argument(
        "--author-page", action="append", default=[],
        help="author homepage URL; repeat for multiple first-author/maintainer sweeps",
    )
    parser.add_argument(
        "--github-page", action="append", default=[],
        help="author or project GitHub/API URL; repeat for multiple sources",
    )
    args = parser.parse_args()
    if args.resume and not args.checkpoint_dir:
        parser.error("--resume requires --checkpoint-dir")
    requested_start_date = args.start_date or args.end_date - dt.timedelta(days=args.lookback_days)
    start_date = effective_start_date(
        requested_start_date,
        announcement_overlap_days=args.announcement_overlap_days,
    )
    queries = queries_for_track(args.track)
    client = ArxivClient(
        minimum_interval_seconds=3.0,
        maximum_retries=5,
        retry_backoff_seconds=3.0,
        cache_dir=args.arxiv_cache_dir,
        checkpoint_dir=args.checkpoint_dir,
        resume=args.resume,
    )
    papers = discover_candidates(
        client,
        queries,
        start_date=start_date,
        end_date=args.end_date,
        page_size=args.page_size,
        maximum_results_per_query=args.maximum_results_per_query,
        recall_mode=args.recall_mode,
    )
    source_failures = []
    source_stats = []
    if args.cross_source_config or args.author_page or args.github_page or args.snowball_seeds:
        sources = (
            list(load_sources(args.cross_source_config, args.track))
            if args.cross_source_config else []
        )
        sources.extend(
            DiscoverySource(f"author-page-{index}", "author-page", url)
            for index, url in enumerate(args.author_page, start=1)
        )
        sources.extend(
            DiscoverySource(f"github-page-{index}", "github-page", url)
            for index, url in enumerate(args.github_page, start=1)
        )
        external, provenance, source_failures, source_stats = discover_external(
            sources,
            client=client,
            known_papers=(item.paper for item in papers),
            catalog_papers=catalog_papers_from_manifest(Path(args.manifest)),
            track=args.track,
            snowball_seeds=(
                value.strip() for value in args.snowball_seeds.split(",") if value.strip()
            ),
            source_snapshots=load_source_snapshots(args.source_snapshots),
        )
        external = [paper for paper in external if external_paper_in_window(
            paper, provenance, start_date=start_date, end_date=args.end_date,
        )]
        papers = merge_external_candidates(papers, external, provenance)
    statuses = repository_paper_statuses(Path(args.manifest), Path(args.ledger))
    candidates = triage_candidates(papers, statuses)
    payload = build_discovery_payload(
        track=args.track,
        start_date=start_date,
        end_date=args.end_date,
        query_names=(query.name for query in queries),
        candidates=candidates,
    )
    payload["requested_window"] = {
        "start": str(requested_start_date),
        "end": str(args.end_date),
    }
    payload["announcement_overlap_days"] = args.announcement_overlap_days
    payload["recall_mode"] = args.recall_mode
    review_queue = official_review_queue(
        source_stats, start_date=start_date, end_date=args.end_date,
    )
    payload["cross_source"] = {
        "enabled": bool(
            args.cross_source_config or args.author_page
            or args.github_page or args.snowball_seeds
        ),
        "config": str(args.cross_source_config) if args.cross_source_config else None,
        "source_failures": source_failures,
        "source_stats": source_stats,
        "coverage_complete": (
            bool(source_stats)
            and not source_failures
            and not review_queue
            and all(
                source.get("transport_status", source["status"]) == "ok"
                for source in source_stats
            )
            and not any(source.get("pagination_capped") for source in source_stats)
        ),
    }
    payload["cross_source"]["official_review_queue_count"] = len(review_queue)
    if args.official_review_output:
        Path(args.official_review_output).write_text(json.dumps({
            "schema_version": 1,
            "track": args.track,
            "window": {"start": str(start_date), "end": str(args.end_date)},
            "review_state": "identity_unresolved",
            "coverage_complete": payload["cross_source"]["coverage_complete"],
            "source_failures": source_failures,
            "items": review_queue,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        payload["cross_source"]["official_review_output"] = args.official_review_output
    payload["arxiv_transport"] = {
        **coverage_summary(client.query_reports),
        "cache_dir": str(args.arxiv_cache_dir),
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        atomic_json(Path(args.output), payload)
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
