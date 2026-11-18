"""Finite mechanism and negative controls, not model/capability evaluation."""
from copy import deepcopy

import pytest

from auto_research.agent_research import agent_gym as gym
from auto_research.agent_research import bats


@pytest.mark.parametrize("seed", [42, 43, 44])
@pytest.mark.parametrize("module", [bats, gym])
def test_actual_diagnostics_and_cpu_boundary(module, seed):
    result = module.diagnostic(seed)
    assert result["seed"] == seed
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(result["checks"].values())
    with pytest.raises(ValueError):
        module.diagnostic(seed, "cuda")


def test_budget_stops_at_any_exhausted_tool_and_rejects_overrun():
    tracker = bats.BudgetTracker({"search": 1, "browse": 9})
    tracker.record_call("search")
    assert not tracker.active
    assert tracker.snapshot()["browse"]["remaining"] == 9
    with pytest.raises(ValueError):
        tracker.record_call("browse")
    assert tracker.used == {"search": 1, "browse": 0}
    assert not bats.BudgetTracker({"search": 0}).active


@pytest.mark.parametrize("value", [-1, True, 1.1])
def test_budget_rejects_invalid_counts(value):
    with pytest.raises(ValueError):
        bats.BudgetTracker({"search": value})


def test_budget_update_is_atomic_and_unknown_tool_not_free():
    tracker = bats.BudgetTracker({"search": 2})
    for tool, count in [("browse", 1), ("search", 3), ("search", 0)]:
        with pytest.raises(ValueError):
            tracker.record_call(tool, count)
    assert tracker.used == {"search": 0}
    snapshot = tracker.snapshot()
    snapshot["search"]["used"] = 99
    assert tracker.used["search"] == 0


def test_cost_prices_and_cache_semantics_are_explicit():
    value = bats.unified_cost(bats.TokenUsage(100, 20, 40), {"search": 2},
                             input_price=.002, output_price=.004, cache_price=.0005,
                             tool_prices={"search": .01})
    assert value == pytest.approx(.24)
    with pytest.raises(ValueError):
        bats.TokenUsage(3, 1, 4)
    with pytest.raises(ValueError):
        bats.unified_cost(bats.TokenUsage(1, 1), {"unpriced": 1},
                          input_price=0, output_price=0, cache_price=0, tool_prices={})
    with pytest.raises(ValueError):
        bats.unified_cost(bats.TokenUsage(1, 1), {}, input_price=float("nan"),
                          output_price=0, cache_price=0, tool_prices={})


def test_pivot_clears_raw_history_but_not_usage_or_summaries():
    state = bats.BATSState("public", bats.BudgetTracker({"search": 5}))
    state.tool_observation("search", "failed first direction")
    state.apply_external_verdict("candidate", bats.Verdict.PIVOT, summary="external summary")
    assert state.trajectory == [] and state.summaries == ["external summary"]
    assert state.tracker.used["search"] == 1 and state.attempt == 1
    assert not state.verified_answers
    state.tracker.record_call("search", 4)
    assert state.final_answer() == "candidate"


def test_success_uses_external_selector_not_gold_correctness():
    state = bats.BATSState("public question", bats.BudgetTracker({"search": 4}))
    state.apply_external_verdict("first", bats.Verdict.SUCCESS, summary="externally accepted")
    state.apply_external_verdict("second", bats.Verdict.SUCCESS, summary="another acceptance")
    assert state.attempt == 2
    with pytest.raises(ValueError):
        state.final_answer(lambda answers: answers[0])
    state.tracker.record_call("search", 4)
    with pytest.raises(ValueError):
        state.final_answer()
    assert state.final_answer(lambda answers: answers[1]) == "second"
    with pytest.raises(ValueError):
        state.final_answer(lambda answers: "gold-shaped answer outside candidates")
    assert not ({"gold", "answer", "verified_answers"} & set(state.actor_payload()))


def test_continue_keeps_attempt_and_conditional_compression():
    state = bats.BATSState("public", bats.BudgetTracker({"search": 3}))
    state.tool_observation("search", "public")
    state.apply_external_verdict("one", bats.Verdict.CONTINUE)
    assert state.trajectory == ["public"] and state.attempt == 0
    state.apply_external_verdict("two", bats.Verdict.CONTINUE, compress_history=True, summary="external compressed")
    assert not state.trajectory and state.attempt == 0
    with pytest.raises(ValueError):
        state.apply_external_verdict("three", "SUCCESS", summary="not enum")
    with pytest.raises(ValueError):
        state.apply_external_verdict("three", bats.Verdict.PIVOT)


def rule(identity="r", scope="scope", priority=10, actions=None, conditions=None):
    return gym.Rule(identity, scope, priority, conditions or (gym.Condition("amount", "less_than", 2000),),
                    actions or (gym.Action(1, edits=(("status", "approved"),)),))


def approved(candidate):
    impact = gym.assess_impact(candidate, {"target": {"amount": 1000}}, "target")
    return gym.admit(candidate, impact, approver="external human", approve=True)


