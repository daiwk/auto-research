"""Closed selection, original evidence, and implementation remain independent."""
from hashlib import sha256
import json
from pathlib import Path

from auto_research.discovery_watermark import audit_review_watermark


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov09-review-closure"


def read(name):
    return json.loads((AUDIT / name).read_bytes())


def test_closed_selection_has_exact_partition_and_no_method_or_gpu_promotion():
    screen = read("p2-selection-screen.json")
    frozen = read("p2-selection-input.json")
    assert sha256((AUDIT / "p2-selection-input.json").read_bytes()).hexdigest() == screen["frozen_input_sha256"]
    initial = {row[0] for row in frozen["records"]}
    selected = {row["id"] for row in screen["records"]}
    primary = set(screen["excluded_primary_ids"])
    assert len(initial) == 4359 and not screen["protected_records"]
    assert not selected & primary and initial == selected | primary
    register = read("paper-register.json")
    assert register["candidate_review_complete"] and register["selection_review_complete"]
    assert not register["method_review_complete"] and not register["implementation_complete"]
    registered = {row["id"]: row for row in register["papers"]}
    assert len(registered) == register["unique_papers"] == len(register["papers"])
    assert {row["id"] for row in register["papers"] if row["status"] == "not_selected_p2"} == selected
    for identity in selected:
        row = registered[identity]
        assert row["method_review_completed"] is row["fulltext_review_completed"] is False
        assert row["originality_not_rejected"] and not row["automatic_implementation_queue"]
    for identity in primary:
        assert registered[identity]["status"] != "not_selected_p2"
        assert registered[identity]["reviews"]
    assert audit_review_watermark(ROOT) == []


def test_priority_discoveries_and_online_evidence_do_not_become_p2_or_implementation():
    register = {row["id"]: row for row in read("paper-register.json")["papers"]}
    for identity in ("2610.40578", "2611.09291", "2611.01647", "2611.01695", "2611.06123"):
        row = register[identity]
        assert row["status"] != "not_selected_p2" and row["reviews"]
        assert row["method_review_completed"] and not row["automatic_implementation_queue"]
        assert row["implementation_status"] == "not_changed_by_review"


def test_source_dispositions_do_not_promote_withdrawal_or_abstract_scope_to_method_review():
    register = {row["id"]: row for row in read("paper-register.json")["papers"]}
    for identity in ("2610.33258", "2611.08494"):
        row = register[identity]
        assert row["review_scope"] == "bounded-source-check"
        assert row["method_review_completed"] is False
        assert not any(review.get("fulltext_review_completed") for review in row["reviews"])


def test_containing_queries_keep_raw_caps_and_real_monthly_replacements():
    register_ids = {row["id"] for row in read("paper-register.json")["papers"]}
    repairs = []
    for track in ("recommendation", "foundation-model", "post-training", "agent"):
        for mode in ("submission-window", "late-index"):
            value = read(f"{track}-{mode}-retrieval.json")
            assert value["requested_window"] == {"start": "2026-10-16", "end": "2026-11-09"}
            transport = value["arxiv_transport"]
            assert transport["coverage_complete"] and transport["transport_complete"]
            assert transport["capped_queries"] == transport["failed_queries"] == 0
            assert all(q["state"] == "exhausted" and not q["cache_fallback_pages"] for q in transport["queries"])
            assert {c["arxiv_id"] for c in value["candidates"]} <= register_ids
            source_keys = {f"{r['run_id']}/{r['artifact_name']}/{r['file']}"
                           for r in value["derived_from"]["source_receipts"]}
            source_keys |= {"llm-2610-replacement.json", "llm-2611-replacement.json", "nov09-tail-all-categories.atom"}
            assert all(c["source_capture"] in source_keys for c in value["candidates"])
            assert value["derived_from"]["actual_query_bounds_preserved"]
            repairs.extend(value["derived_from"]["query_replacements"])
    assert len(repairs) == 1
    assert repairs[0]["original_query_report"]["state"] == "capped"
    replacements = repairs[0]["actual_replacement_receipts"]
    assert [(r["month"], r["query"]["next_offset"]) for r in replacements] == [("2610", 2098), ("2611", 368)]


def test_replacement_only_versions_point_to_the_real_replacement_capture():
    papers = {row["id"]: row for row in read("paper-register.json")["papers"]}
    for identity, revision in (("2610.06729", 3), ("2610.06116", 2), ("2610.18877", 2),
                               ("2610.00685", 2), ("2611.00009", 1), ("2611.03656", 1)):
        assert papers[identity]["revision"] == revision
        assert papers[identity]["capture"] == f"llm-{identity[:4]}-replacement.json"
