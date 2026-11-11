"""The P2 selection closure must not pretend to be a substantive paper review."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "nov09_p2_selection_tested", SCRIPTS / "screen_nov09_p2_selection.py")
assert SPEC and SPEC.loader
screen = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(screen)


def fixture(monkeypatch, abstract="We introduce a new public benchmark and original algorithm."):
    row = {
        "arxiv_id": "2610.30000", "revision": 1, "title": "A New Algorithm",
        "abstract": abstract, "published": "2026-10-22T00:00:00Z",
        "metadata_sha256": "metadata", "captures": ["capture.json"],
        "priority_review_required": False, "priority_source_matches": [],
        "priority_query_matches": [], "source_provenance": [],
    }
    receipts = {"capture.json": "capture-hash"}
    frozen = {
        "window": screen.WINDOW, "source_inventory_commit": "frozen-commit",
        "source_inventory_sha256": "frozen-inventory-hash", "frozen_pending_count": 1,
        "source_receipts": receipts,
        "records": [["2610.30000", 1, ["foundation-model"], "P2", "model_mention", {}]],
    }
    policy = {
        "window": screen.WINDOW, "terminal_selection_decision": screen.DECISION,
        "review_scope": screen.SCOPE, "input_inventory_sha256": "frozen-inventory-hash",
        "frozen_pending_count": 1, "always_protected_identities": {},
        "frozen_input_sha256": sha256(screen.stable_json(frozen)).hexdigest(),
        "authorization": {"p2_selection_closure_allowed": True},
    }
    monkeypatch.setattr(screen, "load_observations", lambda _: ({("2610.30000", 1): row}, receipts))
    return row, frozen, policy


def test_original_algorithm_is_only_window_selection_not_originality_rejection(monkeypatch):
    _, frozen, policy = fixture(monkeypatch)
    output = screen.build(Path("unused"), frozen, policy)
    row = output["records"][0]
    assert row["decision"] == "not_selected_this_window_p2"
    assert row["selection_review_done"] is True
    assert row["originality_not_rejected"] is True
    assert row["method_verified"] is row["method_review_completed"] is False
    assert row["fulltext_review_completed"] is row["high_cost"] is row["implementation"] is False
    assert output["global_substantive_ledger_write"] is False
    assert output["counts"] == {
        "frozen_pending": 1, "selected_window_only": 1,
        "protected_pending_original": 0, "excluded_primary": 0,
    }


@pytest.mark.parametrize("abstract,signal", [
    ("Developed at Google Research.", "text_organization_mention"),
    ("We observe an A/B result on real traffic.", "text_production_mention"),
    ("The system is deployed to external users.", "deployment_signal"),
])
def test_positive_priority_or_production_signals_are_protected(monkeypatch, abstract, signal):
    _, frozen, policy = fixture(monkeypatch, abstract)
    output = screen.build(Path("unused"), frozen, policy)
    assert not output["records"]
    assert output["protected_ids"] == ["2610.30000"]
    assert signal in output["protected_records"][0]["protection_reasons"]


def test_generic_future_deployment_motivation_is_not_an_ab_claim(monkeypatch):
    _, frozen, policy = fixture(monkeypatch, "Our method may support resource-efficient future deployment.")
    assert screen.build(Path("unused"), frozen, policy)["records"]


@pytest.mark.parametrize("protected_route", ["industrial_application", "official_priority"])
def test_frozen_priority_routes_cannot_be_downgraded(monkeypatch, protected_route):
    _, frozen, policy = fixture(monkeypatch)
    frozen["records"][0][4] = protected_route
    policy["frozen_input_sha256"] = sha256(screen.stable_json(frozen)).hexdigest()
    output = screen.build(Path("unused"), frozen, policy)
    assert not output["records"]
    assert output["protected_ids"] == ["2610.30000"]


def test_explicit_known_author_or_production_identity_stays_protected(monkeypatch):
    _, frozen, policy = fixture(monkeypatch)
    policy["always_protected_identities"]["2610.30000"] = "known-author recall"
    output = screen.build(Path("unused"), frozen, policy)
    assert output["protected_records"][0]["protection_reasons"]["policy_protected_identity"]


def test_fingerprinted_semantic_clarification_does_not_clear_source_priority(monkeypatch, tmp_path):
    row, frozen, policy = fixture(monkeypatch, "We evaluate a Google model on a public dataset.")
    clarification = {
        "id": row["arxiv_id"], "revision": 1, "metadata_sha256": "metadata",
        "cleared_protection_rules": ["text_organization_mention"],
        "abstract_witness": "evaluate a Google model", "reason": "model vendor, not an affiliation assertion",
        "fulltext_review_completed": False, "priority_attribution_verified": False,
    }
    path = tmp_path / "clarification.json"
    path.write_text(json.dumps({"clarifications": [clarification]}))
    output = screen.build(Path("unused"), frozen, policy, protection_review_json=[path])
    assert output["records"][0]["signal_clarifications"]
    row["priority_review_required"] = True
    assert screen.build(Path("unused"), frozen, policy, protection_review_json=[path])["protected_ids"]
    clarification["cleared_protection_rules"] = ["source_priority_flag"]
    path.write_text(json.dumps({"clarifications": [clarification]}))
    with pytest.raises(ValueError, match="overbroad"):
        screen.build(Path("unused"), frozen, policy, protection_review_json=[path])


def test_only_exact_completed_originals_are_dynamically_excluded(monkeypatch, tmp_path):
    row, frozen, policy = fixture(monkeypatch)
    review = {key: row[key] for key in ("revision", "title", "published", "metadata_sha256")}
    review.update({
        "id": row["arxiv_id"], "review_done": True, "fulltext_review_completed": True,
        "source_url": "https://arxiv.org/html/2610.30000v1", "source_sha256": "source-hash",
        "decision": "rejected", "resolution": "original_checked_not_selected", "reason": "scoped review",
    })
    path = tmp_path / "original.json"
    path.write_text(json.dumps({"reviews": [review]}))
    output = screen.build(Path("unused"), frozen, policy, exclude_primary_json=[path])
    assert output["excluded_primary_ids"] == [row["arxiv_id"]]
    assert not output["records"] and not output["protected_ids"]
    review["revision"] = 2
    path.write_text(json.dumps({"reviews": [review]}))
    with pytest.raises(ValueError, match="incomplete primary"):
        screen.build(Path("unused"), frozen, policy, exclude_primary_json=[path])


def test_source_receipts_and_window_authorization_are_enforced(monkeypatch):
    row, frozen, policy = fixture(monkeypatch)
    wrong = deepcopy(policy)
    wrong["authorization"]["p2_selection_closure_allowed"] = False
    with pytest.raises(ValueError, match="policy"):
        screen.build(Path("unused"), frozen, wrong)
    row["published"] = "2026-11-10T00:00:00Z"
    with pytest.raises(ValueError, match="outside"):
        screen.build(Path("unused"), frozen, policy)
    row["published"] = "2026-10-22T00:00:00Z"
    wrong = deepcopy(frozen)
    wrong["source_receipts"]["capture.json"] = "changed"
    policy["frozen_input_sha256"] = sha256(screen.stable_json(wrong)).hexdigest()
    with pytest.raises(ValueError, match="receipts"):
        screen.build(Path("unused"), wrong, policy)
