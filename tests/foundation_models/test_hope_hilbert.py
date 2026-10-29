import math

import numpy as np
import pytest
from scipy.integrate import quad

from auto_research.foundation_models.hope_hilbert import (
    diagnostic, operator_pair_gram, prune_dense_neuron, pruning_rates,
    relu_cross_kernel, relu_moments, restore_dense_neuron, warped_correlation,
)


@pytest.mark.parametrize("beta,gamma", [(0., 1.), (.7, -.3), (-1.2, 2.1), (1., 0.), (-1., 0.)])
def test_relu_moments_match_independent_integration(beta, gamma):
    mean, second, variance = relu_moments(beta, gamma)
    if gamma:
        s = abs(gamma)
        normal = lambda z: math.exp(-z*z/2) / math.sqrt(2*math.pi)
        m = quad(lambda z: (beta+s*z)*normal(z), -beta/s, math.inf)[0]
        q = quad(lambda z: (beta+s*z)**2*normal(z), -beta/s, math.inf)[0]
        assert mean == pytest.approx(m, abs=1e-11)
        assert second == pytest.approx(q, abs=1e-11)
    else:
        assert mean == max(0, beta)
    assert variance == pytest.approx(second-mean*mean, abs=1e-12)


@pytest.mark.parametrize("rho", [-1., -.9, -.2, 0., .7, .999, 1.])
def test_zero_mean_kernel_recovers_arc_cosine_exactly(rho):
    got = relu_cross_kernel(0., 1.4, 0., .8, rho)
    expected = 1.4*.8/(2*math.pi)*(math.sqrt(1-rho*rho)+(math.pi-math.acos(rho))*rho)
    assert got == pytest.approx(expected, abs=1e-11)


@pytest.mark.parametrize("rho", [-1., -.3, .4, 1.])
def test_biased_cross_symmetry_bounds_and_limit(rho):
    bi, si, bj, sj = .4, .7, -.2, 1.3
    k = relu_cross_kernel(bi, si, bj, sj, rho)
    assert k == pytest.approx(relu_cross_kernel(bj, sj, bi, si, rho), abs=1e-11)
    assert 0 <= k <= math.sqrt(relu_moments(bi, si)[1]*relu_moments(bj, sj)[1]) + 1e-12
    if abs(rho) == 1:
        split = sorted({-bi/si, -bj/(rho*sj)})
        f = lambda z: max(0., bi+si*z)*max(0., bj+rho*sj*z)*math.exp(-z*z/2)/math.sqrt(2*math.pi)
        points = [-math.inf, *split, math.inf]
        independent = sum(quad(f, a, b, epsabs=1e-12)[0] for a, b in zip(points, points[1:]))
        assert k == pytest.approx(independent, abs=1e-11)


def test_independent_and_deterministic_marginals():
    mi = relu_moments(.4, .7)[0]
    mj = relu_moments(-.2, 1.3)[0]
    assert relu_cross_kernel(.4, .7, -.2, 1.3, 0.) == mi*mj
    assert relu_cross_kernel(2., 0., -.2, 1.3, .8) == 2*mj
    assert relu_cross_kernel(-2., 0., -.2, 1.3, -.8) == 0


def test_diagonal_consistency_and_centering_not_conflated():
    w = np.array([[1., 2.], [1., 2.]])
    out = np.array([[2., -1.], [2., -1.]])
    beta, gamma = np.array([.3, .3]), np.array([.8, .8])
    uncentered = operator_pair_gram(w, out, beta, gamma, centered=False)
    centered = operator_pair_gram(w, out, beta, gamma, centered=True)
    m, q, var = relu_moments(.3, .8)
    assert uncentered == pytest.approx(np.full((2, 2), 5*q))
    assert centered == pytest.approx(np.full((2, 2), 5*var))
    assert uncentered[0, 0]-centered[0, 0] == pytest.approx(5*m*m)


@pytest.mark.parametrize("beta,gamma", [(1e8, 1.), (1e6, -.3), (1., 1e-100)])
def test_large_positive_mean_keeps_small_representable_variance(beta, gamma):
    mean, _, variance = relu_moments(beta, gamma)
    assert mean == beta
    assert variance == pytest.approx(gamma*gamma, rel=1e-14, abs=0)


def test_large_mean_centered_gram_uses_exact_independence_and_diagonal_limits():
    beta, gamma = np.full(2, 1e8), np.ones(2)
    out = np.ones((2, 1))
    independent = operator_pair_gram(np.eye(2), out, beta, gamma)
    identical = operator_pair_gram(np.ones((2, 2)), out, beta, gamma)
    assert np.array_equal(independent, np.eye(2))
    assert np.array_equal(identical, np.ones((2, 2)))


