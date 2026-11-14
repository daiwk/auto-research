"""EnvHarness wrapper semantics on transitions; not an Agent benchmark."""
import pytest

from auto_research.agent_research.envharness import (
    Blocked, ContractWrapper, Response, SerialChain, StageWrapper, diagnostic,
)


class Fixture:
    def __init__(self, goal=2, verdict=None):
        self.goal, self.verdict = goal, verdict
        self.resets = self.steps_total = self.evaluations = 0

    def reset(self, seed):
        self.resets += 1
        self.position = self.budget_used = 0
        return Response(self.observe())

    def observe(self):
        return str(self.position)

    def step(self, action):
        self.steps_total += 1
        self.budget_used += 1
        self.position += action == "advance"
        return Response(self.observe(), self.position >= self.goal)

    def evaluate(self):
        self.evaluations += 1
        return self.position >= self.goal if self.verdict is None else self.verdict

    def notify_replay_complete(self):
        self.budget_used = 0


def test_stage_replays_ordinary_actions_and_rewinds_only_counters():
    env = Fixture(3)
    stage = StageWrapper(env, ["advance", "advance"])
    assert stage.reset(42) == Response("2")
    assert env.position == 2 and env.steps_total == 2 and env.budget_used == 0
    assert stage.step("advance") == Response("3", True)
    assert stage.evaluate() is True
    assert env.budget_used == 1
    assert stage.reset(42) == Response("2")


def test_contract_block_reobserves_filters_without_stepping_or_verifying():
    env = Fixture()
    contract = ContractWrapper(env, filter_action=lambda action, state: Blocked("no") if action == "bad" else action,
                               filter_observation=lambda observation: "visible=" + observation)
    assert contract.reset(42) == Response("visible=0")
    blocked = contract.step("bad")
    assert blocked == Response("visible=0\nBlocked: no")
    assert env.steps_total == env.evaluations == 0
    assert contract.step("advance") == Response("visible=1")
    assert contract.step("advance") == Response("visible=2", True)
    assert contract.evaluate() is True and env.evaluations == 1


def test_hook_order_action_transition_observation_and_unchanged_verifier():
    env = Fixture(1, verdict=False)
    seen = []

    def rewrite(action, state):
        seen.append(("action", action, state))
        return "advance"

    def transition(action, response):
        seen.append(("transition", action, response.observation))
        return Response("changed", response.terminated)

    contract = ContractWrapper(env, filter_action=rewrite, modify_transition=transition,
                               filter_observation=lambda observation: observation.upper())
    contract.reset(42)
    assert contract.step("other") == Response("CHANGED", True)
    assert seen == [("action", "other", "0"), ("transition", "advance", "1")]
    assert contract.evaluate() is False


def test_chain_lazy_handoff_shared_budget_and_cached_conjunction():
    a, b = Fixture(1), Fixture(2)
    chain = SerialChain(a, b, step_budget=3)
    chain.reset(42)
    assert b.resets == 0 and not chain.evaluate()
    first = chain.step("advance")
    assert first == Response("1\n--- Next task ---\n0", False)
    assert b.resets == 1 and a.evaluations == 1
    assert chain.step("advance").terminated is False
    assert chain.step("advance").terminated is True
    assert chain.evaluate() is True and chain.evaluate() is True
    assert a.evaluations == b.evaluations == 1
    with pytest.raises(ValueError, match="terminated"):
        chain.step("advance")


def test_first_verifier_failure_does_not_start_second_or_claim_success():
    a, b = Fixture(1, verdict=False), Fixture(1)
    chain = SerialChain(a, b, step_budget=5)
    chain.reset(42)
    assert chain.step("advance").terminated is True
    assert not chain.evaluate() and b.resets == b.evaluations == 0


def test_budget_before_handoff_and_partial_second_do_not_get_gold_verifier():
    a, b = Fixture(1), Fixture(1)
    chain = SerialChain(a, b, step_budget=1)
    chain.reset(42)
    assert chain.step("advance").terminated and not chain.evaluate()
    assert a.evaluations == 1 and b.resets == b.evaluations == 0
    a, b = Fixture(1), Fixture(3)
    chain = SerialChain(a, b, step_budget=2)
    chain.reset(42)
    chain.step("advance")
    assert chain.step("advance").terminated and not chain.evaluate()
    assert b.resets == 1 and b.evaluations == 0


