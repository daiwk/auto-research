"""Priority historical identities must not disappear behind date/P2 bookkeeping."""
import datetime as dt
import hashlib
import json
from pathlib import Path

import pytest

from auto_research.discovery_history import reconcile_priority_history
from auto_research.discovery_sources import (
    DiscoverySource, discover_external, extract_source_hits, load_sources,
)
from auto_research.models import Paper
from scripts import discover_papers as cli
from scripts import reconcile_priority_history as history_cli

SCIENTIST_TWO = "2609.19644"
EVENT = "https://research.google/conferences-and-events/google-at-colm-2026/"


def paths(tmp_path, *, papers=(), decisions=()):
    manifest, ledger = tmp_path / "manifest.json", tmp_path / "ledger.json"
    manifest.write_text(json.dumps({"papers": list(papers)}))
    ledger.write_text(json.dumps({"batches": [{"candidates": list(decisions)}]}))
    return manifest, ledger


def source(**kwargs):
    return DiscoverySource("Google event", "official-research", EVENT,
                           organization="Google", historical_inventory=True, **kwargs)


class Client:
    def lookup(self, identities):
        return [Paper("ScientistTwo", "Agent mechanism", [], "2026-09-20", "", identity)
                for identity in identities]

    def search(self, *_args, **_kwargs):
        return []


def stats(content=None, *, selected_source=None):
    content = content or f'<a href="https://arxiv.org/html/{SCIENTIST_TWO}v1">Read paper</a>'
    return discover_external([selected_source or source()], client=Client(),
                             fetcher=lambda _url: content, track="agent")[3]


def test_fixed_html_pdf_versions_and_lookalike_domains_are_not_confused():
    hits = extract_source_hits(source(),
        f'https://arxiv.org/html/{SCIENTIST_TWO}v1 https://arxiv.org/pdf/{SCIENTIST_TWO}v2.pdf '
        'https://notarxiv.org/abs/2610.00001 https://arxiv.org.evil.test/abs/2610.00002')
    assert [hit.arxiv_id for hit in hits] == [SCIENTIST_TWO]
    assert hits[0].provenance()["historical_inventory"] is True


def test_missing_scientist_two_has_fixed_capture_and_priority_original_review(tmp_path):
    observed = stats()
    receipt, witness = observed[0]["capture_receipts"][0], observed[0]["inventory_records"][0]
    assert receipt["capture_kind"] == "decoded-text-utf8"
    assert receipt["source_url"] == EVENT and receipt["captured_at"]
    assert witness["observed_version"] == "v1"
    assert witness["decoded_text_sha256"] == receipt["decoded_text_sha256"]
    result = reconcile_priority_history(observed, *paths(tmp_path), expected_sources=[source()])
    assert result["source_identity_count"] == 1
    candidate = result["candidates"][0]
    assert candidate["arxiv_id"] == SCIENTIST_TWO
    assert candidate["reconciliation_status"] == "needs-review"
    assert candidate["review_bucket"] == "priority-fulltext-review"
    assert candidate["full_text_review_required"] and candidate["historical_review_required"]
    assert candidate["priority_source_matches"] == ["Google"]
    assert candidate["method_review_completed"] is False
    assert candidate["automatic_implementation_queue"] is False
    assert result["all_institutional_history_exhaustive"] is False
    assert result["review_watermark_advanced"] is False
    assert result["industrial_online_evidence_accepted"] is False


@pytest.mark.parametrize("old", [
    {"status": "rejected", "resolution": "historical_first_publication", "review_done": True},
    {"status": "rejected", "resolution": "not_selected_this_window_p2",
     "review_scope": "title-abstract-selection", "review_done": True},
    {"status": "rejected", "resolution": "known", "review_done": True},
])
def test_old_date_selection_or_generic_known_does_not_close_priority_method_review(tmp_path, old):
    result = reconcile_priority_history(stats(), *paths(tmp_path, decisions=[old | {"id": SCIENTIST_TWO}]))
    assert result["candidates"][0]["full_text_review_required"] is True
    assert result["candidates"][0]["method_or_cost_review_closed"] is False


