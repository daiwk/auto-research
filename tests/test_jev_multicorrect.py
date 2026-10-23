from dataclasses import asdict
import math

import pytest

from auto_research.system_one.multicorrect import (
    EvaluatorRow, PublicChoiceList, binary_ece, collect_public_predictions, diagnostic,
    evaluate, evaluate_test, fit_validation_threshold, identical_copy_gap,
)


def test_ranked_corrects_can_still_fail_threshold_selection():
    row = EvaluatorRow("x", (.90,.05,.03,.02), frozenset({0,1}), 4)
    m = evaluate((row,), .25)
    assert m["correct_probability_gap_pp"] == pytest.approx(85)
    assert m["strictly_ranked_with_distractor"] == 1
    assert m["below_uniform_given_strict_ranking"] == 1
    assert m["exact_set_accuracy"] == 0 and m["micro_recall"] == .5


def test_refusals_are_failures_even_for_no_correct_list():
    m = evaluate((EvaluatorRow("x", None, frozenset(), 2),), .25)
    assert m["refusals"] == 1 and m["exact_set_accuracy"] == 0
    assert m["correct_probability_gap_pp"] is None
    assert m["below_uniform_given_strict_ranking"] is None


def test_validation_threshold_is_frozen_and_test_cannot_refit():
    validation = (EvaluatorRow("v", (.9,.05,.03,.02), frozenset({0,1}), 4),)
    rule = fit_validation_threshold(validation)
    assert rule.threshold == .04
    with pytest.raises(ValueError, match="overlap"):
        evaluate_test(rule, validation)
    test = (EvaluatorRow("t", (.8,.1,.06,.04), frozenset({0,1}), 4),)
    assert evaluate_test(rule, test)["exact_set_accuracy"] == 0
    assert evaluate(test, .07)["exact_set_accuracy"] == 1  # Test oracle is NOT used.


def test_micro_counts_and_strict_ranking_exclude_all_correct_and_ties():
    rows = (EvaluatorRow("a", (.5,.3,.2), frozenset({0,1}), 3),
            EvaluatorRow("b", (.5,.5), frozenset({0,1}), 2),
            EvaluatorRow("c", (.4,.3,.3), frozenset({0,1}), 3))
    m = evaluate(rows, .3)
    assert m["strictly_ranked_with_distractor"] == 1
    assert m["micro_precision"] == pytest.approx(6/7)
    assert m["micro_recall"] == 1


def test_public_callback_receives_no_gold_or_private_evaluator_state():
    request = PublicChoiceList("x", "public", ("a", "b"))
    seen = []
    def predictor(row):
        seen.append(asdict(row))
        assert not hasattr(row, "correct")
        with pytest.raises(AttributeError):
            object.__setattr__(row, "correct", {0})
        return (.5,.5)
    assert collect_public_predictions((request,), predictor) == {"x": (.5,.5)}
    assert set(seen[0]) == {"request_id", "question", "choices"}
    with pytest.raises(ValueError, match="duplicate"):
        collect_public_predictions((request,request), predictor)
    private = EvaluatorRow("x", (.5,.5), frozenset({0}), 2)
    with pytest.raises(ValueError, match="only rebuilt public"):
        collect_public_predictions((private,), lambda _: pytest.fail("gold reached predictor"))
    with pytest.raises(ValueError):
        PublicChoiceList("x", {"private_gold": "not a string"}, ("a", "b"))


@pytest.mark.parametrize("p", [(.8,.8), (-.1,1.1), (math.nan,1.), (math.inf,0.), (.5,), (0.,0.)])
def test_invalid_distribution_not_silently_normalized(p):
    with pytest.raises(ValueError):
        EvaluatorRow("x", p, frozenset({0}), 2)


def test_explicit_rounded_api_probabilities_preserved_not_renormalized():
    with pytest.raises(ValueError):
        EvaluatorRow("x", (.50,.49), frozenset({0}), 2)
    row = EvaluatorRow("x", (.50,.49), frozenset({0}), 2, rounding_decimals=2)
    assert sum(row.probabilities) == .99


def test_identical_copy_and_binary_ece_independent_references():
    assert identical_copy_gap(((.2,.2,.2,.2,.2),)) == 0
    assert identical_copy_gap(((.6,.1,.1,.1,.1),)) == 50
    assert binary_ece((.05,.2,.8),(False,True,True)) == pytest.approx(1.05/3)
    assert binary_ece((.05,.2,.8),(False,True,True),exclude_first_bin=True) == pytest.approx(.5)
    assert binary_ece((.05,),(False,),exclude_first_bin=True) == 0
    # Upstream yes_bins uses (low,high], with zero included in the first bin.
    assert binary_ece((.1,.11),(True,False),exclude_first_bin=True) == pytest.approx(.11)
    assert binary_ece((0.,1.),(False,True)) == 0
    assert identical_copy_gap(((.34,.17,.16,.16,.16),),rounding_decimals=2) == pytest.approx(18)
    assert identical_copy_gap(((.35,.18,.16,.16,.16),),rounding_decimals=2) == pytest.approx(19)
    with pytest.raises(ValueError):
        identical_copy_gap(((.34,.17,.16,.16,.16),))


@pytest.mark.parametrize("seed", [42,43,44])
def test_only_contract_counts_not_model_capability(seed):
    r = diagnostic(seed)
    assert all(r["checks"].values()) and r["metrics"]["model_calls"] == 0
    assert not any("accuracy" in key or "success" in key for key in r["metrics"])
