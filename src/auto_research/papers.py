from __future__ import annotations

import datetime as dt
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from .models import Paper

ARXIV_API = "https://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}


class ArxivClient:
    """Small dependency-free arXiv client, sorted by newest submission."""

    def __init__(self, timeout: int = 30, user_agent: str = "auto-research/0.1"):
        self.timeout = timeout
        self.user_agent = user_agent

    def search(
        self, query: str, limit: int = 8, categories: tuple[str, ...] = ()
    ) -> list[Paper]:
        if limit <= 0:
            return []
        terms = re.findall(r"[A-Za-z0-9][A-Za-z0-9_.+-]*", query)[:8]
        search_query = " AND ".join(f'all:"{term}"' for term in terms)
        if categories:
            category_query = " OR ".join(f"cat:{category}" for category in categories)
            search_query = f"({search_query}) AND ({category_query})"
        if not search_query:
            raise ValueError("paper query contains no searchable terms")
        params = urllib.parse.urlencode(
            {
                "search_query": search_query,
                "start": 0,
                "max_results": limit,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
        )
        request = urllib.request.Request(
            f"{ARXIV_API}?{params}", headers={"User-Agent": self.user_agent}
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return parse_arxiv_feed(response.read())


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
