import itertools

import numpy as np
import pytest

from auto_research.reproductions.attribution_sets_components import (
    binomial_tail, squared_risk, unbiased_cell,
)
from auto_research.foundation_models.google16_mild import (
    fit_router, margin_schedule, route, surrogate_and_gradient,
)
from auto_research.foundation_models.google16_proeval import EmpiricalGP
from auto_research.reproductions.spatial_ads_components import (
    Disk, constraints, feasible_ii, round_solution, solve_relaxation,
)


def test_attribution_exact_expectation_over_hidden_binary_streams():
    # Exhaustively verify Theorem1, not a fitted benchmark; learner only sees h(A).
    n, p, k, j = 10, .3, 1, 1
    prior = np.array([1.])
    h0, h1 = .2, .8
    mean1 = (1-p)*h0*h0+p*h1*h1
    mean2 = 1-2*((1-p)*h0+p*h1)
    expectation = 0
    for labels in itertools.product((0, 1), repeat=n):
        m = sum(labels)
        if j > m-k:
            continue
        weight = p**m*(1-p)**(n-m)
        conversion = [i for i, y in enumerate(labels) if y][j-1]
        for r in range(k):
            window = [h1 if labels[conversion-r+i] else h0 for i in range(k)]
            for pos in (1,):
                value = unbiased_cell(1-2*window[pos-1], n=n, p=p, j=j,
                    prior=prior, position=pos, mean_f1=mean1, mean_f2=mean2)
                if pos == 1:
                    expectation += weight*prior[r]*value
    actual_risk = (1-p)*h0*h0+p*(1-h1)**2
    assert expectation == pytest.approx(actual_risk, abs=1e-10)
    assert binomial_tail(5, .5, 3) == pytest.approx(.5)


def test_attribution_printed_v1_finite_n_counterexample_is_preserved():
    # For constant h, the Theorem1 moment identity must also preserve mass.
    # Literal printed beta1*p+beta0 = pi*B+(1-pi), NOT B for k>1.
    n, p, j, k, pi = 10, .3, 2, 2, .6
    b = binomial_tail(n, p, j+k)
    bm = binomial_tail(n-1, p, j+k-1)
    beta0 = (1-p*bm)/(1-p)*(1-pi)
    beta1 = pi*b/p+(bm-(1-p*bm)/(1-p))*(1-pi)
    assert beta1*p+beta0 == pytest.approx(pi*b+1-pi)
    assert abs(beta1*p+beta0-b) > .1
    # The implementation must match the source, and expose—not hide—the mismatch.
    value = unbiased_cell(.6, n=n, p=p, j=j, prior=[pi, 1-pi], position=1,
                          mean_f1=.04, mean_f2=.6)
    assert abs(b*value-(.04+p*.6)) > .1


def test_attribution_fixed_denominator_and_invalid_signals():
    kwargs = dict(n=100, p=.2, prior=[.7, .3], mean_prediction=.4,
                  mean_squared_prediction=.2)
    assert squared_risk([], **kwargs) == 0
    with pytest.raises(ValueError, match="integral"):
        squared_risk([], **{**kwargs, "n": 99})
    with pytest.raises(ValueError):
        unbiased_cell(.4, n=10, p=.3, j=2, prior=[1, 1], position=1,
                      mean_f1=.2, mean_f2=.4)


def test_proeval_bq_acquisition_equals_exact_variance_drop():
    scores = np.array([[.1, .2, .8, .4], [.3, .3, .2, .8], [.6, .1, .7, .1], [.8, .7, .3, .4]])
    gp = EmpiricalGP(scores, historical_ids=['a', 'b', 'c', 'd'], target_id='target')
    before = gp.quadrature()['variance']
    acquisition = gp.acquisition()
    for index in range(4):
        clone = EmpiricalGP(scores, historical_ids=['a', 'b', 'c', 'd'], target_id='target')
        clone.observe(index, .45)
        assert before-clone.quadrature()['variance'] == pytest.approx(acquisition[index])
    gp.observe(gp.select(), .8)
    assert gp.quadrature()['variance'] < before
    assert gp.select(objective='failure', threshold=100) is None
    with pytest.raises(ValueError, match="no target"):
        EmpiricalGP(scores, historical_ids=['a', 'b', 'c', 'target'], target_id='target')


def test_mild_gradient_matches_finite_difference_and_shift_invariance():
    scores = np.array([[.3, -.2, .6], [.2, .4, -.3]])
    costs = np.array([[.1, .8, .4], [.9, .3, .5]])
    rho = margin_schedule([70, 20, 10])
    loss, grad = surrogate_and_gradient(scores, costs, rho)
    assert surrogate_and_gradient(scores+100, costs, rho)[0] == pytest.approx(loss)
    for idx in np.ndindex(scores.shape):
        step = np.zeros_like(scores)
        step[idx] = 1e-6
        numeric = (surrogate_and_gradient(scores+step, costs, rho)[0]
                   - surrogate_and_gradient(scores-step, costs, rho)[0])/2e-6
        assert grad[idx] == pytest.approx(numeric, abs=1e-7)


def test_mild_train_then_infer_without_costs_or_labels():
    x = np.array([[1, -1], [1, -.5], [1, .5], [1, 1.]])
    costs = np.array([[0, 1], [0, 1], [1, 0], [1, 0.]])
    w, losses = fit_router(x, costs, [.5, .5], steps=100)
    assert losses[-1] < losses[0]
    assert route(x, w).tolist() == [0, 0, 1, 1]
    assert route(x, np.zeros((2, 2))).tolist() == [1]*4


def test_spatial_lp_and_paper_rounding_probability():
    d = np.array([[0, .4, 1], [.4, 0, .6], [1, .6, 0]])
    disks = [Disk(0, .5, 2, 0), Disk(1, .5, 1, 1), Disk(2, .7, 3, 2)]
    x, upper = solve_relaxation(d, disks)
    _, a = constraints(d, disks)
    assert np.max(a@x) <= 1+1e-8
    # Algorithm1 marginal inclusion is exactly x_i/9; diagnostic Monte Carlo.
    included = np.zeros(3)
    for seed in range(2000):
        selected = round_solution(d, disks, x, seed=seed)
        assert feasible_ii(d, disks, selected)
        included[selected] += 1
    assert included/2000 == pytest.approx(x/9, abs=.025)
    assert upper >= sum(v.weight for v in disks)/9


def test_spatial_rejects_nonmetric_and_infeasible_lp_point():
    with pytest.raises(ValueError):
        constraints([[0, .2, 1], [.2, 0, .2], [1, .2, 0]], [Disk(0, .2, 1, 0)])
    with pytest.raises(ValueError, match="feasible"):
        round_solution([[0, 1], [1, 0]], [Disk(0, .5, 1, 0), Disk(1, .5, 1, 0)], [1, 1], seed=1)
