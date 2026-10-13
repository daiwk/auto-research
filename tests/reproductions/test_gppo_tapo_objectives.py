import math

import pytest
import torch

from auto_research.reproductions.gppo_framework.objective import estimated_divergence, gppo_loss, proximal_bounds
from auto_research.reproductions.tapo_trajectory.objective import length_aware_clipping, tapo_loss, trajectory_ratio


@pytest.mark.parametrize("geometry", ["tv", "chi2", "hellinger", "kl"])
@pytest.mark.parametrize("topology", ["mc", "atomic", "binary"])
def test_twelve_proximal_regions_really_follow_the_estimator(geometry, topology):
    probability = torch.tensor([.1, .5, .9], dtype=torch.float64)
    low, high = proximal_bounds(probability.log(), geometry=geometry, topology=topology, delta=.02)
    assert (low < 1).all() and (high > 1).all()
    assert (probability * high <= 1).all()
    assert (estimated_divergence(low, probability, geometry=geometry, topology=topology) <= .02000001).all()
    assert (estimated_divergence(high, probability, geometry=geometry, topology=topology) <= .02000001).all()


def test_paper_ppo_dppo_ripo_mappings_are_distinct_and_probability_aware():
    log_mu = torch.tensor([.01, .5], dtype=torch.float64).log()
    lower, upper = proximal_bounds(log_mu, geometry="tv", topology="mc", delta=.1)
    assert torch.allclose(lower, torch.full_like(lower, .8))
    assert torch.allclose(upper, torch.full_like(upper, 1.2))
    lower, upper = proximal_bounds(log_mu, geometry="tv", topology="binary", delta=.01)
    assert torch.allclose(upper, 1 + .01 / log_mu.exp())
    lower, upper = proximal_bounds(log_mu, geometry="chi2", topology="atomic", delta=.01)
    assert torch.allclose(upper, 1 + (.01 / log_mu.exp()).sqrt())
    assert upper[0] > upper[1]


def test_atomic_region_is_accurate_for_rare_llm_tokens_not_lost_to_linear_bisection():
    log_mu = torch.tensor([-60.], dtype=torch.float64)
    _, upper = proximal_bounds(log_mu, geometry="chi2", topology="atomic", delta=.04)
    assert torch.allclose(upper, 1 + (.04 / log_mu.exp()).sqrt(), rtol=1e-10)


def test_rounded_deterministic_token_has_a_finite_complement_limit():
    low, high = proximal_bounds(torch.tensor([0.]), geometry="kl", topology="binary", delta=.01)
    assert torch.isfinite(low).all() and torch.isfinite(high).all()
    assert high <= 1.000001


def test_raw_kl_and_two_sided_log_are_not_silently_equated():
    log_mu = torch.tensor([math.log(.1)], dtype=torch.float64)
    raw_low, raw_high = proximal_bounds(log_mu, geometry="kl", topology="mc", delta=.23)
    two_low, two_high = proximal_bounds(log_mu, geometry="two_sided_log", topology="mc", delta=.23)
    assert torch.allclose(raw_low, two_low)
    assert raw_high > 9.99
    assert torch.allclose(two_high, torch.tensor([math.exp(.23)], dtype=torch.float64))
    with pytest.raises(ValueError, match="only"):
        proximal_bounds(log_mu, geometry="two_sided_log", topology="atomic")


def test_tapo_forward_and_local_only_gradient_match_equation_15():
    log_current = torch.tensor([[.2, -.1, .3]], dtype=torch.float64, requires_grad=True)
    log_behavior = torch.zeros_like(log_current)
    mask = torch.ones_like(log_current, dtype=torch.bool)
    ratio = trajectory_ratio(log_current, log_behavior, mask)
    expected = torch.tensor([[math.exp(.2), math.exp(.05), math.exp(.4 / 3)]], dtype=torch.float64)
    assert torch.allclose(ratio, expected)
    ratio[0, 2].backward()
    assert log_current.grad[0, 0] == log_current.grad[0, 1] == 0
    assert torch.allclose(log_current.grad[0, 2], expected[0, 2])


def test_tapo_prompt_padding_is_not_counted_as_trajectory():
    mask = torch.tensor([[False, False, True, True, True]])
    low, high = length_aware_clipping(mask, horizon=3)
    assert low[0, 2] == pytest.approx(.8)
    assert high[0, 2] == pytest.approx(1.2)
    assert low[0, -1] == pytest.approx(.9997)
    assert high[0, -1] == pytest.approx(1.0004)
    ratio = trajectory_ratio(torch.tensor([[100., 200., .1, .2, .3]]), torch.zeros((1, 5)), mask)
    assert ratio[0, -1] == pytest.approx(math.exp(.2))


def test_proximal_losses_update_inside_and_stop_clipped_gradient():
    old = torch.full((2, 4), math.log(.2))
    current = old.clone().requires_grad_()
    mask = torch.ones_like(current, dtype=torch.bool)
    advantages = torch.tensor([1., -1.])
    loss, _ = gppo_loss(current, old, advantages, mask)
    loss.backward()
    assert current.grad.abs().sum() > 0
    current = (old + .5).requires_grad_()
    loss, _ = tapo_loss(current, old, torch.ones(2), mask, horizon=4)
    loss.backward()
    assert current.grad.abs().sum() == 0
