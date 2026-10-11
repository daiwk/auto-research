import numpy as np
import pytest

from auto_research.agent_research.ontrack_transport import (
    diagnostic, frontier_marginal, graph_distances, gw_gradient, objective, sinkhorn, solve,
)


def test_true_quadratic_gw_gradient_matches_finite_difference_not_index_proxy():
    rng = np.random.default_rng(8)
    a = graph_distances([[], [0], [0]])
    b = graph_distances([[], [0], [1], [1]])
    t = rng.random((3, 4))
    g = gw_gradient(t, a, b)
    def quadratic(x):
        return .5 * np.sum(gw_gradient(x, a, b) * x)
    delta = np.zeros_like(t)
    delta[1, 2] = 1e-6
    derivative = (quadratic(t + delta) - quadratic(t - delta)) / 2e-6
    assert derivative == pytest.approx(g[1, 2], rel=1e-6)


def test_frontier_uses_previous_mass_and_keeps_independent_antichain_active():
    parents = [[], [0], [0], [1, 2]]
    nu, active, _ = frontier_marginal(parents, np.zeros((0, 4)))
    np.testing.assert_allclose(nu, [.25, .075, .075, .0025])
    assert active.tolist() == [True, False, False, False]
    previous = np.array([[.25, 0., 0., 0.]])
    nu, active, _ = frontier_marginal(parents, previous)
    assert active.tolist() == [True, True, True, False]
    assert nu[1] == nu[2] == .25


def test_unbalanced_sinkhorn_can_destroy_bad_mass_not_force_marginals():
    costs = np.array([[0., 1.], [10., 10.]])
    state = sinkhorn(costs, [.5, .5], [.5, .5], inner=200)
    assert state.coupling[1].sum() < 1e-10
    assert state.coupling[0].sum() > .1
    assert np.isfinite(state.coupling).all()


def test_final_cold_solve_is_permutation_equivariant_and_disables_online_ages():
    a = graph_distances([[], [0], [0]])
    c = np.array([[0., .8, .8], [.8, 0., .8], [.8, .8, 0.]])
    mass = np.ones(3) / 3
    result = solve(c, a, a, mass, mass, outer=10, inner=50)
    permutation = np.array([0, 2, 1])
    permuted = solve(c[permutation], a[permutation][:, permutation], a, mass, mass, outer=10, inner=50)
    np.testing.assert_allclose(permuted.coupling, result.coupling[permutation], atol=1e-10)
    assert diagnostic(c, result.coupling, a, a, mass, mass) != objective(c, result.coupling, a, a, mass, mass)
    with pytest.raises(ValueError, match="age weights"):
        solve(c, a, a, mass, mass, ages=[1., 2., 1.])


def test_warm_streaming_keeps_old_rows_and_adds_provisional_structural_row():
    d = graph_distances([[], [0]])
    first = solve(np.array([[0., 1.]]), np.zeros((1, 1)), d, [.5], [.5, .15], ages=[0.])
    second = solve(np.array([[0., 1.], [1., 0.]]), d, d, [.5, .5], [.5, .5], state=first, ages=[1., 0.])
    assert second.coupling.shape == (2, 2)
    assert second.coupling[0, 0] >= .3 * first.coupling[0, 0]
    with pytest.raises(ValueError, match="chronological"):
        graph_distances([[1], []])
