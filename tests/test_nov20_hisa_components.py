"""Literal angle, causal, normalization and gradient controls; not model scores."""

import importlib.util
import math
from pathlib import Path
import pytest
import torch

PATH = Path(__file__).resolve().parents[1] / "src/auto_research/foundation_models/hisa_components.py"
SPEC = importlib.util.spec_from_file_location("nov20_hisa_reference", PATH)
hisa = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(hisa)


@pytest.fixture(autouse=True)
def single_thread():
    previous = torch.get_num_threads()
    torch.set_num_threads(1)
    yield
    torch.set_num_threads(previous)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic(seed):
    result = hisa.diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(type(value) is bool and value for value in result["checks"].values())
    assert all(math.isfinite(value) for value in result["metrics"].values())


@pytest.mark.parametrize("seed", [True, -1, 1.2])
def test_bad_seed(seed):
    with pytest.raises(ValueError):
        hisa.diagnostic(seed)


def test_strict_boundary_uses_unwrapped_angle_not_modulo():
    # theta_0=1: distance1 is excluded at Phi=1, including exactly the boundary.
    mask = hisa.pair_mask([1], [0, 1, 2], 2, angle_budget=1)
    assert mask.tolist() == [[[False], [True], [False]]]
    # Seven radians is beyond Phi even though its wrapped angle is < pi/2.
    assert not hisa.pair_mask([7], [0], 2)[0, 0, 0]


def test_single_pair_literal_rope_rotation():
    q = torch.tensor([1.0, 2.0], dtype=torch.float64).reshape(1, 1, 1, 2)
    k = torch.tensor([3.0, 4.0], dtype=torch.float64).reshape(1, 1, 1, 2)
    observed = hisa.scores(q, k, query_positions=[1], key_positions=[0],
                           angle_budget=math.inf).item()
    expected = ((math.cos(1) - 2 * math.sin(1)) * 3
                + (math.sin(1) + 2 * math.cos(1)) * 4) / math.sqrt(2)
    assert observed == pytest.approx(expected, abs=1e-12)


def test_dropped_pair_is_not_renormalized_by_active_dimension():
    q = torch.tensor([1.0, 0.0, 0.0, 2.0], dtype=torch.float64).reshape(1, 1, 1, 4)
    k = torch.tensor([1.0, 2.0, 3.0, 4.0], dtype=torch.float64).reshape(1, 1, 1, 4)
    observed = hisa.scores(q, k, query_positions=[3], key_positions=[0],
                           angle_budget=1).item()
    # Only slow pair l=1 survives: theta=10000^(-1/2)=.01.
    numerator = -6 * math.sin(.03) + 8 * math.cos(.03)
    assert observed == pytest.approx(numerator / 2, abs=1e-12)
    assert observed != pytest.approx(numerator / math.sqrt(2))


def test_no_active_pair_masks_whole_key_before_softmax():
    q = torch.ones(1, 1, 1, 2, dtype=torch.float64)
    k = torch.ones(1, 1, 2, 2, dtype=torch.float64)
    v = torch.tensor([100.0, 3.0], dtype=torch.float64).reshape(1, 1, 2, 1)
    logits = hisa.scores(q, k, query_positions=[1], angle_budget=1)
    assert logits[0, 0, 0, 0].isneginf()
    assert logits.softmax(-1)[0, 0, 0, 0] == 0
    assert hisa.attention(q, k, v, query_positions=[1], angle_budget=1).item() == 3


def test_no_causal_reachable_key_is_explicit_error_not_nan():
    q = torch.ones(1, 1, 1, 2, dtype=torch.float64)
    with pytest.raises(ValueError, match="within reach"):
        hisa.scores(q, q, query_positions=[10], key_positions=[0], angle_budget=1)
    with pytest.raises(ValueError, match="within reach"):
        hisa.scores(q, q, query_positions=[0], key_positions=[1])


@pytest.mark.parametrize("positions", [[], [0.5], [-1], [True], [[0]], [1, 1], [2, 1]])
def test_invalid_positions(positions):
    with pytest.raises(ValueError):
        hisa.pair_mask(positions, [0], 4)


@pytest.mark.parametrize("dim,base,phi", [
    (0, 10000, 1), (3, 10000, 1), (True, 10000, 1),
    (4, 0, 1), (4, float("inf"), 1), (4, True, 1),
    (4, 10000, 0), (4, 10000, float("nan")), (4, 10000, True),
])
def test_invalid_geometry(dim, base, phi):
    with pytest.raises(ValueError):
        hisa.pair_mask([0], [0], dim, base, phi)


def test_shape_precision_finiteness_and_offset_contracts():
    q = torch.ones(1, 2, 3, 4, dtype=torch.float64)
    k = q.clone()
    for bad in [q.float(), q[:, :1], q[..., :3], q[..., 0], q * float("nan")]:
        with pytest.raises(ValueError):
            hisa.scores(q, bad)
    with pytest.raises(ValueError):
        hisa.attention(q, k, k[:, :, :2])
    with pytest.raises(ValueError):
        hisa.scores(q.half(), k.half())
    with pytest.raises(ValueError):
        hisa.scores(q, k, query_positions=[0, 1])


def test_future_value_gradient_is_zero():
    q = torch.randn(1, 1, 4, 4, dtype=torch.float64, requires_grad=True)
    k = torch.randn_like(q, requires_grad=True)
    v = torch.randn_like(q, requires_grad=True)
    out = hisa.attention(q, k, v)
    dq, dk, dv = torch.autograd.grad(out[:, :, :2].sum(), (q, k, v))
    assert all(torch.isfinite(t).all() for t in [dq, dk, dv])
    assert torch.count_nonzero(dk[:, :, 2:]) == 0
    assert torch.count_nonzero(dv[:, :, 2:]) == 0


def test_extreme_valid_score_overflow_is_rejected():
    q = torch.full((1, 1, 1, 4), 1e30, dtype=torch.float32)
    with pytest.raises(ValueError, match="overflowed"):
        hisa.scores(q, q)
