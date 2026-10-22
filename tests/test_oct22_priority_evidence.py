from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/"docs/research-audits/oct22-priority-backfill"


def module():
    return runpy.run_path(str(ROOT/"scripts/build_oct22_priority_artifacts.py"))


def result(key="logact"):
    m = module()
    return json.loads((ROOT/m["metric_path"](m["records"]()[key])).read_text())


def test_bounded_delta_and_terminal_exceptions():
    coverage = json.loads((AUDIT/"source-coverage.json").read_text())
    assert coverage["counts"]["fresh_since_last_scan"] == coverage["counts"]["changed_version_identities"] == 0
    assert not coverage["review_watermark_advanced"] and not coverage["all_sources_exhaustive"]
    assert coverage["review_watermark"]["after"] == "2026-10-15"
    for row in coverage["official_directory_deltas"]:
        if row["organization"] in {"Google", "Meta"}:
            assert row["new_directory_urls"] is None and row["changed_records"] is None
    scope = json.loads((AUDIT/"task-scope.json").read_text())
    assert {p["key"] for p in scope["papers"]} == {"deepsea", "logact"}
    for row in scope["papers"] + scope["archived_exceptions"]:
        assert row["review_done"] and not row["automatic_retry"]
        assert row["full_experiment_status"] == "not_reproduced_high_cost"
    archived = scope["archived_exceptions"][0]
    assert archived["exact_first_publication_date"] is None and not archived["code_reused"]
    assert not archived["blocking"]


def test_frozen_cpu_contract_evidence():
    module()["check"]()
    schema = json.loads((AUDIT/"deepsea-official-schema.json").read_text())
    assert schema["test_rows"] == 3250 and schema["model_calls"] == 0
    assert schema["public_field_names"] == ["question"]
    assert not schema["benchmark_text_exported"] and not schema["used_for_training_or_selection"]


@pytest.mark.parametrize("field,value", [("diagnostic_only", False), ("promotion_eligible", True),
    ("evolve_integrated", True), ("evaluation_tier", "l3_pipeline"), ("formal_comparison", True),
    ("pretrained_model_calls", 1), ("full_experiment_status", "reproduced")])
def test_no_fixture_promotion(field, value):
    row = result()
    row[field] = value
    with pytest.raises(ValueError, match="claim boundary"):
        module()["validate_result"]("logact", row)


@pytest.mark.parametrize("field", ["id", "revision", "recipe", "capability_benchmark"])
def test_rehashed_dataset_relabel_rejected(field):
    m, row = module(), result()
    row["dataset"][field] = True if field == "capability_benchmark" else "wrong"
    row["provenance"]["dataset_fingerprint"] = "sha256:"+m["digest"]({"dataset": row["dataset"],
        "source": row["provenance"]["executed_source_sha256"], "seeds": row["seeds"]})
    with pytest.raises(ValueError, match="dataset identity"):
        m["validate_result"]("logact", row)


def test_fake_commit_not_admitted(tmp_path):
    m = module()
    raw = {"device": "cpu", "accelerator": "CPU", "seeds": [42, 43, 44],
           "diagnostic_only": True, "formal_comparison": False, "promotion_eligible": False,
           "evolve_integrated": False, "pretrained_model_calls": 0, "full_experiment_status": "not_reproduced_high_cost",
           "components": {k: {} for k in m["MODULES"]}, "code_commit": "0"*40,
           "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
               for p in (m["RUNNER"], *m["MODULES"].values())}}
    path = tmp_path/"fake.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match="Git object is unavailable"):
        m["curate"](path)


def test_wrong_method_or_lost_execution_contract_rejected():
    m, row = module(), result()
    changed = deepcopy(row)
    changed["method"] = "deepsea"
    with pytest.raises(ValueError, match="component identity"):
        m["validate_result"]("logact", changed)
    changed = deepcopy(row)
    changed["per_seed"][0]["metrics"]["distinct_effects"] = 2
    changed["metrics"] = m["aggregate"](changed["per_seed"])
    with pytest.raises(ValueError, match="recovery failed"):
        m["validate_result"]("logact", changed)


@pytest.mark.parametrize("field", ["archive_sha256", "json_sha256", "upstream_revision", "split",
    "test_rows", "language_test_counts", "public_field_names", "gold_fields_excluded",
    "projected_prefix_sha256", "model_calls", "used_for_training_or_selection"])
def test_official_schema_receipt_cannot_be_relabelled(field):
    row = json.loads((AUDIT/"deepsea-official-schema.json").read_text())
    row[field] = "wrong"
    with pytest.raises(ValueError, match="official schema"):
        module()["validate_official_inspection"](row)


def test_eight_copies_of_one_category_are_not_complete_coverage():
    row = {"source": "cs.AI", "parse_complete": True, "status": "retrieved",
        "announced_on": "2026-10-21", "parsed_entries": 1, "expected_entries": 1, "records": [{}]}
    with pytest.raises(ValueError, match="distinct categories"):
        module()["validate_capture"]([deepcopy(row) for _ in range(8)])


@pytest.mark.parametrize("field,value", [("announced_on", "2026-10-20"), ("status", "unavailable"),
    ("parsed_entries", 2), ("parse_complete", False)])
def test_wrong_bulletin_or_incomplete_capture_rejected(field, value):
    m = module()
    rows = [{"source": name, "parse_complete": True, "status": "retrieved",
        "announced_on": "2026-10-21", "parsed_entries": 1, "expected_entries": 1, "records": [{}]}
        for name in m["CATEGORIES"]]
    rows[0][field] = value
    with pytest.raises(ValueError, match="same-bulletin"):
        m["validate_capture"](rows)


@pytest.mark.parametrize("key", ["deepsea", "logact"])
def test_defining_checks_cannot_be_deleted_or_renamed(key):
    m, row = module(), result(key)
    row["per_seed"][0]["checks"] = {"unrelated_true": True}
    with pytest.raises(ValueError, match="defining contract"):
        m["validate_result"](key, row)


@pytest.mark.parametrize("field,value", [("manifest_ref", "wrong:key"), ("fixture_demo", False), ("schema_version", 1)])
def test_schema_manifest_and_fixture_identity_locked(field, value):
    m, row = module(), result()
    row[field] = value
    with pytest.raises(ValueError, match="identity differs"):
        m["validate_result"]("logact", row)


@pytest.mark.parametrize("field", ["raw_runner_artifact_sha256", "official_schema_inspection_sha256"])
def test_raw_and_official_data_binding_locked(field):
    m, row = module(), result()
    row["provenance"][field] = "wrong"
    with pytest.raises(ValueError, match="provenance binding"):
        m["validate_result"]("logact", row)
