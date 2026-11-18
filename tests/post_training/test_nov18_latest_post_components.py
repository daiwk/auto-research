"""Independent scalar/gradient and failure-path checks, not model evaluation."""

import importlib
import math
import json
import pytest
import torch

from auto_research.post_training import ambient_sft, sh_opd, leaf_opd, streaming_opd, specal
from auto_research.post_training import regularized_score_centering as rsc
from auto_research.post_training import margin_dynamics_tpo as tpo
from auto_research.post_training import ca_zodpo, jev_safety_reward as jev
from auto_research.post_training import optimistic_verifier_audit as oracle
from auto_research.post_training import confidence_adaptive_granularity as granularity
from auto_research.post_training import design_taste_admission as taste

NAMES = [
    "ambient_sft",
    "sh_opd",
    "leaf_opd",
    "streaming_opd",
    "specal",
    "regularized_score_centering",
    "margin_dynamics_tpo",
    "ca_zodpo",
    "jev_safety_reward",
    "optimistic_verifier_audit",
    "confidence_adaptive_granularity",
    "design_taste_admission",
]


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics_execute_bounded_components(name, seed):
    m = importlib.import_module("auto_research.post_training." + name)
    out = m.diagnostic(seed, device="cpu")
    assert out["seed"] == seed and out["diagnostic_only"] is True
    assert out["evaluation_tier"] in {"l0_interface", "l1_mechanism"}
    assert all(type(v) is bool and v for v in out["checks"].values())
    assert all(type(v) in {float, int} and math.isfinite(v) for v in out["metrics"].values())
    assert json.loads(json.dumps(out)) == out


def test_ambient_exact_temperature_kl_without_t_squared():
    s = torch.tensor([[[0.2, -0.1]]], dtype=torch.float64, requires_grad=True)
    q = torch.tensor([[[1.0, -1.0]]], dtype=torch.float64, requires_grad=True)
    out, ce, kl = ambient_sft.loss(
        s, q, torch.tensor([[1]]), torch.tensor([[True]]), temperature=2.0, weight=0.3
    )
    qp = torch.softmax(q.detach() / 2, -1)
    expected = (qp * (qp.log() - torch.log_softmax(s / 2, -1))).sum()
    assert kl.item() == pytest.approx(expected.item())
    assert out.item() == pytest.approx(ce.item() + 0.3 * expected.item())
    out.backward()
    assert q.grad is None


@pytest.mark.parametrize("temperature", [0, -1, float("nan"), True])
def test_ambient_invalid_temperature(temperature):
    with pytest.raises(ValueError):
        ambient_sft.loss(
            torch.ones(1, 1, 2),
            torch.ones(1, 1, 2),
            torch.zeros(1, 1, dtype=torch.long),
            torch.ones(1, 1, dtype=torch.bool),
            temperature=temperature,
            weight=1.0,
        )


def test_sh_survival_and_expected_horizon_exact():
    h, p = sh_opd.horizon_distribution(2, 8, 1.0)
    assert p.tolist() == pytest.approx([1 - 0.5, 0.5 - 1 / 3, 1 / 3 - 0.25, 0.25])
    assert (h * p).sum().item() == pytest.approx(2 * (1 + 0.5 + 1 / 3 + 0.25))
    assert sh_opd.implicit_block_weights(2, 8, 0).tolist() == [0.25] * 4
    with pytest.raises(ValueError):
        sh_opd.horizon_distribution(3, 8, 1)
    with pytest.raises(ValueError):
        sh_opd.generate_batch([1], lambda prompt, **kwargs: [0] * 9, horizon=8)


def test_sh_token_mean_is_not_mean_of_response_means():
    values = torch.tensor([[1.0, 99.0], [3.0, 5.0]], requires_grad=True)
    mask = torch.tensor([[True, False], [True, True]])
    out = sh_opd.token_mean(values, mask)
    assert out.item() == 3.0
    assert out.item() != (1 + (3 + 5) / 2) / 2
    out.backward()
    assert torch.allclose(values.grad, torch.tensor([[1 / 3, 0], [1 / 3, 1 / 3]]))


