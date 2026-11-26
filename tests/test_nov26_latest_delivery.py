"""Finite Nov25 first releases deliveredNov26; no backlog/watermark inflation."""
import hashlib

from english_learning_sources import question_units
from oct18_frozen_sources import verify_sources
from run_nov26_latest_components import AUDIT, ROOT, config, load, source_hashes, validate_raw


def test_exact_scope_and_terminal_cost_decisions():
    scope=load(AUDIT/"task-scope.json")
    count=scope["counts"]
    assert (count["accepted_papers"],count["low_cost_components"],count["high_cost_review_only"],count["cuda_components"])==(11,8,3,1)
    assert count["first_publications_by_date"]=={"2026-11-25":11}
    assert count["authored_bilingual_questions"]==44 and count["full_capability_reproductions"]==0
    assert scope["selected_scope_complete"] is True
    assert scope["all_sources_exhaustive"] is scope["watermark_advanced"] is False
    for row in scope["papers"]:
        assert row["full_experiment_status"]==("not_run_scope_limited" if row["key"]=="rap" else "not_reproduced_high_cost")
        assert row["promotion_eligible"] is row["evolve_integrated"] is row["automatic_retry"] is False
        assert row["announced_on"] == "2026-11-26"


def test_frozen_real_cpu_and_cuda_evidence():
    frozen=load(AUDIT/"frozen-sources.json")
    assert frozen["source_sha256"]==source_hashes()
    verify_sources(ROOT,frozen["commit"],frozen["source_sha256"],frozen["proof"])
    for device,count in (("cpu",8),("cuda",1)):
        raw=load(AUDIT/f"raw-{device}.json")
        validate_raw(raw,frozen)
        assert len(raw["components"])==count and raw["seeds"]==[42,43,44]
    assert set(load(AUDIT/"raw-cuda.json")["components"])=={"camar"}


def test_high_cost_review_only_never_fabricates_a_run():
    rows=[r for r in load(AUDIT/"task-scope.json")["papers"] if r["implementation_status"]=="deferred_high_cost"]
    assert {r["key"] for r in rows}=={"jepa-eu","care-opd","agentic-longlive"}
    for row in rows:
        assert row["adapter"] is None and row.get("local_operator") is None
        assert row["status"]=="deferred" and row["resolution"]=="not_reproduced_high_cost"
        assert "不复现（审查 DONE）" in row["deferral_reason"]
        assert row["component_implemented"] is row["requires_gpu_validation"] is False
        assert not (ROOT/"docs"/row["detail_path"]).parent.joinpath("metrics").exists()


def test_reviewed_english_original_figures_and_bound_metrics():
    for row in load(AUDIT/"task-scope.json")["papers"]:
        page=ROOT/"docs"/row["detail_path"]
        digest=hashlib.sha256(page.read_bytes()).hexdigest()
        assert f"<!-- source-sha256: {digest} -->" in page.with_name("README-en.md").read_text()
        for token in ("<!-- paper-figure:start -->","### 原论文关键图","assets/paper-figure-01.png",
                      "图片来自[原论文]","版权归原作者所有","<!-- paper-figure:end -->"):
            assert token in page.read_text(),(row["key"],token)
        assert (page.parent/"assets/paper-figure-01.png").stat().st_size>=5000
        assert (page.parent/"assets/provenance.json").is_file()
        if row["key"] in config()["components"]:
            for device in ("cpu","cuda") if row["requires_gpu_validation"] else ("cpu",):
                result=load(page.parent/f"metrics/component-{device}-seeds42-44.json")
                assert result["diagnostic_only"] is True and result["formal_comparison"] is False


