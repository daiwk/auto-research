"""ALPS bounded components: independent formulas, isolation and real gradients."""
import importlib
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest

torch = pytest.importorskip("torch")
from auto_research.foundation_models.alps import (
    crossview_geometry, crossview_loss_from_pred, diagnostic, geometry_queries,
    sincos_2d, stage2_objective, teacher_targets,
)


def test_minimal_import_does_not_load_torch():
    code = "import sys; import auto_research.foundation_models.alps; assert 'torch' not in sys.modules"
    subprocess.run([sys.executable, "-c", code], check=True)


def test_equal_full_crops_default_grid_and_axis_order():
    box = torch.tensor([[0., 0., 1.]])
    positions, valid, ratio = crossview_geometry(box, box)
    assert positions.shape == (1, 196, 2)
    torch.testing.assert_close(positions[0, :3], torch.tensor([[.5, .5], [.5, 1.5], [.5, 2.5]]))
    torch.testing.assert_close(positions[0, 14], torch.tensor([1.5, .5]))
    assert valid.all() and ratio.item() == 0


def test_geometry_matches_independent_scalar_formula_and_half_open_edges():
    a = torch.tensor([[.25, .25, .5], [0., 0., 1.]])
    b = torch.tensor([[0., 0., 1.], [.25, .25, .5]])
    positions, valid, ratio = crossview_geometry(a, b, 2)
    # B's first center equals A's lower boundary; last equals upper boundary.
    assert valid[0].tolist() == [True, False, False, False]
    for batch in range(2):
        for y in range(2):
            for x in range(2):
                yy = (float(b[batch, 0]) + (y+.5)/2*float(b[batch, 2]) - float(a[batch, 0])) / float(a[batch, 2])
                xx = (float(b[batch, 1]) + (x+.5)/2*float(b[batch, 2]) - float(a[batch, 1])) / float(a[batch, 2])
                torch.testing.assert_close(positions[batch, y*2+x], torch.tensor([2*yy, 2*xx]))
                assert bool(valid[batch, y*2+x]) == (0 <= yy < 1 and 0 <= xx < 1)
        assert float(ratio[batch]) == pytest.approx(math.log(float(b[batch, 2]/a[batch, 2])))


@pytest.mark.parametrize("box", [
    [[0., 0., 0.]], [[0., 0., -.1]], [[-.1, 0., .5]], [[0., .5, .6]],
    [[float('nan'), 0., .5]], [[0., float('inf'), .5]], [[0., 1.]],
])
def test_invalid_boxes_rejected(box):
    with pytest.raises(ValueError):
        crossview_geometry(torch.tensor(box), torch.tensor([[0., 0., 1.]]))


@pytest.mark.parametrize("grid", [0, -1, True, 1.5])
def test_invalid_grid_rejected(grid):
    with pytest.raises(ValueError):
        crossview_geometry(torch.tensor([[0., 0., 1.]]), torch.tensor([[0., 0., 1.]]), grid)


def test_batch_mismatch_rejected():
    with pytest.raises(ValueError, match="same batch"):
        crossview_geometry(torch.tensor([[0., 0., 1.]]), torch.tensor([[0., 0., 1.], [0., 0., 1.]]))


def test_sincos_frequency_denominator_and_y_first_order():
    p = torch.tensor([[[2., 3.]]])
    actual = sincos_2d(p, 8)
    expected = [math.sin(2), math.sin(.02), math.cos(2), math.cos(.02),
                math.sin(3), math.sin(.03), math.cos(3), math.cos(.03)]
    torch.testing.assert_close(actual[0, 0], torch.tensor(expected))


@pytest.mark.parametrize("width", [0, 2, 5, True])
def test_invalid_position_width_rejected(width):
    with pytest.raises(ValueError):
        sincos_2d(torch.ones(1, 2), width)


def test_geometry_queries_include_log_squared_affine_bias_and_gradients():
    positions = torch.tensor([[[.5, .5], [1.5, 2.5]]])
    log_ratio = torch.tensor([math.log(2)])
    m = torch.arange(8.).requires_grad_()
    weight = torch.arange(16.).reshape(8, 2).requires_grad_()
    bias = torch.ones(8, requires_grad=True)
    result = geometry_queries(positions, log_ratio, m, weight, bias)
    expected = m + sincos_2d(positions, 8) + bias + weight[:, 0]*math.log(2) + weight[:, 1]*math.log(2)**2
    torch.testing.assert_close(result, expected)
    result.square().sum().backward()
    assert all(x.grad is not None and torch.isfinite(x.grad).all() for x in (m, weight, bias))


def test_query_parameter_mismatch_rejected():
    with pytest.raises(ValueError, match="shape mismatch"):
        geometry_queries(torch.zeros(2, 4, 2), torch.zeros(1), torch.zeros(8), torch.ones(8, 2), torch.zeros(8))


