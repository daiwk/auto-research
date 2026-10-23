from copy import deepcopy
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/"docs/research-audits/oct22-bulletin-components"


def module():
    return runpy.run_path(str(ROOT/"scripts/build_oct22_bulletin_artifacts.py"))


def result(key="cord"):
    return json.loads((ROOT/module()["metric_path"](key)).read_text())


def test_real_frozen_cuda_and_cpu_contract_evidence():
    module()["check"]()
    scope = json.loads((AUDIT/"task-scope.json").read_text())
    assert scope["selected_scope_complete"] and scope["gpu_validated_component_count"] == 4
    for row in scope["papers"]:
        assert row["review_done"] and row["full_experiment_status"] == "not_reproduced_high_cost"
        assert not row["promotion_eligible"] and not row["evolve_integrated"]
    assert all(r["component_accepted"] for r in scope["papers"] if r["key"] in module()["MODULES"])
    coverage = json.loads((AUDIT/"source-coverage.json").read_text())
    assert coverage["counts"]["components_pending_gpu_and_integration"] == 0
    assert coverage["delivery_status"] == "bounded_scope_complete"
    assert not coverage["review_watermark_advanced"] and not coverage["all_sources_exhaustive"]


@pytest.mark.parametrize("key", ["alps", "asteroid", "cord", "csd", "jev-multicorrect"])
def test_all_defining_checks_are_locked(key):
    row = result(key)
    row["per_seed"][0]["checks"] = {"unrelated_true": True}
    with pytest.raises(ValueError, match="defining contract"):
        module()["validate_result"](key, row)


@pytest.mark.parametrize("field,value", [("evaluation_tier", "l3_pipeline"), ("formal_comparison", True),
    ("promotion_eligible", True), ("evolve_integrated", True), ("diagnostic_only", False),
    ("pretrained_model_calls", 1), ("fixture_demo", False), ("full_experiment_status", "reproduced")])
def test_no_diagnostic_can_be_relabelled_as_capability(field, value):
    row = result()
    row[field] = value
    with pytest.raises(ValueError, match="L1 claim"):
        module()["validate_result"]("cord", row)


@pytest.mark.parametrize("key", ["alps", "asteroid", "cord", "csd", "jev-multicorrect"])
@pytest.mark.parametrize("field,value", [
    ("adapter", {"spec_key": "unearned-adapter"}),
    ("implementation_status", "full_pipeline"), ("evaluation_tier", "l3_pipeline"),
    ("diagnostic_only", False), ("promotion_eligible", True), ("evolve_integrated", True),
    ("full_experiment_status", "reproduced"), ("full_experiment_review_done", False),
    ("review_done", False), ("automatic_retry", True), ("automatic_implementation_queue", True),
])
def test_component_catalog_cannot_upgrade_or_retry_l1_evidence(monkeypatch, key, field, value):
    m = module()
    catalog = deepcopy(m["records"]())
    catalog[key][field] = value
    monkeypatch.setitem(m["check"].__globals__, "records", lambda: catalog)
    with pytest.raises(ValueError, match="component catalog contract"):
        m["check"]()


@pytest.mark.parametrize("key", ["alps", "asteroid", "cord", "csd", "jev-multicorrect"])
def test_component_catalog_requires_exact_gpu_contract(monkeypatch, key):
    m = module()
    catalog = deepcopy(m["records"]())
    catalog[key]["requires_gpu_validation"] = key not in m["CUDA_KEYS"]
    monkeypatch.setitem(m["check"].__globals__, "records", lambda: catalog)
    with pytest.raises(ValueError, match="component catalog GPU contract"):
        m["check"]()


@pytest.mark.parametrize("key", ["alps", "asteroid", "cord", "csd", "jev-multicorrect"])
def test_component_catalog_cannot_redirect_gpu_receipt(monkeypatch, key):
    m = module()
    catalog = deepcopy(m["records"]())
    catalog[key]["gpu_validation_artifact"] = "docs/gpu-validations/unrelated.json"
    monkeypatch.setitem(m["check"].__globals__, "records", lambda: catalog)
    with pytest.raises(ValueError, match="component catalog GPU contract"):
        m["check"]()


