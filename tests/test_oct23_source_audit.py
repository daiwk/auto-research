from collections import Counter
from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("oct23_audit", ROOT/"scripts/build_oct23_source_audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def inputs():
    receipts, catalog = [], {}
    for category in sorted(audit.CATEGORIES):
        receipts.append({"kind": "arxiv", "source": category, "page": 1,
                         "url": f"https://arxiv.org/list/{category}/new?show=2000",
                         "status": "retrieved", "checked_at": "2026-10-23T09:24:00+00:00",
                         "announced_on": "2026-10-23", "parse_complete": True,
                         "sha256": "a"*64, "records": []})
    for index, (key, (domain, paper_id)) in enumerate(audit.SELECTED.items()):
        historical = key == "gemma-priority-protocol"
        if not historical:
            receipts[index % 8]["records"].append({"id": paper_id+"v1", "title": key,
                "entry_kind": "cross-list" if key in {"openattention", "moezip", "aopd"} else "new"})
        catalog[key] = {"key": key, "domain": domain, "title": key,
            "paper_url": f"https://arxiv.org/abs/{paper_id}v1", "detail_path": f"{domain}/{paper_id}-{key}/README.md",
            "first_author": "Author", "first_author_affiliation": "Google" if historical else "University",
            "priority": "P0" if historical else "P1", "published_at": "2026-09-25T02:43:40Z" if historical else "2026-10-22T07:19:49Z",
            "summary": "source-scale basis", "evaluation_tier": "l1_mechanism",
            "full_experiment_status": "not_run_scope_limited_protocol" if historical else "not_reproduced_high_cost",
            "requires_gpu_validation": key not in {"gemma-priority-protocol", "rkl-policy-distillation"}}
    for page in receipts:
        counts = Counter(row["entry_kind"] for row in page["records"])
        page["expected_entries"] = page["parsed_entries"] = len(page["records"])
        page["sections"] = [{"kind": kind, "shown": counts[kind], "expected": counts[kind]}
                            for kind in ("new", "cross-list", "replacement")]
    baseline = {"raw_capture_sha256": "b"*64,
                "bulletin_ids_by_category": {"cs.AI": ["2610.30206v1", "2501.00001v1"]},
                "retrieval_receipts": [{"checked_at": "2026-10-22T02:39:40+00:00"}]}
    deltas = []
    for organization in ("Google", "Meta", "Google DeepMind"):
        receipts.append({"kind": "official", "source": organization, "page": 1, "status": "retrieved",
                         "checked_at": "2026-10-23T09:24:00+00:00"})
        urls = [{"title": slug, "url": f"https://research.google/pubs/{slug}/", "directory_date": None}
                for slug in audit.GOOGLE_DECISIONS] if organization == "Google" else []
        deltas.append({"organization": organization, "attempted_pages": 1, "retrieved_pages": 1,
                       "new_directory_urls": urls, "changed_records": []})
    return receipts, baseline, deltas, catalog


def reports(values=None):
    return audit.build_reports(*(values or inputs()), "d"*64)


def test_separate_snapshot_first_publication_historical_and_crosslist_counts():
    coverage, scope, _ = reports()
    assert coverage["counts"]["selected_papers"] == 9
    assert coverage["counts"]["components_pending_verification"] == 8
    assert coverage["counts"]["reference_only_review_done"] == 1
    assert coverage["counts"]["unique_bulletin_identities"] == 8
    assert coverage["counts"]["snapshot_added_base_identities_not_new_paper_count"] == 7
    assert coverage["counts"]["snapshot_retained_base_identities"] == 1
    assert coverage["counts"]["selected_first_publication_after_baseline_capture"] == 8
    gemma = next(row for row in scope["papers"] if row["key"] == "gemma-priority-protocol")
    assert gemma["intake_class"] == "historical-backfill"
    assert gemma["observed_versions"] == []
    assert not gemma["first_publication_after_baseline_capture"]
    assert gemma["full_experiment_status"] == "not_run_scope_limited_protocol"
    assert all(not row["component_accepted"] and not row["component_implemented"] for row in scope["papers"])
    assert not scope["selected_scope_complete"]
    for row in scope["papers"]:
        assert row["review_done"] is (row["key"] == "onelatent")
    assert not coverage["full_bulletin_full_text_review_complete"]
    assert coverage["review_watermark"] == {"before": "2026-10-15", "after": "2026-10-15"}


def test_five_google_directory_urls_are_classified_not_called_new_papers():
    coverage, scope, _ = reports()
    reviews = scope["official_new_directory_dispositions"]
    assert len(reviews) == 5
    assert Counter(row["decision"] for row in reviews) == {
        "outside_topic_scope": 3, "archived_source_exception": 1, "selected_historical_backfill": 1}
    tdc = next(row for row in reviews if row["decision"] == "archived_source_exception")
    assert tdc["first_publication_date"] == "2026-10-08"
    assert tdc["exact_first_publication_timestamp"] is None
    assert not tdc["full_text_review_done"] and not tdc["blocking"]
    assert not tdc["automatic_retry"]
    assert all(row["directory_new_url_not_first_publication"] for row in reviews)
    assert coverage["counts"]["google_directory_added_urls_not_new_paper_count"] == 5


def test_failed_directory_is_unknown_never_zero():
    values = inputs()
    row = next(row for row in values[0] if row["source"] == "Meta")
    row["status"] = "unavailable"
    next(row for row in values[2] if row["organization"] == "Meta")["retrieved_pages"] = 0
    coverage, _, _ = reports(values)
    meta = next(row for row in coverage["official_directory_deltas"] if row["organization"] == "Meta")
    assert meta["new_directory_urls"] is None and meta["changed_records"] is None
    assert not meta["delta_known"]
    assert meta["status"] == "source_unavailable_not_zero_delta"


def test_explicit_exceptions_do_not_become_negative_affiliation_or_auto_queue():
    coverage, scope, ledger = reports()
    for report in (coverage, scope, ledger):
        rows = {row["id"]: row for row in report["additional_dispositions"]}
        assert rows["2610.30423"]["decision"] == "not_selected_under_industrial_evidence_gate"
        assert rows["2610.30154"]["decision"] == "archived_identity_date_exception"
        for paper_id in ("2610.30920", "2610.30934"):
            assert rows[paper_id]["verified_priority_organizations"] is None
            assert not rows[paper_id]["full_text_review_done"]
        assert all(not row["automatic_implementation_queue"] and not row["automatic_retry"]
                   for row in rows.values())


@pytest.mark.parametrize("field,value", [("status", "unavailable"), ("parse_complete", False),
                                         ("announced_on", "2026-10-22"), ("parsed_entries", 999)])
def test_bad_bulletin_rejected(field, value):
    values = inputs()
    values[0][0][field] = value
    with pytest.raises(ValueError):
        reports(values)


def test_unreviewed_google_url_rejected():
    values = inputs()
    values[2][0]["new_directory_urls"].append({"title": "unknown", "url": "https://research.google/pubs/new-unreviewed/"})
    with pytest.raises(ValueError, match="requires explicit review"):
        reports(values)


def test_duplicate_category_and_missing_selected_paper_rejected():
    values = inputs()
    values[0][1]["source"] = values[0][0]["source"]
    with pytest.raises(ValueError, match="eight distinct"):
        reports(values)
    values = inputs()
    target = next(page for page in values[0] if any(row["id"] == "2610.30951v1" for row in page.get("records", [])))
    next(row for row in target["records"] if row["id"] == "2610.30951v1")["id"] = "2510.00001v1"
    with pytest.raises(ValueError, match="absent"):
        reports(values)


def test_append_only_and_duplicate_refusal_preserve_prior_batches():
    original = {"schema_version": 1, "batches": [{"batch": "old", "candidates": [{"status": "implemented"}]}]}
    snapshot = deepcopy(original)
    _, _, batch = reports()
    result = audit.append_batch(original, batch)
    assert original == snapshot
    assert result["batches"][:-1] == original["batches"]
    with pytest.raises(ValueError, match="already exists"):
        audit.append_batch(result, batch)


def test_committed_actual_capture_and_pending_scope_if_materialized():
    path = ROOT/audit.AUDIT_REL/"source-coverage.json"
    if not path.exists():
        pytest.skip("actual source capture not materialized yet")
    coverage = json.loads(path.read_text())
    assert coverage["actual_announced_on"] == "2026-10-23"
    assert len(coverage["bulletin_ids_by_category"]) == 8
    assert not coverage["all_sources_exhaustive"] and not coverage["review_watermark_advanced"]
    assert not coverage["full_bulletin_full_text_review_complete"]
    assert coverage["counts"]["category_entries_including_crosslists_and_replacements"] == 1260
    scope = json.loads((path.parent/"task-scope.json").read_text())
    assert set(scope["fixed_component_keys"]) == audit.COMPONENT_KEYS
    assert set(scope["reference_only_keys"]) == audit.REFERENCE_KEYS
