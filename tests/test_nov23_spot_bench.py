import math

import pytest

from auto_research.foundation_models.spot_bench import diagnostic, score, timeliness


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic(seed):
    assert all(diagnostic(seed)["checks"].values())


def test_best_of_first_k_matches_not_best_over_all_future_predictions():
    one = score([1, 2], [(2, 2)], [[True, True]], occupancy=1)
    two = score([1, 2], [(2, 2)], [[True, True]], occupancy=2)
    assert one["weighted_tp"] < 1 and one["fp_predictions"] == 1
    assert two["weighted_tp"] == 1 and two["fp_predictions"] == 0


def test_algorithm1_and_upstream_allow_multiple_slots_no_invented_closest_break():
    result = score([2], [(1, 3), (2, 4)], [[True], [True]])
    assert result["tp_slots"] == 2 and result["weighted_tp"] == 2


def test_semantic_matrix_is_evaluator_input_and_bad_semantics_count_as_fp_fn():
    result = score([2], [(1, 3)], [[False]])
    assert result["fp_predictions"] == result["fn_slots"] == 1
    assert result["timeliness_f1"] == 0
    with pytest.raises(ValueError):
        score([2], [(1, 3)], [[1]])


def test_chronological_sort_preserves_original_semantic_indices():
    a = score([5, 2], [(1, 3)], [[False, True]])
    assert a["pred_matched"] == [False, True]
    assert a["fp_predictions"] == 1 and a["tp_slots"] == 1


def test_explicit_threshold_and_gaussian_tails():
    assert timeliness(0, 1, 2, sigma_early=2, sigma_late=1) == pytest.approx(math.exp(-.125))
    assert timeliness(3, 1, 2, sigma_early=2, sigma_late=1) == pytest.approx(math.exp(-.5))
    assert score([0], [(1, 2)], [[True]], threshold=.99)["tp_slots"] == 0


@pytest.mark.parametrize("kw", [{"occupancy": True}, {"occupancy": 0}, {"threshold": math.nan}, {"sigma_late": 0}, {"device": "cuda"}])
def test_invalid_protocol_rejected(kw):
    with pytest.raises(ValueError):
        score([1], [(0, 2)], [[True]], **kw)


def test_empty_stream_and_nonfinite_intervals():
    assert score([], [], [])["timeliness_f1"] == 0
    with pytest.raises(ValueError):
        score([math.inf], [(0, 1)], [[True]])
    with pytest.raises(ValueError):
        score([1], [(2, 0)], [[True]])


def test_closed_slot_can_be_skipped_without_marking_open_slot_match_false_positive():
    result = score([1, 2], [(0, 3), (1, 3)], [[True, True], [False, True]], occupancy=1)
    assert result["slot_counts"] == [1, 1]
    assert result["fp_predictions"] == 0


def test_ineligible_predictions_do_not_consume_occupancy():
    result = score([-1000, 1, 2], [(0, 3)], [[True, False, True]], occupancy=1)
    assert result["slot_counts"] == [1]
    assert result["pred_matched"] == [False, False, True]
    assert result["fp_predictions"] == 2
