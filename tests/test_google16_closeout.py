"""Exact accepted16 scope; interfaces, diagnostics and full experiments differ."""
import hashlib
import json
from pathlib import Path

import pytest

from auto_research.discovery import repository_paper_records
from auto_research.gpu_validation import load_gpu_receipt
from scripts.closeout_google16_components import AUDIT, BATCH, GPU_KEYS, KEYS, build

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text())


def test_exact_accepted16_delivered_without_full_experiment_or_capability_claim():
    scope = read(AUDIT/"task-scope.json")
    assert scope["accepted_ids"] == list(KEYS)
    assert scope["component_count"] == 16
    assert scope["gpu_validated_component_count"] == 5
    assert scope["capability_reproductions_claimed"] == 0
    assert scope["review_watermark_advanced"] is scope["all_sources_exhaustive"] is False
    ledger = read(ROOT/"docs/paper-discovery-ledger.json")
    rows = [b for b in ledger["batches"] if b["batch"] == BATCH][0]["candidates"]
    assert {r["id"] for r in rows} == set(KEYS)
    assert all(r["diagnostic_only"] and not r["promotion_eligible"]
               and not r["automatic_implementation_queue"] for r in rows)
    assert all(r["implementation_status"] in {"component_only", "evaluation_protocol_interface"} for r in rows)
    assert next(r for r in rows if r["key"] == "spatial-ads")["full_experiment_resolution"] == "not_applicable_theoretical_paper"
    assert all(r["full_experiment_resolution"].startswith("not_reproduced")
               for r in rows if r["key"] != "spatial-ads")
    records = repository_paper_records(ROOT/"docs/research-manifest.json", ROOT/"docs/paper-discovery-ledger.json")
    assert all(records[identity]["repository_status"] == "catalogued" for identity in KEYS)
    build(check=True)


def test_gpu_receipts_retain_actual_source_hashes_and_diagnostic_limits():
    for key in GPU_KEYS:
        path = ROOT/f"docs/gpu-validations/{key}-a100-20261021.json"
        receipt = load_gpu_receipt(path)
        assert receipt["adapter_key"] == key
        assert "A100" in receipt["accelerator"]["model"]
        assert receipt["diagnostic_only"] and not receipt["promotion_eligible"]
        raw = ROOT/receipt["provenance"]["raw_result_path"]
        assert hashlib.sha256(raw.read_bytes()).hexdigest() == receipt["provenance"]["raw_result_sha256"]
    gate = load_gpu_receipt(ROOT/"docs/gpu-validations/modular-robust-generative-a100-20261021.json")
    assert gate["metrics"]["global_partition_residual"] > .01
    ams = read(AUDIT/"evidence/google16-neural-final-a100-seed42.json")["components"]["activation-model-scanner"]
    assert ams["metrics"]["forward_passes"] == 96
    assert ams["safety_capability_validated"] is False
    assert ams["independent_baseline_used"] is False
    causal = read(AUDIT/"evidence/google16-causal-raw-a100-seed42.json")
    assert causal["security_accuracy_measured"] is False
    assert causal["sanitizer_observed"] is causal["regeneration_observed"] is False


def test_old_39_review_snapshot_remains_asof_not_rewritten():
    old = read(AUDIT.parent/"google-meta-closeout-20261021/google39-reviews.json")
    accepted = [r for r in old["records"] if r["review_decision"] == "accepted"]
    assert {r["id"] for r in accepted} == set(KEYS)
    assert all(r["implementation_status"] == "not_implemented" for r in accepted)
    assert all(r["full_text_review"]["full_article_read"] is False for r in accepted)


def test_checked_in_evidence_survives_squash_merge_without_old_git_refs(monkeypatch):
    import scripts.closeout_google16_components as closeout

    def forbidden(*args, **kwargs):
        raise AssertionError("historical check must use retained executed-source snapshots")

    monkeypatch.setattr(closeout.subprocess, "check_output", forbidden)
    assert closeout.build(check=True)["component_count"] == 16


@pytest.mark.parametrize("corrupt_owned", [False, True])
def test_historical_figure_check_preserves_later_rows_but_rejects_owned_changes(monkeypatch, corrupt_owned):
    from copy import deepcopy
    import scripts.closeout_google16_components as closeout

    path = ROOT/"docs/paper-figures-manifest.json"
    original_read, original_write = closeout.read, closeout.write
    virtual = deepcopy(original_read(path))
    future = {"page": "docs/future/README.md", "arxiv_id": "9999.99999", "sha256": "future-owned"}
    virtual.append(future)
    if corrupt_owned:
        next(row for row in virtual if row.get("arxiv_id") in KEYS)["sha256"] = "wrong-owned-hash"

    def read_with_future(target):
        return deepcopy(virtual) if target == path else original_read(target)

    def check_virtual(target, value, check):
        if target == path:
            assert check and value == virtual, "owned figure fields changed"
            assert value[-1] == future
        else:
            original_write(target, value, check)

    monkeypatch.setattr(closeout, "read", read_with_future)
    monkeypatch.setattr(closeout, "write", check_virtual)
    if corrupt_owned:
        with pytest.raises(AssertionError, match="owned figure fields changed"):
            closeout.build(check=True)
    else:
        assert closeout.build(check=True)["component_count"] == 16
