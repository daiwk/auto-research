import itertools
import math

import numpy as np
import pytest
import torch

from auto_research.post_training import drd_mopd, excursion_td, maxim, mcpo


@pytest.mark.parametrize("module", [maxim, mcpo, excursion_td, drd_mopd])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_seeded_diagnostics_have_real_checks(module, seed):
    result = module.diagnostic(seed)
    assert result["seed"] == seed
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert result["checks"] and all(result["checks"].values())
    assert all(math.isfinite(value) for value in result["metrics"].values())


@pytest.mark.parametrize("module", [maxim, mcpo, excursion_td])
def test_cpu_components_reject_cuda(module):
    with pytest.raises(ValueError, match="CPU"):
        module.diagnostic(42, "cuda")


def test_maxim_valid_token_pmi_and_null_control():
    conditional = np.array([[-1., -2., np.nan], [-.5, -.7, -3.]])
    null = np.array([[-3., -2., np.nan], [-1., -1., -1.]])
    mask = np.array([[True, True, False], [True, True, True]])
    assert np.allclose(maxim.normalized_pmi(conditional, null, mask), [1., -.4])
    assert np.all(maxim.normalized_pmi(null, null, mask) == 0)
    # Adding the same target-difficulty offset to both queries cancels.
    assert np.allclose(maxim.normalized_pmi(conditional - 2, null - 2, mask), [1., -.4])
    with pytest.raises(ValueError):
        maxim.normalized_pmi(conditional, null, np.zeros_like(mask))


def test_maxim_sigmoid_and_schedule_exact_reference():
    pred, cons = np.array([-.4, .8]), np.array([-.2, .3])
    expected = 1 / (1 + np.exp(-pred)) - .5 + .25 * (1 / (1 + np.exp(-cons)) - .5)
    assert np.allclose(maxim.shaping_reward(pred, cons), expected)
    assert maxim.cosine_weight(3, hold_until=3, decay_until=7) == 1.
    assert maxim.cosine_weight(5, hold_until=3, decay_until=7) == pytest.approx(.5)
    assert maxim.cosine_weight(7, hold_until=3, decay_until=7) == 0.
    with pytest.raises(ValueError):
        maxim.shaping_reward(pred, cons, consistency_weight=2.)


def test_maxim_return_padding_no_future_leakage():
    task, shape = np.array([[0., 2., np.nan]]), np.array([[1., -1., np.nan]])
    mask = np.array([[True, True, False]])
    result = maxim.discounted_returns(task, shape, mask, gamma=.5, shape_weight=.2)
    assert np.allclose(result, [[1.05, 1.9, 0.]])
    with pytest.raises(ValueError, match="right padding"):
        maxim.discounted_returns(np.zeros((1, 3)), np.zeros((1, 3)), np.array([[True, False, True]]), gamma=.9, shape_weight=1.)


def test_mcpo_exact_clipped_linear_not_bandpass():
    top_two = np.array([[[.95, .01], [.65, .10], [.45, .4]]])
    mask = np.ones((1, 3), dtype=bool)
    for advantage in (2., -2.):
        h = np.clip((1 - (top_two[0, :, 0] - top_two[0, :, 1]) - .1) / .6, 0, 1)
        weights = np.exp(math.log(4) * np.sign(advantage) * h)
        expected = advantage * weights / weights.mean()
        assert np.allclose(mcpo.token_credit(top_two, np.array([advantage]), mask)[0], expected)
    assert h[-1] == 1.  # Highest uncertainty is NOT dropped by a band-pass.
    assert np.allclose(mcpo.token_credit(top_two, np.array([2.]), mask, kappa=0.), 2.)


def test_mcpo_padding_batch_independence_and_validation():
    top_two = np.array([[[.7, .1], [.4, .3], [np.nan, np.nan]], [[.8, .1], [.6, .2], [.5, .4]]])
    mask = np.array([[True, True, False], [True, True, True]])
    together = mcpo.token_credit(top_two, np.array([1., -2.]), mask)
    assert np.allclose(together[0], mcpo.token_credit(top_two[:1], np.array([1.]), mask[:1])[0])
    assert together[0, -1] == 0
    with pytest.raises(ValueError):
        mcpo.token_credit(top_two[..., ::-1], np.array([1., -2.]), mask)


def test_excursion_duration_mixture_and_endpoints():
    ratios = np.array([2., .25, 1.5])
    assert np.all(excursion_td.excursion_weights(ratios, 0.)[np.triu_indices(3)] == 1)
    assert excursion_td.excursion_weights(ratios, 1.)[0, 2] == pytest.approx(np.prod(ratios))
    mixed = excursion_td.excursion_weights(ratios, .5)[0, 2]
    assert mixed == pytest.approx(.5 + .25 * 2 + .125 * 2 * .25 + .125 * 2 * .25 * 1.5)
    assert mixed != pytest.approx(np.prod(.5 + .5 * ratios))


