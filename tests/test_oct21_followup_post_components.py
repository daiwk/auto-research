"""Independent formulas, negative controls and privacy-of-target boundaries."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import torch

from auto_research.post_training.oct21_followup_distillation import (
    a2d_candidate_opd_loss, a2d_question_reward, a2d_token_signal,
    calibrate_a2d_scale, minimal_edit_masks, projected_distillation_loss, verified_edit_masks,
)


@pytest.fixture(scope="module")
def runner():
    path = Path(__file__).resolve().parents[1] / "scripts/run_oct21_followup_post_components.py"
    spec = importlib.util.spec_from_file_location("followup_post_runner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_a2d_union_not_intersection_and_teacher_mass_not_renormalized(runner):
    s = torch.tensor([[[4., 3., 0., -1.]]], dtype=torch.float64)
    t = torch.tensor([[[-1., 0., 3., 4.]]], dtype=torch.float64)
    m = torch.ones(1, 1, dtype=torch.bool)
    result = a2d_token_signal(s, t, m, top_k=2)
    ds, cs = runner.scalar_a2d_reference(s[0].tolist(), t[0].tolist(), 2)
    assert result["union_support"].all()
    assert result["discrepancy"].item() == pytest.approx(ds[0], abs=1e-12)
    assert result["compatibility"].item() == pytest.approx(cs[0], abs=1e-12)
    assert 0 < result["compatibility"].item() < .05


def test_a2d_pool_calibration_and_reward_factors_detached():
    d = torch.tensor([[0., 1., 2.], [3., 4., float("nan")]], requires_grad=True)
    mask = torch.tensor([[True, True, True], [True, True, False]])
    ref = calibrate_a2d_scale(d, mask)
    assert ref.item() == pytest.approx(3.8)
    assert not ref.requires_grad
    s, t = torch.randn(2, 3, 5, requires_grad=True), torch.randn(2, 3, 5, requires_grad=True)
    reward, audit = a2d_question_reward(s, t, mask, torch.tensor([.5, 1.]), top_k=2,
        delta_ref=float(ref), response_budget=3)
    assert not reward.requires_grad
    assert reward[1].item() == 0  # entire batch cluster gets zero when share=1.
    assert audit["length_factor"][0].item() == pytest.approx(.7)


def test_a2d_padding_nan_does_not_poison_reward_or_update():
    s = torch.randn(1, 3, 6, dtype=torch.float64, requires_grad=True)
    t, old = torch.randn_like(s, requires_grad=True), torch.randn_like(s, requires_grad=True)
    mask = torch.tensor([[True, True, False]])
    with torch.no_grad():
        s[:, -1], t[:, -1], old[:, -1] = float("nan"), float("inf"), float("nan")
    reward, _ = a2d_question_reward(old, t, mask, torch.tensor([.5]), top_k=3, delta_ref=.2, response_budget=3)
    loss, audit = a2d_candidate_opd_loss(s, old, t, mask, top_k=3)
    loss.backward()
    assert torch.isfinite(reward).all() and torch.isfinite(loss)
    assert torch.isfinite(s.grad).all() and s.grad[~mask].eq(0).all()
    assert t.grad is None and old.grad is None and not audit["fixed_advantage"].requires_grad


def test_a2d_clipping_uses_signed_minimum_not_clipped_advantage():
    old = torch.tensor([[[2., 1., 0.]]], dtype=torch.float64, requires_grad=True)
    current = torch.tensor([[[4., -2., -1.]]], dtype=torch.float64, requires_grad=True)
    teacher = torch.tensor([[[0., 3., 1.]]], dtype=torch.float64, requires_grad=True)
    mask = torch.ones(1, 1, dtype=torch.bool)
    loss, a = a2d_candidate_opd_loss(current, old, teacher, mask, top_k=2)
    ratio, advantage = a["probability_ratio"], a["fixed_advantage"]
    expected = -torch.minimum(ratio * advantage, ratio.clamp(.8, 1.2) * advantage).sum()
    assert torch.allclose(loss, expected)
    loss.backward()
    assert current.grad.norm() > 0 and old.grad is None and teacher.grad is None


@pytest.mark.parametrize("options", [{"top_k": True}, {"top_k": 0}, {"top_k": 8}, {"clip": float("nan")}])
def test_a2d_invalid_update_options(options):
    with pytest.raises(ValueError):
        a2d_candidate_opd_loss(torch.zeros(1, 2, 4), torch.zeros(1, 2, 4), torch.zeros(1, 2, 4), torch.ones(1, 2, dtype=torch.bool), **options)


@pytest.mark.parametrize("options", [{"delta_ref": -1.}, {"delta_ref": float("nan")}, {"response_budget": 1}, {"diversity_weight": -1.}])
def test_a2d_invalid_reward_options(options):
    options = {"delta_ref": .1, **options}
    with pytest.raises(ValueError):
        a2d_question_reward(torch.zeros(1, 2, 4), torch.zeros(1, 2, 4), torch.ones(1, 2, dtype=torch.bool), torch.tensor([.5]), top_k=2, **options)


@pytest.mark.parametrize(("old", "new", "expected"), [
    ([1, 2, 3, 4], [1, 7, 3, 8], ([False, True, False, True], [False, True, False, True])),
    ([1, 2], [1, 9, 2], ([False, False], [False, True, False])),
    ([1, 9, 2], [1, 2], ([False, True, False], [False, False])),
    ([], [1], ([], [True])), ([1], [], ([True], [])),
])
def test_exact_edit_masks_cover_disjoint_changes_insertions_and_deletions(old, new, expected):
    assert minimal_edit_masks(old, new) == expected


def test_projection_verifier_rejects_bad_pairs_and_no_model_access():
    with pytest.raises(ValueError):
        verified_edit_masks([1], [2], lambda x: x == [1])
    with pytest.raises(ValueError):
        verified_edit_masks([1], [2], lambda _: False)
    assert verified_edit_masks([1], [2], lambda x: x == [2]) == ([True], [True])


def test_diff_local_loss_gradient_reference_freeze_and_self_correct_not_projection_sft():
    p = torch.tensor([[-1., -2., -3.]], dtype=torch.float64, requires_grad=True)
    n = torch.tensor([[-2., -3., -4.]], dtype=torch.float64, requires_grad=True)
    rp, rn = torch.full_like(p, -2., requires_grad=True), torch.full_like(n, -3., requires_grad=True)
    pm, nm = torch.tensor([[False, True, False]]), torch.tensor([[False, True, False]])
    own = torch.tensor([[-1., -2.]], dtype=torch.float64, requires_grad=True)
    loss, audit = projected_distillation_loss(p, n, rp, rn, pm, nm,
        self_correct_log_probs=own, self_correct_mask=torch.ones_like(own, dtype=torch.bool))
    assert loss.item() == pytest.approx(torch.nn.functional.softplus(torch.tensor(0.)).item() + 3, abs=1e-7)
    loss.backward()
    assert torch.allclose(p.grad, torch.tensor([[0., -.05, 0.]], dtype=torch.float64))
    assert torch.allclose(n.grad, torch.tensor([[0., .05, 0.]], dtype=torch.float64))
    assert rp.grad is None and rn.grad is None and own.grad.eq(-1).all()
    assert audit["sft_target"] == "student_own_verified_correct"


def test_one_sided_edit_and_inactive_nonfinite_are_supported():
    p = torch.tensor([[-1., float("nan")]], requires_grad=True)
    n = torch.tensor([[-2., float("inf")]], requires_grad=True)
    loss, _ = projected_distillation_loss(p, n, torch.zeros_like(p), torch.zeros_like(n),
        torch.tensor([[True, False]]), torch.tensor([[False, False]]))
    loss.backward()
    assert torch.isfinite(loss) and torch.isfinite(p.grad).all() and torch.isfinite(n.grad).all()
    assert n.grad.eq(0).all()


def test_no_edit_rejected_and_projection_sft_not_silently_added():
    p, n = torch.full((1, 2), -1.), torch.full((1, 2), -2.)
    with pytest.raises(ValueError):
        projected_distillation_loss(p, n, p, n, torch.zeros_like(p, dtype=torch.bool), torch.zeros_like(n, dtype=torch.bool))
    loss, audit = projected_distillation_loss(p, n, p, n, torch.ones_like(p, dtype=torch.bool), torch.ones_like(n, dtype=torch.bool))
    assert loss.item() == pytest.approx(.69314718)
    assert audit["self_correct_sft_loss"].item() == 0


@pytest.mark.parametrize("method", ["run_a2d", "run_projected"])
def test_complete_small_component_diagnostic(runner, method):
    torch.set_num_threads(1)
    torch.manual_seed(42)
    result = getattr(runner, method)("cpu")
    assert all(result["checks"].values())
    assert result["metrics"]["gradient_reference_max_abs_error"] < 1e-10
