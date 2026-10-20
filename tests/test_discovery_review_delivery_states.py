"""Review decisions do not manufacture delivery or reproduction claims."""
import datetime as dt
import json

import pytest

from auto_research.discovery import (
    DiscoveredPaper, repository_paper_records, repository_paper_statuses,
    triage_candidates, build_discovery_payload, render_discovery_summary,
)
from auto_research.discovery_review import pending_implementation_disposition
from auto_research.models import Paper
from scripts.record_discovery_review import build_batch


def paths(tmp_path, papers=(), rows=()):
    manifest, ledger = tmp_path / "manifest.json", tmp_path / "ledger.json"
    manifest.write_text(json.dumps({"papers": list(papers)}))
    ledger.write_text(json.dumps({"batches": [{"candidates": list(rows)}]}))
    return manifest, ledger


@pytest.mark.parametrize("resolution", ["affordable_candidate_not_implemented", "affordable_core_review_candidate"])
def test_oct15_structured_acceptance_is_not_hidden_by_fulltext_read(tmp_path, resolution):
    row = {"id": "2610.20413", "status": "deferred", "resolution": resolution,
           "full_text_review": {"scope": "full-text", "source_locations": ["§3"]}}
    assert repository_paper_statuses(*paths(tmp_path, rows=[row])) == {
        "2610.20413": "accepted-unimplemented"}
    assert pending_implementation_disposition(row)


@pytest.mark.parametrize("reason", ["下一批须核验", "保留下一批优先", "待实现", "pending implementation"])
def test_prose_is_not_structured_acceptance(tmp_path, reason):
    row = {"id": "2610.20413", "status": "deferred", "reason": reason}
    assert not pending_implementation_disposition(row)
    assert repository_paper_statuses(*paths(tmp_path, rows=[row])) == {"2610.20413": "review-deferred"}


def test_catalog_component_and_full_cost_resolution_coexist(tmp_path):
    record = repository_paper_records(*paths(tmp_path,
        papers=[{"paper_url": "https://arxiv.org/abs/2610.09159", "implementation_status": "component_only"}],
        rows=[{"id": "2610.09159", "status": "deferred", "resolution": "not_reproduced_high_cost"}],
    ))["2610.09159"]
    assert record == {"repository_status": "catalogued", "catalogued": True,
        "implementation_status": "component_only", "automatic_implementation_queue": False,
        "full_experiment_resolution": "not_reproduced_high_cost"}


@pytest.mark.parametrize("reverse", [False, True])
def test_reference_duplicate_cannot_hide_component_catalog_and_no_tier_is_invented(tmp_path, reverse):
    papers = [{"paper_url": "https://arxiv.org/abs/2610.09159", "implementation_status": status}
              for status in ("deferred_high_cost", "component_only")]
    record = repository_paper_records(*paths(tmp_path, papers=papers[::-1] if reverse else papers))["2610.09159"]
    assert record["repository_status"] == "catalogued"
    assert record["catalog_implementation_statuses"] == ["component_only", "deferred_high_cost"]
    assert record["implementation_status"] == "mixed_catalog_entries"


def test_accepted_review_can_close_without_claiming_delivery_or_autoqueue():
    candidate = {"arxiv_id": "2610.20413", "title": "Method", "repository_status": "new",
                 "source_provenance": [{"organization": "Google"}]}
    decision = {"id": "2610.20413", "status": "deferred", "priority": "P1",
        "review_decision": "accepted", "review_done": True, "reason": "Affordable core opportunity",
        "implementation_status": "not_implemented", "automatic_implementation_queue": False,
        "full_text_review": {"scope": "full-text", "source_locations": ["Methods", "Experiments"]}}
    batch = build_batch({"track": "foundation-model", "candidates": [candidate]},
                        {"decisions": [decision]}, batch_name="review-not-delivery")
    assert batch["candidates"][0]["implementation_status"] == "not_implemented"
    assert batch["candidates"][0]["status"] == "deferred"
    for field, value in [("review_done", False), ("automatic_implementation_queue", True)]:
        with pytest.raises(ValueError, match="accepted-unimplemented"):
            build_batch({"track": "foundation-model", "candidates": [candidate]},
                        {"decisions": [{**decision, field: value}]}, batch_name="bad")


