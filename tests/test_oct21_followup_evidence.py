import json
from copy import deepcopy
from pathlib import Path
import runpy

import pytest


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/oct21-followup"


def test_followup_is_same_bulletin_not_fabricated_fresh_papers():
    coverage = json.loads((AUDIT / "source-coverage.json").read_text())
    assert coverage["scope_kind"] == "same-bulletin-backlog-followup"
    assert coverage["counts"]["fresh_since_last_scan"] == len(coverage["new_bulletin_identities"]) == 0
    assert coverage["counts"]["new_official_urls"] == 0
    assert coverage["review_watermark"] == {"before": "2026-10-15", "after": "2026-10-15"}
    assert not coverage["all_sources_exhaustive"] and not coverage["review_watermark_advanced"]
    assert len([r for r in coverage["retrieval_receipts"] if r["kind"] == "arxiv" and r["parse_complete"]]) == 8


def test_six_paper_scope_and_high_cost_is_terminal_not_fake_implementation():
    scope = json.loads((AUDIT / "task-scope.json").read_text())
    assert len(scope["papers"]) == len({r["key"] for r in scope["papers"]}) == 6
    assert sum(r["component_implemented"] for r in scope["papers"]) == 5
    for row in scope["papers"]:
        assert row["review_done"] is True
        assert row["automatic_retry"] is row["automatic_implementation_queue"] is False
        assert row["cost_assessment"]["scale"]
    from auto_research.paper_specs.catalog import catalog_records
    record = next(r for r in catalog_records() if r["key"] == "residency-rl")
    assert record["first_author_affiliation"] == "Google DeepMind"
    assert record["published_at"] == "2026-08-07T17:04:41Z"
    assert record["code"] is None and "明确不公开" in record["code_status"]
    assert record["adapter"] is None and not record.get("local_operator") and not record.get("local_command")
    assert record["implementation_status"] == "deferred_high_cost" and record["review_done"]


def test_actual_followup_evidence_and_portable_source_proofs():
    runpy.run_path(str(ROOT / "scripts/build_oct21_followup_artifacts.py"))["check"]()


def test_source_audit_rejects_unrelated_baseline_before_writing_ledger(tmp_path):
    current, old = tmp_path/"current", tmp_path/"wrong-baseline"
    current.mkdir()
    old.mkdir()
    (current/"retrieval.json").write_text("[]")
    (old/"retrieval.json").write_text("[]")
    module = runpy.run_path(str(ROOT / "scripts/build_oct21_followup_artifacts.py"))
    with pytest.raises(ValueError, match="baseline does not match PR217"):
        module["source_audit"](current, old)


@pytest.mark.parametrize("field", ["adapter_key", "commit", "source", "seeds", "dataset", "metric_path", "raw_sha"])
def test_gpu_receipt_cannot_rebind_same_metrics_to_wrong_paper_or_source(field):
    module = runpy.run_path(str(ROOT / "scripts/build_oct21_followup_artifacts.py"))
    key = "ask-to-distill"
    relative = Path("docs/post-training/2610.27450-ask-to-distill/metrics/component-cuda-seeds42-44.json")
    result = json.loads((ROOT/relative).read_text())
    receipt = deepcopy(json.loads((ROOT/"docs/gpu-validations/ask-to-distill-a100-20261021-followup.json").read_text()))
    if field == "adapter_key":
        receipt["adapter_key"] = "wrong-paper"
    elif field == "commit":
        receipt["provenance"]["commit"] = "0" * 40
    elif field == "source":
        receipt["executed_source_sha256"] = {"wrong-source.py": "0" * 64}
    elif field == "seeds":
        receipt["seeds"] = [1, 2, 3]
    elif field == "dataset":
        receipt["dataset"]["id"] = "wrong-dataset"
    elif field == "metric_path":
        receipt["provenance"]["metric_artifact_path"] = "wrong/path.json"
    else:
        receipt["provenance"]["raw_runner_artifact_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="GPU"):
        module["validate_receipt_binding"](key, receipt, result, relative)
