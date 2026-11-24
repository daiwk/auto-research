import numpy as np
import pytest

from auto_research.reproductions.weight_coding import centered_ranks, concept_direction, diagnostic, edit, search


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic(seed):
    assert all(diagnostic(seed)["checks"].values())


def test_primitives_are_functional_and_match_definitions():
    w = np.arange(6.).reshape(2, 3)
    ref = np.ones_like(w)
    assert np.array_equal(edit(w, "reset", reference=ref), ref)
    assert np.array_equal(edit(w, "remove"), np.zeros_like(w))
    assert np.allclose(edit(w, "interpolate", reference=ref, coefficient=.25), .75*w+.25)
    assert np.allclose(edit(w, "steer", reference=ref, coefficient=-2), w-2)
    assert np.array_equal(w, np.arange(6.).reshape(2, 3))


def test_ties_are_permutation_invariant_and_zero_centered():
    assert np.array_equal(centered_ranks([2, 2, 2]), [0, 0, 0])
    assert np.allclose(centered_ranks([3, 1, 3, 2]), [1/3, -.5, 1/3, -1/6])


def test_row_scale_cannot_change_directions_or_zero_entries():
    w = np.array([[1., 0.], [1., 2.]])
    result = search(w, lambda x: -float(np.sum(x*x)), lambda x: -float(np.sum(x*x)),
                    mode="row_log_scales", steps=10)
    assert result.weights[0, 1] == 0
    assert np.isclose(result.weights[1, 1] / result.weights[1, 0], 2)
    assert np.all(result.weights[w != 0] / w[w != 0] > 0)


def test_search_never_uses_a_test_callback_and_validation_schedule_is_explicit():
    seen = []
    def validation(w):
        seen.append(w.copy())
        return -float(np.sum(w*w))
    result = search(np.ones(2), lambda w: -float(np.sum(w*w)), validation, steps=11, pairs=3)
    assert result.objective_calls == 66
    assert result.validation_calls == len(seen) == 3  # initial, step10, final


def test_row_log_scale_underflow_is_not_branch_removal():
    with pytest.raises(ValueError, match="underflow|overflow"):
        search(np.ones((2, 2)), lambda w: -float(np.sum(w*w)),
               lambda w: -float(np.sum(w*w)), mode="row_log_scales",
               learning_rate=1000, steps=1, seed=42)


@pytest.mark.parametrize("kwargs", [{"steps":0}, {"pairs":True}, {"sigma":0}, {"learning_rate":float('nan')}, {"mode":"unknown"}])
def test_bad_search_settings(kwargs):
    with pytest.raises(ValueError):
        search(np.ones(2), lambda _: 0, lambda _: 0, **kwargs)


def test_bad_data_and_nonfinite_scores_rejected():
    for w in ([], [float('nan')], [0., 0.]):
        with pytest.raises(ValueError):
            search(w, lambda _: 0, lambda _: 0)
    with pytest.raises(ValueError):
        search([1.], lambda _: float('nan'), lambda _: 0)
    with pytest.raises(ValueError):
        concept_direction([[1.]], [[1.]])
    with pytest.raises(ValueError):
        edit([1.], "compress")
    with pytest.raises(ValueError):
        diagnostic(device="cuda")
