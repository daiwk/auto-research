"""CPU mechanism contracts; fixtures are not model capability benchmarks."""
from dataclasses import replace
import math

import numpy as np
import pytest

from auto_research.agent_research import gacc_bench as gacc
from auto_research.agent_research import leash
from auto_research.agent_research import probe_audit as probe
from auto_research.agent_research import rsi_flow as rsi
from auto_research.agent_research import terminal_rsi as terminal


def test_rsi_frozen_parent_failed_attempt_and_report_isolation():
    seen, scored = [], []
    state = rsi.TaskState({"weight": 0}, {"version": 0}, {"format": 0})
    train = [[rsi.Task("train-a", {"x": 1})]]
    report = [rsi.Task("report-b", {"x": 2})]

    def propose(parent, tasks, baseline, skills):
        seen.append(parent.fingerprint())
        parent.model["weight"] += 1
        if len(seen) == 1:
            parent.harness["version"] += 1  # Invalid declared scope, retained failure.
        return parent

    def evaluator(candidate, tasks, split):
        scored.append((split, tuple(t.task_id for t in tasks)))
        return {t.task_id: candidate.model["weight"] for t in tasks}

    result = rsi.evolve(state, train, report, selector=lambda a, s, c: "model",
                        proposers={c: propose for c in rsi.COMPONENTS}, evaluator=evaluator)
    assert seen[0] == seen[1] == state.fingerprint()
    assert state.model["weight"] == 0 and result.state.model["weight"] == 1
    assert not result.attempts[0].valid and result.attempts[1].accepted
    assert len(result.skills) == 2 and result.skills[0]["accepted"] is False
    assert scored[-1] == ("reporting", ("report-b",))
    assert all(split == "training" for split, _ in scored[:-1])


@pytest.mark.parametrize("report", [rsi.Task("x", {"n": 2}), rsi.Task("y", {"n": 1})])
def test_rsi_rejects_identifier_or_payload_overlap(report):
    with pytest.raises(ValueError, match="disjoint"):
        rsi.evolve(rsi.TaskState(0, 0, 0), [[rsi.Task("x", {"n": 1})]], [report],
                   selector=lambda *a: "model", proposers={c: None for c in rsi.COMPONENTS},
                   evaluator=lambda *a: {})


def test_rsi_failed_evaluator_cannot_drop_denominator():
    state = rsi.TaskState(0, 0, 0)
    def evaluate(candidate, tasks, split):
        return {} if candidate.model else {t.task_id: 0. for t in tasks}
    result = rsi.evolve(state, [[rsi.Task("a", 1)]], [rsi.Task("b", 2)],
                        selector=lambda *a: "model",
                        proposers={c: lambda p, *a: replace(p, model=1) for c in rsi.COMPONENTS},
                        evaluator=evaluate)
    assert len(result.attempts) == 2 and all(not a.valid for a in result.attempts)
    assert result.state == state


def test_rsi_failure_memory_does_not_forward_private_exception_text():
    state = rsi.TaskState(0, 0, 0)
    def proposer(parent, *args):
        raise RuntimeError("PRIVATE_GOLD_MUST_NOT_LEAK")
    result = rsi.evolve(state, [[rsi.Task("a", 1)]], [rsi.Task("b", 2)],
        selector=lambda *a: "model", proposers={c: proposer for c in rsi.COMPONENTS},
        evaluator=lambda s, ts, split: {t.task_id: 0. for t in ts})
    assert len(result.attempts) == 2
    assert "PRIVATE_GOLD" not in str(result.attempts)


