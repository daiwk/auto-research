import math

import numpy as np
import pytest

from auto_research.system_one.request_audit import (
    RetrievalRequest, allowed_label_distribution, audit_paired_predictions,
    binary_pair_metrics, compile_independent, intervention, select_action,
    retained_ab_preference,
)


def request():
    return RetrievalRequest("where?", (("A", "one"), ("B", "two"), ("C", "three")),
                            (("qa", "Does A answer the query?"),), ("A", "B"))


def test_independent_channels_and_gold_free_compilation():
    base = request()
    expanded = intervention(base, "request_expansion", question=("qb", "Does B answer?"))
    assert expanded.passages == base.passages and expanded.eligible == base.eligible
    assert compile_independent(base, "qa") == compile_independent(expanded, "qa")
    evidence = intervention(base, "evidence_addition", passage=("D", "irrelevant"))
    assert evidence.questions == base.questions and evidence.eligible == base.eligible
    assert compile_independent(base, "qa") != compile_independent(evidence, "qa")
    candidate = intervention(base, "candidate_expansion", candidate="C")
    assert candidate.questions == base.questions and candidate.passages == base.passages
    assert compile_independent(base, "qa") == compile_independent(candidate, "qa")
    with pytest.raises(ValueError):
        intervention(base, "candidate_expansion", candidate="D")


def test_allowed_mass_different_from_conditional_probability():
    result = allowed_label_distribution(np.log([.001, .009, .99]), [0, 1])
    assert result["allowed_label_mass"] == pytest.approx(.01)
    assert result["normalized_probability"] == pytest.approx([.1, .9])
    assert allowed_label_distribution([-10000, -10001, 0], [0, 1])["normalized_probability"] == pytest.approx([.7310585786, .2689414214])
    with pytest.raises(ValueError, match="integer"):
        allowed_label_distribution([0, 1], [0.2, 1.0])


def test_candidate_expansion_uses_retained_preference_not_raw_mass():
    assert retained_ab_preference({"A": .6, "B": .4}) == pytest.approx(.6)
    assert retained_ab_preference({"A": .3, "B": .2, "C": .5}) == pytest.approx(.6)
    with pytest.raises(ValueError, match="no probability"):
        retained_ab_preference({"A": 0, "B": 0, "C": 1})


def test_strict_ties_and_action_swaps_are_separate():
    result = binary_pair_metrics([.5, .4, .7], [.9, .6, .8])
    assert result["strict_flip_rate"] == pytest.approx(1 / 3)
    assert result["threshold_tie_rate"] == pytest.approx(1 / 3)
    assert select_action({"A": .5, "B": .5}) is None
    assert select_action({"B": .8, "A": .8}) == "A"


def paired(year, query, scenario, after):
    return {"year": year, "query_id": query, "scenario": scenario,
            "before": {"A": .7, "B": .6}, "after": after, "positive_labels": ["A"]}


def test_query_bootstrap_and_years_separate():
    rows = [paired(2019, "q1", "one", {"A": .6, "B": .7}),
            paired(2019, "q1", "two", {"A": .7, "B": .6}),
            paired(2019, "q2", "one", {"A": .6, "B": .7}),
            paired(2019, "q2", "two", {"A": .7, "B": .6}),
            paired(2020, "q1", "one", {"A": .7, "B": .6})]
    result = audit_paired_predictions(rows, resamples=100)
    assert result["years"]["2019"]["metrics"]["action_change"]["mean"] == .5
    assert result["years"]["2019"]["metrics"]["strict_flip_rate"]["ci95"] is None
    assert result["years"]["2020"]["metrics"]["action_change"]["query_event_upper_bound_95"] == pytest.approx(.95)
    assert audit_paired_predictions(rows, resamples=100) == result


def test_reject_mismatched_targets_incomplete_scenarios_and_nan():
    row = paired(2019, "q1", "one", {"A": .7, "B": .6})
    with pytest.raises(ValueError, match="duplicate"):
        audit_paired_predictions([row, row])
    with pytest.raises(ValueError, match="scenarios"):
        audit_paired_predictions([row, paired(2019, "q2", "two", {"A": .7, "B": .6})])
    with pytest.raises(ValueError):
        binary_pair_metrics([.4], [math.nan])
    with pytest.raises(ValueError):
        audit_paired_predictions([paired(2019, "q1", "one", {"A": .7})])
