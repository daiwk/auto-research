from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("oct16_component_records", ROOT / "scripts/finalize_oct16_component_records.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_selected_batch_is_idempotent_and_does_not_change_prior_reviews():
    original = json.loads((ROOT / MODULE.LEDGER).read_text())
    figures, ledger = MODULE.build_records(ROOT)
    prior = [b for b in original["batches"] if b["batch"] != MODULE.BATCH]
    assert [b for b in ledger["batches"] if b["batch"] != MODULE.BATCH] == prior
    batch = next(b for b in ledger["batches"] if b["batch"] == MODULE.BATCH)
    assert len(batch["candidates"]) == 15
    assert batch["accepted_scope_counts"] == {"historical_p0": 2, "p1": 12, "existing_method_supplement": 1}
    assert not batch["coverage_complete"] and not batch["review_watermark_advanced"]
    assert not batch["review_snapshot_modified"]
    assert all(c["status"] == "deferred" and c["status_scope"] == "full_paper_reproduction"
               and c["resolution"] == "not_reproduced_high_cost" and c["review_done"]
               and not c["automatic_retry"] and not c["automatic_implementation_queue"]
               and c["implementation_status"] in {"component_only", "evaluation_protocol_interface"}
               and not c["promotion_eligible"] and not c["evolve_integrated"] for c in batch["candidates"])
    assert sum(c["component_validation"]["requires_gpu_validation"] for c in batch["candidates"]) == 11
    assert len(figures) == len({f["page"] for f in figures})
    again_figures, again_ledger = MODULE.build_records(ROOT)
    assert again_figures == figures and again_ledger == ledger


def test_transx_original_figure_is_preserved_with_unique_report_supplement():
    figures, _ = MODULE.build_records(ROOT)
    transx = next(f for f in figures if f["page"] == "docs/reproductions/2607.28940-transx/README.md")
    assert transx["arxiv_id"] == "2607.28940"
    assert transx["asset"].endswith("assets/paper-figure-01.png")
    reports = [f for f in transx["supplementary_figures"] if f["arxiv_id"] == "2610.20913"]
    assert len(reports) == 1 and reports[0]["asset"].endswith("assets/report-page.png")


def test_figure_merge_retains_existing_primary_and_is_repeatable():
    original = [{"page": "docs/one.md", "asset": "old.png", "arxiv_id": "old"}]
    before = deepcopy(original)
    additions = [("docs/one.md", {"asset": "new.png", "arxiv_id": "new"}),
                 ("docs/two.md", {"asset": "second.png", "arxiv_id": "second"})]
    merged = MODULE.merge_figures(original, additions)
    assert original == before
    assert merged[0]["asset"] == "old.png"
    assert len(merged[0]["supplementary_figures"]) == 1
    assert MODULE.merge_figures(merged, additions) == merged
    with pytest.raises(ValueError, match="duplicate pages"):
        MODULE.merge_figures(original + original, [])


def test_gpu_acceptance_calls_validator_and_rejects_stale_source(monkeypatch, tmp_path):
    # Unit-only mocked receipt: not a production GPU artifact or execution claim.
    selected = MODULE.Selected("unit", "0000.00000", "agent", "Figure 1", "https://example.test",
                               "unit-only", "unit-only", "src/algorithm.py", "scripts/runner.py")
    catalog = {"component_key": "unit-component", "gpu_validation_artifact": "receipt.json"}
    for relative in (selected.source_file, selected.runner):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("unit-only source")
    (tmp_path / "receipt.json").write_text("unit-only placeholder, never committed as GPU evidence")
    hashes = {relative: hashlib.sha256((tmp_path / relative).read_bytes()).hexdigest()
              for relative in (selected.source_file, selected.runner)}
    calls = []
    def mocked_loader(path):
        calls.append(path)
        return {"adapter_key": "unit-component", "accelerator": {"model": "NVIDIA A100"},
                "provenance": {"artifact_path": "receipt.json", "commit": "unit-only"},
                "executed_source_sha256": hashes}
    monkeypatch.setattr(MODULE, "load_gpu_receipt", mocked_loader)
    result = MODULE.validate_component_gpu(tmp_path, catalog, selected)
    assert calls == [tmp_path / "receipt.json"]
    assert result["adapter_key"] == "unit-component" and result["source_hashes_verified"] == 2
    (tmp_path / selected.source_file).write_text("changed since the mocked execution")
    with pytest.raises(ValueError, match="source hash differs"):
        MODULE.validate_component_gpu(tmp_path, catalog, selected)
    hashes.clear()
    with pytest.raises(ValueError, match="executed_source_sha256"):
        MODULE.validate_component_gpu(tmp_path, catalog, selected)


def test_gpu_acceptance_never_treats_missing_file_as_passed(tmp_path):
    selected = MODULE.SELECTED[0]
    with pytest.raises(ValueError, match="missing"):
        MODULE.validate_component_gpu(tmp_path, {"gpu_validation_artifact": "missing.json"}, selected)


@pytest.fixture
def novelty_cpu_fixture(tmp_path):
    # This copies an already-measured CPU diagnostic for acceptance unit tests;
    # no mocked or fabricated artifact is installed as production evidence.
    selected = next(item for item in MODULE.SELECTED if item.key == "novelty-patching")
    relative = "docs/foundation-models/2610.22100-novelty-patching/metrics/component-cpu.json"
    metric = tmp_path / relative
    metric.parent.mkdir(parents=True)
    metric.write_bytes((ROOT / relative).read_bytes())
    for name in (selected.source_file, selected.runner):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes())
    catalog = {"requires_gpu_validation": False, "diagnostic_only": True,
               "promotion_eligible": False, "evolve_integrated": False}
    return tmp_path, catalog, selected, metric


