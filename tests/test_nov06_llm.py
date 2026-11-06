"""Paper-component tests; no models or benchmark data are loaded."""

import math
from random import Random

import pytest

from auto_research.post_training.cord_rollout import diagnostic as cord_diagnostic, maximal_coupling


def test_convpe_exact_tap_lag_and_head_mapping():
    torch = pytest.importorskip("torch")
    from auto_research.foundation_models.convpe import ConvPEBias

    layer = ConvPEBias(1, 1, 2, 4, 2).double()
    with torch.no_grad():
        layer.projection.weight.fill_(1)
        layer.convolution.weight.copy_(torch.tensor([[[10, 1]], [[1, 2]], [[0, 3]], [[2, 0]]]))
        layer.convolution.bias.copy_(torch.tensor([0, 0, 1, -1]))
    x = torch.tensor([[[1.0], [2.0], [3.0]]], dtype=torch.float64, requires_grad=True)
    first = [[1, 0, 0], [5, 12, 0], [0, 8, 23]]
    second = [[4, 0, 0], [1, 7, 0], [0, 3, 10]]
    expected = torch.tensor([[first, second, first, second]], dtype=x.dtype)
    bias = layer(x)
    torch.testing.assert_close(bias, expected, rtol=0, atol=0)
    assert layer.compact_bias(x).shape == (1, 3, 2, 2)
    grad = torch.autograd.grad(bias[:, :, 1].sum(), x)[0]
    assert bool((grad[:, :2] != 0).all())
    assert grad[0, 2].item() == 0
    torch.testing.assert_close(
        layer(x[:, 2:], query_start=2, history=x[:, 1:2]), bias[:, :, 2:],
    )


def test_convpe_requires_history_at_absolute_offset():
    torch = pytest.importorskip("torch")
    from auto_research.foundation_models.convpe import ConvPEBias

    with pytest.raises(ValueError, match="divide"):
        ConvPEBias(3, 2, 3, 3, 2)
    layer = ConvPEBias(3, 2, 3, 2, 1)
    x = torch.zeros((1, 4, 3))
    with pytest.raises(ValueError, match="exactly"):
        layer(x[:, 3:], query_start=3, history=x[:, 2:3])
    with pytest.raises(ValueError, match="at most"):
        layer(x[:, 3:], query_start=3, history=x[:, :3])
    with pytest.raises(ValueError, match="nonnegative"):
        layer(x, query_start=-1)
    with pytest.raises(ValueError, match="nonempty"):
        layer(x[:, :0])


def test_convpe_window_one_perturbing_other_positions_changes_no_local_score():
    torch = pytest.importorskip("torch")
    from auto_research.foundation_models.convpe import ConvPEBias

    layer = ConvPEBias(2, 1, 1, 2, 1).double()
    x = torch.ones(1, 4, 2, dtype=torch.float64)
    changed = x.clone()
    changed[:, [0, 1, 3]] = 200
    torch.testing.assert_close(layer(x)[:, :, 2], layer(changed)[:, :, 2])
    torch.testing.assert_close(layer(x[:, 2:3], query_start=2), layer(x)[:, :, 2:3, :3])
    assert int(layer(x).triu(1).count_nonzero()) == 0


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_convpe_diagnostic_cpu(seed):
    pytest.importorskip("torch")
    from auto_research.foundation_models.convpe import diagnostic

    result = diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(check is True for check in result["checks"].values())


def test_cord_interpolates_in_log_space_and_uses_exact_residual():
    p, t = (0.6, 0.3, 0.1), (0.2, 0.3, 0.5)
    coupling = maximal_coupling(p, t, 0.6)
    target = (0.3555112609216215, 0.3435799614878549, 0.3009087775905235)
    assert coupling.target == pytest.approx(target, abs=4e-4)
    marginal = tuple(
        a * keep + r
        for a, keep, r in zip(p, coupling.keep_probabilities, coupling.residual, strict=True)
    )
    assert marginal == pytest.approx(coupling.target, abs=1e-14)
    assert coupling.replacement_probability == pytest.approx(
        math.fsum(abs(a-b) for a, b in zip(p, coupling.target, strict=True)) / 2,
    )
    assert coupling.residual[0] == 0
    assert all(mass > 0 for mass in coupling.residual[1:])
    # Uniform replacements would put mass back on an already overweight token.
    wrong_first = p[0] * coupling.keep_probabilities[0] + coupling.replacement_probability / 3
    assert wrong_first > coupling.target[0]


def test_cord_endpoint_preserves_student_rng_and_handles_zero_support():
    p, t = (0.6, 0.4, 0), (0.0, 0.0, 1.0)
    with pytest.raises(ValueError, match="disjoint"):
        maximal_coupling(p, t, 0.5)
    student = maximal_coupling(p, t, 0)
    actual_rng, expected_rng = Random(9), Random(9)
    actual = [student.draw(actual_rng) for _ in range(32)]
    expected = expected_rng.choices(range(3), p, k=32)
    assert [draw.token for draw in actual] == expected
    assert not any(draw.replaced for draw in actual)
    assert actual_rng.getstate() == expected_rng.getstate()
    teacher = maximal_coupling(p, t, 1)
    for _ in range(20):
        assert teacher.draw(actual_rng).token == 2
    assert teacher.replacement_probability == 1


def test_cord_zero_mass_at_interior_alpha_and_equal_policies():
    p, t = (0.6, 0.4, 0), (0.0, 0.2, 0.8)
    coupling = maximal_coupling(p, t, 0.5)
    assert coupling.target == (0, 1, 0)
    assert coupling.replacement_probability == pytest.approx(0.6)
    rng = Random(1)
    assert all(coupling.draw(rng).token == 1 for _ in range(20))
    equal = maximal_coupling(t, t, 0.6)
    assert equal.target == t and equal.replacement_probability == 0


@pytest.mark.parametrize(
    "p,t,alpha",
    [
        ([], [], 0.5),
        ([1], [0.5, 0.5], 0.5),
        ([0.5, 0.4], [0.5, 0.5], 0.5),
        ([float("nan"), 1], [0.5, 0.5], 0.5),
        ([-0.1, 1.1], [0.5, 0.5], 0.5),
        ([0.5, 0.5], [0.5, 0.5], -0.01),
        ([0.5, 0.5], [0.5, 0.5], float("nan")),
    ],
)
def test_cord_rejects_invalid_distribution(p, t, alpha):
    with pytest.raises(ValueError):
        maximal_coupling(p, t, alpha)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cord_diagnostic_cpu(seed):
    result = cord_diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(check is True for check in result["checks"].values())


def test_cord_does_not_accept_a_cuda_claim():
    with pytest.raises(ValueError, match="CPU-only"):
        cord_diagnostic(42, device="cuda")
