"""Independent math, failure controls and real tiny-policy update contracts."""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import statistics
import sys

import pytest
import torch

from auto_research.post_training import gr_opd, sim_opd, tree_opsd

ROOT = Path(__file__).resolve().parents[2]


def test_tree_merges_complete_prefix_not_just_matching_actor_text():
    a, b, c = tree_opsd.Turn((2,), (8,)), tree_opsd.Turn((3,), (9,)), tree_opsd.Turn((4,))
    merged = tree_opsd.merge_rollout_prefixes((1,), [[a, c], [a, c], [b, c]])
    assert len(merged["nodes"]) == 4
    assert merged["leaf_indices"] == [1, 1, 3]
    assert merged["nodes"][1]["history"] == (1, 2, 8)
    assert merged["nodes"][3]["history"] == (1, 3, 9)
    # An observation is context identity, not an actor span to score.
    changed = tree_opsd.Turn((2,), (10,))
    assert len(tree_opsd.merge_rollout_prefixes((1,), [[a, c], [changed, c]])["nodes"]) == 4


def test_tree_backup_uses_sample_std_and_full_span_likelihood_not_uniform_weight():
    parents = [-1, 0, 0, 1, 1]
    logp = torch.tensor([-2., -1., -3., -2., -4.], dtype=torch.float64, requires_grad=True)
    rewards = torch.tensor([0., .5, 1.], dtype=torch.float64, requires_grad=True)
    result = tree_opsd.tree_credit(parents, logp, [2, 3, 4], rewards)
    # sample std = .5; parent 1 backs up the .5/1 leaves with exp(-2)/exp(-4).
    expected_one = math.exp(-4) / (math.exp(-2) + math.exp(-4))
    expected_root = (math.exp(-1) * expected_one - math.exp(-3)) / (math.exp(-1) + math.exp(-3))
    assert result.tolist() == pytest.approx([expected_root, expected_one, -1., 0., 1.])
    assert not result.requires_grad
    assert result[1] != pytest.approx(.5)
    assert tree_opsd.tree_credit(parents, logp, [2, 3, 4], torch.ones(3)).count_nonzero() == 0


def test_tree_duplicate_leaf_rewards_cannot_conflict_and_all_leaves_must_be_covered():
    with pytest.raises(ValueError, match="conflicting"):
        tree_opsd.tree_credit([-1], torch.zeros(1), [0, 0], torch.tensor([0., 1.]))
    with pytest.raises(ValueError, match="exactly all"):
        tree_opsd.tree_credit([-1, 0, 0], torch.zeros(3), [1, 1], torch.zeros(2))
    with pytest.raises(ValueError, match="acyclic"):
        tree_opsd.tree_credit([-1, 2, 0], torch.zeros(3), [1, 2], torch.zeros(2))


def test_tree_posterior_exact_kl_tangent_mask_and_frozen_targets():
    current = torch.tensor([[.1, .3, float("nan")], [-.2, float("nan"), float("nan")]], dtype=torch.float64, requires_grad=True)
    old = torch.zeros_like(current, requires_grad=True)
    mask = torch.tensor([[True, True, False], [True, False, False]])
    credit = torch.tensor([.4, -.4], dtype=torch.float64, requires_grad=True)
    loss, audit = tree_opsd.posterior_loss(current, old, mask, credit, terminal_count=4)
    tau = 3 / (.25 * 2)
    p, q = [1 / (1 + math.exp(-.2)), 1 / (1 + math.exp(.2))], [.5 + .4 / tau, .5 - .4 / tau]
    terms = [a * math.log(a / b) + (1 - a) * math.log((1 - a) / (1 - b)) for a, b in zip(q, p, strict=True)]
    assert float(loss.detach()) == pytest.approx(tau * (2 * terms[0] + terms[1]) / 3, abs=1e-14)
    assert audit["unique_actor_tokens"] == 3
    loss.backward()
    assert current.grad.isfinite().all() and current.grad[~mask].count_nonzero() == 0
    assert old.grad is None and credit.grad is None
    baseline = torch.zeros(2, 2, dtype=torch.float64, requires_grad=True)
    zero_loss, _ = tree_opsd.posterior_loss(baseline, baseline.detach(), torch.ones_like(baseline, dtype=torch.bool), credit, terminal_count=4)
    gradient = torch.autograd.grad(zero_loss, baseline)[0]
    torch.testing.assert_close(gradient, -credit.detach()[:, None].expand_as(baseline) / 4)