def test_explicit_high_cost_done_is_terminal_without_implementation_or_new_review(tmp_path):
    decision = {"id": SCIENTIST_TWO, "status": "deferred", "resolution": "not_reproduced_high_cost",
                "reason": "Published multi-node training exceeds one GPU", "review_done": True,
                "cost_assessment": {"basis": "Methods configuration", "source_url": EVENT}}
    result = reconcile_priority_history(stats(), *paths(tmp_path, decisions=[decision]))
    row = result["candidates"][0]
    assert row["reconciliation_status"] == "reviewed" and not row["full_text_review_required"]
    assert row["method_or_cost_review_closed"] is True and row["method_review_completed"] is False
    assert row["prior_disposition"]["resolution"] == "not_reproduced_high_cost"
    assert row["automatic_retry"] is False and row["automatic_implementation_queue"] is False


def test_source_archive_remains_nonblocking_not_fake_fulltext(tmp_path):
    decision = {"id": SCIENTIST_TWO, "status": "deferred", "resolution": "source_exception_archived",
                "source_exception": {"source_url": EVENT, "error": "HTTP404", "attempted_at": "2026-11-13"}}
    row = reconcile_priority_history(stats(), *paths(tmp_path, decisions=[decision]))["candidates"][0]
    assert row["reconciliation_status"] == "archived-exception"
    assert row["full_text_review_required"] is False and row["method_review_completed"] is False


def test_accepted_unimplemented_remains_a_review_opportunity_not_an_automatic_task(tmp_path):
    decision = {"id": SCIENTIST_TWO, "status": "deferred", "review_decision": "accepted",
                "implementation_status": "not_implemented", "full_text_review": {
                    "scope": "full-text", "source_locations": ["Methods", "Experiments"]}}
    row = reconcile_priority_history(stats(), *paths(tmp_path, decisions=[decision]))["candidates"][0]
    assert row["reconciliation_status"] == "accepted-unimplemented"
    assert row["method_review_completed"] is True and row["full_text_review_required"] is False
    assert row["automatic_implementation_queue"] is False


def test_exact_identity_deduplicates_repeated_sources_but_not_similar_titles(tmp_path):
    observed = stats(f'<a href="https://arxiv.org/abs/{SCIENTIST_TWO}v1">Same Title</a>'
                     f'<a href="https://arxiv.org/pdf/{SCIENTIST_TWO}v2">Same Title</a>')
    observed += stats(selected_source=DiscoverySource("Google project", "author-page",
        "https://research.google/projects/related/", organization="Google", historical_inventory=True))
    papers = [{"paper_url": "https://arxiv.org/abs/2609.00001", "title": "Same Title"}]
    result = reconcile_priority_history(observed, *paths(tmp_path, papers=papers))
    assert result["source_identity_count"] == 1
    assert result["candidates"][0]["reconciliation_status"] == "needs-review"
    assert len(result["candidates"][0]["inventory_witnesses"]) == 3
    papers.append({"paper_url": f"https://arxiv.org/abs/{SCIENTIST_TWO}", "title": "Different title",
                   "implementation_status": "component_only"})
    result = reconcile_priority_history(observed, *paths(tmp_path, papers=papers))
    assert result["source_identity_count"] == 1
    assert result["candidates"][0]["reconciliation_status"] == "catalogued"
    assert result["needs_original_review_count"] == 0


def test_fixed_identity_survives_arxiv_metadata_lookup_outage(tmp_path):
    class Offline(Client):
        def lookup(self, identities):
            raise OSError("metadata endpoint unavailable")
    _, provenance, errors, observed = discover_external([source()], client=Offline(),
        fetcher=lambda _: f'https://arxiv.org/abs/{SCIENTIST_TWO}v1')
    assert SCIENTIST_TWO in provenance and errors
    result = reconcile_priority_history(observed, *paths(tmp_path))
    assert result["source_identity_count"] == 1 and result["needs_original_review_count"] == 1


