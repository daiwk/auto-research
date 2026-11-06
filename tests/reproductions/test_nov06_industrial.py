import math

import pytest
import torch

from auto_research.reproductions.ice_components import (
    click_distribution_loss,
    gate_click_features,
    ice_objective,
    impression_attention_bias,
    impression_survival,
    sequence_value,
)
from auto_research.reproductions.ured_components import DAY, Candidate, Exposure, ScoredSession, mine_ured


def test_ice_depth_survival_and_joint_utility():
    log_depth = torch.tensor([[0.2, 0.3, 0.5]], dtype=torch.float64).log()
    expected = torch.tensor([[1, .8, .5]], dtype=torch.float64)
    assert torch.allclose(impression_survival(log_depth), expected)
    weights = log_depth.new_tensor([[2, 0, 4]])
    assert sequence_value(log_depth, torch.zeros_like(log_depth), weights).item() == pytest.approx(2)


def test_ice_gates_do_not_update_impression_branch():
    p = torch.tensor([[1, .5, .2]], dtype=torch.float64, requires_grad=True)
    feature = torch.ones(1, 3, 2, dtype=p.dtype, requires_grad=True)
    assert torch.allclose(impression_attention_bias(p).exp(), p[:, :, None] * p[:, None, :] + 1e-8)
    assert not impression_attention_bias(p).requires_grad
    out = gate_click_features(feature, p, alpha=.25)
    out.sum().backward()
    assert p.grad is None
    assert torch.allclose(feature.grad[..., 0], .75 + .25 * p)


def test_ice_listwise_kl_treats_empty_clicks_as_uniform():
    logits = torch.zeros(2, 3, dtype=torch.float64)
    clicks = torch.tensor([[0, 1, 1], [0, 0, 0]])
    assert click_distribution_loss(logits, clicks).item() == pytest.approx(math.log(1.5))
    assert click_distribution_loss(logits[1:], clicks[1:]).item() == pytest.approx(0, abs=1e-12)


def test_ice_objective_factorizes_and_masks_unreached_conditional_clicks():
    log_depth = torch.tensor([[.2, .3, .5]], dtype=torch.float64).log().requires_grad_()
    click = torch.zeros_like(log_depth, requires_grad=True)
    out = ice_objective(log_depth, click, torch.tensor([[1, 1, 0]]), torch.tensor([[0, 1, 0]]),
                        distribution_weight=0)
    assert out["impression"].item() == pytest.approx(-math.log(.8) - math.log(.5))
    assert out["conditional_click"].item() == pytest.approx(2 * math.log(2))
    out["total"].backward()
    assert click.grad[0, 2] == 0
    assert log_depth.grad.abs().sum() > 0


@pytest.mark.parametrize("shown, clicked", [([0, 0, 0], [0, 0, 0]), ([1, 0, 1], [0, 0, 0]),
                                            ([1, 0, 0], [0, 1, 0]), ([1, 1, 1], [0, 2, 0])])
def test_ice_rejects_inconsistent_labels(shown, clicked):
    logits = torch.zeros(1, 3)
    with pytest.raises(ValueError):
        ice_objective(logits, logits, torch.tensor([shown]), torch.tensor([clicked]))


def test_ice_stable_impression_loss_when_softmax_saturates():
    depth = torch.tensor([[1000, -1000]], dtype=torch.float64, requires_grad=True)
    out = ice_objective(depth, torch.zeros_like(depth), torch.ones(1, 2), torch.zeros(1, 2))
    assert out["impression"].item() == pytest.approx(2000)
    out["total"].backward()
    assert torch.isfinite(depth.grad).all()


def test_ured_filters_in_paper_order_with_latest_duplicate():
    now = 50 * DAY
    log = (
        ScoredSession("u", now - DAY, (Candidate("a", "old-category", 1), Candidate("b", "new", .9))),
        ScoredSession("u", now - 1, (Candidate("a", "new", .7), Candidate("c", "shown", 1),
                                    Candidate("d", "other", .4)), frozenset({"c"})),
        ScoredSession("other", now - 1, (Candidate("x", "new", 9),)),
    )
    result = mine_ured("u", now, log, (), session_limit=2)
    assert [(p.item, p.category, p.score) for p in result] == [("a", "new", .7), ("d", "other", .4), ("b", "new", .9)]
    # The user cap is applied before novelty. Rejected items do not refill from
    # lower ranked entries that were never materialized into the user pool.
    assert mine_ured("u", now, log, (Exposure("u", now - 2, "q", "new"),), user_limit=1) == ()


def test_ured_asof_and_history_boundaries_are_leakage_free():
    now = 50 * DAY
    log = (
        ScoredSession("u", now - 30 * DAY, (Candidate("include", "old", 1),)),
        ScoredSession("u", now - 30 * DAY - 1, (Candidate("stale", "other", 2),)),
        ScoredSession("u", now, (Candidate("future", "new", 3),)),
    )
    exposures = (Exposure("u", now - 15 * DAY - 1, "past", "old"),
                 Exposure("u", now, "include", "old"))
    assert [p.item for p in mine_ured("u", now, log, exposures)] == ["include"]
    assert mine_ured("u", now, log, (*exposures, Exposure("u", now - 15 * DAY, "past", "old"))) == ()
    assert mine_ured("u", now, log, (*exposures, Exposure("u", now - 40 * DAY, "include", "old"))) == ()


def test_ured_never_reinserts_shown_or_invalid_rows():
    a = Candidate("a", "c", 1)
    with pytest.raises(ValueError):
        ScoredSession("u", 0, (a, a))
    with pytest.raises(ValueError):
        Candidate("a", "c", float("nan"))
    assert mine_ured("u", 1, (ScoredSession("u", 0, (a,), frozenset({"a"})),), ()) == ()
