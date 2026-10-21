from dataclasses import fields, replace

import pytest

from auto_research.agent_research.google16_tfrbench import (
    Event,
    ForecastView,
    ReferenceModels,
    build_reference,
    evaluate_forecaster,
    mase,
    matrix,
)

HISTORY = matrix([[1], [2], [3], [4]])
TARGET = matrix([[5], [6]])


def models(forecast=None, consistency=None):
    return ReferenceModels(
        search=lambda view: (),
        hypotheses=lambda view: "A rising trend is plausible.",
        verify_assumptions=lambda hypothesis, events: "local fixture assumption only",
        reason=lambda view: ("continue trend", "flat"),
        forecast=forecast or (lambda view: [[5], [6]] if "trend" in view.reasoning else [[4], [4]]),
        consistency=consistency or (lambda trace, forecast: 4),
        diagnose=lambda candidate: "reconsider trend",
        summarize=lambda trace: trace,
        select=lambda candidates: min(range(len(candidates)), key=lambda i: (candidates[i].mase, -candidates[i].consistency)),
    )


def test_mase_formula_and_degenerate_scale_are_not_hidden():
    assert mase(HISTORY, TARGET, matrix([[4], [4]])) == 1.5
    assert mase(HISTORY, TARGET, TARGET) == 0
    assert mase(matrix([[1, 10], [2, 12]]), matrix([[3, 14]]), matrix([[4, 18]])) == 1.5
    with pytest.raises(ValueError, match="zero-scale"):
        mase(matrix([[1], [1]]), matrix([[1]]), matrix([[1]]))
    with pytest.raises(ValueError, match="shape"):
        mase(HISTORY, TARGET, matrix([[5]]))


def test_forecaster_view_excludes_gold_targets_and_one_shot_is_not_selected():
    seen = []

    def forecast(view):
        seen.append(view)
        return [[4], [4]]

    result = evaluate_forecaster(history=HISTORY, target=TARGET, reasoning="flat", forecast=forecast, cutoff="2026-01-01T00:00:00Z")
    assert len(seen) == 1
    assert set(field.name for field in fields(ForecastView)) == {"history", "reasoning", "horizon", "description"}
    assert not result["outcome_feedback"]
    assert result["mase"] == 1.5


def test_post_cutoff_news_rejected_but_known_future_holiday_can_be_forecast_context():
    event = Event("scheduled holiday", "https://example.org/calendar", "2025-12-01T00:00:00Z", "2026-01-02T00:00:00Z")
    result = evaluate_forecaster(history=HISTORY, target=TARGET, reasoning="trend", forecast=lambda view: TARGET, cutoff="2026-01-01T00:00:00Z", events=[event])
    assert result["mase"] == 0
    with pytest.raises(ValueError, match="post-cutoff"):
        evaluate_forecaster(history=HISTORY, target=TARGET, reasoning="trend", forecast=lambda view: TARGET, cutoff="2026-01-01T00:00:00Z", events=[replace(event, published_at="2026-01-03T00:00:00Z")])


def test_reference_is_explicitly_outcome_conditioned_and_summary_rechecked():
    result = build_reference(history=HISTORY, target=TARGET, models=models())
    assert result["reference_accepted"]
    assert result["summary_accepted"]
    assert len(result["candidates"]) == 2
    assert result["protocol"].startswith("outcome_conditioned")
    assert not result["promotion_eligible"]


def test_bad_summary_not_retained_and_low_consistency_never_accepted():
    configured = replace(models(), summarize=lambda trace: "flat")
    result = build_reference(history=HISTORY, target=TARGET, models=configured)
    assert result["reference_accepted"] and result["summary"] is None
    assert result["summary_mase"] == 1.5
    result = build_reference(history=HISTORY, target=TARGET, models=models(consistency=lambda trace, forecast: 3))
    assert not result["reference_accepted"]
    assert len(result["candidates"]) == 6


def test_verifier_selector_and_budgets_fail_closed():
    with pytest.raises(ValueError, match="integer 1..5"):
        build_reference(history=HISTORY, target=TARGET, models=models(consistency=lambda trace, prediction: True))
    with pytest.raises(ValueError, match="candidate index"):
        build_reference(history=HISTORY, target=TARGET, models=replace(models(), select=lambda candidates: -1))
    with pytest.raises(ValueError, match="bounded"):
        build_reference(history=HISTORY, target=TARGET, models=models(), max_loops=4)
