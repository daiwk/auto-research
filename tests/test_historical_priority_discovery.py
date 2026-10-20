"""Date-only bookkeeping must never hide an unreviewed priority paper."""
import json

import pytest

from auto_research.discovery import (
    DiscoveredPaper, repository_paper_statuses, triage_candidates,
)
from auto_research.discovery_review import classify_candidate
from auto_research.models import Paper
from scripts.record_discovery_review import build_batch
from scripts.discover_papers import external_paper_in_window
import datetime as dt


def _candidate(**overrides):
    return {
        "arxiv_id": "2610.14224", "title": "Harness^2",
        "abstract": "Recursive self-improvement of agent harnesses.",
        "repository_status": "new", "matched_queries": ["llm-agent"],
        **overrides,
    }


def _statuses(tmp_path, rows, papers=()):
    manifest, ledger = tmp_path / "manifest.json", tmp_path / "ledger.json"
    manifest.write_text(json.dumps({"papers": list(papers)}))
    ledger.write_text(json.dumps({"batches": [{"candidates": rows}]}))
    return repository_paper_statuses(manifest, ledger)


def test_harness2_date_only_rejection_is_not_a_reviewed_identity(tmp_path):
    statuses = _statuses(tmp_path, [{
        "id": "2610.14224", "status": "rejected", "priority": "P2",
        "resolution": "historical_first_publication", "review_done": True,
        "reason": "2026-10-09 precedes the current window; metadata only",
    }])
    assert statuses.get("2610.14224", "new") == "new"


def test_later_real_cost_closure_stays_terminal_and_catalog_is_authoritative(tmp_path):
    rows = [
        {"id": "2610.14224", "status": "rejected",
         "resolution": "historical_first_publication"},
        {"id": "2610.14224", "status": "deferred",
         "resolution": "not_reproduced_high_cost", "reason": "Full model benchmark cost assessed"},
        {"id": "2610.14224", "status": "historical",
         "review_scope": "historical_metadata_identity_date_scope_only"},
    ]
    assert _statuses(tmp_path, rows) == {"2610.14224": "reviewed"}
    assert _statuses(tmp_path, rows, [{"paper_url": "https://arxiv.org/abs/2610.14224"}]) == {
        "2610.14224": "implemented",
    }


@pytest.mark.parametrize("signal", [
    {"source_provenance": [{"organization": "Google", "source_url": "https://research.google/pubs/harness2/"}]},
    {"source_provenance": [{"source_url": "https://github.com/google-research/harness2"}]},
    {"source_provenance": [{"source_url": "https://github.com/facebookresearch/project"}]},
    {"source_provenance": [{"source_url": "https://github.com/facebook/meta-encoder-eval"}]},
    {"source_provenance": [{"source_url": "https://github.com/google/project"}]},
    {"first_author_affiliation": "Google DeepMind"},
    {"priority_review_required": True},
])
def test_official_priority_source_is_not_lost_without_an_org_query(signal):
    row = classify_candidate("agent", _candidate(**signal))
    assert row["review_bucket"] == "priority-fulltext-review"
    assert row["full_text_review_required"] is True


@pytest.mark.parametrize("url", [
    "https://github.com.evil.invalid/google-research/harness2",
    "https://github.com/not-google-research/harness2",
    "https://research.google.evil.invalid/pubs/",
])
def test_lookalike_domains_and_meta_learning_are_not_priority_affiliations(url):
    row = classify_candidate("agent", _candidate(
        title="Meta-learning for agent prompts", source_provenance=[{"source_url": url}],
    ))
    assert row["review_bucket"] != "priority-fulltext-review"


def test_legacy_version_baseline_cannot_hide_metadata_only_history(tmp_path):
    paper = Paper("Harness^2", "Recursive agent harnessing", ["Researcher"],
                  "2026-10-09T18:34:25Z", "https://arxiv.org/abs/2610.14224v1", "2610.14224v1")
    result = triage_candidates(
        [DiscoveredPaper(paper, (), ({"source_url": "https://github.com/google-research/harness2"},))],
        _statuses(tmp_path, [{
            "id": "2610.14224", "status": "rejected",
            "resolution": "historical_first_publication", "review_done": True,
        }]),
        repository_versions={"2610.14224": {
            "revision": 1, "review_scope": "historical_metadata_identity_date_scope_only",
        }},
    )[0]
    assert result["historical_review_required"] is True
    assert result["review_required"] is result["priority_review_required"] is True
    assert result["revision_review_required"] is False  # No invented new version.


