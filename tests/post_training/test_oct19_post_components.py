"""KnowGPO prior-state credit and DIVERGE observation-protocol contracts."""
from __future__ import annotations

import importlib.util
import itertools
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest
import torch

from auto_research.post_training import reviewed_oct19 as ops

ROOT = Path(__file__).resolve().parents[2]


def fixture_states():
    changes = torch.tensor([[[1, 0], [0, 1], [0, 0]], [[0, 0], [1, 0], [0, 0]],
                            [[1, 0], [0, 1], [0, 0]], [[0, 0], [1, 0], [0, 0]]], dtype=torch.bool)
    valid = torch.ones(4, 3, dtype=torch.bool)
    answer = torch.tensor([[False, False, True]] * 4)
    before, after = ops.accumulate_knowledge(changes, valid)
    return before, after, valid, answer


def test_accumulation_is_monotone_and_repeated_evidence_adds_no_gain():
    changes = torch.tensor([[[True, False], [True, False], [False, True], [False, False]]])
    before, after = ops.accumulate_knowledge(changes, torch.tensor([[True, True, True, False]]))
    assert before.tolist() == [[[False, False], [True, False], [True, False], [True, True]]]
    assert after.tolist() == [[[True, False], [True, False], [True, True], [True, True]]]
    with pytest.raises(ValueError, match="padding"):
        ops.accumulate_knowledge(changes, torch.tensor([[True, False, True, False]]))


def test_knowgpo_uses_prior_state_not_posterior_and_never_mixes_queries():
    before, after, valid, answer = fixture_states()
    credit, audit = ops.knowledge_advantages(["A", "A", "B", "B"], before, after, valid, answer,
        torch.tensor([1., 0., 0., 1.], dtype=torch.float64), omega=.5)
    groups = {(row["query_id"], tuple(row["before_state"])): row for row in audit["groups"]}
    assert groups[("A", (False, False))]["positions"] == [[0, 0], [1, 0], [1, 1]]
    assert groups[("B", (False, False))]["positions"] == [[2, 0], [3, 0], [3, 1]]
    assert groups[("A", (True, False))]["positions"] == [[0, 1]]
    assert groups[("A", (True, False))]["advantages"] == [0.]
    expected = [(1 - 2 / 3) / (math.sqrt(2 / 9) + 1e-6), (-2 / 3) / (math.sqrt(2 / 9) + 1e-6)]
    assert audit["step_advantages"][0, 0] == pytest.approx(expected[0])
    assert audit["step_advantages"][1, 0] == pytest.approx(expected[1])
    assert not credit.requires_grad and audit["step_advantages"][answer].count_nonzero() == 0
    torch.testing.assert_close(credit[answer], .5 * audit["episode_advantages"])
    assert all(all(t != 2 for _, t in row["positions"]) for row in audit["groups"])


@pytest.mark.parametrize("mutation", ["reset", "nonmonotone", "answer_gain"])
def test_knowgpo_rejects_fabricated_states_and_terminal_acquisition(mutation):
    before, after, valid, answer = fixture_states()
    if mutation == "reset":
        before[0, 1] = False
    elif mutation == "nonmonotone":
        after[0, 1] = False
    else:
        after[1, 2, 1] = True
    with pytest.raises(ValueError):
        ops.knowledge_advantages(["A"] * 4, before, after, valid, answer, torch.zeros(4))


def test_broadcast_never_credits_observation_or_padding_and_detaches_verifier_credit():
    step = torch.tensor([[1., -2., 3.]], requires_grad=True)
    ids = torch.tensor([[0, 0, -1, 1, 1, -1, 2, 2, -1]])
    mask = ids >= 0
    result = ops.broadcast_step_advantages(step, ids, mask)
    assert result.tolist() == [[1., 1., 0., -2., -2., 0., 3., 3., 0.]]
    assert not result.requires_grad
    with pytest.raises(ValueError, match="invalid step"):
        ops.broadcast_step_advantages(step, ids + 10, mask)