def test_leaf_second_half_uses_floor_index_and_sequence_mean():
    c = torch.tensor([[-4.0, -3.0, -2.0]])
    full, tail = leaf_opd.supervision_signals(
        c, torch.full_like(c, -1), torch.ones_like(c, dtype=torch.bool)
    )
    assert full.item() == 2 and tail.item() == 1.5
    assert leaf_opd.contexts("x", "private", forget=False) == {"student": "x", "teacher": "x"}
    with pytest.raises(ValueError):
        leaf_opd.contexts("x", "", forget=True)


def test_streaming_topk_negative_sum_clipped_not_normalized():
    # Teacher top1 prob .6; student puts .9 there -> negative partial KL -> zero.
    s = torch.tensor([[[math.log(0.9), math.log(0.1)]]], requires_grad=True)
    t = torch.tensor([[[math.log(0.6), math.log(0.4)]]])
    out, pt = streaming_opd.topk_loss(s, t, torch.tensor([[True]]), k=1)
    assert out.item() == 0 and pt.item() == 0
    out.backward()
    assert s.grad.abs().sum().item() == 0
    seg = streaming_opd.segment([1, 2, 3], 1, [0, 1, 1], terminal=False)
    assert seg.loss_mask == (False, True, True) and not seg.terminal
    with pytest.raises(ValueError):
        streaming_opd.version_lags(seg, 0)


def test_streaming_weighted_means_not_sum_of_segment_means():
    result = streaming_opd.weighted_reduce(torch.tensor([1.0, 3.0]), torch.tensor([1.0, 3.0]))
    assert result.item() == 2.5
    with pytest.raises(ValueError):
        streaming_opd.weighted_reduce(torch.ones(2), torch.zeros(2))


def test_specal_detects_orthogonal_leave_one_outlier_and_freezes_weights():
    z = torch.tensor(
        [[[1.0, 0, 0], [0.9, 0.1, 0], [0.9, -0.1, 0], [0, 0, 1.0]]],
        dtype=torch.float64,
        requires_grad=True,
    )
    a = torch.tensor([[1.0, -1, 1, -1]], dtype=torch.float64)
    out = specal.calibrate(z, a, target_rank=0.5, rank_tolerance=0.3)
    assert out["support"][0, 3].item() < out["support"][0, 0].item()
    assert not out["advantages"].requires_grad
    with pytest.raises(ValueError):
        specal.calibrate(torch.zeros_like(z), a, target_rank=0.5, rank_tolerance=0.3)


def test_rsc_tis_clips_sample_and_auxiliary_separately():
    lp = torch.tensor([math.log(0.8)], dtype=torch.float64, requires_grad=True)
    mu = torch.tensor([math.log(0.2)], dtype=torch.float64)
    aux = torch.tensor([[math.log(0.2), math.log(0.8)]], dtype=torch.float64, requires_grad=True)
    amu = torch.tensor([[math.log(0.8), math.log(0.2)]], dtype=torch.float64)
    out = rsc.loss(lp, mu, torch.tensor([2.0]), aux, amu, beta=0, low=0.5, high=2.0)
    out.backward()
    assert lp.grad.item() == -4.0
    assert aux.grad.tolist()[0] == pytest.approx([0.5, 2.0])
    with pytest.raises(ValueError):
        rsc.loss(lp, mu, torch.tensor([2.0]), aux, amu, aux_weights=torch.ones_like(aux))


def test_tpo_h_exact_normalized_huber_and_s_restoring_force():
    x = torch.tensor([0.0, 1.0, 3.0], dtype=torch.float64, requires_grad=True)
    out = tpo.tpo_h(x, target=0, transition=2)
    assert out.item() == pytest.approx((0 + 0.25 + 2) / 3)
    out.backward()
    assert x.grad.tolist() == pytest.approx([0, 1 / 6, 1 / 3])
    with pytest.raises(ValueError):
        tpo.tpo_s(x, x, smoothing=0.6)


def test_ca_rank_degenerate_contrast_rejected_and_input_unchanged():
    g = torch.Generator().manual_seed(1)
    with pytest.raises(ValueError):
        ca_zodpo.contrastive_basis(torch.ones(3, 4), torch.ones(3, 4), rank=1, generator=g)
    w = torch.ones(2, 3)
    before = w.clone()
    d = torch.full_like(w, 0.5)
    slope = ca_zodpo.central_difference(lambda x: x.square().sum(), w, d, epsilon=0.01)
    assert slope.item() == pytest.approx(6, abs=1e-4)
    assert torch.equal(w, before)


