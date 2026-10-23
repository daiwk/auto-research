"""AOPD/GIFT exact formulas, frozen evidence, gradient and quota contracts."""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import pytest
import torch

from auto_research.post_training import aopd, gift


def test_aopd_leave_one_out_is_prompt_local_and_frozen():
    rewards = torch.tensor([1., 0., .2, .6], dtype=torch.float64, requires_grad=True)
    values = aopd.leave_one_out_advantages(rewards, torch.tensor([7, 7, 9, 9]))
    torch.testing.assert_close(values, torch.tensor([1., -1., -.4, .4], dtype=torch.float64))
    assert not values.requires_grad
    with pytest.raises(ValueError, match="at least two"):
        aopd.leave_one_out_advantages(rewards, torch.tensor([7, 8, 9, 9]))
    with pytest.raises(ValueError, match=r"\[0,1\]"):
        aopd.leave_one_out_advantages(rewards.detach() + 1, torch.tensor([7, 7, 9, 9]))


@pytest.mark.parametrize("cap", [None, 1.2, 4.])
def test_aopd_exhaustive_two_step_estimator_and_gradient_equal_advantage_objective(cap):
    # Enumerate independent rollout PAIRS, rather than treating an exhaustive
    # list as a sampled group. This retains independence of each LOO baseline.
    old = torch.tensor([[.6, .4], [.7, .3], [.2, .8]], dtype=torch.float64).log().requires_grad_()
    teacher = torch.tensor([[.3, .7], [.2, .8], [.8, .2]], dtype=torch.float64).log().requires_grad_()
    current = torch.tensor([[.4, -.1], [-.2, .5], [.8, -.3]], dtype=torch.float64, requires_grad=True)
    paths = list(itertools.product(range(2), repeat=2))
    def reward(path):
        return float(path[0] != path[1])
    def states(path):
        return [0, 1 + path[0]]
    def probability(path):
        p = old.detach().exp()
        return float(p[0, path[0]] * p[1 + path[0], path[1]])
    expectation = current.sum() * 0
    for first, second in itertools.product(paths, repeat=2):
        rows = torch.tensor([states(first), states(second)])
        loss, audit = aopd.aopd_loss(current[rows], old[rows], teacher[rows],
            torch.tensor([first, second]), torch.tensor([reward(first), reward(second)], dtype=torch.float64),
            torch.tensor([0, 0]), torch.ones(2, 2, dtype=torch.bool), clip=cap)
        expectation = expectation + probability(first) * probability(second) * loss
        assert not audit["teacher_target"].requires_grad
    p, q = old.detach().exp(), teacher.detach().exp()
    if cap is not None:
        q = torch.minimum(q, cap * p)  # Deliberately NOT re-normalized.
    logcurrent = current.log_softmax(-1)
    q_root = torch.tensor([float(p[1, 1]), float(p[2, 0])], dtype=torch.float64)
    v_root = (p[0] * q_root).sum()
    oracle = (q[0] * (q_root - v_root) * logcurrent[0]).sum()
    for first in range(2):
        state = 1 + first
        outcomes = torch.tensor([reward((first, second)) for second in range(2)], dtype=torch.float64)
        advantage = outcomes - (p[state] * outcomes).sum()
        oracle = oracle + p[0, first] * (q[state] * advantage * logcurrent[state]).sum()
    oracle = -oracle / 2
    torch.testing.assert_close(expectation, oracle, rtol=1e-12, atol=1e-14)
    actual_grad = torch.autograd.grad(expectation, current, retain_graph=True)[0]
    expected_grad = torch.autograd.grad(oracle, current)[0]
    torch.testing.assert_close(actual_grad, expected_grad, rtol=1e-12, atol=1e-14)
    expectation.backward()
    assert old.grad is None and teacher.grad is None


