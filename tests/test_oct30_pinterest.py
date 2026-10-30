import importlib.util
from pathlib import Path

import pytest
import torch


ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "src/auto_research/reproductions" / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


p = module("pinger_components")
r = module("pinterest_rlbp")


@pytest.mark.parametrize("seed", [42, 43, 44])
@pytest.mark.parametrize("implementation", [p, r])
def test_actual_small_tensor_mechanisms(seed, implementation):
    row = implementation.diagnostic(seed)
    assert row["seed"] == seed and all(row["checks"].values())
    assert all(type(value) is bool for value in row["checks"].values())
    assert row["metrics"]["pretrained_model_calls"] == 0


def test_mask_rules_exhaustively_and_no_future_or_own_dense_path():
    mask = p.interleaved_mask(3, 2)
    for i in range(9):
        for j in range(9):
            qi, qr = divmod(i, 3)
            ki, kr = divmod(j, 3)
            expected = ((qr == kr == 2 and ki <= qi) or
                        (qr < 2 and ((kr == 2 and ki < qi) or (ki == qi and kr <= qr))))
            assert bool(mask[i, j]) is expected
    assert not mask[3, 5] and not mask[4, 0]


def test_invalid_IDs_are_not_selected_and_prefix_depth_is_used():
    scores = torch.tensor([[10., 9.], [8., 7.], [6., 5.]], dtype=torch.float64)
    valid = torch.tensor([[False, True], [True, True], [True, True]])
    selected, raw, adjusted = p.select_prefix_candidates([(0, 0), (0, 1), (1, 0)], scores, 3, 3., valid)
    assert selected == [(0, 1), (2, 0), (1, 0)]
    assert raw.tolist() == [9., 6., 8.]
    assert adjusted.tolist() == [9., 6., 5.]


def test_lambda_zero_and_stable_ties_match_flat_top_scores():
    values = torch.ones(2, 3, dtype=torch.float64)
    selected, _, _ = p.select_prefix_candidates([(1,), (2,)], values, 4, 0.)
    assert selected == [(0, 0), (0, 1), (0, 2), (1, 0)]


@pytest.mark.parametrize("parents,shape,width", [(None, (2, 2), 1), ([(0,), (0,)], (2, 2), 1),
                                               ([(0,), (1, 2)], (2, 2), 1), ([(0,)], (1, 2), 3),
                                               ([(True,)], (1, 2), 1)])
def test_prefix_selection_rejects_invalid_inputs(parents, shape, width):
    with pytest.raises(ValueError):
        p.select_prefix_candidates(parents, torch.zeros(shape, dtype=torch.float64), width, 0.1)


def test_prefix_dpo_reference_gradient_anchor_and_not_last_prefix_only():
    chosen = torch.tensor([[-0.1, -0.4]], dtype=torch.float64, requires_grad=True)
    rejected = torch.tensor([[-0.5, -0.2]], dtype=torch.float64, requires_grad=True)
    rc = torch.tensor([[-0.2, -0.1]], dtype=torch.float64, requires_grad=True)
    rr = torch.tensor([[-0.3, -0.3]], dtype=torch.float64, requires_grad=True)
    anchor = torch.tensor(0.7, dtype=torch.float64, requires_grad=True)
    loss = p.prefix_dpo_loss(chosen, rejected, rc, rr, anchor, beta=0.3, weight=0.4)
    expected = anchor + 0.4 * torch.nn.functional.softplus(-0.3 * ((chosen - rejected).cumsum(-1) - (rc - rr).detach().cumsum(-1))).sum()
    torch.testing.assert_close(loss, expected)
    loss.backward()
    assert rc.grad is None and rr.grad is None and anchor.grad == 1
    assert chosen.grad is not None and chosen.grad[0, 0].abs() > chosen.grad[0, 1].abs()
    assert p.prefix_dpo_loss(chosen, rejected, rc, rr, anchor, weight=0.) == anchor


def test_reference_margin_does_not_create_a_hard_zero_gradient_gate():
    x = torch.tensor([[-0.1]], dtype=torch.float64, requires_grad=True)
    p.prefix_dpo_loss(x, torch.tensor([[-2.]], dtype=torch.float64),
                      torch.tensor([[-0.1]], dtype=torch.float64), torch.tensor([[-1.]], dtype=torch.float64),
                      torch.tensor(0., dtype=torch.float64), beta=0.2).backward()
    assert x.grad.item() < 0


