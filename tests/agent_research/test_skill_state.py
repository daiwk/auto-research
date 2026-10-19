from __future__ import annotations

import json

import pytest

from auto_research.agent_research.skill_state import SkillStateRuntime, merge_patch, parse_transition


def validator(state):
    return set(state) <= {"count", "slots"} and type(state.get("count")) is int and isinstance(state.get("slots", {}), dict)


def transition(patch, action="inert-action"):
    return "TRANSIENT_REASONING_NOT_PERSISTED\n```json\n" + json.dumps({"state_patch": patch, "action": action}) + "\n```"


def test_recursive_merge_null_deletion_preserves_unmentioned_state_without_aliasing():
    source = {"count": 1, "slots": {"a": 10, "b": [20]}}
    patch = {"slots": {"a": None, "c": 30}}
    result = merge_patch(source, patch)
    assert result == {"count": 1, "slots": {"b": [20], "c": 30}}
    result["slots"]["b"].append(40)
    assert source["slots"]["b"] == [20] and patch == {"slots": {"a": None, "c": 30}}


@pytest.mark.parametrize("response", [
    '{"state_patch":{},"action":"a","gold":"private"}',
    '{"state_patch":{},"state_patch":{"count":9},"action":"a"}',
    '{"state_patch":{"count":NaN},"action":"a"}',
    '{"state_patch":[],"action":"a"}',
    '{"state_patch":{},"action":" "}',
    '```json\n{"state_patch":{},"action":"a"}\n```\n```json\n{}\n```',
])
def test_parser_rejects_ambiguous_nonfinite_and_wrong_schema_outputs(response):
    with pytest.raises(ValueError):
        parse_transition(response)


def test_invalid_patch_retry_is_atomic_and_only_current_public_context_is_visible():
    runtime = SkillStateRuntime("immutable spec", {"count": 1, "slots": {"a": 4}}, validator=validator)
    views, actions = [], []
    def actor(context):
        views.append(context)
        assert set(context.__dataclass_fields__) == {"specification", "state_json", "observation_json"}
        return transition({"gold": "forbidden"}) if len(views) == 1 else transition({"count": 2})
    outcome = runtime.step({"public": "latest"}, actor=actor, executor=lambda action: actions.append(action) or "ok")
    assert views[0] == views[1] and outcome.attempts == 2
    assert actions == ["inert-action"] and runtime.snapshot() == {"count": 2, "slots": {"a": 4}}
    next_view = runtime.context({"public": "next"})
    assert "latest" not in next_view.observation_json and "TRANSIENT" not in str(next_view)
    assert not hasattr(runtime, "history") and not hasattr(runtime, "reasoning")


def test_rejected_patch_does_not_commit_or_execute_and_snapshot_is_detached():
    runtime = SkillStateRuntime("spec", {"count": 1}, validator=validator)
    actions = []
    with pytest.raises(ValueError, match="unchanged"):
        runtime.step({}, actor=lambda _: transition({"count": "wrong type"}), executor=actions.append)
    assert runtime.snapshot() == {"count": 1} and runtime.version == 0 and not actions
    copy = runtime.snapshot()
    copy["count"] = 100
    assert runtime.snapshot()["count"] == 1


def test_resource_limits_reject_growth_instead_of_claiming_unconditional_constant_size():
    runtime = SkillStateRuntime("spec", {"count": 1}, validator=validator, max_state_chars=32, max_observation_chars=16)
    with pytest.raises(ValueError, match="observation"):
        runtime.context("x" * 100)
    with pytest.raises(ValueError, match="unchanged"):
        runtime.step({}, actor=lambda _: transition({"slots": {"x": "a" * 100}}), executor=lambda _: None)
    assert runtime.version == 0


@pytest.mark.parametrize("value", [{1: "coerced key"}, {"slots": (1, 2)}, {"x": float("nan")}])
def test_json_coercion_or_nonfinite_initial_state_is_not_silently_accepted(value):
    with pytest.raises(ValueError):
        SkillStateRuntime("spec", value, validator=lambda _: True)


def test_validator_mutations_do_not_change_state_and_executor_failure_is_not_retried():
    def schema(state):
        state["injected"] = "validator private copy"
        return True
    runtime = SkillStateRuntime("spec", {"count": 1}, validator=schema)
    calls = []
    def executor(action):
        calls.append(action)
        raise RuntimeError("external outcome unknown")
    with pytest.raises(RuntimeError, match="unknown"):
        runtime.step({}, actor=lambda _: transition({"count": 2}), executor=executor)
    assert calls == ["inert-action"] and runtime.snapshot() == {"count": 2} and runtime.version == 1


def test_long_horizon_has_no_append_only_prompt_history():
    runtime = SkillStateRuntime("add public deltas", {"count": 0}, validator=validator)
    chars = []
    for _ in range(100):
        def actor(context):
            value = json.loads(context.state_json)["count"] + json.loads(context.observation_json)["delta"]
            return transition({"count": value})
        chars.append(runtime.step({"delta": 1}, actor=actor, executor=lambda _: "ok").prompt_characters)
    assert runtime.snapshot()["count"] == 100 and max(chars) - min(chars) <= 2


@pytest.mark.parametrize("attempts", [0, -1, 9, True])
def test_retry_count_is_bounded(attempts):
    runtime = SkillStateRuntime("spec", {"count": 0}, validator=validator)
    with pytest.raises(ValueError):
        runtime.step({}, actor=lambda _: transition({}), executor=lambda _: None, max_attempts=attempts)
@pytest.mark.parametrize("bad", [float("nan"), float("inf"), (1, 2), {1, 2}])
def test_merge_rejects_non_json_values(bad):
    with pytest.raises(ValueError):
        merge_patch({}, {"bad": bad})


def test_merge_replaces_arrays_and_scalar_with_object():
    assert merge_patch({"items": [1], "scalar": 2}, {"items": [2, 3], "scalar": {"x": 1}}) == {
        "items": [2, 3], "scalar": {"x": 1}}
    assert merge_patch({}, {}) == {}
    with pytest.raises(ValueError):
        SkillStateRuntime("spec", [("x", 1)], validator=lambda _: True)

