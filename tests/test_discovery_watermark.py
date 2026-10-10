import json

import pytest

from auto_research.discovery_watermark import POLICY, audit_review_watermark, partition_archived_official_reviews


def _write(root, name, value):
    path = root / "docs" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def _fixture(root):
    state = {
        "schema_version": 2, "policy": POLICY, "user_authorized_exceptions": True,
        "authorization_record": "User permits explicitly documented unreachable metadata exceptions.",
        "window": {"start": "2026-10-01", "end": "2026-10-07"},
        "review_watermark": "2026-10-07",
        "all_sources_exhaustive": False, "implementation_complete": False,
        "candidate_register": "register.json", "retrieval_receipts": [], "source_reviews": [],
        "coverage_scope": {
            "tracks": ["recommendation", "foundation-model", "post-training", "agent"],
            "recall_modes": ["submission-window", "late-index"],
            "official_sources": [], "limitations": "No claim of whole-web exhaustiveness.",
        },
        "exception_archive": "exceptions.json",
    }
    _write(root, "register.json", {"candidate_review_complete": True, "papers": [{
        "id": "2610.00001", "status": "accepted",
        "reviews": [{"decision": "accepted", "fulltext_review_completed": True}],
    }]})
    for track in ("recommendation", "foundation-model", "post-training", "agent"):
        for mode in ("submission-window", "late-index"):
            artifact = f"{track}-{mode}.json"
            state["retrieval_receipts"].append({"track": track, "mode": mode, "artifact": artifact})
            _write(root, artifact, {"window": state["window"], "arxiv_transport": {
                "coverage_complete": True, "transport_complete": True,
                "capped_queries": 0, "failed_queries": 0,
            }, "candidates": [{"arxiv_id": "2610.00001"}]})
    row = {
        "url": "https://example.test/paper", "review_status": "explicit_exception",
        "exception_type": "date_or_identity_unresolved", "reason": "Official page only gives a year.",
        "attempts": ["official detail", "exact title match"], "counts_as_accepted": False,
        "scope_triage_completed": True, "reopen_when": "Official identity or date changes.",
    }
    for org in ("Google", "Meta"):
        name = f"{org}.json"
        state["source_reviews"].append({"organization": org, "artifact": name})
        state["coverage_scope"]["official_sources"].append({"organization": org, "records": 1, "pages": 1})
        _write(root, name, {"window": state["window"], "expected_records": 1, "pages": ["page1"],
                            "records": [row], "directory_exceptions": []})
    _write(root, "exceptions.json", {
        "record_count": 2, "blocking": False, "retry_policy": "on-new-evidence-only",
        "entries": [dict(row, organization=org, status="archived", blocking=False)
                    for org in ("Google", "Meta")],
    })
    _write(root, "paper-discovery-watermark.json", state)
    return state


def test_explicit_exceptions_can_close_scoped_review_but_not_claim_exhaustiveness(tmp_path):
    _fixture(tmp_path)
    assert audit_review_watermark(tmp_path) == []


@pytest.mark.parametrize("field,value,error", [
    ("user_authorized_exceptions", False, "authorization"),
    ("all_sources_exhaustive", True, "exhaustiveness"),
    ("implementation_complete", True, "implementation"),
    ("review_watermark", "2026-10-10", "watermarks"),
    ("retrieval_receipts", [], "recall channels"),
])
def test_invalid_watermark_claims_are_rejected(tmp_path, field, value, error):
    state = _fixture(tmp_path)
    state[field] = value
    _write(tmp_path, "paper-discovery-watermark.json", state)
    assert any(error in e for e in audit_review_watermark(tmp_path))


@pytest.mark.parametrize("field,value,error", [
    ("scope_triage_completed", False, "unread"),
    ("attempts", [], "attempts"),
    ("counts_as_accepted", True, "accepted"),
    ("reopen_when", "", "reopening"),
])
def test_exceptions_must_be_reviewed_attempted_and_reopenable(tmp_path, field, value, error):
    _fixture(tmp_path)
    payload = json.loads((tmp_path / "docs/Google.json").read_text())
    payload["records"][0][field] = value
    _write(tmp_path, "Google.json", payload)
    assert any(error in e for e in audit_review_watermark(tmp_path))


def test_capped_recall_and_unread_candidate_block_even_exception_policy(tmp_path):
    _fixture(tmp_path)
    path = tmp_path / "docs/agent-late-index.json"
    payload = json.loads(path.read_text())
    payload["arxiv_transport"]["capped_queries"] = 1
    _write(tmp_path, path.name, payload)
    register = json.loads((tmp_path / "docs/register.json").read_text())
    register["papers"][0]["status"] = "pending"
    _write(tmp_path, "register.json", register)
    errors = audit_review_watermark(tmp_path)
    assert any("capped" in e for e in errors)
    assert any("unread" in e for e in errors)


def test_accepted_candidate_still_requires_full_text(tmp_path):
    _fixture(tmp_path)
    register = json.loads((tmp_path / "docs/register.json").read_text())
    register["papers"][0]["reviews"][0]["fulltext_review_completed"] = False
    _write(tmp_path, "register.json", register)
    assert any("full text" in e for e in audit_review_watermark(tmp_path))


def test_artifacts_cannot_escape_docs(tmp_path):
    state = _fixture(tmp_path)
    state["candidate_register"] = "../../private.json"
    _write(tmp_path, "paper-discovery-watermark.json", state)
    assert any("inside docs" in e for e in audit_review_watermark(tmp_path))