@pytest.mark.parametrize("weights", [
    np.array([[1., 0.], [-1., 0.]]),
    np.array([[1., 0.], [.6, .8]]),
])
def test_large_mean_other_centered_covariances_fail_closed(weights):
    with pytest.raises(ValueError, match="cancellation exceeds tolerance"):
        operator_pair_gram(weights, np.ones((2, 1)), np.full(2, 1e8), np.ones(2))


def test_large_positive_biased_cross_does_not_miss_gaussian_mass():
    # Integrating from -infinity to 1e4 without a finite density window can
    # miss all mass around zero and misleadingly return 0 with error 0.
    got = relu_cross_kernel(1e4, 1., 1e4, 1., .6)
    assert got == pytest.approx(1e8 + .6, rel=0, abs=1e-6)


def test_warped_correlation_uses_variance_constraints_not_raw_cosine():
    a, b = np.array([1., 0.]), np.array([.6, .8])
    rho = warped_correlation(a, b, .5, 2.)
    kappa = .6/(1-.6**2)*.5*2.
    assert rho/(1-rho*rho) == pytest.approx(kappa)
    assert warped_correlation(a, a, 1., 1.) == 1.
    assert warped_correlation(a, -a, 1., 1.) == -1.
    assert warped_correlation(a, b, .5, .5) != pytest.approx(.6)
    with pytest.raises(ValueError):
        warped_correlation(np.zeros(2), b, 1., 1.)


def test_pruning_rate_static_footprints_and_last_neuron_barrier():
    capacities = np.array([.25, .8, 1.2])
    footprints = np.array([3., 35., 5.])
    rates, index = pruning_rates(capacities, footprints)
    assert rates == pytest.approx(3*capacities/(capacities.sum()-capacities)/footprints)
    assert index == 1 != np.argmin(capacities)
    rates, index = pruning_rates(np.array([0., 1.]), np.ones(2))
    assert index == 0 and rates[0] == 0 and math.isinf(rates[1])
    with pytest.raises(ValueError, match="no admissible"):
        pruning_rates(np.array([1.]), np.ones(1))


def test_dense_prune_compensates_mean_and_exact_undo_without_mutation():
    weights = np.array([[1., 2.], [-.2, .3]])
    means = np.array([.5, -.7])
    activation_means = np.array([.8, .4])
    snapshot_w, snapshot_m = weights.copy(), means.copy()
    pruned, adjusted, packet = prune_dense_neuron(weights, means, 0, .8)
    assert np.array_equal(weights, snapshot_w) and np.array_equal(means, snapshot_m)
    assert np.array_equal(pruned[0], np.zeros(2))
    assert adjusted == pytest.approx(means-.8*weights[0])
    assert activation_means @ pruned-adjusted == pytest.approx(activation_means @ weights-means)
    restored, restored_mean = restore_dense_neuron(pruned, adjusted, packet)
    assert np.array_equal(restored, weights) and np.array_equal(restored_mean, means)
    assert np.array_equal(pruned[0], np.zeros(2))
    with pytest.raises(ValueError, match="stale"):
        restore_dense_neuron(pruned+.01, adjusted, packet)


@pytest.mark.parametrize("call", [
    lambda: relu_moments(float("nan"), 1.),
    lambda: relu_cross_kernel(0., 1., 0., 1., 1.001),
    lambda: relu_moments(True, 1.),
    lambda: pruning_rates(np.array([0., 0.]), np.ones(2)),
    lambda: pruning_rates(np.array([1., -1.]), np.ones(2)),
    lambda: pruning_rates(np.array([1., 2.]), np.array([0., 1.])),
    lambda: prune_dense_neuron(np.ones((2, 2)), np.ones(2), True, 1.),
    lambda: prune_dense_neuron(np.ones((2, 2)), np.ones(3), 0, 1.),
    lambda: prune_dense_neuron(np.ones((2, 2)), np.ones(2), 0, -.1),
    lambda: diagnostic(42, "cuda"),
])
def test_fail_closed_invalid_inputs(call):
    with pytest.raises(ValueError):
        call()


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_measures_actual_numerical_contracts(seed):
    row = diagnostic(seed)
    assert len(row["checks"]) == 7 and all(row["checks"].values())
    assert row["metrics"]["cross_kernel_reference_error"] < 1e-10
    assert row["metrics"]["restore_error"] == 0
    assert row["metrics"]["capacity_only_negative_control_rate_gap"] > 0