def test_terminal_skip_observations_chunk_continuation_and_negative_control():
    rewards = [0., 0., 0., 0., 1.]
    values = [.1, 999., .3, 999., .5]
    turns = [0, 0, 0, 1, 1]
    generated = [True, False, True, False, True]
    done = [False, False, False, False, True]
    full = terminal.tb_gae(rewards, values, turns, generated, done, gamma_turn=.9, lambda_turn=.8)
    short = terminal.tb_gae([0., 0., 1.], [.1, .3, .5], [0, 0, 1], [True] * 3,
                            [False, False, True], gamma_turn=.9, lambda_turn=.8)
    np.testing.assert_allclose(full.advantages[full.generated_indices], short.advantages)
    carry = terminal.Continuation(.5, float(full.advantages[4]), 1)
    prefix = terminal.tb_gae(rewards[:3], values[:3], turns[:3], generated[:3], done[:3],
                             gamma_turn=.9, lambda_turn=.8, continuation=carry)
    np.testing.assert_allclose(prefix.advantages, full.advantages[:3])
    wrong = terminal.tb_gae(rewards[:3], values[:3], turns[:3], generated[:3], done[:3],
                            gamma_turn=.9, lambda_turn=.8,
                            continuation=terminal.Continuation(.5, 0., 1))
    assert abs(wrong.advantages[0] - full.advantages[0]) > .1


def test_terminal_unit_clocks_and_reward_multiplicity():
    result = terminal.tb_gae([0., 0., 2.], [.4, .5, .8], [0, 1, 2], [True] * 3,
                             [False, False, True], gamma_turn=1., lambda_turn=1.)
    np.testing.assert_allclose(result.advantages, [1.6, 1.5, 1.2])
    with pytest.raises(ValueError, match="cutoff"):
        terminal.tb_gae([0.], [0.], [0], [True], [False])
    with pytest.raises(ValueError, match="observations"):
        terminal.tb_gae([1., 0.], [0., 0.], [0, 0], [False, True], [False, True])


def test_frozen_rewards_preserve_failure_vs_strict_success():
    div = terminal.calibrate_family_divisors({"f": [1, 2, 3, 10]})
    assert div.for_family("unknown") == 82.
    with pytest.raises(TypeError):
        div.values["f"] = 3
    assert terminal.reward(20, False, "f", div, kind="fdr") > 1
    assert terminal.reward(1e300, False, "f", div) < 1
    assert terminal.reward(0, True, "f", div) == 1
    assert terminal.reward(100, False, "f", div, report_valid=False) == 0
    with pytest.raises(ValueError):
        terminal.calibrate_family_divisors({"f": [1]}, split="test")


def test_lda_matches_independent_quadratic_distances_and_heldout_transform():
    x = np.array([[-2., 2.], [-1., 1.], [1., -1.], [2., -2.]])
    model = leash.fit_lda(x, [0, 0, 1, 1], ridge=.2)
    query = np.array([[0., 0.], [-3., 3.]])
    z = (query - model.mean) / model.scale
    expected = [float((v-model.pass_mean) @ model.precision @ (v-model.pass_mean)
                      - (v-model.fail_mean) @ model.precision @ (v-model.fail_mean)) for v in z]
    np.testing.assert_allclose(model.score(query), expected)
    assert model.score(query)[1] > model.score(query)[0]
    np.testing.assert_allclose(model.mean, [0., 0.])


def test_leash_grouped_oof_and_disjoint_reference():
    rng = np.random.default_rng(42)
    ids = [f"task-{i}" for i in range(12) for _ in range(2)]
    y = np.tile([0, 1], 12)
    x = rng.normal(size=(24, 3)) + y[:, None]
    result = leash.crossfit_reference(x, y, ids, folds=4)
    assert len(result.scores) == 24 and math.isfinite(result.oof_auroc)
    for task, fold in result.task_folds.items():
        assert task not in result.fold_training_tasks[fold]
    with pytest.raises(ValueError, match="disjoint"):
        leash.crossfit_reference(x, y, ids, folds=4, excluded_task_ids=[ids[0]])
    with pytest.raises(ValueError):
        leash.crossfit_reference(x, y, ids, folds=4, split="test")


def test_leash_task_max_budget_and_tied_scores():
    calibration = leash.calibrate_escalation([1., 2., 3., 4.],
        [[0., 9.], [1., 1.], [3., 2.], [4., 0.]], initial_target=.25, overall_target=.5)
    assert calibration.initial_routed == 1 and calibration.overall_routed == 2
    tied = leash.calibrate_escalation([1.] * 4, [[2.] * 8] * 4)
    assert tied.overall_routed == 0
    with pytest.raises(ValueError):
        leash.calibrate_escalation([1.], [[1.]], split="test")
    assert leash.calibrate_shadow([0., 1., 2.]) == pytest.approx(1.8)
    with pytest.raises(ValueError):
        leash.calibrate_shadow([1., 2.], split="test")


