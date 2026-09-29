"""Cross-source paper recall with explicit, auditable provenance."""

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
import gzip
from html.parser import HTMLParser
import html
import json
import re
from pathlib import Path
from typing import Callable, Iterable
import unicodedata
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse
import urllib.request

from .models import Paper
from .papers import ArxivClient, canonical_arxiv_id


ARXIV_LINK = re.compile(
    r"(?:arxiv\.org/(?:abs|pdf)/|arxiv:)(\d{4}\.\d{4,5})(?:v\d+)?",
    re.IGNORECASE,
)

TRACK_TITLE_TERMS = {
    "recommendation": ("recommend", "rank", "retriev", "advertis", "search", "personaliz"),
    "foundation-model": ("language model", "transformer", "multimodal", "vision", "token"),
    "post-training": (
        "reinforcement", "post-train", "preference", "distill", "reward", "grpo", "dpo",
    ),
    "agent": ("agent", "tool", "memory", "planning", "reasoning"),
}


@dataclass(frozen=True)
class DiscoverySource:
    name: str
    kind: str
    url: str
    track: str = "all"
    organization: str | None = None
    max_pages: int = 1
    max_title_lookups: int = 0


@dataclass(frozen=True)
class CrossSourceHit:
    arxiv_id: str
    source_name: str
    source_kind: str
    source_url: str
    organization: str | None
    relation: str = "direct"
    seed_arxiv_id: str | None = None
    source_published: str | None = None

    def provenance(self) -> dict:
        result = {
            "source": self.source_name,
            "source_kind": self.source_kind,
            "source_url": self.source_url,
            "organization": self.organization,
            "relation": self.relation,
            "seed_arxiv_id": self.seed_arxiv_id,
        }
        if self.source_published:
            result["source_published"] = self.source_published
        return result


