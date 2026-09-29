import json

import pytest

from auto_research.discovery import (
    DiscoveredPaper, build_discovery_payload, merge_external_candidates,
    render_discovery_summary,
)
import datetime as dt
from auto_research.discovery_sources import (
    DiscoverySource, discover_external, extract_source_hits, page_url,
    publication_records, normalized_title,
    semantic_scholar_citation_hits,
)
from auto_research.models import Paper
from scripts.record_discovery_review import build_batch
from scripts.discover_papers import external_paper_in_window


def test_external_sources_extract_arxiv_links_and_keep_provenance():
    source = DiscoverySource(
        "Google Research", "official-research", "https://research.google/pubs/",
        organization="Google",
    )
    hits = extract_source_hits(
        source,
        '<a href="https://arxiv.org/abs/2608.12345v2">paper</a> arXiv:2608.12345',
    )
    assert len(hits) == 1
    assert hits[0].arxiv_id == "2608.12345"
    assert hits[0].provenance()["source_kind"] == "official-research"


def test_title_identity_does_not_collapse_word_boundaries():
    assert normalized_title("MaD-RL") == normalized_title("MaD RL")
    assert normalized_title("AB") != normalized_title("A-B")


def test_citation_snowball_records_relation_and_seed():
    payload = {
        "references": [{"externalIds": {"ArXiv": "2607.00001v2"}}],
        "citations": [{"externalIds": {"ArXiv": "2608.00002"}}],
    }
    hits = semantic_scholar_citation_hits(
        ["2608.10000"], fetcher=lambda _: json.dumps(payload)
    )
    assert {(hit.arxiv_id, hit.relation) for hit in hits} == {
        ("2607.00001", "reference"), ("2608.00002", "citation")
    }
    assert {hit.seed_arxiv_id for hit in hits} == {"2608.10000"}


def test_source_failure_is_visible_and_does_not_drop_other_sources():
    class Client:
        def lookup(self, ids):
            return [Paper("Paper", "", [], "2026-08-20T00:00:00Z", "url", next(iter(ids)))]

    sources = (
        DiscoverySource("ok", "author-page", "https://ok"),
        DiscoverySource("bad", "github", "https://bad"),
    )
    def fetcher(url):
        if url.endswith("bad"):
            raise OSError("down")
        return "https://arxiv.org/abs/2608.12345"
    papers, provenance, failures, source_stats = discover_external(
        sources, client=Client(), fetcher=fetcher
    )
    assert papers[0].arxiv_id == "2608.12345"
    assert provenance["2608.12345"][0]["source"] == "ok"
    assert failures == [{"source": "bad", "url": "https://bad", "error": "down"}]
    assert [(item["source"], item["status"]) for item in source_stats] == [
        ("ok", "ok"), ("bad", "error")
    ]


def test_successful_page_without_arxiv_ids_is_not_counted_as_covered():
    class Client:
        def lookup(self, ids):
            assert not ids
            return []

    source = DiscoverySource("dynamic-page", "official-research", "https://example.test")
    papers, provenance, failures, source_stats = discover_external(
        (source,), client=Client(), fetcher=lambda _: "<html>Recent papers</html>"
    )
    assert papers == []
    assert provenance == {}
    assert failures == []
    assert source_stats == [{
        "source": "dynamic-page", "url": "https://example.test",
        "arxiv_ids_extracted": 0, "status": "no_arxiv_ids",
    }]


@pytest.mark.parametrize("url,html,title", [
    (
        "https://research.google/pubs/?sort=-publication__year",
        '<a href="/pubs/a-new-method/"><span>A New Method</span></a>'
        '<a href="/pubs/a-new-method/">View details</a>',
        "A New Method",
    ),
    (
        "https://ai.meta.com/global_search/?page=1",
        '<h4>Reinforcement Learning</h4><h4>A New Method</h4>'
        '<a href="/research/publications/a-new-method/">Read the Paper</a>',
        "A New Method",
    ),
])
def test_official_listing_title_is_reconciled_without_arxiv_link(url, html, title):
    class Client:
        def lookup(self, ids):
            assert list(ids) == []
            return []

    source = DiscoverySource("official", "official-research", url, organization="Meta")
    records = publication_records(source, html)
    assert records[0][0] == title
    _, provenance, failures, stats = discover_external(
        [source], client=Client(), fetcher=lambda _: html,
        known_papers=[Paper(title, "", [], "2026-09-20", "", "2609.12345")],
    )
    assert not failures
    assert provenance["2609.12345"][0]["relation"] == "exact-title"
    assert stats[0]["status"] == "partial"
    assert stats[0]["exact_title_matches"] == 1
    assert stats[0]["unresolved_publications"] == []


def test_official_listing_keeps_unresolved_title_and_paginates():
    source = DiscoverySource(
        "meta", "official-research", "https://ai.meta.com/global_search/?page=1",
        max_pages=2,
    )
    requested = []
    def fetcher(url):
        requested.append(url)
        return '<h4>Unmatched Work</h4><a href="/research/publications/work/">Read the Paper</a>'
    class Client:
        def lookup(self, ids):
            assert not ids
            return []
    _, _, _, stats = discover_external([source], client=Client(), fetcher=fetcher)
    assert requested == [source.url, page_url(source.url, 2)]
    assert stats[0]["status"] == "partial"
    assert stats[0]["unresolved_publications"] == [{
        "title": "Unmatched Work", "url": "https://ai.meta.com/research/publications/work/",
    }]