@pytest.mark.parametrize("items,levels", [(0, 2), (2, 0), (True, 2), (128, 32)])
def test_mask_budget_and_types_fail_closed(items, levels):
    with pytest.raises(ValueError):
        p.interleaved_mask(items, levels)


def test_relative_rewards_keep_CPC_sign_and_zero_baseline_is_undefined():
    x = torch.tensor([1., 4.], dtype=torch.float64)
    torch.testing.assert_close(r.relative_lift(x, x * 2), torch.full_like(x, -0.5))
    with pytest.raises(ValueError):
        r.relative_lift(x, torch.zeros_like(x))


def test_nine_actions_preserve_D_and_nonpositive_or_collapsed_alpha_is_rejected():
    table = r.action_multipliers(0.2)
    assert table.shape == (9, 3) and (table[:, 2] == 1).all()
    torch.testing.assert_close(table[0], torch.tensor([0.8, 0.8, 1.], dtype=torch.float64))
    for alpha in (0, 1, -0.1, float("nan"), True, 1e-30):
        with pytest.raises(ValueError):
            r.action_multipliers(alpha)


def test_TD_backups_use_max_BU_min_CPC_and_are_detached():
    qb = torch.zeros(1, 9, dtype=torch.float64, requires_grad=True)
    qc = torch.zeros(1, 9, dtype=torch.float64, requires_grad=True)
    future = torch.arange(9, dtype=torch.float64).reshape(1, 9).requires_grad_()
    reward = torch.ones(1, dtype=torch.float64, requires_grad=True)
    result = r.two_head_td_loss(qb, qc, torch.tensor([0]), reward, reward,
                                gamma=0.5, next_bu=future, next_cpc=future)
    assert result["bu"].item() == 25 and result["cpc"].item() == 1
    result["total"].backward()
    assert future.grad is None and reward.grad is None
    assert qb.grad[0, 0] == -10 and qc.grad[0, 0] == -2
    assert qb.grad[0, 1:].abs().sum() == 0


def test_contextual_bandit_does_not_silently_consume_future_Qs():
    q = torch.zeros(2, 9)
    with pytest.raises(ValueError):
        r.two_head_td_loss(q, q, torch.tensor([0, 0]), torch.ones(2), torch.ones(2), next_bu=q)


def test_stable_topK_and_extreme_finite_scores():
    q = torch.zeros(1, 9, dtype=torch.float64)
    policy = r.fused_policy(q, q, torch.zeros(1, dtype=q.dtype), top_k=2)
    torch.testing.assert_close(policy[0, :2], torch.tensor([0.5, 0.5], dtype=q.dtype))
    assert policy[0, 2:].sum() == 0
    huge = torch.tensor([[1e308, -1e308] + [0.] * 7], dtype=torch.float64)
    assert torch.isfinite(r.fused_policy(huge, q, torch.zeros(1, dtype=q.dtype), temperature=1e-300)).all()
    with pytest.raises(ValueError):
        r.fused_policy(q.float(), q.float(), torch.zeros(1), temperature=1e-300)


def test_IPS_is_ordinary_mean_not_self_normalized_and_requires_support():
    p1 = torch.tensor([0.2, 0.5], dtype=torch.float64)
    log = torch.tensor([0.5, 0.25], dtype=torch.float64)
    reward = torch.tensor([1., 3.], dtype=torch.float64)
    assert r.ips_value(p1, log, reward).item() == 3.2
    with pytest.raises(ValueError):
        r.ips_value(p1, torch.zeros_like(log), reward)


def test_preprocessing_is_explicit_after_fusion_and_can_change_probabilities():
    bu = torch.arange(9, dtype=torch.float64)[None, :]
    cpc = bu * 0.5
    beta = torch.ones(1, dtype=bu.dtype)
    calls = []

    def external(scores):
        calls.append(scores.clone())
        return scores * 2

    identity = r.fused_policy(bu, cpc, beta)
    rescaled = r.fused_policy(bu, cpc, beta, preprocess=external)
    assert len(calls) == 1
    torch.testing.assert_close(calls[0], bu - beta[:, None] * cpc)
    assert torch.equal(identity > 0, rescaled > 0)
    assert not torch.allclose(identity, rescaled)
    for callback in (lambda s: s[:, :1], lambda s: s.float(), lambda s: s * float("nan"), 4):
        with pytest.raises(ValueError):
            r.fused_policy(bu, cpc, beta, preprocess=callback)
