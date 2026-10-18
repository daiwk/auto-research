"""SKILL.state's explicit state loop (2608.26263v3, Algorithm 1).

Only (immutable specification, current state, latest observation) reaches the
model callback. No model, shell, tool registry or benchmark is supplied here.
The application owns its fixed domain schema and public-observation boundary.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
import re
from typing import Callable, Mapping


def _json(value: object) -> str:
    def check(item, depth=0):
        if depth > 32:
            raise ValueError("bounded JSON nesting required")
        if type(item) is dict:
            if any(not isinstance(key, str) or not key for key in item):
                raise ValueError("nonempty string JSON keys required")
            for child in item.values():
                check(child, depth + 1)
        elif type(item) is list:
            for child in item:
                check(child, depth + 1)
        elif type(item) not in (str, int, float, bool, type(None)):
            raise ValueError("JSON-native state and observations required")
    check(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValueError(f"non-finite JSON constant: {value}")


def merge_patch(state: Mapping[str, object], patch: Mapping[str, object]) -> dict:
    """Recursive dictionary merge; null deletes rather than setting a null slot."""
    if type(state) is not dict or type(patch) is not dict:
        raise ValueError("state and patch must be dictionaries")
    _json(state)
    _json(patch)
    merged = deepcopy(dict(state))
    for key, value in patch.items():
        if not isinstance(key, str) or not key:
            raise ValueError("nonempty string state keys required")
        if value is None:
            merged.pop(key, None)
        elif isinstance(value, dict):
            previous = merged.get(key, {})
            merged[key] = merge_patch(previous if isinstance(previous, Mapping) else {}, value)
        else:
            merged[key] = deepcopy(value)
    return merged


def parse_transition(response: str, *, max_response_chars: int = 32768) -> tuple[dict, str]:
    """Parse the exact two-field structured block; transient text is not retained."""
    if not isinstance(response, str) or len(response) > max_response_chars:
        raise ValueError("bounded text model response required")
    blocks = re.findall(r"```json\s*\n(.*?)\n```", response, re.DOTALL)
    if "```" in response and len(blocks) != 1:
        raise ValueError("exactly one JSON fenced block required")
    if len(blocks) == 1 and response.count("```") != 2:
        raise ValueError("ambiguous extra fenced blocks")
    text = blocks[0] if blocks else response
    try:
        item = json.loads(text, object_pairs_hook=_unique_object, parse_constant=_reject_constant)
    except (json.JSONDecodeError, TypeError, RecursionError) as error:
        raise ValueError("malformed transition JSON") from error
    if (not isinstance(item, dict) or set(item) != {"state_patch", "action"}
            or not isinstance(item["state_patch"], dict)
            or not isinstance(item["action"], str) or not item["action"].strip()):
        raise ValueError("exact state_patch dictionary and nonempty action required")
    _json(item)
    return item["state_patch"], item["action"]


@dataclass(frozen=True)
class ExecutionContext:
    specification: str
    state_json: str
    observation_json: str


@dataclass(frozen=True)
class StepOutcome:
    action: str
    observation: object
    version: int
    attempts: int
    prompt_characters: int


class SkillStateRuntime:
    """Single-agent runtime; invalid patches retry before any action execution.

    The state/observation character limits are explicit local resource guards,
    not a proof that every real task admits a bounded sufficient statistic.
    Valid state is committed before executing the action, as in Algorithm 1.
    Executor exceptions propagate without automatic retry or a claimed rollback
    of external side effects. This is not a sandbox for untrusted callbacks.
    """

    def __init__(self, specification: str, state: Mapping[str, object], *,
                 validator: Callable[[dict], bool], max_state_chars: int = 8192,
                 max_observation_chars: int = 8192, max_response_chars: int = 32768):
        if (not isinstance(specification, str) or not specification.strip()
                or not callable(validator)
                or any(type(n) is not int or n < 1 for n in (
                    max_state_chars, max_observation_chars, max_response_chars))):
            raise ValueError("immutable specification, validator and positive budgets required")
        self._specification = specification
        self._validator = validator
        self._max_state_chars = max_state_chars
        self._max_observation_chars = max_observation_chars
        self._max_response_chars = max_response_chars
        self._version = 0
        if type(state) is not dict:
            raise ValueError("initial state must be a JSON dictionary")
        self._state = self._validate(deepcopy(state))

    def _validate(self, candidate: dict) -> dict:
        encoded = _json(candidate)
        if len(encoded) > self._max_state_chars:
            raise ValueError("state character budget exceeded")
        # A validator receives a disposable copy, not mutable persistent state.
        if self._validator(deepcopy(candidate)) is not True:
            raise ValueError("domain schema rejected state")
        return candidate

    @property
    def version(self) -> int:
        return self._version

    def snapshot(self) -> dict:
        return deepcopy(self._state)

    def context(self, observation: object) -> ExecutionContext:
        encoded = _json(observation)
        if len(encoded) > self._max_observation_chars:
            raise ValueError("observation character budget exceeded")
        return ExecutionContext(self._specification, _json(self._state), encoded)

    def step(self, observation: object, *, actor: Callable[[ExecutionContext], str],
             executor: Callable[[str], object], max_attempts: int = 2) -> StepOutcome:
        if type(max_attempts) is not int or max_attempts < 1 or max_attempts > 8:
            raise ValueError("bounded retry count required")
        context = self.context(observation)
        prompt_chars = len(context.specification) + len(context.state_json) + len(context.observation_json)
        for attempt in range(1, max_attempts + 1):
            # The actor sees no previous response, reasoning, gold, grader or
            # rejected candidate. A retry receives exactly the same public view.
            response = actor(context)
            try:
                patch, action = parse_transition(response, max_response_chars=self._max_response_chars)
                candidate = self._validate(merge_patch(self._state, patch))
            except (ValueError, TypeError, RecursionError):
                if attempt == max_attempts:
                    raise ValueError("transition rejected; persistent state unchanged") from None
                continue
            del response, patch
            self._state = candidate
            self._version += 1
            result = executor(action)
            return StepOutcome(action, result, self._version, attempt, prompt_chars)
        raise AssertionError("unreachable")
