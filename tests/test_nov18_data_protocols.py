"""Non-capability contracts for four bounded November 18 CPU components."""

from datetime import datetime, timezone
import math

import pytest

from auto_research.foundation_models import stratified_retention_protocol as retention
from auto_research.foundation_models import tokenization_premium as premium
from auto_research.multimodal import library_retrieval_protocol as library
from auto_research.multimodal import rslivebench_uav_protocol as uav


@pytest.mark.parametrize("module", [retention, premium, library, uav])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostics_are_finite_bounded_reports(module, seed):
    result = module.diagnostic(seed)
    assert module.REQUIRES_GPU_VALIDATION is False
    assert result["seed"] == seed
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] in {"l0_interface", "l1_mechanism"}
    assert result["checks"] and all(type(x) is bool and x for x in result["checks"].values())
    assert all(isinstance(x, (int, float)) and math.isfinite(x) for x in result["metrics"].values())
    with pytest.raises(ValueError, match="CPU"):
        module.diagnostic(seed, "cuda")


def test_retention_separates_correction_negative_flip_and_final_recovery():
    panel = ("a", "b")
    report = retention.invariant_retention([
        retention.ProbeRound(0, panel, (True, False)),
        retention.ProbeRound(1, panel, (False, True)),
        retention.ProbeRound(2, panel, (True, True)),
    ])
    assert report["minimum_retention"] == 0.5
    assert report["negative_flips"] == 1
    assert report["corrected_initial_or_intermediate_errors"] == 2
    with pytest.raises(ValueError, match="stay fixed"):
        retention.invariant_retention([
            retention.ProbeRound(0, panel, (True, True)),
            retention.ProbeRound(1, ("b", "a"), (True, True)),
        ])
    with pytest.raises(ValueError, match="held-out"):
        retention.invariant_retention([retention.ProbeRound(0, panel, (True, True))], adaptation_ids=["a"])


def test_revision_uses_observations_streak_heldout_and_censoring():
    trace = retention.ChangeTrace("change", "regularity", (0.2, -0.2, 0.2, 0.2), "new", "adapt", 4)
    assert retention.revision_report([trace])["regularity"]["latencies"] == [4]
    never = retention.ChangeTrace("never", "regularity", (0.0,) * 4, "new", "adapt", 4)
    censored = retention.ChangeTrace("late", "regularity", (0.2,), "new", "adapt", 4, True)
    report = retention.revision_report([never, censored])["regularity"]
    assert report == {"latencies": [], "never_revised": 1, "censored": 1, "median_latency": None}
    with pytest.raises(ValueError, match="held-out episode"):
        retention.revision_report([retention.ChangeTrace("x", "instance", (0.2, 0.3), "same", "same", 2)])
    with pytest.raises(ValueError, match="censored"):
        retention.revision_report([retention.ChangeTrace("x", "instance", (0.2,), "new", "adapt", 2)])


def test_premium_matches_equation_one_and_excludes_unknown_collapse():
    source = {1: premium.ArticleCount(10), 2: premium.ArticleCount(90)}
    english = {1: premium.ArticleCount(10), 2: premium.ArticleCount(30)}
    report = premium.tokenization_premium(source, english, required_articles=[1, 2])
    assert report["premium"] == 2.5  # not mean([1,3]) == 2
    source[2] = premium.ArticleCount(1, 1)
    report = premium.tokenization_premium(source, english, required_articles=[1, 2])
    assert report["premium"] is None and report["available"] is False
    assert len(premium.UDHR_ARTICLES) == 27
    with pytest.raises(ValueError, match="same declared articles"):
        premium.tokenization_premium(source, {1: premium.ArticleCount(10)}, required_articles=[1, 2])


def test_abstention_cannot_hide_ece_or_reduce_full_energy_denominator():
    confidences, correctness = [0.8, 0.4], [True, False]
    low = premium.selective_audit(confidences, correctness, threshold=0.0, bins=2, total_energy_joules=5)
    high = premium.selective_audit(confidences, correctness, threshold=0.6, bins=2, total_energy_joules=5)
    assert low["all_item_ece"] == high["all_item_ece"] == pytest.approx(0.3)
    assert high["coverage"] == 0.5 and high["risk"] == 0.0
    assert high["correct_answers_per_joule"] == low["correct_answers_per_joule"] == 0.2
    assert premium.selective_audit(confidences, correctness, threshold=1)["risk"] is None
    for kwargs in [{"threshold": 1.1}, {"threshold": 0.5, "total_energy_joules": 0}]:
        with pytest.raises(ValueError):
            premium.selective_audit(confidences, correctness, **kwargs)


def test_author_tokenizer_protocol_joins_articles_once_in_article_order():
    seen = []

    def boundary_sensitive_tokenizer(text):
        seen.append(text)
        return [1] if text == "a b" else [1, 2, 3]

    report = premium.measure_aligned_texts(
        {2: "b", 1: "a"}, {1: "c", 2: "d"}, boundary_sensitive_tokenizer,
        required_articles=[1, 2],
    )
    assert seen == ["a b", "c d"]
    assert report["premium"] == 1 / 3
    collapsed = premium.measure_aligned_texts(
        {1: "a"}, {1: "b"}, lambda _: [0], unknown_token_id=0, required_articles=[1],
    )
    assert collapsed["premium"] is None


def at(month, day):
    return datetime(2026, month, day, tzinfo=timezone.utc)


