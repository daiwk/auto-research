"""Cross-source paper recall with explicit, auditable provenance."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Callable, Iterable
import urllib.request

from .models import Paper
from .papers import ArxivClient, canonical_arxiv_id


ARXIV_LINK = re.compile(
    r"(?:arxiv\.org/(?:abs|pdf)/|arxiv:)(\d{4}\.\d{4,5})(?:v\d+)?",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class DiscoverySource:
    name: str
    kind: str
    url: str
    track: str = "all"
    organization: str | None = None


@dataclass(frozen=True)
class CrossSourceHit:
    arxiv_id: str
    source_name: str
    source_kind: str
    source_url: str
    organization: str | None
    relation: str = "direct"
    seed_arxiv_id: str | None = None

    def provenance(self) -> dict:
        return {
            "source": self.source_name,
            "source_kind": self.source_kind,
            "source_url": self.source_url,
            "organization": self.organization,
            "relation": self.relation,
            "seed_arxiv_id": self.seed_arxiv_id,
        }


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
        return response.read().decode("utf-8", errors="replace")


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
) -> tuple[list[Paper], dict[str, list[dict]], list[dict]]:
    """Fetch sources, resolve IDs through arXiv and retain source failures."""
    hits: list[CrossSourceHit] = []
    failures: list[dict] = []
    for source in sources:
        try:
            hits.extend(extract_source_hits(source, fetcher(source.url)))
        except Exception as exc:  # each source is independently auditable
            failures.append({"source": source.name, "url": source.url, "error": str(exc)})
    if snowball_seeds:
        try:
            hits.extend(semantic_scholar_citation_hits(snowball_seeds, fetcher=fetcher))
        except Exception as exc:
            failures.append({"source": "semantic-scholar-snowball", "error": str(exc)})
    provenance: dict[str, list[dict]] = {}
    for hit in hits:
        provenance.setdefault(hit.arxiv_id, []).append(hit.provenance())
    papers = client.lookup(provenance)
    return papers, provenance, failures
