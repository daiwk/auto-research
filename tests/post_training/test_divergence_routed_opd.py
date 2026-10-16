import pytest
import torch

from auto_research.post_training.divergence_routed_opd import (
    candidate_rewards, prepare_routing, routed_ppo_loss,
)


def test_topk_union_keeps_each_teacher_and_student_token_once():
    p = torch.tensor([[[4., 3., 2., 1.]]])
    q = torch.tensor([[[1., 2., 3., 4.]]], requires_grad=True)
    route = prepare_routing(p, q, torch.ones(1, 1, dtype=torch.bool), top_k=2)
    assert int(route.support.sum()) == 4
    assert set(route.indices[route.support].tolist()) == {0, 1, 2, 3}
    assert torch.allclose(route.old_log_probs.exp().sum(-1), torch.ones(1, 1))
    assert torch.allclose(route.teacher_log_probs.exp().sum(-1), torch.ones(1, 1))
    assert not route.teacher_log_probs.requires_grad
    same = prepare_routing(p, p, torch.ones(1, 1, dtype=torch.bool), top_k=2)
    assert int(same.support.sum()) == 2
    assert torch.allclose(same.js, torch.zeros_like(same.js))


def test_js_gate_uses_valid_batch_positions_and_retains_cutoff_ties():
    p = torch.zeros(1, 5, 2)
    q = torch.tensor([[[0., 0.], [1., 0.], [2., 0.], [3., 0.], [30., -30.]]])
    mask = torch.tensor([[True, True, True, True, False]])
    route = prepare_routing(p, q, mask, top_k=2, fraction=.25)
    assert route.gate.tolist() == [[False, False, False, True, False]]
    tied = prepare_routing(p, p, mask, top_k=2, fraction=.2)
    assert torch.equal(tied.gate, mask)


def test_candidate_reward_matches_paper_and_teacher_is_detached():
    p = torch.tensor([[[0., -4., -5.]]], requires_grad=True)
    q = torch.tensor([[[-4., 0., -5.]]], requires_grad=True)
    route = prepare_routing(p, q, torch.ones(1, 1, dtype=torch.bool), top_k=2, fraction=1.)
    expected = -route.old_log_probs.exp() * torch.where(
        route.support, route.old_log_probs - route.teacher_log_probs, 0.)
    expected += route.teacher_log_probs.exp()
    reward = candidate_rewards(route)
    assert torch.allclose(reward, expected)
    assert not reward.requires_grad
    loss, audit = routed_ppo_loss(p, route)
    loss.backward()
    assert torch.isfinite(p.grad).all()
    assert q.grad is None
    assert audit["response_positions"] == 1


def test_clipped_surrogate_is_not_just_static_kl_and_has_actual_update():
    old = torch.tensor([[[0., -1., -2.], [0., 1., 2.]]])
    teacher = old.flip(-1)
    mask = torch.ones(1, 2, dtype=torch.bool)
    route = prepare_routing(old, teacher, mask, top_k=2)
    logits = torch.nn.Parameter(old.clone())
    optimizer = torch.optim.SGD([logits], lr=.1)
    loss, _ = routed_ppo_loss(logits, route)
    lp = logits.log_softmax(-1)
    # At behavior policy, eq.10 is negative candidate-reward sum, not KL.
    assert torch.allclose(loss, -candidate_rewards(route).sum(-1).mean())
    loss.backward()
    assert logits.grad.abs().sum() > 0
    optimizer.step()
    assert not torch.equal(logits.detach(), old)
    assert lp.shape == logits.shape


def test_invalid_mask_empty_response_and_nonfinite_fail():
    logits = torch.zeros(1, 2, 4)
    with pytest.raises(ValueError, match="valid generated"):
        prepare_routing(logits, logits, torch.zeros(1, 2, dtype=torch.bool), top_k=2)
    with pytest.raises(ValueError):
        prepare_routing(logits, logits, torch.ones(1, 2), top_k=2)
    with pytest.raises(ValueError):
        prepare_routing(logits, logits, torch.ones(1, 2, dtype=torch.bool), top_k=5)


def test_offpolicy_ratios_apply_the_clipped_candidate_surrogate():
    old = torch.zeros(1, 1, 2)
    teacher = torch.tensor([[[-2., 2.]]])
    route = prepare_routing(old, teacher, torch.ones(1, 1, dtype=torch.bool), top_k=2, fraction=1.)
    current = torch.tensor([[[-1., 1.]]], requires_grad=True)
    clipped, _ = routed_ppo_loss(current, route, clip_epsilon=.1)
    wider, _ = routed_ppo_loss(current, route, clip_epsilon=.9)
    candidate_lp = current.gather(-1, route.indices).masked_fill(~route.support, -torch.inf).log_softmax(-1)
    ratio = torch.where(route.support, candidate_lp - route.old_log_probs, 0.).exp()
    advantage = candidate_rewards(route)
    expected = -torch.minimum(ratio * advantage, ratio.clamp(.9, 1.1) * advantage).sum()
    assert torch.allclose(clipped, expected)
    assert clipped > wider


def test_masked_positions_do_not_contribute_to_ppo_loss():
    torch.manual_seed(42)
    old, teacher = torch.randn(2, 4, 8), torch.randn(2, 4, 8)
    mask = torch.tensor([[False, True, True, False], [False, True, False, False]])
    route = prepare_routing(old, teacher, mask, top_k=3)
    current = old.clone().requires_grad_()
    loss, _ = routed_ppo_loss(current, route)
    loss.backward()
    assert torch.equal(current.grad[~mask], torch.zeros_like(current.grad[~mask]))


def test_appendix_kth_largest_rule_routes_six_of_32_valid_positions():
    old = torch.zeros(1, 40, 2)
    teacher = torch.zeros_like(old)
    teacher[0, :32, 0] = torch.linspace(.01, 4., 32)
    teacher[0, 32:, 0] = 100.  # Invalid positions must not affect count or cutoff.
    mask = torch.arange(40).unsqueeze(0) < 32
    route = prepare_routing(old, teacher, mask, top_k=2, fraction=.2)
    assert int(route.gate.sum()) == 6  # round(.2 * 32), not interpolated quantile's 7.
    assert route.gate[0, :26].tolist() == [False] * 26
    assert route.gate[0, 26:32].tolist() == [True] * 6
    assert not route.gate[~mask].any()


def test_single_valid_position_has_k_zero_unless_fraction_is_explicitly_one():
    old = torch.zeros(1, 1, 2)
    teacher = torch.tensor([[[0., 2.]]])
    mask = torch.ones(1, 1, dtype=torch.bool)
    no_route = prepare_routing(old, teacher, mask, top_k=2)
    assert not no_route.gate.any()
    difference = torch.where(no_route.support,
                             no_route.old_log_probs - no_route.teacher_log_probs, 0.)
    assert torch.allclose(candidate_rewards(no_route), -no_route.old_log_probs.exp() * difference)
    routed = prepare_routing(old, teacher, mask, top_k=2, fraction=1.)
    assert routed.gate.all()


def test_kth_largest_cutoff_keeps_equal_scores_even_when_count_exceeds_k():
    old = torch.zeros(1, 32, 2)
    teacher = torch.ones_like(old)
    route = prepare_routing(old, teacher, torch.ones(1, 32, dtype=torch.bool), top_k=2)
    assert route.gate.all()  # K=6, all 32 positions share the actual Kth score.
