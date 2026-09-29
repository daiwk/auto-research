import pytest

from auto_research.post_training.paired_public_comparison import PublicRun, compare_runs


def _run(method, seed, validation, test, *, steps=10):
    return PublicRun(method, seed, validation, test, steps, 128, "data-v1", "model-v1")


def test_test_data_cannot_override_validation_choice():
    runs = tuple(
        _run("baseline", seed, 0.5, 0.4) for seed in (42, 43, 44)
    ) + tuple(
        _run("candidate", seed, 0.4, 1.0) for seed in (42, 43, 44)
    )
    result = compare_runs(runs, baseline="baseline")
    assert result["winner"] == "baseline"
    assert result["test_used_for_selection"] is False
    assert result["paired_test_differences"] == (0.0, 0.0, 0.0)


def test_pairing_and_budget_enforced():
    runs = tuple(_run("baseline", seed, 0.5, 0.4) for seed in (42, 43, 44)) + tuple(
        _run("candidate", seed, 0.6, 0.5) for seed in (42, 43, 44)
    )
    result = compare_runs(runs, baseline="baseline")
    assert result["winner"] == "candidate"
    assert result["paired_test_difference_mean"] == pytest.approx(0.1)
    with pytest.raises(ValueError, match="budgets"):
        compare_runs(runs[:-1] + (_run("candidate", 44, 0.6, 0.5, steps=11),),
                     baseline="baseline")
    with pytest.raises(ValueError, match="seeds"):
        compare_runs(runs[:-1] + (_run("candidate", 45, 0.6, 0.5),),
                     baseline="baseline")
