"""The Nov15 watermark closes selection, not unread methods or implementations."""
from hashlib import sha256
import json
from pathlib import Path

from auto_research.discovery_watermark import audit_review_watermark
from scripts.prepare_nov15_review_closure import metadata_digest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov15-review-closure"


def read(path):
    return json.loads(path.read_bytes())


def test_current_watermark_and_historical_predecessor_are_distinct():
    state = read(ROOT / "docs/paper-discovery-watermark.json")
    assert state["window"] == {"start": "2026-11-10", "end": "2026-11-15"}
    assert state["review_watermark"] == "2026-11-15"
    assert state["selection_review_complete"] and not state["method_review_complete"]
    assert not state["all_sources_exhaustive"] and not state["implementation_complete"]
    previous = ROOT / "docs" / state["previous_review_state"]
    assert sha256(previous.read_bytes()).hexdigest() == state["previous_review_state_sha256"]
    assert read(previous)["review_watermark"] == "2026-11-09"
    assert state["next_scan_start_with_overlap"] == "2026-11-14"
    assert audit_review_watermark(ROOT) == []


def test_actual_cap_and_actual_split_replacements_are_preserved():
    receipt = read(AUDIT / "foundation-model-late-index-retrieval.json")
    original = receipt["original_capped_queries_preserved"]
    assert len(original) == 1 and original[0]["query"] == "LLM"
    assert original[0]["state"] == "capped" and original[0]["next_offset"] == 2000
    repaired = [q for q in receipt["arxiv_transport"]["queries"] if q["query"] == "LLM"]
    assert {tuple(q["identifier_months"]) for q in repaired} == {("2610",), ("2611",)}
    assert all(q["state"] == "exhausted" and q["coverage_complete"] and q["transport_complete"]
               and q["cache_fallback_pages"] == 0 for q in repaired)
    assert [q["next_offset"] for q in repaired] == [2100, 886]
    assert receipt["containing_capture"]["original_window"] != receipt["requested_window"]


def test_register_partition_is_selection_not_method_or_delivery():
    register = read(AUDIT / "paper-register.json")
    report = read(AUDIT / "review-inventory.json")
    screen = read(AUDIT / "p2-selection-screen.json")
    papers = {r["id"]: r for r in register["papers"]}
    assert len(papers) == len(register["papers"]) == report["counts"]["registered_unique_identities"]
    assert register["candidate_review_complete"] and register["selection_review_complete"]
    assert not screen["protected_records"] and not screen["protected_ids"]
    selected = {r["id"]: r for r in screen["records"]}
    assert set(selected) == {i for i, p in papers.items() if p["status"] == "not_selected_p2"}
    assert all(r["selection_review_done"] and r["originality_not_rejected"]
               and not r["method_review_completed"] and not r["fulltext_review_completed"]
               and not r["high_cost"] and not r["implementation"] for r in selected.values())
    assert all(not p["automatic_implementation_queue"] for p in papers.values())
    assert not any(p["implementation_status"] in {"implemented", "component_only"} for p in papers.values())
    for paper in papers.values():
        for review in paper.get("reviews", []):
            assert review["review_done"] and review["fulltext_review_completed"]
            assert review["metadata_sha256"] == paper["metadata_sha256"]
            assert len(review["source_sha256"]) == 64 and review["locations"]
            if review["resolution"] == "not_reproduced_high_cost":
                assert review["status"] == "deferred" and review["cost_assessment"]["scale"]
                assert review["automatic_retry"] is False


def test_protected_revisions_and_industrial_evidence_have_real_decisions():
    papers = {p["id"]: p for p in read(AUDIT / "paper-register.json")["papers"]}
    for identity in ("2610.00890", "2610.03713", "2610.13672", "2610.15020", "2610.19095", "2610.20579"):
        assert papers[identity]["reviews"][0]["fulltext_review_completed"]
        assert papers[identity]["revision"] > 1
    fore = papers["2611.13442"]["reviews"][0]
    assert "Meta" in fore["verified_priority_organizations"]
    assert fore["resolution"] == "not_reproduced_high_cost"
    amd = papers["2611.17501"]["reviews"][0]
    assert "Meta" in amd["verified_priority_organizations"] and amd["decision"] == "rejected"
    for identity in ("2611.12727", "2611.14938"):
        review = papers[identity]["reviews"][0]
        assert review["production_gate_passed"] and review["resolution"] == "not_reproduced_private_data"
    for identity in ("2611.16139", "2611.17921"):
        assert papers[identity]["reviews"][0]["resolution"] == "industrial_online_gate_not_met"


def test_fingerprints_do_not_accept_changes_in_meaning():
    row = {"title": "A paper", "abstract": "Some finding", "authors": ["A Author"]}
    assert metadata_digest(row) == metadata_digest(row | {"title": "A  paper"})
    assert metadata_digest(row) != metadata_digest(row | {"abstract": "Different finding"})
