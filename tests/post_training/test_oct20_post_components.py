"""SPOD/APSD/TAR defining formulas, gradients, negative controls and boundaries."""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import sys

import pytest
import torch

from auto_research.post_training import apsd, spod, tar

ROOT = Path(__file__).resolve().parents[2]


def binary_logits(probabilities):
    return torch.tensor([[[math.log(p), math.log(1 - p)] for p in row] for row in probabilities], dtype=torch.float64)


def binary_kl(q, p):
    return q * math.log(q / p) + (1 - q) * math.log((1 - q) / (1 - p))


def test_spod_complete_action_gate_success_and_episode_state_token_balancing():
    student = binary_logits([[.4, .5], [.2, .5], [.3, .3]]).requires_grad_()
    teacher = binary_logits([[.16, .5], [.7, .5], [.1, .1]]).requires_grad_()
    mask = torch.tensor([[True, False], [True, False], [True, True]])
    labels = torch.tensor([[0, -1], [0, -1], [0, 0]])
    loss, audit = spod.success_preserving_loss(student, teacher, labels, mask, ["A", "A", "B"], {"A": True, "B": False})
    expected = ((math.log(.5 / .4) + binary_kl(.7, .2)) / 2 + binary_kl(.1, .3)) / 2
    assert float(loss.detach()) == pytest.approx(expected, abs=1e-14)
    assert audit["gate"].tolist() == [True, False, False]
    loss.backward()
    assert student.grad.isfinite().all() and student.grad[~mask].count_nonzero() == 0
    assert teacher.grad is None
    # End of action matters: support is a product across ALL action tokens.
    _, whole = spod.success_preserving_loss(binary_logits([[.8, .1]]), binary_logits([[.4, .4]]),
        torch.zeros(1, 2, dtype=torch.long), torch.ones(1, 2, dtype=torch.bool), ["A"], {"A": True})
    assert whole["gate"].tolist() == [False]


def test_spod_floor_and_mask_are_complementary_and_above_floor_stops():
    for p, floor_active in ((.4, True), (.8, False)):
        student = binary_logits([[p]]).requires_grad_()
        teacher = binary_logits([[.16]])
        loss, audit = spod.success_preserving_loss(student, teacher, torch.zeros(1, 1, dtype=torch.long),
            torch.ones(1, 1, dtype=torch.bool), ["A"], {"A": True})
        assert audit["gate"].item()
        loss.backward()
        if floor_active:
            assert float(student.grad[0, 0, 0]) == pytest.approx(-(1 - p))
        else:
            assert student.grad.count_nonzero() == 0
        # Keeping KL would still erode successful choices, even above the floor.
        assert audit["action_forward_kl"].item() > 0


def test_spod_padding_nan_not_training_outcomes_and_exact_binary_contract():
    s = torch.tensor([[[0., 1.], [float("nan"), float("nan")]]], requires_grad=True)
    t = torch.zeros_like(s)
    mask = torch.tensor([[True, False]])
    value, _ = spod.success_preserving_loss(s, t, torch.tensor([[0, -1]]), mask, ["A"], {"A": False})
    value.backward()
    assert s.grad.isfinite().all()
    with pytest.raises(ValueError, match="Boolean"):
        spod.success_preserving_loss(s, t, torch.tensor([[0, -1]]), mask, ["A"], {"A": 1})
    with pytest.raises(ValueError, match="coverage"):
        spod.success_preserving_loss(s, t, torch.tensor([[0, -1]]), mask, ["A"], {"B": True})


