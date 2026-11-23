"""Experience selection formulas and schedule invariants, not agent accuracy."""
import numpy as np
import pytest

from auto_research.agent_research.acting_to_learning import (
    REQUIRES_GPU_VALIDATION, diagnostic, global_schedule, matched_schedule,
    optimizer_aware_features, relevance_scores,
)


def test_optimizer_feature_matches_unbiased_free_ranking_expression():
    g = np.array([[[2., -1.], [1., 3.]]])
    m, v = np.array([[.5, -.2]]), np.array([[.3, .7]])
    expected = (.9 * m[:, None] + .1 * g) / np.sqrt(.999 * v[:, None] + .001 * g**2 + 1e-8)
    np.testing.assert_allclose(optimizer_aware_features(g, m, v), expected)


def test_checkpoint_average_precedes_max_over_families():
    features = np.array([[[1., 0.]], [[1., 0.]]])
    a = np.array([[[1., 0.]], [[-1., 0.]]])
    b = -a
    assert relevance_scores(features, [a, b]).tolist() == [0.]
    # Maximizing a family separately at every checkpoint would incorrectly give1.


def test_each_support_vector_normalized_but_family_mean_not_renormalized():
    feature = np.array([[[1., 0.]]])
    family = np.array([[[100., 0.], [0., 1.]]])
    assert relevance_scores(feature, [family]).tolist() == [.5]


@pytest.mark.parametrize("bad", [0, -1, True, 1.5])
def test_invalid_epsilon(bad):
    if bad == 1.5:
        # beta, not epsilon: epsilon has no paper-defined upper bound.
        with pytest.raises(ValueError):
            optimizer_aware_features([[[1.]]], [[0.]], [[1.]], beta1=bad)
    else:
        with pytest.raises(ValueError):
            optimizer_aware_features([[[1.]]], [[0.]], [[1.]], epsilon=bad)


def test_invalid_moments_zero_vectors_and_overflow_fail_closed():
    with pytest.raises(ValueError):
        optimizer_aware_features([[[1.]]], [[0.]], [[-1.]])
    with pytest.raises(ValueError):
        optimizer_aware_features([[[1e308]]], [[0.]], [[1.]])
    with pytest.raises(ValueError):
        relevance_scores([[[0., 0.]]], [np.ones((1, 1, 2))])
    with pytest.raises(ValueError):
        relevance_scores([[[1., 0.]]], [np.zeros((1, 1, 2))])


def test_global_deduplicates_content_and_preserves_complete_passes():
    contents = ("a", "b", "a", "c", "d")
    schedule = global_schedule(contents, [2, 2, 2, 1, 0], support_size=2, seed=42)
    assert len(schedule) == 6
    assert all(set(schedule[i:i + 2]) == {0, 1} for i in (0, 2, 4))
    assert 2 not in schedule  # score ties use first representatives.


def test_random_duplicate_rows_do_not_gain_sampling_probability():
    for seed in range(20):
        one = global_schedule(("a", "b", "c"), [0, 0, 0], support_size=2, seed=seed, rule="random")
        repeated = global_schedule(("a", "b", "c", "a", "a"), [0]*5, support_size=2, seed=seed, rule="random")
        assert one == repeated


def test_matched_selection_uses_all_eligible_contents_not_only_reference():
    contents = ("a", "b", "c", "d", "e", "f")
    strata = ("p", "p", "p", "c", "c", "c")
    reference = (0, 3, 1, 4, 0, 3, 1, 4)
    schedule = matched_schedule(contents, [0, 1, 2, 0, 1, 2], strata, reference)
    assert all(strata[a] == strata[b] for a, b in zip(schedule, reference))
    assert set(schedule) == {1, 2, 4, 5}
    assert all(schedule.count(index) == 2 for index in set(schedule))


def test_matched_cycle_visits_selected_identity_before_repeating():
    schedule = matched_schedule(("a", "b", "c"), [0, 1, 2], ("s",)*3, (0, 1, 0, 1, 0))
    assert set(schedule[:2]) == {1, 2} and set(schedule[2:4]) == {1, 2}


def test_bad_selection_contracts_rejected():
    with pytest.raises(ValueError):
        global_schedule(("a",), [0], support_size=2)
    with pytest.raises(ValueError):
        global_schedule(("a",), [float("nan")], support_size=1)
    with pytest.raises(ValueError):
        matched_schedule(("a", "a"), [0, 0], ("x", "y"), (0, 1))
    with pytest.raises(ValueError):
        matched_schedule(("a",), [0], ("x",), (True,))
    with pytest.raises(ValueError):
        matched_schedule(("a",), [0], (["x"],), (0,))


def test_cpu_diagnostic_contract():
    assert REQUIRES_GPU_VALIDATION is False
    for seed in (42, 43, 44):
        result = diagnostic(seed)
        assert result["seed"] == seed and result["diagnostic_only"] is True
        assert result["evaluation_tier"] == "l1_mechanism" and all(result["checks"].values())
        assert result["training_executed"] is False and result["agent_evaluation_executed"] is False
    with pytest.raises(ValueError):
        diagnostic(42, "cuda")
