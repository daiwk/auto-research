"""Capture a bounded official Google/Meta directory delta, not a paper census."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import argparse
from datetime import datetime, timezone
import gzip
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov18-latest/priority"
AUDIT = ROOT / "docs/research-audits/nov18-latest"


def paper_links(links):
    """Google mixes absolute detail URLs with relative navigation links."""
    normalized = {url.removeprefix("https://research.google") for url in links}
    return {url for url in normalized if re.fullmatch(r"/pubs/[^/?]+/", url)}


def directory_delta(baseline, current, *, comparison_complete):
    """Observed additions survive partial recall; missing pages prove no removal."""
    return {
        "baseline_urls": len(baseline), "current_urls": len(current),
        "comparison_complete": comparison_complete,
        "added": sorted(current - baseline),
        "removed": sorted(baseline - current) if comparison_complete else [],
        "unobserved_baseline_urls": len(baseline - current),
    }


def html_bytes(raw):
    """Decode transport gzip without changing the retained response bytes."""
    return gzip.decompress(raw) if raw.startswith(b"\x1f\x8b") else raw


class DirectoryLinks(HTMLParser):
    """Read link inventories without optional scraping dependencies."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = set()
        self.has_html = False

    def handle_starttag(self, tag, attrs):
        if tag == "html":
            self.has_html = True
        if tag == "a":
            for key, value in attrs:
                if key == "href" and value is not None:
                    self.links.add(value)
                    break

    handle_startendtag = handle_starttag


def parsed_capture_fields(raw):
    decoded = html_bytes(raw)
    parser = DirectoryLinks()
    parser.feed(decoded.decode("utf-8-sig", errors="replace"))
    parser.close()
    links = sorted(parser.links)
    return {"links": links, "decoded_sha256": hashlib.sha256(decoded).hexdigest(),
            "transport_gzip_decoded": decoded is not raw,
            "parse_complete": parser.has_html and bool(links)}


