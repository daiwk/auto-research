import pytest
import torch

from auto_research.post_training.rap_walk import (
    power_temper, rap_walk_advantages, rap_walk_grpo_loss,
)


def graph():
    return torch.tensor([[.5, .9, .2, .7], [.1, .5, .8, .7],
                         [.8, .2, .5, .6], [.3, .3, .4, .5]], dtype=torch.float64)


def test_transitive_direction_gives_winner_more_credit():
    w = torch.tensor([[.5, .8, .9], [.2, .5, .8], [.1, .2, .5]])
    advantage, audit = rap_walk_advantages(w)
    assert advantage[0] > advantage[1] > advantage[2]
    assert audit["stationary"][0] > audit["stationary"][2]
    assert audit["stationary_residual"] < 1e-9
    assert torch.allclose(audit["transition"].sum(-1), torch.ones(3, dtype=torch.float64))
    assert torch.equal(audit["transition"].diagonal(), torch.zeros(3, dtype=torch.float64))


def test_cycles_clarity_stationary_tempering_and_final_normalization():
    advantage, audit = rap_walk_advantages(graph(), entropy_floor=.95)
    assert audit["cyclicity"].max() > 0
    assert audit["normalized_entropy"] >= .95 - 1e-10
    assert abs(float(audit["graph_proposal"].sum())) < 1e-12
    assert abs(float(advantage.mean())) < 1e-10
    assert abs(float(advantage.square().mean()) - 1.) < 1e-6
    assert .1 <= audit["mixing_coefficient"] <= .5


def test_permutation_equivariance_and_ties_are_zero():
    permutation = torch.tensor([3, 1, 0, 2])
    a, _ = rap_walk_advantages(graph())
    b, _ = rap_walk_advantages(graph()[permutation][:, permutation])
    assert torch.allclose(b, a[permutation], atol=1e-7)
    ties, audit = rap_walk_advantages(torch.full((4, 4), .5))
    assert torch.equal(ties, torch.zeros_like(ties))
    assert audit["normalized_entropy"] == pytest.approx(1.)


def test_entropy_calibration_selects_largest_feasible_power():
    p = torch.tensor([.999, .0005, .0005], dtype=torch.float64)
    q, exponent = power_temper(p, .9)
    assert 0 < exponent < 1
    assert float(-(q * q.log()).sum() / torch.log(torch.tensor(3.))) >= .9 - 1e-7
    no_change, one = power_temper(torch.ones(3) / 3., .8)
    assert one == 1.
    assert torch.allclose(no_change, torch.ones(3) / 3.)


def test_graph_aggregator_rejects_noncomplementary_and_nonsquare_input():
    with pytest.raises(ValueError):
        rap_walk_advantages(torch.ones(3, 4))
    with pytest.raises(ValueError, match="sum to one"):
        rap_walk_advantages(torch.full((3, 3), .7))
    with pytest.raises(RuntimeError, match="did not converge"):
        rap_walk_advantages(graph(), max_iterations=1)


def test_actual_grpo_loss_gradient_is_not_a_video_capability_claim():
    logits = torch.nn.Parameter(torch.randn(4, 3))
    labels = torch.zeros(4, 2, dtype=torch.long)
    old = logits.detach().log_softmax(-1).gather(-1, labels)
    current = logits.log_softmax(-1).gather(-1, labels)
    pairwise = graph().requires_grad_()
    teacher = old.clone().requires_grad_()
    loss, _ = rap_walk_grpo_loss(current, old, torch.ones_like(current, dtype=torch.bool),
                                pairwise, reference_log_probs=teacher, kl_beta=.01)
    loss.backward()
    assert torch.isfinite(logits.grad).all() and logits.grad.abs().sum() > 0
    assert pairwise.grad is None
    assert teacher.grad is None


def test_rollout_mask_and_group_must_match():
    logp = torch.zeros(4, 2)
    with pytest.raises(ValueError):
        rap_walk_grpo_loss(logp, logp, torch.zeros_like(logp, dtype=torch.bool), graph())
    with pytest.raises(ValueError):
        rap_walk_grpo_loss(logp[:3], logp[:3], torch.ones_like(logp[:3], dtype=torch.bool), graph())
