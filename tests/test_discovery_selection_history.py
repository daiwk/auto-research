"""Validated selection history survives watermark advances without hiding new evidence."""
from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path

import pytest

from auto_research.discovery import (
    DiscoveredPaper, _window_selection_records, paper_metadata_sha256,
    repository_paper_records, repository_paper_statuses, repository_paper_versions,
    triage_candidates,
)
from auto_research.models import Paper


SEMANTICS = "selection-screening-with-protected-primary-review"


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def read(path):
    return json.loads(path.read_bytes())


def window_state(docs, name, window, papers, *, previous=None):
    audit = docs / "research-audits" / name
    policy = {
        "window": window, "authorization": {"answer": "允许 P2 选题级结案",
                                            "p2_selection_closure_allowed": True},
        "terminal_selection_decision": "not_selected_this_window_p2",
        "review_scope": "title-abstract-selection", "always_protected_identities": {},
    }
    policy_path = audit / "p2-selection-policy.json"
    write(policy_path, policy)
    entries = []
    for paper in papers:
        entries.append({
            "id": paper.arxiv_id.split("v")[0], "revision": int(paper.arxiv_id.split("v")[1]),
            "title": paper.title, "published": paper.published,
            "metadata_sha256": paper_metadata_sha256(paper), "priority": "P2",
            "selection_review_done": True, "method_review_completed": False,
            "fulltext_review_completed": False, "originality_not_rejected": True,
            "automatic_implementation_queue": False,
        })
    write(audit / "p2-selection-screen.json", {
        "window": window, "policy_sha256": sha256(policy_path.read_bytes()).hexdigest(),
        "protected_records": [], "protected_ids": [],
        "records": [r | {"decision": "not_selected_this_window_p2", "method_verified": False,
                          "scope": "title-abstract-selection", "high_cost": False,
                          "implementation": False, "automatic_retry": False} for r in entries],
    })
    write(audit / "paper-register.json", {
        "requested_window": window, "candidate_review_complete": True,
        "selection_review_complete": True, "method_review_complete": False,
        "review_semantics": SEMANTICS,
        "papers": [r | {"status": "not_selected_p2", "review_scope": "title-abstract-selection",
                         "protected_priority_signal": False, "protected_production_signal": False}
                   for r in entries],
    })
    state = {
        "window": window, "review_watermark": window["end"], "review_semantics": SEMANTICS,
        "selection_review_complete": True, "method_review_complete": False,
        "candidate_register": (audit / "paper-register.json").relative_to(docs).as_posix(),
        "selection_policy": policy_path.relative_to(docs).as_posix(),
    }
    if previous is not None:
        state |= {"previous_review_state": previous.relative_to(docs).as_posix(),
                  "previous_review_state_sha256": sha256(previous.read_bytes()).hexdigest()}
    path = audit / "closed-watermark-proposal.json"
    write(path, state)
    return path


def history_repo(tmp_path, *, current_papers=None):
    docs = tmp_path / "docs"
    old = Paper("Old Method", "An original old algorithm.", ["A"], "2026-10-22T00:00:00Z",
                "https://arxiv.org/abs/2610.30000v1", "2610.30000v1")
    new = Paper("New Method", "An original new algorithm.", ["B"], "2026-11-11T00:00:00Z",
                "https://arxiv.org/abs/2611.13000v1", "2611.13000v1")
    previous = window_state(docs, "nov09", {"start": "2026-10-16", "end": "2026-11-09"}, [old])
    current = window_state(docs, "nov15", {"start": "2026-11-10", "end": "2026-11-15"},
                           [new] if current_papers is None else current_papers, previous=previous)
    write(docs / "paper-discovery-watermark.json", read(current))
    for name, value in (("research-manifest.json", {"papers": []}),
                        ("paper-discovery-ledger.json", {"batches": []}),
                        ("paper-discovery-versions.json", {"papers": []})):
        write(docs / name, value)
    return docs, old, new


def load(docs):
    return (repository_paper_statuses(docs / "research-manifest.json", docs / "paper-discovery-ledger.json"),
            repository_paper_versions(docs / "paper-discovery-versions.json"))


def fingerprints(docs):
    return {str(p.relative_to(docs)): sha256(p.read_bytes()).hexdigest()
            for p in docs.rglob("*") if p.is_file()}