@pytest.mark.parametrize("changed,limit", [(True, 2), (False, 6)])
def test_shadow_never_executes_probe_and_respects_limits(changed, limit):
    shadow = leash.ShadowOversight(1.)
    invoked = []
    for step in range(1, 60):
        shadow.monitor(step, probe_score=lambda: 2.,
                       intervene=lambda: invoked.append("strong-reflection") or changed)
    assert len(invoked) == shadow.interventions == limit
    assert shadow.probes == limit


def test_shadow_schedule_starts_on_first_post_handoff_strong_step():
    shadow = leash.ShadowOversight(1.)
    probed_steps = []
    for step in range(1, 12):
        shadow.monitor(step, probe_score=lambda: probed_steps.append(step) or 0.,
                       intervene=lambda: False)
    assert probed_steps == [1, 4, 7, 10]
    assert shadow.interventions == 0


def _policies():
    return probe.example_verifiers(required_fields={"search_flights": ["origin", "destination"]},
                                   restricted_destinations=["ZZZ"])


def test_probe_verifiers_dedup_and_complete_denominators():
    trace = [probe.Turn("find", "ok", (probe.ToolCall("search_flights", {"destination": "AAA"}, {}),))] * 3
    policies = _policies()
    events = probe.deterministic_rescore(trace, policies)
    reward = probe.violation_reward(events, policies)
    assert reward["per_turn"] == [1., .5, 0.]
    summary = probe.audit_metrics([events, [()]],
        declared_policy_ids=[p.policy_id for p in policies] + ["semantic-not-implemented"],
        implemented_policy_ids=[p.policy_id for p in policies])
    assert summary["policy_coverage"] == .2
    assert summary["episodes_without_verified_hits"] == 1
    assert summary["unsupported_policies"] == ["semantic-not-implemented"]
    assert summary["verifier_hits"] == 3
    assert summary["violation_yield_per_100_episodes"] == 150.
    assert summary["distinct_episode_policy_yield_per_100_episodes"] == 50.


def test_probe_raw_yield_keeps_repeated_verifier_hits():
    summary = probe.audit_metrics([[("same-policy",)] * 3],
        declared_policy_ids=["same-policy"], implemented_policy_ids=["same-policy"])
    assert summary["violation_yield_per_100_episodes"] == 300.
    assert summary["distinct_episode_policy_hits"] == 1
    assert summary["distinct_episode_policy_yield_per_100_episodes"] == 100.


def test_probe_private_evaluator_never_passed_to_auditor_or_target():
    observed = []
    def auditor(scenario, history):
        assert not hasattr(scenario, "policies") and not hasattr(scenario, "gold")
        assert all(len(turn) == 2 for turn in history)
        observed.append(history)
        return "Find a flight"
    def target(history):
        assert history[-1] == ("user", "Find a flight")
        return probe.Turn(history[-1][1], "Need an origin")
    result = probe.audit_episode(probe.PublicAuditScenario("p1", "travel"), auditor=auditor,
        target=target, private_evaluator=lambda trace: {"private-secret": 13}, max_turns=2)
    assert len(observed) == 2 and result["private_evaluation"] == {"private-secret": 13}
    assert all("private-secret" not in str(history) for history in observed)


def test_probe_consent_cannot_be_reused_for_another_mutation_intent():
    call = probe.ToolCall("book_flight", {"destination": "AAA"}, {})
    trace = [probe.Turn("yes", "done", (call,), user_confirmed_mutation=True),
             probe.Turn("another trip", "done", (call,))]
    events = probe.deterministic_rescore(trace, _policies())
    assert "confirmation" not in events[0] and "confirmation" in events[1]


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -1.])
def test_nonfinite_or_negative_reward_rejected(bad):
    with pytest.raises(ValueError):
        terminal.reward(bad, True, "f", terminal.FamilyDivisors({"f": 1.}))


@pytest.mark.parametrize("bad", [float("nan"), 0., -1.])
def test_invalid_lda_ridge_rejected(bad):
    with pytest.raises(ValueError):
        leash.fit_lda([[1.], [2.]], [0, 1], ridge=bad)


