"""EnvHarness v1 Stage/Contract/serial Chain control components.

Trusted environment verifiers remain external. There is no EnvRigger model,
generated-code compiler, subprocess sandbox, RL learner or benchmark bridge.
The callable hooks below run in the caller's process and must be trusted.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import random
from typing import Protocol

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Response:
    observation: str
    terminated: bool = False

    def __post_init__(self):
        if not isinstance(self.observation, str) or type(self.terminated) is not bool:
            raise ValueError("string observation and explicit termination boolean required")


@dataclass(frozen=True)
class Blocked:
    reason: str

    def __post_init__(self):
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("explicit blocked-action reason required")


class Environment(Protocol):
    def reset(self, seed: int) -> Response: ...
    def step(self, action: str) -> Response: ...
    def observe(self) -> str: ...
    def evaluate(self) -> bool: ...
    def notify_replay_complete(self) -> None: ...


def _response(value):
    if not isinstance(value, Response):
        raise ValueError("environment or hook must return a typed Response")
    return value


def _action(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("nonempty action string required")
    return value


def _verdict(env):
    value = env.evaluate()
    if type(value) is not bool:
        raise ValueError("external verifier must return an explicit boolean")
    return value


class Wrapper:
    def __init__(self, inner: Environment):
        self.inner = inner
        self._started = False
        self._done = self._failed = False

    def _guard(self, *, active=False):
        if not self._started or self._failed:
            raise ValueError("reset required before interaction or after a failed callback")
        if active and self._done:
            raise ValueError("wrapped episode has terminated")

    def _poison(self):
        self._failed = self._done = True

    def reset(self, seed: int) -> Response:
        self._started = self._done = self._failed = False
        try:
            if type(seed) is not int:
                raise ValueError("integer seed required")
            response = _response(self.inner.reset(seed))
            self._started, self._done = True, response.terminated
            return response
        except Exception:
            self._poison()
            raise

    def step(self, action: str) -> Response:
        self._guard(active=True)
        try:
            response = _response(self.inner.step(_action(action)))
            self._done = response.terminated
            return response
        except Exception:
            self._poison()
            raise

    def observe(self) -> str:
        self._guard()
        value = self.inner.observe()
        if not isinstance(value, str):
            raise ValueError("observation must be a string")
        return value

    def evaluate(self) -> bool:
        self._guard()
        return _verdict(self.inner)

    def notify_replay_complete(self) -> None:
        self._guard(active=True)
        self.inner.notify_replay_complete()


class StageWrapper(Wrapper):
    """Appendix C Setups: reachable-state replay, then rewind episode counters."""

    def __init__(self, inner: Environment, actions: Sequence[str]):
        super().__init__(inner)
        if isinstance(actions, (str, bytes)) or not isinstance(actions, Sequence):
            raise ValueError("explicit replay action sequence required")
        self.actions = tuple(_action(action) for action in actions)

    def reset(self, seed: int) -> Response:
        try:
            result = super().reset(seed)
            for action in self.actions:
                result = super().step(action)
            if result.terminated:
                raise ValueError("prepared initial state must be nonterminal; replay cannot continue past termination")
            self.inner.notify_replay_complete()
            return Response(self.observe())
        except Exception:
            self._poison()
            raise


class ContractWrapper(Wrapper):
    """Appendix C Rules: action/transition/observation hooks, verifier unchanged.

    Blocked actions re-observe and filter the current observation without calling
    inner.step. No hook receives a gold answer, plan or evaluate callback here.
    This signature is a local narrow interface, not the complete upstream ABI.
    """

    def __init__(self, inner: Environment, *,
                 filter_action: Callable[[str, str], str | Blocked] = lambda action, state: action,
                 modify_transition: Callable[[str, Response], Response] = lambda action, response: response,
                 filter_observation: Callable[[str], str] = lambda observation: observation):
        super().__init__(inner)
        if not all(callable(hook) for hook in (filter_action, modify_transition, filter_observation)):
            raise ValueError("trusted callable hooks required")
        self.filter_action = filter_action
        self.modify_transition = modify_transition
        self.filter_observation = filter_observation

    def _filter(self, observation):
        value = self.filter_observation(observation)
        if not isinstance(value, str):
            raise ValueError("observation hook must return a string")
        return value

    def reset(self, seed: int) -> Response:
        try:
            response = super().reset(seed)
            return Response(self._filter(response.observation), response.terminated)
        except Exception:
            self._poison()
            raise

    def observe(self) -> str:
        return self._filter(super().observe())

    def step(self, action: str) -> Response:
        self._guard(active=True)
        try:
            proposed = self.filter_action(_action(action), super().observe())
            if isinstance(proposed, Blocked):
                return Response(self.observe() + "\nBlocked: " + proposed.reason)
            response = super().step(_action(proposed))
            modified = _response(self.modify_transition(proposed, response))
            # Narrow local safety convention: hooks may terminate early but
            # cannot revive an inner environment that has already terminated.
            self._done = response.terminated or modified.terminated
            return Response(self._filter(modified.observation), self._done)
        except Exception:
            self._poison()
            raise


class SerialChain:
    """Serial Link only: lazy B, shared submitted-step budget, cached conjunction.

    Reset B only when A terminates successfully and budget remains. A failure or
    shared-budget exhaustion ends the composite without pretending B succeeded.
    There is no branching, compatibility judgement or shared semantic objective.
    """

    def __init__(self, first: Environment, second: Environment, *, step_budget: int):
        if type(step_budget) is not int or step_budget < 1:
            raise ValueError("positive shared step budget required")
        self.first, self.second, self.step_budget = first, second, step_budget
        self._started = False
        self._failed = False

    def reset(self, seed: int) -> Response:
        if type(seed) is not int:
            raise ValueError("integer seed required")
        self._started = self._failed = False
        self._seed, self._steps, self._leg = seed, 0, 0
        self._outcomes: list[bool | None] = [None, None]
        self._done = False
        # The narrow component requires an active initial task. Completing a
        # benchmark during reset needs an external bridge, not fabricated calls.
        try:
            response = _response(self.first.reset(seed))
            if response.terminated:
                raise ValueError("serial chain requires a nonterminal initial task")
            self._observation = response.observation
            self._started = True
            return response
        except Exception:
            self._failed = self._done = True
            raise

    def _require_started(self):
        if not self._started or self._failed:
            raise ValueError("reset must precede interaction and follow any failed callback")

    def observe(self) -> str:
        self._require_started()
        return self._observation

    def notify_replay_complete(self) -> None:
        self._require_started()
        (self.first if self._leg == 0 else self.second).notify_replay_complete()
        self._steps = 0

    def step(self, action: str) -> Response:
        self._require_started()
        if self._done:
            raise ValueError("composite episode has terminated")
        current = self.first if self._leg == 0 else self.second
        _action(action)
        # Charge submitted interactions even if an external callback then fails.
        self._steps += 1
        try:
            response = _response(current.step(action))
            self._observation = response.observation
            if response.terminated:
                self._outcomes[self._leg] = _verdict(current)
                if self._leg == 0 and self._outcomes[0] and self._steps < self.step_budget:
                    initial = _response(self.second.reset(self._seed))
                    self._leg = 1
                    self._observation += "\n--- Next task ---\n" + initial.observation
                    if initial.terminated:
                        self._outcomes[1], self._done = _verdict(self.second), True
                else:
                    self._done = True
            if self._steps >= self.step_budget:
                self._done = True
            return Response(self._observation, self._done)
        except Exception:
            self._failed = self._done = True
            raise

    def evaluate(self) -> bool:
        self._require_started()
        # Never re-run scorers, never inspect a still-running leg's hidden truth.
        return self._done and self._outcomes == [True, True]


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Deterministic toy transition truth tables; no Agent performance score."""
    if device != "cpu":
        raise ValueError("CPU-only environment wrappers; no CUDA model")
    if type(seed) is not int:
        raise ValueError("integer seed required")

    class Fixture:
        def __init__(self, name, required):
            self.name, self.required = name, required
            self.resets = self.calls = self.evaluations = 0

        def reset(self, fixture_seed):
            self.resets += 1
            self.position = self.steps = 0
            return Response(self.observe())

        def observe(self):
            return f"{self.name}:{self.position}"

        def step(self, action):
            self.calls += 1
            self.steps += 1
            self.position += action == "advance"
            return Response(self.observe(), self.position >= self.required)

        def notify_replay_complete(self):
            self.steps = 0

        def evaluate(self):
            self.evaluations += 1
            return self.position >= self.required

    base = Fixture("stage", 3)
    staged = StageWrapper(base, ["advance"])
    stage_initial = staged.reset(seed)
    stage_ok = stage_initial.observation == "stage:1" and base.steps == 0 and base.calls == 1
    rules = ContractWrapper(staged, filter_action=lambda action, state: Blocked("fixture rule")
                            if action == "blocked" else action,
                            filter_observation=lambda observation: "filtered:" + observation)
    rules.reset(seed)
    before = base.calls
    blocked = rules.step("blocked")
    blocked_ok = base.calls == before and blocked.observation.startswith("filtered:")
    first, second = Fixture("A", 1), Fixture("B", 1)
    chain = SerialChain(first, second, step_budget=3)
    chain.reset(seed)
    lazy = second.resets == 0 and not chain.evaluate()
    middle = chain.step("advance")
    end = chain.step("advance")
    first_evals, second_evals = first.evaluations, second.evaluations
    verdicts = [chain.evaluate() for _ in range(2)]
    # Seed only changes an unused fixture label, not three independent agents.
    failure = Fixture(str(random.Random(seed).randint(0, 999)), 4)
    unstarted = Fixture("unstarted", 1)
    short = SerialChain(failure, unstarted, step_budget=1)
    short.reset(seed)
    exhausted = short.step("advance")
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"stage_replay_actions": len(staged.actions), "chain_agent_steps": chain._steps,
                        "first_verifier_calls": first.evaluations, "second_verifier_calls": second.evaluations,
                        "blocked_inner_steps": base.calls - before},
            "checks": {"reachable_replay_resets_budget": stage_ok,
                       "blocked_action_does_not_mutate_inner": blocked_ok,
                       "lazy_second_environment": lazy,
                       "handoff_masks_first_termination": not middle.terminated and second.resets == 1,
                       "cached_verifier_conjunction": end.terminated and all(verdicts)
                       and (first.evaluations, second.evaluations) == (first_evals, second_evals) == (1, 1),
                       "shared_budget_exhaustion_is_not_success": exhausted.terminated and not short.evaluate()
                       and unstarted.resets == unstarted.evaluations == 0}}
