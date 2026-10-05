import pytest

from auto_research.agent_research.adastep import StepObservation, assign_step_credit


def _group(returns_zero, returns_one, *, task_id="task"):
    return [
        StepObservation(task_id, "state", action, value, 0.5)
        for action, values in (("zero", returns_zero), ("one", returns_one))
        for value in values
    ]


def test_action_explained_variance_and_within_action_noise():
    signal = assign_step_credit(_group([0, 0.1], [1, 1.1]))
    assert signal[0].coefficient > 0.98
    assert all(item.estimable for item in signal)
    noise = assign_step_credit(_group([0, 1], [0, 1]))
    assert [item.coefficient for item in noise] == pytest.approx([0] * 4)
    assert [item.combined_advantage for item in noise] == pytest.approx([0.5] * 4)


def test_sparse_and_tied_groups_follow_paper_fallback():
    sparse = assign_step_credit(_group([0], [1]))
    assert all(item.coefficient == 1 and not item.estimable for item in sparse)
    tied = assign_step_credit(_group([1, 1], [1, 1]))
    assert all(item.local_advantage == 0 and item.combined_advantage == 0.5 for item in tied)
    with pytest.raises(ValueError):
        assign_step_credit([])


def test_normalization_uses_total_group_std_not_per_action_std():
    observations = _group([0, 0], [1, 1])
    credits = assign_step_credit(observations, normalize_local=True)
    assert [item.local_advantage for item in credits] == [-1, -1, 1, 1]


def test_identical_anchor_names_from_different_tasks_do_not_share_statistics():
    first = _group([0, 0], [1, 1], task_id="first")
    second = _group([10, 10], [10, 10], task_id="second")
    credits = assign_step_credit(first + second)
    assert [item.local_advantage for item in credits[:4]] == [-0.5, -0.5, 0.5, 0.5]
    assert all(item.local_advantage == 0 for item in credits[4:])