def test_cpu_acceptance_binds_real_measured_scope_and_source(novelty_cpu_fixture):
    root, catalog, selected, path = novelty_cpu_fixture
    accepted = MODULE.validate_component_cpu(root, catalog, selected, [path])
    assert accepted["manifest_ref"] == "foundation-models:novelty-patching"
    assert accepted["capability_claim_verified"] is False
    assert "not_a_raw_cache_rerun" in accepted["verification"]
    assert accepted["input_fingerprints"]["training_fingerprint"]
    (root / selected.runner).write_text("unit-only stale runner")
    with pytest.raises(ValueError, match="source binding"):
        MODULE.validate_component_cpu(root, catalog, selected, [path])


@pytest.mark.parametrize("mutation", [
    lambda p: p.update(schema_version=1),
    lambda p: p.update(manifest_ref="foundation-models:wrong"),
    lambda p: p.update(method="wrong"),
    lambda p: p.update(diagnostic_only=False),
    lambda p: p.update(promotion_eligible=True),
    lambda p: p.update(evolve_integrated=True),
    lambda p: p["evaluation_protocol"].update(formal_comparison=True),
    lambda p: p["evaluation_protocol"].pop("claim_policy"),
    lambda p: p["provenance"].update(runner_sha256="0" * 64),
    lambda p: p["dataset"].update(revision="wrong"),
    lambda p: p["dataset"].update(source_sha256="0" * 64),
    lambda p: p["dataset"].update(documents=493),
    lambda p: p["dataset"].update(test_read=True),
    lambda p: p.update(deterministic=False),
    lambda p: p.update(seeds=[42]),
    lambda p: p.update(metrics={}),
    lambda p: p["metrics"].update(threshold=float("nan")),
])
def test_cpu_acceptance_rejects_schema_claim_scope_and_nonfinite_mutations(novelty_cpu_fixture, mutation):
    root, catalog, selected, path = novelty_cpu_fixture
    payload = json.loads(path.read_text())
    mutation(payload)
    path.write_text(json.dumps(payload))
    with pytest.raises(ValueError):
        MODULE.validate_component_cpu(root, catalog, selected, [path])


def test_cpu_acceptance_recomputes_all_three_official_inputs():
    catalogs = ROOT / "src/auto_research/paper_specs/catalog/agent-research"
    for selected in (item for item in MODULE.SELECTED if item.track == "agent"):
        catalog = json.loads((catalogs / f"{selected.key}.json").read_text())
        paths = list((ROOT / "docs" / catalog["detail_path"]).parent.glob("metrics/*.json"))
        result = MODULE.validate_component_cpu(ROOT, catalog, selected, paths)
        assert result["input_fingerprints"]
        assert result["verification"] == "committed_official_input_hashes_and_actual_cpu_recomputation_no_new_model"
        assert result["capability_claim_verified"] is False


