from __future__ import annotations

import datetime as dt
import hashlib
import json
from dataclasses import asdict
import re
import time
from collections.abc import Iterable
from pathlib import Path
import urllib.parse
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

from .models import Paper

ARXIV_API = "https://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}


class ArxivClient:
    """Small dependency-free arXiv client, sorted by newest submission."""

    def __init__(
        self,
        timeout: int = 30,
        user_agent: str = "auto-research/0.1",
        minimum_interval_seconds: float = 3.0,
        maximum_retries: int = 3,
        retry_backoff_seconds: float = 3.0,
        cache_dir: Path | None = None,
        checkpoint_dir: Path | None = None,
        resume: bool = False,
    ):
        self.timeout = timeout
        self.user_agent = user_agent
        self.minimum_interval_seconds = minimum_interval_seconds
        self.maximum_retries = maximum_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.cache_dir = cache_dir
        self.checkpoint_dir = checkpoint_dir
        self.resume = resume
        self.query_reports: list[dict] = []
        self.cache_fallbacks: list[str] = []
        self._last_request_at: float | None = None

    def search(
        self,
        query: str,
        limit: int = 8,
        categories: tuple[str, ...] = (),
        *,
        start: int = 0,
        match: str = "all",
        date_from: dt.date | None = None,
        date_to: dt.date | None = None,
    ) -> list[Paper]:
        if limit <= 0:
            return []
        terms = re.findall(r"[A-Za-z0-9][A-Za-z0-9_.+-]*", query)[:8]
        if match not in {"all", "any"}:
            raise ValueError("match must be 'all' or 'any'")
        operator = " AND " if match == "all" else " OR "
        search_query = operator.join(f'all:"{term}"' for term in terms)
        if categories:
            category_query = " OR ".join(f"cat:{category}" for category in categories)
            search_query = f"({search_query}) AND ({category_query})"
        if not search_query:
            raise ValueError("paper query contains no searchable terms")
        if date_from is not None and date_to is not None:
            if date_from > date_to:
                raise ValueError("search start must not exceed end")
            search_query = (
                f"({search_query}) AND submittedDate:"
                f"[{date_from:%Y%m%d}0000 TO {date_to:%Y%m%d}2359]"
            )
        params = urllib.parse.urlencode(
            {
                "search_query": search_query,
                "start": start,
                "max_results": limit,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
        )
        request = urllib.request.Request(
            f"{ARXIV_API}?{params}", headers={"User-Agent": self.user_agent}
        )
        if self._last_request_at is not None and self.minimum_interval_seconds > 0:
            elapsed = time.monotonic() - self._last_request_at
            if elapsed < self.minimum_interval_seconds:
                time.sleep(self.minimum_interval_seconds - elapsed)
        payload = self._read(request)
        return parse_arxiv_feed(payload)

    def search_pages(
        self,
        query: str,
        *,
        categories: tuple[str, ...] = (),
        page_size: int = 50,
        maximum_results: int = 200,
        match: str = "all",
        date_from: dt.date | None = None,
        date_to: dt.date | None = None,
        tolerate_failures: bool = False,
    ) -> list[Paper]:
        """Retrieve more than one arXiv page and de-duplicate versioned IDs.

        Discovery must not silently equate the first handful of search results
        with full coverage.  The bounded pagination keeps interactive searches
        cheap while allowing audit jobs to use a materially wider candidate
        pool than :meth:`search`'s UI-oriented default.
        """
        if page_size <= 0 or maximum_results <= 0:
            raise ValueError("page_size and maximum_results must be positive")
        identity = dict(
            query=query,
            categories=list(categories),
            match=match,
            page_size=page_size,
            maximum_results=maximum_results,
            date_from=str(date_from),
            date_to=str(date_to),
            scan_id=getattr(self, "scan_id", None),
        )
        digest = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
        path = self.checkpoint_dir / f"{digest}.json" if self.checkpoint_dir else None
        report = {
            **identity,
            "fingerprint": digest,
            "next_offset": 0,
            "state": "pending",
            "coverage_complete": False,
            "transport_complete": True,
            "cache_fallback_pages": 0,
            "pages": 0,
            "resumed": False,
        }
        papers: list[Paper] = []
        seen: set[str] = set()
        if self.resume and path is not None and path.is_file():
            saved = json.loads(path.read_text(encoding="utf-8"))
            if saved.get("identity") != identity:
                raise ValueError("discovery checkpoint identity mismatch")
            report.update(saved["report"])
            report["resumed"] = True
            papers = [Paper(**row) for row in saved["papers"]]
            seen = {canonical_arxiv_id(paper.arxiv_id) for paper in papers}
            if report["state"] == "exhausted":
                self.query_reports.append(report)
                return papers

        def checkpoint():
            if path is not None:
                from .discovery_checkpoint import atomic_json

                atomic_json(
                    path,
                    {
                        "identity": identity,
                        "report": report,
                        "papers": [asdict(paper) for paper in papers],
                    },
                )

        start_offset = report["next_offset"]
        if report["state"] == "capped":
            self.query_reports.append(report)
            return papers
        report.update(state="running", transport_complete=True, error=None)
        for start in range(start_offset, maximum_results, page_size):
            requested = min(page_size, maximum_results - start)
            fallbacks = len(self.cache_fallbacks)
            try:
                kwargs = dict(start=start, match=match)
                if date_from is not None:
                    kwargs["date_from"] = date_from
                if date_to is not None:
                    kwargs["date_to"] = date_to
                page = self.search(query, requested, categories, **kwargs)
            except (OSError, ValueError, ET.ParseError) as exc:
                report.update(
                    state="failed", transport_complete=False, error=f"{type(exc).__name__}: {exc}"
                )
                checkpoint()
                self.query_reports.append(report)
                if not tolerate_failures:
                    raise
                return papers
            cached = len(self.cache_fallbacks) > fallbacks
            if cached:
                report.update(
                    state="cached",
                    transport_complete=False,
                    cache_fallback_pages=report["cache_fallback_pages"] + 1,
                )
                checkpoint()
            for paper in page:
                paper_identity = canonical_arxiv_id(paper.arxiv_id)
                if paper_identity not in seen:
                    seen.add(paper_identity)
                    papers.append(paper)
            if cached:
                break
            report["pages"] += 1
            report["next_offset"] = start + len(page)
            if len(page) < requested:
                report.update(state="exhausted", coverage_complete=True)
                checkpoint()
                break
            report["state"] = "capped" if start + requested >= maximum_results else "running"
            checkpoint()
        self.query_reports.append(report)
        return papers

    def lookup(self, arxiv_ids: Iterable[str]) -> list[Paper]:
        """Resolve canonical IDs found by non-arXiv discovery sources."""
        identities = list(dict.fromkeys(canonical_arxiv_id(value) for value in arxiv_ids))
        if not identities:
            return []
        params = urllib.parse.urlencode(
            {"id_list": ",".join(identities), "max_results": len(identities)}
        )
        request = urllib.request.Request(
            f"{ARXIV_API}?{params}", headers={"User-Agent": self.user_agent}
        )
        if self._last_request_at is not None and self.minimum_interval_seconds > 0:
            elapsed = time.monotonic() - self._last_request_at
            if elapsed < self.minimum_interval_seconds:
                time.sleep(self.minimum_interval_seconds - elapsed)
        payload = self._read(request)
        return parse_arxiv_feed(payload)

    def _read(self, request: urllib.request.Request) -> bytes:
        """Read arXiv with bounded backoff for transient throttling.

        arXiv has also intermittently returned 406 for a previously valid query
        that succeeds unchanged on the next request.  Retrying it alongside
        429/5xx keeps
        every discovery entry point consistent and avoids four track-specific
        scripts each inventing a different recovery policy.
        """
        for attempt in range(self.maximum_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    payload = response.read()
                self._last_request_at = time.monotonic()
                self._write_cache(request.full_url, payload)
                return payload
            except urllib.error.HTTPError as exc:
                if exc.code not in {406, 429, 500, 502, 503, 504}:
                    raise
                if attempt >= self.maximum_retries:
                    return self._cached_or_raise(request.full_url, exc)
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                try:
                    delay = float(retry_after) if retry_after else 0.0
                except ValueError:
                    delay = 0.0
                delay = max(delay, self.retry_backoff_seconds * (2**attempt))
                time.sleep(delay)
            except (TimeoutError, urllib.error.URLError, ConnectionError):
                # A read timeout or a transient socket/DNS reset is as common
                # as HTTP 429 around arXiv announcement bursts.  Previously
                # these escaped immediately, aborting the entire four-track
                # discovery job before its bounded retry policy could help.
                if attempt >= self.maximum_retries:
                    return self._cached_or_raise(request.full_url, None)
                time.sleep(self.retry_backoff_seconds * (2**attempt))
        raise AssertionError("unreachable")

    def _cache_path(self, url: str) -> Path | None:
        if self.cache_dir is None:
            return None
        digest = hashlib.sha256(url.encode("utf-8")).hexdigest()
        return self.cache_dir / f"{digest}.xml"

    def _write_cache(self, url: str, payload: bytes) -> None:
        path = self._cache_path(url)
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(".tmp")
        temporary.write_bytes(payload)
        temporary.replace(path)

    def _cached_or_raise(self, url: str, error: BaseException | None) -> bytes:
        path = self._cache_path(url)
        if path is not None and path.is_file():
            self.cache_fallbacks.append(url)
            return path.read_bytes()
        if error is not None:
            raise error
        raise urllib.error.URLError(
            "arXiv request exhausted retries and no cached page is available"
        )


def canonical_arxiv_id(arxiv_id: str) -> str:
    """Strip an arXiv version suffix without changing the numerical ID."""
    return re.sub(r"v\d+$", "", arxiv_id)


def deduplicate_papers(groups: Iterable[Iterable[Paper]]) -> list[Paper]:
    """Merge query results, retaining the newest metadata for each arXiv ID."""
    by_id: dict[str, Paper] = {}
    for group in groups:
        for paper in group:
            identity = canonical_arxiv_id(paper.arxiv_id)
            current = by_id.get(identity)
            if current is None or paper.published > current.published:
                by_id[identity] = paper
    return sorted(by_id.values(), key=lambda paper: paper.published, reverse=True)


def parse_arxiv_feed(payload: bytes) -> list[Paper]:
    root = ET.fromstring(payload)
    papers: list[Paper] = []
    for entry in root.findall("atom:entry", NS):
        url = _text(entry, "atom:id")
        if "api/errors" in url or _text(entry, "atom:title").lower() == "error":
            raise ValueError("arXiv API error: " + _text(entry, "atom:summary"))
        papers.append(
            Paper(
                title=" ".join(_text(entry, "atom:title").split()),
                abstract=" ".join(_text(entry, "atom:summary").split()),
                authors=[_text(author, "atom:name") for author in entry.findall("atom:author", NS)],
                published=_text(entry, "atom:published"),
                url=url,
                arxiv_id=url.rstrip("/").split("/")[-1],
            )
        )
    return papers


def freshness_note(papers: list[Paper]) -> str:
    if not papers:
        return "No papers were retrieved; the experiment continued offline."
    newest = papers[0].published[:10]
    age = (dt.date.today() - dt.date.fromisoformat(newest)).days
    return f"Newest retrieved arXiv submission: {newest} ({age} days old)."


def _text(node: ET.Element, path: str) -> str:
    child = node.find(path, NS)
    return child.text.strip() if child is not None and child.text else ""