def test_previous_selection_is_retained_read_only_after_watermark_advance(tmp_path):
    docs, old, new = history_repo(tmp_path)
    before = fingerprints(docs)
    statuses, versions = load(docs)
    assert statuses == {"2610.30000": "selection-reviewed", "2611.13000": "selection-reviewed"}
    assert set(versions) == set(statuses)
    for paper in (old, new):
        row = triage_candidates([DiscoveredPaper(paper, ())], statuses, repository_versions=versions)[0]
        assert row["selection_only"] and not row["review_required"] and not row["method_verified"]
        assert not row["automatic_implementation_queue"]
    assert versions["2610.30000"]["selection_artifact"].startswith("research-audits/nov09/")
    assert fingerprints(docs) == before


def test_three_windows_merge_with_latest_exact_observation_winning(tmp_path):
    docs, old, _ = history_repo(tmp_path)
    oldest = replace(old, title="Earliest Method", arxiv_id="2609.10000v1",
                     url="https://arxiv.org/abs/2609.10000v1", published="2026-09-10T00:00:00Z")
    older_path = window_state(docs, "oct15", {"start": "2026-09-01", "end": "2026-10-15"}, [oldest])
    old_path = window_state(docs, "nov09", {"start": "2026-10-16", "end": "2026-11-09"},
                            [old], previous=older_path)
    replacement = replace(old, title="Revised old method", abstract="New revision evidence.",
                          arxiv_id="2610.30000v2", url="https://arxiv.org/abs/2610.30000v2")
    current = window_state(docs, "nov15", {"start": "2026-11-10", "end": "2026-11-15"},
                           [replacement], previous=old_path)
    write(docs / "paper-discovery-watermark.json", read(current))
    statuses, versions = load(docs)
    assert set(statuses) == {"2609.10000", "2610.30000"}
    assert versions["2610.30000"]["revision"] == 2
    assert versions["2610.30000"]["metadata_sha256"] == paper_metadata_sha256(replacement)
    assert "/nov15/" in versions["2610.30000"]["selection_artifact"]


def test_valid_empty_new_window_does_not_erase_old_selection(tmp_path):
    docs, _, _ = history_repo(tmp_path, current_papers=[])
    assert load(docs)[0] == {"2610.30000": "selection-reviewed"}


@pytest.mark.parametrize("kind", ["revision", "metadata", "priority-query", "priority-source", "production"])
def test_historical_selection_reopens_on_new_evidence(tmp_path, kind):
    docs, paper, _ = history_repo(tmp_path)
    statuses, versions = load(docs)
    queries, sources = (), ()
    if kind == "revision":
        paper = replace(paper, arxiv_id="2610.30000v2", url="https://arxiv.org/abs/2610.30000v2")
    elif kind == "metadata":
        paper = replace(paper, abstract="New evidence is not the frozen abstract.")
    elif kind == "priority-query":
        queries = ("priority-org-google",)
    elif kind == "priority-source":
        sources = ({"source_url": "https://research.meta.ai/papers/new/"},)
    else:
        sources = ({"source_url": "https://arxiv.org/html/2610.30000v1#S5",
                    "production_evidence": {"kind": "production_ab",
                                            "excerpt": "Randomized A/B on real user traffic."}},)
    row = triage_candidates([DiscoveredPaper(paper, queries, sources)], statuses,
                            repository_versions=versions)[0]
    assert row["selection_reopened"] and row["review_required"]
    if kind == "production":
        assert row["production_review_required"]


@pytest.mark.parametrize("mutation", [
    "authorization", "policy-hash", "register-flags", "screen-partition", "protected", "implemented",
])
def test_invalid_historical_window_fails_open_instead_of_suppressing(tmp_path, mutation):
    docs, _, _ = history_repo(tmp_path)
    audit = docs / "research-audits/nov09"
    if mutation == "authorization":
        path = audit / "p2-selection-policy.json"
        obj = read(path); obj["authorization"]["p2_selection_closure_allowed"] = False
    elif mutation in {"register-flags", "implemented"}:
        path = audit / "paper-register.json"; obj = read(path)
        if mutation == "register-flags":
            obj["papers"][0]["method_review_completed"] = True
        else:
            obj["papers"][0]["implementation_status"] = "implemented"
    else:
        path = audit / "p2-selection-screen.json"; obj = read(path)
        if mutation == "policy-hash":
            obj["policy_sha256"] = "stale"
        elif mutation == "screen-partition":
            obj["records"] = []
        else:
            obj["protected_records"] = [{"id": "2610.99999"}]
    write(path, obj)
    assert load(docs) == ({}, {})


