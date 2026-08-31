import json
import subprocess
import sys
from pathlib import Path


def test_latest_p0_p1_discovery_batch_is_closed():
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, str(root / "scripts/audit_paper_coverage.py"), "--strict"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert "closed" in completed.stdout


def test_weekend_empty_batch_is_explicitly_verified():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "docs/paper-discovery-ledger.json").read_text(encoding="utf-8"))
    weekend = next(
        batch for batch in data["batches"]
        if batch.get("scope_kind") == "incremental-weekend-review"
    )
    assert set(weekend["empty_tracks_verified"]) == set(weekend["required_tracks"])
    assert weekend["candidates"] == []
    assert weekend["empty_review"]["source_artifact"]


def test_global_discovery_batch_covers_declared_subtopics():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "docs/paper-discovery-ledger.json").read_text(encoding="utf-8"))
    global_batches = [batch for batch in data["batches"] if batch.get("scope_kind") == "global"]
    assert global_batches, "the ledger must contain a cross-domain global audit"
    latest = global_batches[-1]
    required = {(item["track"], item["subtopic"]) for item in latest["required_subtopics"]}
    covered = {(item["track"], item["subtopic"]) for item in latest["candidates"]}
    assert required <= covered


def test_google_and_meta_eligible_papers_are_audited_as_p0():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "docs/paper-discovery-ledger.json").read_text(encoding="utf-8"))
    batches = [
        batch for batch in data["batches"]
        if batch.get("scope_kind") == "institution-priority"
    ]
    assert batches
    latest = batches[-1]
    assert set(latest["priority_institutions"]) == {"Google", "Meta"}
    assert {entry["organization"] for entry in latest["institution_sweeps"]} == {
        "Google", "Meta"
    }
    candidates = {entry["id"]: entry for entry in latest["candidates"]}
    assert {"2606.25147", "2607.12281"} <= candidates.keys()
    for sweep in latest["institution_sweeps"]:
        assert sweep["candidate_discovery_gate"] == "affiliation-and-topic"
        assert sweep["abstract_online_evidence_required"] is False
        assert sweep["full_text_review_required"] is True
    for paper_id in ("2606.25147", "2607.12281"):
        review = candidates[paper_id]["evidence_review"]
        assert review["scope"] == "full-text"
        assert review["abstract_used_as_gate"] is False
        assert review["locations"]
        assert review["matched_terms"]
    for entry in candidates.values():
        assert entry["priority"] == "P0"
        assert entry["status"] == "implemented"
        assert entry["priority_reason"]
        assert entry["evidence_gate"]


def test_latest_recommendation_scan_is_high_recall_and_catches_genrec():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "docs/paper-discovery-ledger.json").read_text(encoding="utf-8"))
    batches = [
        batch for batch in data["batches"]
        if batch.get("scope_kind") == "high-recall-correction"
    ]
    assert batches
    latest = batches[-1]
    assert latest["pagination"]["page_size"] >= 25
    assert latest["pagination"]["maximum_results_per_query"] >= 100
    assert {"Google", "Meta", "Netflix"} <= set(latest["priority_organization_terms"])
    assert {
        "priority-org-google", "priority-org-meta", "priority-org-netflix"
    } <= set(latest["organization_query_matrix"])
    genrec = next(entry for entry in latest["candidates"] if entry["id"] == "2608.10257")
    assert {"llm-recommendation", "production-evidence"} <= set(genrec["matched_queries"])
    assert genrec["status"] == "implemented"
    assert genrec["evidence_review"]["scope"] == "full-text"