def test_real_later_closure_overrides_an_old_metadata_version_baseline(tmp_path):
    paper = Paper("Harness^2", "Recursive agent harnessing", ["Researcher"],
                  "2026-10-09T18:34:25Z", "https://arxiv.org/abs/2610.14224v1", "2610.14224v1")
    statuses = _statuses(tmp_path, [{
        "id": "2610.14224", "status": "deferred", "resolution": "not_reproduced_high_cost",
    }])
    result = triage_candidates(
        [DiscoveredPaper(paper, (), ({"source_url": "https://github.com/google-research/harness2"},))],
        statuses, repository_versions={"2610.14224": {
            "revision": 1, "review_scope": "historical_metadata_identity_date_scope_only",
        }},
    )[0]
    assert result["review_required"] is result["historical_review_required"] is False


@pytest.mark.parametrize("status", ["rejected", "deferred", "implemented"])
def test_recording_gate_rejects_date_only_terminal_dispositions(status):
    artifact = {"track": "agent", "candidates": [_candidate()]}
    decisions = {"decisions": [{
        "id": "2610.14224", "priority": "P2", "status": status,
        "resolution": "historical_first_publication", "reason": "Before the window",
    }]}
    with pytest.raises(ValueError, match="metadata-only"):
        build_batch(artifact, decisions, batch_name="invalid-date-closure")


def test_recording_gate_enforces_priority_review_from_official_repository():
    artifact = {"track": "agent", "candidates": [_candidate(source_provenance=[{
        "source_url": "https://github.com/google-research/harness2",
    }])]}
    decisions = {"decisions": [{
        "id": "2610.14224", "priority": "P2", "status": "rejected",
        "reason": "Abstract only",
    }]}
    with pytest.raises(ValueError, match="full_text_review"):
        build_batch(artifact, decisions, batch_name="invalid-priority-closure")


def test_archived_unavailable_source_is_not_retried_as_date_only_history(tmp_path):
    assert _statuses(tmp_path, [{
        "id": "2610.14224", "status": "rejected", "resolution": "source_unavailable_archived",
        "review_scope": "source_exception_archived_identity_only", "reason": "Primary source unavailable",
    }]) == {"2610.14224": "reviewed"}


def test_new_official_priority_evidence_survives_cross_month_window_filter():
    paper = Paper("Harness^2", "Recursive agent harnessing", ["Researcher"],
                  "2026-10-09T18:34:25Z", "https://arxiv.org/abs/2610.14224", "2610.14224")
    provenance = {"2610.14224": [{"source_url": "https://github.com/google-research/harness2"}]}
    settings = {"start_date": dt.date(2026, 11, 1), "end_date": dt.date(2026, 11, 3)}
    assert external_paper_in_window(paper, provenance, repository_statuses={}, **settings)
    assert not external_paper_in_window(
        paper, provenance, repository_statuses={"2610.14224": "reviewed"}, **settings,
    )
    assert not external_paper_in_window(
        paper, provenance, repository_statuses={"2610.14224": "implemented"}, **settings,
    )
    assert not external_paper_in_window(paper, {}, repository_statuses={}, **settings)


@pytest.mark.parametrize("review_done", [False, True])
def test_accepted_pending_delivery_is_visible_but_real_cost_closure_wins(tmp_path, review_done):
    pending = {"id": "2610.07338", "status": "deferred", "review_decision": "accepted",
               "implementation_status": "not_implemented", "reason": "审查通过，待核心算法实现",
               "review_done": review_done}
    assert _statuses(tmp_path, [pending]) == {"2610.07338": "implementation-pending"}
    row = classify_candidate("foundation-model", _candidate(repository_status="implementation-pending"))
    assert row["review_bucket"] == "implementation-pending"
    assert row["full_text_review_required"] is False  # Already reviewed, not implemented.
    closed = {"id": "2610.07338", "status": "deferred", "review_done": True,
              "resolution": "not_reproduced_high_cost", "reason": "Cost reviewed; not reproduced"}
    assert _statuses(tmp_path, [pending, closed]) == {"2610.07338": "reviewed"}