def test_unavailable_uncovered_empty_or_unwitnessed_inventory_is_explicit(tmp_path):
    class Down:
        def __call__(self, _url):
            raise OSError("HTTP503")
    observed = discover_external([source()], client=Client(), fetcher=Down())[3]
    result = reconcile_priority_history(observed, *paths(tmp_path), expected_sources=[source()])
    assert result["source_identity_count"] == 0
    assert {row["type"] for row in result["exceptions"]} == {"source_unavailable", "capture_unavailable"}
    assert any(row["attempted"] for row in result["exceptions"])
    result = reconcile_priority_history([], *paths(tmp_path), expected_sources=[source()])
    assert result["exceptions"][0]["type"] == "inventory_not_captured"
    assert result["exceptions"][0]["attempted"] is False
    observed = stats('<h1>ScientistTwo</h1>')
    result = reconcile_priority_history(observed, *paths(tmp_path))
    assert result["exceptions"][0]["type"] == "identity_unresolved"
    observed = stats()
    observed[0]["inventory_records"][0]["decoded_text_sha256"] = "0" * 64
    result = reconcile_priority_history(observed, *paths(tmp_path))
    assert result["source_identity_count"] == 0
    assert result["exceptions"][0]["type"] == "invalid_inventory_identity"


def test_existing_pagination_budget_is_reused_and_partial_history_is_not_exhaustive(tmp_path):
    selected = DiscoverySource("Google directory", "official-research", "https://research.google/pubs/",
                               organization="Google", historical_inventory=True, max_pages=1)
    observed = stats(f'<div data-max-pages="4">https://arxiv.org/abs/{SCIENTIST_TWO}</div>',
                     selected_source=selected)
    assert observed[0]["pagination_capped"] is True
    result = reconcile_priority_history(observed, *paths(tmp_path))
    assert "pages_uncovered" in {row["type"] for row in result["exceptions"]}
    assert result["source_identity_count"] == 1 and not result["all_institutional_history_exhaustive"]


def test_priority_old_p2_can_pass_dates_but_nonpriority_or_closed_cost_cannot():
    paper = Paper("ScientistTwo", "", [], "2026-09-20", "", SCIENTIST_TWO)
    kwargs = {"start_date": dt.date(2026, 11, 12), "end_date": dt.date(2026, 11, 13)}
    provenance = {SCIENTIST_TWO: [{"source_url": EVENT, "organization": "Google"}]}
    assert cli.external_paper_in_window(paper, provenance,
        repository_statuses={SCIENTIST_TWO: "selection-reviewed"}, **kwargs)
    assert not cli.external_paper_in_window(paper, {SCIENTIST_TWO: [{"organization": "Other"}]},
        repository_statuses={SCIENTIST_TWO: "selection-reviewed"}, **kwargs)
    assert not cli.external_paper_in_window(paper, provenance,
        repository_statuses={SCIENTIST_TWO: "reviewed"}, **kwargs)


def test_default_config_registers_independent_historical_event_inventory():
    configured = load_sources(Path("configs/paper-discovery-sources.json"), "agent")
    assert any(item.url == EVENT and item.historical_inventory for item in configured)


@pytest.mark.parametrize("name,budgets", [
    ("Google Research publications", (40, 5, 12)),
    ("Google Research recent cross-year publications", (2, 3, 6)),
    ("Google DeepMind publications", (20, 5, 12)),
    ("Meta AI publications", (6, 5, 12)),
])
def test_existing_institutional_inventory_flags_do_not_expand_fetch_budgets(name, budgets):
    configured = {item.name: item for item in load_sources(
        Path("configs/paper-discovery-sources.json"), "agent")}
    selected = configured[name]
    assert selected.historical_inventory is True
    assert (selected.max_pages, selected.max_title_lookups, selected.max_detail_lookups) == budgets
    assert selected.review_policy == "incremental"


