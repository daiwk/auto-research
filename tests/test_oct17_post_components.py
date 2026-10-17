"""Exact formula/reference, masked gradients and workflow guards, not capability."""
import itertools
import random

import pytest
import torch
from torch import nn

from auto_research.post_training import clean_rm, elite_replay, progress_reward
from auto_research.post_training import shared_residual_distillation as srd


def test_srd_groups_are_disjoint_and_controls_are_other_problems():
    ids = ["a"] * 4 + ["b"] * 5
    groups = srd.split_peers(ids, seed=4)
    assert len(groups) == 5 and groups == srd.split_peers(ids, seed=4)
    for group in groups:
        assert group.target not in group.peers and len(set(group.peers)) == 2
        assert all(ids[p] == ids[group.target] for p in group.peers)
        assert ids[group.control] != ids[group.target]
    with pytest.raises(ValueError, match="two problems"):
        srd.split_peers(["a"] * 4)
    with pytest.raises(ValueError, match="K > M"):
        srd.split_peers(["a"] * 2 + ["b"] * 4)


def test_srd_center_minmod_target_matches_scalar_reference_and_detaches():
    base = torch.tensor([[.8, .2, -.4]], dtype=torch.float64, requires_grad=True)
    control = torch.tensor([[-.1, .2, .7]], dtype=torch.float64, requires_grad=True)
    peers = torch.tensor([[[2., .3, -1.]], [[1., .6, -.2]]], dtype=torch.float64, requires_grad=True)
    target, details = srd.shared_residual_target(base, control, peers)
    q0, qc = base.detach().softmax(-1)[0], control.detach().softmax(-1)[0]
    residuals = []
    for peer in peers.detach()[:, 0]:
        d = peer.log_softmax(-1) - qc.log()
        residuals.append(d - sum(q0[i] * d[i] for i in range(3)))
    retained = torch.tensor([min(float(d[i]) for d in residuals) if all(d[i] > 0 for d in residuals)
        else max(float(d[i]) for d in residuals) if all(d[i] < 0 for d in residuals) else 0. for i in range(3)], dtype=torch.float64)
    torch.testing.assert_close(target[0], (q0.log() + retained).softmax(-1))
    torch.testing.assert_close((details["centered_residuals"] * q0).sum(-1), torch.zeros(2, 1, dtype=torch.float64), atol=1e-14, rtol=0)
    assert not target.requires_grad and all(x.grad is None for x in (base, control, peers))
    reversed_peer = control.detach()[None].expand(2, -1, -1).clone()
    unchanged, _ = srd.shared_residual_target(base, control, reversed_peer)
    torch.testing.assert_close(unchanged, base.detach().softmax(-1))


