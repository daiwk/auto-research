from copy import deepcopy
import hashlib
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/oct21-priority-backfill"


def module():
    return runpy.run_path(str(ROOT / "scripts/build_oct21_priority_artifacts.py"))


def test_sources_failures_are_not_zero_deltas_or_exhaustive_coverage():
    coverage = json.loads((AUDIT/"source-coverage.json").read_text())
    assert coverage["counts"]["fresh_since_last_scan"] == len(coverage["new_bulletin_identities"]) == 0
    assert coverage["counts"]["historical_backfill"] == coverage["counts"]["same_bulletin_backfill"] == 2
    assert not coverage["review_watermark_advanced"] and not coverage["all_sources_exhaustive"]
    assert coverage["review_watermark"]["after"] == "2026-10-15"
    deltas = {d["organization"]: d for d in coverage["official_directory_deltas"]}
    for org in ("Google", "Meta"):
        assert deltas[org]["status"] == "source_unavailable_not_zero_delta"
        assert deltas[org]["new_directory_urls"] is None
    assert deltas["Google DeepMind"]["retrieved_pages"] == 9
    assert deltas["Google DeepMind"]["new_directory_urls"] == []


def test_four_component_scope_cost_terminal_and_no_capability_promotion():
    rows = json.loads((AUDIT/"task-scope.json").read_text())["papers"]
    assert {r["key"] for r in rows} == {"mice", "flint", "spec-driven-tests", "system-one-rerank"}
    for row in rows:
        assert row["component_implemented"] and row["review_done"]
        assert row["full_experiment_status"] == "not_reproduced_high_cost"
        assert row["cost_assessment"]["scale"]
        assert row["automatic_retry"] is row["automatic_implementation_queue"] is False


def test_executed_source_and_gpu_receipt_integrity():
    module()["check"]()
    result = json.loads((ROOT/"docs/multimodal-models/2610.28435-system-one-rerank/metrics/component-cuda-seeds42-44.json").read_text())
    assert result["pretrained_model_calls"] == 3
    assert result["checkpoint"]["public_id"] == "HuggingFaceTB/SmolVLM-256M-Instruct"
    assert result["checkpoint"]["revision"] == "7e3e67edbbed1bf9888184d9df282b700a323964"
    assert all(row["metrics"]["vlm_forward_passes"] == 1 for row in result["per_seed"])


def test_runner_asserted_nonexistent_commit_cannot_be_curated(tmp_path):
    source = "scripts/run_oct21_priority_backfill.py"
    raw = {"device": "cpu", "seeds": [42, 43, 44], "diagnostic_only": True,
           "code_commit": "0"*40, "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
               for p in (source, "src/auto_research/agent_research/spec_driven_tests.py")},
           "components": {"spec-driven-tests": {"per_seed": [{"seed": seed, "checks": {"fixture_passed": True},
               "metrics": {"cases": 1}} for seed in (42, 43, 44)]}}}
    path = tmp_path/"fake.json"
    path.write_text(json.dumps(raw))
    paths = {key: str(path) for key in module()["COMPONENTS"]}
    with pytest.raises(ValueError, match="Git object is unavailable"):
        module()["curate"](paths)


@pytest.mark.parametrize("field", ["id", "revision", "recipe", "capability_benchmark"])
def test_recomputed_fingerprint_cannot_relabel_generated_data(field):
    m = module()
    result = json.loads((ROOT/"docs/agent-research/2608.17177-spec-driven-tests/metrics/component-cpu-seeds42-44.json").read_text())
    result["dataset"][field] = True if field == "capability_benchmark" else "different"
    p = result["provenance"]
    p["dataset_fingerprint"] = "sha256:"+m["digest"]({"dataset": result["dataset"], "source": p["executed_source_sha256"], "seeds": result["seeds"]})
    with pytest.raises(ValueError, match="dataset identity"):
        m["validate_result"]("spec-driven-tests", result)


@pytest.mark.parametrize("field", ["key", "commit", "source", "checkpoint", "accelerator", "fingerprint"])
def test_receipt_misbindings_are_rejected(field):
    m = module()
    path = Path("docs/multimodal-models/2610.28435-system-one-rerank/metrics/component-cuda-seeds42-44.json")
    result = json.loads((ROOT/path).read_text())
    receipt = deepcopy(json.loads((ROOT/"docs/gpu-validations/system-one-rerank-a100-20261021-late.json").read_text()))
    if field == "key":
        receipt["adapter_key"] = "wrong"
    elif field == "commit":
        receipt["provenance"]["commit"] = "0"*40
    elif field == "source":
        receipt["executed_source_sha256"] = {"wrong.py": "0"*64}
    elif field == "checkpoint":
        receipt["checkpoint"]["revision"] = "wrong"
    elif field == "accelerator":
        receipt["accelerator"]["model"] = "NVIDIA A30"
    else:
        receipt["provenance"]["dataset_fingerprint"] = "0"*64
    with pytest.raises(ValueError, match="GPU"):
        m["validate_binding"]("system-one-rerank", receipt, result, path)


@pytest.mark.parametrize("field,value", [("evaluation_tier", "l3_pipeline"), ("formal_comparison", True),
    ("diagnostic_only", False), ("promotion_eligible", True), ("evolve_integrated", True),
    ("full_experiment_status", "reproduced")])
def test_diagnostic_cannot_be_promoted_by_relabeling(field, value):
    result = json.loads((ROOT/"docs/agent-research/2608.17177-spec-driven-tests/metrics/component-cpu-seeds42-44.json").read_text())
    result[field] = value
    with pytest.raises(ValueError, match="claim boundary"):
        module()["validate_result"]("spec-driven-tests", result)