@pytest.mark.parametrize("terminal,has_identity", [(False, True), (True, True), (True, False)])
def test_default_official_run_writes_history_even_without_recent_announcement_delta(
        tmp_path, monkeypatch, terminal, has_identity):
    decision = ({"id": SCIENTIST_TWO, "status": "deferred", "resolution": "not_reproduced_high_cost",
                 "reason": "Published multi-node budget exceeds one GPU"} if terminal else {
                     "id": SCIENTIST_TWO, "status": "rejected", "resolution": "not_selected_this_window_p2",
                     "review_scope": "title-abstract-selection"})
    manifest, ledger = paths(tmp_path, decisions=[decision])
    config = tmp_path / "sources.json"
    config.write_text(json.dumps({"sources": [vars(source())]}))
    output = tmp_path / "paper-candidates-agent.json"
    monkeypatch.setattr(cli, "ArxivClient", lambda **_: Client())
    monkeypatch.setattr(cli, "discover_candidates", lambda *_args, **_kwargs: [])
    original = cli.discover_external
    monkeypatch.setattr(cli, "discover_external", lambda sources, **kwargs: original(sources,
        fetcher=lambda _: f'https://arxiv.org/abs/{SCIENTIST_TWO}v1' if has_identity else '<h1>No fixed ID</h1>',
        **kwargs))
    Client.query_reports = []
    monkeypatch.setattr("sys.argv", ["discover_papers.py", "--track", "agent", "--skip-announcements",
        "--start-date", "2026-11-12", "--end-date", "2026-11-13", "--cross-source-config", str(config),
        "--manifest", str(manifest), "--ledger", str(ledger), "--reviewed-versions", str(tmp_path / "absent.json"),
        "--output", str(output)])
    before = ledger.read_bytes()
    assert cli.main() == 0
    payload = json.loads(output.read_text())
    report = json.loads(output.with_name(output.stem + "-historical-review.json").read_text())
    assert report["source_identity_count"] == int(has_identity)
    assert report["needs_original_review_count"] == int(has_identity and not terminal)
    if not terminal:
        assert payload["candidates"][0]["arxiv_id"] == SCIENTIST_TWO
        assert payload["candidates"][0]["historical_review_required"] is True
        assert payload["candidates"][0]["automatic_implementation_queue"] is False
    else:
        assert payload["candidates"] == []
    # Retrieval can succeed while a fixed identity still needs method review,
    # or while a captured shell has no fixed identity. These are different axes.
    assert payload["cross_source"]["source_retrieval_complete"] is True
    expected_complete = terminal and has_identity
    assert payload["cross_source"]["historical_review_complete"] is expected_complete
    assert payload["cross_source"]["coverage_complete"] is expected_complete
    assert payload["cross_source"]["historical_review_scope"] == "configured captured source identities only"
    assert report["all_institutional_history_exhaustive"] is False
    assert report["review_watermark_advanced"] is False
    assert ledger.read_bytes() == before
    assert payload["cross_source"]["historical_review"] == report


def test_saved_inventory_cli_is_portable_without_source_cache(tmp_path, monkeypatch, capsys):
    manifest, ledger = paths(tmp_path)
    config = tmp_path / "sources.json"
    config.write_text(json.dumps({"sources": [vars(source())]}))
    artifact = tmp_path / "inventory.json"
    artifact.write_text(json.dumps({"source_stats": stats()}))
    monkeypatch.setattr("sys.argv", ["reconcile_priority_history.py", "--artifact", str(artifact),
        "--manifest", str(manifest), "--ledger", str(ledger), "--source-config", str(config)])
    original = Path.read_text
    def no_cache(path, *args, **kwargs):
        assert ".cache" not in path.relative_to(tmp_path).parts
        return original(path, *args, **kwargs)
    monkeypatch.setattr(Path, "read_text", no_cache)
    assert history_cli.main() == 0
    report = json.loads(capsys.readouterr().out)
    assert report["needs_original_review_count"] == 1
    assert report["automatic_implementation_queue"] is False


def test_decoded_capture_hash_is_explicitly_not_a_network_byte_claim():
    content = f'<a href="https://arxiv.org/abs/{SCIENTIST_TWO}">论文</a>'
    receipt = stats(content)[0]["capture_receipts"][0]
    assert receipt["decoded_text_sha256"] == hashlib.sha256(content.encode()).hexdigest()
    assert receipt["decoded_text_bytes"] == len(content.encode())
    assert "raw_sha256" not in receipt


@pytest.mark.parametrize("field,value", [
    ("identity_url", "https://arxiv.org/abs/2609.19643v1"),
    ("identity_url", "https://arxiv.org.evil.test/abs/2609.19644v1"),
    ("observed_version", "v2"),
    ("arxiv_id", "2609.19644v1"),
])
def test_identity_version_and_url_witness_must_agree_exactly(tmp_path, field, value):
    observed = stats()
    observed[0]["inventory_records"][0][field] = value
    result = reconcile_priority_history(observed, *paths(tmp_path))
    assert result["source_identity_count"] == 0
    assert result["exceptions"][0]["type"] == "invalid_inventory_identity"