def test_srd_coordinate_clipping_signed_terms_and_full_kl_limit():
    student = torch.tensor([[0., 0.]], dtype=torch.float64, requires_grad=True)
    teacher = torch.tensor([[.9, .1]], dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([True])
    terms = teacher.detach() * (teacher.detach().log() - student.log_softmax(-1))
    clipped = srd.clipped_distillation_loss(student, teacher, mask, coordinate_cap=.01)
    torch.testing.assert_close(clipped, terms.clamp_max(.01).sum())
    assert clipped < 0  # clipping the positive coordinate may yield negative total
    full = srd.clipped_distillation_loss(student, teacher, mask, coordinate_cap=100)
    torch.testing.assert_close(full, terms.sum())
    clipped.backward()
    assert teacher.grad is None and torch.isfinite(student.grad).all()


def test_srd_invalid_padding_never_enters_softmax_and_has_zero_gradient():
    logits = torch.tensor([[[.2, -.2], [float("nan"), float("inf")]]], requires_grad=True)
    teacher = torch.tensor([[[.7, .3], [float("nan"), float("nan")]]])
    mask = torch.tensor([[True, False]])
    loss = srd.clipped_distillation_loss(logits, teacher, mask, coordinate_cap=100)
    loss.backward()
    assert torch.isfinite(logits.grad).all() and torch.equal(logits.grad[:, 1], torch.zeros(1, 2))
    with pytest.raises(ValueError, match="sum to one"):
        srd.clipped_distillation_loss(logits, torch.ones_like(logits), mask)


def _plan():
    return progress_reward.ProgressPlan(("approach", "grasp", "place"),
        (lambda s: s[:, 0] >= .3, lambda s: s[:, 0] >= .6, lambda s: s[:, 0] >= .9), lambda s: s[:, 0])


def test_progress_current_state_stage_can_regress_and_selects_embedding():
    states = torch.tensor([[.1], [.4], [.8], [1.], [.1]])
    plan = _plan()
    assert plan.stage(states).tolist() == [0, 1, 2, 2, 0]
    embeddings = torch.tensor([[1., 2.], [3., 4.], [5., 6.]])
    result = progress_reward.augment_state(states, plan, embeddings)
    torch.testing.assert_close(result[:, :1], states)
    torch.testing.assert_close(result[:, 1:], embeddings[[0, 1, 2, 2, 0]])
    with pytest.raises(ValueError, match="one fixed-size"):
        progress_reward.augment_state(states, plan, embeddings[:2])


def test_progress_literal_formula_terminal_boundary_and_telescoping():
    phi = torch.tensor([.2, .4, .9, 1.], dtype=torch.float64)
    success = torch.tensor([False, False, True])
    result = progress_reward.progress_reward(phi[:-1], phi[1:], success, gamma=.8, bonus=2)
    torch.testing.assert_close(result, .8 * phi[1:] - phi[:-1] + 2 * success)
    episodic = progress_reward.progress_reward(phi[:-1], phi[1:], success, gamma=.8, bonus=0, terminated=success)
    torch.testing.assert_close(sum(.8 ** i * episodic[i] for i in range(3)), -phi[0])
    # A time-limit cutoff is not a true terminal and must retain its potential.
    truncated = progress_reward.progress_reward(phi[:-1], phi[1:], success, gamma=.8, bonus=0,
        terminated=torch.zeros(3, dtype=torch.bool))
    torch.testing.assert_close(sum(.8 ** i * truncated[i] for i in range(3)), -phi[0] + .8 ** 3 * phi[-1])


def _elite(question="a", solution="correct", tokens=(1, 2), approach="one", structure=(0,)):
    return elite_replay.Elite(question, solution, tokens, approach, structure)


def test_elite_archive_verifies_realized_cells_shortest_quality_and_freeze():
    archive = elite_replay.EliteArchive({"a": ("one", "two")})
    verifier = lambda q, text: text.startswith("correct")
    assert not archive.insert(_elite(solution="wrong"), verifier)
    assert archive.insert(_elite(tokens=(1, 2, 3)), verifier)
    assert not archive.insert(_elite(solution="correct tie", tokens=(4, 5, 6)), verifier)
    assert archive.insert(_elite(solution="correct shorter", tokens=(1,)), verifier)
    assert archive.cells["a"][("one", 0)].solution == "correct shorter"
    target, parent = archive.choose_target("a", random.Random(1))
    assert target == "two" and parent.approach == "one"
    # Candidate realizes approach one despite target two: it belongs to one.
    assert archive.insert(_elite(solution="correct new structure", structure=(1,)), verifier)
    archive.freeze()
    with pytest.raises(RuntimeError, match="frozen"):
        archive.insert(_elite(), verifier)


def test_elite_directed_search_balances_attempts_and_restores_frozen_model():
    archive = elite_replay.EliteArchive({"a": ("one", "two"), "b": ("one", "two")})
    verifier = lambda q, text: text == "correct"
    for q in ("a", "b"):
        archive.insert(_elite(question=q), verifier)
    base = nn.Linear(1, 1).train()
    original = base.weight.detach().clone()
    requested = []
    def generate(model, question, target, parent):
        assert not model.training and not torch.is_grad_enabled()
        assert parent is not None
        requested.append(target)
        return _elite(question=question, approach=target)
    audit = elite_replay.map_elites_search(base, archive, generate=generate, verify=verifier,
        mutations_per_question=5, seed=5)
    assert requested[0] == "two" and audit["occupied_cells"] == 4 and audit["mutation_attempts"] == 10
    assert base.training and base.weight.grad is None and torch.equal(base.weight, original)
    archive.freeze()
    samples = archive.sample_balanced(40)
    assert sum(s.question == "a" for s in samples) == 20
    assert sum(s.question == "a" and s.approach == "one" for s in samples) == 10


def test_elite_sampler_does_not_overweight_questions_with_more_cells():
    archive = elite_replay.EliteArchive({"a": ("one",), "b": ("one", "two", "three")})
    for q, approaches in archive.applicable.items():
        for approach in approaches:
            archive.insert(_elite(question=q, approach=approach), lambda q, s: True)
    archive.freeze()
    samples = archive.sample_balanced(60)
    assert sum(s.question == "a" for s in samples) == sum(s.question == "b" for s in samples) == 30
    assert [sum(s.question == "b" and s.approach == a for s in samples) for a in ("one", "two", "three")] == [10] * 3


def test_elite_mixed_loss_exact_value_length_normalization_mask_and_detach():
    current = torch.tensor([[[-.2, -.5, float("inf")], [-1., float("nan"), float("nan")]]], dtype=torch.float64, requires_grad=True)
    old = current.detach().clone().requires_grad_()
    mask = torch.tensor([[[True, True, False], [True, False, False]]])
    rewards = torch.tensor([[1., 0.]], dtype=torch.float64, requires_grad=True)
    replay = torch.tensor([[-.3, -.6], [-.8, float("nan")]], dtype=torch.float64, requires_grad=True)
    replay_mask = torch.tensor([[True, True], [True, False]])
    loss, info = elite_replay.grpo_replay_loss(current, old, rewards, mask, replay, replay_mask, replay_weight=.25)
    torch.testing.assert_close(info["replay_loss"], torch.tensor((.45 + .8) / 2, dtype=torch.float64))
    torch.testing.assert_close(loss, .75 * info["grpo_loss"] + .25 * info["replay_loss"])
    loss.backward()
    assert old.grad is None and rewards.grad is None
    assert torch.isfinite(current.grad).all() and torch.isfinite(replay.grad).all()
    assert torch.equal(current.grad[~mask], torch.zeros_like(current.grad[~mask]))
    assert replay.grad[1, 1] == 0


@pytest.mark.parametrize("dtype", [torch.float32, torch.float64])
def test_elite_rejects_finite_logps_with_unrepresentable_ratio_before_nan_backward(dtype):
    current = torch.tensor([[[-1.], [-1.]]], dtype=dtype, requires_grad=True)
    old = torch.tensor([[[-1000.], [-1.]]], dtype=dtype)
    with pytest.raises(ValueError, match="representable exponential"):
        elite_replay.grpo_replay_loss(current, old, torch.tensor([[1., 0.]], dtype=dtype),
            torch.ones_like(current, dtype=torch.bool), torch.zeros(1, 1, dtype=dtype),
            torch.ones(1, 1, dtype=torch.bool))


def test_clean_exact_transport_matches_exhaustive_and_envelope_gradient():
    cost = torch.tensor([[3., 1., 2.], [2., 4., .5], [.1, 2., 3.]], dtype=torch.float64, requires_grad=True)
    value, plan = clean_rm.exact_uniform_transport(cost)
    reference = min(sum(float(cost.detach()[i, p[i]]) for i in range(3)) / 3 for p in itertools.permutations(range(3)))
    assert float(value.detach()) == pytest.approx(reference)
    torch.testing.assert_close(plan.sum(0), torch.full((3,), 1 / 3, dtype=torch.float64))
    torch.testing.assert_close(plan.sum(1), torch.full((3,), 1 / 3, dtype=torch.float64))
    value.backward()
    torch.testing.assert_close(cost.grad, plan)
    with pytest.raises(ValueError, match="equal batches"):
        clean_rm.exact_uniform_transport(torch.zeros(2, 3))


def test_clean_joint_semantics_disambiguate_same_preference_histograms():
    features = torch.tensor([[0.], [3.]], dtype=torch.float64)
    preferences = torch.tensor([0., 1.], dtype=torch.float64)
    correct = clean_rm.joint_cost(features, preferences, features, preferences)
    wrong = clean_rm.joint_cost(features, preferences.flip(0), features, preferences)
    correct_value, _ = clean_rm.exact_uniform_transport(correct)
    wrong_value, _ = clean_rm.exact_uniform_transport(wrong)
    assert correct_value == 0 and wrong_value > 0
    # Marginal-only matching could exchange the semantic identities at no cost.
    marginal_only = (preferences.flip(0)[:, None] - preferences[None]).square()
    assert clean_rm.exact_uniform_transport(marginal_only)[0] == 0


@pytest.mark.parametrize("family", ["square", "logistic"])
def test_clean_corrected_loss_is_unbiased_for_both_true_feedback_states(family):
    prediction = torch.tensor([.2, -.7], dtype=torch.float64, requires_grad=True)
    mu = torch.tensor([.2, .1], dtype=torch.float64, requires_grad=True)
    nu = torch.tensor([.15, .3], dtype=torch.float64, requires_grad=True)
    one = clean_rm.corrected_reward_loss(prediction, torch.ones(2), mu, nu, family=family, reduction="none")
    zero = clean_rm.corrected_reward_loss(prediction, torch.zeros(2), mu, nu, family=family, reduction="none")
    if family == "square":
        positive, negative = (prediction - 1).square(), prediction.square()
    else:
        positive, negative = torch.nn.functional.softplus(-prediction), torch.nn.functional.softplus(prediction)
    torch.testing.assert_close((1 - mu.detach()) * one + mu.detach() * zero, positive)
    torch.testing.assert_close(nu.detach() * one + (1 - nu.detach()) * zero, negative)
    one.mean().backward()
    assert mu.grad is None and nu.grad is None and torch.isfinite(prediction.grad).all()


def test_clean_noise_estimator_is_actually_fitted_by_joint_ot_without_oracle_rates():
    torch.manual_seed(42)
    model = clean_rm.NoiseEstimator(2).double()
    features = torch.tensor([[0., 0.], [0., 1.], [2., 0.], [2., 1.]], dtype=torch.float64)
    noisy = torch.tensor([0., 1., 1., 0.], dtype=torch.float64)
    clean_features = features + .01
    clean = torch.tensor([0., 0., 1., 1.], dtype=torch.float64)
    before = [p.detach().clone() for p in model.parameters()]
    optimizer = torch.optim.SGD(model.parameters(), lr=.03)
    loss, info = clean_rm.noise_estimation_loss(model, features, noisy, clean_features, clean)
    optimizer.zero_grad()
    loss.backward()
    assert all(torch.isfinite(p.grad).all() for p in model.parameters())
    optimizer.step()
    assert any(not torch.equal(a, b) for a, b in zip(before, model.parameters(), strict=True))
    assert (info["mu"] + info["nu"] <= .95 + 1e-10).all()
    with pytest.raises(ValueError, match="nondegenerate"):
        clean_rm.recover_preferences(noisy, torch.ones(4), torch.ones(4))