def test_tree_target_stops_and_overshoot_reverses_without_clipping_invalid_credit():
    tau, q = 1 / (.25 * math.sqrt(2)), .7
    score = torch.tensor([[math.log(q / (1 - q))], [math.log(q / (1 - q)) + 1]], dtype=torch.float64, requires_grad=True)
    value, _ = tree_opsd.posterior_loss(score, torch.zeros_like(score), torch.ones_like(score, dtype=torch.bool),
        torch.full((2,), (q - .5) * tau, dtype=torch.float64), terminal_count=2)
    gradient = torch.autograd.grad(value, score)[0]
    assert abs(float(gradient[0])) < 1e-14 and gradient[1] > 0
    with pytest.raises(ValueError, match="do not clip"):
        tree_opsd.posterior_loss(score, torch.zeros_like(score), torch.ones_like(score, dtype=torch.bool), torch.tensor([10., -10.]), terminal_count=2)


def test_simopd_pool_normalizes_each_token_then_means_selected_layers_and_positions():
    states = torch.tensor([[[[3., 4.], [0., 2.], [float("nan"), 0.]]], [[[0., 5.], [2., 0.], [0., float("nan")]]]], dtype=torch.float64, requires_grad=True)
    pooled = sim_opd.pool_response_states(states, torch.tensor([[True, True, False]]))
    torch.testing.assert_close(pooled, torch.tensor([[(.6 + 0 + 0 + 1) / 4, (.8 + 1 + 1 + 0) / 4]], dtype=torch.float64))
    pooled.sum().backward()
    assert states.grad.isfinite().all() and states.grad[:, :, -1].count_nonzero() == 0
    with pytest.raises(ValueError, match="active tokens"):
        sim_opd.pool_response_states(states, torch.zeros(1, 3, dtype=torch.bool))


def test_simopd_forward_kl_cross_dimensions_and_paired_fifo_detaches_history():
    bank = sim_opd.PairedMemoryBank(3)
    sb = torch.tensor([[1., 0.], [0., 1.], [1., 1.]], dtype=torch.float64, requires_grad=True)
    tb = torch.tensor([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]], dtype=torch.float64, requires_grad=True)
    bank.append(sb, tb, ("A", "B", "C"))
    student = torch.tensor([[1., .2]], dtype=torch.float64, requires_grad=True)
    teacher = torch.tensor([[.2, 1., .3]], dtype=torch.float64, requires_grad=True)
    loss, audit = bank.loss(student, teacher, temperature=.5)
    ls = torch.tensor([[1., .2]], dtype=torch.float64)
    st = [float(torch.nn.functional.cosine_similarity(ls, row[None])) / .5 for row in sb.detach()]
    tt = [float(torch.nn.functional.cosine_similarity(teacher.detach(), row[None])) / .5 for row in tb.detach()]
    normalize = lambda values: [math.exp(v) / sum(math.exp(x) for x in values) for v in values]
    ps, pt = normalize(st), normalize(tt)
    expected = sum(t * math.log(t / s) for s, t in zip(ps, pt, strict=True))
    assert float(loss.detach()) == pytest.approx(expected, abs=1e-14)
    loss.backward()
    assert student.grad.abs().sum() > 0
    assert teacher.grad is None and sb.grad is None and tb.grad is None
    assert not bank.student.requires_grad and not bank.teacher.requires_grad
    assert audit["bank_response_ids"] == ("A", "B", "C")
    bank.append(sb[:2], tb[:2], ("D", "E"))
    assert bank.ids == ("C", "D", "E")
    torch.testing.assert_close(bank.student, torch.stack((sb[2], sb[0], sb[1])).detach())