@pytest.mark.parametrize("alpha", [0., .5, .9, 1.])
def test_apsd_target_geometry_reference_cases_and_true_student_dependence(alpha):
    s = torch.tensor([[[1., -.5, .2]]], dtype=torch.float64, requires_grad=True)
    q = torch.tensor([[[-.3, .7, 1.2]]], dtype=torch.float64, requires_grad=True)
    value, audit = apsd.asymmetric_self_distillation_loss(s, q, torch.tensor([True]), torch.ones(1, 1, dtype=torch.bool), correct_alpha=alpha)
    ps, pq = s.log_softmax(-1), q.detach().log_softmax(-1)
    expected_target = ((1 - alpha) * ps + alpha * pq).log_softmax(-1)
    torch.testing.assert_close(audit["target_log_probs"], expected_target, rtol=0, atol=1e-15)
    expected_loss = (ps.exp() * (ps - expected_target)).sum()
    torch.testing.assert_close(value, expected_loss)
    value.backward()
    assert q.grad is None and s.grad.isfinite().all()
    if alpha == 0:
        assert abs(float(value.detach())) < 1e-14 and s.grad.abs().max() < 1e-14


def test_apsd_full_gradient_matches_finite_difference_and_target_detach_is_wrong():
    s = torch.tensor([[[.8, -.4, 1.]], [[-.2, .3, .9]]], dtype=torch.float64, requires_grad=True)
    q = torch.tensor([[[.1, .9, -.5]], [[.2, -.7, .4]]], dtype=torch.float64, requires_grad=True)
    correct, mask = torch.tensor([True, False]), torch.ones(2, 1, dtype=torch.bool)
    def objective(x):
        return apsd.asymmetric_self_distillation_loss(x, q, correct, mask)[0]
    assert torch.autograd.gradcheck(objective, (s,), eps=1e-6, atol=1e-7, rtol=1e-5)
    loss, audit = apsd.asymmetric_self_distillation_loss(s, q, correct, mask)
    full = torch.autograd.grad(loss, s, retain_graph=True)[0]
    lp, lq = s.log_softmax(-1), q.detach().log_softmax(-1)
    stop = (lp.exp() * (lp - audit["target_log_probs"].detach())).sum() / 2
    stopped = torch.autograd.grad(stop, s, retain_graph=True)[0]
    scaled_sdpo = (audit["alpha"][:, None] * (lp.exp() * (lp - lq)).sum(-1)).sum() / 2
    scaled = torch.autograd.grad(scaled_sdpo, s)[0]
    torch.testing.assert_close(stopped, scaled)
    assert (full - stopped).norm() > 1e-3
    assert q.grad is None


def test_apsd_mask_and_correctness_validation():
    s = torch.tensor([[[1., -1.], [float("nan"), float("nan")]]], dtype=torch.float64, requires_grad=True)
    q = torch.zeros_like(s, requires_grad=True)
    mask = torch.tensor([[True, False]])
    value, _ = apsd.asymmetric_self_distillation_loss(s, q, torch.tensor([False]), mask)
    value.backward()
    assert s.grad.isfinite().all() and s.grad[~mask].count_nonzero() == 0 and q.grad is None
    with pytest.raises(ValueError, match="Boolean correctness"):
        apsd.asymmetric_self_distillation_loss(s, q, torch.tensor([1.]), mask)


def test_tar_fps_filters_wrong_responses_and_selects_original_indices():
    embeddings = torch.tensor([[1., 0.], [float("nan"), float("nan")], [0., 1.], [-1., 0.]], dtype=torch.float64)
    correct = torch.tensor([True, False, True, True])
    assert tar.farthest_point_prototypes(embeddings, correct, initial_index=0) == [0, 3, 2]
    assert tar.farthest_point_prototypes(embeddings, torch.zeros(4, dtype=torch.bool)) == []
    with pytest.raises(ValueError, match="correct response"):
        tar.farthest_point_prototypes(embeddings, correct, initial_index=1)
    with pytest.raises(ValueError, match="nonzero"):
        tar.farthest_point_prototypes(torch.zeros(2, 3), torch.ones(2, dtype=torch.bool))