def load_sources(path: Path, track: str) -> tuple[DiscoverySource, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return tuple(
        DiscoverySource(**item)
        for item in payload.get("sources", [])
        if item.get("track", "all") in {"all", track}
    )


def fetch_text(url: str, timeout: int = 30) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "auto-research/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if "pdf" in response.headers.get("Content-Type", "").lower():
            raise ValueError("PDF source needs a text/PDF extractor; no HTML coverage claimed")
        content = response.read()
        if content.startswith(b"\x1f\x8b"):
            content = gzip.decompress(content)
        return content.decode("utf-8", errors="replace")


def extract_source_hits(source: DiscoverySource, content: str) -> tuple[CrossSourceHit, ...]:
    return tuple(
        CrossSourceHit(
            arxiv_id=identity,
            source_name=source.name,
            source_kind=source.kind,
            source_url=source.url,
            organization=source.organization,
        )
        for identity in dict.fromkeys(
            canonical_arxiv_id(match.group(1)) for match in ARXIV_LINK.finditer(content)
        )
    )


def normalized_title(title: str) -> str:
    """Conservative cross-source identity: never infer a paper from a fuzzy slug."""
    normalized = unicodedata.normalize("NFKC", title).casefold()
    return " ".join("".join(
        character if character.isalnum() else " " for character in normalized
    ).split())


class _PublicationLinks(HTMLParser):
    def __init__(self, source_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.source_url = source_url
        self.records: list[tuple[str, str, str | None]] = []
        self.heading: list[str] | None = None
        self.last_heading = ""
        self.paragraph: list[str] | None = None
        self.last_date: str | None = None
        self.anchor: list[str] | None = None
        self.href = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h4":
            self.heading = []
        if tag == "p":
            self.paragraph = []
        if tag == "a":
            self.anchor = []
            self.href = dict(attrs).get("href") or ""

    def handle_data(self, data: str) -> None:
        if self.heading is not None:
            self.heading.append(data)
        if self.paragraph is not None:
            self.paragraph.append(data)
        if self.anchor is not None:
            self.anchor.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "p" and self.paragraph is not None:
            value = " ".join("".join(self.paragraph).split())
            try:
                self.last_date = dt.datetime.strptime(value, "%B %d, %Y").date().isoformat()
            except ValueError:
                pass
            self.paragraph = None
        if tag == "h4" and self.heading is not None:
            self.last_heading = " ".join("".join(self.heading).split())
            self.heading = None
        if tag == "a" and self.anchor is not None:
            url = urljoin(self.source_url, self.href)
            parsed = urlparse(url)
            google = parsed.netloc == "research.google" and parsed.path.startswith("/pubs/")
            meta = parsed.netloc == "ai.meta.com" and parsed.path.startswith(
                "/research/publications/"
            )
            if (google or meta) and parsed.path.rstrip("/") not in {
                "/pubs", "/research/publications",
            }:
                label = " ".join("".join(self.anchor).split())
                title = self.last_heading if meta or label.lower() == "view details" else label
                if title and title.lower() not in {"read the paper", "view details"}:
                    self.records.append((title, url, self.last_date if meta else None))
            self.anchor = None


class _DeepMindPublications(HTMLParser):
    """Read dated publication cards, not unrelated links on the listing page."""

    def __init__(self, source_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.source_url = source_url
        self.records: list[tuple[str, str, str | None]] = []
        self.href: str | None = None
        self.field: str | None = None
        self.title: list[str] = []
        self.date: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "a" and self.href is None:
            url = urljoin(self.source_url, attributes.get("href") or "")
            parsed = urlparse(url)
            if parsed.netloc == "deepmind.google" and re.fullmatch(
                r"/research/publications/\d+/?", parsed.path
            ):
                self.href = url
                self.title = []
                self.date = []
        elif tag == "span" and self.href:
            classes = (attributes.get("class") or "").split()
            if "list-group__description" in classes:
                self.field = "title"
            elif "list-group__date" in classes:
                self.field = "date"

    def handle_data(self, data: str) -> None:
        if self.field == "title":
            self.title.append(data)
        elif self.field == "date":
            self.date.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "span":
            self.field = None
        elif tag == "a" and self.href:
            title = " ".join("".join(self.title).split())
            date_text = " ".join("".join(self.date).split())
            try:
                published = dt.datetime.strptime(date_text, "%d %B %Y").date().isoformat()
            except ValueError:
                published = None
            if title:
                self.records.append((title, self.href, published))
            self.href = None
            self.field = None


class _RecSysPosters(HTMLParser):
    """Read paper titles from official 2026 poster accordion headers."""

    def __init__(self, source_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.source_url = source_url
        self.records: list[tuple[str, str, str | None]] = []
        self.fragment: str | None = None
        self.title: list[str] = []
        self.in_spot = False
        self.after_break = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "a" and self.fragment is None:
            fragment = attributes.get("rel") or ""
            if re.fullmatch(r"#accordion-\d+-slide-\d+", fragment):
                self.fragment = fragment
                self.title = []
                self.after_break = False
        elif self.fragment and tag == "span" and "paper-type" in (
            attributes.get("class") or ""
        ).split():
            self.in_spot = True
        elif self.fragment and tag == "br":
            self.after_break = True

    def handle_data(self, data: str) -> None:
        if self.fragment and not self.in_spot and not self.after_break:
            self.title.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "span":
            self.in_spot = False
        elif tag == "a" and self.fragment:
            title = " ".join("".join(self.title).split())
            if title:
                self.records.append((title, urljoin(self.source_url, self.fragment), None))
            self.fragment = None


def _sigir_accepted_papers(source_url: str, content: str) -> tuple[
    tuple[str, str, str | None], ...
]:
    """Extract only accepted paper titles from SIGIR's escaped Next.js payload.

    The official page renders its track lists into serialized text blocks,
    sometimes twice. There are no per-paper links or first-publication dates.
    """
    pattern = re.compile(
        r"\\u003cp\\u003e\[(?:fp|sp|ip|rp|rr|pr|lre|de|dc)\]"
        r"\s*\\u003ci\\u003e"
        r"(.*?)\\u003c/i\\u003e", re.DOTALL | re.IGNORECASE,
    )
    records = []
    for match in pattern.finditer(content):
        title = re.sub(
            r"\\u([0-9a-fA-F]{4})",
            lambda item: chr(int(item.group(1), 16)), match.group(1),
        )
        title = " ".join(html.unescape(re.sub(r"<[^>]+>", "", title)).split())
        if title:
            records.append((title, source_url, None))
    return tuple(dict.fromkeys(records))


def publication_records(
    source: DiscoverySource, content: str,
) -> tuple[tuple[str, str, str | None], ...]:
    """Extract official detail links without assuming they expose arXiv IDs."""
    parsed = urlparse(source.url)
    if parsed.netloc in {"research.google", "ai.meta.com"}:
        parser = _PublicationLinks(source.url)
    elif parsed.netloc == "deepmind.google" and parsed.path.startswith(
        "/research/publications/"
    ):
        parser = _DeepMindPublications(source.url)
    elif parsed.netloc == "recsys.acm.org" and re.fullmatch(
        r"/recsys26/posters-\d+/?", parsed.path
    ):
        parser = _RecSysPosters(source.url)
    elif parsed.netloc == "sigir2026.org" and parsed.path.endswith(
        "/pages/program/accepted-papers"
    ):
        return _sigir_accepted_papers(source.url, content)
    else:
        return ()
    parser.feed(content)
    return tuple(dict.fromkeys(parser.records))


def page_url(url: str, page: int) -> str:
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["page"] = str(page)
    return urlunparse(parsed._replace(query=urlencode(query)))


def prioritized_records(
    records: Iterable[tuple[str, str, str | None]], track: str,
) -> list[tuple[str, str, str | None]]:
    terms = TRACK_TITLE_TERMS.get(track, ())
    return sorted(
        records,
        key=lambda record: not any(term in record[0].casefold() for term in terms),
    )


def semantic_scholar_citation_hits(
    seed_ids: Iterable[str],
    *,
    fetcher: Callable[[str], str] = fetch_text,
    limit: int = 100,
) -> tuple[CrossSourceHit, ...]:
    """Recall references and citations around already relevant seed papers."""
    hits: list[CrossSourceHit] = []
    for seed in dict.fromkeys(canonical_arxiv_id(value) for value in seed_ids):
        url = (
            "https://api.semanticscholar.org/graph/v1/paper/ARXIV:"
            f"{seed}?fields=references.externalIds,citations.externalIds&limit={limit}"
        )
        payload = json.loads(fetcher(url))
        for relation in ("references", "citations"):
            for record in payload.get(relation, []) or []:
                external = (record or {}).get("externalIds") or {}
                identity = external.get("ArXiv")
                if identity:
                    hits.append(CrossSourceHit(
                        canonical_arxiv_id(str(identity)), "semantic-scholar-snowball",
                        "citation-snowball", url, None, relation[:-1], seed,
                    ))
    unique = {(hit.arxiv_id, hit.relation, hit.seed_arxiv_id): hit for hit in hits}
    return tuple(unique.values())


def discover_external(
    sources: Iterable[DiscoverySource],
    *,
    client: ArxivClient,
    fetcher: Callable[[str], str] = fetch_text,
    snowball_seeds: Iterable[str] = (),
    known_papers: Iterable[Paper] = (),
    track: str = "all",
) -> tuple[list[Paper], dict[str, list[dict]], list[dict], list[dict]]:
    """Fetch sources, resolve IDs, and distinguish empty extraction from coverage."""
    hits: list[CrossSourceHit] = []
    title_resolved_papers: list[Paper] = []
    failures: list[dict] = []
    source_stats: list[dict] = []
    title_index: dict[str, list[Paper]] = {}
    known_ids: set[str] = set()
    for paper in known_papers:
        title_index.setdefault(normalized_title(paper.title), []).append(paper)
        known_ids.add(canonical_arxiv_id(paper.arxiv_id))
    for source in sources:
        try:
            if source.max_pages < 1 or source.max_title_lookups < 0:
                raise ValueError("max_pages must be positive and max_title_lookups non-negative")
            extracted: list[CrossSourceHit] = []
            records: dict[tuple[str, str], tuple[str, str, str | None]] = {}
            for page in range(1, source.max_pages + 1):
                url = source.url if page == 1 else page_url(source.url, page)
                content = fetcher(url)
                if source.kind != "official-conference":
                    extracted.extend(extract_source_hits(source, content))
                for title, detail_url, published in publication_records(source, content):
                    records.setdefault(
                        (normalized_title(title), detail_url), (title, detail_url, published)
                    )
            direct_count = len(extracted)
            matched = 0
            title_lookups = 0
            lookup_errors: list[dict] = []
            unresolved: list[dict] = []
            for title, detail_url, published in prioritized_records(records.values(), track):
                candidates = title_index.get(normalized_title(title), ())
                identities = {canonical_arxiv_id(item.arxiv_id) for item in candidates}
                if not identities and title_lookups < source.max_title_lookups:
                    title_lookups += 1
                    try:
                        searched = client.search(title, limit=5, match="all")
                        exact = [
                            item for item in searched
                            if normalized_title(item.title) == normalized_title(title)
                        ]
                        identities = {canonical_arxiv_id(item.arxiv_id) for item in exact}
                        if len(identities) == 1:
                            title_resolved_papers.extend(exact)
                    except Exception as exc:
                        lookup_errors.append({"title": title, "error": str(exc)})
                if len(identities) == 1:
                    extracted.append(CrossSourceHit(
                        identities.pop(), source.name, source.kind, detail_url,
                        source.organization, "exact-title", source_published=published,
                    ))
                    matched += 1
                else:
                    item = {"title": title, "url": detail_url}
                    if published:
                        item["source_published"] = published
                    unresolved.append(item)
            hits.extend(extracted)
            stat = {
                "source": source.name,
                "url": source.url,
                "arxiv_ids_extracted": direct_count,
                "status": "partial" if records else "ok" if extracted else "no_arxiv_ids",
            }
            if records:
                stat.update({
                    "pages_scanned": source.max_pages,
                    "official_publications": len(records),
                    "exact_title_matches": matched,
                    "title_lookups_attempted": title_lookups,
                    "title_lookup_errors": lookup_errors,
                    "unresolved_publications": unresolved,
                    "note": "Listing is not proof of exhaustive date coverage; unresolved titles require review.",
                })
            source_stats.append(stat)
        except Exception as exc:  # each source is independently auditable
            failures.append({"source": source.name, "url": source.url, "error": str(exc)})
            source_stats.append({
                "source": source.name, "url": source.url,
                "arxiv_ids_extracted": 0, "status": "error",
            })
    if snowball_seeds:
        try:
            hits.extend(semantic_scholar_citation_hits(snowball_seeds, fetcher=fetcher))
        except Exception as exc:
            failures.append({"source": "semantic-scholar-snowball", "error": str(exc)})
    provenance: dict[str, list[dict]] = {}
    for hit in hits:
        provenance.setdefault(hit.arxiv_id, []).append(hit.provenance())
    try:
        papers = client.lookup([
            identity for identity in provenance if identity not in known_ids
        ])
    except Exception as exc:
        failures.append({"source": "arxiv-id-lookup", "error": str(exc)})
        papers = []
    resolved = {canonical_arxiv_id(item.arxiv_id): item for item in papers}
    resolved.update({canonical_arxiv_id(item.arxiv_id): item for item in title_resolved_papers})
    return list(resolved.values()), provenance, failures, source_stats
