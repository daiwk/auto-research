import math
import random

import pytest

from auto_research.post_training import dfrl


class FixedRandom(random.Random):
    def __init__(self, value):
        super().__init__(0)
        self.value = value
        self.calls = 0

    def random(self):
        self.calls += 1
        return self.value


def test_cost_sign_within_instance_baseline_and_hindsight_cancellation():
    assert dfrl.cost_advantages(((1., 4., 7.), (10., 10., 10.))) == (
        (4.5, 0., -4.5), (0., 0., 0.))
    assert dfrl.cost_advantages(((101., 104., 107.),)) == ((4.5, 0., -4.5),)


def test_skipped_batch_does_not_call_or_materialize_exact_solver():
    def forbidden():
        raise AssertionError("I=0 must not invoke exact optimization")
    rng = FixedRandom(.8)
    row = dfrl.corrected_advantages(((2., 5.), (9., 1.)), forbidden, .2, rng=rng)
    assert row.advantages == ((3., -3.), (-8., 8.))
    assert not row.exact_evaluated and rng.calls == 1


def test_one_correction_draw_and_one_lazy_supplier_for_the_entire_batch():
    calls = []

    def exact():
        calls.append(1)
        return ((1., 5.), (10., 4.))
    rng = FixedRandom(.1)
    row = dfrl.corrected_advantages(((2., 2.), (6., 6.)), exact, .25, rng=rng)
    assert row.advantages == ((16., -16.), (-24., 24.))
    assert row.exact_evaluated and calls == [1] and rng.calls == 1


def test_exact_expectation_over_both_bernoulli_outcomes():
    cheap = ((7., 3., 5.), (8., 9., 3.))
    exact = ((1., 2., 7.), (6., 5., 4.))
    probability = .2
    selected = dfrl.corrected_advantages(cheap, lambda: exact, probability, rng=FixedRandom(.1))
    skipped = dfrl.corrected_advantages(cheap, lambda: exact, probability, rng=FixedRandom(.8))
    target = dfrl.cost_advantages(exact)
    for i, row in enumerate(target):
        for j, value in enumerate(row):
            assert probability*selected.advantages[i][j]+(1-probability)*skipped.advantages[i][j] == pytest.approx(value)


def test_p_one_equals_exact_and_warm_start_has_no_early_exact_calls():
    calls = []

    def exact():
        calls.append(1)
        return ((1., 7.),)
    row = dfrl.corrected_advantages(((8., 8.),), exact, 1., rng=FixedRandom(.999))
    assert row.advantages == ((6., -6.),)
    calls.clear()
    cheap, phase = dfrl.warm_start_advantages(((4., 6.),), exact, step=2, warm_start_steps=3)
    assert (cheap, phase, calls) == (((2., -2.),), "heuristic", [])
    exact_row, phase = dfrl.warm_start_advantages(((4., 6.),), exact, step=3, warm_start_steps=3)
    assert exact_row == ((6., -6.),) and phase == "exact" and calls == [1]


def test_small_exact_knapsack_is_not_an_llm_or_observed_parameter_oracle():
    assert dfrl.enumerate_knapsack((10., 3.), (2., 1.), 2.) == (1, 0)
    assert dfrl.enumerate_knapsack((1., 3.), (2., 1.), 2.) == (0, 1)
    assert dfrl.enumerate_knapsack((1., 1.), (1., 1.), 1.) == (0, 1)
    assert dfrl.enumerate_knapsack((-1., -2.), (1., 1.), 0.) == (0, 0)


@pytest.mark.parametrize("bad", [[], [[1.]], [[1., 2.], [1., 2., 3.]], [[True, 2.]], [[math.nan, 1.]], [[math.inf, 1.]]])
def test_invalid_costs_rejected(bad):
    with pytest.raises(ValueError):
        dfrl.cost_advantages(bad)


@pytest.mark.parametrize("p", [0., -1., 1.01, True, math.nan, math.inf])
def test_invalid_probabilities_rejected(p):
    with pytest.raises(ValueError):
        dfrl.corrected_advantages(((1., 2.),), lambda: ((1., 2.),), p, rng=FixedRandom(.1))


def test_shape_mismatch_and_arithmetic_overflow_rejected():
    with pytest.raises(ValueError):
        dfrl.corrected_advantages(((1., 2.),), lambda: ((1., 2., 3.),), .5, rng=FixedRandom(.1))
    with pytest.raises(ValueError):
        dfrl.cost_advantages(((1e308, -1e308),))
    with pytest.raises(ValueError):
        dfrl.corrected_advantages(((0., 0.),), lambda: ((1e308, 0.),), 1e-308, rng=FixedRandom(0.))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_controls_are_real_cpu_mechanism_checks(seed):
    result = dfrl.diagnostic(seed)
    assert result["device"] == "cpu" and result["diagnostic_only"]
    assert result["controls"] == result["checks"] and all(result["checks"].values())
    assert result["metrics"]["analytic_gradient_max_abs_error"] < 1e-12
    with pytest.raises(ValueError):
        dfrl.diagnostic(seed, "cuda")