def test_ex_retrace_exact_operator_matches_full_path_enumeration():
    rng = np.random.default_rng(11)
    p = rng.dirichlet(np.ones(2), size=(2, 2))
    pi, mu = rng.dirichlet(np.ones(2), size=2), rng.dirichlet(np.ones(2), size=2)
    reward, q = rng.normal(size=(2, 2)), rng.normal(size=(2, 2))
    offset, matrix = excursion_td.expected_operator(p, reward, pi, mu, horizon=2, gamma=.8, trace_lambda=.7, beta=.4, rho_bar=.9)
    expected = np.zeros((2, 2))
    for s0, a0, s1, a1, s2 in itertools.product(range(2), repeat=5):
        probability = p[s0, a0, s1] * mu[s1, a1] * p[s1, a1, s2]
        target = excursion_td.ex_retrace_targets(q, np.array([s0, s1, s2]), np.array([a0, a1]), np.array([reward[s0, a0], reward[s1, a1]]), pi, mu, gamma=.8, trace_lambda=.7, beta=.4, rho_bar=.9)[0]
        expected[s0, a0] += probability * target
    assert np.allclose(expected.ravel(), offset + matrix @ q.ravel(), atol=1e-12)


def test_ex_retrace_beta_zero_sample_is_behavior_n_step_in_expectation():
    q = np.array([[1., 3.]])
    pi, mu = np.array([[.9, .1]]), np.array([[.2, .8]])
    result = excursion_td.ex_retrace_targets(q, np.array([0, 0]), np.array([0]), np.array([2.]), pi, mu, gamma=.9, beta=0.)
    assert result[0] == pytest.approx(2 + .9 * 2.6)
    with pytest.raises(ValueError):
        excursion_td.excursion_weights(np.array([-1.]), .5)


def test_drd_modes_and_single_coefficients():
    assert torch.equal(drd_mopd.route_matrix(4, "other", 1), 1 - torch.eye(4, dtype=torch.float64))
    route = drd_mopd.route_matrix(4, "single_component", 6)
    assert torch.count_nonzero(route[:, [0, 2, 3]]) == 0
    assert route[:, 1].tolist() == [1 / 3, 1., 1 / 3, 1 / 3]
    with pytest.raises(ValueError):
        drd_mopd.route_matrix(1, "own", 1)
    with pytest.raises(ValueError):
        drd_mopd.route_matrix(3, "alternate", 0)


def test_drd_matches_independent_torch_adamw_and_retains_inactive_state():
    router = drd_mopd.DeltaAdamW(torch.tensor([2., -1.], dtype=torch.float64), 3, learning_rate=.03, weight_decay=.1, max_grad_norm=.4)
    parameters = [torch.nn.Parameter(torch.zeros(2, dtype=torch.float64)) for _ in range(3)]
    optimizers = [torch.optim.AdamW([p], lr=.03, weight_decay=.1) for p in parameters]
    grads = torch.tensor([[1., 2.], [-.5, 1.], [3., -.2]], dtype=torch.float64)
    for step, mode in enumerate(["own", "single_component", "other", "single_component"], start=1):
        route = drd_mopd.route_matrix(3, mode, step)
        routed = route.T @ grads
        before = router.deltas.clone(), router.first.clone(), router.second.clone(), router.steps.clone()
        selected = router.step(grads, mode=mode, rollout_step=step)
        for j in range(3):
            if selected[j]:
                g = routed[j] * min(1., .4 / (float(routed[j].norm()) + 1e-12))
                parameters[j].grad = g
                optimizers[j].step()
            else:
                for old, new in zip(before, (router.deltas, router.first, router.second, router.steps)):
                    assert torch.equal(old[j], new[j])
            assert torch.allclose(router.deltas[j], parameters[j], atol=1e-14)


def test_drd_step_losses_uses_single_composite_before_all_updates():
    router = drd_mopd.DeltaAdamW(torch.zeros(2, dtype=torch.float64), 2, learning_rate=.05, max_grad_norm=None)
    seen = []
    def loss(weight):
        seen.append(weight.detach().clone())
        return (weight - 1).square().sum()
    router.step_losses([loss, loss], mode="own", rollout_step=1)
    assert torch.equal(seen[0], seen[1])
    assert torch.equal(router.base, torch.zeros_like(router.base))
    assert torch.allclose(router.composed(), router.deltas.sum(0))
