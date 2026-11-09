"""The bounded November review must not certify its unread candidate pool."""
from datetime import date
from hashlib import sha256

import pytest

from scripts.build_nov09_review_inventory import (
    AUDIT, BATCH, END, HIGH_COST, MODES, ROOT, RUNS, TRACKS, closed_query, ledger_row, local_day, read,
)


def test_coverage_replaces_cap_but_does_not_imply_review():
    value = read(AUDIT / "review-inventory.json")
    assert value["requested_window"] == {"start": "2026-10-16", "end": END.isoformat()}
    assert local_day("2026-10-15T16:01:38Z") == date(2026, 10, 16)
    assert value["arxiv_recall_matrix_covered"]
    assert not value["all_sources_exhaustive"] and not value["review_watermark_advanced"]
    assert not value["candidate_review_complete"]
    receipts = value["capture_receipts"]
    assert {(r["run_id"], r["track"], r["mode"]) for r in receipts} == {
        (run, track, mode) for run in RUNS for track in TRACKS for mode in MODES
    }
    assert len(receipts) == 24
    failures = [q for r in receipts for q in r["queries"] if not closed_query(q)]
    assert len(failures) == 1 and failures[0]["state"] == "capped"
    assert failures[0]["query"] == "LLM" and failures[0]["next_offset"] == 2000
    replacements = value["query_replacements"]
    assert [(r["month"], r["query"]["next_offset"]) for r in replacements] == [
        ("2610", 2098), ("2611", 368),
    ]
    assert all(closed_query(r["query"]) for r in replacements)


def test_pending_pool_remains_deduplicated_and_is_not_written_as_terminal():
    value = read(AUDIT / "review-inventory.json")
    rows = [row for group in value["pending_identities_by_local_first_publication"].values() for row in group]
    ids = {row[0] for row in rows}
    assert len(ids) == len(rows) == value["counts"]["pending_identity_review"]
    assert len(rows) == sum(value["pending_bucket_counts"].values())
    ledger = read(ROOT / "docs/paper-discovery-ledger.json")
    batch = next(b for b in ledger["batches"] if b["batch"] == BATCH)
    assert batch["delivery_status"] == "partial_review_pending" and not batch["selected_scope_complete"]
    assert batch["review_watermark"]["before"] == batch["review_watermark"]["after"]
    assert batch["counts"]["implementations"] == batch["counts"]["gpu_runs"] == 0
    terminal = {row["id"]: row for row in batch["candidates"]}
    assert sorted(terminal) == value["primary_reviewed_ids"]
    assert not ids.intersection(terminal)
    assert not ids.intersection(value["pending_late_index_scope_triage"])
    for row in terminal.values():
        assert row["review_done"] and not row["automatic_retry"] and not row["automatic_implementation_queue"]
        assert row["implementation_status"] == "not_implemented_by_review"
        if row["resolution"] == HIGH_COST:
            assert row["status"] == "deferred" and row["full_experiment_review_done"]
            assert row["fulltext_review_completed"] and row["cost_assessment"]["basis"]


def test_high_cost_decision_must_have_original_evidence_and_cannot_accept():
    review = read(AUDIT / "additional-primary-reviews.json")["reviews"]
    paper = next(row for row in review if row["resolution"] == HIGH_COST)
    with pytest.raises(ValueError, match="original evidence"):
        ledger_row(paper | {"fulltext_review_completed": False}, "review.json")
    with pytest.raises(ValueError, match="original evidence"):
        ledger_row(paper | {"decision": "accepted"}, "review.json")
    with pytest.raises(ValueError, match="nonterminal"):
        ledger_row(paper | {"review_done": False}, "review.json")


def test_bilingual_review_preserves_coverage_boundary():
    zh = (AUDIT / "README.md").read_bytes()
    en = (ROOT / "docs/en/research-audits/nov09-review-closure/README.md").read_text(encoding="utf-8")
    assert f"<!-- source-sha256: {sha256(zh).hexdigest()} -->" in en
    assert "not a completed watermark" in en and "未推进水位" in (
        ROOT / "docs/paper-discovery-audit.md"
    ).read_text(encoding="utf-8")