def refresh_capture(row):
    """Reparse this exact cached response; never infer empty from a failure."""
    if "capture" not in row:
        return row
    try:
        raw = (CACHE / row["capture"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError("cached response fingerprint changed")
        return row | parsed_capture_fields(raw)
    except Exception as error:
        return row | {"parse_complete": False, "status": "source_exception_archived",
                      "blocking": False, "automatic_retry": False, "error_type": type(error).__name__}


def capture(url):
    name = hashlib.sha256(url.encode()).hexdigest()[:20] + ".html"
    try:
        with urlopen(
            Request(url, headers={"User-Agent": "auto-research/primary-source-review"}), timeout=30
        ) as response:
            raw = response.read()
            status = response.status
        (CACHE / name).write_bytes(raw)
        return {
            "url": url,
            "http_status": status,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
            "capture": name,
            **parsed_capture_fields(raw),
        }
    except Exception as error:
        return {
            "url": url,
            "status": "source_exception_archived",
            "blocking": False,
            "automatic_retry": False,
            "error_type": type(error).__name__,
        }


def main():
    global CACHE, AUDIT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default="2026-11-16")
    parser.add_argument("--end", default="2026-11-18")
    parser.add_argument("--cache-dir", type=Path, default=CACHE)
    parser.add_argument("--audit-dir", type=Path, default=AUDIT)
    parser.add_argument(
        "--reconcile-captures",
        action="store_true",
        help="Reparse this run's actual captures without repeating network requests",
    )
    args = parser.parse_args()
    if args.start > args.end:
        parser.error("start <= end required")
    for value in (args.start, args.end):
        datetime.strptime(value, "%Y-%m-%d")
    CACHE, AUDIT = args.cache_dir.resolve(), args.audit_dir.resolve()
    CACHE.mkdir(parents=True, exist_ok=True)
    AUDIT.mkdir(parents=True, exist_ok=True)
    old = {
        org: json.loads(
            (
                ROOT / f"docs/research-audits/nov15-review-closure/{org}-source-review.json"
            ).read_text()
        )
        for org in ("google", "meta")
    }
    urls = sorted(
        {
            row["url"]
            for group in old.values()
            for row in group["pages"]
            if "research.google/pubs/?" in row["url"] or "ai.meta.com/results/?" in row["url"]
        }
    )
    urls += [
        "https://research.google/blog/2026/11/",
        "https://deepmind.google/research/publications/",
        "https://deepmind.google/blog/",
        "https://ai.meta.com/research/",
        "https://ai.meta.com/research/publications/",
    ]
    previous = None
    if args.reconcile_captures:
        previous = json.loads((AUDIT / "priority-source-captures.json").read_text())
        captures = [refresh_capture(row) for row in previous["pages"]]
    else:
        with ThreadPoolExecutor(max_workers=4) as pool:
            captures = list(pool.map(capture, urls))
    baseline = set()
    current = set()
    for page in old["google"]["pages"]:
        if "research.google/pubs/?" not in page["url"]:
            continue
        cached = ROOT / ".cache/nov15-closure/google" / ("page-" + str(page["page"]) + ".html")
        if cached.exists():
            baseline.update(
                paper_links(parsed_capture_fields(cached.read_bytes())["links"])
            )
    # The exact old URL inventory also appears in records; use it when capture names differ.
    for row in old["google"]["records"]:
        url = row.get("url", "")
        if re.fullmatch(r"https://research.google/pubs/[^/?]+/", url):
            baseline.add(url.removeprefix("https://research.google"))
    # Earlier reviewed baseline records are not necessarily repeated in the latest delta.
    for cached in (ROOT / ".cache/nov15-closure/google").glob("*.html"):
        if not cached.name.startswith(("page", "directory", "google-page", "google-first")):
            continue
        baseline.update(
            paper_links(parsed_capture_fields(cached.read_bytes())["links"])
        )
    for row in captures:
        if "research.google/pubs/?" in row["url"]:
            current.update(paper_links(row.get("links", [])))
    added = sorted(current - baseline)
    with ThreadPoolExecutor(max_workers=4) as pool:
        detail_captures = list(
            pool.map(capture, ("https://research.google" + url for url in added))
        )
    repositories = previous["repository_events"] if previous else []
    for org in () if previous else ("google-research", "google-deepmind", "facebookresearch"):
        for event in ("created", "pushed"):
            query = f"org:{org} {event}:{args.start}..{args.end}"
            process = subprocess.run(
                [
                    "gh",
                    "api",
                    "-X",
                    "GET",
                    "search/repositories",
                    "-f",
                    "q=" + query,
                    "-f",
                    "per_page=100",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if process.returncode:
                repositories.append(
                    {
                        "organization": org,
                        "event": event,
                        "status": "source_exception_archived",
                        "blocking": False,
                        "automatic_retry": False,
                    }
                )
                continue
            raw = process.stdout.encode()
            data = json.loads(raw)
            (CACHE / f"{org}-{event}.json").write_bytes(raw)
            repositories.append(
                {
                    "organization": org,
                    "event": event,
                    "query": query,
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "total_count": data["total_count"],
                    "incomplete_results": data["incomplete_results"],
                    "items": [
                        {
                            k: item.get(k)
                            for k in (
                                "full_name",
                                "html_url",
                                "description",
                                "created_at",
                                "pushed_at",
                            )
                        }
                        for item in data["items"]
                    ],
                }
            )
    google_pages = [row for row in captures if "research.google/pubs/?" in row["url"]]
    comparable = bool(google_pages) and all(row.get("parse_complete") is True for row in google_pages)
    payload = {
        "schema_version": 1,
        "checked_on": args.end,
        "window": {"start": args.start, "end": args.end},
        "scope": "Fresh finite official directory and repository-event delta; not affiliation or method exhaustion.",
        "all_sources_exhaustive": False,
        "baseline": "nov15-review-closure/google-source-review.json",
        "baseline_sha256": hashlib.sha256(
            (
                ROOT / "docs/research-audits/nov15-review-closure/google-source-review.json"
            ).read_bytes()
        ).hexdigest(),
        "pages": captures,
        "google_directory_delta": directory_delta(baseline, current, comparison_complete=comparable),
        "added_details": detail_captures,
        "repository_events": repositories,
        "limitations": [
            "Official membership and familiar author names are recall signals, never byline proof.",
            "Repository push dates are not publication dates or evidence of a new algorithm.",
            "An unavailable directory is archived nonblocking, not evidence of zero new papers.",
            "A transport200 response without a valid parsed HTML link inventory is incomplete, not an empty directory. Raw compressed response hashes are preserved separately from decoded hashes.",
        ],
    }
    (AUDIT / "priority-source-captures.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "pages": len(captures),
                "google_added_urls": len(added),
                "repository_events": len(repositories),
            }
        )
    )


if __name__ == "__main__":
    main()