def test_wrapper_order_is_not_commutative():
    blocked_stage = ContractWrapper(StageWrapper(Fixture(5), ["advance"]),
                                   filter_action=lambda action, state: Blocked("no"))
    assert blocked_stage.reset(42).observation == "1"
    inside = ContractWrapper(Fixture(5), filter_action=lambda action, state: Blocked("no"))
    assert StageWrapper(inside, ["advance"]).reset(42).observation == "0"


@pytest.mark.parametrize("value", [True, 0, -1, 1.5, None])
def test_bad_shared_budgets_rejected(value):
    with pytest.raises(ValueError):
        SerialChain(Fixture(), Fixture(), step_budget=value)


def test_malformed_hook_or_verifier_output_does_not_become_success():
    env = Fixture(1, verdict=1)
    chain = SerialChain(env, Fixture(), step_budget=2)
    chain.reset(42)
    with pytest.raises(ValueError, match="boolean"):
        chain.step("advance")
    with pytest.raises(ValueError, match="reset"):
        chain.evaluate()
    contract = ContractWrapper(Fixture(), modify_transition=lambda action, response: {})
    contract.reset(42)
    with pytest.raises(ValueError, match="Response"):
        contract.step("advance")
    with pytest.raises(ValueError, match="reset"):
        contract.step("advance")


def test_terminal_latch_cannot_be_revived_by_blocked_action_or_transition_hook():
    env = Fixture(1)
    contract = ContractWrapper(env, filter_action=lambda action, state: Blocked("no") if action == "bad" else action,
                               modify_transition=lambda action, response: Response(response.observation, False))
    contract.reset(42)
    assert contract.step("advance").terminated is True
    with pytest.raises(ValueError, match="terminated"):
        contract.step("bad")
    assert env.steps_total == 1


def test_stage_replay_never_steps_past_terminal_and_requires_reset_after_error():
    env = Fixture(1)
    stage = StageWrapper(env, ["advance", "advance"])
    with pytest.raises(ValueError, match="terminated"):
        stage.reset(42)
    assert env.steps_total == 1
    with pytest.raises(ValueError, match="reset"):
        stage.step("advance")
    with pytest.raises(ValueError, match="nonterminal"):
        StageWrapper(Fixture(1), ["advance"]).reset(42)


@pytest.mark.parametrize("failure", ["step", "response", "verifier", "second-reset"])
def test_external_failures_poison_chain_and_cannot_be_retried_into_success(failure):
    a, b = Fixture(1), Fixture(1)
    chain = SerialChain(a, b, step_budget=4)
    chain.reset(42)

    def broken_step(action):
        a.steps_total += 1
        raise RuntimeError("external side effect then failure")

    if failure == "step":
        a.step = broken_step
    elif failure == "response":
        a.step = lambda action: {}
    elif failure == "verifier":
        a.verdict = 1
    else:
        b.reset = lambda seed: {}
    with pytest.raises((RuntimeError, ValueError)):
        chain.step("advance")
    assert chain._steps == 1
    before = (a.steps_total, a.evaluations, b.resets, b.evaluations)
    for callback in (lambda: chain.step("advance"), chain.evaluate, chain.observe, chain.notify_replay_complete):
        with pytest.raises(ValueError, match="reset"):
            callback()
    assert (a.steps_total, a.evaluations, b.resets, b.evaluations) == before


def test_interaction_requires_reset_and_invalid_replay_not_accepted():
    chain = SerialChain(Fixture(), Fixture(), step_budget=2)
    for call in (chain.observe, chain.evaluate, lambda: chain.step("advance")):
        with pytest.raises(ValueError, match="reset"):
            call()
    with pytest.raises(ValueError):
        StageWrapper(Fixture(), "advance")


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_only_cpu(seed):
    row = diagnostic(seed)
    assert all(row["checks"].values())
    assert row["diagnostic_only"] is True and row["evaluation_tier"] == "l1_mechanism"
    with pytest.raises(ValueError, match="CPU"):
        diagnostic(seed, "cuda")
