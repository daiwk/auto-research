"""Independent equations, frozen supervision, masks and honest catalog status."""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest
import torch

from auto_research.post_training import reviewed_oct18 as ops

ROOT = Path(__file__).resolve().parents[2]
KEYS = ("tag-reward-gating", "mrtpo", "token-teacher-selection", "ig-opd", "rshd")


def test_tag_anchor_is_pooled_probe_reverse_ratio_not_forward_or_response_mean():
    probe = torch.tensor([[[-1., -2., 0.], [-3., 0., 0.]], [[-1., -1., -1.], [-1., 0., 0.]]])
    base = torch.tensor([[[-2., -2., 0.], [-3., 0., 0.]], [[-2., -2., -2.], [-1., 0., 0.]]])
    mask = torch.tensor([[[True, True, False], [True, False, False]], [[True, True, True], [True, False, False]]])
    anchor, estimates = ops.elect_anchor(probe, base, mask)
    torch.testing.assert_close(estimates, torch.tensor([1 / 3, 3 / 4]))
    assert anchor == 0
    assert not estimates.requires_grad


def test_tag_gate_preserves_anchor_priority_and_exact_denominator():
    rewards = torch.tensor([[0., 1., 1.], [1., 0., 0.], [1., 1., 1.]], requires_grad=True)
    weights = torch.tensor([17., 2., 3.], requires_grad=True)
    result = ops.tag_reward(rewards, 0, weights)
    torch.testing.assert_close(result, torch.tensor([0., 1 / 6, 1.]))
    assert not result.requires_grad
    assert weights[0] == 17
    with pytest.raises(ValueError, match=r"\[0,1\]"):
        ops.tag_reward(rewards - 3, 0)
    with pytest.raises(ValueError, match="nonnegative"):
        ops.tag_reward(rewards, 0, -weights)


def test_group_advantages_use_population_scale_and_all_fail_is_zero():
    values = torch.tensor([[[0., 1.], [1., 1.], [0., 1.]]])
    result = ops.group_advantages(values)
    expected = (values[..., 0] - 1 / 3) / (math.sqrt(2 / 9) + 1e-6)
    torch.testing.assert_close(result[..., 0], expected)
    assert result[..., 1].count_nonzero() == 0
    assert ops.group_advantages(torch.zeros(1, 8)).count_nonzero() == 0


def test_mrtpo_independent_js_weights_signed_credit_mean_and_zero_information():
    all_values = torch.tensor([[[2., 0.], [0., 2.]], [[0., 1.], [2., -1.]]], dtype=torch.float64, requires_grad=True)
    omitted = torch.stack((torch.zeros_like(all_values), all_values.detach()), 1).requires_grad_()
    rewards = torch.tensor([[1., -2.], [-1., 2.]], dtype=torch.float64, requires_grad=True)
    mask = torch.ones(2, 2, dtype=torch.bool)
    result, audit = ops.mrtpo_advantages(rewards, all_values, omitted, mask)
    for b in range(2):
        qs = []
        for t in range(2):
            p = all_values[b, t].detach().softmax(-1).tolist()
            q = [.5, .5]
            js = sum((p[v] * math.log(p[v] / ((p[v] + q[v]) / 2))
                      + q[v] * math.log(q[v] / ((p[v] + q[v]) / 2))) / 2 for v in range(2))
            qs.append(math.sqrt(js / math.log(2)))
        mean = sum(qs) / 2
        torch.testing.assert_close(audit["weights"][b, 0], torch.tensor([.5 + .5 * v / mean for v in qs], dtype=torch.float64))
    torch.testing.assert_close(audit["weights"][:, 1], torch.ones(2, 2, dtype=torch.float64))
    torch.testing.assert_close(audit["bounded"].mean(1), rewards.detach().sum(1))
    assert float(audit["bounded"].square().mean()) <= 2 * float(audit["uniform"].square().mean()) + 1e-12
    assert not result.requires_grad
    warmup, initial = ops.mrtpo_advantages(rewards, all_values, omitted, mask, step=0)
    torch.testing.assert_close(initial["weights"], torch.ones_like(initial["weights"]))
    assert warmup.isfinite().all()