@pytest.mark.parametrize("review_done", [False, True])
def test_recording_gate_does_not_claim_pending_delivery_as_terminal(review_done):
    artifact = {"track": "agent", "candidates": [_candidate()]}
    decisions = {"decisions": [{
        "id": "2610.14224", "priority": "P1", "status": "deferred", "review_decision": "accepted",
        "implementation_status": "not_implemented", "reason": "审查通过，待核心算法实现",
        "review_done": review_done,
    }]}
    with pytest.raises(ValueError, match="implementation-pending"):
        build_batch(artifact, decisions, batch_name="invalid-pending-closure")


def test_official_priority_backfill_never_recalls_explicit_future_publication():
    paper = Paper("Future paper", "Agent research", ["Researcher"],
                  "2026-12-01T00:00:00Z", "https://arxiv.org/abs/2612.00001", "2612.00001")
    assert not external_paper_in_window(
        paper, {"2612.00001": [{"source_url": "https://github.com/google-research/project"}]},
        start_date=dt.date(2026, 11, 1), end_date=dt.date(2026, 11, 3), repository_statuses={},
    )


def test_legacy_metadata_review_level_is_not_a_substantive_closure(tmp_path):
    assert _statuses(tmp_path, [{
        "id": "2610.14224", "status": "rejected", "review_done": True,
        "review_level": "historical_metadata_abstract_scope_triage",
    }]) == {}


def test_a_generic_known_resolution_cannot_hide_structured_pending_delivery(tmp_path):
    assert _statuses(tmp_path, [{
        "id": "2610.07338", "status": "deferred", "review_decision": "accepted",
        "implementation_status": "not_implemented", "resolution": "known",
        "reason": "Accepted, pending implementation", "review_done": True,
    }]) == {"2610.07338": "implementation-pending"}


@pytest.mark.parametrize("reverse", [False, True])
def test_generic_known_row_never_overrides_an_accepted_pending_row(tmp_path, reverse):
    rows = [{"id": "2610.07338", "status": "deferred", "review_decision": "accepted",
             "implementation_status": "not_implemented", "reason": "待核心算法实现"},
            {"id": "2610.07338", "status": "rejected", "resolution": "known", "review_done": True}]
    assert _statuses(tmp_path, rows[::-1] if reverse else rows) == {
        "2610.07338": "implementation-pending",
    }


def test_explicit_cost_closure_wins_over_retained_old_metadata_fields(tmp_path):
    assert _statuses(tmp_path, [{
        "id": "2610.14224", "status": "deferred", "resolution": "not_reproduced_high_cost",
        "review_scope": "historical_metadata_identity_date_scope_only", "review_done": True,
        "reason": "Full model benchmark beyond budget",
    }]) == {"2610.14224": "reviewed"}


def test_discovered_nonterminal_row_is_not_reviewed_and_legacy_cost_stays_closed(tmp_path):
    assert _statuses(tmp_path, [{"id": "2610.14224", "status": "new", "review_done": False}]) == {}
    assert _statuses(tmp_path, [{
        "id": "2610.14224", "status": "deferred", "reason": "成本过高，暂不复现；原文多卡训练",
    }]) == {"2610.14224": "reviewed"}


def test_legacy_next_batch_priority_is_visible_and_explicit_cost_is_not_retried(tmp_path):
    assert _statuses(tmp_path, [{
        "id": "2610.11316", "status": "deferred", "reason": "MetaEncoder 需真实checkpoint评测；保留下一批优先。",
    }]) == {"2610.11316": "implementation-pending"}
    assert _statuses(tmp_path, [{
        "id": "2610.11316", "status": "deferred", "reason": "成本过高，不复现；旧记录曾写待实现。",
    }]) == {"2610.11316": "reviewed"}
