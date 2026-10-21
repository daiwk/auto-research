from pathlib import Path
import json
import runpy


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT/"docs/research-audits/oct21-components"


def test_fixed_twelve_paper_scope_and_terminal_cost_decisions():
    scope = json.loads((AUDIT/"task-scope.json").read_text())
    assert len(scope["papers"]) == 12
    assert len({r["id"] for r in scope["papers"]}) == 12
    assert len(scope["fixed_component_keys"]) == 8
    assert len(scope["reference_only_keys"]) == 4
    for row in scope["papers"]:
        assert row["review_done"] is True
        assert row["full_experiment_status"] == "not_reproduced_high_cost"
        assert row["automatic_retry"] is row["automatic_implementation_queue"] is False
        assert row["cost_assessment"]["scale"]
    old = [r for r in scope["papers"] if r["intake_class"] == "historical-backfill"]
    assert len(old) == 1 and old[0]["key"] == "esc"


def test_actual_source_delta_is_not_global_review_closure():
    coverage = json.loads((AUDIT/"source-coverage.json").read_text())
    assert coverage["all_sources_exhaustive"] is coverage["review_watermark_advanced"] is False
    assert coverage["review_watermark"] == {"before": "2026-10-15", "after": "2026-10-15"}
    assert len(coverage["arxiv_sources"]) == 8
    assert all(r["parse_complete"] and r["announced_on"] == "2026-10-21" for r in coverage["arxiv_sources"])
    assert coverage["counts"]["category_entries_including_crosslists_and_replacements"] == sum(
        r["parsed_entries"] for r in coverage["arxiv_sources"])
    assert coverage["counts"]["new_to_repository_recent_papers"] == 11
    identities = {identity.split("v")[0] for values in coverage["bulletin_ids_by_category"].values() for identity in values}
    assert len(identities) == coverage["counts"]["unique_bulletin_identities"]
    assert sum(map(len, coverage["bulletin_ids_by_category"].values())) == coverage["counts"]["category_entries_including_crosslists_and_replacements"]


def test_actual_component_evidence_and_gpu_source_proofs():
    module = runpy.run_path(str(ROOT/"scripts/curate_oct21_component_evidence.py"))
    module["check"]()


def test_reference_only_items_have_no_fake_executable_path():
    scope = json.loads((AUDIT/"task-scope.json").read_text())
    from auto_research.paper_specs.catalog import catalog_records
    index = {(r["domain"],r["key"]):r for r in catalog_records()}
    for row in scope["papers"]:
        record = index[row["domain"],row["key"]]
        assert record.get("promotion_eligible") is False
        assert record.get("evolve_integrated") is False
        if row["key"] in scope["reference_only_keys"]:
            assert record["adapter"] is None
            assert not record.get("local_operator") and not record.get("local_command")
            assert not record.get("requires_gpu_validation")
            assert not list((ROOT/"docs"/Path(row["detail_path"]).parent/"metrics").glob("*.json"))