def test_impact_target_and_collateral_need_explicit_approval():
    candidate = rule()
    cases = {"target": {"amount": 1000}, "collateral": {"amount": 500}, "safe": {"amount": 3000}}
    impact = gym.assess_impact(candidate, cases, "target")
    assert impact.target_matched and impact.collateral_ids == ("collateral",)
    for kwargs in [{"approver": None, "approve": True}, {"approver": "human", "approve": False},
                   {"approver": "human", "approve": True}]:
        with pytest.raises(ValueError):
            gym.admit(candidate, impact, **kwargs)
    accepted = gym.admit(candidate, impact, approver="human", approve=True, acknowledge_collateral=True)
    assert accepted.approved_digest == candidate.digest
    with pytest.raises(ValueError):
        gym.assess_impact(candidate, cases, "target", split="test")


def test_changed_rule_cannot_reuse_old_assessment():
    first = rule()
    impact = gym.assess_impact(first, {"target": {"amount": 1000}}, "target")
    changed = rule(actions=(gym.Action(1, edits=(("status", "changed"),)),))
    with pytest.raises(ValueError):
        gym.admit(changed, impact, approver="human", approve=True)


def test_target_must_match_even_with_human_flag():
    candidate = rule()
    impact = gym.assess_impact(candidate, {"target": {"amount": 4000}}, "target")
    with pytest.raises(ValueError):
        gym.admit(candidate, impact, approver="human", approve=True)


def test_conditions_are_and_joined_and_dynamic_reference_is_public_context():
    candidate = rule(conditions=(gym.Condition("name", "equals", "_DYNAMIC_extracted.name_"),
                                gym.Condition("amount", "less_than", 2000)))
    assert candidate.matches({"name": " Acme ", "extracted": {"name": "acme"}, "amount": 1000})
    assert not candidate.matches({"name": "other", "extracted": {"name": "acme"}, "amount": 1000})
    assert not candidate.matches({"name": "acme", "extracted": {"name": "acme"}, "amount": 3000})
    with pytest.raises(ValueError):
        gym.Condition("amount", "invented_operator", 1)


def test_scope_mutex_and_priority_not_input_order():
    first = rule("first", priority=1, actions=(gym.Action(1, edits=(("status", "first"),)),))
    second = rule("second", priority=2, actions=(gym.Action(1, edits=(("status", "second"),)),))
    result = gym.execute({"status": "old"}, {"amount": 1}, (approved(second), approved(first)))
    assert result["output"] == {"status": "first"}
    assert [t["selected"] for t in result["trace"]] == [True, False]


def test_tier_merging_executes_real_continuation_then_patch_then_edit():
    rules = [rule("c1", "c1", actions=(gym.Action(3, resume_from="phase4", context="late"),)),
             rule("c2", "c2", actions=(gym.Action(3, resume_from="phase2", context="early"),)),
             rule("p1", "p1", actions=(gym.Action(2, target_fields=("status",)),)),
             rule("p2", "p2", actions=(gym.Action(2, target_fields=("status", "steps")),)),
             rule("e", "e", actions=(gym.Action(1, edits=(("status", "final"),)),))]
    calls = []
    def continuation(before, start, contexts):
        calls.append(("continue", start, contexts))
        return {"status": "continued", "steps": 3}
    def patcher(before, fields, contexts):
        calls.append(("patch", before["status"], fields))
        return {"status": "patched", "steps": 4}
    original = {"status": "old", "steps": 0}
    result = gym.execute(original, {"amount": 1}, tuple(approved(r) for r in rules),
                         continuation=continuation, patcher=patcher)
    assert result["execution_order"] == [3, 2, 1]
    assert calls[0][1] == "phase2" and calls[1][1] == "continued"
    assert calls[1][2] == ("status", "steps")
    assert result["external_callback_calls"] == 2 and result["output"] == {"status": "final", "steps": 4}
    assert original == {"status": "old", "steps": 0}


def test_no_callback_is_not_silently_reported_success():
    patch = approved(rule(actions=(gym.Action(2, target_fields=("status",)),)))
    with pytest.raises(ValueError):
        gym.execute({"status": "old"}, {"amount": 1}, (patch,))
    with pytest.raises(ValueError):
        gym.execute({"status": "old"}, {"amount": 1}, (patch,), patcher=lambda *args: {"extra": "bad"})


def test_typed_edit_rejects_schema_changes_and_preserves_caller_on_failure():
    original = {"status": "old"}
    for edits in [(("status", 1),), (("absent", "new"),)]:
        candidate = approved(rule(actions=(gym.Action(1, edits=edits),)))
        with pytest.raises(ValueError):
            gym.execute(original, {"amount": 1}, (candidate,))
        assert original == {"status": "old"}


def test_duplicate_priorities_and_stale_approval_fail():
    one = approved(rule("one"))
    two = approved(rule("two"))
    with pytest.raises(ValueError):
        gym.execute({"status": "old"}, {"amount": 1}, (one, two))
    stale = gym.ApprovedRule(one.rule, "human", "0" * 64)
    with pytest.raises(ValueError):
        gym.execute({"status": "old"}, {"amount": 1}, (stale,))


def test_runtime_context_and_external_results_do_not_share_gold_channel():
    public = {"amount": 1}
    before = deepcopy(public)
    result = gym.execute({"status": "old"}, public, (approved(rule()),))
    assert public == before
    assert result["semantic_correctness_verified"] is False
