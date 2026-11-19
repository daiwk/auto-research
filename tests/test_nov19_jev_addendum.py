"""EgoJev postprocessing formula tests, without a VLM or gold answers."""

import math
import pytest

from auto_research.system_one import egojev_components as ego


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic(seed):
    result = ego.diagnostic(seed)
    assert result["evaluation_tier"] == "l1_mechanism" and result["diagnostic_only"] is True
    assert all(type(v) is bool and v for v in result["checks"].values())
    assert all(type(v) in (int, float) and math.isfinite(v) for v in result["metrics"].values())
    assert ego.REQUIRES_GPU_VALIDATION is False


def test_literal_window_mass_geometric_fusion_not_plain_product():
    p = (0.1, 0.1, 0.3, 0.5)
    assert ego.window_probabilities(p, 2) == pytest.approx((0.2, 0.8))
    fine = (0.05, 0.05, 0.05, 0.05, 0.8, 0, 0, 0)
    expected = [math.sqrt(p[s // 2] * v) for s, v in enumerate(fine)]
    expected = [v / sum(expected) for v in expected]
    actual = ego.fuse_readouts(p, 2, {1: (1.0, 0.0, 0.0, 0.0)})
    assert actual == pytest.approx(expected)
    assert actual[5:] == (0.0, 0.0, 0.0)
    assert ego.fuse_readouts(p, 2, {}) == p
    with pytest.raises(ValueError):
        ego.fuse_readouts(p, 2, {0: (1.0, 0.0, 0.0, 0.0)})


def test_piecewise_uniform_quantiles_interpolate_and_skip_zero_bins():
    assert ego.quantile_times((0.0, 1.0), 10.0, 2) == (6.25, 8.75)
    assert ego.quantile_times((0.5, 0.0, 0.5), 3.0, 2) == (0.5, 2.5)
    # At a CDF plateau choose the left generalized inverse, not the next bin.
    assert ego.quantile_times((0.5, 0.0, 0.5), 3.0, 1) == (1.0,)
    assert ego.quantile_times((1.0, 0.0, 0.0, 0.0), 8.0, 4) == (0.25, 0.75, 1.25, 1.75)


def test_tiny_overlap_does_not_underflow_into_false_disjoint_support():
    out = ego.fuse_readouts((1e-200, 0.0, 1.0), 1, {0: (1e-200, 1.0, 0.0)})
    assert out == (1.0, 0.0, 0.0)
    with pytest.raises(ValueError, match="disjoint support"):
        ego.fuse_readouts((0.0, 0.0, 1.0), 1, {0: (1.0, 0.0, 0.0)})


@pytest.mark.parametrize("bad", [[], [0.0, 0.0], [-1.0, 2.0], [True, 1.0], [float("nan"), 1.0]])
def test_invalid_probabilities(bad):
    with pytest.raises(ValueError):
        ego.quantile_times(bad, 10.0, 2)


def test_strict_window_and_cpu_contract():
    with pytest.raises(ValueError):
        ego.fuse_readouts([1.0, 1.0, 1.0], 2, {})
    with pytest.raises(ValueError):
        ego.fuse_readouts([1.0, 1.0, 1.0, 1.0], 2, {0: [0.0, 0.0, 0.0, 0.0]})
    with pytest.raises(ValueError):
        ego.diagnostic(True)
    with pytest.raises(ValueError):
        ego.diagnostic(42, "cuda")
