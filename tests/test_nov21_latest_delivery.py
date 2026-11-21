"""Overlapping selections and historical priority backfills are not new releases."""

import hashlib

from oct18_frozen_sources import verify_sources
from run_nov21_latest_components import AUDIT, ROOT, config, load, source_hashes, validate_raw


def test_exact_intake_counts_and_dates_do_not_claim_fresh_publications():
    scope = load(AUDIT / "task-scope.json")
    counts = scope["counts"]
    assert (counts["accepted_papers"], counts["low_cost_components"], counts["cuda_components"],
            counts["high_cost_review_only"]) == (7, 7, 1, 0)
    assert (counts["new_first_releases"], counts["overlap_new_selections"],
            counts["historical_backfill"]) == (0, 6, 1)
    assert (counts["first_published_nov19"], counts["first_published_nov18"]) == (5, 1)
    assert scope["selected_scope_complete"] is True
    assert scope["watermark_advanced"] is scope["all_sources_exhaustive"] is False
    assert counts["full_capability_reproductions"] == 0
    assert all(row["promotion_eligible"] is row["evolve_integrated"] is False for row in scope["papers"])
    assert all(row["full_experiment_status"] == "not_reproduced_high_cost" for row in scope["papers"])


def test_exact_cpu_cuda_source_seed_evidence():
    frozen = load(AUDIT / "frozen-sources.json")
    assert frozen["source_sha256"] == source_hashes()
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for device, count in (("cpu", 7), ("cuda", 1)):
        raw = load(AUDIT / f"raw-{device}.json")
        validate_raw(raw, frozen)
        assert len(raw["components"]) == count and raw["seeds"] == [42, 43, 44]
        assert raw["formal_comparison"] is raw["evolve_integrated"] is False
    assert set(load(AUDIT / "raw-cuda.json")["components"]) == {"mv-jepa"}


def test_all_new_papers_have_reviewed_bilingual_figures_and_diagnostic_artifacts():
    for paper in load(AUDIT / "task-scope.json")["papers"]:
        page = ROOT / "docs" / paper["detail_path"]
        digest = hashlib.sha256(page.read_bytes()).hexdigest()
        assert f"<!-- source-sha256: {digest} -->" in page.with_name("README-en.md").read_text()
        assert (page.parent / "assets/paper-figure-01.png").stat().st_size > 1000
        assert (page.parent / "assets/provenance.json").is_file()
        item = config()["components"][paper["key"]]
        for device in ("cpu", "cuda") if item["cuda"] else ("cpu",):
            metric = load(page.parent / f"metrics/component-{device}-seeds42-44.json")
            assert metric["diagnostic_only"] is True
            assert metric["formal_comparison"] is False


def test_reviewed_learning_sources_cover_every_level_and_same_topic_update():
    from close_nov21_latest_intake import learning_counts

    counts = learning_counts(set(load(AUDIT / "intake-scope.json")["accepted_papers"]))
    assert counts == {"authored_bilingual_questions": 28, "same_topic_deep_dive_updates": 7}


def test_scan_recall_is_not_a_new_paper_or_backlog_count():
    coverage = load(AUDIT / "source-coverage.json")
    assert coverage["first_releases_since_requested_start"] == 0
    assert coverage["announcement_identity_delta_from_previous_batch"] == 0
    assert coverage["metadata_identities"] == 883 and coverage["announcement_identities"] == 1081
    assert coverage["watermark_advanced"] is coverage["all_sources_exhaustive"] is False
    assert coverage["priority_directory_transport_exceptions"] == 54
    assert coverage["priority_directory_parse_complete"] == 2
    assert coverage["google_directory_comparison_complete"] is False
    initial = AUDIT / coverage["capture_repair"]["initial_receipt"]
    assert hashlib.sha256(initial.read_bytes()).hexdigest() == coverage["capture_repair"]["initial_receipt_sha256"]
    after = load(AUDIT / "priority-source-captures.json")
    assert after["google_directory_delta"]["removed"] == []
    assert all(row.get("transport_gzip_decoded") is True for row in after["pages"] if row.get("parse_complete"))


def test_protected_priority_reviews_and_existing_terminal_status_are_preserved():
    review = load(AUDIT / "priority-primary-selection.json")
    assert {row["identity"] for row in review["priority_admissions"]} == {"agent-research:memlife"}
    meta_ranker = next(row for row in review["selected_primary_reviews"] if row.get("arxiv_id") == "2611.25527v1")
    assert meta_ranker["verified_first_author_affiliation"] == "Meta Platforms, Inc."
    assert meta_ranker["component_implemented"] is False
    assert "abstract-only" in meta_ranker["review_scope"]
    assert "offline" in meta_ranker["reason"] and "production" in meta_ranker["reason"]
    assert review["existing_terminal_priority_candidates"][0]["decision"].endswith("no_automatic_reproduction_retry")
    assert load(ROOT / "docs/paper-discovery-watermark.json")["review_watermark"] == "2026-11-15"
