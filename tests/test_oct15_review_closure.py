"""Frozen October 15 evidence cannot turn transport or review into capability."""
import json
from dataclasses import replace
from pathlib import Path

import pytest

from auto_research.discovery import DiscoveredPaper, paper_metadata_sha256, triage_candidates
from auto_research.models import Paper


ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs/research-audits/oct15-review-closure"
TRACKS = ("recommendation", "foundation-model", "post-training", "agent")


def _read(name):
    return json.loads((DIRECTORY / name).read_text())


def test_containing_retrieval_preserves_real_bounds_and_replaces_the_capped_query():
    replacements = []
    for track in TRACKS:
        for mode in ("submission-window", "late-index"):
            receipt = _read(f"{track}-{mode}-retrieval.json")
            assert receipt["requested_window"] == {"start": "2026-10-13", "end": "2026-10-15"}
            derived = receipt["derived_from"]
            assert derived["actual_query_bounds_preserved"] is True
            assert len(derived["source_sha256"]) == 64
            assert derived["source_requested_window"]["start"] < receipt["requested_window"]["start"]
            transport = receipt["arxiv_transport"]
            assert transport["coverage_complete"] and transport["transport_complete"]
            assert transport["capped_queries"] == transport["failed_queries"] == 0
            for query in transport["queries"]:
                assert query["state"] == "exhausted" and query["transport_complete"]
                assert not query["cache_fallback_pages"]
                if mode == "submission-window":
                    assert query["date_from"] <= "2026-10-12" <= "2026-10-15" <= query["date_to"]
                else:
                    assert "2610" in query["identifier_months"]
            replacements.extend(derived["query_replacements"])
    assert len(replacements) == 1
    replacement = replacements[0]
    assert replacement["original_query_report"]["state"] == "capped"
    exact_october = replacement["replacement_query_report"]
    assert exact_october["identifier_months"] == ["2610"]
    assert exact_october["state"] == "exhausted"
    assert exact_october["next_offset"] == 1088
    assert len(replacement["replacement_sha256"]) == 64


def test_new_publication_history_and_revisions_are_not_mixed():
    register = _read("paper-register.json")
    decisions = [row for track in TRACKS for row in _read(f"{track}-reviews.json")["reviews"]]
    by_id = {row["id"]: row for row in decisions}
    assert len(decisions) == len(by_id) == 2114
    fresh = [row for row in register["papers"] if row["review_origin"] == "new_identity_review"]
    assert {row["id"] for row in fresh} == set(by_id)
    current = [row for row in fresh if "2026-10-13" <= row["published"][:10] <= "2026-10-15"]
    assert len(current) == register["coverage_counts"]["fresh_first_publication_in_window"] == 794
    assert len(fresh) - len(current) == register["coverage_counts"]["fresh_historical_or_overlap"] == 1320
    assert register["coverage_counts"]["queried_unique"] == 3742
    revisions = _read("revision-reviews.json")["reviews"]
    assert len(revisions) == 11
    assert not set(by_id).intersection(row["id"] for row in revisions)
    assert all(row["new_paper"] is False and row["semantic_diff_claimed"] is False for row in revisions)
    # An October identifier/bulletin is not proof of October 13 first publication.
    assert by_id["2610.18883"]["published"].startswith("2026-10-01")


def test_cost_closure_and_source_exceptions_never_become_implementations():
    for name in [*(f"{track}-reviews.json" for track in TRACKS),
                 "revision-reviews.json", "root-priority-reviews.json"]:
        for row in _read(name)["reviews"]:
            assert row["review_done"] is True and row["automatic_retry"] is False
            assert row["full_article_read"] is False
            assert row.get("implementation_status") != "implemented"
            if row["resolution"] == "not_reproduced_high_cost":
                assert row["decision"] != "accepted"
                cost = row["cost_assessment"]
                assert all(cost.get(key) for key in
                           ("source_url", "basis", "scale", "available_resource", "cost_type"))
                assert not {"gpu_validation_artifact", "metrics", "checkpoint"}.intersection(row)
            if row["decision"] == "accepted":
                assert row["fulltext_review_completed"] is True
    register = _read("paper-register.json")
    assert register["candidate_review_complete"] is True
    assert register["implementation_complete"] is register["all_sources_exhaustive"] is False
    assert all(row["status"] != "pending" and row["automatic_implementation_queue"] is False
               for row in register["papers"])
    archive = _read("exception-archive.json")
    assert archive["blocking"] is False and archive["retry_policy"] == "on-new-evidence-only"
    for exception in register["source_exceptions"]:
        assert exception["counts_as_accepted"] is False
        assert exception["scope_triage_completed"] is True
        assert exception["attempts"] and all(item["error"] for item in exception["attempts"])


def test_material_revision_corrections_are_explicit_not_silent_promotions():
    revisions = {row["id"]: row for row in _read("revision-reviews.json")["reviews"]}
    assert revisions["2609.04047"]["resolution"] == "correction_reviewed_fixed_tiers_withdrawn"
    spark = revisions["2608.04962"]
    assert spark["revision"] == 2 and spark["implementation_status"] == "existing_evidence_not_upgraded_by_review"
    text = (ROOT / "docs/post-training/2608.04962-specroll/README.md").read_text()
    assert "v2 SPARK" in text and "不代表已经实现" in text


@pytest.mark.parametrize("scope", [
    "bounded_cost_gate_not_algorithm_acceptance",
    "historical_metadata_identity_date_scope_only",
    "source_exception_archived_identity_only",
])
def test_observed_terminal_version_avoids_identical_requeue_without_hiding_new_evidence(scope):
    paper = Paper(
        title="Reviewed disposition", abstract="Observed metadata, not algorithm acceptance.",
        authors=["Researcher"], published="2026-10-01T00:00:00Z",
        updated="2026-10-14T00:00:00Z", arxiv_id="2610.00001v2",
        url="https://arxiv.org/abs/2610.00001v2",
    )
    baseline = {"2610.00001": {
        "revision": 2, "metadata_sha256": paper_metadata_sha256(paper),
        "review_scope": scope, "algorithm_acceptance_inferred": False,
    }}

    def triage(value):
        return triage_candidates(
            [DiscoveredPaper(value, (), ({"entry_kind": "replacement"},))],
            {"2610.00001": "reviewed"}, repository_versions=baseline,
        )[0]

    unchanged = triage(paper)
    assert unchanged["review_required"] is unchanged["revision_review_required"] is False
    assert unchanged["repository_status"] == "reviewed"  # Never promoted to implemented.
    assert triage(replace(paper, abstract="New material evidence"))["review_required"] is True
    newer = triage(replace(paper, arxiv_id="2610.00001v3"))
    assert newer["review_required"] is True and newer["revision_review_reason"] == "newer-version"