def test_mrtpo_padding_nan_is_excluded_from_replay_and_averages():
    values = torch.tensor([[[2., 0.], [float("nan")] * 2], [[1., 2.], [2., 1.]]], dtype=torch.float64)
    omitted = torch.stack((values.clone(), values.clone()), 1)
    mask = torch.tensor([[True, False], [True, True]])
    result, audit = ops.mrtpo_advantages(torch.tensor([[1., 0.], [-1., 0.]]), values, omitted, mask)
    assert result.isfinite().all() and result[0, 1] == 0
    assert audit["weights"][0, :, 1].count_nonzero() == 0
    with pytest.raises(ValueError, match="valid logits"):
        ops.mrtpo_advantages(torch.zeros(2, 2), values + float("nan"), omitted, mask)


@pytest.mark.parametrize("criterion", ["entropy", "hellinger", "features"])
def test_teacher_routing_scores_hard_soft_arithmetic_mixture_and_detach(criterion):
    student = torch.tensor([[[1., 0.], [0., 2.]]], dtype=torch.float64, requires_grad=True)
    teachers = torch.tensor([[[[2., 0.], [0., 2.]]], [[[0., 2.], [2., 0.]]]], dtype=torch.float64, requires_grad=True)
    mask = torch.ones(1, 2, dtype=torch.bool)
    student_f = torch.tensor([[[0., 0.], [1., 1.]]], dtype=torch.float64, requires_grad=True)
    teacher_f = torch.tensor([[[[0., 0.], [2., 2.]]], [[[1., 1.], [1., 1.]]]], dtype=torch.float64, requires_grad=True)
    target, weights = ops.route_teachers(student, teachers, mask, criterion=criterion,
        temperature=.3, student_features=student_f, teacher_features=teacher_f)
    probabilities = teachers.detach().softmax(-1)
    if criterion == "entropy":
        scores = (probabilities * teachers.detach().log_softmax(-1)).sum(-1)
    elif criterion == "hellinger":
        scores = -(.5 * (probabilities.sqrt() - student.detach().softmax(-1).sqrt()[None]).square().sum(-1)).sqrt()
    else:
        scores = -(teacher_f.detach() - student_f.detach()[None]).square().sum(-1)
    torch.testing.assert_close(weights, (scores / .3).softmax(0))
    torch.testing.assert_close(target.exp(), (weights[..., None] * probabilities).sum(0))
    hard, hard_weights = ops.route_teachers(student, teachers, mask, criterion=criterion,
        temperature=0, student_features=student_f, teacher_features=teacher_f)
    assert (hard_weights.sum(0) == 1).all() and ((hard_weights == 0) | (hard_weights == 1)).all()
    torch.testing.assert_close(hard.exp(), (hard_weights[..., None] * probabilities).sum(0))
    labels = torch.tensor([[0, 1]])
    loss = ops.routed_opd_loss(student, target, labels, mask)
    loss.backward()
    assert student.grad is not None and student.grad.isfinite().all()
    assert all(v.grad is None for v in (teachers, teacher_f, student_f))


