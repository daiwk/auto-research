"""A new priority source must reopen P2 selection without posing as a revision."""

import json

import pytest

from auto_research import discovery_watermark
from auto_research.discovery import DiscoveredPaper, paper_metadata_sha256, triage_candidates
from auto_research.discovery_review import classify_artifact, unresolved_candidates
from auto_research.models import Paper
from scripts import audit_paper_coverage


def _selection_artifact(priority_signal):
    paper = Paper(
        "An original agent method", "A reproducible agent algorithm.", ["Author"],
        "2026-10-22T00:00:00Z", "https://arxiv.org/abs/2610.30000v1", "2610.30000v1",
    )
    queries = ("priority-org-google",) if priority_signal == "query" else ()
    sources = (
        ({"source_url": "https://ai.meta.com/research/publications/new/"},)
        if priority_signal == "source" else ()
    )
    rows = triage_candidates(
        [DiscoveredPaper(paper, queries, sources)],
        {"2610.30000": "selection-reviewed"},
        repository_versions={"2610.30000": {
            "revision": 1, "metadata_sha256": paper_metadata_sha256(paper), "selection_only": True,
        }},
    )
    return classify_artifact({"track": "agent", "candidates": rows})


def _audit_artifact(tmp_path, monkeypatch, artifact, *, historical_identity=False, strict=True):
    docs = tmp_path / "docs"
    docs.mkdir()
    ledger_path = docs / "paper-discovery-ledger.json"
    batches = []
    if historical_identity:
        batches.append({"batch": "old-date-triage", "candidates": [{
            "id": "2610.30000", "priority": "P2", "status": "deferred",
            "reason": "Only the historical identity and publication date were checked.",
            "review_scope": "historical_metadata_identity_date_scope_only",
            "resolution": "historical_first_publication",
        }]})
    ledger_path.write_text(json.dumps({"batches": batches}))
    artifact_path = docs / "pending.json"
    artifact_path.write_text(json.dumps(artifact))
    monkeypatch.setattr(audit_paper_coverage, "ROOT", tmp_path)
    monkeypatch.setattr(audit_paper_coverage, "LEDGER", ledger_path)
    # Exercise the pending-artifact gate, independently of the watermark gate.
    monkeypatch.setattr(discovery_watermark, "audit_review_watermark", lambda _root: [])
    return audit_paper_coverage.audit(strict=strict, pending_artifacts=(artifact_path,))


@pytest.mark.parametrize("priority_signal", ["query", "source"])
@pytest.mark.parametrize("historical_identity", [False, True])
def test_strict_audit_blocks_priority_reopening_even_with_old_metadata_identity(
    tmp_path, monkeypatch, priority_signal, historical_identity,
):
    artifact = _selection_artifact(priority_signal)
    row = artifact["candidates"][0]
    assert row["repository_status"] == "selection-reviewed"
    assert row["selection_reopened"] is row["priority_review_required"] is True
    assert row["revision_review_required"] is False
    assert row["revision_review_reason"] is None
    assert row["selection_reopen_reason"] == "new-priority-evidence-after-selection"
    assert row["review_bucket"] == "priority-fulltext-review"
    assert unresolved_candidates([artifact]) == [row]

    errors = _audit_artifact(
        tmp_path, monkeypatch, artifact, historical_identity=historical_identity,
    )
    assert len(errors) == 1
    assert "unreviewed P0/P1 candidates" in errors[0]
    assert "2610.30000" in errors[0]


def test_unchanged_selection_is_not_a_strict_pending_method_review(tmp_path, monkeypatch):
    artifact = _selection_artifact(None)
    row = artifact["candidates"][0]
    assert row["selection_reopened"] is row["review_required"] is False
    assert row["method_verified"] is False
    assert row["review_bucket"] == "selection-reviewed-method-unverified"
    assert unresolved_candidates([artifact]) == []
    assert _audit_artifact(tmp_path, monkeypatch, artifact) == []


def test_priority_reopening_only_blocks_the_strict_gate(tmp_path, monkeypatch):
    assert _audit_artifact(tmp_path, monkeypatch, _selection_artifact("query"), strict=False) == []


@pytest.mark.parametrize("historical_identity", [False, True])
def test_existing_non_selection_id_deduplication_is_unchanged(
    tmp_path, monkeypatch, historical_identity,
):
    artifact = {"candidates": [{"arxiv_id": "2610.30000", "repository_status": "new"}]}
    errors = _audit_artifact(
        tmp_path, monkeypatch, artifact, historical_identity=historical_identity,
    )
    assert len(errors) == (0 if historical_identity else 1)
