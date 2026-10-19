"""Offline Oct19 scope and evidence mutation tests; no GPU or old Git refs needed.

Most tests intentionally require the final committed metric/receipt/proof files.
Missing evidence is a failure, not a skip. The shared-commit union unit test uses
an explicit mock proof to test curator bookkeeping without claiming execution.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path

import pytest

from auto_research.gpu_validation import load_gpu_receipt
from auto_research.paper_specs.catalog import catalog_records

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("oct19_evidence", ROOT / "scripts/curate_oct19_component_evidence.py")
admission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admission)

EXPECTED_COMPONENTS = {"skill-state", "alpha-diana", "agent-perturb", "diverge-ideation", "fpot", "lamp", "knowgpo"}
EXPECTED_REFERENCES = {"auto-sft", "gen4p"}
EXPECTED_SCOPE = EXPECTED_COMPONENTS | EXPECTED_REFERENCES


def records():
    return {row["key"]: row for row in catalog_records() if row["key"] in EXPECTED_SCOPE}


def metric_for(key):
    device, _, (domain, identity, _) = admission.item_for(key)
    path = ROOT / f"docs/{domain}/{identity}-{key}/metrics/component-{device}-seeds42-44.json"
    assert path.is_file(), f"final measured evidence is required, not skipped: {path}"
    return json.loads(path.read_text())


def receipt_for(key):
    return load_gpu_receipt(ROOT / records()[key]["gpu_validation_artifact"])


def raw_payload_for(group):
    device, _, items = admission.GROUPS[group]
    measured = {key: metric_for(key) for key in items}
    commits = {metric["provenance"]["commit"] for metric in measured.values()}
    assert len(commits) == 1
    source_hashes = {}
    for metric in measured.values():
        for path, digest in metric["provenance"]["executed_source_sha256"].items():
            assert path not in source_hashes or source_hashes[path] == digest
            source_hashes[path] = digest
    first = next(iter(measured.values()))
    return {"schema_version": 2, "device": device, "accelerator": first["provenance"]["accelerator"],
        "code_commit": next(iter(commits)), "executed_source_uncommitted": False,
        "executed_source_sha256": source_hashes, "seeds": [42, 43, 44],
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "evaluation_protocol": {"tier": "l1_mechanism", "seeds": [42, 43, 44], "formal_comparison": False},
        "components": {key: {"dataset": metric["dataset"], "per_seed": metric["per_seed"],
            "metrics": metric["metrics"], "diagnostic_only": True, "promotion_eligible": False,
            "evolve_integrated": False, "full_experiment_status": "not_reproduced_high_cost"}
            for key, metric in measured.items()}}


@pytest.fixture
def portable_raw_admission(monkeypatch):
    # Raw admission normally checks git-show when the operator freezes sources.
    # Persistent CI must use the committed Merkle proof even after squash+delete.
    original = admission.source_hashes

    def portable(commit, hashes, expected, *, require_git=True):
        original(commit, hashes, expected, require_git=False)

    monkeypatch.setattr(admission, "source_hashes", portable)


def test_fixed_nine_paper_scope_and_high_cost_references_have_no_fake_adapter():
    rows = records()
    assert set(rows) == set(admission.COSTS) == EXPECTED_SCOPE
    assert set(admission.REFERENCES) == EXPECTED_REFERENCES
    assert {key for _, _, items in admission.GROUPS.values() for key in items} == EXPECTED_COMPONENTS
    for key, row in rows.items():
        admission.validate_catalog_identity(row)
        assert row["adapter"] is None and row["diagnostic_only"] is True
        assert row["promotion_eligible"] is False and row["evolve_integrated"] is False
        assert row["full_experiment_status"] == "not_reproduced_high_cost" and row["review_done"] is True
        assert row["first_author_affiliation"] and row["published_at"]
        assert row["published"] == ("2026-08-26" if key == "skill-state" else "2026-10-14" if key == "alpha-diana" else "2026-10-15")
        text = (ROOT / "docs" / row["detail_path"]).read_text()
        for token in ("## 论文信息", "### 核心公式", "不复现", "DONE", "assets/paper-figure-01.png"):
            assert token in text, (key, token)
        if key in EXPECTED_REFERENCES:
            assert row["implementation_status"] == "deferred_high_cost"
            assert not row.get("local_operator") and not row.get("local_command")
            assert not row.get("requires_gpu_validation") and not row.get("gpu_validation_artifact")
        else:
            assert row["implementation_status"] in {"component_only", "evaluation_protocol_interface"}
            module, member = row["local_operator"].rsplit(".", 1)
            assert callable(getattr(importlib.import_module(module), member))


@pytest.mark.parametrize("key", ["fpot", "lamp", "gen4p"])
def test_foundation_papers_reachable_by_institution_topic_and_year(key):
    row = records()[key]
    for dimension in ("organization", "topic", "year"):
        page = ROOT / f"docs/foundation-models/catalog/by-{dimension}.md"
        assert Path(row["detail_path"]).parent.name in page.read_text(), (key, dimension)


@pytest.mark.parametrize("key", sorted(EXPECTED_COMPONENTS))
def test_real_committed_component_artifacts_and_receipts_are_revalidated(key):
    metric = metric_for(key)
    device = admission.validate_curated(metric, key)
    assert admission.CHECKS[key]
    row = records()[key]
    if device == "cuda":
        assert row["requires_gpu_validation"] is True
        receipt = receipt_for(key)
        admission.validate_receipt_binding(receipt, metric, key)
        assert any(model in receipt["accelerator"]["model"] for model in ("A100", "A30"))
    else:
        assert not row.get("requires_gpu_validation") and not row.get("gpu_validation_artifact")


def test_persistent_evidence_checks_do_not_need_git_history_or_network(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("committed evidence verification must not fetch or git-show an ancestor")

    monkeypatch.setattr(admission.subprocess, "check_output", forbidden)
    for key in sorted(EXPECTED_COMPONENTS):
        admission.validate_curated(metric_for(key), key)


@pytest.mark.parametrize("group", sorted(admission.GROUPS))
def test_raw_group_validation_can_use_portable_frozen_evidence(group, portable_raw_admission):
    admission.validate_payload(raw_payload_for(group), group)


@pytest.mark.parametrize("mutation", ["diagnostic", "promotion", "evolve", "dirty", "missing_seed",
    "reordered_seeds", "failed_seed", "nested_failure", "aggregate", "source_hash", "source_scope",
    "wrong_commit", "component_identity", "dataset", "fixture_promoted", "full_claim", "outcome"])
def test_raw_payload_mutations_fail_closed(mutation, portable_raw_admission):
    payload = deepcopy(raw_payload_for("agent"))
    component = payload["components"]["alpha-diana"]
    if mutation == "diagnostic":
        payload["diagnostic_only"] = False
    elif mutation == "promotion":
        component["promotion_eligible"] = True
    elif mutation == "evolve":
        component["evolve_integrated"] = True
    elif mutation == "dirty":
        payload["executed_source_uncommitted"] = True
    elif mutation == "missing_seed":
        component["per_seed"].pop()
    elif mutation == "reordered_seeds":
        payload["seeds"] = [43, 42, 44]
    elif mutation == "failed_seed":
        component["per_seed"][0]["status"] = "failed"
    elif mutation == "nested_failure":
        component["result"] = {"status": "partial"}
    elif mutation == "aggregate":
        component["metrics"][next(iter(component["metrics"]))] = {"mean": 9999, "std": 0, "n": 3}
    elif mutation == "source_hash":
        payload["executed_source_sha256"][next(iter(payload["executed_source_sha256"]))] = "0"*64
    elif mutation == "source_scope":
        payload["executed_source_sha256"].pop(next(iter(payload["executed_source_sha256"])))
    elif mutation == "wrong_commit":
        payload["code_commit"] = "0"*40
    elif mutation == "component_identity":
        payload["components"]["foreign-method"] = payload["components"].pop("alpha-diana")
    elif mutation == "dataset":
        component["dataset"]["id"] = "different-public-benchmark"
    elif mutation == "fixture_promoted":
        component["dataset"]["public_benchmark_evaluated"] = True
    elif mutation == "full_claim":
        component["full_experiment_status"] = "full_reproduction_passed"
    else:
        component["per_seed"][0]["metrics"]["gold_fields_exposed_to_actor"] = 1
        component["metrics"] = admission.aggregate(component["per_seed"])
    with pytest.raises(ValueError):
        admission.validate_payload(payload, "agent")


@pytest.mark.parametrize("mutation", ["diagnostic", "promotion", "evolve", "missing_seed", "seed_failure",
    "aggregate", "identity", "manifest_ref", "source_hash", "source_scope", "wrong_commit",
    "artifact_path", "input_fingerprint", "missing_dataset", "changed_dataset", "full_claim",
    "unfinished_review", "tier", "protocol_seeds", "formal_comparison", "outcome"])
def test_curated_mutations_are_not_trusted_pass_certificates(mutation):
    metric = deepcopy(metric_for("alpha-diana"))
    if mutation in {"diagnostic", "promotion", "evolve"}:
        metric[{"diagnostic": "diagnostic_only", "promotion": "promotion_eligible", "evolve": "evolve_integrated"}[mutation]] = mutation != "diagnostic"
    elif mutation == "missing_seed":
        metric["per_seed"].pop()
    elif mutation == "seed_failure":
        metric["per_seed"][0]["result"] = {"status": "timeout"}
    elif mutation == "aggregate":
        metric["metrics"][next(iter(metric["metrics"]))] = {"mean": 9999, "std": 0, "n": 3}
    elif mutation == "identity":
        metric["method"] = "agent-perturb"
    elif mutation == "manifest_ref":
        metric["manifest_ref"] = "foundation-models:alpha-diana"
    elif mutation == "source_hash":
        metric["provenance"]["executed_source_sha256"][next(iter(metric["provenance"]["executed_source_sha256"]))] = "0"*64
    elif mutation == "source_scope":
        metric["provenance"]["executed_source_sha256"].pop(next(iter(metric["provenance"]["executed_source_sha256"])))
    elif mutation == "wrong_commit":
        metric["provenance"]["commit"] = "0"*40
    elif mutation == "artifact_path":
        metric["provenance"]["artifact_path"] = "docs/other/metrics.json"
    elif mutation == "input_fingerprint":
        metric["provenance"]["dataset_fingerprint"] = "sha256:"+"0"*64
    elif mutation == "missing_dataset":
        metric["dataset"] = {}
    elif mutation == "changed_dataset":
        metric["dataset"]["id"] = "different-public-benchmark"
        metric["provenance"]["dataset_fingerprint"] = admission.generated_input_fingerprint(
            metric["dataset"], metric["provenance"]["executed_source_sha256"])
    elif mutation == "full_claim":
        metric["full_experiment_status"] = "reproduced_full_pipeline"
    elif mutation == "unfinished_review":
        metric["full_experiment_review_done"] = False
    elif mutation == "tier":
        metric["evaluation_tier"] = metric["evaluation_protocol"]["tier"] = "l3_formal"
    elif mutation == "protocol_seeds":
        metric["evaluation_protocol"]["seeds"] = [42]
    elif mutation == "formal_comparison":
        metric["evaluation_protocol"]["formal_comparison"] = True
    else:
        metric["per_seed"][0]["metrics"]["gold_fields_exposed_to_actor"] = 1
        metric["metrics"] = admission.aggregate(metric["per_seed"])
    with pytest.raises(ValueError):
        admission.validate_curated(metric, "alpha-diana")


@pytest.mark.parametrize("field,value", [("paper_url", "https://arxiv.org/abs/9999.99999"),
    ("domain", "agent-research"), ("detail_path", "different/README.md")])
def test_catalog_identity_is_fixed_not_registry_self_report(field, value):
    row = deepcopy(records()["fpot"])
    row[field] = value
    with pytest.raises(ValueError, match="identity"):
        admission.validate_catalog_identity(row)


@pytest.mark.parametrize("mutation", ["key", "metrics", "dataset", "sources", "commit", "metric_path",
    "receipt_path", "seeds", "accelerator", "diagnostic", "promotion", "evolve", "full_claim",
    "checkpoint_commit", "command_commit", "command_device", "command_runner", "command_seeds"])
def test_receipt_is_bound_to_exact_metric_execution_and_claim_scope(mutation):
    metric, receipt = metric_for("fpot"), deepcopy(receipt_for("fpot"))
    if mutation == "key":
        receipt["adapter_key"] = "lamp"
    elif mutation == "metrics":
        receipt["metrics"] = {}
    elif mutation == "dataset":
        receipt["dataset"] = {"id": "different", "revision": "changed"}
    elif mutation == "sources":
        receipt["executed_source_sha256"] = {}
    elif mutation == "commit":
        receipt["provenance"]["commit"] = "0"*40
    elif mutation == "metric_path":
        receipt["provenance"]["metric_artifact_path"] = "docs/different.json"
    elif mutation == "receipt_path":
        receipt["provenance"]["artifact_path"] = "docs/gpu-validations/different.json"
    elif mutation == "seeds":
        receipt["seeds"] = [42]
    elif mutation == "accelerator":
        receipt["accelerator"]["model"] = "NVIDIA B200"
    elif mutation in {"diagnostic", "promotion", "evolve"}:
        receipt[{"diagnostic": "diagnostic_only", "promotion": "promotion_eligible", "evolve": "evolve_integrated"}[mutation]] = mutation != "diagnostic"
    elif mutation == "full_claim":
        receipt["full_experiment_status"] = "full_reproduction_passed"
    elif mutation == "checkpoint_commit":
        receipt["checkpoint"]["revision"] = "0"*40
    else:
        argv = receipt["command"]
        if mutation == "command_runner":
            argv[1] = "scripts/different.py"
        else:
            flag = {"command_commit": "--code-commit", "command_device": "--device", "command_seeds": "--seeds"}[mutation]
            argv[argv.index(flag)+1] = {"command_commit": "0"*40, "command_device": "cpu", "command_seeds": "42"}[mutation]
    with pytest.raises(ValueError):
        admission.validate_receipt_binding(receipt, metric, "fpot")


@pytest.mark.parametrize("key", sorted(EXPECTED_REFERENCES))
@pytest.mark.parametrize("field,value", [("local_operator", "fake.run"), ("local_command", "python fake.py"),
    ("gpu_validation_artifact", "docs/gpu-validations/fake.json"), ("adapter", "fake-adapter"),
    ("requires_gpu_validation", True)])
def test_high_cost_reference_cannot_be_finalized_as_executable(key, field, value, monkeypatch):
    rows = deepcopy(records())
    # Validate the unmodified baseline first; another missing artifact must not
    # make the mutation test pass for an unrelated failure.
    for name in EXPECTED_COMPONENTS:
        admission.validate_curated(metric_for(name), name)
    for row in rows.values():
        assert row["review_done"] is True
    rows[key][field] = value
    monkeypatch.setattr(admission, "catalog_records", lambda: tuple(rows.values()))
    monkeypatch.setattr(admission, "write_json", lambda *args: None)
    with pytest.raises(ValueError, match="reference|adapter|GPU|execution"):
        admission.finalize()


@pytest.mark.parametrize("key,field,value", [("fpot", "requires_gpu_validation", False),
    ("alpha-diana", "diagnostic_only", False), ("fpot", "adapter", "unearned-adapter")])
def test_catalog_cannot_drop_gpu_gate_or_diagnostic_boundary(key, field, value, monkeypatch):
    rows = deepcopy(records())
    for name in EXPECTED_COMPONENTS:
        admission.validate_curated(metric_for(name), name)
    assert all(row["review_done"] is True for row in rows.values())
    rows[key][field] = value
    monkeypatch.setattr(admission, "catalog_records", lambda: tuple(rows.values()))
    monkeypatch.setattr(admission, "write_json", lambda *args: None)
    with pytest.raises(ValueError, match="boundary|adapter|GPU|gpu|CUDA|cuda"):
        admission.finalize()


def test_shared_frozen_commit_proof_union_preserves_both_group_scopes(tmp_path, monkeypatch):
    commit = "1"*40
    proof_path = tmp_path / "proof.json"
    captured_scopes = []
    monkeypatch.setattr(admission, "ROOT", tmp_path)
    monkeypatch.setattr(admission, "SOURCE_PROOFS", proof_path)
    monkeypatch.setattr(admission, "validate_payload", lambda payload, group: admission.GROUPS[group])

    def capture(root, frozen, hashes):
        assert root == tmp_path and frozen == commit
        captured_scopes.append(set(hashes))
        return {"mock_only": True, "paths": sorted(hashes), "objects": {}}

    monkeypatch.setattr(admission, "capture_sources", capture)
    expected_union = set()
    expected_captures = []
    for group in ("agent", "skill"):
        _, runner, items = admission.GROUPS[group]
        paths = {runner, *(f"src/auto_research/{module}.py" for _, _, module in items.values())}
        expected_union |= paths
        expected_captures.append(paths)
        payload = {"code_commit": commit, "executed_source_sha256": {path: "2"*64 for path in paths},
            "components": {key: {"dataset": {"id": "mock-plumbing-only", "revision": "not-execution-evidence"},
                "per_seed": [{"seed": seed, "metrics": {"mock_value": seed}} for seed in (42, 43, 44)]}
                for key in items}}
        path = tmp_path / f"{group}.json"
        path.write_text(json.dumps(payload))
        admission.curate(path, group)
    bundle = json.loads(proof_path.read_text())
    assert set(bundle["commits"]) == {commit}
    assert set(bundle["commits"][commit]["executed_source_sha256"]) == expected_union
    assert set(bundle["commits"][commit]["proof"]["paths"]) == expected_union
    assert bundle["commits"][commit]["proof"]["objects"] == {}
    assert captured_scopes == expected_captures
    assert captured_scopes[0].isdisjoint(captured_scopes[1])
    assert captured_scopes[0] | captured_scopes[1] == expected_union


def test_curating_current_scope_preserves_archived_proof_when_other_scope_sources_changed(tmp_path, monkeypatch):
    commit = "1"*40
    proof_path = tmp_path / "proof.json"
    _, old_runner, old_items = admission.GROUPS["agent"]
    old_paths = {old_runner, *(f"src/auto_research/{module}.py" for _, _, module in old_items.values())}
    old_hash = hashlib.sha256(b"archived measured source").hexdigest()
    old_hashes = {path: old_hash for path in old_paths}
    old_oid, fresh_oid = "a"*40, "b"*40
    old_object = {"mock_only": "archived Git tree bytes must remain unchanged"}
    fresh_object = {"mock_only": "current measured Git tree bytes"}
    proof_path.write_text(json.dumps({"schema_version": 1, "commits": {commit: {
        "executed_source_sha256": old_hashes,
        "proof": {"mock_only": True, "paths": sorted(old_paths), "objects": {old_oid: old_object}},
    }}}))
    # Another group now has newer working-tree bytes, while its old proof still
    # belongs to the original frozen commit. Re-capturing that group is invalid.
    for name in old_paths:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("newer unmeasured source version")
        assert hashlib.sha256(path.read_bytes()).hexdigest() != old_hashes[name]
    monkeypatch.setattr(admission, "ROOT", tmp_path)
    monkeypatch.setattr(admission, "SOURCE_PROOFS", proof_path)
    monkeypatch.setattr(admission, "validate_payload", lambda payload, group: admission.GROUPS[group])
    _, runner, items = admission.GROUPS["skill"]
    measured_paths = {runner, *(f"src/auto_research/{module}.py" for _, _, module in items.values())}
    captured = []

    def capture(root, frozen, hashes):
        assert root == tmp_path and frozen == commit
        assert set(hashes) == measured_paths
        assert not set(hashes) & old_paths, "must not recapture stale files from another group"
        captured.append(set(hashes))
        return {"mock_only": True, "paths": sorted(hashes), "objects": {fresh_oid: fresh_object}}

    monkeypatch.setattr(admission, "capture_sources", capture)
    measured_hashes = {name: "2"*64 for name in measured_paths}
    payload = {"code_commit": commit, "executed_source_sha256": measured_hashes,
        "components": {key: {"dataset": {"id": "mock-plumbing-only", "revision": "not-execution-evidence"},
            "per_seed": [{"seed": seed, "metrics": {"mock_value": seed}} for seed in (42, 43, 44)]}
            for key in items}}
    source = tmp_path / "current-skill-scope.json"
    source.write_text(json.dumps(payload))
    admission.curate(source, "skill")
    archived = json.loads(proof_path.read_text())["commits"][commit]
    assert captured == [measured_paths]
    assert archived["executed_source_sha256"] == {**old_hashes, **measured_hashes}
    assert set(archived["proof"]["paths"]) == old_paths | measured_paths
    assert archived["proof"]["objects"] == {old_oid: old_object, fresh_oid: fresh_object}


def test_ledger_selected_scope_does_not_promote_or_advance_review_watermark():
    ledger = json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())
    batch = next(row for row in ledger["batches"] if row["batch"] == admission.BATCH)
    assert batch["review_watermark_advanced"] is False and batch["coverage_complete"] is False
    assert {row["key"] for row in batch["candidates"]} == EXPECTED_SCOPE
    assert batch["component_validation_counts"] == {"gpu_validated_components": 3,
        "cpu_validated_components_or_interfaces": 4, "review_only": 2}
    for row in batch["candidates"]:
        assert row["review_done"] is True and row["terminal"] is True
        assert row["automatic_retry"] is False and row["automatic_implementation_queue"] is False
        assert row["status_scope"] == "full_paper_reproduction"


def test_source_receipts_distinguish_oct16_overlap_from_august_google_backfill():
    report = json.loads((ROOT / "docs/research-audits/oct19-components/source-coverage.json").read_text())
    assert report["all_sources_exhaustive"] is False
    assert report["review_watermark"]["before"] == report["review_watermark"]["after"] == "2026-10-15"
    assert report["review_watermark"]["advanced"] is False and report["review_watermark"]["reason"]
    assert len(report["arxiv_sources"]) == 6
    assert all(receipt["announced_on"] == "2026-10-16" and receipt["parse_complete"]
        and receipt["expected_entries"] == receipt["parsed_entries"]
        for source in report["arxiv_sources"] for receipt in source["page_receipts"])
    assert {row["key"] for row in report["selected_papers"]} == EXPECTED_SCOPE
    assert report["counts"]["google_historical_backfill"] == 1
    assert report["counts"]["oct16_announcement_overlap"] == 8
