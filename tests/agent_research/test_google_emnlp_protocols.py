"""Independent numerical/protocol checks; no agent sees oracle answers."""
from datetime import date, datetime
import itertools
import math

import pytest
import torch

from auto_research.agent_research import dmast as dm
from auto_research.agent_research import finance_harness_protocol as fh
from auto_research.agent_research import sopbench_protocol as sop


def test_dmast_roles_pool_before_success_only_penalty_and_modes_seeds_separate():
    rewards = torch.tensor([1., 0., 0., 1., 1., 0., 1., 1.], requires_grad=True)
    task = torch.zeros(8, dtype=torch.long)
    modes = torch.tensor([True]*4 + [False]*4)
    seeds = torch.tensor([0]*6 + [1, 1])
    roles = torch.tensor([0, 1, 0, 1, 0, 0, 0, 0])
    penalties = torch.tensor([[.1, .8]]*8, requires_grad=True)
    adv, eligible = dm.pooled_advantages(rewards, task, modes, seeds, roles, penalties,
                                       std_correction=0, epsilon=1e-6)
    expected = (rewards[:6, None].detach() - .1 * (rewards[:6, None].detach() > 0) * penalties[:6].detach() - .5) / (.5 + 1e-6)
    torch.testing.assert_close(adv[:6], expected)
    assert eligible.tolist() == [True]*6 + [False]*2
    assert not adv.requires_grad and not eligible.requires_grad
    # Failed trajectories do not receive a length penalty.
    torch.testing.assert_close(adv[1, 0], adv[1, 1])
    # Separating role statistics or normalizing shaped rewards would be wrong.
    assert not torch.allclose(adv[:4].sum(0), torch.zeros(2))
    with pytest.raises(ValueError, match="clean"):
        dm.pooled_advantages(rewards, task, modes, seeds, torch.ones(8, dtype=torch.long), penalties,
                             std_correction=0, epsilon=1e-6)


@pytest.mark.parametrize("std_correction", [0, 1])
def test_dmast_explicit_std_convention(std_correction):
    r = torch.tensor([1., 0., 0., 1.], dtype=torch.float64)
    ids = torch.zeros(4, dtype=torch.long)
    adv, eligible = dm.pooled_advantages(r, ids, torch.ones(4, dtype=torch.bool), ids,
        torch.tensor([0, 1, 0, 1]), torch.zeros(4, 1), std_correction=std_correction, epsilon=1e-6)
    torch.testing.assert_close(adv[:, 0], (r - .5) / (r.std(correction=std_correction) + 1e-6))
    assert eligible.all()


def test_dmast_exact_clipped_pg_kappa_and_sampling_correction_gradient():
    logits = torch.tensor([[[[-1.2, .4], [-4., .1], [-1.1, -.3], [-4., -.7]]]],
                          dtype=torch.float64, requires_grad=True)
    actions = torch.zeros(1, 1, 4, dtype=torch.long)
    current = logits.detach().log_softmax(-1)[..., 0]
    old = (current - torch.tensor([[[math.log(2.), math.log(.5), 0., 0.]]])).requires_grad_()
    sampled = (old.detach() - torch.tensor([[[math.log(.5), math.log(.09), math.log(2.), math.log(.1)]]])).requires_grad_()
    # Ensure legitimate nonpositive logs while retaining the desired ratios.
    sampled = sampled.detach().clamp_max(-.001).requires_grad_()
    ref = (current - .2).requires_grad_()
    adv = torch.tensor([[.7]], dtype=torch.float64, requires_grad=True)
    loss, audit = dm.grpo_loss(logits, actions, old, sampled, ref, adv, torch.tensor([True]), torch.ones(1, 1, 4, dtype=torch.bool))
    lp = logits.log_softmax(-1)[..., 0]
    ratio = (lp - old.detach()).exp()
    correction = (old.detach() - sampled.detach()).exp()
    correction = torch.where(correction < .1, 0., correction.clamp_max(1.))
    expected = (-correction * torch.minimum(ratio * .7, ratio.clamp(.9, 1.3) * .7)
                + .05 * ((ref.detach() - lp).exp() - 1 - (ref.detach() - lp))).mean()
    torch.testing.assert_close(loss, expected, rtol=1e-12, atol=1e-14)
    expected_grad = torch.autograd.grad(expected, logits, retain_graph=True)[0]
    loss.backward()
    torch.testing.assert_close(logits.grad, expected_grad, rtol=1e-12, atol=1e-14)
    assert old.grad is sampled.grad is ref.grad is adv.grad is None
    assert audit["valid_tokens"] == 4


