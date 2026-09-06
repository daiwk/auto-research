import datetime as dt

from auto_research.discovery import (
    PRIORITY_ORGANIZATION_TERMS,
    DiscoveredPaper,
    DiscoveryQuery,
    build_discovery_payload,
    discover_candidates,
    queries_for_track,
    recommendation_queries,
    render_discovery_summary,
    repository_paper_statuses,
    triage_candidates,
)
from auto_research.discovery import paper_is_in_window
from auto_research.models import Paper
from scripts.discover_papers import effective_start_date


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
    assert papers[0].to_dict()["abstract"] == "recommendation ranking production experiment"
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


def test_daily_announcement_scan_overlaps_the_preceding_submission_day():
    assert effective_start_date(
        dt.date(2026, 8, 27), announcement_overlap_days=1
    ) == dt.date(2026, 8, 26)


def test_late_indexed_arxiv_id_month_is_an_independent_recall_path():
    paper = _paper("2609.01622", "RecEvolve", "2026-07-20")
    assert paper_is_in_window(
        paper,
        start_date=dt.date(2026, 9, 1),
        end_date=dt.date(2026, 9, 6),
    )
    assert not paper_is_in_window(
        paper,
        start_date=dt.date(2026, 8, 1),
        end_date=dt.date(2026, 8, 31),
    )


def test_triage_diffs_repository_and_only_prioritizes_google_meta(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        '{"papers": [{"paper_url": "https://arxiv.org/abs/2608.00001"}]}',
        encoding="utf-8",
    )
    ledger = tmp_path / "ledger.json"
    ledger.write_text(
        '{"batches": [{"candidates": [{"id": "2608.00002", "status": "rejected"}]}]}',
        encoding="utf-8",
    )
    statuses = repository_paper_statuses(manifest, ledger)
    papers = [
        DiscoveredPaper(_paper("2608.00001", "Known", "2026-08-10"), ("priority-org-meta",)),
        DiscoveredPaper(_paper("2608.00002", "Reviewed", "2026-08-10"), ("recsys-general",)),
        DiscoveredPaper(_paper("2608.00003", "Google", "2026-08-10"), ("priority-org-google",)),
        DiscoveredPaper(_paper("2608.00004", "Netflix", "2026-08-10"), ("priority-org-netflix",)),
    ]
    candidates = triage_candidates(papers, statuses)
    assert [item["repository_status"] for item in candidates] == [
        "implemented",
        "reviewed",
        "new",
        "new",
    ]
    assert [item["priority_review_required"] for item in candidates] == [False, False, True, False]

    payload = build_discovery_payload(
        track="recommendation",
        start_date=dt.date(2026, 8, 1),
        end_date=dt.date(2026, 8, 13),
        query_names=("recsys-general",),
        candidates=candidates,
    )
    summary = render_discovery_summary(payload)
    assert payload["triage_counts"] == {
        "new": 2,
        "implemented": 1,
        "reviewed": 1,
        "google_meta_priority_review": 1,
    }
    assert summary.index("Google / Meta 重点复核") < summary.index("其他新候选")
    assert "Netflix 及其他机构进入普通候选队列" in summary