def test_ambiguous_exact_title_is_not_attributed_to_either_paper():
    source = DiscoverySource("google", "official-research", "https://research.google/pubs/")
    class Client:
        def lookup(self, ids):
            assert not ids
            return []
    _, provenance, _, stats = discover_external(
        [source], client=Client(),
        fetcher=lambda _: '<a href="/pubs/a-new-method/">A New Method</a>',
        known_papers=[
            Paper("A New Method", "", [], "2026-09-20", "", identity)
            for identity in ("2609.00001", "2609.00002")
        ],
    )
    assert provenance == {}
    assert len(stats[0]["unresolved_publications"]) == 1


def test_bounded_official_title_lookup_recalls_exact_paper_only():
    source = DiscoverySource(
        "Meta", "official-research", "https://ai.meta.com/global_search/?page=1",
        max_title_lookups=1,
    )
    class Client:
        def search(self, title, *, limit, match):
            assert (title, limit, match) == ("MaD-RL", 5, "all")
            return [
                Paper("MaD-RL", "", [], "2026-09-12", "", "2609.31644"),
                Paper("MaD-RL Extra", "", [], "2026-09-12", "", "2609.00001"),
            ]
        def lookup(self, ids):
            assert list(ids) == ["2609.31644"]
            return []
    html = (
        '<h4>MaD-RL</h4><a href="/research/publications/mad-rl/">Read the Paper</a>'
        '<h4>Second Paper</h4>'
        '<a href="/research/publications/second/">Read the Paper</a>'
    )
    papers, provenance, failures, stats = discover_external(
        [source], client=Client(), fetcher=lambda _: html,
    )
    assert not failures
    assert [paper.arxiv_id for paper in papers] == ["2609.31644"]
    assert provenance["2609.31644"][0]["relation"] == "exact-title"
    assert stats[0]["title_lookups_attempted"] == 1
    assert stats[0]["unresolved_publications"] == [{
        "title": "Second Paper", "url": "https://ai.meta.com/research/publications/second/",
    }]


def test_title_lookup_budget_prefers_relevant_track_before_page_order():
    source = DiscoverySource(
        "Google", "official-research", "https://research.google/pubs/",
        max_title_lookups=1,
    )
    class Client:
        def search(self, title, *, limit, match):
            assert title == "Recommendation Ranker"
            return []
        def lookup(self, ids):
            assert list(ids) == []
            return []
    html = (
        '<a href="/pubs/biology-study/">Biology Study</a>'
        '<a href="/pubs/recommendation-ranker/">Recommendation Ranker</a>'
    )
    _, _, _, stats = discover_external(
        [source], client=Client(), fetcher=lambda _: html, track="recommendation",
    )
    assert stats[0]["title_lookups_attempted"] == 1


def test_official_publication_date_recalls_older_arxiv_submission():
    meta = DiscoverySource(
        "Meta", "official-research", "https://ai.meta.com/global_search/?page=1"
    )
    records = publication_records(
        meta,
        '<p>September 24, 2026</p><h4>MaD-RL</h4>'
        '<a href="/research/publications/mad-rl/">Read the Paper</a>',
    )
    assert records[0][2] == "2026-09-24"
    paper = Paper("MaD-RL", "", [], "2026-08-12", "", "2608.31644v1")
    provenance = {"2608.31644": [{
        "relation": "exact-title", "source_published": "2026-09-24",
    }]}
    assert external_paper_in_window(
        paper, provenance, start_date=dt.date(2026, 9, 20),
        end_date=dt.date(2026, 9, 29),
    )
    assert not external_paper_in_window(
        paper, provenance, start_date=dt.date(2026, 9, 25),
        end_date=dt.date(2026, 9, 29),
    )


def test_official_provenance_survives_when_paper_already_found_by_arxiv():
    paper = Paper("A New Method", "", [], "2026-09-20", "", "2609.12345")
    official = {"source": "Google Research", "relation": "exact-title"}
    merged = merge_external_candidates(
        [DiscoveredPaper(paper, ("llm-architecture",))], [],
        {paper.arxiv_id: [official]},
    )
    assert merged[0].source_provenance == (official,)
    assert merged[0].query_names == ("llm-architecture",)


def test_summary_discloses_partial_official_listing_coverage():
    payload = build_discovery_payload(
        track="post-training", start_date=dt.date(2026, 9, 20),
        end_date=dt.date(2026, 9, 29), query_names=(), candidates=[],
    )
    payload["cross_source"] = {
        "source_failures": [],
        "source_stats": [{
            "source": "Meta", "status": "partial", "exact_title_matches": 1,
            "unresolved_publications": [{"title": "Unmatched", "url": "https://example.org"}],
        }],
    }
    summary = render_discovery_summary(payload)
    assert "官方列表仅部分对账" in summary
    assert "精确匹配 1，未匹配 1" in summary
    assert "不能推进全来源覆盖水位" in summary


def test_terminal_review_batch_requires_every_new_candidate_decision():
    artifact = {
        "track": "recommendation",
        "window": {"start": "2026-08-19", "end": "2026-08-20"},
        "candidates": [{
            "arxiv_id": "2608.12345", "title": "Paper", "repository_status": "new",
            "matched_queries": ["recsys-general"], "source_provenance": [],
        }],
    }
    with pytest.raises(ValueError, match="lack terminal decisions"):
        build_batch(artifact, {"decisions": []}, batch_name="test")
    batch = build_batch(artifact, {"decisions": [{
        "id": "2608.12345", "status": "rejected", "priority": "P1",
        "reason": "no public benchmark",
    }]}, batch_name="test")
    assert batch["candidates"][0]["status"] == "rejected"
    assert batch["candidates"][0]["matched_queries"] == ["recsys-general"]
