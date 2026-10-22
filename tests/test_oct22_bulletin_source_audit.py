from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("oct22_bulletin_audit", ROOT/"scripts/build_oct22_bulletin_source_audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def inputs():
    receipts, catalog = [], {}
    for source, (key, (domain, paper_id)) in zip(sorted(audit.CATEGORIES), audit.SELECTED.items()):
        row = {"id": paper_id+"v1", "title": key, "abstract": "not exported", "entry_kind": "new"}
        receipts.append({"kind": "arxiv", "source": source, "page": 1, "url": "https://arxiv.org/list/"+source+"/new",
            "checked_at": "2026-10-22T02:39:00+00:00", "status": "retrieved", "sha256": "a"*64,
            "announced_on": "2026-10-22", "expected_entries": 1, "parsed_entries": 1,
            "sections": [{"kind": k, "shown": int(k == "new"), "expected": int(k == "new")}
                         for k in ("new", "cross-list", "replacement")],
            "parse_complete": True, "records": [row]})
        catalog[key] = {"key": key, "domain": domain, "title": key, "paper_url": f"https://arxiv.org/abs/{paper_id}v1",
                        "detail_path": f"{domain}/{paper_id}-{key}/README.md", "first_author": "Author",
                        "first_author_affiliation": "University", "priority": "P1", "summary": "paper cost basis",
                        "published_at": "2026-10-21T17:59:56Z", "evaluation_tier": "l1_mechanism",
                        "requires_gpu_validation": key in audit.COMPONENT_KEYS}
    p = receipts[0]
    p["records"].append({"id": "2610.22671v2", "title": "MemoProAgent: Toward Memory-Driven Proactive Assistance", "entry_kind": "replacement"})
    p["expected_entries"] = p["parsed_entries"] = 2
    p["sections"][-1]["shown"] = p["sections"][-1]["expected"] = 1
    baseline = {"raw_capture_sha256": "b"*64, "bulletin_ids_by_category": {"cs.AI": ["2610.22671v1", "2501.00001v1"]},
                "retrieval_receipts": [{"checked_at": "2026-10-21T17:53:03+00:00"}]}
    deltas = []
    for org, ok in (("Google", False), ("Meta", False), ("Google DeepMind", True)):
        receipts.append({"kind": "official", "source": org, "page": 1,
                         "checked_at": "2026-10-22T02:39:00+00:00", "status": "retrieved" if ok else "unavailable"})
        deltas.append({"organization": org, "attempted_pages": 1, "retrieved_pages": int(ok),
                       "new_directory_urls": [], "changed_records": [], "all_sources_exhaustive": False})
    return receipts, baseline, deltas, catalog


def report(values=None):
    return audit.build_reports(*(values or inputs()), "d"*64)


def test_failed_directory_delta_is_unknown_null_not_zero():
    coverage, _, _ = report()
    for row in coverage["official_directory_deltas"]:
        if row["organization"] in {"Google", "Meta"}:
            assert row["new_directory_urls"] is None and row["changed_records"] is None
            assert not row["delta_known"] and row["status"] == "source_unavailable_not_zero_delta"
        else:
            assert row["delta_known"] and row["new_directory_urls"] == []
        assert not row["all_sources_exhaustive"]


def test_snapshot_differences_are_not_first_publication_counts():
    coverage, scope, _ = report()
    c = coverage["counts"]
    assert c["unique_bulletin_identities"] == 9
    assert c["snapshot_added_base_identities_not_new_paper_count"] == 8
    assert c["snapshot_retained_base_identities"] == 1
    assert c["snapshot_added_version_strings_not_revision_count"] == 9
    assert "fresh_since_last_scan" not in c
    assert scope["metadata_updates"][0]["key"] == "proper-agent"
    assert scope["metadata_updates"][0]["observed_versions"] == ["2610.22671v2"]
    assert not scope["metadata_updates"][0]["new_paper"]
    assert c["selected_papers"] == 8 and c["metadata_updates"] == 1


def test_components_remain_pending_and_references_terminal_done():
    _, scope, ledger = report()
    assert not scope["selected_scope_complete"]
    for row in ledger["candidates"]:
        if row["key"] in audit.COMPONENT_KEYS:
            assert row["status"] == "accepted-unimplemented" and not row["review_done"]
            assert not row["component_accepted"] and not row["component_implemented"]
            assert row["delivery_status"] == "pending_gpu_and_integration"
        else:
            assert row["status"] == "deferred" and row["review_done"]
            assert row["implementation_status"] == "deferred_high_cost"
        assert row["full_experiment_review_done"]
        assert row["full_experiment_status"] == "not_reproduced_high_cost"
        assert not row["automatic_retry"] and not row["promotion_eligible"]


def test_unchanged_watermark_no_exhaustion_and_no_abstract_export():
    coverage, _, _ = report()
    assert not coverage["all_sources_exhaustive"] and not coverage["review_watermark_advanced"]
    assert coverage["review_watermark"] == {"before": "2026-10-15", "after": "2026-10-15"}
    assert not coverage["full_bulletin_full_text_review_complete"]
    assert "records" not in coverage["retrieval_receipts"][0]
    assert "not exported" not in json.dumps(coverage)


@pytest.mark.parametrize("field,value", [("announced_on", "2026-10-21"), ("parse_complete", False),
                                         ("parsed_entries", 99), ("status", "unavailable")])
def test_incomplete_or_wrong_bulletin_fail_closed(field, value):
    values = inputs()
    values[0][0][field] = value
    with pytest.raises(ValueError):
        report(values)


def test_duplicate_category_rejected_even_with_eight_receipts():
    values = inputs()
    values[0][1]["source"] = values[0][0]["source"]
    with pytest.raises(ValueError, match="eight distinct"):
        report(values)


def test_section_count_mismatch_rejected():
    values = inputs()
    values[0][0]["sections"][0]["shown"] = 0
    with pytest.raises(ValueError, match="section counts"):
        report(values)


def test_selected_id_must_be_in_actual_new_section():
    values = inputs()
    values[0][0]["records"][0]["id"] = "2610.00001v1"
    with pytest.raises(ValueError, match="absent"):
        report(values)


def test_append_preserves_old_scope_and_refuses_overwriting_acceptance():
    before = {"schema_version": 1, "batches": [{"batch": "old", "candidates": [{"id": "2510.00001", "status": "implemented"}]}]}
    original = deepcopy(before)
    _, _, batch = report()
    result = audit.append_batch(before, batch)
    assert before == original and result["batches"][:-1] == original["batches"]
    with pytest.raises(ValueError, match="already exists"):
        audit.append_batch(result, batch)


def test_committed_capture_counts_statuses_and_exact_dates():
    path = ROOT/audit.AUDIT_REL/"source-coverage.json"
    if not path.exists():
        pytest.skip("capture materialization has not run")
    coverage = json.loads(path.read_text())
    c = coverage["counts"]
    assert c["unique_bulletin_identities"] == 964
    assert c["category_entries_including_crosslists_and_replacements"] == 1378
    assert c["snapshot_added_base_identities_not_new_paper_count"] == 934
    assert c["snapshot_retained_base_identities"] == 30
    assert c["new_section_unique_identities_not_exact_first_publication_count"] == 520
    assert c["section_entry_counts"] == {"new": 520, "cross-list": 343, "replacement": 515}
    assert c["selected_first_publication_after_baseline_capture"] == 2
    assert len(coverage["bulletin_ids_by_category"]) == 8
    for row in coverage["retrieval_receipts"]:
        if row["kind"] == "arxiv":
            assert row["announced_on"] == "2026-10-22" and row["parse_complete"]
    scope = json.loads((path.parent/"task-scope.json").read_text())
    selected = {p["key"]: p for p in scope["papers"]}
    assert set(selected) == set(audit.SELECTED)
    assert selected["alps"]["original_published_at"] == "2026-10-21T17:57:11Z"
    assert selected["aw0"]["original_published_at"] == "2026-10-21T17:59:56Z"
    assert {p["key"] for p in selected.values() if p["full_experiment_review_done"]} == set(audit.SELECTED)
