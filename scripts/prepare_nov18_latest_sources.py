"""Capture date-overlapping arXiv metadata and current official bulletins.

This is recall, not method review, affiliation verification or an implementation
queue. Raw captures remain in the local cache; bounded receipts are publishable.
"""

from __future__ import annotations

from dataclasses import asdict
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request

from auto_research.discovery import repository_paper_records
from auto_research.discovery_announcements import parse_bulletin
from auto_research.discovery_sources import fetch_text
from auto_research.papers import ARXIV_API, ArxivClient, canonical_arxiv_id, parse_arxiv_feed

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov18-latest"
CATEGORIES = ("cs.IR", "cs.CL", "cs.LG", "cs.AI", "cs.CV", "cs.RO", "cs.SE", "cs.SD", "cs.DC")


def write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def main():
    global CACHE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default="2026-11-16")
    parser.add_argument("--end", default="2026-11-18")
    parser.add_argument("--overlap-start", default="2026-11-13")
    parser.add_argument("--cache-dir", type=Path, default=CACHE)
    args = parser.parse_args()
    if not args.overlap_start <= args.start <= args.end:
        parser.error("overlap-start <= start <= end required")
    for value in (args.start, args.end, args.overlap_start):
        datetime.strptime(value, "%Y-%m-%d")
    CACHE = args.cache_dir.resolve()
    CACHE.mkdir(parents=True, exist_ok=True)
    client = ArxivClient(minimum_interval_seconds=3, maximum_retries=2, cache_dir=CACHE / "arxiv")
    query = " OR ".join("cat:" + category for category in CATEGORIES)
    floor = args.overlap_start + "T00:00:00"
    found, receipts, exhausted = {}, [], False
    for start in range(0, 10000, 200):
        params = {
            "search_query": "(" + query + ")",
            "start": start,
            "max_results": 200,
            "sortBy": "lastUpdatedDate",
            "sortOrder": "descending",
        }
        url = ARXIV_API + "?" + urlencode(params)
        try:
            raw = client._read(Request(url, headers={"User-Agent": client.user_agent}))
            rows = parse_arxiv_feed(raw)
        except (OSError, ValueError) as error:
            receipts.append({"source_url": url, "error": str(error), "transport_complete": False})
            break
        raw_path = CACHE / "captures" / f"updated-{start}.xml"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(raw if isinstance(raw, bytes) else raw.encode())
        digest = sha256(raw_path.read_bytes()).hexdigest()
        receipts.append(
            {
                "source_url": url,
                "capture": raw_path.relative_to(ROOT).as_posix(),
                "sha256": digest,
                "entries": len(rows),
                "transport_complete": True,
            }
        )
        for paper in rows:
            if (paper.updated or paper.published) >= floor:
                found[canonical_arxiv_id(paper.arxiv_id)] = asdict(paper)
        print("metadata page", start, "entries", len(rows), "retained", len(found), flush=True)
        if len(rows) < 200 or (rows and all((p.updated or p.published) < floor for p in rows)):
            exhausted = True
            break
    known = repository_paper_records(
        ROOT / "docs/research-manifest.json", ROOT / "docs/paper-discovery-ledger.json"
    )
    for identity, row in found.items():
        row["canonical_id"] = identity
        row["repository_status"] = known.get(identity, {}).get("repository_status", "new")
    write(
        CACHE / "metadata-pool.json",
        {
            "schema_version": 1,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "requested_window": {"start": args.start, "end": args.end},
            "overlap_start_utc": floor,
            "categories": CATEGORIES,
            "metadata_only": True,
            "coverage_complete_to_overlap_boundary": exhausted,
            "all_sources_exhaustive": False,
            "receipts": receipts,
            "papers": list(found.values()),
        },
    )
    announcements, bulletin_receipts = {}, []
    for category in CATEGORIES:
        url = f"https://arxiv.org/list/{category}/new?show=2000"
        try:
            raw = fetch_text(url)
            path = CACHE / "captures" / f"{category}-new.html"
            path.write_text(raw)
            entries, report = parse_bulletin(raw)
            bulletin_receipts.append(
                report | {"source_url": url, "capture": path.relative_to(ROOT).as_posix()}
            )
            for entry in entries:
                identity = canonical_arxiv_id(entry.arxiv_id)
                announcements.setdefault(identity, []).append(
                    {
                        "category": category,
                        "announced_on": report["announced_on"],
                        "entry_kind": entry.entry_kind,
                        "arxiv_id": entry.arxiv_id,
                    }
                )
        except (OSError, ValueError) as error:
            bulletin_receipts.append(
                {"source_url": url, "parse_complete": False, "error": str(error)}
            )
    write(
        CACHE / "announcement-pool.json",
        {"metadata_only": True, "receipts": bulletin_receipts, "identities": announcements},
    )
    print(
        "captured",
        len(found),
        "metadata identities and",
        len(announcements),
        "current bulletin identities",
        flush=True,
    )


if __name__ == "__main__":
    main()