def test_cpu_acceptance_rejects_changed_official_counts_and_input(tmp_path):
    selected = next(item for item in MODULE.SELECTED if item.key == "scipivot")
    catalog = json.loads((ROOT / "src/auto_research/paper_specs/catalog/agent-research/scipivot.json").read_text())
    directory = Path("docs") / Path(catalog["detail_path"]).parent
    for name in (selected.source_file, selected.runner,
                 str(directory / "metrics/official-options-audit-cpu.json"),
                 str(directory / "validation/upstream/questions.json"),
                 str(directory / "validation/upstream/all_model_scores.csv")):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((ROOT / name).read_bytes())
    path = tmp_path / directory / "metrics/official-options-audit-cpu.json"
    original = json.loads(path.read_text())
    changed = deepcopy(original)
    changed["aggregate_rows_validated"] = 59
    path.write_text(json.dumps(changed))
    with pytest.raises(ValueError, match="record counts/recomputation"):
        MODULE.validate_component_cpu(tmp_path, catalog, selected, [path])
    path.write_text(json.dumps(original))
    (tmp_path / directory / "validation/upstream/all_model_scores.csv").write_text("unit-only changed input")
    with pytest.raises(ValueError, match="official CPU input missing/changed"):
        MODULE.validate_component_cpu(tmp_path, catalog, selected, [path])


def test_cpu_acceptance_requires_explicit_flag_before_first_acceptance(monkeypatch):
    original_loads = MODULE.json.loads
    def loads_without_prior_cpu_acceptance(text):
        payload = original_loads(text)
        if isinstance(payload, dict) and "batches" in payload:
            for batch in payload["batches"]:
                if batch.get("batch") == MODULE.BATCH:
                    for row in batch["candidates"]:
                        row["component_validation"]["cpu_evidence_validated"] = False
        return payload
    monkeypatch.setattr(MODULE.json, "loads", loads_without_prior_cpu_acceptance)
    calls = []
    def unit_validator(root, catalog, selected, metrics):
        calls.append(selected.key)
        return {"unit_only": True, "capability_claim_verified": False}
    monkeypatch.setattr(MODULE, "validate_component_cpu", unit_validator)
    _, ledger = MODULE.build_records(ROOT)
    batch = next(batch for batch in ledger["batches"] if batch["batch"] == MODULE.BATCH)
    assert not calls and batch["component_validation_counts"]["cpu_metrics_sources_and_inputs_validated"] == 0
    _, ledger = MODULE.build_records(ROOT, accept_cpu_evidence=True)
    batch = next(batch for batch in ledger["batches"] if batch["batch"] == MODULE.BATCH)
    assert set(calls) == {"novelty-patching", "tool-bottleneck-bench", "librarian-agents", "scipivot"}
    assert batch["component_validation_counts"]["cpu_metrics_sources_and_inputs_validated"] == 4


def test_cpu_acceptance_is_explicit_and_previously_accepted_is_revalidated(monkeypatch):
    # Avoid writing shared ledger files: the copied input batch is local to
    # this unit test, and the acceptance call itself is separately exercised.
    original_loads = MODULE.json.loads
    def loads_with_prior_acceptance(text):
        payload = original_loads(text)
        if isinstance(payload, dict) and "batches" in payload:
            for batch in payload["batches"]:
                if batch.get("batch") == MODULE.BATCH:
                    for row in batch["candidates"]:
                        if row["key"] == "novelty-patching":
                            row["component_validation"]["cpu_evidence_validated"] = True
        return payload
    monkeypatch.setattr(MODULE.json, "loads", loads_with_prior_acceptance)
    calls = []
    def reject_stale(root, catalog, selected, metrics):
        calls.append(selected.key)
        raise ValueError("unit-only prior accepted CPU source has changed")
    monkeypatch.setattr(MODULE, "validate_component_cpu", reject_stale)
    with pytest.raises(ValueError, match="prior accepted CPU source"):
        MODULE.build_records(ROOT)
    assert calls == ["novelty-patching"]