def test_dmast_padding_zero_variance_and_nan_do_not_create_signal():
    logits = torch.full((2, 1, 2, 3), float("nan"), requires_grad=True)
    mask = torch.zeros(2, 1, 2, dtype=torch.bool)
    frozen = torch.full((2, 1, 2), float("nan"), requires_grad=True)
    loss, audit = dm.grpo_loss(logits, torch.full((2, 1, 2), -1, dtype=torch.long), frozen,
        frozen, frozen, torch.full((2, 1), float("nan")), torch.zeros(2, dtype=torch.bool), mask)
    loss.backward()
    assert loss.item() == 0 and audit["valid_tokens"] == 0 and logits.grad.count_nonzero() == 0


@pytest.mark.parametrize("chosen_logit", [0., -1000.])
@pytest.mark.parametrize("advantage", [-1., 0.])
def test_dmast_zero_is_or_advantage_and_disabled_kl_skip_overflowing_unused_exp(chosen_logit, advantage):
    logits = torch.tensor([[[[chosen_logit, 0.]]]], dtype=torch.float64, requires_grad=True)
    old = torch.full((1, 1, 1), -1000., dtype=torch.float64, requires_grad=True)
    sampling = torch.full_like(old, -1., requires_grad=True)
    reference = torch.full_like(old, -.7, requires_grad=True)
    loss, audit = dm.grpo_loss(logits, torch.zeros(1, 1, 1, dtype=torch.long), old,
        sampling, reference, torch.tensor([[advantage]], dtype=torch.float64), torch.tensor([True]),
        torch.ones(1, 1, 1, dtype=torch.bool), beta=0.)
    loss.backward()
    assert loss.item() == 0. and audit["pg"].item() == 0. and audit["kl"].item() == 0.
    assert logits.grad.isfinite().all() and logits.grad.count_nonzero() == 0
    assert old.grad is sampling.grad is reference.grad is None


def test_dmast_active_unbounded_branch_is_not_silently_clipped():
    logits = torch.zeros(1, 1, 1, 2, dtype=torch.float64, requires_grad=True)
    old = torch.full((1, 1, 1), -1000., dtype=torch.float64)
    # IS=1 and negative advantage leave the upper branch genuinely unbounded.
    with pytest.raises(ValueError, match="not representable"):
        dm.grpo_loss(logits, torch.zeros(1, 1, 1, dtype=torch.long), old, old,
            torch.full_like(old, -.7), torch.tensor([[-1.]], dtype=torch.float64),
            torch.tensor([True]), torch.ones(1, 1, 1, dtype=torch.bool), beta=0.)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_dmast_shared_policy_diagnostic(seed):
    row = dm.diagnostic(seed)
    assert all(row["checks"].values()) and row["metrics"]["parameter_delta"] > 0
    assert row["metrics"]["eligible_trajectories"] == 6