def test_aopd_truncates_both_terms_without_renormalization_and_honors_padding():
    logits = torch.tensor([[[math.log(.8), math.log(.2)], [float("nan"), float("nan")]],
                           [[math.log(.3), math.log(.7)], [float("nan"), float("nan")]]],
                          dtype=torch.float64, requires_grad=True)
    old = torch.tensor([[[.9, .1], [.5, .5]], [[.9, .1], [.5, .5]]], dtype=torch.float64).log().requires_grad_()
    teacher = torch.tensor([[[.1, .9], [.5, .5]], [[.1, .9], [.5, .5]]], dtype=torch.float64).log().requires_grad_()
    mask = torch.tensor([[True, False], [True, False]])
    actions = torch.tensor([[1, -1], [0, -1]])
    loss, audit = aopd.aopd_loss(logits, old, teacher, actions, torch.tensor([1., 0.]),
                                torch.tensor([0, 0]), mask, clip=4.)
    target = torch.tensor([.1, .4], dtype=torch.float64)
    expected = -(4 * math.log(.2) - float(target @ logits[0, 0].detach())
                 - ((.1 / .9) * math.log(.3) - float(target @ logits[1, 0].detach()))) / 2
    assert float(loss.detach()) == pytest.approx(expected)
    assert audit["truncated_teacher_mass"][0, 0] == pytest.approx(.5)
    loss.backward()
    assert logits.grad.isfinite().all() and logits.grad[~mask].count_nonzero() == 0
    assert old.grad is None and teacher.grad is None
    # All-wrong groups have zero Eq.3.8 signal; no undocumented fallback added.
    zero, _ = aopd.aopd_loss(logits, old, teacher, actions, torch.zeros(2), torch.tensor([0, 0]), mask)
    assert zero.detach().item() == 0


def test_gift_geometry_piecewise_scoring_zero_reference_and_exact_quota():
    r = torch.tensor([[[1., 0.], [1., 0.], [1., 0.], [0., 0.], [1., 0.]]])
    d = torch.tensor([[[1., 2.], [-.1, 3.], [-2., 1.], [1., 1.], [0., 0.]]])
    mask = torch.ones(1, 5, dtype=torch.bool)
    audit = gift.gradient_geometry(r, d, mask)
    torch.testing.assert_close(audit["score"], torch.tensor([[2., -.1, -2., 0., 0.]]))
    assert not audit["eligible"][0, 4] and not audit["usable_rl"][0, 3]
    # quota=floor(.8*5)=4: a hard conflict filter would incorrectly choose 2.
    selected = gift.exact_quota_mask(audit["score"], audit["eligible"], mask, .8)
    assert selected.tolist() == [[True, True, True, True, False]]
    partial = gift.exact_quota_mask(audit["score"], audit["eligible"], mask, .6)
    assert partial.tolist() == [[True, True, False, True, False]]
    assert gift.exact_quota_mask(audit["score"], audit["eligible"], mask, 0.).sum() == 0
    assert not audit["score"].requires_grad


@pytest.mark.parametrize("top_k", [1, 2, 4, 100])
def test_gift_sparse_tail_and_full_geometry_equal_original_logit_autograd(top_k):
    current = torch.tensor([[[.2, -.5, 1., -.3], [.7, -.2, .1, -.9]]], dtype=torch.float64, requires_grad=True)
    teacher = torch.tensor([[[1., .2, -.4, .3], [-.2, 1., .6, .1]]], dtype=torch.float64, requires_grad=True)
    actions = torch.tensor([[0, 2]])
    old = current.detach().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1).requires_grad_()
    advantage = torch.tensor([[.7, -.9]], dtype=torch.float64, requires_grad=True)
    mask = torch.ones(1, 2, dtype=torch.bool)
    loss, audit = gift.gift_loss(current, teacher, old, actions, advantage, mask,
                                step=1, teacher_top_k=top_k)
    logp, logq = current.log_softmax(-1), teacher.detach().log_softmax(-1)
    p, q = logp.exp(), logq.exp()
    if top_k >= 4:
        token_kl = (q * (logq - logp)).sum(-1)
    else:
        selected = torch.zeros_like(p, dtype=torch.bool).scatter(-1, torch.topk(q, top_k, -1).indices, True)
        p_tail = torch.where(selected, 0., p).sum(-1)
        q_tail = torch.where(selected, 0., q).sum(-1)
        token_kl = torch.where(selected, q * (logq - logp), 0.).sum(-1) + q_tail * (q_tail / p_tail).log()
    teacher_grad = torch.autograd.grad(token_kl.sum(), current, retain_graph=True)[0]
    loga = logp.gather(-1, actions[..., None]).squeeze(-1)
    token_rl = -(loga - old.detach()).exp() * advantage.detach()
    rl_grad = torch.autograd.grad(token_rl.sum(), current, retain_graph=True)[0]
    torch.testing.assert_close(audit["teacher_gradient"], teacher_grad, rtol=1e-12, atol=1e-14)
    torch.testing.assert_close(audit["rl_gradient"], rl_grad, rtol=1e-12, atol=1e-14)
    torch.testing.assert_close(loss, (token_rl + token_kl).mean())
    loss.backward()
    assert current.grad.isfinite().all()
    assert old.grad is None and teacher.grad is None and advantage.grad is None


