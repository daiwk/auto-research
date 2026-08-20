"""High-recall, auditable paper candidate discovery.

This module deliberately separates *candidate recall* from the downstream
evidence gate.  Abstract keywords may retrieve a paper, but industrial online
evidence is still accepted only after a full-text review.
"""

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
import json
from pathlib import Path
from typing import Iterable

from .models import Paper
from .papers import ArxivClient, canonical_arxiv_id


@dataclass(frozen=True)
class DiscoveryQuery:
    name: str
    text: str
    categories: tuple[str, ...]
    match: str = "all"


@dataclass(frozen=True)
class DiscoveredPaper:
    paper: Paper
    query_names: tuple[str, ...]
    source_provenance: tuple[dict, ...] = ()

    def to_dict(self) -> dict:
        return {
            "arxiv_id": canonical_arxiv_id(self.paper.arxiv_id),
            "title": self.paper.title,
            "published": self.paper.published,
            "url": self.paper.url,
            "authors": self.paper.authors,
            "matched_queries": list(self.query_names),
            "source_provenance": list(self.source_provenance),
            "evidence_status": "full-text-review-required",
        }


# Use multiple narrow queries instead of one long AND expression.  The matrix
# includes architectural synonyms and production language; company names are
# intentionally not required, so an unfamiliar industrial team remains visible.
RECOMMENDATION_QUERIES: tuple[DiscoveryQuery, ...] = (
    DiscoveryQuery("recsys-general", "recommender system", ("cs.IR", "cs.LG")),
    DiscoveryQuery("recommendation-ranking", "recommendation ranker", ("cs.IR", "cs.LG")),
    DiscoveryQuery("generative-recommendation", "generative recommendation", ("cs.IR", "cs.LG")),
    DiscoveryQuery("llm-recommendation", "LLM recommendation", ("cs.IR", "cs.CL")),
    DiscoveryQuery("industrial-ranking", "industrial ranking recommendation", ("cs.IR", "cs.LG")),
    DiscoveryQuery("production-evidence", "recommendation online A/B", ("cs.IR", "cs.LG")),
    DiscoveryQuery("deployment-evidence", "recommendation deployed production", ("cs.IR", "cs.LG")),
    DiscoveryQuery("search-ranking", "search ranking online A/B", ("cs.IR", "cs.LG")),
    DiscoveryQuery("advertising-ranking", "advertising ranking online A/B", ("cs.IR", "cs.LG")),
)

FOUNDATION_MODEL_QUERIES: tuple[DiscoveryQuery, ...] = (
    DiscoveryQuery("llm-architecture", "language model architecture", ("cs.CL", "cs.LG")),
    DiscoveryQuery("transformer-architecture", "transformer architecture", ("cs.CL", "cs.LG")),
    DiscoveryQuery("efficient-inference", "efficient LLM inference", ("cs.CL", "cs.LG")),
    DiscoveryQuery("long-context", "language model long context", ("cs.CL", "cs.LG")),
    DiscoveryQuery("pretraining-data", "language model pretraining data", ("cs.CL", "cs.LG")),
    DiscoveryQuery("multimodal-llm", "multimodal language model", ("cs.CV", "cs.CL")),
    DiscoveryQuery("vision-language", "vision language model", ("cs.CV", "cs.CL")),
    DiscoveryQuery("model-compression", "language model compression", ("cs.CL", "cs.LG")),
)

POST_TRAINING_QUERIES: tuple[DiscoveryQuery, ...] = (
    DiscoveryQuery("post-training", "language model post training", ("cs.CL", "cs.LG")),
    DiscoveryQuery("preference-optimization", "language model preference optimization", ("cs.CL", "cs.LG")),
    DiscoveryQuery("llm-rl", "reinforcement learning language model", ("cs.CL", "cs.LG")),
    DiscoveryQuery("on-policy-distillation", "on policy distillation language model", ("cs.CL", "cs.LG")),
    DiscoveryQuery("reward-model", "language model reward model", ("cs.CL", "cs.LG")),
    DiscoveryQuery("process-reward", "language model process reward", ("cs.CL", "cs.LG")),
    DiscoveryQuery("test-time-rl", "test time reinforcement learning", ("cs.CL", "cs.LG")),
    DiscoveryQuery("opd", "online policy distillation", ("cs.CL", "cs.LG")),
)