def test_sop_and_unordered_chain_ordered_and_nested_true_or():
    a, b, c = [sop.Rule("single", name, (name + "(u=1)",)) for name in ("a", "b", "c")]
    truth = {"a": True, "b": True, "c": False}
    for order in itertools.permutations(["a(u=1)", "b(u=1)"]):
        result = sop.evaluate_trace({"service": sop.Rule("and", children=(a, b))}, truth,
                                   [*order, "service"], {"done": 1}, {"done": 1})
        assert result["passed"]
    chained = sop.Rule("chain", children=(a, sop.Rule("or", children=(b, c))))
    assert sop.evaluate_trace({"service": chained}, truth, ["a(u=1)", "b(u=1)", "service"], 1, 1)["passed"]
    # Checking a false OR alternative is not a witness for an unverified true one.
    assert not sop.evaluate_trace({"service": chained}, truth, ["a(u=1)", "c(u=1)", "service"], 1, 1)["passed"]
    assert not sop.evaluate_trace({"service": chained}, truth, ["b(u=1)", "a(u=1)", "service"], 1, 1)["passed"]


def test_sop_each_service_uses_only_its_prefix_and_requires_all_three_dimensions():
    rule = sop.Rule("single", "verified", ("check(u=1)",))
    spec, truth = {"service": rule}, {"verified": True}
    assert not sop.evaluate_trace(spec, truth, ["service", "check(u=1)"], 1, 1)["passed"]
    assert not sop.evaluate_trace(spec, truth, ["check(u=2)", "service"], 1, 1)["passed"]
    assert not sop.evaluate_trace(spec, truth, ["check(u=1)", "service"], 0, 1)["passed"]
    assert not sop.evaluate_trace(spec, {"verified": False}, ["check(u=1)", "service"], 1, 1)["passed"]
    assert sop.evaluate_trace(spec, {"verified": False}, [], 0, 0)["passed"]  # Correct refusal.
    assert not sop.evaluate_trace(spec, truth, ["check(u=1)", "service"], True, 1)["database_outcome_match"]
    with pytest.raises(ValueError):
        sop.Rule("single", "x", ())


def test_finance_search_read_and_submission_are_independently_cutoff_guarded():
    store = fh.PointInTimeStore([fh.Document("a", date(2026, 1, 1), "past"),
        fh.Document("b", date(2026, 1, 2), "cutoff"), fh.Document("c", date(2026, 1, 3), "future"),
        fh.Document("u", None, "unknown")], date(2026, 1, 2))
    assert store.search(["c", "b", "u", "a"]) == ("b", "a")
    store.read("a")
    store.validate_submission(["a"])
    with pytest.raises(ValueError, match="PIT violation"):
        store.read("c")
    with pytest.raises(ValueError, match="invalidated"):
        store.validate_submission(["a"])
    with pytest.raises(ValueError):
        fh.PointInTimeStore([fh.Document("a", datetime(2026, 1, 1), "x")], date(2026, 1, 2))


def test_finance_question_equal_rubric_normalization_complete_grades_and_leakage():
    rubrics = {"a": [fh.PrivateCriterion("1", "pre_cutoff")],
               "b": [fh.PrivateCriterion(str(i), "post_cutoff") for i in range(3)]}
    grades = {"a": {"1": 4}, "b": {str(i): 0 for i in range(3)}}
    assert fh.outcome_score(rubrics, grades) == .5  # Pooled-item mean would be .25.
    assert fh.outcome_score(rubrics, grades, kind="pre_cutoff") == 1.
    with pytest.raises(ValueError, match="invalidates"):
        fh.outcome_score(rubrics, grades, invalidated_runs=["a"])
    for invalid in ({"a": {"1": True}, "b": grades["b"]}, {"a": {"1": 5}, "b": grades["b"]}, {"a": grades["a"]}):
        with pytest.raises(ValueError):
            fh.outcome_score(rubrics, invalid)


@pytest.mark.parametrize("module", [sop, fh])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_pure_protocol_diagnostics_are_not_capability_results(module, seed):
    row = module.diagnostic(seed)
    assert all(row["checks"].values()) and row["metrics"]["model_calls"] == 0
    with pytest.raises(ValueError, match="CPU"):
        module.diagnostic(seed, device="cuda")