@pytest.mark.parametrize("key", ["aw0", "right-on-q", "finesid"])
@pytest.mark.parametrize("field,value", [
    ("adapter", {"spec_key": "unearned-adapter"}), ("implementation_status", "component_only"),
    ("evaluation_tier", "l1_mechanism"), ("diagnostic_only", False),
    ("promotion_eligible", True), ("evolve_integrated", True),
    ("full_experiment_status", "reproduced"), ("review_done", False),
    ("automatic_retry", True), ("automatic_implementation_queue", True),
    ("requires_gpu_validation", True), ("gpu_validation_passed", True),
    ("gpu_validation_artifact", "docs/gpu-validations/unearned.json"),
    ("local_operator", "unearned.runtime"), ("local_command", "python unearned.py"),
])
def test_reference_catalog_remains_terminal_review_only(monkeypatch, key, field, value):
    m = module()
    catalog = deepcopy(m["records"]())
    catalog[key][field] = value
    monkeypatch.setitem(m["check"].__globals__, "records", lambda: catalog)
    with pytest.raises(ValueError, match="high-cost terminal catalog contract"):
        m["check"]()


@pytest.mark.parametrize("key", ["alps", "asteroid", "cord", "csd", "jev-multicorrect", "aw0", "right-on-q", "finesid"])
@pytest.mark.parametrize("field", ["diagnostic_only", "promotion_eligible", "evolve_integrated",
    "automatic_retry", "automatic_implementation_queue", "requires_gpu_validation"])
def test_catalog_safety_flags_must_be_explicit(monkeypatch, key, field):
    m = module()
    catalog = deepcopy(m["records"]())
    catalog[key].pop(field, None)
    monkeypatch.setitem(m["check"].__globals__, "records", lambda: catalog)
    with pytest.raises(ValueError, match="catalog.*contract"):
        m["check"]()


@pytest.mark.parametrize("field", ["id", "revision", "recipe", "capability_benchmark"])
def test_rehash_does_not_allow_false_dataset_identity(field):
    m, row = module(), result()
    row["dataset"][field] = True if field == "capability_benchmark" else "wrong"
    row["provenance"]["dataset_fingerprint"] = "sha256:"+m["digest"]({"dataset": row["dataset"],
        "source": row["provenance"]["executed_source_sha256"], "seeds": row["seeds"]})
    with pytest.raises(ValueError, match="dataset/artifact"):
        m["validate_result"]("cord", row)


def test_metric_identity_accelerator_and_independent_reference_locked():
    m = module()
    row = result()
    for field, value, match in (("method", "csd", "component identity"),
        ("manifest_ref", "wrong:cord", "component identity")):
        bad = deepcopy(row)
        bad[field] = value
        with pytest.raises(ValueError, match=match):
            m["validate_result"]("cord", bad)
    row["provenance"]["accelerator"] = "CPU"
    with pytest.raises(ValueError, match="accelerator"):
        m["validate_result"]("cord", row)
    row = result()
    row["per_seed"][0]["metrics"]["gradient_reference_error"] = .1
    row["metrics"] = m["aggregate"](row["per_seed"])
    with pytest.raises(ValueError, match="CORD reference"):
        m["validate_result"]("cord", row)


@pytest.mark.parametrize("field,value", [
    ("seeds", [999]), ("adapter_key", "other"),
    ("accelerator", {"vendor": "NVIDIA", "model": "V100", "count": 9}),
    ("checkpoint", {"public_id": "other", "revision": "wrong", "pretrained": True}),
    ("command", ["echo", "not-a-real-run"]), ("diagnostic_only", False),
    ("promotion_eligible", True), ("evolve_integrated", True),
    ("full_experiment_status", "reproduced"), ("full_experiment_review_done", False),
])
def test_receipt_relabeling_is_rejected(monkeypatch, field, value):
    m = module()
    globals_ = m["check"].__globals__
    original = globals_["load_gpu_receipt"]

    def changed(path):
        receipt = original(path)
        if receipt["adapter_key"] == "asteroid":
            receipt[field] = value
        return receipt

    monkeypatch.setitem(globals_, "load_gpu_receipt", changed)
    with pytest.raises(ValueError, match="exact GPU receipt/run identity"):
        m["check"]()


