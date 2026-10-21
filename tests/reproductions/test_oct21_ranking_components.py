import math

import numpy as np
import pytest

from auto_research.reproductions.baseline_incremental import incremental_term, request_baseline, value_model
from auto_research.reproductions.spar_prefix_balance import rebalance_prefixes


def test_logit_operator_reference_and_center():
    p, b = np.array([.001, .3, .99]), np.array([.01, .2, .9])
    assert np.allclose(incremental_term(p, b), p*p*(1-b)/(p*(1-b)+(1-p)*b))
    assert np.all(incremental_term(p, p, shift=.5) == 0)


def test_hinge_and_demotion_are_distinct():
    assert np.array_equal(incremental_term([.2, .6], .4, magnitude="gap", scale="raw", sharpness=math.inf), np.maximum(np.array([.2, .6])-.4, 0))
    assert incremental_term(0, .5, magnitude="constant", direction="demotion") < -.99
    with pytest.raises(ValueError, match="must not vanish"):
        incremental_term(0, .5, direction="demotion")


@pytest.mark.parametrize("kw", [{"sharpness": 0}, {"sharpness": float("nan")}, {"clamp": 1},
                                    {"scale": "other"}, {"direction": "other"}])
def test_operator_invalid(kw):
    with pytest.raises(ValueError):
        incremental_term(.5, .4, **kw)


def test_historical_baseline_clamps_but_prediction_is_probability():
    assert np.isfinite(incremental_term(.5, 2))
    with pytest.raises(ValueError):
        incremental_term(2, .5)
    assert incremental_term(2, .5, scale="raw") > 0


def test_value_model_independent_weights_and_request_quantile():
    assert value_model([[.5, .2]], [[.1, .3]], raw_weights=[1, 2], incremental_weights=[3, 4]) == pytest.approx([2.4])
    assert request_baseline([1, 2, 3, 4]) == 3.25
    with pytest.raises(ValueError):
        request_baseline([])


def test_prefix_local_minimum_distortion_and_empty_destination():
    # Source 0 is overloaded; item1 is the cheapest legal move (not largest weight).
    residual = np.array([[0.], [.9], [0.]])
    center = np.array([[0.], [2.]])
    copy = center.copy()
    z, reports = rebalance_prefixes(residual, center, [0, 0, 0], [3, 1, 1], [(), (), ()])
    assert reports[0]["moves"][0]["item_index"] == 1
    assert np.array_equal(center, copy)
    # Eq14 gives B=4, so one unit move suffices; equal loads are not promised.
    assert np.array_equal(z, [0, 1, 0])
    assert max(reports[0]["loads_after"]) <= reports[0]["bound"]


def test_prefixes_independent_and_zero_weight():
    z, report = rebalance_prefixes([[0.], [2.], [3.]], [[0.], [2.]], [0, 0, 1], [0, 0, 9], [(0,), (0,), (1,)])
    assert z.tolist() == [0, 0, 1]
    assert all(not x["moves"] for x in report)


@pytest.mark.parametrize("weights,assign,tolerance", [([-1, 2], [0, 1], 1), ([1, 2], [0, 4], 1), ([1, 2], [0, 1], .5)])
def test_prefix_invalid(weights, assign, tolerance):
    with pytest.raises(ValueError):
        rebalance_prefixes([[0.], [2.]], [[0.], [1.]], assign, weights, [(), ()], tolerance=tolerance)


def test_echo_formula_gradient_padding_and_boundary():
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.echo_distillation import selector_losses
    s = torch.tensor([[3., 2., 1., -1., 99.]], dtype=torch.float64, requires_grad=True)
    t = torch.tensor([[0., 1., 3., 4., 99.]], dtype=torch.float64, requires_grad=True)
    valid = torch.tensor([[True, True, True, True, False]])
    r = selector_losses(s, t, valid, keep=2, pairs=2, temperature=2, mining_temperature=.5)
    assert r["selected_indices"].tolist() == [[0, 1]]
    assert r["active_pairs"] == 2
    ref = -(torch.softmax(t[0, :4].detach()/2, 0) * torch.log_softmax(s[0, :4]/2, 0)).sum()*4
    assert float((r["kd"]-ref).detach()) == pytest.approx(0, abs=1e-12)
    (r["kd"]+r["auxiliary"]).backward()
    assert t.grad is None
    assert s.grad[0, 4] == 0
    assert s.grad[0, 3] < 0


def test_echo_no_missing_record_is_connected_zero_auxiliary():
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.echo_distillation import selector_losses
    s = torch.tensor([[3., 1.]], requires_grad=True)
    r = selector_losses(s, s.detach(), torch.ones_like(s, dtype=torch.bool), keep=2, pairs=2)
    assert r["active_pairs"] == 0
    r["auxiliary"].backward()
    assert torch.equal(s.grad, torch.zeros_like(s))


@pytest.mark.parametrize("length,keep", [(2, 2), (70000, 5)])
def test_echo_half_precision_long_history_and_empty_pairs_stay_finite(length, keep):
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.echo_distillation import selector_losses
    s = torch.ones(1, length, dtype=torch.float16, requires_grad=True)
    r = selector_losses(s, s.detach(), torch.ones_like(s, dtype=torch.bool), keep=keep, pairs=3)
    assert r["kd"].dtype == torch.float32
    assert r["kd"].item() == pytest.approx(math.log(length), rel=1e-5)
    assert r["auxiliary"].item() == 0
    (r["kd"]+r["auxiliary"]).backward()
    assert torch.isfinite(s.grad).all()