def test_current_paper_cannot_be_relabelled_historical_to_advance(tmp_path):
    _fixture(tmp_path)
    payload = json.loads((tmp_path / "docs/Google.json").read_text())
    row = payload["records"][0]
    row.update(review_status="historical", date_evidence=["2026-10-03"], arxiv_ids=["2610.00001"])
    _write(tmp_path, "Google.json", payload)
    assert any("historical" in e for e in audit_review_watermark(tmp_path))
    row["date_evidence"] = ["2026-09-30"]
    _write(tmp_path, "Google.json", payload)
    _remove_google_exception(tmp_path)
    assert audit_review_watermark(tmp_path) == []


def test_after_window_requires_post_window_publication_evidence(tmp_path):
    _fixture(tmp_path)
    payload = json.loads((tmp_path / "docs/Google.json").read_text())
    row = payload["records"][0]
    row.update(review_status="after_window", date_evidence=["2026-10-08"])
    _write(tmp_path, "Google.json", payload)
    _remove_google_exception(tmp_path)
    assert audit_review_watermark(tmp_path) == []
    row['date_evidence'].append("2026-10-07")
    _write(tmp_path, "Google.json", payload)
    assert any("after-window" in e for e in audit_review_watermark(tmp_path))


def test_structured_primary_date_evidence_is_preserved(tmp_path):
    _fixture(tmp_path)
    payload = json.loads((tmp_path / "docs/Google.json").read_text())
    row = payload["records"][0]
    row.update(review_status="historical", date_evidence=[{
        "date": "2026-09-23", "type": "arxiv_v1_submission",
        "url": "https://arxiv.org/abs/2609.28776", "location": "submission history",
    }])
    _write(tmp_path, "Google.json", payload)
    _remove_google_exception(tmp_path)
    assert audit_review_watermark(tmp_path) == []
    row["date_evidence"][0]["date"] = "2026-10-03"
    _write(tmp_path, "Google.json", payload)
    assert any("historical" in e for e in audit_review_watermark(tmp_path))


def test_month_precision_cannot_hide_a_window_overlap(tmp_path):
    _fixture(tmp_path)
    payload = json.loads((tmp_path / "docs/Google.json").read_text())
    row = payload["records"][0]
    row.update(review_status="historical", date_evidence=[{
        "date": "2026-09", "precision": "month", "url": "https://example.test/publication",
    }])
    _write(tmp_path, "Google.json", payload)
    _remove_google_exception(tmp_path)
    assert audit_review_watermark(tmp_path) == []
    row["date_evidence"][0]["date"] = "2026-10"
    _write(tmp_path, "Google.json", payload)
    assert any("historical" in e for e in audit_review_watermark(tmp_path))


def test_different_window_receipts_cannot_be_reused(tmp_path):
    _fixture(tmp_path)
    payload = json.loads((tmp_path / "docs/Google.json").read_text())
    payload["window"]["end"] = "2026-10-02"
    _write(tmp_path, "Google.json", payload)
    assert any("different window" in e for e in audit_review_watermark(tmp_path))


def _remove_google_exception(root):
    payload = json.loads((root / "docs/exceptions.json").read_text())
    payload["entries"] = [e for e in payload["entries"] if e["organization"] != "Google"]
    payload["record_count"] = len(payload["entries"])
    _write(root, "exceptions.json", payload)


def test_retired_strict_watermark_is_rejected(tmp_path):
    state = _fixture(tmp_path)
    state["source_exhaustiveness_watermark"] = "2026-10-02"
    _write(tmp_path, "paper-discovery-watermark.json", state)
    assert any("retired" in e for e in audit_review_watermark(tmp_path))


@pytest.mark.parametrize("field,value", [("blocking", True), ("retry_policy", "retry-every-run"),
                                        ("record_count", 1), ("entries", [])])
def test_archive_is_complete_nonblocking_and_only_reopened_on_new_evidence(tmp_path, field, value):
    _fixture(tmp_path)
    payload = json.loads((tmp_path / "docs/exceptions.json").read_text())
    payload[field] = value
    _write(tmp_path, "exceptions.json", payload)
    assert audit_review_watermark(tmp_path)


def test_coverage_counts_cannot_be_inflated(tmp_path):
    state = _fixture(tmp_path)
    state["coverage_scope"]["official_sources"][0]["records"] = 100
    _write(tmp_path, "paper-discovery-watermark.json", state)
    assert any("coverage scope count" in e for e in audit_review_watermark(tmp_path))


@pytest.mark.parametrize("new_evidence", [None, "date", "title", "source"])
def test_archived_official_queue_reopens_only_with_new_evidence(new_evidence):
    source = {"organization": "Google", "url": "https://example.test/paper"}
    item = {"title": "Unresolved paper", "source_published": None, "sources": [source]}
    archive = {"entries": [dict(source, title=item["title"], status="archived", blocking=False)]}
    if new_evidence == "date":
        item["source_published"] = "2026-10-06"
    elif new_evidence == "title":
        item["title"] = "Updated paper identity"
    elif new_evidence == "source":
        item["sources"].append({"organization": "Meta", "url": "https://example.test/new-source"})
    active, archived = partition_archived_official_reviews([item], archive)
    assert active == ([item] if new_evidence else [])
    assert archived == ([] if new_evidence else [item])