def test_teacher_uses_fixed_stats_without_gradients_or_mutation():
    z = torch.arange(12.).reshape(2, 2, 3).requires_grad_()
    mean = torch.tensor([1., 2., 3.], requires_grad=True)
    std = torch.tensor([1., 2., 4.], requires_grad=True)
    before = (mean.detach().clone(), std.detach().clone())
    target = teacher_targets(z, mean, std)
    torch.testing.assert_close(target, (z.detach()-mean.detach())/std.detach())
    assert not target.requires_grad and target.grad_fn is None
    torch.testing.assert_close(mean.detach(), before[0])
    torch.testing.assert_close(std.detach(), before[1])


@pytest.mark.parametrize("std", [[1., 0.], [1., -.1], [1., float('nan')]])
def test_invalid_fixed_teacher_std_rejected(std):
    with pytest.raises(ValueError):
        teacher_targets(torch.ones(1, 2, 2), torch.zeros(2), torch.tensor(std))


def test_per_image_loss_is_not_global_valid_token_average():
    pred = torch.tensor([[[1.], [3.]], [[10.], [99.]]], requires_grad=True)
    target = torch.zeros_like(pred, requires_grad=True)
    valid = torch.tensor([[True, True], [True, False]])
    loss = crossview_loss_from_pred(pred, target, valid)
    assert loss.item() == pytest.approx(((1+9)/2+100)/2)
    assert loss.item() != pytest.approx((1+9+100)/3)
    loss.backward()
    torch.testing.assert_close(pred.grad, torch.tensor([[[.5], [1.5]], [[10.], [0.]]]))
    assert target.grad is None


def test_zero_overlap_image_is_zero_contribution_with_safe_denominator():
    prediction = torch.tensor([[[3.]], [[7.]]], requires_grad=True)
    loss = crossview_loss_from_pred(prediction, torch.zeros_like(prediction), torch.tensor([[False], [True]]))
    assert loss.item() == pytest.approx(24.5)
    loss.backward()
    assert prediction.grad[0].item() == 0


def test_all_masked_is_differentiable_zero_not_nan():
    prediction = torch.randn(2, 3, 4, requires_grad=True)
    loss = crossview_loss_from_pred(prediction, torch.randn_like(prediction), torch.zeros(2, 3, dtype=torch.bool))
    loss.backward()
    assert loss.item() == 0 and torch.equal(prediction.grad, torch.zeros_like(prediction))


@pytest.mark.parametrize("bad_mask", [torch.ones(1, 2), torch.ones(1, 3, dtype=torch.bool)])
def test_loss_mask_must_be_boolean_and_aligned(bad_mask):
    with pytest.raises(ValueError):
        crossview_loss_from_pred(torch.ones(1, 2, 3), torch.ones(1, 2, 3), bad_mask)


def test_nonfinite_tokens_rejected_even_if_masked():
    with pytest.raises(ValueError):
        crossview_loss_from_pred(torch.full((1, 2, 3), float('nan')), torch.zeros(1, 2, 3),
                                torch.zeros(1, 2, dtype=torch.bool))


def test_external_token_objective_matches_separate_components():
    pred = torch.arange(16.).reshape(1, 4, 4).requires_grad_()
    teacher = torch.ones_like(pred, requires_grad=True)
    box = torch.tensor([[0., 0., 1.]])
    loss = stage2_objective(pred, teacher, box, box, torch.ones(4), torch.full((4,), 2.), grid=2)
    torch.testing.assert_close(loss, pred.square().mean())
    loss.backward()
    assert pred.grad is not None and teacher.grad is None


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_formula_gradients_and_negative_controls(seed):
    result = diagnostic(seed)
    assert result["seed"] == seed and result["device"] == "cpu"
    assert all(result["checks"].values())
    assert result["evaluation_tier"] == "l1_mechanism"
    assert not result["promotion_eligible"] and not result["evolve_integrated"]
    assert result["pretrained_model_calls"] == 0
    assert result["full_experiment_status"] == "not_reproduced_high_cost"
    assert all(math.isfinite(value) for value in result["metrics"].values())


def test_catalog_keeps_component_and_high_cost_full_model_separate():
    root = Path(__file__).resolve().parents[1]
    path = root/"src/auto_research/paper_specs/catalog/foundation-models/alps.json"
    metadata = json.loads(path.read_text())
    assert metadata["upstream_revision"] == importlib.import_module("auto_research.foundation_models.alps").UPSTREAM_REVISION
    assert metadata["implementation_status"] == "component_only" and metadata["diagnostic_only"]
    assert not metadata["promotion_eligible"] and metadata["requires_gpu_validation"]
    assert metadata["full_experiment_status"] == "not_reproduced_high_cost"