def test_tar_fps_rejects_finite_vectors_with_overflowed_norms():
    embeddings = torch.tensor([[1e308, 1e308], [1., 0.]], dtype=torch.float64)
    assert embeddings.isfinite().all() and not embeddings[0].norm().isfinite()
    with pytest.raises(ValueError, match="representable norms"):
        tar.farthest_point_prototypes(embeddings, torch.ones(2, dtype=torch.bool), initial_index=0)
    # Nonzero vectors with small but representable norms still normalize to unit length.
    small = torch.tensor([[1e-10, 0.], [0., 1e-10], [-1e-10, 0.]], dtype=torch.float32)
    assert tar.farthest_point_prototypes(small, torch.ones(3, dtype=torch.bool), initial_index=0) == [0, 2, 1]


@pytest.mark.parametrize("current,base", [(1., 2.), (-1., .1), (.1, -1.)])
def test_tar_replay_rejects_positive_active_log_probabilities(current, base):
    current_logp = torch.tensor([[current, 10.]], dtype=torch.float64, requires_grad=True)
    base_logp = torch.tensor([[base, 20.]], dtype=torch.float64)
    with pytest.raises(ValueError, match="nonpositive"):
        tar.adaptive_replay_loss(current_logp, base_logp, torch.tensor([[True, False]]))
    # Padding is not a probability observation and is excluded by the actor mask.
    valid_current = torch.tensor([[-abs(current), 10.]], dtype=torch.float64)
    valid_base = torch.tensor([[-abs(base), 20.]], dtype=torch.float64)
    value, _ = tar.adaptive_replay_loss(valid_current, valid_base, torch.tensor([[True, False]]))
    assert value >= 0