def test_ca_executes_real_dpo_objective_with_reference_and_negative_pair_control():
    # A one-token/two-response policy makes the complete DPO objective explicit.
    g = torch.Generator().manual_seed(9)
    chosen = torch.tensor([[1.0, 1.0], [0.0, 0.0], [0.0, 0.0]], dtype=torch.float64)
    rejected = torch.tensor([[0.0, 0.0], [1.0, 1.0], [0.0, 0.0]], dtype=torch.float64)
    basis = ca_zodpo.contrastive_basis(chosen, rejected, rank=1, generator=g)
    coefficients = torch.tensor([[1.0], [-1.0]], dtype=torch.float64)
    weight = torch.tensor(
        [[0.1, -0.2, 0.3], [-0.1, 0.2, -0.3]], dtype=torch.float64, requires_grad=True
    )
    prompt = torch.tensor([1.0, 0.3, -0.4], dtype=torch.float64)
    reference = torch.tensor([-0.3, 0.3], dtype=torch.float64).log_softmax(-1)

    def dpo(w, reverse=False):
        logp = (w @ prompt).log_softmax(-1)
        margin = (logp[0] - reference[0]) - (logp[1] - reference[1])
        return torch.nn.functional.softplus(-0.7 * (-margin if reverse else margin))

    perturbation = ca_zodpo.direction(coefficients, basis)
    derivative = (torch.autograd.grad(dpo(weight), weight)[0] * perturbation).sum()
    slope = ca_zodpo.central_difference(dpo, weight, perturbation, epsilon=1e-5)
    assert slope.item() == pytest.approx(derivative.item(), abs=1e-9)
    updated, _ = ca_zodpo.momentum_update(
        weight, basis, coefficients, slope, learning_rate=0.01, momentum=0.0
    )
    assert dpo(updated).item() < dpo(weight).item()
    assert dpo(updated, reverse=True).item() > dpo(weight, reverse=True).item()


def test_jev_denominators_and_calibration_isolation():
    r = jev.rates([0.01, 0.8, 0.1, 0.9], [1, 1, 0, 0], [True] * 4, threshold=0.9)
    assert r["gate_pass_rate"] == 0.5 and r["passed_harm_rate"] == 0.25
    assert jev.rates([0.1], [0], [True], threshold=0.9)["gate_pass_rate"] is None
    with pytest.raises(ValueError):
        jev.calibrate_threshold([0.9], [1], split="test")


def test_oracle_enumerates_and_not_all_sufficient_sets():
    rs = oracle.minimal_sufficient_reasons([(0, 1)] * 3, (1, 1, 0), lambda x: bool(x[0] and x[1]))
    assert rs == (frozenset([0, 1]),)
    assert oracle.exact_reward([0, 2], rs)["precision"] == 0.5
    with pytest.raises(ValueError):
        oracle.minimal_sufficient_reasons([(0, 1)] * 13, (0,) * 13, lambda x: False)
    with pytest.raises(ValueError):
        oracle.proxy_audit([1.0, 1.0], [0.0, 0.0])


def test_granularity_abstain_not_exclude_and_recognition_ties_fail():
    paths = [(i, i) for i in range(20)]
    assert granularity.consensus_target(paths)["status"] == "abstain"
    assert granularity.consensus_target([None] * 20)["status"] == "exclude"
    assert granularity.recognition_target([2.0, 3.0], [[2.0], [2.0]]) == 1
    assert (
        granularity.information_utility(
            prior_uncertainty=1000, level_uncertainty=1000, finest_uncertainty=1, correct=True
        )
        == 0
    )


def test_taste_hack_failure_and_hard_gate_override_score():
    assert not taste.admit(
        expert_agreement=1, causal_sensitivity=1, hack_trap_failure=0.3, self_agreement=1
    )["admitted"]
    scores = dict(func=1, design=1, rubric=1, pref=1)
    assert (
        taste.composite_reward({"no_regression": False}, scores, dict.fromkeys(scores, 0.25)) == 0
    )
    with pytest.raises(ValueError):
        taste.composite_reward({"build": True}, scores, dict.fromkeys(scores, 0.1))


def test_gpu_requirement_only_for_cuda_advertised_tensor_operators():
    for i, name in enumerate(NAMES):
        assert importlib.import_module(
            "auto_research.post_training." + name
        ).REQUIRES_GPU_VALIDATION is (i < 8)
