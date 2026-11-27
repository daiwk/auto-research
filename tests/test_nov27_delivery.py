"""This intake must remain bounded and its evidence/translation claims honest."""
from hashlib import sha256
import json
from pathlib import Path

import pytest

import run_nov27_latest_components as runner

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov27-latest"


@pytest.mark.parametrize("key", ["integral-deltanet", "deco-attention", "cafa", "elpsd", "compaction-authorization", "budgeted-submapl", "elbo-tds"])
def test_unified_cpu_contract(key):
    item = runner.config()["components"][key]
    module = runner.load_component("auto_research." + item["module"][:-3].replace("/", "."))
    assert module.REQUIRES_GPU_VALIDATION is item["cuda"]
    runner._base.validate_diagnostic(module.diagnostic(42, device="cpu"), 42, key)


def test_seven_translated_component_pages_with_no_capability_promotion():
    scope = json.loads((AUDIT / "task-scope.json").read_text())
    assert scope["selected_scope_complete"] is True
    assert scope["watermark_advanced"] is False
    assert len(scope["papers"]) == 7
    for row in scope["papers"]:
        page = ROOT / "docs" / row["detail_path"]
        text = page.read_text()
        assert not any(ord(c) < 32 and c not in "\n\t\r" for c in text)
        assert f"<!-- source-sha256: {sha256(page.read_bytes()).hexdigest()} -->" in page.with_name("README-en.md").read_text()
        assert row["evaluation_tier"] == "l1_mechanism"
        assert row["evolve_integrated"] is False
        assert row["promotion_eligible"] is False
        assert row["full_capability_reproduced"] is False
        assert (page.parent / "assets/paper-figure-01.png").is_file()
        if row["full_experiment_status"] == "not_run_scope_limited":
            assert row["full_experiment_review_done"] is False


def test_date_and_priority_observations_are_not_new_publication_claims():
    coverage = json.loads((AUDIT / "source-coverage.json").read_text())
    assert coverage["first_releases_in_requested_window"] == 0
    assert coverage["announcement_identity_delta_from_previous_batch"] == 0
    assert coverage["metadata_coverage_complete_to_overlap_boundary"] is True
    assert coverage["all_sources_exhaustive"] is False
    priority = json.loads((AUDIT / "priority-primary-selection.json").read_text())
    assert priority["new_directory_url_count"] == 0
    jepav = next(r for r in priority["repository_primary_observations"] if r["repository"] == "facebookresearch/JEP-AV")
    assert jepav["paper_arxiv_identity"] is None
    assert jepav["decision"] == "source_only_placeholder"
