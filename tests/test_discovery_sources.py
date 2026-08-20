import json

import pytest

from auto_research.discovery_sources import (
    DiscoverySource, discover_external, extract_source_hits,
    semantic_scholar_citation_hits,
)
from auto_research.models import Paper
from scripts.record_discovery_review import build_batch


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
    papers, provenance, failures = discover_external(sources, client=Client(), fetcher=fetcher)
    assert papers[0].arxiv_id == "2608.12345"
    assert provenance["2608.12345"][0]["source"] == "ok"
    assert failures == [{"source": "bad", "url": "https://bad", "error": "down"}]


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
