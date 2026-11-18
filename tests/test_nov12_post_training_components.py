from copy import deepcopy
import itertools
import math

import numpy as np
import pytest
import torch
from torch import nn

from auto_research.post_training import apmd_reference_reset as apmd
from auto_research.post_training import bopd
from auto_research.post_training import lcs_reference_opd as lcs


@pytest.mark.parametrize("module", [apmd, bopd, lcs])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_all_diagnostics_are_finite_mechanism_checks(module, seed):
    result = module.diagnostic(seed)
    assert result["seed"] == seed
    assert result["evaluation_tier"] == "l1_mechanism" and result["diagnostic_only"] is True
    assert all(value is True for value in result["checks"].values())
    assert all(math.isfinite(v) for v in result["metrics"].values())


@pytest.mark.parametrize("module", [apmd, lcs])
def test_cpu_references_reject_cuda(module):
    with pytest.raises(ValueError, match="CPU"):
        module.diagnostic(42, "cuda")


def test_apmd_exact_target_stationarity_and_unchanged_constant_reward():
    ref = np.array([[.2, .3, .5], [.1, .8, .1]])
    reward = np.array([[.1, .8, -.2], [.6, .2, 1.]])
    target = apmd.mirror_step(ref, reward, .7)
    assert np.allclose(apmd.mirror_step(ref, np.ones_like(reward), .7), ref)
    # Lagrangian stationarity: r - log(p/ref)/eta is response-independent.
    stationarity = reward - (np.log(target) - np.log(ref)) / .7
    assert np.allclose(stationarity, stationarity[:, :1])
    path = apmd.exact_reset_path(ref, reward, .7, 4)
    assert np.allclose(path[-1], apmd.mirror_step(ref, reward, 2.8))
    assert not np.allclose(path[-1], target)


def test_apmd_pairwise_enumeration_and_kimi_bias_independent_reference():
    ref, cand, reward = np.array([[.2, .5, .3]]), np.array([[.6, .1, .3]]), np.array([[.1, .9, -.2]])
    eta = .4
    result = apmd.squared_losses(cand, ref, reward, eta)
    pairwise = 0.
    for a, b in itertools.product(range(3), repeat=2):
        ra = math.log(cand[0, a] / ref[0, a]) / eta
        rb = math.log(cand[0, b] / ref[0, b]) / eta
        pairwise += ref[0, a] * ref[0, b] * (ra - rb - reward[0, a] + reward[0, b]) ** 2
    kl = sum(ref[0, a] * math.log(ref[0, a] / cand[0, a]) for a in range(3))
    assert result["rebel_on_policy"][0] == pytest.approx(pairwise)
    assert result["kimi_squared_kl_bias"][0] == pytest.approx((kl / eta) ** 2)
    assert result["kimi_mean_baseline"][0] == pytest.approx(result["centered_mse"][0] + (kl / eta) ** 2)
    target = apmd.mirror_step(ref, reward, eta)
    at_target = apmd.squared_losses(target, ref, reward, eta)
    assert at_target["centered_mse"][0] < 1e-25
    assert at_target["kimi_mean_baseline"][0] > 0  # Mean baseline does NOT share the exact zero-loss target.


def test_empirical_kimipo_uses_separate_baseline_response_rewards():
    current = np.log([.4, .6]); ref = np.log([.2, .7])
    rewards, baseline = np.array([1., 0.]), np.array([[.2, .4], [.7, .9]])
    expected = np.mean(((current - ref) / .5 - rewards + np.array([.3, .8])) ** 2)
    assert apmd.empirical_kimipo_loss(current, ref, rewards, baseline, .5) == pytest.approx(expected)


@pytest.mark.parametrize("policy", [np.array([[0., 1.]]), np.array([[.4, .4]]), np.array([[np.nan, .5]])])
def test_apmd_invalid_support_is_not_silently_repaired(policy):
    with pytest.raises(ValueError):
        apmd.mirror_step(policy, np.ones_like(policy), .4)


def test_apmd_refuses_eta_and_floating_underflow():
    with pytest.raises(ValueError):
        apmd.mirror_step(np.array([[.5, .5]]), np.array([[0., 1.]]), 0.)
    with pytest.raises(ValueError, match="underflow"):
        apmd.mirror_step(np.array([[.5, .5]]), np.array([[0., 1.]]), 1e5)


def test_lcs_matches_independent_exhaustive_subsequence_search():
    rng = np.random.default_rng(92)
    def subsequences(values):
        return {tuple(values[i] for i in range(len(values)) if bits & (1 << i)) for bits in range(1 << len(values))}
    for _ in range(20):
        a, b = tuple(rng.choice(list("abc"), 5)), tuple(rng.choice(list("abc"), 4))
        expected = max(map(len, subsequences(a) & subsequences(b)))
        assert lcs.lcs_length(a, b) == expected
    assert lcs.lcs_length(("a", "b", "a"), ("a", "a")) == 2


def test_lcs_normalizer_changes_selector_as_in_benchmark_contract():
    failure = lcs.Trajectory("x", tuple("abcdef"), False)
    short = lcs.Trajectory("x", tuple("ab"), True)
    longer = lcs.Trajectory("x", tuple("abcdx"), True)
    pool = lcs.reference_pool([short, longer])
    assert lcs.select_reference(failure, pool, normalizer="shorter")["teacher_reference"] == short
    assert lcs.select_reference(failure, pool, normalizer="failed")["teacher_reference"] == longer


