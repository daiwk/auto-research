"""High-recall, auditable paper candidate discovery.

This module deliberately separates *candidate recall* from the downstream
evidence gate.  Abstract keywords may retrieve a paper, but industrial online
evidence is still accepted only after a full-text review.
"""

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
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

    def to_dict(self) -> dict:
        return {
            "arxiv_id": canonical_arxiv_id(self.paper.arxiv_id),
            "title": self.paper.title,
            "published": self.paper.published,
            "url": self.paper.url,
            "authors": self.paper.authors,
            "matched_queries": list(self.query_names),
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