@pytest.mark.parametrize("mutation", [
    "missing-hash", "missing-link", "wrong-hash", "missing-file", "outside", "absolute",
    "in-tree-absolute", "cycle",
    "nonmonotonic-end", "nonmonotonic-start", "reversed-window",
])
def test_unsafe_or_inconsistent_history_links_fail_open(tmp_path, mutation):
    docs, _, _ = history_repo(tmp_path)
    path = docs / "paper-discovery-watermark.json"
    state = read(path)
    if mutation == "missing-hash":
        del state["previous_review_state_sha256"]
    elif mutation == "missing-link":
        del state["previous_review_state"]
    elif mutation == "wrong-hash":
        state["previous_review_state_sha256"] = "0" * 64
    elif mutation == "missing-file":
        state["previous_review_state"] = "research-audits/absent.json"
    elif mutation == "in-tree-absolute":
        state["previous_review_state"] = str(docs / state["previous_review_state"])
    elif mutation in {"outside", "absolute"}:
        outside = tmp_path / "outside.json"
        write(outside, read(docs / state["previous_review_state"]))
        state["previous_review_state"] = str(outside) if mutation == "absolute" else "../outside.json"
        state["previous_review_state_sha256"] = sha256(outside.read_bytes()).hexdigest()
    elif mutation == "cycle":
        state["previous_review_state"] = "paper-discovery-watermark.json"
    else:
        prior_path = docs / state["previous_review_state"]
        prior = read(prior_path)
        if mutation == "nonmonotonic-end":
            prior["window"]["end"] = "2026-11-15"
        elif mutation == "nonmonotonic-start":
            prior["window"]["start"] = "2026-11-11"
            prior["window"]["end"] = "2026-11-12"
        else:
            prior["window"] = {"start": "2026-11-12", "end": "2026-11-09"}
        prior["review_watermark"] = prior["window"]["end"]
        write(prior_path, prior)
        state["previous_review_state_sha256"] = sha256(prior_path.read_bytes()).hexdigest()
    write(path, state)
    assert load(docs) == ({}, {})


def test_history_cannot_escape_docs_through_symlink(tmp_path):
    docs, _, _ = history_repo(tmp_path)
    state_path = docs / "paper-discovery-watermark.json"
    state = read(state_path)
    outside = tmp_path / "outside.json"
    outside.write_bytes((docs / state["previous_review_state"]).read_bytes())
    link = docs / "alias.json"; link.symlink_to(outside)
    state |= {"previous_review_state": "alias.json",
              "previous_review_state_sha256": sha256(outside.read_bytes()).hexdigest()}
    write(state_path, state)
    assert _window_selection_records(docs) == {}


def test_invalid_current_state_does_not_fall_back_to_history(tmp_path):
    docs, _, _ = history_repo(tmp_path)
    path = docs / "paper-discovery-watermark.json"
    state = read(path); state["method_review_complete"] = True
    write(path, state)
    assert load(docs) == ({}, {})


def test_symlink_cycle_is_a_fail_open_source_failure(tmp_path):
    docs, _, _ = history_repo(tmp_path)
    (docs / "loop-a.json").symlink_to("loop-b.json")
    (docs / "loop-b.json").symlink_to("loop-a.json")
    path = docs / "paper-discovery-watermark.json"
    state = read(path); state["previous_review_state"] = "loop-a.json"
    write(path, state)
    assert _window_selection_records(docs) == {}


def test_catalogued_observation_still_outranks_historical_selection(tmp_path):
    docs, old, _ = history_repo(tmp_path)
    write(docs / "research-manifest.json", {"papers": [{
        "paper_url": old.url, "implementation_status": "component_only"}]})
    records = repository_paper_records(docs / "research-manifest.json", docs / "paper-discovery-ledger.json")
    assert records["2610.30000"]["repository_status"] == "catalogued"
    assert records["2610.30000"]["implementation_status"] == "component_only"
    assert not records["2610.30000"].get("selection_only", False)
