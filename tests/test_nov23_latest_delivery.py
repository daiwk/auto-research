"""Nov20 first releases discoveredNov23 are not Nov23 publications."""

import hashlib

from english_learning_sources import question_units
from oct18_frozen_sources import verify_sources
from run_nov23_latest_components import AUDIT, ROOT, config, load, source_hashes, validate_raw


def test_exact_scope_and_cost_dispositions():
    scope=load(AUDIT/"task-scope.json")
    counts=scope["counts"]
    assert (counts["accepted_papers"],counts["low_cost_components"],counts["high_cost_review_only"],counts["cuda_components"])==(9,7,2,1)
    assert counts["first_published_nov20"]==8 and counts["historical_backfill"]==1
    assert counts["full_capability_reproductions"]==0
    assert scope["selected_scope_complete"] is True
    assert scope["watermark_advanced"] is scope["all_sources_exhaustive"] is False
    for row in scope["papers"]:
        assert row["full_experiment_status"]=="not_reproduced_high_cost"
        assert row["promotion_eligible"] is row["evolve_integrated"] is row["automatic_retry"] is False


def test_frozen_real_cpu_cuda_evidence():
    frozen=load(AUDIT/"frozen-sources.json")
    assert frozen["source_sha256"]==source_hashes()
    verify_sources(ROOT,frozen["commit"],frozen["source_sha256"],frozen["proof"])
    for device,count in (("cpu",7),("cuda",1)):
        raw=load(AUDIT/f"raw-{device}.json")
        validate_raw(raw,frozen)
        assert len(raw["components"])==count and raw["seeds"]==[42,43,44]
    assert set(load(AUDIT/"raw-cuda.json")["components"])=={"aimuon"}


def test_review_only_is_not_a_fabricated_component_or_metric():
    for row in load(AUDIT/"task-scope.json")["papers"]:
        if row["key"] not in {"ctrl","coevobench"}:
            continue
        assert row["status"]=="deferred" and row["resolution"]=="not_reproduced_high_cost"
        assert row["component_implemented"] is False and row.get("local_operator") is None
        assert row["requires_gpu_validation"] is False
        assert not (ROOT/"docs"/row["detail_path"]).parent.joinpath("metrics").exists()


def test_papers_have_reviewed_english_figures_and_actual_component_metrics():
    for row in load(AUDIT/"task-scope.json")["papers"]:
        page=ROOT/"docs"/row["detail_path"]
        digest=hashlib.sha256(page.read_bytes()).hexdigest()
        assert f"<!-- source-sha256: {digest} -->" in page.with_name("README-en.md").read_text()
        assert (page.parent/"assets/paper-figure-01.png").stat().st_size>1000
        assert (page.parent/"assets/provenance.json").is_file()
        if row["key"] in config()["components"]:
            devices=("cpu","cuda") if row["requires_gpu_validation"] else ("cpu",)
            for device in devices:
                metric=load(page.parent/f"metrics/component-{device}-seeds42-44.json")
                assert metric["diagnostic_only"] is True and metric["formal_comparison"] is False


def test_all_nine_papers_have_four_reviewed_bilingual_question_levels():
    seen=set()
    for group in ("foundation","agent","post","root"):
        papers=load(ROOT/f"docs/learning/questions/nov23-latest-{group}.json")["papers"]
        english=load(ROOT/f"docs/en/learning/translations/qa-nov23-latest-{group}.json")["units"]
        assert not seen&set(papers)
        seen.update(papers)
        for record in papers.values():
            assert {q["level"] for q in record["questions"]}=={"basics","mechanism","comparison","implementation"}
        units=question_units({key:value["questions"] for key,value in papers.items()})
        assert set(english)==set(units)
        for key,unit in units.items():
            assert english[key]["source_sha256"]==unit.source_sha256 and english[key]["reviewed"] is True
    assert seen==set(load(AUDIT/"intake-scope.json")["accepted_papers"])
    assert len(load(ROOT/"docs/en/learning/translations/dive-nov23-latest.json")["units"])==36


def test_fresh_metadata_and_old_bulletin_are_not_conflated():
    coverage=load(AUDIT/"source-coverage.json")
    assert coverage["metadata_identities"]==1260 and coverage["announcement_identities"]==1081
    assert coverage["newly_captured_first_releases_since_previous_capture"]==160
    assert coverage["first_releases_in_requested_window"]==0
    assert coverage["announcement_identity_delta_from_previous_batch"]==0
    assert coverage["watermark_advanced"] is coverage["all_sources_exhaustive"] is False
    assert load(ROOT/"docs/paper-discovery-watermark.json")["review_watermark"]=="2026-11-15"


def test_google_priority_and_source_exceptions_are_explicit():
    review=load(AUDIT/"priority-primary-selection.json")
    assert {r["identity"] for r in review["selected_priority_papers"]}=={"foundation-models:disco","foundation-models:spot-bench"}
    archived=[r for r in review["google_added_directory_urls"] if r["decision"]=="source_limitation_archived"]
    assert len(archived)==2 and all(r["automatic_retry"] is False for r in archived)
    assert len(review["source_exceptions"])==2
    spot=next(r for r in load(AUDIT/"task-scope.json")["papers"] if r["key"]=="spot-bench")
    assert spot["first_author_affiliation"]=="National University of Singapore" and spot["published"]=="2026-04-27"
    disco=next(r for r in load(AUDIT/"task-scope.json")["papers"] if r["key"]=="disco")
    assert disco["upstream_revision"] is None
