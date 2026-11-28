"""Keep the single historical Google follow-up bounded and source-bound."""
from hashlib import sha256
import json
from pathlib import Path

import pytest

import run_nov28_habitats_component as runner

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov28-latest"


def load(path):
    return json.loads(path.read_text())


def test_cpu_diagnostic_matches_unified_contract():
    module = runner.load_component("auto_research.agent_research.habitats")
    assert module.REQUIRES_GPU_VALIDATION is False
    runner._base.validate_diagnostic(module.diagnostic(42, device="cpu"), 42, "habitats")
    with pytest.raises(ValueError, match="outside"):
        runner.load_component("auto_research.agent_research.other")


def test_source_bound_actual_result_and_no_invented_cuda():
    frozen = load(AUDIT / "frozen-sources.json")
    assert runner.source_hashes() == frozen["source_sha256"]
    raw = load(AUDIT / "raw-cpu.json")
    runner.validate_raw(raw, frozen)
    with pytest.raises(ValueError, match="No CUDA"):
        runner.validate_raw(raw | {"device": "cuda"}, frozen)
    assert not (AUDIT / "raw-cuda.json").exists()
    assert len(frozen["source_sha256"]) == 5


def test_scope_dates_and_failed_sources_are_not_exhaustiveness():
    scope = load(AUDIT / "task-scope.json")
    assert scope["selected_scope_complete"] is True
    assert scope["accepted_papers"] == ["agent-research:habitats"]
    assert scope["watermark_advanced"] is False
    assert scope["all_sources_exhaustive"] is False
    row = scope["papers"][0]
    assert row["published"] == "2026-11-23"
    assert row["announced_on"] == "2026-11-24"
    assert row["discovered_on"] == "2026-11-28"
    assert row["full_experiment_status"] == "not_reproduced_high_cost"
    assert row["full_experiment_review_done"] is True
    for key in ("requires_gpu_validation", "evolve_integrated", "promotion_eligible", "full_capability_reproduced"):
        assert row[key] is False
    coverage = load(AUDIT / "source-coverage.json")
    assert coverage["first_releases_in_requested_window"] == 0
    assert coverage["new_metadata_identities_relative_to_nov27"] == []
    assert coverage["changed_paper_fact_identities"] == []
    assert coverage["announcement_identity_delta_from_previous_batch"] == 0
    assert coverage["official_directory_successful_captures"] == 0
    assert coverage["github_requests_captured"] == 13
    index = load(AUDIT / "metadata-index.json")
    baseline_path = ROOT / index["baseline"]
    assert index["schema_version"] == 2
    assert index["baseline_sha256"] == sha256(baseline_path.read_bytes()).hexdigest()
    assert set(index["identity_ids"]) <= {r["canonical_id"] for r in load(baseline_path)["identities"]}
    assert len(index["identity_ids"]) == coverage["metadata_identities"]
    assert index["added_identity_ids"] == index["changed_original_fact_identity_ids"] == index["added_announcement_identity_ids"] == []
    priority = load(AUDIT / "priority-primary-selection.json")
    arrow = next(r for r in priority["repository_primary_observations"] if r["repository"] == "google-deepmind/arrow")
    assert arrow["paper_arxiv_identity"] is arrow["first_published_at"] is None
    assert arrow["decision"] == "source_exception_archived"


def test_reviewed_writeup_and_learning_scope():
    page = ROOT / "docs/agent-research/2611.31160-habitats/README.md"
    assert f"<!-- source-sha256: {sha256(page.read_bytes()).hexdigest()} -->" in page.with_name("README-en.md").read_text()
    paper = load(ROOT / "docs/learning/questions/nov28-latest-agent.json")["papers"]["agent-research:habitats"]
    assert {r["level"] for r in paper["questions"]} == {"basics", "mechanism", "comparison", "implementation"}
    assert len(paper["questions"]) == 4
    assert (page.parent / "assets/paper-figure-01.png").is_file()