def test_simopd_warmup_and_misaligned_history_are_not_silently_accepted():
    bank = sim_opd.PairedMemoryBank(3)
    bank.append(torch.ones(1, 2), torch.ones(1, 3), ("one",))
    with pytest.raises(ValueError, match="degenerate"):
        bank.loss(torch.ones(1, 2), torch.ones(1, 3))
    with pytest.raises(ValueError, match="identity"):
        bank.append(torch.ones(2, 2), torch.ones(2, 3), ("one",))
    with pytest.raises(ValueError, match="dimensions"):
        bank.append(torch.ones(1, 4), torch.ones(1, 3), ("two",))


@pytest.mark.parametrize("side", ["student", "teacher"])
def test_simopd_rejects_zero_hidden_dimension_and_mismatched_dtypes(side):
    student, teacher = torch.ones(2, 2), torch.ones(2, 3)
    bank = sim_opd.PairedMemoryBank(3)
    bank.append(student, teacher, ("A", "B"))
    empty_student = torch.empty(2, 0) if side == "student" else student
    empty_teacher = torch.empty(2, 0) if side == "teacher" else teacher
    with pytest.raises(ValueError, match="nonempty"):
        sim_opd.PairedMemoryBank(3).append(empty_student, empty_teacher, ("A", "B"))
    with pytest.raises(ValueError, match="nonempty"):
        bank.loss(empty_student, empty_teacher)
    with pytest.raises(ValueError, match="dtype"):
        sim_opd.PairedMemoryBank(3).append(student.double(), teacher, ("A", "B"))
    with pytest.raises(ValueError, match="dtype"):
        bank.append(student.double(), teacher.double(), ("C", "D"))
    with pytest.raises(ValueError, match="dtype"):
        bank.loss(student.double(), teacher.double())
    with pytest.raises(ValueError, match="floating"):
        bank.loss(student.long(), teacher.long())


def test_gr_opd_discounted_mean_population_std_and_pressure_not_raw_sum():
    teacher = torch.tensor([[2., 4., float("nan")], [0., 4., 8.], [-8., float("nan"), float("nan")]], dtype=torch.float64, requires_grad=True)
    old = torch.zeros_like(teacher, requires_grad=True)
    mask = torch.tensor([[True, True, False], [True, True, True], [True, False, False]])
    advantage, audit = gr_opd.sequence_credit(teacher, old, mask, ["Q", "Q", "solo"], gamma=.5, pressure=.25)
    values = [(2 + .5 * 4) / 1.5, (0 + .5 * 4 + .25 * 5) / 1.75]
    mu, sigma = statistics.mean(values), statistics.pstdev(values)
    expected = [max(-5., min(5., (v - mu + .25 * mu) / (sigma + 1e-6))) for v in values]
    assert audit["sequence_scores"].tolist() == pytest.approx(values + [-5.])
    assert advantage.tolist() == pytest.approx(expected + [-5.])
    assert not advantage.requires_grad and not audit["sequence_scores"].requires_grad
    zero, _ = gr_opd.sequence_credit(teacher, old, mask, ["A", "B", "C"], pressure=0.)
    assert zero.count_nonzero() == 0