AGENT_QUERIES: tuple[DiscoveryQuery, ...] = (
    DiscoveryQuery("llm-agent", "LLM agent", ("cs.AI", "cs.CL")),
    DiscoveryQuery("agentic-rl", "agentic reinforcement learning", ("cs.AI", "cs.LG")),
    DiscoveryQuery("tool-agent", "language model tool use agent", ("cs.AI", "cs.CL")),
    DiscoveryQuery("web-agent", "web agent language model", ("cs.AI", "cs.CL")),
    DiscoveryQuery("software-agent", "software engineering agent", ("cs.SE", "cs.AI")),
    DiscoveryQuery("agent-memory", "language model agent memory", ("cs.AI", "cs.CL")),
    DiscoveryQuery("agent-planning", "language model agent planning", ("cs.AI", "cs.CL")),
    DiscoveryQuery("multi-agent", "large language model multi agent", ("cs.AI", "cs.CL")),
)

PRIORITY_ORGANIZATION_TERMS: tuple[str, ...] = (
    "Google",
    "Google DeepMind",
    "Meta",
    "Netflix",
    "ByteDance",
    "TikTok",
    "Alibaba",
    "Taobao",
    "Kuaishou",
    "Pinterest",
    "Amazon",
    "Microsoft",
    "Tencent",
)

# These are the only organizations that receive an automatic high-priority
# review warning. Other organization queries improve recall but remain in the
# normal queue; in particular, Netflix is deliberately not promoted.
PRIORITY_REVIEW_QUERY_NAMES: frozenset[str] = frozenset(
    {"priority-org-google", "priority-org-google-deepmind", "priority-org-meta"}
)


def repository_paper_statuses(
    manifest_path: Path,
    ledger_path: Path,
) -> dict[str, str]:
    """Load canonical arXiv IDs already implemented or explicitly reviewed."""
    statuses: dict[str, str] = {}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for paper in manifest.get("papers", []):
        paper_url = str(paper.get("paper_url", ""))
        arxiv_id = paper_url.rstrip("/").split("/")[-1]
        if arxiv_id:
            statuses[canonical_arxiv_id(arxiv_id)] = "implemented"

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    for batch in ledger.get("batches", []):
        for candidate in batch.get("candidates", []):
            arxiv_id = candidate.get("id")
            if not arxiv_id:
                continue
            identity = canonical_arxiv_id(str(arxiv_id))
            statuses.setdefault(identity, "reviewed")
    return statuses


def triage_candidates(
    papers: Iterable[DiscoveredPaper],
    repository_statuses: dict[str, str],
) -> list[dict]:
    """Diff recalled papers against the repository and add review signals."""
    candidates: list[dict] = []
    for discovered in papers:
        item = discovered.to_dict()
        identity = item["arxiv_id"]
        status = repository_statuses.get(identity, "new")
        priority_matches = sorted(PRIORITY_REVIEW_QUERY_NAMES.intersection(discovered.query_names))
        item.update(
            {
                "repository_status": status,
                "priority_review_required": status == "new" and bool(priority_matches),
                "priority_query_matches": priority_matches,
            }
        )
        candidates.append(item)
    return candidates


def build_discovery_payload(
    *,
    track: str,
    start_date: dt.date,
    end_date: dt.date,
    query_names: Iterable[str],
    candidates: list[dict],
) -> dict:
    counts = {
        status: sum(candidate["repository_status"] == status for candidate in candidates)
        for status in ("new", "implemented", "reviewed")
    }
    counts["google_meta_priority_review"] = sum(
        bool(candidate["priority_review_required"]) for candidate in candidates
    )
    return {
        "schema_version": 2,
        "track": track,
        "window": {"start": str(start_date), "end": str(end_date)},
        "query_matrix": list(query_names),
        "candidate_count": len(candidates),
        "triage_counts": counts,
        "candidates": candidates,
    }