def test_free_target_assignment_can_reuse_a_reference_without_balancing():
    reference = lcs.Trajectory("x", ("a", "b"), True)
    pool = lcs.reference_pool([reference, lcs.Trajectory("x", ("c",), True)])
    for actions in [("a", "b", "bad"), ("a", "extra", "b")]:
        assert lcs.select_reference(lcs.Trajectory("x", actions, False), pool, normalizer="failed")["teacher_reference"] == reference


def test_lcs_pool_deduplicates_whole_sequences_preserving_order_and_repetition():
    first = lcs.Trajectory("x", ("a", "a", "b"), True)
    pool = lcs.reference_pool([first, first, lcs.Trajectory("x", ("a", "b"), True), lcs.Trajectory("x", ("b", "a"), True), lcs.Trajectory("x", ("z",), False)])
    assert len(pool["x"]) == 3
    assert pool["x"][0] == first
    assert lcs.select_reference(lcs.Trajectory("other", ("a",), False), pool, normalizer="failed")["teacher_reference"] is None


def test_lcs_exact_tool_identity_and_empty_boundary():
    a = lcs.canonical_tool_call("move", {"room": 2, "x": 1})
    b = lcs.canonical_tool_call("move", {"x": 1, "room": 2})
    assert a == b
    assert a != lcs.canonical_tool_call("move", {"x": 2, "room": 2})
    assert lcs.compatibility((), ("a",), normalizer="failed") == 0.
    with pytest.raises(ValueError):
        lcs.canonical_tool_call("move", {"x": float("nan")})
    with pytest.raises(ValueError):
        lcs.lcs_length(iter(["a"]), ("a",))


def test_failure_only_mean_skips_successes_and_all_success_batch():
    assert lcs.failure_only_mean([2., float("nan"), 6.], [False, True, False]) == 4.
    assert lcs.failure_only_mean([float("nan")], [True]) is None
    with pytest.raises(ValueError):
        lcs.failure_only_mean([float("nan")], [False])


def test_bopd_fkl_direction_and_equal_trajectory_weighting():
    student = torch.tensor([[[.4, .6], [.2, .8], [.5, .5]], [[.3, .7], [.6, .4], [.1, .9]]], dtype=torch.float64).log().requires_grad_()
    teacher = torch.tensor([[[.8, .2], [.5, .5], [.6, .4]], [[.1, .9], [.2, .8], [.7, .3]]], dtype=torch.float64).log().requires_grad_()
    mask = torch.tensor([[True, False, False], [True, True, True]])
    per_token = (teacher.detach().exp() * (teacher.detach() - student)).sum(-1)
    expected = (per_token[0, 0] + per_token[1].mean()) / 2
    loss = bopd.forward_kl(student, teacher, mask)
    assert torch.allclose(loss, expected)
    assert not torch.allclose(loss, per_token[mask].mean())
    loss.backward()
    assert teacher.grad is None
    assert torch.count_nonzero(student.grad[~mask]) == 0
    assert student.grad[mask].norm() > 0


def test_bopd_fkl_gradcheck_and_nan_padding():
    student, teacher = torch.randn(2, 3, 4, dtype=torch.float64, requires_grad=True), torch.randn(2, 3, 4, dtype=torch.float64)
    mask = torch.tensor([[True, True, False], [True, True, True]])
    assert torch.autograd.gradcheck(lambda x: bopd.forward_kl(x, teacher, mask), (student,))
    padded_s, padded_t = student.detach().clone(), teacher.clone()
    padded_s[~mask] = float("nan");padded_t[~mask] = float("nan")
    assert torch.allclose(bopd.forward_kl(padded_s, padded_t, mask), bopd.forward_kl(student, teacher, mask))


def test_bopd_handoff_restores_parameters_buffers_and_new_optimizer_state():
    initial = nn.BatchNorm1d(3, dtype=torch.float64)
    intermediate = deepcopy(initial)
    with torch.no_grad():
        intermediate.weight.add_(.5)
        intermediate.running_mean.add_(1.)
        intermediate.num_batches_tracked.add_(7)
    bundle = bopd.stage_two_handoff(initial, intermediate, lambda ps: torch.optim.AdamW(ps))
    for name, tensor in initial.state_dict().items():
        assert torch.equal(tensor, bundle.student.state_dict()[name])
        assert tensor.data_ptr() != bundle.student.state_dict()[name].data_ptr()
    for name, tensor in intermediate.state_dict().items():
        assert torch.equal(tensor, bundle.teacher.state_dict()[name])
        assert tensor.data_ptr() != bundle.teacher.state_dict()[name].data_ptr()
    assert not bundle.optimizer.state
    assert bundle.student.training and not bundle.teacher.training
    assert all(not p.requires_grad for p in bundle.teacher.parameters())


def test_bopd_rejects_reused_optimizer_and_mismatched_model():
    initial, intermediate = nn.Linear(3, 4), nn.Linear(3, 4)
    old = torch.optim.AdamW(intermediate.parameters())
    with pytest.raises(ValueError, match="fresh"):
        bopd.stage_two_handoff(initial, intermediate, lambda _: old)
    with pytest.raises(ValueError, match="architecture"):
        bopd.stage_two_handoff(initial, nn.Linear(2, 4), lambda ps: torch.optim.AdamW(ps))


@pytest.mark.skipif(not torch.cuda.is_available(), reason="actual CUDA required")
def test_bopd_actual_cuda_diagnostic():
    result = bopd.diagnostic(42, "cuda:0")
    assert result["device"] == "cuda:0" and all(result["checks"].values())