def test_gr_ppo_balances_responses_not_tokens_and_ignores_masked_nan():
    current = torch.tensor([[math.log(2), float("nan")], [math.log(.5), math.log(1.1)]], dtype=torch.float64, requires_grad=True)
    old = torch.zeros_like(current, requires_grad=True)
    a = torch.tensor([1., -2.], dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([[True, False], [True, True]])
    loss = gr_opd.clipped_policy_loss(current, old, mask, a)
    expected = (-min(2., 1.2) - (min(.5 * -2, .8 * -2) + min(1.1 * -2, 1.1 * -2)) / 2) / 2
    assert float(loss.detach()) == pytest.approx(expected)
    assert float(loss.detach()) != pytest.approx((-1.2 + 1.6 + 2.2) / 3)
    loss.backward()
    assert current.grad.isfinite().all() and current.grad[~mask].count_nonzero() == 0
    assert old.grad is None and a.grad is None


def test_gr_teacher_eos_alignment_never_changes_student_rollout_or_padding():
    original = torch.tensor([[4, 5, 0], [5, 4, 5]], dtype=torch.long)
    mask = torch.tensor([[True, True, False], [True, True, False]])
    copied = gr_opd.teacher_scoring_copy(original, mask, student_eos=5, teacher_eos=6)
    assert copied.tolist() == [[4, 6, 0], [5, 4, 5]]
    assert original.tolist() == [[4, 5, 0], [5, 4, 5]]


@pytest.mark.parametrize("dtype", [torch.float16, torch.float32, torch.float64])
def test_gr_ppo_extreme_clipped_positive_branch_has_finite_zero_gradient(dtype):
    current = torch.tensor([[-1.]], dtype=dtype, requires_grad=True)
    old = torch.tensor([[-1001.]], dtype=dtype)
    loss = gr_opd.clipped_policy_loss(current, old, torch.ones(1, 1, dtype=torch.bool), torch.ones(1, dtype=dtype))
    assert float(loss.detach()) == pytest.approx(-1.2, abs=.002)
    loss.backward()
    assert torch.isfinite(current.grad).all() and current.grad.count_nonzero() == 0
    # The other selected branch is mathematically unbounded, not a clipped term.
    with pytest.raises(ValueError, match="not representable"):
        gr_opd.clipped_policy_loss(current, old, torch.ones(1, 1, dtype=torch.bool), -torch.ones(1, dtype=dtype))


def load_runner():
    spec = importlib.util.spec_from_file_location("evening_post_runner", ROOT / "scripts/run_oct19_evening_post_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("key", ["treeopsd", "simopd", "gr-opd"])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_real_tiny_causal_updates_match_independent_references(key, seed):
    module = load_runner()
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    function = {"treeopsd": module.run_treeopsd, "simopd": module.run_simopd, "gr-opd": module.run_gr_opd}[key]
    result = function("cpu", 3)
    metric = result["metrics"]
    assert metric["parameter_delta_l2"] > 0 and metric["gradient_norm_min"] > 0
    assert metric["optimizer_updates"] == 3 and metric["loss_reference_max_abs_error"] < 1e-12
    if key == "treeopsd":
        assert metric["credit_reference_max_abs_error"] < 1e-12
        assert metric["shared_prefix_turn_savings_min"] > 0
        assert metric["target_gradient_max_abs_error"] < 1e-12 and metric["overshoot_loss_gradient"] > 0
    else:
        assert metric["teacher_parameter_delta_l2"] == metric["teacher_gradient_count"] == 0
    if key == "simopd":
        assert metric["warmup_optimizer_updates"] == 0 and metric["paired_preupdate_fifo_verified"]
        assert metric["mispaired_bank_negative_control_abs_difference_min"] > 0
    if key == "gr-opd":
        assert metric["credit_reference_max_abs_error"] < 1e-12
        assert metric["global_token_weighting_negative_control_abs_difference_max"] > 0


def test_runner_schema_hashes_and_immutable_output(tmp_path, monkeypatch):
    module = load_runner()
    output = tmp_path / "result.json"
    arguments = ["runner", "--methods", "treeopsd,simopd,gr-opd", "--seeds", "42,43,44", "--steps", "1",
                 "--code-commit", "a" * 40, "--output", str(output)]
    monkeypatch.setattr(sys, "argv", arguments)
    module.main()
    payload = json.loads(output.read_text())
    assert set(payload["executed_source_sha256"]) == set(module.SOURCES)
    assert payload["full_experiment_status"] == "not_reproduced_high_cost"
    for component in payload["components"].values():
        assert component["full_experiment_status"] == "not_reproduced_high_cost"
        assert component["diagnostic_only"] and not component["promotion_eligible"] and not component["evolve_integrated"]
        assert [row["seed"] for row in component["per_seed"]] == [42, 43, 44]
        assert component["metrics"]["parameter_delta_l2"]["n"] == 3
        assert component["dataset"]["id"].startswith("synthetic:")
    before = output.read_bytes()
    with pytest.raises(SystemExit):
        module.main()
    assert output.read_bytes() == before