@pytest.mark.parametrize("field,value", [
    ("raw_runner_artifact_sha256", "0"*64),
    ("artifact_path", "docs/gpu-validations/another.json"),
    ("metric_artifact_path", "docs/unrelated/metrics.json"),
    ("accelerator", "CPU"),
    ("dataset_fingerprint", "sha256:"+"0"*64),
])
def test_receipt_provenance_is_exactly_bound(monkeypatch, field, value):
    m = module()
    globals_ = m["check"].__globals__
    original = globals_["load_gpu_receipt"]

    def changed(path):
        receipt = original(path)
        if receipt["adapter_key"] == "asteroid":
            receipt["provenance"][field] = value
        return receipt

    monkeypatch.setitem(globals_, "load_gpu_receipt", changed)
    with pytest.raises(ValueError, match="exact GPU receipt/run identity"):
        m["check"]()


def actual_raw():
    raw_bytes = {device: (AUDIT/f"raw-{device}.json").read_bytes() for device in ("cpu", "cuda")}
    return {device: json.loads(data) for device, data in raw_bytes.items()}, raw_bytes


def test_updated_aggregate_cannot_hide_changed_per_seed_evidence():
    m, row = module(), result("asteroid")
    row["per_seed"][0]["metrics"]["parameter_update_l2"] = 999.0
    row["metrics"] = m["aggregate"](row["per_seed"])
    m["validate_result"]("asteroid", row)  # Still plausible as a standalone diagnostic.
    raw, raw_bytes = actual_raw()
    with pytest.raises(ValueError, match="raw runner per-seed"):
        m["validate_raw_binding"]("asteroid", row, raw, raw_bytes)


def test_raw_bytes_are_retained_and_not_merely_an_unverifiable_hash():
    m, row = module(), result("asteroid")
    raw, raw_bytes = actual_raw()
    m["validate_raw_binding"]("asteroid", row, raw, raw_bytes)
    changed = {**raw_bytes, "cuda": raw_bytes["cuda"] + b" "}
    with pytest.raises(ValueError, match="raw runner SHA"):
        m["validate_raw_binding"]("asteroid", row, raw, changed)


@pytest.mark.parametrize("field,value", [("accelerator", "CPU"), ("code_commit", "0"*40)])
def test_result_identity_must_match_actual_raw(field, value):
    m, row = module(), result("asteroid")
    raw, raw_bytes = actual_raw()
    raw["cuda"][field] = value
    with pytest.raises(ValueError, match="raw runner source/accelerator"):
        m["validate_raw_binding"]("asteroid", row, raw, raw_bytes)


def test_paper_figures_and_first_author_aggregation_are_not_priority_org_aliases():
    catalog = module()["records"]()
    figures = json.loads((ROOT/"docs/paper-figures-manifest.json").read_text())
    for key in (*module()["MODULES"], "aw0", "right-on-q", "finesid"):
        record = catalog[key]
        rows = [r for r in figures if r["page"] == "docs/"+record["detail_path"]]
        assert len(rows) == 1 and rows[0]["visually_inspected"]
        assert (ROOT/rows[0]["asset"]).stat().st_size > 10000
        text = (ROOT/"docs"/record["detail_path"]).read_text()
        assert "## 论文信息" in text and "DONE" in text and "不复现" in text
    assert "Santa Cruz" in catalog["alps"]["first_author_affiliation"]
    assert catalog["asteroid"]["first_author_affiliation"] == "University of Washington"
    assert catalog["right-on-q"]["first_author_affiliation"] == "University of Michigan, Ann Arbor"
