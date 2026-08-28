from __future__ import annotations

import datetime as dt
import re
import time
from collections.abc import Iterable
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
        minimum_interval_seconds: float = 0.0,
        maximum_retries: int = 3,
        retry_backoff_seconds: float = 2.0,
    ):
        self.timeout = timeout
        self.user_agent = user_agent
        self.minimum_interval_seconds = minimum_interval_seconds
        self.maximum_retries = maximum_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self._last_request_at: float | None = None

    def search(
        self,
        query: str,
        limit: int = 8,
        categories: tuple[str, ...] = (),
        *,
        start: int = 0,
        match: str = "all",
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
    ) -> list[Paper]:
        """Retrieve more than one arXiv page and de-duplicate versioned IDs.

        Discovery must not silently equate the first handful of search results
        with full coverage.  The bounded pagination keeps interactive searches
        cheap while allowing audit jobs to use a materially wider candidate
        pool than :meth:`search`'s UI-oriented default.
        """
        if page_size <= 0 or maximum_results <= 0:
            return []
        papers: list[Paper] = []
        seen: set[str] = set()
        for start in range(0, maximum_results, page_size):
            requested = min(page_size, maximum_results - start)
            page = self.search(
                query,
                requested,
                categories,
                start=start,
                match=match,
            )
            for paper in page:
                identity = canonical_arxiv_id(paper.arxiv_id)
                if identity not in seen:
                    seen.add(identity)
                    papers.append(paper)
            if len(page) < requested:
                break
        return papers

    def lookup(self, arxiv_ids: Iterable[str]) -> list[Paper]:
        """Resolve canonical IDs found by non-arXiv discovery sources."""
        identities = list(dict.fromkeys(canonical_arxiv_id(value) for value in arxiv_ids))
        if not identities:
            return []
        params = urllib.parse.urlencode({"id_list": ",".join(identities), "max_results": len(identities)})
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

        arXiv returns 429/5xx during announcement bursts.  Retrying here keeps
        every discovery entry point consistent and avoids four track-specific
        scripts each inventing a different recovery policy.
        """
        for attempt in range(self.maximum_retries + 1):
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    payload = response.read()
                self._last_request_at = time.monotonic()
                return payload
            except urllib.error.HTTPError as exc:
                if exc.code not in {429, 500, 502, 503, 504} or attempt >= self.maximum_retries:
                    raise
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                try:
                    delay = float(retry_after) if retry_after else 0.0
                except ValueError:
                    delay = 0.0
                delay = max(delay, self.retry_backoff_seconds * (2**attempt))
                time.sleep(delay)
        raise AssertionError("unreachable")


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
        papers.append(
            Paper(
                title=" ".join(_text(entry, "atom:title").split()),
                abstract=" ".join(_text(entry, "atom:summary").split()),
                authors=[
                    _text(author, "atom:name")
                    for author in entry.findall("atom:author", NS)
                ],
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