def test_teacher_sampled_loss_is_per_response_and_not_undifferentiated_kl():
    logits = torch.tensor([[[1., 0.], [3., -1.]], [[0., 2.], [float("nan")] * 2]], dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([[True, True], [True, False]])
    target = torch.tensor([[[.2, .8], [.7, .3]], [[.6, .4], [.5, .5]]], dtype=torch.float64).log()
    labels = torch.tensor([[0, 1], [1, -1]])
    loss = ops.routed_opd_loss(logits, target, labels, mask)
    scalar = []
    for b in range(2):
        terms = []
        for t in range(2):
            if mask[b, t]:
                lp = logits[b, t].log_softmax(-1)[labels[b, t]]
                terms.append(-(target[b, t, labels[b, t]] - lp.detach()) * lp)
        scalar.append(torch.stack(terms).mean())
    torch.testing.assert_close(loss, torch.stack(scalar).mean())
    loss.backward()
    assert logits.grad.isfinite().all() and (logits.grad[~mask] == 0).all()


def test_information_gain_uses_log_stabilized_mean_probability_and_telescopes():
    scores = torch.tensor([[[-4., -2.], [-2., -1.], [-3., -2.]]], dtype=torch.float64, requires_grad=True)
    gained = ops.information_gains(scores, torch.ones_like(scores, dtype=torch.bool))
    potentials = [math.log(math.exp(v) + .001) for v in (-3., -1.5, -2.5)]
    torch.testing.assert_close(gained, torch.tensor([[potentials[1] - potentials[0], potentials[2] - potentials[1]]], dtype=torch.float64))
    assert not gained.requires_grad and gained[0, 0] > 0 and gained[0, 1] < 0


def test_ig_budgets_equal_turns_not_tokens_and_iqc_outside_itc_and_formatting():
    student = torch.full((1, 7), -2., dtype=torch.float64, requires_grad=True)
    teacher = torch.full((1, 7), -1., dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([[True] * 6 + [False]])
    turns = torch.tensor([[0, 1, 1, 2, 2, 2, -1]])
    decisions = torch.tensor([[True, False, True, False, False, False, False]])
    gains = torch.tensor([[1., -2., 0.]], dtype=torch.float64, requires_grad=True)
    result, audit = ops.ig_calibrated_advantages(student, teacher, mask, turns, gains, decisions, step=60)
    rms = math.sqrt(5 / 3)
    raw = [1 + .1 * math.tanh(abs(v) / rms) for v in (1., -2., 0.)]
    shares = [v / sum(raw) for v in raw]
    torch.testing.assert_close(audit["turn_shares"], torch.tensor([shares], dtype=torch.float64))
    torch.testing.assert_close(audit["iqc"], torch.tensor([[10., 0., -20., 0., 0., 0., 0.]], dtype=torch.float64))
    expected = [6 * shares[0] + 10, 3 * shares[1], 3 * shares[1] - 20,
                2 * shares[2], 2 * shares[2], 2 * shares[2], 0.]
    torch.testing.assert_close(result, torch.tensor([expected], dtype=torch.float64))
    assert not result.requires_grad
    equal, no_gain = ops.ig_calibrated_advantages(student, teacher, mask, turns, gains * 0, decisions, strength=0)
    torch.testing.assert_close(equal, torch.tensor([[2., 1., 1., 2 / 3, 2 / 3, 2 / 3, 0.]], dtype=torch.float64))
    assert no_gain["iqc"].count_nonzero() == 0
    with pytest.raises(ValueError, match="action-critical"):
        ops.ig_calibrated_advantages(student, teacher, mask, turns, gains, decisions & False)


def test_note_screen_admission_strict_fresh_outcomes_and_all_fail_recovery():
    assert ops.note_has_answer((1, 7, 8, 3), (7, 8))
    assert not ops.note_has_answer((1, 7, 3, 8), (7, 8))
    assert ops.admit_note([0, 0, 0], [0, 1], valid=True, leaks_answer=False)
    assert not ops.admit_note([0, 1], [0, 1], valid=True, leaks_answer=False)
    assert not ops.admit_note([0, 0], [1, 1], valid=True, leaks_answer=True)
    assert not ops.admit_note([0, 0], [1, 1], valid=False, leaks_answer=False)
    with pytest.raises(ValueError, match="binary"):
        ops.admit_note([0, .5], [1], valid=True, leaks_answer=False)


def test_rshd_aux_uses_clipped_detached_lift_and_counts_zero_weight_tokens():
    plain = torch.tensor([[[0., 1.], [2., 0.]], [[1., 0.], [float("nan")] * 2]], dtype=torch.float64, requires_grad=True)
    privileged = torch.tensor([[[2., 0.], [3., 0.]], [[0., 1.], [float("nan")] * 2]], dtype=torch.float64, requires_grad=True)
    labels, mask = torch.tensor([[0, 1], [0, -1]]), torch.tensor([[True, True], [True, False]])
    loss, weights = ops.rshd_aux_loss(plain, privileged, labels, mask, torch.tensor([True, False]), cap=.5)
    lp = plain[0].log_softmax(-1)
    expected = -.5 * lp[0, 0] / 2  # second admitted token has zero lift but counts
    torch.testing.assert_close(loss, expected)
    assert weights[0, 0] == .5 and weights[0, 1] == 0 and weights[1].count_nonzero() == 0
    loss.backward()
    assert plain.grad.isfinite().all() and (plain.grad[~mask] == 0).all() and privileged.grad is None
    zero, _ = ops.rshd_aux_loss(plain, privileged, labels, mask, torch.tensor([False, False]))
    assert zero.item() == 0


def runner():
    spec = importlib.util.spec_from_file_location("oct18_post_runner", ROOT / "scripts/run_oct18_post_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("name", ["run_tag", "run_mrtpo", "run_routing", "run_ig", "run_rshd"])
def test_real_causal_rollouts_updates_references_and_negative_controls(name):
    torch.set_num_threads(1)
    torch.manual_seed(42)
    values = getattr(runner(), name)("cpu", 3)
    assert values["parameter_delta_l2"] > 0 and values["gradient_norm_min"] > 0 and values["optimizer_updates"] == 3
    for key, value in values.items():
        if "error" in key or "negative_control" in key:
            assert abs(value) < 1e-10, (key, value)
    if name == "run_rshd":
        assert values["accepted_notes"] > 0 and values["positive_lift_tokens"] > 0
        assert values["note_writer_receives_reference_answer"] is False
        assert values["semantic_note_screen_implemented"] is False


def test_runner_refuses_overwrite_without_running(tmp_path):
    output = tmp_path / "existing.json"
    output.write_text("preserve me")
    result = subprocess.run([sys.executable, str(ROOT / "scripts/run_oct18_post_components.py"), "--output", str(output)],
        cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode != 0 and "immutable" in result.stderr and output.read_text() == "preserve me"


def test_ig_reference_answer_is_scored_only_by_the_frozen_teacher(monkeypatch):
    module = runner()
    original = module.score
    probes = []

    def record(model, prompt, response, device):
        if len(response) == 1:
            assert all(not parameter.requires_grad for parameter in model.parameters())
            probes.append((prompt, response))
        return original(model, prompt, response, device)

    monkeypatch.setattr(module, "score", record)
    torch.manual_seed(42)
    module.run_ig("cpu", 1)
    assert len(probes) == 8 * 3
    assert {len(prompt) for prompt, _ in probes} == {2, 5, 8}


def test_rshd_note_writer_receives_only_prompt_failed_response_and_failure_marker(monkeypatch):
    module = runner()
    original = module.sample
    requests = []

    def record(model, prompt, length, device):
        if length == 2:
            assert len(prompt) == 6  # two prompt tokens + three failed tokens + marker
            assert prompt[-1] == 27
            assert all(not parameter.requires_grad for parameter in model.parameters())
            requests.append(prompt)
        return original(model, prompt, length, device)

    monkeypatch.setattr(module, "sample", record)
    torch.manual_seed(42)
    module.run_rshd("cpu", 1)
    assert requests


@pytest.mark.parametrize("key", KEYS)
def test_component_catalog_cannot_promote_diagnostics_or_full_experiments(key):
    row = json.loads((ROOT / "src/auto_research/paper_specs/catalog/post-training" / f"{key}.json").read_text())
    assert row["adapter"] is None and row["implementation_status"] == "component_only"
    assert row["diagnostic_only"] is True and row["promotion_eligible"] is False and row["evolve_integrated"] is False
    assert row["full_experiment_status"] == "not_reproduced_high_cost" and row["requires_gpu_validation"] is True
    assert row["gpu_validation_artifact"] == f"docs/gpu-validations/{key}-a100-20261018.json"
    assert row["first_author_affiliation"] and row["published_at"].startswith(row["published"])
    text = (ROOT / "docs" / row["detail_path"]).read_text()
    for token in ("## 论文信息", "## 原始论文总结", "### 核心公式", "## 本地复现", "不复现", "DONE"):
        assert token in text
@pytest.mark.parametrize("dtype", [torch.float16, torch.float32, torch.float64])
def test_hard_teacher_routing_preserves_exact_zero_mass_at_extreme_logits(dtype):
    from auto_research.post_training.reviewed_oct18 import route_teachers

    student = torch.zeros(1, 1, 2, dtype=dtype)
    teachers = torch.tensor([[[[100., -100.]]], [[[-100., 100.]]]], dtype=dtype)
    mask = torch.ones(1, 1, dtype=torch.bool)
    target, weights = route_teachers(student, teachers, mask, criterion="entropy", temperature=0)
    assert torch.equal(weights[:, 0, 0], torch.tensor([1., 0.], dtype=dtype))
    assert torch.equal(target, teachers[0].log_softmax(-1))

