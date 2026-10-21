from __future__ import annotations

import json
import math
from pathlib import Path
import subprocess
import sys

import pytest
import torch

from auto_research.multimodal.mice import (
    instance_aware_masks, instance_log_bias, mice_joint_attention,
    mice_joint_bias, run_mice_diagnostic,
)


def example_masks(dtype=torch.float32):
    masks = torch.zeros(2, 3, 5, dtype=dtype)
    masks[0, 1, 1] = 1
    masks[1, 1, 3] = 1
    return masks


def test_gaussian_smoothing_matches_independent_scalar_convolution():
    masks = example_masks(torch.float64)
    actual = instance_aware_masks(masks)
    sigma = .8
    normalizer = sum(math.exp(-(i*i+j*j)/(2*sigma*sigma))
                     for i in range(-1, 2) for j in range(-1, 2))
    expected = torch.zeros_like(masks)
    for n, origin in enumerate((1, 3)):
        for y in range(3):
            for x in range(5):
                dx, dy = x-origin, y-1
                if abs(dx) <= 1 and abs(dy) <= 1:
                    expected[n, y, x] = math.exp(-(dx*dx+dy*dy)/(2*sigma*sigma))/normalizer
    expected[0, 1, 3] = expected[1, 1, 1] = 0
    torch.testing.assert_close(actual, expected)
    assert actual[0, 1, 2] > 0


def test_instance_aware_smoothing_removes_other_object_not_background():
    masks = example_masks()
    result = instance_aware_masks(masks, kernel_size=5)
    assert result[0, 1, 3] == 0 and result[1, 1, 1] == 0
    assert result[0, 1, 2] > 0 and result[1, 1, 2] > 0
    assert result[0, 1, 1] > 0


def test_paper_log_epsilon_temperature_and_strict_own_region():
    masks = example_masks()
    bias = instance_log_bias(masks, temperature=8)
    smooth = instance_aware_masks(masks)
    assert bias[0, 1, 1] == 0
    torch.testing.assert_close(bias[0, 1, 2], smooth[0, 1, 2].log()/8)
    assert bias[0, 1, 3] == pytest.approx(math.log(1e-30)/8)
    assert torch.isfinite(bias).all()
    torch.testing.assert_close(instance_log_bias(masks, temperature=2), 4*bias)


def test_default_temperature_is_mice_bench_eight_not_inverse_eighth():
    masks = example_masks()
    default = instance_log_bias(masks)
    explicit_eight = instance_log_bias(masks, temperature=8.0)
    lomoe_one = instance_log_bias(masks, temperature=1.0)
    mistaken_inverse = instance_log_bias(masks, temperature=1.0/8.0)
    torch.testing.assert_close(default, explicit_eight)
    torch.testing.assert_close(lomoe_one, 8*default)
    torch.testing.assert_close(mistaken_inverse, 64*default)
    groups = torch.tensor([0, 1, 2])
    torch.testing.assert_close(mice_joint_bias(masks, groups),
                               mice_joint_bias(masks, groups, temperature=8.0))


def test_low_precision_masks_do_not_underflow_paper_epsilon():
    for dtype in (torch.float16, torch.bfloat16):
        bias = instance_log_bias(example_masks(dtype), kernel_size=1)
        assert bias.dtype == torch.float32 and torch.isfinite(bias).all()
        assert bias[0, 1, 3] == pytest.approx(math.log(1e-30)/8)


def test_all_paper_joint_blocks_and_deliberate_context_asymmetry():
    masks = torch.tensor([[[0, 1, 0, 0]], [[0, 0, 0, 1]]])
    groups = torch.tensor([0, 1, 2])
    b = mice_joint_bias(masks, groups)
    # Prompt 0/1/2, latent 3..6, context 7..10. Background raster positions 0,2.
    torch.testing.assert_close(b[:3, :3], torch.eye(3).log())
    assert (b[0, 3:] == 0).all()                         # global -> all visual
    assert (b[[3, 5], 3:] == 0).all()                    # background latent -> visual
    assert (b[[3, 5], 0] == 0).all()                     # background -> global
    assert (b[7:, 3:] == 0).all() and (b[7:, 0] == 0).all()  # context -> visual/global
    assert b[8, 1] == 0 and b[10, 2] == 0                # context -> own text
    assert torch.isneginf(b[7, 1]) and torch.isneginf(b[8, 2])
    assert b[1, 4] == 0 and b[1, 8] == 0                # own local text -> latent/context
    assert b[4, 1] == 0 and not bool(torch.isneginf(b[4, 2]))
    assert torch.isneginf(b[4, 0])                       # edited latent cannot read global text
    assert b[4, 10] == pytest.approx(math.log(1e-30)/8)   # finite paper epsilon across instances
    assert b[10, 4] == 0                                # context row is NOT mirrored
    assert (b[4, [4, 8]] == 0).all()


