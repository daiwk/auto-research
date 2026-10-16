"""Numerical contracts, gradients, masks and frozen-role guards for six components."""
from copy import deepcopy
from dataclasses import replace
import math

import pytest
import torch
from torch import nn

from auto_research.post_training import cce_opd, ggpo, sif, stopd, tf_opd, waypoint_opd


def test_tf_closed_form_is_weighted_average_not_task_arithmetic_and_stationary():
    base = torch.zeros(2, 2, dtype=torch.double)
    teachers = [torch.tensor([[1., 2.], [3., 4.]], dtype=torch.double),
                torch.tensor([[3., -2.], [0., 5.]], dtype=torch.double)]
    gram = torch.tensor([[2., .3], [.3, 1.]], dtype=torch.double)
    fused, info = tf_opd.solve_layer(base, teachers, [gram, gram], weights=[1., 3.])
    torch.testing.assert_close(fused.double(), (teachers[0] + 3 * teachers[1]) / 4)
    assert info["normal_equation_residual_l2"] < 1e-12
    trial = fused.double().requires_grad_()
    shrunk = .9 * gram + .1 * torch.diag_embed(gram.diagonal())
    objective = sum(w * torch.sum(((trial - t) @ shrunk) * (trial - t))
                    for w, t in zip([1., 3.], teachers, strict=True))
    assert torch.autograd.grad(objective, trial)[0].abs().max() < 1e-6


def test_tf_orthogonal_gram_and_unreproduced_share():
    base = torch.zeros(1, 2)
    teachers = [torch.tensor([[2., 7.]]), torch.tensor([[9., 3.]])]
    grams = [torch.diag(torch.tensor([1., 0.])), torch.diag(torch.tensor([0., 1.]))]
    fused, info = tf_opd.solve_layer(base, teachers, grams, alpha=1.)
    torch.testing.assert_close(fused, torch.tensor([[2., 3.]]))
    assert info["unreproduced_share"] == [0., 0.]
    with pytest.raises(ValueError, match="positive semidefinite"):
        tf_opd.solve_layer(base, teachers[:1], [-torch.eye(2)])