def test_clipped_ppo_and_actual_full_distribution_kl_match_independent_reference():
    current = torch.tensor([[[2., 0., -1.], [0., 1., 2.], [float("nan")] * 3]], dtype=torch.float64, requires_grad=True)
    old = torch.tensor([[[0., 1., 2.], [2., 1., 0.], [float("nan")] * 3]], dtype=torch.float64, requires_grad=True)
    reference = torch.zeros(1, 3, 3, dtype=torch.float64, requires_grad=True)
    labels, mask = torch.tensor([[0, 2, -1]]), torch.tensor([[True, True, False]])
    credit = torch.tensor([[1., -2., float("nan")]], dtype=torch.float64, requires_grad=True)
    loss, parts = ops.knowgpo_policy_loss(current, old, reference, labels, mask, credit, kl_coefficient=.2)
    terms, kls = [], []
    for t in range(2):
        lp, lo = current[0, t].log_softmax(-1), old[0, t].detach().log_softmax(-1)
        lr = reference[0, t].detach().log_softmax(-1)
        ratio = (lp[labels[0, t]] - lo[labels[0, t]]).exp()
        a = credit[0, t].detach()
        kl = (lp.exp() * (lp - lr)).sum()
        kls.append(kl)
        terms.append(-torch.minimum(ratio * a, ratio.clamp(.8, 1.2) * a) + .2 * kl)
    torch.testing.assert_close(loss, torch.stack(terms).mean())
    torch.testing.assert_close(parts["reverse_kl"], torch.stack(kls).mean())
    assert parts["reverse_kl"] > 0
    loss.backward()
    assert current.grad.isfinite().all() and (current.grad[~mask] == 0).all()
    assert all(value.grad is None for value in (old, reference, credit))


def cards():
    return [{"problem_gap": "gap: missing capability", "core_claim": "claim", "method": "method: intervention", "inspiration": "source"} for _ in range(3)]


def validate(values, **kwargs):
    return ops.validate_idea_schema(values, expected_count=3, has_think_block=kwargs.get("think", True),
        has_answer_block=kwargs.get("answer", True), problem_label_valid=lambda t: t.startswith("gap:"),
        method_label_valid=lambda t: t.startswith("method:"))


def test_structural_gate_requires_both_blocks_four_fields_taxonomy_and_exact_k():
    values = cards()
    assert validate(values)
    assert not validate(values, think=False) and not validate(values, answer=False)
    assert not validate(values[:2])
    for field in ops.IDEA_FIELDS:
        bad = [dict(row) for row in values]
        bad[0][field] = ""
        assert not validate(bad)
    bad = [dict(row) for row in values]
    bad[1]["method"] = "invalid label"
    assert not validate(bad)


def test_judge_observation_contract_two_order_votes_and_three_field_mean():
    values = cards()
    for i, row in enumerate(values):
        row["id"] = i
    calls = []

    def impact(card, reverse):
        calls.append((card["id"], reverse))
        return card["id"] == 0 or (card["id"] == 1 and not reverse)

    q, d = ops.observe_idea_judgments(values, schema_valid=True, impact_judge=impact,
        field_distance_judge=lambda a, b: [.2, .4, .6])
    assert q == [1., .5, 0.] and len(calls) == 6
    assert d[0][0] == 0 and d[0][1] == pytest.approx(.4) and d[0][1] == d[1][0]
    with pytest.raises(ValueError, match="Boolean"):
        ops.observe_idea_judgments(values, schema_valid=True, impact_judge=lambda *_: .5,
            field_distance_judge=lambda *_: [0., 0., 0.])


def test_invalid_schema_never_invokes_judges_or_validates_missing_observations():
    def forbidden(*_):
        pytest.fail("invalid output invoked an expensive judge")
    assert ops.observe_idea_judgments(cards(), schema_valid=False, impact_judge=forbidden,
        field_distance_judge=forbidden) == ([], [])
    assert ops.set_reward([], [], schema_valid=False, judged_token_length=100)["reward"] == 0


def test_set_reward_uses_generation_order_no_patience_and_capped_judged_field_length():
    q, d = [1., .5, .8], [[0., .9, .1], [.9, 0., .1], [.1, .1, 0.]]
    value = ops.set_reward(q, d, schema_valid=True, judged_token_length=2500)
    assert value["marginals"] == pytest.approx([1., .45, .08])
    assert value["reward"] == pytest.approx(.05 + 1 + .45 + .08 - 1.5)
    assert ops.set_reward(q, d, schema_valid=True, judged_token_length=1000)["length_penalty"] == 0
    assert ops.set_reward(q, d, schema_valid=True, judged_token_length=4000)["length_penalty"] == 3
    assert ops.set_reward(q, d, schema_valid=True, judged_token_length=9000)["length_penalty"] == 3
    duplicates = [[0.] * 3 for _ in q]
    assert ops.set_reward(q, duplicates, schema_valid=True, judged_token_length=0)["marginals"] == [1., 0., 0.]
    reverse = ops.set_reward(q[::-1], [row[::-1] for row in d[::-1]], schema_valid=True, judged_token_length=0)
    assert reverse["set_score"] != pytest.approx(value["set_score"])