def test_tar_two_detached_soft_gates_weighted_denominator_and_all_trajectory_mean():
    current = torch.tensor([[-3., -1., float("nan")], [-.5, -1., -2.]], dtype=torch.float64, requires_grad=True)
    base = torch.tensor([[-1., -2., float("nan")], [-1., -2., -3.]], dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([[True, True, False], [True, True, True]])
    loss, audit = tar.adaptive_replay_loss(current, base, mask)
    gate, token = 1 - math.exp(-.5), 1 - math.exp(-2)
    assert float(loss.detach()) == pytest.approx(gate * (token * 3) / (1e-8 + token) / 2)
    assert audit["trajectory_gate"].tolist() == pytest.approx([gate, 0.])
    assert audit["token_weights"][0].tolist() == pytest.approx([token, 0., 0.])
    loss.backward()
    assert float(current.grad[0, 0]) == pytest.approx(-gate * token / (1e-8 + token) / 2)
    assert current.grad[0, 1:].count_nonzero() == current.grad[1].count_nonzero() == 0
    assert base.grad is None and not audit["token_weights"].requires_grad and not audit["trajectory_gate"].requires_grad


@pytest.mark.parametrize("dtype", [torch.float16, torch.float32, torch.float64])
def test_tar_zero_gate_extreme_discrepancies_and_small_epsilon_are_finite(dtype):
    current = torch.tensor([[-1.], [-1001.]], dtype=dtype, requires_grad=True)
    base = torch.tensor([[-1001.], [-1.]], dtype=dtype, requires_grad=True)
    loss, audit = tar.adaptive_replay_loss(current, base, torch.ones(2, 1, dtype=torch.bool))
    assert torch.isfinite(loss) and audit["trajectory_gate"].tolist() == [0., 1.]
    loss.backward()
    assert current.grad.isfinite().all() and base.grad is None and current.grad[0] == 0


@pytest.mark.parametrize("operator", ["spod", "apsd"])
def test_half_precision_extreme_logits_do_not_produce_zero_times_infinity(operator):
    s = torch.tensor([[[60000., -60000.]]], dtype=torch.float16, requires_grad=True)
    t = torch.tensor([[[-60000., 60000.]]], dtype=torch.float16, requires_grad=True)
    mask = torch.ones(1, 1, dtype=torch.bool)
    if operator == "spod":
        loss, _ = spod.success_preserving_loss(s, t, torch.zeros(1, 1, dtype=torch.long), mask, ["A"], {"A": False})
    else:
        loss, _ = apsd.asymmetric_self_distillation_loss(s, t, torch.tensor([False]), mask)
    assert loss.isfinite()
    loss.backward()
    assert s.grad.isfinite().all() and t.grad is None


def runner():
    spec = importlib.util.spec_from_file_location("oct20_post_runner", ROOT / "scripts/run_oct20_post_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("seed", [42, 43, 44])
@pytest.mark.parametrize("method", ["spod", "apsd", "tar-adaptive-replay"])
def test_actual_tiny_policy_updates_and_independent_references(method, seed):
    module = runner()
    torch.set_num_threads(1)
    torch.manual_seed(seed)
    function = {"spod": module.run_spod, "apsd": module.run_apsd, "tar-adaptive-replay": module.run_tar}[method]
    result = function("cpu", 3)
    metrics = result["metrics"]
    assert metrics["parameter_delta_l2"] > 0 and metrics["gradient_norm_min"] > 0
    assert metrics["optimizer_updates"] == 3 and metrics["loss_reference_max_abs_error"] < 1e-12
    if method == "spod":
        assert metrics["protected_decisions_total"] > 0 and metrics["floor_without_mask_negative_control_difference_max"] > 0
        assert metrics["teacher_parameter_delta_l2"] == metrics["teacher_gradient_count"] == 0
    elif method == "apsd":
        assert metrics["finite_difference_max_abs_error"] < 1e-8 and metrics["logit_gradient_reference_max_abs_error"] < 1e-12
        assert metrics["detached_target_negative_control_gradient_difference_min"] > 0
        assert metrics["self_teacher_parameter_delta_during_update_max"] == metrics["self_teacher_gradient_count"] == 0
        assert metrics["self_teacher_is_current_policy_copy"] and not metrics["feedback_in_actor_condition"]
    else:
        assert metrics["replay_gradient_reference_max_abs_error"] < 1e-12
        assert metrics["nonzero_replay_updates"] > 0 and metrics["replay_gradient_norm_max"] > 0
        assert metrics["base_parameter_delta_l2"] == metrics["base_gradient_count"] == 0
        assert not metrics["base_trajectories_replaced_with_gold"] and not metrics["semantic_encoder_used"]


def test_apsd_actor_never_receives_training_feedback_condition(monkeypatch):
    module, seen = runner(), []
    original = module.sample
    def record(model, history, device, length=2):
        seen.append(history)
        assert len(history) == 2 and history[0] == 1 and history[1] in (2, 3)
        return original(model, history, device, length)
    monkeypatch.setattr(module, "sample", record)
    torch.manual_seed(42)
    module.run_apsd("cpu", 1)
    assert len(seen) == 4


def test_runner_immutable_output_fixed_recipe_and_source_scope(tmp_path, monkeypatch):
    module = runner()
    output = tmp_path / "result.json"
    monkeypatch.setattr(sys, "argv", ["run", "--methods", "apsd", "--seeds", "42,43,44", "--steps", "1",
                                    "--code-commit", "a" * 40, "--output", str(output)])
    module.main()
    payload = json.loads(output.read_text())
    assert set(payload["executed_source_sha256"]) == set(module.SOURCES) and len(module.SOURCES) == 4
    item = payload["components"]["apsd"]
    assert item["dataset"]["id"] == "synthetic:oct20-apsd-v1" and item["dataset"]["capability_benchmark"] is False
    assert item["dataset"]["revision"] == "sha256:" + payload["executed_source_sha256"][module.SOURCES[0]]
    assert item["metrics"]["parameter_delta_l2"]["n"] == 3
    assert item["full_experiment_status"] == "not_reproduced_high_cost"
    assert item["diagnostic_only"] and not item["promotion_eligible"] and not item["evolve_integrated"]
    before = output.read_bytes()
    with pytest.raises(SystemExit):
        module.main()
    assert output.read_bytes() == before
