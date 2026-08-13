import datetime as dt

from auto_research.discovery import (
    PRIORITY_ORGANIZATION_TERMS,
    DiscoveryQuery,
    discover_candidates,
    queries_for_track,
    recommendation_queries,
)
from auto_research.models import Paper


def _paper(arxiv_id: str, title: str, published: str) -> Paper:
    return Paper(
        title=title,
        abstract="recommendation ranking production experiment",
        authors=["Researcher"],
        published=f"{published}T00:00:00Z",
        url=f"https://arxiv.org/abs/{arxiv_id}",
        arxiv_id=arxiv_id,
    )


class FakeClient:
    def __init__(self):
        self.calls = []

    def search_pages(self, query, **kwargs):
        self.calls.append((query, kwargs))
        if query == "LLM recommendation":
            return [
                _paper("2608.10257v1", "GenRec", "2026-08-10"),
                _paper("2607.00001v1", "Old", "2026-07-01"),
            ]
        return [_paper("2608.10257v2", "GenRec revised", "2026-08-12")]


def test_discovery_uses_all_queries_keeps_provenance_and_deduplicates_versions():
    client = FakeClient()
    queries = (
        DiscoveryQuery("llm", "LLM recommendation", ("cs.IR",)),
        DiscoveryQuery("online", "recommendation online A/B", ("cs.IR",)),
    )
    papers = discover_candidates(
        client,
        queries,
        start_date=dt.date(2026, 8, 10),
        end_date=dt.date(2026, 8, 13),
        page_size=25,
        maximum_results_per_query=100,
    )
    assert len(client.calls) == 2
    assert len(papers) == 1
    assert papers[0].paper.title == "GenRec revised"
    assert papers[0].query_names == ("llm", "online")
    assert papers[0].to_dict()["evidence_status"] == "full-text-review-required"


def test_recommendation_matrix_includes_priority_organization_sweep():
    names = {query.name for query in recommendation_queries()}
    for organization in PRIORITY_ORGANIZATION_TERMS:
        slug = organization.lower().replace(" ", "-")
        assert f"priority-org-{slug}" in names


def test_all_research_tracks_have_multi_query_discovery_matrices():
    for track in ("recommendation", "foundation-model", "post-training", "agent"):
        queries = queries_for_track(track)
        assert len(queries) >= 8
        assert len({query.name for query in queries}) == len(queries)