def test_fifo_uses_admission_not_capture_age_and_requires_new_imagery():
    scenes = tuple(uav.Scene(str(i), at(1, 1), at(1, 2)) for i in range(4))
    window = uav.RollingWindow(at(1, 2), scenes)
    updated, retired = window.advance(uav.Scene("new", at(1, 3), at(2, 1)), at(2, 1))
    assert retired == scenes[0]
    assert [s.scene_id for s in updated.scenes] == ["1", "2", "3", "new"]
    with pytest.raises(ValueError, match="strictly between"):
        window.advance(uav.Scene("old-photo", at(1, 2), at(2, 1)), at(2, 1))
    with pytest.raises(ValueError, match="timezone"):
        uav.Scene("naive", datetime(2026, 1, 1), at(2, 1))


def test_embargo_requires_retirement_and_four_calendar_months():
    assert not uav.disclosure_allowed(first_release=at(1, 31), retired_at=at(2, 1), now=at(5, 30))
    assert uav.disclosure_allowed(first_release=at(1, 31), retired_at=at(2, 1), now=at(5, 31))
    assert not uav.disclosure_allowed(first_release=at(1, 1), retired_at=at(6, 1), now=at(5, 31))
    assert not uav.disclosure_allowed(first_release=at(1, 1), retired_at=None, now=at(12, 1))
    # Calendar month end clamps October 31 + 4 months to next February 28.
    assert uav.disclosure_allowed(first_release=at(10, 31), retired_at=at(12, 1), now=datetime(2027, 2, 28, tzinfo=timezone.utc))


def test_sc_count_strict_parser_relative_thresholds_and_zero_prediction():
    assert uav.strict_count_mra("10", 10) == 100
    assert uav.strict_count_mra("8", 10) == 70
    assert uav.strict_count_mra("0", 10) == 0
    for invalid in ["10 cars", " 10", "10\n", "10.0", "+10", "-1", "１０"]:
        assert uav.strict_count_mra(invalid, 10) == 0
    with pytest.raises(ValueError, match="positive reference"):
        uav.strict_count_mra("0", 0)


def test_uav_hierarchy_group_macro_and_missing_vs_unparseable():
    protocol = [uav.QuestionSpec("a", "0", "t", "c"), uav.QuestionSpec("b", "0", "t", "c")]
    protocol += [uav.QuestionSpec(str(i), str(i), "t", "c") for i in [1, 2, 3]]
    complete = uav.aggregate_scores(protocol, {"a": 100, "b": 100, "1": 0, "2": None, "3": 0}, expected_groups=list("0123"))
    assert complete["overall"] == 25  # not question-micro 40
    assert complete["unparseable_predictions"] == 1
    partial = uav.aggregate_scores(protocol, {"a": 100, "1": 0, "2": None, "3": 0}, expected_groups=list("0123"))
    assert partial["overall"] is None and partial["missing_questions"] == ["b"]
    with pytest.raises(ValueError, match="unknown"):
        uav.aggregate_scores(protocol, {"unknown": 0}, expected_groups=list("0123"))


def test_late_interaction_uses_max_per_query_token_and_distance_direction():
    q, p = [[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]]
    assert library.late_interaction_score(q, p) == 2
    assert library.late_interaction_score(q, p, metric="euclidean") == 0
    assert library.late_interaction_score(q, [[-1.0, -1.0]], metric="manhattan") == -6
    assert library.late_interaction_score([[2.0]], [[3.0]], metric="dot") == 6
    for vectors in [([[0.0, 0.0]], p), ([[1.0]], p), ([[float("nan"), 0.0]], p)]:
        with pytest.raises(ValueError):
            library.late_interaction_score(*vectors)


def test_retrieval_uses_gold_only_in_evaluation_and_retains_unretrieved_labels():
    report = library.retrieval_metrics(["x", "a", "b", "c", "y"], {"a", "c", "z"})
    assert report["precision_at_k"] == 0.4
    assert report["recall_at_k"] == 2 / 3
    assert report["ap_at_k"] == (1 / 2 + 2 / 4) / 3
    assert report["reciprocal_rank_at_k"] == 0.5
    assert library.retrieval_metrics(["a"], {"a"})["precision_at_k"] == 0.2
    with pytest.raises(ValueError, match="unique"):
        library.retrieval_metrics(["a", "a"], {"a"})
    with pytest.raises(ValueError, match="nonempty"):
        library.retrieval_metrics(["a"], set())


def test_late_interaction_extreme_finite_inputs_stay_finite_or_fail_explicitly():
    assert library.late_interaction_score([[1e300, 1e300]], [[1e300, 1e300]]) == pytest.approx(1)
    assert library.late_interaction_score([[1e308] * 4], [[1e308] * 4]) == pytest.approx(1)
    assert library.late_interaction_score([[1e-300, 0]], [[1e-300, 0]]) == pytest.approx(1)
    for metric in ["dot", "euclidean", "manhattan"]:
        with pytest.raises(ValueError, match="finite float range"):
            library.late_interaction_score([[1e308, 1e308]], [[-1e308, -1e308]], metric=metric)


def test_subsets_can_overlap_and_timing_does_not_invert_mean_latency():
    report = library.subgroup_means({"a": {"ap": 0.5}, "b": {"ap": 1.0}}, {"multi_page": ["a"], "conceptual": ["a", "b"]})
    assert report == {"multi_page": {"ap": 0.5}, "conceptual": {"ap": 0.75}}
    timing = library.timing_summary([100, 200, 300], elapsed_seconds=0.4, scope="database_only_preencoded")
    assert timing["qps"] == 7.5  # not 1000 / mean(100,200,300) == 5
    assert timing["p95_latency_ms"] == pytest.approx(290)
    assert timing["p99_latency_ms"] == pytest.approx(298)
    with pytest.raises(ValueError, match="scope"):
        library.timing_summary([10], elapsed_seconds=1, scope="unqualified")
