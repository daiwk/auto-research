"""Budget effects must not be confused with same-step or best-seed claims."""
import itertools
import math

import pytest

from auto_research.foundation_models.muon_paired_budget import (
    ValidationTrajectory, frozen_pool_regret, interpolate_loss, normalized_validation_auc,
    optimizer_time_share, paired_budget_comparison, paired_relative_gain_interval,
    select_by_validation_data_auc, stable_data_crossover,
)


def _trajectory(run="ref", seed=42, times=(0., 1., 2., 3., 4.), losses=(4., 3., 2., 1.5, 1.)):
    return ValidationTrajectory(run, seed, (0., 1., 2., 3., 4.), times, losses)


def test_linear_auc_interpolation_common_horizon_and_time_ranking_reversal():
    assert normalized_validation_auc((0., 2., 5.), (6., 4., 1.), 3.) == 4.5
    assert interpolate_loss((0., 2., 5.), (6., 4., 1.), 3.) == 3.
    ref = _trajectory()
    alt = _trajectory("alt", times=(0., 2., 4., 6., 8.), losses=(4., 2.6, 1.5, 1.1, .7))
    data = paired_budget_comparison(ref, alt, axis="data")
    time = paired_budget_comparison(ref, alt, axis="time")
    assert math.isclose(data["reference_auc"], 2.25)
    assert math.isclose(data["alternative_auc"], 1.8875)
    assert math.isclose(time["alternative_auc"], 2.675)
    assert data["relative_auc_gain"] > 0 and time["relative_auc_gain"] < 0
    assert time["common_horizon"] == 4 and time["alternative_endpoint_loss"] == 1.5


def test_validation_selection_uses_auc_not_final_loss_and_no_short_failed_run():
    ref = _trajectory()
    better_auc = _trajectory("better", losses=(4., 1., 1., 1., 2.))
    assert select_by_validation_data_auc([ref, better_auc]) == better_auc
    assert select_by_validation_data_auc([_trajectory("z"), _trajectory("a")]).run_id == "a"
    incomplete = ValidationTrajectory("incomplete", 42, (0., 1.), (0., 1.), (4., 1.))
    with pytest.raises(ValueError):
        select_by_validation_data_auc([ref, incomplete])
    with pytest.raises(ValueError):
        select_by_validation_data_auc([ref, _trajectory("other", seed=43)])


def test_stable_crossover_requires_all_later_checkpoints():
    ref = _trajectory(losses=(4., 4., 4., 4., 4.))
    recover = _trajectory("alt", losses=(4., 3., 4.1, 3., 3.))
    assert stable_data_crossover(ref, recover) == 3
    final_failure = _trajectory("bad", losses=(3., 3., 3., 3., 4.1))
    assert stable_data_crossover(ref, final_failure) is None


def test_bootstrap_resamples_seed_pairs_and_preserves_zero_uncertainty_ratio():
    ref, alt = {42: 1., 43: 10., 44: 100.}, {42: .8, 43: 8., 44: 80.}
    result = paired_relative_gain_interval(ref, alt, resamples=300, seed=42)
    assert result["relative_gain"] == pytest.approx(.2)
    assert result["lower"] == pytest.approx(.2) and result["upper"] == pytest.approx(.2)
    with pytest.raises(ValueError):
        paired_relative_gain_interval(ref, {43: 8., 44: 80., 45: 1.})


def test_regret_matches_small_enumerated_pool_expectation_and_ends_at_zero():
    pool = (1., 1.5, 2.)
    exact = []
    for budget in (1, 2, 3):
        exact.append(sum(min(order[:budget]) - 1 for order in itertools.permutations(pool)) / 6)
    sampled = frozen_pool_regret(pool, permutations=10000, seed=42)
    assert sampled == pytest.approx(exact, abs=.01)
    assert sampled[-1] == 0 and all(a >= b for a, b in zip(sampled, sampled[1:]))
    assert frozen_pool_regret([1., 1.], permutations=1) == (0., 0.)


@pytest.mark.parametrize("x,loss,horizon", [
    ((1., 2.), (2., 1.), 2.), ((0., 0.), (2., 1.), 1.),
    ((0., 2.), (2., float("nan")), 2.), ((0., 2.), (2., 1.), 3.),
    ((0., 2.), (2., 1.), 0.), ((0., 2.), (2., 0.), 1.),
])
def test_auc_rejects_invalid_or_unmeasured_curves(x, loss, horizon):
    with pytest.raises(ValueError):
        normalized_validation_auc(x, loss, horizon)


def test_pairing_and_clock_contracts():
    with pytest.raises(ValueError):
        paired_budget_comparison(_trajectory(), _trajectory(seed=43), axis="data")
    with pytest.raises(ValueError):
        paired_budget_comparison(_trajectory(), _trajectory(), axis="steps")
    assert optimizer_time_share(10., 6.) == .6
    with pytest.raises(ValueError):
        optimizer_time_share(10., 11.)
    with pytest.raises(ValueError):
        frozen_pool_regret([1., float("nan")])
