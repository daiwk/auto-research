"""Window-only selection state must suppress neither new evidence nor real reviews."""
from dataclasses import replace
import datetime as dt
from hashlib import sha256
import json

import pytest

from auto_research.discovery import (
    DiscoveredPaper, build_discovery_payload, paper_metadata_sha256,
    render_discovery_summary, repository_paper_records, repository_paper_statuses,
    repository_paper_versions, triage_candidates,
)
from auto_research.models import Paper


def write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False))


def selection_repo(tmp_path):
    docs = tmp_path / "docs"
    audit = docs / "research-audits/closed"
    paper = Paper("New Method", "An original algorithm.", ["Author"],
                  "2026-10-22T00:00:00Z", "https://arxiv.org/abs/2610.30000v1", "2610.30000v1")
    flags = {
        "priority": "P2", "selection_review_done": True, "method_review_completed": False,
        "fulltext_review_completed": False, "originality_not_rejected": True,
        "automatic_implementation_queue": False,
    }
    entry = {
        "id": "2610.30000", "revision": 1, "title": paper.title,
        "published": paper.published, "metadata_sha256": paper_metadata_sha256(paper), **flags,
    }
    window = {"start": "2026-10-16", "end": "2026-11-09"}
    policy = {
        "window": window, "authorization": {
            "answer": "允许 P2 选题级结案", "p2_selection_closure_allowed": True},
        "terminal_selection_decision": "not_selected_this_window_p2",
        "review_scope": "title-abstract-selection", "always_protected_identities": {},
    }
    write(audit / "p2-selection-policy.json", policy)
    screen = {"window": window, "policy_sha256": sha256(
        (audit / "p2-selection-policy.json").read_bytes()).hexdigest(),
        "protected_records": [], "protected_ids": [],
        "records": [entry | {"decision": "not_selected_this_window_p2", "method_verified": False,
                             "scope": "title-abstract-selection",
                             "high_cost": False, "implementation": False, "automatic_retry": False}]}
    write(audit / "p2-selection-screen.json", screen)
    semantics = "selection-screening-with-protected-primary-review"
    register = {
        "requested_window": window,
        "candidate_review_complete": True, "selection_review_complete": True,
        "method_review_complete": False, "review_semantics": semantics,
        "papers": [entry | {"status": "not_selected_p2", "review_scope": "title-abstract-selection",
                            "protected_priority_signal": False, "protected_production_signal": False}],
    }
    write(audit / "paper-register.json", register)
    state = {
        "review_semantics": semantics, "selection_review_complete": True,
        "method_review_complete": False, "window": window, "review_watermark": "2026-11-09",
        "candidate_register": "research-audits/closed/paper-register.json",
        "selection_policy": "research-audits/closed/p2-selection-policy.json",
    }
    write(docs / "paper-discovery-watermark.json", state)
    write(docs / "research-manifest.json", {"papers": []})
    write(docs / "paper-discovery-ledger.json", {"batches": []})
    write(docs / "paper-discovery-versions.json", {"papers": []})
    return docs, paper


def load(docs):
    return (repository_paper_statuses(docs / "research-manifest.json", docs / "paper-discovery-ledger.json"),
            repository_paper_versions(docs / "paper-discovery-versions.json"))


def test_exact_selection_is_not_repeated_historical_method_review(tmp_path):
    docs, paper = selection_repo(tmp_path)
    statuses, versions = load(docs)
    assert statuses == {"2610.30000": "selection-reviewed"}
    row = triage_candidates([DiscoveredPaper(paper, ())], statuses, repository_versions=versions)[0]
    assert row["selection_only"] is True and row["method_verified"] is False
    assert row["review_required"] is row["historical_review_required"] is False
    assert row["accepted_unimplemented"] is row["automatic_implementation_queue"] is False
    assert row["evidence_status"] == "selection-reviewed-method-unverified"
    payload = build_discovery_payload(track="agent", start_date=dt.date(2026, 11, 8),
                                     end_date=dt.date(2026, 11, 11), query_names=(), candidates=[row])
    assert payload["triage_counts"]["selection-reviewed"] == 1
    assert payload["triage_counts"]["reviewed"] == 0
    assert "方法未核验" in render_discovery_summary(payload)