class TransitionTeacher(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(3, 3)
        self.head = nn.Linear(3, 3, bias=False)
        with torch.no_grad():
            self.embedding.weight.copy_(torch.eye(3))
            self.head.weight.copy_(torch.tensor([[-100., -100., -100.], [100., -100., -100.], [-100., 100., 100.]]))

    def forward(self, ids):
        return self.head(self.embedding(ids))


def test_tf_actual_teacher_generation_filter_replay_and_hook_cleanup():
    teacher = TransitionTeacher().train()
    rollout = tf_opd.sample_teacher_rollout(teacher, torch.tensor([[0]]), teacher_id="teacher-A",
        eos_token_id=2, max_new_tokens=5, decode=lambda ids: str(ids))
    assert teacher.training and rollout.terminated and rollout.tokens.tolist() == [[0, 1, 2]]
    rejected = replace(rollout, terminated=False)
    looping = replace(rollout, response_text="repeat " * 3000)
    assert not tf_opd.retain_rollout(rejected) and not tf_opd.retain_rollout(looping)
    assert not tf_opd.retain_rollout(rollout, require_correct=True)
    grams, audit = tf_opd.collect_teacher_grams(teacher, [rollout, rejected, looping], teacher_id="teacher-A")
    torch.testing.assert_close(grams["head"], torch.eye(3) / 3)
    assert audit["kept_rollouts"] == 1 and audit["layer_token_counts"]["head"] == 3
    assert not teacher.head._forward_pre_hooks
    assert all(p.grad is None for p in teacher.parameters())
    with pytest.raises(ValueError, match="own rollouts"):
        tf_opd.collect_teacher_grams(teacher, [rollout], teacher_id="wrong-teacher")
    assert not teacher.head._forward_pre_hooks


def test_waypoint_gate_centering_fallback_batch_mask_and_local_gradient():
    old = torch.zeros(1, 3, 3, dtype=torch.double)
    initial = old.clone().requires_grad_()
    middle = torch.tensor([[[1., -1., 0.], [2., -2., 0.], [0., 0., 0.]]], dtype=torch.double, requires_grad=True)
    final = torch.tensor([[[2., -2., 0.], [1., -1., 0.], [1., -1., 0.]]], dtype=torch.double, requires_grad=True)
    tokens = torch.zeros(1, 3, dtype=torch.long)
    mask = torch.tensor([[True, True, True]])
    reference = old.log_softmax(-1)[..., 0].requires_grad_()
    credit = waypoint_opd.prepare_credit(old, initial, middle, final, tokens, reference, mask, top_k=3)
    torch.testing.assert_close(credit.gate, torch.tensor([[1., 0., 1.]], dtype=torch.double))
    torch.testing.assert_close(credit.advantages.sum(-1), torch.zeros(1, 3, dtype=torch.double), atol=1e-12, rtol=0)
    current = old.clone().requires_grad_()
    loss, _ = waypoint_opd.waypoint_ppo_loss(current, tokens, credit, kl_coefficient=0)
    grad = torch.autograd.grad(loss, current)[0]
    expected = torch.zeros_like(current).scatter_(-1, credit.candidates, -credit.advantages / 3)
    torch.testing.assert_close(grad, expected, atol=1e-12, rtol=1e-10)
    assert all(x.grad is None for x in (initial, middle, final, reference))
    shifted = waypoint_opd.prepare_credit(old, initial + 300, middle - 50, final + 40, tokens,
        reference, torch.tensor([[True, True, False]]), top_k=3)
    assert shifted.gate[0, 2] == 0 and shifted.scale == 1.5
    with pytest.raises(ValueError, match="share one"):
        waypoint_opd.validate_snapshot_lineage([{"run_id": "a", "step": 0}, {"run_id": "b", "step": 1}, {"run_id": "a", "step": 2}])


def test_waypoint_dense_credit_updates_unsampled_candidates_and_clips():
    old = torch.zeros(1, 1, 4)
    initial = old.clone()
    middle = torch.tensor([[[2., 1., -1., -2.]]])
    final = 2 * middle
    ids = torch.zeros(1, 1, dtype=torch.long)
    credit = waypoint_opd.prepare_credit(old, initial, middle, final, ids,
        old.log_softmax(-1)[..., 0], torch.ones(1, 1, dtype=torch.bool), top_k=4)
    current = nn.Parameter(old.clone())
    optimizer = torch.optim.SGD([current], lr=.1)
    loss, _ = waypoint_opd.waypoint_ppo_loss(current, ids, credit, kl_coefficient=0)
    loss.backward()
    assert current.grad[0, 0, 1] != 0  # not the sampled token
    optimizer.step()
    assert current[0, 0, 1] > 0 and current[0, 0, 3] < 0


def test_ggpo_raw_value_gradient_translation_invariance_and_mask():
    current = torch.tensor([[[-1., -2., 77.], [-3., -4., 88.], [-1., -3., 99.]]], dtype=torch.double, requires_grad=True)
    reference = current.detach().clone().requires_grad_()
    rewards = torch.tensor([[0., 1., 0.]], dtype=torch.double, requires_grad=True)
    mask = torch.tensor([[[True, True, False]] * 3])
    beta = .5
    loss, _ = ggpo.ggpo_loss(current, reference, rewards, mask, beta=beta, normalize=False)
    expected_value = beta * (torch.logsumexp(rewards.detach() / beta, -1) - math.log(3)) - rewards.detach().mean(-1)
    torch.testing.assert_close(loss, expected_value.squeeze())
    grad = torch.autograd.grad(loss, current)[0]
    coefficients = -beta * ((rewards.detach() / beta).softmax(-1) - 1 / 3)
    torch.testing.assert_close(grad, coefficients.unsqueeze(-1).expand_as(current).masked_fill(~mask, 0))
    shifted, _ = ggpo.ggpo_loss(current, reference, rewards + 1e6, mask, beta=beta, mixed_only=False, normalize=False)
    torch.testing.assert_close(shifted, loss)
    assert reference.grad is None and rewards.grad is None


def test_ggpo_clipped_branch_retains_saturated_token_gradient_and_refresh_roles():
    current = torch.tensor([[[4., 0.], [-4., 0.]]], dtype=torch.double, requires_grad=True)
    reference = torch.zeros_like(current, requires_grad=True)
    rewards = torch.tensor([[0., 1.]], dtype=torch.double)
    mask = torch.ones_like(current, dtype=torch.bool)
    clipped, _ = ggpo.clipped_coefficient_surrogate(current, reference, rewards, mask, beta=.5)
    gradient = torch.autograd.grad(clipped, current)[0]
    assert gradient[0, 0, 0] != 0 and gradient[0, 1, 0] != 0
    learner = nn.Linear(2, 2)
    policies = ggpo.GGPOPolicies.from_learner(learner, refresh_interval=2)
    original_behavior = deepcopy(policies.behavior.state_dict())
    with torch.no_grad():
        learner.weight.add_(1.)
    assert not policies.after_optimizer_step(learner)
    assert policies.after_optimizer_step(learner)
    torch.testing.assert_close(policies.reference.weight, learner.weight)
    torch.testing.assert_close(policies.behavior.weight, original_behavior["weight"])
    policies.sync_behavior(learner)
    torch.testing.assert_close(policies.behavior.weight, learner.weight)
    assert all(not p.requires_grad for p in policies.reference.parameters())


def test_stopd_exact_inclusion_and_expected_gradient_including_natural_eos():
    length, width, natural_length = 10, 4, 9
    probability = stopd.inclusion_probabilities(length, width)
    torch.testing.assert_close(probability, torch.tensor([1.] * 4 + [.6] * 4 + [.2] * 2, dtype=torch.double))
    anchors = torch.arange(length)
    cutoffs = stopd.cutoffs_from_anchors(anchors, length, width)
    empirical = (cutoffs[:, None] >= torch.arange(1, length + 1)).double().mean(0)
    torch.testing.assert_close(empirical, probability)
    parameter = torch.tensor(.7, dtype=torch.double, requires_grad=True)
    factors = torch.arange(1, natural_length + 1, dtype=torch.double)
    losses = (parameter - factors).square()
    full_gradient = torch.autograd.grad(losses.sum(), parameter, retain_graph=True)[0]
    expected_gradient = 0.
    for cutoff in cutoffs:
        retained = min(int(cutoff), natural_length)  # position 9 is the actual EOS
        weighted = (losses[:retained] / probability[:retained]).sum()
        expected_gradient += torch.autograd.grad(weighted, parameter, retain_graph=True)[0] / length
    torch.testing.assert_close(expected_gradient, full_gradient)
    assert empirical[natural_length - 1] > 0


def test_stopd_plan_before_generation_warmup_and_previous_batch_denominator():
    schedule = stopd.STOPDSchedule(10, 4)
    warmup = schedule.begin_batch(1)
    with pytest.raises(ValueError, match="completed"):
        schedule.begin_batch(1)
    warmup_mask = torch.tensor([[True] * 3 + [False] * 7])
    _, info = schedule.loss(warmup, torch.ones(1, 10), warmup_mask)
    assert info["denominator"] == 3 and warmup.warmup
    schedule.finish_batch(warmup, warmup_mask)
    plan = schedule.begin_batch(1, generator=torch.Generator().manual_seed(3))
    mask = torch.arange(10)[None, :] < plan.cutoffs[:, None]
    value, info = schedule.loss(plan, torch.ones(1, 10), mask)
    assert info["denominator"] == 3 and info["normalizer_source"] == "previous_batch"
    assert value == pytest.approx(info["weighted_count_for_next_batch"] / 3)
    schedule.finish_batch(plan, mask)
    next_plan = schedule.begin_batch(1, generator=torch.Generator().manual_seed(3))
    assert next_plan.denominator == info["weighted_count_for_next_batch"]
    with pytest.raises(ValueError, match="cutoff"):
        schedule.loss(next_plan, torch.ones(1, 10), torch.ones(1, 10, dtype=torch.bool))


def test_stopd_local_reverse_kl_frozen_teacher():
    student = torch.randn(2, 3, 4, requires_grad=True)
    teacher = torch.randn(2, 3, 4, requires_grad=True)
    stopd.reverse_kl_token_losses(student, teacher).sum().backward()
    assert student.grad.abs().sum() > 0 and teacher.grad is None


def test_cce_union_full_vocab_entropy_all_token_denominator_and_frozen_teacher():
    full = torch.tensor([[[2., 1., 0., -1.], [2., 1., 0., -1.]]], dtype=torch.double, requires_grad=True)
    masked = torch.tensor([[[0., 3., 0., -1.], [0., 3., 0., -1.]]], dtype=torch.double, requires_grad=True)
    old = full.detach().clone()
    ids = torch.zeros(1, 2, dtype=torch.long)
    valid = torch.ones(1, 2, dtype=torch.bool)
    credit = cce_opd.prepare_credit(old, full, masked, ids, valid,
        torch.tensor([[True, False]]), top_k=1, entropy_threshold=.1)
    assert credit.support.sum(-1).tolist() == [[2, 2]]
    torch.testing.assert_close(credit.target_probabilities.sum(-1), torch.ones(1, 2, dtype=torch.double))
    expected_entropy = -(full.detach().softmax(-1) * full.detach().log_softmax(-1)).sum(-1)
    torch.testing.assert_close(credit.teacher_entropy, expected_entropy)
    current = old.clone().requires_grad_()
    loss, info = cce_opd.cce_ppo_loss(current, ids, credit)
    grad = torch.autograd.grad(loss, current)[0]
    expected = (current.detach().softmax(-1) - credit.target_probabilities) / 2
    expected[:, 1] = 0
    torch.testing.assert_close(grad, expected)
    assert grad[0, 0, 3] > 0  # outside support still receives full-softmax gradient
    assert info["valid_tokens"] == 2 and info["auxiliary_tokens"] == 1
    assert full.grad is None and masked.grad is None


def test_cce_condition_pair_preserves_exact_same_prefix_and_requires_review():
    question = "Write a positive number. Give one token."
    with pytest.raises(ValueError, match="reviewed"):
        cce_opd.ConditionPair.from_reviewed_span(question, (8, 16), semantic_reviewed=False)
    pair = cce_opd.ConditionPair.from_reviewed_span(question, (8, 16), semantic_reviewed=True)
    prefix = torch.tensor([1, 2, 3])
    calls = []
    def scorer(prompt, generated):
        calls.append((prompt, generated.clone()))
        return torch.ones(3, 4, requires_grad=True)
    views = cce_opd.score_teacher_views(scorer, pair, prefix)
    assert len(calls) == 2 and torch.equal(calls[0][1], calls[1][1])
    assert all(not view.requires_grad for view in views)


def test_sif_default_550_profile_windows_votes_sample_std_and_exclusion():
    certainty = torch.stack([torch.arange(600., 0., -1), torch.arange(599., -1., -1), torch.zeros(600)])
    certainty = certainty.unsqueeze(0).repeat(2, 1, 1)
    certainty[1] = 1  # homogeneous rewards: entire group must be removed
    mask = torch.ones(2, 3, 600, dtype=torch.bool)
    mask[0, 2, 549:] = False  # below default eligibility
    credit = sif.prepare_credit(certainty, mask)
    assert sif.VotingConfig().minimum_length == 550
    assert credit.eligible.tolist() == [[True, True, False], [True, True, True]]
    assert credit.rewards[0].tolist() == [1., 0., 0.]
    assert credit.retained_groups.tolist() == [True, False]
    torch.testing.assert_close(credit.profiles[0, 0, [0, -1]], torch.tensor([550.5, 50.5]))
    torch.testing.assert_close(credit.advantages[0, :2], torch.tensor([1., -1.]) / math.sqrt(2), atol=2e-6, rtol=1e-5)
    assert not credit.update_mask[0, 2].any() and not credit.update_mask[1].any()
    assert not credit.pairwise_votes[0].diagonal().any()


def test_sif_self_certainty_not_entropy_and_policy_kl_both_masked():
    logits = torch.tensor([[1., 2., 3.]], dtype=torch.double)
    expected = torch.nn.functional.kl_div(logits.log_softmax(-1), torch.full_like(logits, 1 / 3), reduction="sum")
    torch.testing.assert_close(sif.token_self_certainty(logits).squeeze(), expected)
    config = sif.VotingConfig(windows=2, width=2, minimum_stride=1, window_wins=2)
    certainty = torch.tensor([[[3., 3., 3.], [2., 2., 2.], [1., 1., 1.]], [[1., 1., 1.]] * 3])
    mask = torch.ones_like(certainty, dtype=torch.bool)
    mask[0, 2, -1] = False
    credit = sif.prepare_credit(certainty, mask, config=config)
    current = torch.zeros_like(certainty, requires_grad=True)
    old = torch.zeros_like(current, requires_grad=True)
    reference = torch.full_like(current, -.5, requires_grad=True)
    loss, _ = sif.sif_ppo_loss(current, old, reference, credit, kl_coefficient=1.)
    loss.backward()
    assert current.grad[0, :2].abs().sum() > 0
    assert not current.grad[0, 2].any() and not current.grad[1].any()
    assert old.grad is None and reference.grad is None


def test_ggpo_actual_tiny_categorical_parameter_update_reduces_frozen_group_gap():
    logits = nn.Parameter(torch.zeros(4, dtype=torch.double))
    optimizer = torch.optim.SGD([logits], lr=.5)
    reference = logits.detach().log_softmax(-1)[None, :, None]
    rewards = torch.tensor([[0., 1., 0., 1.]], dtype=torch.double)
    mask = torch.ones(1, 4, 1, dtype=torch.bool)
    initial, _ = ggpo.ggpo_loss(logits.log_softmax(-1)[None, :, None], reference, rewards, mask, beta=.5)
    for _ in range(4):
        optimizer.zero_grad()
        loss, _ = ggpo.ggpo_loss(logits.log_softmax(-1)[None, :, None], reference, rewards, mask, beta=.5)
        loss.backward()
        optimizer.step()
    final, _ = ggpo.ggpo_loss(logits.log_softmax(-1)[None, :, None], reference, rewards, mask, beta=.5)
    assert final < initial and logits[1] > logits[0]


def test_waypoint_invalid_token_has_no_policy_or_kl_gradient():
    old = torch.zeros(1, 2, 3)
    middle = torch.tensor([[[2., -1., 0.], [1., -2., 0.]]])
    ids = torch.zeros(1, 2, dtype=torch.long)
    credit = waypoint_opd.prepare_credit(old, old, middle, 2 * middle, ids,
        torch.full((1, 2), -2.), torch.tensor([[True, False]]), top_k=3)
    current = old.clone().requires_grad_()
    loss, _ = waypoint_opd.waypoint_ppo_loss(current, ids, credit, kl_coefficient=1.)
    gradient = torch.autograd.grad(loss, current)[0]
    assert gradient[0, 0].abs().sum() > 0 and not gradient[0, 1].any()


def test_ggpo_homogeneous_group_filter_and_clipped_unclipped_gradient_equivalence():
    values = torch.randn(2, 3, 4, dtype=torch.double, requires_grad=True)
    mask = torch.ones_like(values, dtype=torch.bool)
    reference = values.detach().clone()
    homogeneous = torch.tensor([[0., 0., 0.], [1., 1., 1.]], dtype=torch.double)
    empty, info = ggpo.ggpo_loss(values, reference, homogeneous, mask)
    assert info["retained_groups"] == 0
    assert not torch.autograd.grad(empty, values, retain_graph=True)[0].any()
    rewards = torch.tensor([[1., 0., 0.], [0., 1., 1.]], dtype=torch.double)
    direct, _ = ggpo.ggpo_loss(values, reference, rewards, mask, beta=.5)
    surrogate, _ = ggpo.clipped_coefficient_surrogate(values, reference, rewards, mask, beta=.5, clipping_radius=1e6)
    a = torch.autograd.grad(direct, values, retain_graph=True)[0]
    b = torch.autograd.grad(surrogate, values)[0]
    torch.testing.assert_close(a, b)