def render_discovery_summary(payload: dict) -> str:
    """Render a compact GitHub Actions review queue."""
    counts = payload["triage_counts"]
    lines = [
        f"# {payload['track']} 论文候选差分",
        "",
        f"扫描窗口：{payload['window']['start']} 至 {payload['window']['end']}",
        "",
        "| 新候选 | 已实现 | 已审计 | Google / Meta 重点复核 |",
        "| ---: | ---: | ---: | ---: |",
        f"| {counts['new']} | {counts['implemented']} | {counts['reviewed']} | "
        f"{counts['google_meta_priority_review']} |",
        "",
        "## Google / Meta 重点复核",
        "",
        "机构查询命中只是召回信号，必须打开 PDF 核对一作 affiliation 和正文线上证据。",
        "Netflix 及其他机构进入普通候选队列，不享受自动置顶。",
        "",
    ]
    priority = [item for item in payload["candidates"] if item["priority_review_required"]]
    lines.extend(_candidate_lines(priority, empty="本次没有新的 Google / Meta 重点候选。"))
    lines.extend(["", "## 其他新候选", ""])
    other_new = [
        item
        for item in payload["candidates"]
        if item["repository_status"] == "new" and not item["priority_review_required"]
    ]
    lines.extend(_candidate_lines(other_new, empty="本次没有其他新候选。"))
    lines.extend(
        [
            "",
            "## 已处理候选",
            "",
            f"已实现 {counts['implemented']} 篇，已审计但未实现 {counts['reviewed']} 篇；"
            "详情保留在 JSON artifact。",
            "",
        ]
    )
    return "\n".join(lines)


def _candidate_lines(candidates: Iterable[dict], *, empty: str) -> list[str]:
    items = list(candidates)
    if not items:
        return [empty]
    return [
        f"- [{item['arxiv_id']} · {item['title']}]({item['url']})（{item['published'][:10]}）"
        for item in items
    ]


def recommendation_queries() -> tuple[DiscoveryQuery, ...]:
    """Return topic queries plus a supplementary priority-organization sweep.

    arXiv does not expose structured affiliations, so these organization queries
    cannot replace PDF affiliation review. They catch company names present in
    titles/abstracts and make that extra sweep observable.
    """
    organization_queries = tuple(
        DiscoveryQuery(
            f"priority-org-{organization.lower().replace(' ', '-')}",
            f"{organization} recommendation",
            ("cs.IR", "cs.LG", "cs.CL"),
        )
        for organization in PRIORITY_ORGANIZATION_TERMS
    )
    return RECOMMENDATION_QUERIES + organization_queries


def queries_for_track(track: str) -> tuple[DiscoveryQuery, ...]:
    matrices = {
        "recommendation": recommendation_queries(),
        "foundation-model": FOUNDATION_MODEL_QUERIES,
        "post-training": POST_TRAINING_QUERIES,
        "agent": AGENT_QUERIES,
    }
    try:
        return matrices[track]
    except KeyError as exc:
        raise ValueError(f"unknown discovery track: {track}") from exc


def discover_candidates(
    client: ArxivClient,
    queries: Iterable[DiscoveryQuery],
    *,
    start_date: dt.date,
    end_date: dt.date,
    page_size: int = 50,
    maximum_results_per_query: int = 200,
) -> list[DiscoveredPaper]:
    """Run every query, retain provenance, date-filter and de-duplicate."""
    found: dict[str, Paper] = {}
    origins: dict[str, set[str]] = {}
    for query in queries:
        papers = client.search_pages(
            query.text,
            categories=query.categories,
            page_size=page_size,
            maximum_results=maximum_results_per_query,
            match=query.match,
        )
        for paper in papers:
            published = dt.date.fromisoformat(paper.published[:10])
            if not start_date <= published <= end_date:
                continue
            identity = canonical_arxiv_id(paper.arxiv_id)
            if identity not in found or paper.published > found[identity].published:
                found[identity] = paper
            origins.setdefault(identity, set()).add(query.name)
    return [
        DiscoveredPaper(found[identity], tuple(sorted(origins[identity])))
        for identity in sorted(found, key=lambda key: found[key].published, reverse=True)
    ]


def merge_external_candidates(
    arxiv_results: Iterable[DiscoveredPaper],
    external_papers: Iterable[Paper],
    provenance: dict[str, list[dict]],
) -> list[DiscoveredPaper]:
    """Merge external recall without erasing query or source provenance."""
    merged = {
        canonical_arxiv_id(item.paper.arxiv_id): item for item in arxiv_results
    }
    for paper in external_papers:
        identity = canonical_arxiv_id(paper.arxiv_id)
        sources = tuple(provenance.get(identity, ()))
        current = merged.get(identity)
        if current is None:
            merged[identity] = DiscoveredPaper(paper, (), sources)
        else:
            merged[identity] = DiscoveredPaper(
                paper if paper.published > current.paper.published else current.paper,
                current.query_names,
                tuple((*current.source_provenance, *sources)),
            )
    return sorted(merged.values(), key=lambda item: item.paper.published, reverse=True)
