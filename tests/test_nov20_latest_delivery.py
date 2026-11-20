"""The exact Nov20 scope is distinct from recall counts and capability evidence."""

import hashlib
import json
from pathlib import Path

from oct18_frozen_sources import verify_sources
from run_nov20_latest_components import AUDIT, ROOT, config, load, source_hashes, validate_raw


def test_exact_fixed_scope_and_nonpromotion():
    scope = load(AUDIT / "task-scope.json")
    counts = scope["counts"]
    assert (counts["accepted_papers"], counts["low_cost_components"], counts["cuda_components"],
            counts["high_cost_review_only"]) == (11, 9, 4, 2)
    assert (counts["new_first_releases"], counts["announcement_overlap_backfill"],
            counts["historical_backfill"]) == (7, 3, 1)
    assert scope["selected_scope_complete"] is True
    assert scope["watermark_advanced"] is False and scope["all_sources_exhaustive"] is False
    assert counts["full_capability_reproductions"] == 0
    assert len({p["domain"] + ":" + p["key"] for p in scope["papers"]}) == 11
    assert all(p["promotion_eligible"] is False and p["evolve_integrated"] is False for p in scope["papers"])


def test_real_source_bound_seed_device_scope():
    frozen = load(AUDIT / "frozen-sources.json")
    assert frozen["source_sha256"] == source_hashes()
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for device, count in [("cpu", 9), ("cuda", 4)]:
        raw = load(AUDIT / f"raw-{device}.json")
        validate_raw(raw, frozen)
        assert len(raw["components"]) == count
        assert raw["seeds"] == [42, 43, 44]
        assert raw["formal_comparison"] is False and raw["evolve_integrated"] is False
    old = load(AUDIT / "source-freeze-history/71aca03f-unexecuted.json")
    assert old["commit"] != frozen["commit"]
    changed = {k for k, v in old["source_sha256"].items() if frozen["source_sha256"][k] != v}
    assert changed == {"src/auto_research/foundation_models/hisa_components.py",
                       "src/auto_research/post_training/visalloc.py"}


def test_all_bilingual_pages_figures_and_review_only_boundaries():
    scope = load(AUDIT / "task-scope.json")
    for paper in scope["papers"]:
        page = ROOT / "docs" / paper["detail_path"]
        digest = hashlib.sha256(page.read_bytes()).hexdigest()
        assert f"<!-- source-sha256: {digest} -->" in page.with_name("README-en.md").read_text()
        figure = page.parent / "assets/paper-figure-01.png"
        assert figure.is_file() and figure.stat().st_size > 1000
        assert figure.with_name("provenance.json").is_file()
        if not paper["component_implemented"]:
            assert not paper.get("local_operator")
            assert not (page.parent / "metrics").exists()
            assert paper["status"] == "deferred" and paper["resolution"] == "not_reproduced_high_cost"
        else:
            item = config()["components"][paper["key"]]
            for device in ("cpu", "cuda") if item["cuda"] else ("cpu",):
                metric = load(page.parent / f"metrics/component-{device}-seeds42-44.json")
                assert metric["diagnostic_only"] is True and metric["formal_comparison"] is False


def test_authored_learning_complete_with_live_fingerprints():
    from close_nov20_latest_intake import learning_counts

    counts = learning_counts(set(load(AUDIT / "intake-scope.json")["accepted_papers"]))
    assert counts == {"authored_bilingual_questions": 44, "same_topic_deep_dive_updates": 11}


def test_failed_capture_not_interpreted_as_empty_research_and_retry_preserved():
    index = load(AUDIT / "metadata-index.json")
    assert index["initial_failed_api_receipts"][0]["transport_complete"] is False
    assert index["coverage_complete_to_overlap_boundary"] is True
    assert len(index["identities"]) == 1884
    assert len(index["announced_identities"]) == 1081
    assert index["metadata_inventory_is_implementation_backlog"] is False
    assert all(x["parse_complete"] for x in index["announcement_receipts"])


def test_watermark_not_changed_by_incremental_delivery():
    scope = load(AUDIT / "source-coverage.json")
    assert scope["watermark_advanced"] is False and scope["all_sources_exhaustive"] is False
    # Do not pin the live global watermark: later complete review windows may advance it.
    assert scope["fixed_intake"] == "intake-scope.json"
