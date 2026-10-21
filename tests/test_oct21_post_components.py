"""Defining-update tests: frozen coefficients, masks, negative controls."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest
import torch

from auto_research.post_training.oct21_distillation import (
    adaptive_pullback_loss, adaptive_pullback_weights, transition_distillation_loss,
)


@pytest.fixture(scope="module")
def runner():
    path = Path(__file__).resolve().parents[1] / "scripts/run_oct21_post_components.py"
    spec = importlib.util.spec_from_file_location("oct21_post_runner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pullback_uses_original_not_recursively_weighted_profile():
    ratio = torch.tensor([[1., 1., 3., 3., 5., 5.]], dtype=torch.float64, requires_grad=True)
    mask = torch.ones_like(ratio, dtype=torch.bool)
    weights, audit = adaptive_pullback_weights(ratio, mask, block_size=2)
    assert weights.tolist() == [[1., 1., 1 / 3, 1 / 3, 3 / 5, 3 / 5]]
    assert audit["selected_boundaries"] == [[0, 1]]
    assert not weights.requires_grad
    # A recursive profile would incorrectly assign the last block 1/5.
    assert weights[0, -1] != 1 / 5


def test_signed_coefficients_are_scaled_not_clipped_or_shifted():
    s = torch.tensor([[1., 1., -2., 10.]], dtype=torch.float64, requires_grad=True)
    t = torch.zeros_like(s, requires_grad=True)
    loss, audit = adaptive_pullback_loss(s, t, torch.ones_like(s, dtype=torch.bool), block_size=2, z=0)
    assert audit["weights"].tolist() == [[1., 1., .2, .2]]
    loss.backward()
    assert torch.allclose(s.grad, torch.tensor([[.25, .25, -.1, .5]], dtype=torch.float64))
    assert t.grad is None


def test_z_detector_variance_short_block_and_top_alpha():
    ratio = torch.tensor([[1., 3., 2., 4., 10.]], dtype=torch.float64)
    mask = torch.ones_like(ratio, dtype=torch.bool)
    _, z_audit = adaptive_pullback_weights(ratio, mask, block_size=2)
    _, rank_audit = adaptive_pullback_weights(ratio, mask, block_size=2, detector="top-alpha", alpha=.5)
    assert z_audit["selected_boundaries"] == [[]]
    assert rank_audit["selected_boundaries"] == [[1]]


def test_zero_reference_no_floor_and_unchanged_sustained_high_block():
    r = torch.tensor([[0., 0., 3., 3., 3., 3.]])
    w, _ = adaptive_pullback_weights(r, torch.ones_like(r, dtype=torch.bool), block_size=2)
    assert w.tolist() == [[1., 1., 0., 0., 1., 1.]]


def test_padding_inactive_nonfinite_does_not_poison_loss_or_gradient():
    s = torch.tensor([[1., float("nan"), 1., 3., 3., float("inf")]], dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([[True, False, True, True, True, False]])
    loss, audit = adaptive_pullback_loss(s, torch.zeros_like(s), mask, block_size=2)
    assert torch.isfinite(loss)
    loss.backward()
    assert torch.isfinite(s.grad).all()
    assert s.grad[~mask].eq(0).all()
    assert audit["selected_boundaries"] == [[0]]


@pytest.mark.parametrize("kwargs", [{"block_size": 0}, {"block_size": True}, {"z": float("nan")},
                                     {"alpha": 1.1}, {"detector": "magnitude"}])
def test_pullback_invalid_options(kwargs):
    with pytest.raises(ValueError):
        adaptive_pullback_weights(torch.ones(1, 4), torch.ones(1, 4, dtype=torch.bool), **kwargs)


def test_pullback_reference_and_real_updates(runner):
    torch.set_num_threads(1)
    torch.manual_seed(42)
    result = runner.run_method("ap-opd", "cpu", 2)
    assert result["metrics"]["parameter_delta_l2"] > 0
    assert result["metrics"]["loss_reference_max_abs_error"] < 1e-12
    assert result["metrics"]["logit_gradient_reference_max_abs_error"] < 1e-12
    assert result["metrics"]["teacher_parameter_delta_max"] == 0
    assert result["metrics"]["teacher_gradient_count"] == 0
    assert result["metrics"]["staircase_recursive_profile_negative_control_difference"] > .3


def test_optd_scalar_loss_and_analytic_gradient(runner):
    torch.manual_seed(17)
    s = torch.randn(2, 4, 3, 7, dtype=torch.float64, requires_grad=True)
    t = torch.randn_like(s, requires_grad=True)
    loss, audit = transition_distillation_loss(s, t, torch.ones(2, 3, dtype=torch.bool), top_k=4)
    expected, gradients = runner.optd_reference(s.detach().tolist(), t.detach().tolist(), top_k=4)
    assert float(loss.detach()) == pytest.approx(expected, abs=1e-12)
    loss.backward()
    assert torch.allclose(s.grad, torch.tensor(gradients, dtype=torch.float64), atol=1e-12, rtol=1e-10)
    assert s.grad[:, 0].norm() > 0  # Shallow readout receives transition gradients.
    assert t.grad is None
    assert audit["transition_scale"] == 3
    assert not audit["transition_coefficients"].requires_grad


def test_optd_fixed_final_candidates_and_destination_weights():
    s = torch.tensor([[[[8., 0., -1.]], [[0., 8., -1.]], [[-1., 0., 8.]]]], dtype=torch.float64, requires_grad=True)
    t = torch.zeros_like(s)
    _, audit = transition_distillation_loss(s, t, torch.ones(1, 1, dtype=torch.bool), top_k=2)
    assert audit["candidate_ids"].tolist() == [[[2, 1]]]
    # One candidate set across readouts, not a new top-k for each layer.
    assert audit["student_delta"].shape == (1, 2, 1, 2)


def test_optd_tail_selects_last_active_tokens_and_padding_safe():
    torch.manual_seed(7)
    s = torch.randn(2, 3, 5, 6, dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([[True, True, True, True, False], [False, True, False, True, True]])
    with torch.no_grad():
        s.masked_fill_(~mask[:, None, :, None], float("nan"))
    t = torch.randn_like(s)
    loss, audit = transition_distillation_loss(s, t, mask, top_k=3, transition_tail=2)
    assert audit["transition_mask"].tolist() == [[False, False, True, True, False], [False, False, False, True, True]]
    assert torch.isfinite(loss)
    loss.backward()
    assert torch.isfinite(s.grad).all()
    assert s.grad[~mask[:, None, :, None].expand_as(s)].eq(0).all()


@pytest.mark.parametrize("kwargs", [{"top_k": 0}, {"top_k": 7}, {"top_k": True},
                                     {"transition_tail": 0}, {"transition_weight": float("inf")}])
def test_optd_invalid_options(kwargs):
    with pytest.raises(ValueError):
        transition_distillation_loss(torch.zeros(1, 3, 4, 6), torch.zeros(1, 3, 4, 6),
                                     torch.ones(1, 4, dtype=torch.bool), **kwargs)


def test_optd_not_increment_softmax_or_mse(runner):
    torch.set_num_threads(1)
    torch.manual_seed(43)
    result = runner.run_method("optd", "cpu", 2)
    m = result["metrics"]
    assert m["loss_reference_max_abs_error"] < 1e-12
    assert m["logit_gradient_reference_max_abs_error"] < 1e-12
    assert m["negative_control_difference_max"] > 1e-4
    assert m["parameter_delta_l2"] > 0
    assert m["teacher_parameter_delta_max"] == 0


def test_response_empty_and_nonfinite_rejected():
    with pytest.raises(ValueError):
        adaptive_pullback_weights(torch.ones(1, 3), torch.zeros(1, 3, dtype=torch.bool))
    with pytest.raises(ValueError):
        transition_distillation_loss(torch.full((1, 2, 3, 4), float("nan")), torch.zeros(1, 2, 3, 4),
                                     torch.ones(1, 3, dtype=torch.bool), top_k=2)