def test_source_exception_requires_actual_attempt_evidence_not_fake_fulltext():
    candidate = {"arxiv_id": "2610.20413", "title": "Method", "repository_status": "new",
                 "source_provenance": [{"organization": "Google"}]}
    decision = {"id": "2610.20413", "status": "deferred", "priority": "P1", "reason": "Source unavailable",
        "resolution": "source_exception_archived", "source_exception": {
            "source_url": "https://arxiv.org/html/2610.20413v1", "attempted_at": "2026-10-21T00:00:00Z",
            "error": "HTTP 404", "archive_reason": "No readable primary text; nonblocking exception"}}
    batch = build_batch({"track": "foundation-model", "candidates": [candidate]},
                        {"decisions": [decision]}, batch_name="source-exception")
    assert "full_text_review" not in batch["candidates"][0]
    del decision["source_exception"]["error"]
    with pytest.raises(ValueError, match="source_exception"):
        build_batch({"track": "foundation-model", "candidates": [candidate]},
                    {"decisions": [decision]}, batch_name="fake")


@pytest.mark.parametrize("reverse", [False, True])
def test_generic_known_with_fulltext_locations_still_cannot_hide_acceptance(tmp_path, reverse):
    rows = [{"id": "2610.20413", "status": "deferred", "review_decision": "accepted",
             "implementation_status": "not_implemented"},
            {"id": "2610.20413", "status": "rejected", "resolution": "known",
             "full_text_review": {"scope": "full-text", "source_locations": ["Methods"]}}]
    assert repository_paper_statuses(*paths(tmp_path, rows=rows[::-1] if reverse else rows)) == {
        "2610.20413": "accepted-unimplemented"}


@pytest.mark.parametrize("has_fulltext", [False, True])
def test_nonpriority_source_exception_also_requires_attempt_proof(has_fulltext):
    candidate = {"arxiv_id": "2610.20413", "title": "Method", "repository_status": "new"}
    decision = {"id": "2610.20413", "status": "deferred", "priority": "P2", "reason": "unavailable",
                "resolution": "source_exception_archived"}
    if has_fulltext:
        decision["full_text_review"] = {"scope": "full-text", "source_locations": ["Methods"]}
    with pytest.raises(ValueError, match="source_exception"):
        build_batch({"track": "agent", "candidates": [candidate]}, {"decisions": [decision]}, batch_name="bad")


def test_explicit_followup_cost_decision_is_not_dropped_for_an_accepted_paper():
    candidate = {"arxiv_id": "2610.20413", "title": "Method", "repository_status": "accepted-unimplemented",
                 "implementation_review_required": False}
    decision = {"id": "2610.20413", "status": "deferred", "priority": "P1", "reason": "Beyond resource budget",
                "resolution": "not_reproduced_high_cost"}
    assert len(build_batch({"track": "agent", "candidates": [candidate]},
        {"decisions": [decision]}, batch_name="explicit-followup")["candidates"]) == 1
    assert build_batch({"track": "agent", "candidates": [candidate]},
                       {"decisions": []}, batch_name="not-a-queue")["candidates"] == []


def test_summary_never_calls_catalog_full_implementation():
    paper = Paper("Method", "Algorithm", ["A"], "2026-10-20", "url", "2610.20413")
    candidates = triage_candidates([DiscoveredPaper(paper, ("priority-org-google",))],
                                  {"2610.20413": "accepted-unimplemented"})
    assert candidates[0]["accepted_unimplemented"] is True
    assert candidates[0]["implementation_review_required"] is False
    assert candidates[0]["automatic_implementation_queue"] is False
    payload = build_discovery_payload(track="foundation-model", start_date=dt.date(2026, 10, 20),
        end_date=dt.date(2026, 10, 21), query_names=[], candidates=candidates)
    summary = render_discovery_summary(payload)
    assert "已实现" not in summary
    assert "非自动交付队列" in summary
    assert payload["triage_counts"]["accepted-unimplemented"] == 1