def test_cu_greedy_is_labeled_lower_bound_exact_is_bounded_and_independently_enumerated():
    q, d = [.8, 1., .6], [[0., .4, .9], [.4, 0., .2], [.9, .2, 0.]]
    exact, _ = ops.creative_utility(q, d, exact=True)
    expected = []
    for order in itertools.permutations(range(3)):
        total = sum(.9 ** t * q[i] * min([d[i][j] for j in order[:t]], default=1.) for t, i in enumerate(order))
        expected.append(total / (1 + .9 + .81))
    assert exact == pytest.approx(max(expected))
    greedy, order = ops.creative_utility(q, d)
    assert greedy <= exact + 1e-15 and order[0] == 1
    with pytest.raises(ValueError, match="eight"):
        ops.creative_utility([.5] * 9, [[0.] * 9 for _ in range(9)], exact=True)


@pytest.mark.parametrize("quality,distance", [([float("nan")], [[0.]]), ([1.], [[.2]]),
    ([.5, 1.], [[0., .5], [.3, 0.]]), ([1.2], [[0.]])])
def test_bad_judge_observations_are_rejected(quality, distance):
    with pytest.raises(ValueError):
        ops.set_reward(quality, distance, schema_valid=True, judged_token_length=0)


def runner():
    spec = importlib.util.spec_from_file_location("oct19_post_runner", ROOT / "scripts/run_oct19_post_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_real_tiny_policy_updates_reference_and_group_audit_without_private_actor_input(monkeypatch):
    module = runner()
    seen = []
    original = module.sample

    def record(model, public_history, device):
        assert isinstance(public_history, tuple) and all(type(token) is int for token in public_history)
        seen.append(public_history)
        return original(model, public_history, device)

    monkeypatch.setattr(module, "sample", record)
    torch.manual_seed(42)
    torch.set_num_threads(1)
    result = module.run_knowgpo("cpu", 3)
    values = result["metrics"]
    assert values["parameter_delta_l2"] > 0 and values["gradient_norm_min"] > 0 and values["reverse_kl_max"] > 0
    assert values["reference_delta_l2"] == 0 and values["reference_gradient_count"] == 0
    assert values["credit_reference_max_abs_error"] < 1e-12 and values["loss_reference_max_abs_error"] < 1e-12
    assert len(result["group_audit"]) == 3 and len(seen) == 12 * 3 * 3
    assert all(row["groups"] for row in result["group_audit"])
    assert values["answer_process_max_abs_credit"] == values["observation_credit_max_abs_error"] == 0


def test_cpu_protocol_retains_explicit_judge_observations_not_fake_scijudge():
    result = runner().run_diverge(42)
    assert result["metrics"]["actual_model_or_api_judge_used"] is False
    assert result["metrics"]["scientific_quality_measured"] is False
    assert result["metrics"]["reward_and_exact_cu_reference_max_abs_error"] < 1e-12
    assert result["metrics"]["greedy_lower_bound_violation"] == 0
    assert result["metrics"]["generation_order_negative_control_abs_difference"] > 0
    assert len(result["observation_audit"]) == 12


def test_runner_immutable_and_diverge_cannot_be_mislabeled_as_cuda(tmp_path):
    output = tmp_path / "exists.json"
    output.write_text("preserve")
    command = [sys.executable, str(ROOT / "scripts/run_oct19_post_components.py")]
    result = subprocess.run(command + ["--output", str(output)], cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode and "immutable" in result.stderr and output.read_text() == "preserve"
    denied = subprocess.run(command + ["--methods", "diverge-ideation", "--device", "cuda", "--output", str(tmp_path / "new.json")],
        cwd=ROOT, text=True, capture_output=True, check=False)
    assert denied.returncode and "CPU-only" in denied.stderr


@pytest.mark.parametrize("key", ["knowgpo", "diverge-ideation"])
def test_catalog_is_nonpromotable_and_upstream_placeholder_is_not_released_code(key):
    row = json.loads((ROOT / "src/auto_research/paper_specs/catalog/post-training" / f"{key}.json").read_text())
    assert row["adapter"] is None and row["diagnostic_only"] is True and row["promotion_eligible"] is False
    assert row["evolve_integrated"] is False and row["full_experiment_status"] == "not_reproduced_high_cost"
    assert "占位" in row["code_status"] and "待" in row["code_status"]
    assert row["requires_gpu_validation"] is (key == "knowgpo")
    text = (ROOT / "docs" / row["detail_path"]).read_text()
    assert all(v in text for v in ("## 论文信息", "## 原始论文总结", "### 核心公式", "## 本地复现", "不复现", "DONE"))
