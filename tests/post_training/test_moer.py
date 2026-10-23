"""MOER printed equations, single-prefix rollback and evidence isolation."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pytest
import torch

from auto_research.post_training import moer


def test_cosine_cot_prefix_and_single_candidate_rollback_contract():
    assert [moer.prefix_ratio(s) for s in (0, 49, 50, 275, 500, 501, 1000)] == pytest.approx([1., 1., 1., .55, .1, .1, .1])
    ratios = [moer.prefix_ratio(s) for s in range(1001)]
    assert all(a >= b for a, b in zip(ratios, ratios[1:]))
    assert moer.expert_cot_prefix(tuple(range(10)), 275) == tuple(range(5))
    assert moer.selective_rollback((1, 2), (8, 9), (1, 2, 3), guided_correct=True, expert_verified=True) == ((1, 2, 8, 9), False)
    assert moer.selective_rollback((1, 2), (8, 9), (1, 2, 3), guided_correct=False, expert_verified=True) == ((1, 2, 3), True)
    with pytest.raises(ValueError, match="verified"):
        moer.selective_rollback((1,), (2,), (1, 3), guided_correct=False, expert_verified=False)
    with pytest.raises(ValueError, match="belong"):
        moer.selective_rollback((7,), (2,), (1, 3), guided_correct=True, expert_verified=True)
    assert moer.prefix_ratio(10**400) == .1
    for bad in (-1, 1.5, True):
        with pytest.raises(ValueError):
            moer.prefix_ratio(bad)
    with pytest.raises(ValueError):
        moer.prefix_ratio(500, anneal_steps=50, warmup_steps=50)


def test_union_advantage_is_prompt_local_frozen_and_not_std_normalized():
    rewards = torch.tensor([0., 1., 1., .25, .75, 1.], dtype=torch.float64, requires_grad=True)
    groups = torch.tensor([3, 3, 3, 7, 7, 7])
    off = torch.tensor([False, False, True, False, False, True])
    advantage = moer.mixed_group_advantages(rewards, groups, off)
    torch.testing.assert_close(advantage, rewards.detach() - torch.tensor([2/3]*6, dtype=torch.float64))
    assert not advantage.requires_grad
    assert advantage[0] != pytest.approx(-math.sqrt(2))
    with pytest.raises(ValueError, match="exactly one"):
        moer.mixed_group_advantages(rewards, torch.zeros(6, dtype=torch.long), off)
    with pytest.raises(ValueError, match="verified"):
        moer.mixed_group_advantages(rewards.detach() * .5, groups, off)


def inputs():
    logits = torch.tensor([[[.2, -.3], [.7, -.4]], [[-1., 1.], [.3, -.8]],
                           [[-.3, .1], [.8, -.2]]], dtype=torch.float64, requires_grad=True)
    actions = torch.tensor([[0, 1], [0, 0], [1, 0]])
    old = logits.detach().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1).requires_grad_()
    rewards = torch.tensor([0., 1., 1.], dtype=torch.float64, requires_grad=True)
    return logits, old, actions, rewards, torch.tensor([0, 0, 0]), torch.tensor([False, False, True]), torch.ones(3, 2, dtype=torch.bool)


def test_eq_4_5_6_scalar_and_gradient_reference_with_global_token_denominator():
    logits, old, actions, rewards, groups, off, mask = inputs()
    mask[0, 1] = False
    loss, audit = moer.moer_loss(logits, old, actions, rewards, groups, off, mask)
    probabilities = logits.softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    advantages = torch.tensor([-2/3, 1/3, 1/3], dtype=torch.float64)[:, None]
    ratio = probabilities / old.detach().exp()
    on_terms = torch.minimum(ratio * advantages, ratio.clamp(.8, 1.24) * advantages)
    off_terms = probabilities / probabilities.detach().clamp_min(.1) * advantages
    expected = -(torch.where(audit["on_mask"], on_terms, 0.) + .2 * torch.where(audit["off_mask"], off_terms, 0.)).sum() / 5
    torch.testing.assert_close(loss, expected, rtol=1e-12, atol=1e-14)
    reference_gradient = torch.autograd.grad(expected, logits, retain_graph=True)[0]
    loss.backward()
    torch.testing.assert_close(logits.grad, reference_gradient, rtol=1e-12, atol=1e-14)
    assert old.grad is None and rewards.grad is None
    assert audit["off_mask"][2].all() and not audit["on_mask"][2].any()
    assert logits.grad[~mask].count_nonzero() == 0


@pytest.mark.parametrize("probability", [.02, .6])
def test_trust_region_has_nonzero_exact_gradient_above_and_below_floor(probability):
    logits = torch.tensor([[[0., 0.]], [[math.log(probability), math.log(1-probability)]]], dtype=torch.float64, requires_grad=True)
    old = torch.tensor([[-math.log(2)], [float("nan")]], dtype=torch.float64, requires_grad=True)
    loss, _ = moer.moer_loss(logits, old, torch.tensor([[0], [0]]), torch.tensor([0., 1.]),
        torch.tensor([0, 0]), torch.tensor([False, True]), torch.ones(2, 1, dtype=torch.bool))
    loss.backward()
    weight = probability / max(probability, .1)
    expected = -.2 * .5 * weight * torch.tensor([1-probability, -(1-probability)], dtype=torch.float64) / 2
    torch.testing.assert_close(logits.grad[1, 0], expected, rtol=1e-12, atol=1e-14)
    assert logits.grad[1].norm() > 0 and old.grad is None


@pytest.mark.parametrize("advantage_sign,ratio_value", [(1, 1.5), (-1, .75)])
def test_asymmetric_clipping_zeroes_only_correct_on_policy_branch(advantage_sign, ratio_value):
    logits, old, actions, rewards, groups, off, mask = inputs()
    row = 1 if advantage_sign > 0 else 0
    with torch.no_grad():
        old[row] -= math.log(ratio_value)
    loss, _ = moer.moer_loss(logits, old, actions, rewards, groups, off, mask)
    loss.backward()
    assert logits.grad[row].count_nonzero() == 0
    assert logits.grad[2].norm() > 0


def test_padding_off_policy_old_and_zero_advantages_cannot_leak_gradients():
    logits, old, actions, rewards, groups, off, mask = inputs()
    mask[0, 1] = False
    with torch.no_grad():
        logits[0, 1] = float("nan")
        old[0, 1] = float("nan")
        old[off] = float("nan")
        actions[0, 1] = -1
    loss, _ = moer.moer_loss(logits, old, actions, rewards, groups, off, mask)
    loss.backward()
    assert logits.grad.isfinite().all() and logits.grad[~mask].count_nonzero() == 0
    zero, _ = moer.moer_loss(logits, old, actions, torch.ones(3), groups, off, mask)
    zero_gradient = torch.autograd.grad(zero, logits)[0]
    assert zero.item() == 0 and zero_gradient.count_nonzero() == 0
    assert old.grad is None and rewards.grad is None


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_is_real_numerical_update_not_capability_measurement(seed):
    result = moer.diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"]
    assert all(result["checks"].values())
    assert all(math.isfinite(v) for v in result["metrics"].values())
    assert result["metrics"]["parameter_delta"] > 0 and result["metrics"]["model_calls"] == 0


def test_moer_metadata_figure_license_cost_and_nonpromotion_boundaries():
    root = Path(__file__).resolve().parents[2]
    catalog = json.loads((root / "src/auto_research/paper_specs/catalog/post-training/moer.json").read_text())
    assert catalog["published_at"] == "2026-10-22T07:54:45Z" and catalog["announced_on"] == "2026-10-23"
    assert catalog["upstream_revision"] == "7dafbe33118e61597a4f0186d538c1630430c0be"
    assert catalog["first_author"] == "Xuyang Zhong" and catalog["first_author_affiliation"] == "City University of Hong Kong"
    assert catalog["code_license"] == "not_confirmed_first_party"
    assert catalog["adapter"] is None and catalog["diagnostic_only"] and not catalog["promotion_eligible"]
    assert not catalog["evolve_integrated"] and not catalog["automatic_retry"] and not catalog["automatic_implementation_queue"]
    assert catalog["review_done"] and catalog["full_experiment_review_done"]
    assert catalog["full_experiment_status"] == "not_reproduced_high_cost"
    assert catalog["requires_gpu_validation"] and catalog["gpu_validation_artifact"] == "docs/gpu-validations/moer-a100-20261024.json"
    folder = root / "docs/post-training/2610.30873-moer"
    readme = (folder / "README.md").read_text()
    for field in ("## 论文信息", "原始发布日期", "公司 / 作者机构", "原作者代码", "原作者代码许可", "本地 Adapter / key", "本地代码", "diagnostic only", "成本过高，不复现（审查 DONE）", "未报告", "evolve_integrated=false"):
        assert field in readme
    provenance = json.loads((folder / "assets/provenance.json").read_text())
    assert provenance["license"] == "CC BY 4.0" and provenance["transformation"] == "rasterization_only"
    assert provenance["image"] == provenance["local_path"] == "paper-figure-01.png"
    assert "assets/paper-figure-01.png" in readme
    assert hashlib.sha256((folder / "assets" / provenance["local_path"]).read_bytes()).hexdigest() == provenance["sha256"]
    assert (folder / "assets" / provenance["local_path"]).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert hashlib.sha256((folder / "assets" / provenance["original_svg_path"]).read_bytes()).hexdigest() == provenance["original_svg_sha256"]