@pytest.mark.parametrize("kind", ["revision", "metadata", "priority-query", "priority-source", "missing-baseline"])
def test_selection_reopens_instead_of_hiding_new_evidence(tmp_path, kind):
    docs, paper = selection_repo(tmp_path)
    statuses, versions = load(docs)
    queries, provenance = (), ()
    if kind == "revision":
        paper = replace(paper, arxiv_id="2610.30000v2", url="https://arxiv.org/abs/2610.30000v2")
    elif kind == "metadata":
        paper = replace(paper, abstract="Changed algorithm and online evidence.")
    elif kind == "priority-query":
        queries = ("priority-org-google",)
    elif kind == "priority-source":
        provenance = ({"source_url": "https://ai.meta.com/research/publications/new/"},)
    else:
        versions = {}
    row = triage_candidates([DiscoveredPaper(paper, queries, provenance)], statuses,
                            repository_versions=versions)[0]
    assert row["selection_reopened"] is row["review_required"] is True
    if kind.startswith("priority"):
        assert row["priority_review_required"] is True
        assert row["selection_reopen_reason"] == "new-priority-evidence-after-selection"
        assert row["revision_review_required"] is False  # A new source is not a new arXiv revision.
    else:
        assert row["revision_review_required"] is True


@pytest.mark.parametrize("mutation", [
    "state-semantics", "authorization", "register-flags", "protected", "hash",
    "implemented", "component_only",
])
def test_only_complete_authorized_current_register_can_suppress_recall(tmp_path, mutation):
    docs, _ = selection_repo(tmp_path)
    audit = docs / "research-audits/closed"
    if mutation == "state-semantics":
        path = docs / "paper-discovery-watermark.json"
        obj = json.loads(path.read_text()); obj["review_semantics"] = "old-date-only-triage"
    elif mutation == "authorization":
        path = audit / "p2-selection-policy.json"
        obj = json.loads(path.read_text()); obj["authorization"]["p2_selection_closure_allowed"] = False
    elif mutation in {"register-flags", "implemented", "component_only"}:
        path = audit / "paper-register.json"
        obj = json.loads(path.read_text())
        if mutation == "register-flags":
            obj["papers"][0]["method_review_completed"] = True
        else:
            obj["papers"][0]["implementation_status"] = mutation
    else:
        path = audit / "p2-selection-screen.json"
        obj = json.loads(path.read_text())
        if mutation == "protected":
            obj["protected_ids"] = ["2610.40000"]
        else:
            obj["policy_sha256"] = "stale"
    write(path, obj)
    assert load(docs) == ({}, {})


def test_real_catalog_and_substantive_review_outrank_window_selection(tmp_path):
    docs, paper = selection_repo(tmp_path)
    write(docs / "research-manifest.json", {"papers": [{
        "paper_url": paper.url, "implementation_status": "component_only"}]})
    assert load(docs)[0]["2610.30000"] == "catalogued"
    write(docs / "research-manifest.json", {"papers": []})
    write(docs / "paper-discovery-ledger.json", {"batches": [{"candidates": [{
        "id": "2610.30000", "status": "rejected", "review_decision": "rejected",
        "resolution": "not_selected_after_protected_original_review", "review_done": True,
        "full_text_review": {"scope": "full-text", "source_locations": ["§3"]},
    }]}]})
    records = repository_paper_records(docs / "research-manifest.json", docs / "paper-discovery-ledger.json")
    assert records["2610.30000"]["repository_status"] == "reviewed"


def test_metadata_only_baseline_is_replaced_by_exact_authorized_selection(tmp_path):
    docs, _ = selection_repo(tmp_path)
    write(docs / "paper-discovery-versions.json", {"papers": [{
        "arxiv_id": "2610.30000", "revision": 1, "metadata_sha256": "old",
        "review_scope": "historical_metadata_identity_date_scope_only"}]})
    versions = load(docs)[1]
    assert versions["2610.30000"]["selection_only"] is True
