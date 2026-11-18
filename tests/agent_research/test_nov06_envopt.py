import pytest

from auto_research.agent_research.envopt import (
    Step,
    Trial,
    Validation,
    diagnostic,
    replay_environment_evolution,
    select_training_environment,
)


def test_inner_rule_uses_best_accepted_cost_and_ignores_unreliable_or_equal_cost():
    trials = (
        Trial("a", "fixed", 6, True),
        Trial("b", "fixed", 7, True),
        Trial("c", "fixed", 1, False),
        Trial("d", "fixed", 6, True),
        Trial("e", "fixed", 5, True),
    )
    assert select_training_environment("base", "fixed", 8, trials) == ("e", 2)
    with pytest.raises(ValueError, match="fixed target harness"):
        select_training_environment("base", "fixed", 8, (Trial("x", "modified", 1, True),))


@pytest.mark.parametrize(("cost", "accuracy"), [(4, 1), (1, 0.625)])
def test_first_regression_rolls_back_exactly_one_step(cost, accuracy):
    baseline = Validation("base", 8, 1)
    prior = Validation("a", 3, 0.875)
    steps = (
        Step(("train-a",), "base", 8, (Trial("a", "fixed", 3, True),), prior),
        Step(("train-b",), "a", 3, (Trial("b", "fixed", 1, True),), Validation("b", cost, accuracy)),
        Step(("must-not-run",), "unreached", 0, (), Validation("unreached", 0, 1)),
    )
    result = replay_environment_evolution(baseline, ("val",), "fixed", steps, tolerance=0.125)
    assert result.retained == prior
    assert result.accepted_steps == 1
    assert result.rollback_step == 2


def test_shard_overlap_and_mismatched_validation_rejected():
    baseline = Validation("base", 8, 1)
    with pytest.raises(ValueError, match="disjoint"):
        replay_environment_evolution(
            baseline, ("val",), "fixed",
            (Step(("val",), "base", 8, (), baseline),), tolerance=0,
        )
    with pytest.raises(ValueError, match="training-selected"):
        replay_environment_evolution(
            baseline, ("val",), "fixed",
            (Step(("train",), "base", 8, (), Validation("other", 4, 1)),), tolerance=0,
        )


def test_accepts_equal_validation_cost_and_exact_tolerance():
    baseline = Validation("base", 8, 1)
    next_result = Validation("a", 8, 0.875)
    step = Step(("train",), "base", 8, (Trial("a", "fixed", 4, True),), next_result)
    outcome = replay_environment_evolution(baseline, ("val",), "fixed", (step,), tolerance=0.125)
    assert outcome.retained == next_result
    assert outcome.rollback_step is None


def test_invalid_numbers_and_diagnostic_contract():
    with pytest.raises(ValueError, match="finite"):
        Validation("base", float("nan"), 1)
    with pytest.raises(ValueError, match="explicit bool"):
        Trial("a", "fixed", 1, 1)
    for seed in (42, 43, 44):
        result = diagnostic(seed)
        assert result["seed"] == seed and all(result["checks"].values())
        assert result["diagnostic_only"] is True
        assert result["metrics"]["retained_steps"] == 1
    with pytest.raises(ValueError, match="CPU-only"):
        diagnostic(42, "cuda")