def test_local_prompt_rows_and_latent_to_prompt_are_spatially_soft():
    masks = example_masks()
    groups = torch.tensor([0, 1, 1, 2])
    b = mice_joint_bias(masks, groups, temperature=1)
    local = instance_log_bias(masks, temperature=1).flatten(1)
    area, start = 15, 4
    torch.testing.assert_close(b[1, start:start+area], local[0])
    torch.testing.assert_close(b[start:start+area, 1], local[0])
    assert b[1, start+7] < 0 and b[1, start+7] > math.log(1e-30)


def test_global_prompt_optional_and_group_order_not_assumed():
    masks = example_masks()
    b = mice_joint_bias(masks, torch.tensor([2, 1, 2, 1]))
    assert b.shape == (34, 34)
    assert torch.isfinite(b).any(dim=-1).all()
    assert b[0, 2] == 0 and torch.isneginf(b[0, 1])


def test_joint_attention_equals_formula_and_preserves_trainable_qkv():
    g = torch.Generator().manual_seed(42)
    b = mice_joint_bias(example_masks(), torch.tensor([0, 1, 2]))
    q, k, v = [torch.randn(2, len(b), 4, generator=g, requires_grad=True) for _ in range(3)]
    actual, weights = mice_joint_attention(q, k, v, b, return_weights=True)
    expected = torch.softmax(q @ k.transpose(-1, -2)/2 + b, dim=-1) @ v
    torch.testing.assert_close(actual, expected)
    assert (weights[:, 0, 1:3] == 0).all()
    actual.square().sum().backward()
    for x in (q, k, v):
        assert torch.isfinite(x.grad).all() and x.grad.norm() > 0
    changed = v.detach().clone()
    changed[:, 2] += 1000
    altered = mice_joint_attention(q.detach(), k.detach(), changed, b)
    torch.testing.assert_close(altered[:, 1], actual.detach()[:, 1])


@pytest.mark.parametrize("dtype", [torch.float16, torch.bfloat16])
def test_joint_attention_low_precision_is_finite(dtype):
    b = mice_joint_bias(example_masks(dtype), torch.tensor([0, 1, 2]))
    q = torch.randn(2, len(b), 4).to(dtype).requires_grad_(True)
    out = mice_joint_attention(q, q, q, b)
    assert out.dtype == dtype and torch.isfinite(out).all()
    out.float().square().mean().backward()
    assert torch.isfinite(q.grad).all()


@pytest.mark.parametrize("kernel", [0, 2, -1, True, 3.5])
def test_bad_kernels_fail_closed(kernel):
    with pytest.raises(ValueError):
        instance_aware_masks(example_masks(), kernel_size=kernel)


@pytest.mark.parametrize("setting", [{"temperature": 0}, {"temperature": float("nan")},
                                     {"epsilon": 0}, {"epsilon": 1}, {"epsilon": 1e-100}])
def test_bad_log_parameters_fail_closed(setting):
    with pytest.raises(ValueError):
        instance_log_bias(example_masks(), **setting)


def test_invalid_masks_and_prompt_ownership_fail_closed():
    good = example_masks()
    bad = [torch.zeros(0, 2, 2), torch.zeros(2, 2), torch.full((2, 2, 2), float("nan")),
           good*.5, torch.zeros_like(good), torch.ones(2, 2, 2)]
    for masks in bad:
        with pytest.raises(ValueError):
            instance_aware_masks(masks)
    for groups in (torch.tensor([0, 1]), torch.tensor([0, 1, 3]), torch.tensor([0., 1., 2.]),
                   torch.tensor([False, True]), torch.tensor([[0, 1, 2]])):
        with pytest.raises(ValueError):
            mice_joint_bias(good, groups)


def test_invalid_attention_and_all_masked_rows_fail_closed():
    q = torch.randn(2, 4, 3)
    for b in (torch.zeros(3, 3), torch.full((4, 4), -torch.inf),
              torch.full((4, 4), float("nan")), torch.ones(4, 4)):
        with pytest.raises(ValueError):
            mice_joint_attention(q, q, q, b)
    with pytest.raises(ValueError):
        mice_joint_attention(q, q[..., :-1], q, torch.zeros(4, 4))


def test_diagnostic_is_reproducible_and_not_a_capability_benchmark():
    result = run_mice_diagnostic(42)
    assert result == run_mice_diagnostic(42)
    assert result["diagnostic_only"] and not result["promotion_eligible"]
    assert not result["evolve_integrated"] and result["pretrained_model_calls"] == 0
    assert result["metrics"]["cross_prompt_probability_max"] == 0
    assert result["metrics"]["q_gradient_norm"] > 0
    assert all(result["checks"].values())
    assert result["metrics"]["removed_mask_mean_square_delta"] > 0
    assert result["metrics"]["removed_log_bias_mean_square_delta"] > 0
    assert result["recipe"]["implementation_policy"] == "paper_v1"
    json.dumps(result, allow_nan=False)


def test_module_import_does_not_require_torch():
    root = Path(__file__).resolve().parents[1]
    code = """
import importlib.abc, sys
class NoTorch(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'torch':
            raise AssertionError('torch imported eagerly')
sys.meta_path.insert(0, NoTorch())
from auto_research.multimodal import mice
assert mice.PAPER_ID == '2606.31278v1'
"""
    subprocess.run([sys.executable, "-c", code], cwd=root, check=True)
