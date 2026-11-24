"""The finite eight-paper delivery must not claim a full-window review."""
import hashlib

from english_learning_sources import question_units
from oct18_frozen_sources import verify_sources
from run_nov24_latest_components import AUDIT, ROOT, config, load, source_hashes, validate_raw


def test_exact_scope_and_cost_dispositions():
    scope=load(AUDIT/"task-scope.json")
    counts=scope["counts"]
    assert (counts["accepted_papers"],counts["low_cost_components"],counts["high_cost_review_only"],counts["cuda_components"])==(8,7,1,1)
    assert counts["first_publications_by_date"]=={"2025-02-10":1,"2026-11-22":1,"2026-11-23":6}
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
    assert set(load(AUDIT/"raw-cuda.json")["components"])=={"deep-cross-attention"}


def test_review_only_has_no_fabricated_execution():
    row=next(r for r in load(AUDIT/"task-scope.json")["papers"] if r["key"]=="morse")
    assert row["implementation_status"]=="deferred_high_cost"
    assert "不复现（审查 DONE）" in row["deferral_reason"]
    assert row["status"]=="deferred" and row["resolution"]=="not_reproduced_high_cost"
    assert row["component_implemented"] is False and row.get("local_operator") is None
    assert row["requires_gpu_validation"] is False
    assert not (ROOT/"docs"/row["detail_path"]).parent.joinpath("metrics").exists()


def test_papers_have_reviewed_english_figures_and_metrics():
    for row in load(AUDIT/"task-scope.json")["papers"]:
        page=ROOT/"docs"/row["detail_path"]
        digest=hashlib.sha256(page.read_bytes()).hexdigest()
        assert f"<!-- source-sha256: {digest} -->" in page.with_name("README-en.md").read_text()
        assert (page.parent/"assets/paper-figure-01.png").stat().st_size>=5000
        assert (page.parent/"assets/provenance.json").is_file()
        for token in ("<!-- paper-figure:start -->", "### 原论文关键图", "assets/paper-figure-01.png",
                      "图片来自[原论文]", "版权归原作者所有", "<!-- paper-figure:end -->"):
            assert token in page.read_text(), (row["key"], token)
        if row["key"] in config()["components"]:
            for device in ("cpu","cuda") if row["requires_gpu_validation"] else ("cpu",):
                metric=load(page.parent/f"metrics/component-{device}-seeds42-44.json")
                assert metric["diagnostic_only"] is True and metric["formal_comparison"] is False


def test_all_papers_have_four_reviewed_bilingual_question_levels():
    seen=set()
    for group in ("foundation","agent","post","root"):
        papers=load(ROOT/f"docs/learning/questions/nov24-latest-{group}.json")["papers"]
        english=load(ROOT/f"docs/en/learning/translations/qa-nov24-latest-{group}.json")["units"]
        assert not seen&set(papers)
        seen.update(papers)
        for record in papers.values():
            assert {q["level"] for q in record["questions"]}=={"basics","mechanism","comparison","implementation"}
        units=question_units({key:value["questions"] for key,value in papers.items()})
        assert set(english)==set(units)
        for key,unit in units.items():
            assert english[key]["source_sha256"]==unit.source_sha256 and english[key]["reviewed"] is True
    assert seen==set(load(AUDIT/"intake-scope.json")["accepted_papers"])
    assert len(load(ROOT/"docs/en/learning/translations/dive-nov24-latest.json")["units"])==32


def test_recent_metadata_is_not_a_qualified_paper_or_backlog_count():
    coverage=load(AUDIT/"source-coverage.json")
    assert coverage["metadata_identities"]==2597 and coverage["announcement_identities"]==883
    assert coverage["newly_captured_recent_first_releases_by_date"]=={"2026-11-20":406,"2026-11-21":302,"2026-11-22":300,"2026-11-23":464}
    assert coverage["first_releases_in_requested_window"]==0
    assert coverage["announcement_dates_observed"]==["2026-11-23"]
    assert coverage["watermark_advanced"] is coverage["all_sources_exhaustive"] is False
    assert load(ROOT/"docs/paper-discovery-watermark.json")["review_watermark"]=="2026-11-15"


def test_google_priority_byline_dates_and_production_evidence():
    review=load(AUDIT/"priority-primary-selection.json")
    assert {r["identity"] for r in review["selected_priority_papers"]}=={"foundation-models:deep-cross-attention","post-training:vopd"}
    assert review["new_directory_urls_relative_to_previous_batch"]==0 and len(review["source_exceptions"])==2
    papers={r["key"]:r for r in load(AUDIT/"task-scope.json")["papers"]}
    assert papers["deep-cross-attention"]["first_author_affiliation"]=="University of California, Irvine"
    assert papers["vopd"]["first_author_affiliation"]=="Stanford University"
    assert papers["vopd"]["code"] and "尚未发布" in papers["vopd"]["code_status"]
    online=papers["weight-coding"]["online_ab"][0]
    assert online["lift_percent"]==10.7 and "not site-wide" in online["traffic"]