def _codec():
    return gacc.TokenCodec("fixture-codepoint-ids", "v1", lambda s: list(map(ord, s)),
                           lambda t: "".join(map(chr, t)))


def test_gacc_withheld_questions_cache_budget_and_all_question_macro():
    cases = [gacc.GoalCase("ctx", "goal", "abcdef", "keep-a", (
        gacc.Question("q1", "first", "a"), gacc.Question("q2", "last", "f")))]
    seen, cache = [], {}
    def compress(value):
        assert set(value.__dataclass_fields__) == {"context", "goal", "token_budget"}
        seen.append(value)
        return value.context
    def read(value):
        assert not hasattr(value, "reference_answer")
        return value.memory[0] if value.question == "first" else value.memory[-1]
    kwargs = dict(compressor=compress, reader=read,
                  judge=lambda x: x.candidate_answer == x.reference_answer,
                  codec=_codec(), retention_ratio=.5, compressor_revision="fixture-v1",
                  reader_revision="fixed-v1", judge_revision="fixed-v1", cache=cache)
    result = gacc.evaluate(cases, **kwargs)
    repeated = gacc.evaluate(cases, **kwargs)
    assert len(seen) == 1 and repeated["compressions"] == 0
    assert result["micro_accuracy"] == .5 and result["macro_all_question_success"] == 0
    assert result["rows"][0]["retained_tokens"] == 3
    assert result["tokenizer"]["identity_verified"] is False
    gacc.evaluate(cases, **(kwargs | {"compressor_revision": "different-model"}))
    assert len(seen) == 2


def test_gacc_rejects_duplicate_goals_and_roundtrip_over_budget():
    case = gacc.GoalCase("c", "g", "abc", "x", (gacc.Question("q", "x", "y"),))
    kwargs = dict(compressor=lambda x: "abc", reader=lambda x: "y", judge=lambda x: True,
                  codec=_codec(), retention_ratio=.1, compressor_revision="c",
                  reader_revision="r", judge_revision="j")
    with pytest.raises(ValueError, match="unique"):
        gacc.evaluate([case, case], **kwargs)
    bad_codec = gacc.TokenCodec("bad", "v1", lambda s: list(map(ord, s)), lambda _: "abcdef")
    with pytest.raises(ValueError, match="round trip"):
        gacc.evaluate([case], **(kwargs | {"codec": bad_codec}))


def test_gacc_shorter_memory_is_not_padded_and_name_is_not_verification():
    case = gacc.GoalCase("c", "g", "abcdefgh", "x", (gacc.Question("q", "x", "a"),))
    codec = _codec()
    declared = gacc.TokenCodec("cl100k_base", "arbitrary-fixture", codec.encode, codec.decode)
    result = gacc.evaluate([case], compressor=lambda x: "a", reader=lambda x: x.memory,
        judge=lambda x: x.candidate_answer == x.reference_answer, codec=declared,
        retention_ratio=.5, compressor_revision="c", reader_revision="r", judge_revision="j")
    row = result["rows"][0]
    assert row["retained_tokens"] == 1 and row["unused_token_budget"] == 3
    assert row["padding_tokens"] == 0 and row["memory_tokens_reencoded"] == 1
    assert result["tokenizer"]["name"] == "cl100k_base"
    assert result["tokenizer"]["identity_verified"] is False


@pytest.mark.parametrize("ratio", [0., .1])
def test_gacc_strict_floor_zero_budget_keeps_empty_memory(ratio):
    case = gacc.GoalCase("c", "g", "abc", "x", (gacc.Question("q", "x", ""),))
    observed = []
    def compress(value):
        observed.append(value.token_budget)
        return value.context
    result = gacc.evaluate([case], compressor=compress, reader=lambda x: x.memory,
        judge=lambda x: x.candidate_answer == x.reference_answer, codec=_codec(),
        retention_ratio=ratio, compressor_revision="c", reader_revision="r", judge_revision="j")
    row = result["rows"][0]
    assert observed == [0] and row["token_budget"] == 0
    assert row["retained_tokens"] == row["padding_tokens"] == row["memory_tokens_reencoded"] == 0
    assert result["micro_accuracy"] == 1.