def test_gift_clipped_ppo_branches_zero_gradient_and_tail_not_bucket_geometry():
    current = torch.tensor([[[.2, -.5, 1., -.3]]], dtype=torch.float64, requires_grad=True)
    teacher = torch.tensor([[[1., .2, -.4, .3]]], dtype=torch.float64)
    actions = torch.tensor([[0]])
    base_logp = current.detach().log_softmax(-1)[..., 0]
    for advantage, ratio in ((1., 1.5), (-1., .5)):
        _, audit = gift.gift_loss(current, teacher, base_logp - math.log(ratio), actions,
            torch.tensor([[advantage]], dtype=torch.float64), torch.ones(1, 1, dtype=torch.bool),
            step=1, teacher_top_k=1)
        assert audit["rl_gradient"].count_nonzero() == 0
        assert audit["score"].item() == 0 and audit["selected"].item()
    # Tail aggregation must still give different gradients to distinct original
    # logits outside top-k; a 2-D bucket-space vector would erase this fact.
    _, audit = gift.gift_loss(current, teacher, base_logp, actions, torch.ones(1, 1),
        torch.ones(1, 1, dtype=torch.bool), step=1, teacher_top_k=1)
    assert audit["teacher_gradient"].shape[-1] == 4
    assert audit["teacher_gradient"][0, 0, 1] != audit["teacher_gradient"][0, 0, 2]


def test_gift_coverage_uses_all_valid_denominator_and_not_selected_set():
    current = torch.tensor([[[.5, -.1], [.2, -.2], [.9, -.4], [float("nan"), float("nan")]]], dtype=torch.float64, requires_grad=True)
    teacher = torch.zeros_like(current, requires_grad=True)
    actions = torch.tensor([[0, 0, 0, -1]])
    mask = torch.tensor([[True, True, True, False]])
    old = torch.tensor([[-.7, -.7, -.7, float("nan")]])
    advantage = torch.tensor([[1., -1., .2, float("nan")]])
    loss, audit = gift.gift_loss(current, teacher, old, actions, advantage, mask,
                                step=44, teacher_top_k=1)
    assert audit["retention"] == .5 and audit["selected"].sum() == 1
    expected = audit["token_kl"][audit["selected"]].sum() / 3
    torch.testing.assert_close(audit["teacher_loss"], expected)
    loss.backward()
    assert current.grad.isfinite().all() and current.grad[~mask].count_nonzero() == 0
    assert teacher.grad is None
    assert [gift.coverage_ratio(i) for i in (1, 10, 44, 77, 78, 96)] == pytest.approx([1., 1., .5, 1 / 68, 0., 0.])
    _, exited = gift.gift_loss(current, teacher, old, actions, advantage, mask, step=78)
    assert not exited["selected"].any() and exited["teacher_loss"] == 0


@pytest.mark.parametrize("module", [aopd, gift])
def test_bounded_diagnostics_update_parameters_without_privileged_gradients(module):
    result = module.diagnostic(42)
    assert result["diagnostic_only"] and all(result["checks"].values())
    assert all(math.isfinite(value) for value in result["metrics"].values())
    assert result["metrics"]["gradient_norm"] > 0 and result["metrics"]["parameter_delta"] > 0
    if module is aopd:
        assert result["checks"]["rollout_policy_detached"]
        assert result["metrics"]["loss_after"] < result["metrics"]["loss_before"]
    else:
        assert result["checks"]["old_policy_detached"] and result["checks"]["advantages_detached"]


def test_oct23_documentation_metadata_cost_and_diagnostic_boundaries():
    root = Path(__file__).resolve().parents[2]
    for paper, key in (("2610.31563", "aopd"), ("2610.30796", "gift")):
        readme = (root / "docs" / "post-training" / f"{paper}-{key}" / "README.md").read_text()
        for required in ("## 论文信息", "原始发布日期", "公司 / 作者机构", "原作者代码", "原作者代码许可",
                         "本地 Adapter / key", "本地代码", "diagnostic only", "成本过高，不复现（审查 DONE）",
                         "未报告", "evolve_integrated=false"):
            assert required in readme
        metrics_path = root / "docs" / "post-training" / f"{paper}-{key}" / "metrics" / "component-cpu-seeds42-44.json"
        if metrics_path.exists():
            data = json.loads(metrics_path.read_text())
            assert data["diagnostic_only"] and data["seeds"] == [42, 43, 44]