def test_eleven_papers_have_four_authored_reviewed_question_levels():
    seen=set()
    for group in ("foundation","agent","post","root"):
        papers=load(ROOT/f"docs/learning/questions/nov26-latest-{group}.json")["papers"]
        english=load(ROOT/f"docs/en/learning/translations/qa-nov26-latest-{group}.json")["units"]
        assert not seen&set(papers)
        seen.update(papers)
        units=question_units({key:value["questions"] for key,value in papers.items()})
        assert set(english)==set(units)
        for record in papers.values():
            assert {q["level"] for q in record["questions"]}=={"basics","mechanism","comparison","implementation"}
        for key,unit in units.items():
            assert english[key]["reviewed"] is True and english[key]["source_sha256"]==unit.source_sha256
    assert seen==set(load(AUDIT/"intake-scope.json")["accepted_papers"])
    assert len(load(ROOT/"docs/en/learning/translations/dive-nov26-latest.json")["units"])==44


def test_metadata_and_current_bulletin_are_recall_not_selected_backlog():
    coverage=load(AUDIT/"source-coverage.json")
    assert coverage["metadata_identities"]==1200 and coverage["announcement_identities"]==1157
    assert coverage["new_metadata_identities_relative_to_nov25_capture"]==1149
    assert coverage["newly_captured_recent_first_releases_by_date"]=={"2026-11-24":194,"2026-11-25":595}
    assert coverage["first_releases_in_requested_window"]==0
    assert coverage["announcement_dates_observed"]==["2026-11-26"]
    assert coverage["all_sources_exhaustive"] is coverage["watermark_advanced"] is False
    assert load(ROOT/"docs/paper-discovery-watermark.json")["review_watermark"]=="2026-11-15"


def test_google_meta_priority_preserves_source_identity_and_date_limits():
    review=load(AUDIT/"priority-primary-selection.json")
    assert review["selected_priority_papers"]==[]  # finite intake, not absence
    assert review["new_directory_urls_relative_to_previous_batch"]==0
    assert review["google_new_blog"]["existing_identity"]=="agent-research:fuse-evaluator"
    assert review["google_new_blog"]["paper_first_published_at"]=="2026-09-15T17:37:29Z"
    observations=review["repository_primary_observations"]
    assert len(observations)==5 and all(len(r["capture_sha256"])==64 for r in observations)
    assert next(r for r in observations if r["repository"]=="google-deepmind/disco")["decision"]=="existing_paper_public_code_observed"
    scale=load(AUDIT/"scale4d-primary-report.json")
    assert scale["verified_priority_organizations"]==["Meta"]
    assert scale["report_dated_on"]=="2026-11-25" and scale["first_published_at"] is None
    assert scale["arxiv_id"] is None and scale["local_experiment_run"] is False
    assert scale["review_resolution"]=="not_reproduced_high_cost" and scale["automatic_retry"] is False
    assert scale["cost_assessment"]["full_training"]["gpus_per_node"] is None


def test_rap_cost_and_interface_evidence_are_not_upgraded():
    scope=load(AUDIT/"task-scope.json")
    assert scope["counts"]["l1_mechanism_components"]==7 and scope["counts"]["l0_interfaces"]==1
    rap=next(r for r in scope["papers"] if r["key"]=="rap")
    assert rap["full_experiment_review_done"] is False
    metric=load(ROOT/"docs"/rap["detail_path"].replace("README.md","metrics/component-cpu-seeds42-44.json"))
    assert metric["full_experiment_status"]=="not_run_scope_limited" and metric["full_experiment_review_done"] is False
    dual=next(r for r in scope["papers"] if r["key"]=="dualpm")
    assert dual["evaluation_tier"]=="l0_interface"
    coverage=load(AUDIT/"source-coverage.json")
    assert coverage["metadata_coverage_complete_to_overlap_boundary"] is False
    assert coverage["metadata_transport_exceptions"] and "429" in coverage["metadata_transport_exceptions"][0]["error"]
    old=load(AUDIT/"raw-cpu-attempt1.json")
    current=load(AUDIT/"raw-cpu.json")
    assert old["code_commit"]!=current["code_commit"]
    assert load(AUDIT/"frozen-sources-attempt1.json")["commit"]==old["code_commit"]
