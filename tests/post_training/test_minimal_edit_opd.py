"""ME-OPD old-policy routing, exact selected-token objective and boundaries."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pytest
import torch

from auto_research.post_training import minimal_edit_opd as me


def inputs():
    logits = torch.tensor([[[.2, -.3], [.7, -.4], [.1, -.2]],
        [[-1., 1.], [.3, -.8], [.6, -.1]],
        [[-.3, .1], [.8, -.2], [.4, .2]],
        [[.5, .2], [-.4, .3], [-.6, .5]]], dtype=torch.float64, requires_grad=True)
    actions = torch.tensor([[0, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 0]])
    old = logits.detach().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1).clone().requires_grad_()
    teacher = (old.detach() + torch.tensor([[-.5, .1, 0.]], dtype=torch.float64)).clamp_max(-.01).requires_grad_()
    rewards = torch.tensor([1., 0., 0., 0.], dtype=torch.float64, requires_grad=True)
    groups = torch.tensor([0, 0, 0, 0])
    mask = torch.ones(4, 3, dtype=torch.bool)
    return logits, actions, old, teacher, rewards, groups, mask


def snapshot(old, teacher, rewards, groups, mask, correction=0):
    advantages = me.full_group_advantages(rewards, groups, std_correction=correction, epsilon=1e-6)
    return me.freeze_rollouts(old, teacher, rewards, mask, task_advantages=advantages)


def local_loss(logits, actions, batch, **kwargs):
    task = (me.correct_rollout_grpo(me.sampled_log_probabilities(logits, actions, batch), batch)
        if batch.correct.any() else None)
    return me.minimal_edit_loss(logits, actions, batch, correct_task_loss=task, **kwargs)


def test_full_group_rewards_precede_routing_and_statistics_are_explicit():
    rewards = torch.tensor([1., 0., 0., 0., 1., 1., 1., 0.], requires_grad=True)
    groups = torch.tensor([5]*4 + [9]*4)
    for correction in (0, 1):
        advantage = me.full_group_advantages(rewards, groups, std_correction=correction, epsilon=1e-6)
        expected = torch.cat([(row - row.mean()) / (row.std(correction=correction) + 1e-6)
            for row in rewards.detach().reshape(2, 4)])
        torch.testing.assert_close(advantage, expected)
        assert advantage[rewards == 1].min() > 0 and not advantage.requires_grad
    assert me.full_group_advantages(torch.ones(4), groups[:4], std_correction=0, epsilon=1e-6).count_nonzero() == 0
    with pytest.raises(ValueError, match="binary"):
        me.full_group_advantages(torch.tensor([1., .5]), torch.zeros(2, dtype=torch.long), std_correction=0, epsilon=1e-6)
    with pytest.raises(ValueError, match="same K"):
        me.full_group_advantages(torch.ones(5), torch.tensor([0, 0, 1, 1, 1]), std_correction=0, epsilon=1e-6)
    with pytest.raises(ValueError, match="K >= 2"):
        me.full_group_advantages(torch.ones(2), torch.tensor([0, 1]), std_correction=0, epsilon=1e-6)


def test_correct_only_task_failed_only_strict_old_mask_and_frozen_clones():
    _, _, old, teacher, rewards, groups, mask = inputs()
    batch = snapshot(old, teacher, rewards, groups, mask)
    expected = torch.tensor([[False]*3, [True, False, False], [True, False, False], [True, False, False]])
    assert torch.equal(batch.corrective_mask, expected)
    assert batch.correct.tolist() == [True, False, False, False]
    with torch.no_grad():
        old.fill_(-9.)
        teacher.fill_(-.001)
        rewards.zero_()
        mask.zero_()
    assert torch.equal(batch.corrective_mask, expected)
    assert batch.actor_mask.all() and batch.correct[0]
    assert all(not value.requires_grad for value in (batch.old_log_prob, batch.teacher_log_prob, batch.advantages))


def test_printed_eq1_global_selected_z_scalar_and_gradient_not_dense_kl():
    logits, actions, old, teacher, rewards, groups, mask = inputs()
    # Deliberately unequal selected-token counts: row1=2, row2=1,row3=1.
    with torch.no_grad():
        teacher[1, 1] = old[1, 1] - .4
    batch = snapshot(old, teacher, rewards, groups, mask)
    loss, audit = local_loss(logits, actions, batch, corrective_weight=.4)
    p = logits.softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    adv = (1. - .25) / (math.sqrt(3/16) + 1e-6)
    ratio = p[0] / old[0].detach().exp()
    task = -torch.minimum(ratio * adv, ratio.clamp(.8, 1.2) * adv).mean()
    terms = p.log() - teacher.detach()
    correction = (terms[1, 0] + terms[1, 1] + terms[2, 0] + terms[3, 0]) / 4
    reference = task + .4 * correction
    torch.testing.assert_close(loss, reference, rtol=1e-12, atol=1e-14)
    expected_gradient = torch.autograd.grad(reference, logits, retain_graph=True)[0]
    loss.backward()
    torch.testing.assert_close(logits.grad, expected_gradient, rtol=1e-12, atol=1e-14)
    assert audit["selected_tokens"] == 4 and audit["correct_rollouts"] == 1
    assert old.grad is None and teacher.grad is None and rewards.grad is None
    assert logits.grad[1, 2].count_nonzero() == 0
    assert logits.grad[2:, 1:].count_nonzero() == 0
    assert logits.grad[0].norm() > 0 and logits.grad[1, 0].norm() > 0


def test_mask_uses_old_policy_while_grpo_ratio_uses_current_over_old():
    logits, actions, old, teacher, rewards, groups, mask = inputs()
    batch = snapshot(old, teacher, rewards, groups, mask)
    with torch.no_grad():
        # Selected wrong token's current probability is now BELOW teacher;
        # it must remain selected. Correct token ratio >1.2 must be clipped.
        logits[1, 0, 0] = -20.
        for token, action in enumerate(actions[0]):
            logits[0, token, action] = 10.
    loss, audit = local_loss(logits, actions, batch)
    loss.backward()
    assert audit["selected_tokens"] == 3
    assert logits.grad[1, 0].norm() > 0
    assert logits.grad[0].count_nonzero() == 0
    sampled = logits.detach().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    assert sampled[1, 0] < teacher[1, 0]
    assert torch.equal(batch.corrective_mask, snapshot(old, teacher, rewards, groups, mask).corrective_mask)


@pytest.mark.parametrize("all_correct", [False, True])
def test_zero_z_and_empty_task_branch_are_differentiable_without_fake_signal(all_correct):
    logits, actions, old, teacher, rewards, groups, mask = inputs()
    with torch.no_grad():
        rewards.fill_(int(all_correct))
        teacher.copy_(old + .001)
    batch = snapshot(old, teacher, rewards, groups, mask)
    loss, audit = local_loss(logits, actions, batch)
    loss.backward()
    assert loss.item() == 0 and audit["selected_tokens"] == 0
    assert audit["correct_rollouts"] == (4 if all_correct else 0)
    assert logits.grad.isfinite().all() and logits.grad.count_nonzero() == 0


def test_all_failed_nonzero_correction_still_trains_without_task_branch():
    logits, actions, old, teacher, rewards, groups, mask = inputs()
    batch = snapshot(old, teacher, torch.zeros_like(rewards), groups, mask)
    loss, audit = local_loss(logits, actions, batch)
    loss.backward()
    assert audit["correct_rollouts"] == 0 and audit["task_loss"].item() == 0
    assert audit["selected_tokens"] == 4 and logits.grad[:, 0].norm() > 0


def test_exact_composition_requires_external_correct_task_loss_and_freezes_advantages():
    logits, actions, old, teacher, rewards, _, mask = inputs()
    advantages = torch.tensor([3., -1., -1., -1.], requires_grad=True, dtype=torch.float64)
    batch = me.freeze_rollouts(old, teacher, rewards, mask, task_advantages=advantages)
    external = logits[0].square().sum() * .03
    loss, audit = me.minimal_edit_loss(logits, actions, batch, correct_task_loss=external)
    torch.testing.assert_close(loss.detach(), external.detach() + .01 * audit["corrective_loss"])
    loss.backward()
    assert advantages.grad is None
    with pytest.raises(ValueError, match="external scalar"):
        me.minimal_edit_loss(logits, actions, batch, correct_task_loss=None)
    with pytest.raises(ValueError, match="external scalar"):
        me.minimal_edit_loss(logits, actions, batch, correct_task_loss=torch.ones(2))
    failed = me.freeze_rollouts(old, teacher, torch.zeros_like(rewards), mask, task_advantages=advantages)
    with pytest.raises(ValueError, match="pass None"):
        me.minimal_edit_loss(logits, actions, failed, correct_task_loss=external)


def test_unused_teacher_correct_rows_and_padding_nan_cannot_pollute_gradient():
    logits, actions, old, teacher, rewards, groups, mask = inputs()
    mask[1, 2] = False
    with torch.no_grad():
        teacher[0] = float("nan")
        teacher[1, 2] = float("nan")
        old[1, 2] = float("nan")
        logits[1, 2] = float("nan")
        actions[1, 2] = -1
    batch = snapshot(old, teacher, rewards, groups, mask)
    loss, _ = local_loss(logits, actions, batch)
    loss.backward()
    assert loss.isfinite() and logits.grad.isfinite().all()
    assert logits.grad[~mask].count_nonzero() == 0
    with pytest.raises(ValueError, match="nonpositive"):
        snapshot(old, torch.full_like(teacher, float("nan")), rewards, groups, mask)


@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16])
def test_low_precision_probability_math_is_promoted(dtype):
    logits, actions, old, teacher, rewards, groups, mask = inputs()
    reduced = logits.detach().to(dtype).requires_grad_()
    batch = snapshot(old.to(dtype), teacher.to(dtype), rewards.to(dtype), groups, mask)
    loss, _ = local_loss(reduced, actions, batch)
    loss.backward()
    assert loss.dtype == torch.float32 and reduced.grad.isfinite().all()


@pytest.mark.parametrize("bad", [-1., float("inf"), float("nan"), 1e308])
def test_invalid_or_unrepresentable_corrective_weight_fails(bad):
    logits, actions, old, teacher, rewards, groups, mask = inputs()
    batch = snapshot(old, teacher, rewards, groups, mask)
    if bad == 1e308:
        # force a representational overflow of the combined float64 objective
        with torch.no_grad():
            logits[1:, 0, 0] = -1e100
    with pytest.raises(ValueError):
        local_loss(logits, actions, batch, corrective_weight=bad)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_checks_numerical_component_not_capability(seed):
    result = me.diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"]
    assert all(type(value) is bool and value for value in result["checks"].values())
    assert all(isinstance(value, (float, int)) and math.isfinite(value) for value in result["metrics"].values())
    assert result["metrics"]["selected_tokens"] == 5 and result["metrics"]["model_calls"] == 0


def test_paper_metadata_cost_figure_and_nonpromotion_contract():
    root = Path(__file__).resolve().parents[2]
    catalog = json.loads((root / "src/auto_research/paper_specs/catalog/post-training/minimal-edit-opd.json").read_text())
    assert catalog["first_author"] == "Wen Ye" and catalog["first_author_affiliation"] == "Meta Superintelligence Labs"
    assert catalog["published_at"] == "2026-10-21T17:59:28Z" and catalog["announced_on"] == "2026-10-23"
    assert catalog["code"] is None and catalog["upstream_revision"] is None and catalog["code_license"] is None
    assert catalog["priority"] == "P0" and catalog["diagnostic_only"] and catalog["adapter"] is None
    assert not catalog["promotion_eligible"] and not catalog["evolve_integrated"]
    assert catalog["requires_gpu_validation"] and catalog["gpu_validation_artifact"] == "docs/gpu-validations/minimal-edit-opd-a100-20261025.json"
    assert catalog["full_experiment_status"] == "not_reproduced_high_cost" and catalog["review_done"]
    assert catalog["full_experiment_review_done"] and not catalog["automatic_retry"] and not catalog["automatic_implementation_queue"]
    folder = root / "docs/post-training/2610.30231-minimal-edit-opd"
    readme = (folder / "README.md").read_text()
    for field in ("## 论文信息", "原始发布日期", "公司 / 作者机构", "原作者代码", "原作者代码许可", "本地 Adapter / key", "本地代码", "diagnostic only", "成本过高，不复现（审查 DONE）", "未报告", "evolve_integrated=false", "本地约定"):
        assert field in readme
    provenance = json.loads((folder / "assets/provenance.json").read_text())
    image = folder / "assets" / provenance["local_path"]
    assert provenance["license"] == "CC BY 4.0" and provenance["transformation"] == "none"
    assert provenance["image"] == "paper-figure-01.png" and image.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert hashlib.sha256(image.read_bytes()).hexdigest() == provenance["sha256"]
