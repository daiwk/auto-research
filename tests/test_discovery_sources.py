import json
import gzip
import io

import pytest

from auto_research.discovery import (
    DiscoveredPaper, build_discovery_payload, merge_external_candidates,
    render_discovery_summary,
)
import datetime as dt
from auto_research.discovery_sources import (
    DiscoverySource, catalog_papers_from_manifest, discover_external, extract_source_hits,
    fetch_text, official_review_queue, page_url,
    publication_records, normalized_title, load_source_snapshots,
    semantic_scholar_citation_hits,
)
from auto_research.models import Paper
from scripts.record_discovery_review import build_batch
from scripts.discover_papers import external_paper_in_window
from scripts.build_discovery_source_snapshot import build_snapshot


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


def test_fetch_text_decodes_gzip_even_when_origin_omits_content_encoding(monkeypatch):
    response = io.BytesIO(gzip.compress(b"<html>official listing</html>"))
    response.headers = {"Content-Type": "text/html"}
    monkeypatch.setattr("urllib.request.urlopen", lambda request, timeout: response)
    assert fetch_text("https://example.org/") == "<html>official listing</html>"


def test_github_token_is_only_sent_to_https_github_api(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    requests = []

    def fake_urlopen(request, timeout):
        requests.append(request)
        response = io.BytesIO(b"{}")
        response.headers = {"Content-Type": "application/json"}
        return response

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    fetch_text("https://api.github.com/orgs/google-research/repos")
    fetch_text("https://example.org/")
    fetch_text("http://api.github.com/")
    assert requests[0].get_header("Authorization") == "Bearer test-token"
    assert requests[1].get_header("Authorization") is None
    assert requests[2].get_header("Authorization") is None


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
        "transport_status": "ok", "review_policy": "incremental", "track": "all",
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
    (
        "https://ai.meta.com/results/?content_types%5B0%5D=publication&page=1",
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


def test_official_detail_page_resolves_arxiv_before_title_search():
    source = DiscoverySource(
        "Google", "official-research", "https://research.google/pubs/",
        organization="Google", max_detail_lookups=1,
    )
    listing = '<a href="/pubs/agent-memory/">Agent Memory</a>'

    def fetcher(url):
        if url == source.url:
            return listing
        assert url == "https://research.google/pubs/agent-memory/"
        return '<a href="https://arxiv.org/abs/2609.12345v2">Download</a>'

    class Client:
        def lookup(self, ids):
            assert list(ids) == ["2609.12345"]
            return [Paper("Agent Memory", "", [], "2026-09-29", "", "2609.12345")]

    papers, provenance, failures, stats = discover_external(
        [source], client=Client(), fetcher=fetcher, track="agent",
    )
    assert not failures
    assert [paper.arxiv_id for paper in papers] == ["2609.12345"]
    assert provenance["2609.12345"][0]["relation"] == "official-detail"
    assert stats[0]["detail_lookups_attempted"] == 1
    assert stats[0]["unresolved_publications"] == []


def test_deepmind_listing_extracts_dated_official_cards_only():
    source = DiscoverySource(
        "DeepMind", "official-research", "https://deepmind.google/research/publications/"
    )
    html = (
        '<a href="/research/publications/265605/">'
        '<span class="list-group__date">1 September 2026</span>'
        '<span class="list-group__description">Designing Proactive Thought Partners '
        'for Writing</span></a>'
        '<a href="/research/publications/">All publications</a>'
    )
    assert publication_records(source, html) == ((
        "Designing Proactive Thought Partners for Writing",
        "https://deepmind.google/research/publications/265605/", "2026-09-01",
    ),)


def test_deepmind_pagination_follows_official_paths_and_reports_cap():
    source = DiscoverySource(
        "DeepMind", "official-research", "https://deepmind.google/research/publications/",
        max_pages=2,
    )
    requested = []

    def fetcher(url):
        requested.append(url)
        page = len(requested)
        return (
            '<a href="/research/publications/page/2/">2</a>'
            '<a href="/research/publications/page/3/">3</a>'
            f'<a href="/research/publications/{page}/">'
            f'<span class="list-group__description">Paper {page}</span></a>'
        )

    class Client:
        def lookup(self, ids):
            assert not ids
            return []

    _, _, failures, stats = discover_external([source], client=Client(), fetcher=fetcher)
    assert not failures
    assert requested == [source.url, "https://deepmind.google/research/publications/page/2/"]
    assert stats[0]["pages_scanned"] == 2
    assert stats[0]["pages_available"] == 3
    assert stats[0]["pagination_capped"] is True
    assert stats[0]["official_publications"] == 2


def test_google_directory_uses_declared_page_count_and_preserves_year_filter():
    source = DiscoverySource(
        "Google", "official-research",
        "https://research.google/pubs/?category=2026&sort=-publication__year",
        max_pages=40,
    )
    requested = []

    def fetcher(url):
        requested.append(url)
        return ('<form data-max-pages="2"></form>'
                f'<a href="/pubs/paper-{len(requested)}/">Paper {len(requested)}</a>')

    class Client:
        def lookup(self, ids):
            assert not ids
            return []

    _, _, failures, stats = discover_external([source], client=Client(), fetcher=fetcher)
    assert not failures
    assert len(requested) == 2
    assert "category=2026" in requested[1] and "page=2" in requested[1]
    assert stats[0]["pages_available"] == 2
    assert stats[0]["pagination_capped"] is False
    # Fetching both pages still leaves their paper identities unresolved.
    assert len(stats[0]["unresolved_publications"]) == 2


def test_google_directory_reports_truncation_even_when_fetched_pages_succeed():
    source = DiscoverySource("Google", "official-research",
                             "https://research.google/pubs/", max_pages=2)

    class Client:
        def lookup(self, ids):
            return []

    _, _, failures, stats = discover_external(
        [source], client=Client(),
        fetcher=lambda url: '<form data-max-pages="27"></form>'
                            '<a href="/pubs/example/">Example</a>',
    )
    assert not failures
    assert stats[0]["pages_available"] == 27
    assert stats[0]["pagination_capped"] is True


def test_one_failed_listing_page_preserves_other_pages_and_reports_gap():
    source = DiscoverySource(
        "Google", "official-research", "https://research.google/pubs/",
        max_pages=3,
    )

    def fetcher(url):
        if "page=2" in url:
            raise TimeoutError("page unavailable")
        return (
            f'<a href="/pubs/paper-{url[-1]}/">'
            f'Paper {url[-1]}</a>'
        )

    class Client:
        def lookup(self, ids):
            assert not ids
            return []

    _, _, failures, stats = discover_external(
        [source], client=Client(), fetcher=fetcher,
    )
    assert failures == [{
        "source": "Google", "url": page_url(source.url, 2),
        "page": 2, "error": "page unavailable",
    }]
    assert stats[0]["status"] == "partial"
    assert stats[0]["pages_scanned"] == 2
    assert stats[0]["official_publications"] == 2
    assert stats[0]["page_failures"] == failures


def test_manifest_exact_title_is_counted_as_already_cataloged(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({"papers": [
        {"title": "RankGraph-2", "paper_url": "https://arxiv.org/abs/2606.18379"},
        {"title": "No arXiv paper", "paper_url": "https://example.org/paper"},
    ]}), encoding="utf-8")
    catalog = catalog_papers_from_manifest(path)
    assert [paper.arxiv_id for paper in catalog] == ["2606.18379"]

    class Client:
        def lookup(self, ids):
            assert not ids
            return []

    source = DiscoverySource(
        "RecSys", "official-conference", "https://recsys.acm.org/recsys26/session-2/"
    )
    html = (
        '<a rel="#accordion-1-slide-1"><span class="paper-type">IND</span>'
        'RankGraph-2<br />by Authors</a>'
    )
    _, provenance, failures, stats = discover_external(
        [source], client=Client(), fetcher=lambda _: html,
        catalog_papers=iter(catalog),
    )
    assert not failures
    assert provenance["2606.18379"][0]["relation"] == "exact-title"
    assert stats[0]["catalog_title_matches"] == 1
    assert stats[0]["unresolved_publications"] == []


def test_official_review_queue_groups_titles_without_claiming_identity():
    stats = [
        {"source": "RecSys", "organization": "ACM RecSys", "unresolved_publications": [
            {"title": "New Ranking Paper", "url": "https://recsys.acm.org/a"},
        ]},
        {"source": "Google", "organization": "Google", "unresolved_publications": [
            {"title": "New Ranking Paper", "url": "https://research.google/a",
             "source_published": "2026-09-29"},
            {"title": "Other Google Paper", "url": "https://research.google/b",
             "source_published": "2026-09-28"},
        ]},
    ]
    queue = official_review_queue(stats)
    assert len(queue) == 2
    assert queue[0]["title"] == "New Ranking Paper"
    assert queue[0]["review_state"] == "identity_unresolved"
    assert queue[0]["google_meta_priority"] is True
    assert len(queue[0]["sources"]) == 2
    assert queue[0]["source_published"] == "2026-09-29"


def test_official_review_queue_filters_dated_history_but_keeps_undated_review_items():
    stats = [{
        "source": "Google", "organization": "Google",
        "unresolved_publications": [
            {"title": "Old paper", "url": "https://example/old", "source_published": "2025-01-01"},
            {"title": "Current paper", "url": "https://example/new", "source_published": "2026-09-29"},
            {"title": "Needs date review", "url": "https://example/undated"},
            {"title": "2", "url": "https://example/pagination"},
        ],
    }]
    queue = official_review_queue(
        stats, start_date=dt.date(2026, 9, 27), end_date=dt.date(2026, 9, 30),
    )
    assert {item["title"] for item in queue} == {"Current paper", "Needs date review"}


def test_official_review_queue_excludes_static_snapshot_and_cross_track_noise():
    stats = [
        {
            "source": "SIGIR", "organization": "ACM SIGIR",
            "review_policy": "snapshot", "track": "recommendation",
            "unresolved_publications": [],
        },
        {
            "source": "Google", "organization": "Google", "track": "agent",
            "unresolved_publications": [
                {"title": "Quantum Chemistry", "url": "https://google.example/q"},
                {"title": "Agent Memory", "url": "https://google.example/a"},
            ],
        },
    ]
    queue = official_review_queue(stats)
    assert [item["title"] for item in queue] == ["Agent Memory"]


def test_static_snapshot_only_reviews_new_titles(tmp_path):
    snapshot_path = tmp_path / "snapshots.json"
    snapshot_path.write_text(json.dumps({
        "sources": {"SIGIR": ["Known Ranking Paper"]},
    }), encoding="utf-8")
    snapshots = load_source_snapshots(snapshot_path)
    source = DiscoverySource(
        "SIGIR", "official-conference",
        "https://sigir2026.org/en-AU/pages/program/accepted-papers",
        track="recommendation", review_policy="snapshot",
    )
    html = (
        r"\u003cp\u003e[fp] \u003ci\u003eKnown Ranking Paper\u003c/i\u003e"
        r"\u003cp\u003e[fp] \u003ci\u003eNew Search Paper\u003c/i\u003e"
    )

    class Client:
        def lookup(self, ids):
            assert not ids
            return []

    _, _, failures, stats = discover_external(
        [source], client=Client(), fetcher=lambda _: html,
        track="recommendation", source_snapshots=snapshots,
    )
    assert not failures
    assert stats[0]["snapshot_baseline_present"] is True
    assert stats[0]["snapshot_publication_titles"] == [
        "Known Ranking Paper", "New Search Paper",
    ]
    assert stats[0]["snapshot_known_publications"] == 1
    assert stats[0]["snapshot_new_publications"] == 1
    assert stats[0]["unresolved_publications"] == [{
        "title": "New Search Paper", "url": source.url,
    }]


def test_snapshot_builder_prefers_complete_publication_inventory():
    artifact = {"cross_source": {"source_stats": [{
        "source": "SIGIR", "snapshot_publication_titles": ["Known", "Resolved"],
        "unresolved_publications": [{"title": "Known"}],
    }]}}
    config = {"sources": [{"name": "SIGIR", "url": "https://example.test",
                            "kind": "official-conference", "review_policy": "snapshot"}]}
    payload = build_snapshot(artifact, config, checked_at="2026-09-30")
    assert payload["sources"] == {"SIGIR": ["Known", "Resolved"]}
    assert "not an acceptance" in payload["note"]


def test_recsys_session_uses_same_paper_header_contract_as_posters():
    source = DiscoverySource(
        "RecSys 2026 session 2", "official-conference",
        "https://recsys.acm.org/recsys26/session-2/", track="recommendation",
    )
    html = (
        '<li><a rel="#accordion-1-slide-1">'
        '<span class="paper-type" title="Research">RES</span>'
        'CONGA: Continual Neural Gated Architecture<br />by Authors</a></li>'
    )
    assert publication_records(source, html) == ((
        "CONGA: Continual Neural Gated Architecture",
        "https://recsys.acm.org/recsys26/session-2/#accordion-1-slide-1", None,
    ),)


def test_recsys_posters_keep_distinct_titles_and_do_not_claim_page_arxiv_links():
    source = DiscoverySource(
        "RecSys 2026 posters 2", "official-conference",
        "https://recsys.acm.org/recsys26/posters-2/", track="recommendation",
    )
    html = (
        '<li><a rel="#accordion-1-slide-1">'
        '<span class="paper-type" title="Research">Spot A1</span>'
        'RankGraph-2: Lifecycle Co-Design<br />by Authors</a></li>'
        '<li><a rel="#accordion-1-slide-2">'
        '<span class="paper-type" title="Research">Spot A2</span>'
        'PROMISE: Process Reward Models<br />by Authors</a></li>'
        '<p>A related reference is arXiv:2609.99999, not a poster identity.</p>'
    )
    records = publication_records(source, html)
    assert [record[0] for record in records] == [
        "RankGraph-2: Lifecycle Co-Design", "PROMISE: Process Reward Models",
    ]
    assert records[0][1].endswith("#accordion-1-slide-1")
    assert records[0][2] is None

    class Client:
        def lookup(self, ids):
            assert list(ids) == []
            return []

    _, provenance, failures, stats = discover_external(
        [source], client=Client(), fetcher=lambda _: html,
    )
    assert provenance == {}
    assert failures == []
    assert stats[0]["arxiv_ids_extracted"] == 0
    assert stats[0]["official_publications"] == 2
    assert len(stats[0]["unresolved_publications"]) == 2
    assert stats[0]["status"] == "partial"


def test_sigir_accepted_papers_deduplicates_serialized_tracks_without_fake_dates():
    source = DiscoverySource(
        "SIGIR 2026 accepted papers", "official-conference",
        "https://sigir2026.org/en-AU/pages/program/accepted-papers",
        track="recommendation",
    )
    html = (
        r"\u003cp\u003e[fp] \u003ci\u003eFirst Ranking Paper\u003c/i\u003e"
        r"\u003cp\u003e[ip] \u003ci\u003eSecond Search Paper\u003c/i\u003e"
        r"\u003cp\u003e[rp] \u003ci\u003eThird Resource Paper\u003c/i\u003e"
        r"\u003cp\u003e[fp] \u003ci\u003eFirst Ranking Paper\u003c/i\u003e"
    )
    records = publication_records(source, html)
    assert records == (
        ("First Ranking Paper", source.url, None),
        ("Second Search Paper", source.url, None),
        ("Third Resource Paper", source.url, None),
    )

    class Client:
        def lookup(self, ids):
            assert list(ids) == []
            return []

    _, provenance, failures, stats = discover_external(
        [source], client=Client(), fetcher=lambda _: html,
    )
    assert provenance == {}
    assert failures == []
    assert stats[0]["official_publications"] == 3
    assert len(stats[0]["unresolved_publications"]) == 3


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
        "official_review_queue_count": 1,
        "official_review_output": "paper-official-review.json",
        "source_stats": [{
            "source": "Meta", "status": "partial", "exact_title_matches": 1,
            "unresolved_publications": [{"title": "Unmatched", "url": "https://example.org"}],
        }],
    }
    summary = render_discovery_summary(payload)
    assert "官方列表仅部分对账" in summary
    assert "精确匹配 1，未匹配 1" in summary
    assert "不能推进全来源覆盖水位" in summary
    assert "paper-official-review.json" in summary


def test_summary_handles_transport_failure_without_reconciliation_counts():
    payload = build_discovery_payload(
        track="recommendation", start_date=dt.date(2026, 10, 1),
        end_date=dt.date(2026, 10, 3), query_names=(), candidates=[],
    )
    payload["cross_source"] = {
        "source_failures": [{"source": "Google Research", "error": "timeout"}],
        "official_review_queue_count": 0,
        "source_stats": [{
            "source": "Google Research", "status": "error",
            "transport_status": "timeout",
        }],
    }
    summary = render_discovery_summary(payload)
    assert "跨来源失败 1 项" in summary
    assert "Google Research（精确匹配 0，未匹配 0）" in summary
    assert "不能推进全来源覆盖水位" in summary


def test_summary_reports_healthy_snapshot_delta_without_false_partial_warning():
    payload = build_discovery_payload(
        track="recommendation", start_date=dt.date(2026, 9, 28),
        end_date=dt.date(2026, 9, 30), query_names=(), candidates=[],
    )
    payload["cross_source"] = {
        "source_failures": [], "official_review_queue_count": 0,
        "coverage_complete": True,
        "source_stats": [{
            "source": "SIGIR", "status": "partial", "transport_status": "ok",
            "review_policy": "snapshot", "snapshot_known_publications": 100,
            "snapshot_new_publications": 0, "unresolved_publications": [],
        }],
    }
    summary = render_discovery_summary(payload)
    assert "静态会议目录按已审快照做增量对账" in summary
    assert "没有遗留身份待核条目" in summary
    assert "官方列表仅部分对账" not in summary


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
