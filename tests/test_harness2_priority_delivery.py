"""Integration evidence for the bounded Harness² and priority-backfill MR."""
import json
from pathlib import Path

from auto_research.discovery import repository_paper_statuses
from scripts.audit_historical_priority_backfill import build_inventory
from scripts.curate_harness2_component import validate_curated

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/harness2-priority-repair"


def read(path):
    return json.loads(path.read_text())


def test_harness2_has_real_bounded_cpu_evidence_not_a_capability_claim():
    data = read(ROOT / "docs/agent-research/2610.14224-harness2/metrics/component-cpu-seeds42-44.json")
    validate_curated(data)
    assert data["metrics"]["actual_python_rollouts_total"] == 96
    assert data["metrics"]["improvement_stages_total"] == 72
    assert data["diagnostic_only"] is True
    assert data["promotion_eligible"] is data["evolve_integrated"] is False


def test_reviewed_cost_closures_and_component_delivery_are_separate():
    batch = read(AUDIT / "closure-decisions.json")
    rows = batch["candidates"]
    assert len({row["id"] for row in rows}) == len(rows) == 22
    assert batch["review_watermark_advanced"] is batch["all_sources_exhaustive"] is False
    component = [row for row in rows if row["status"] == "implemented"]
    assert [row["id"] for row in component] == ["2610.14224"]
    assert component[0]["implementation_status"] == "component_only"
    assert component[0]["requires_gpu_validation"] is False
    for row in rows:
        assert row["automatic_retry"] is row["automatic_implementation_queue"] is False
        assert row["review_done"] is True
        assert row["full_text_review"]["full_article_read"] is False
        assert all(row["cost_assessment"].get(k) for k in (
            "source_url", "basis", "scale", "available_resource", "cost_type"))
        if row["id"] != "2610.14224":
            assert row["status"] == "deferred"
            assert row["resolution"] == "not_reproduced_high_cost"
            assert row["low_cost_component_implemented_in_this_mr"] is False
            assert not {"metrics_artifact", "gpu_validation_artifact"}.intersection(row)


def test_fixed_google_date_only_omissions_now_have_honest_catalog_entries():
    statuses = repository_paper_statuses(ROOT / "docs/research-manifest.json", ROOT / "docs/paper-discovery-ledger.json")
    assert statuses["2610.14224"] == "implemented"  # Component only; checked above.
    assert statuses["2610.15150"] == statuses["2610.04109"] == "reviewed"  # Reference-only cost closures.
    for identity in ("2610.07338", "2610.05417", "2610.09015", "2610.09202", "2610.09440",
                     "2610.10990", "2610.11019", "2610.11316", "2610.13886"):
        assert statuses[identity] == "reviewed"  # New real cost decisions, not old generic 'known'.


def test_priority_inventory_is_reproducible_and_does_not_hide_remaining_metadata():
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    expected = build_inventory(read(AUDIT / "google-audit.json"), read(AUDIT / "meta-audit.json"),
        read(ledger_path), repository_paper_statuses(ROOT / "docs/research-manifest.json", ledger_path))
    assert read(AUDIT / "backfill-inventory.json") == expected
    assert expected["counts"]["all_ledger_date_only_unique_identities"] == 198
    assert expected["counts"]["scoped_current_statuses"]["new"] > 0
    assert expected["counts"]["all_ledger_unclosed_pending_delivery_identities"] > 0
    assert expected["all_sources_exhaustive"] is expected["review_watermark_advanced"] is False
    assert expected["frozen_review_snapshots_modified"] is False
