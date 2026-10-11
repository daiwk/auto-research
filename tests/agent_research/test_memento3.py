"""Hand-written programs below are unit fixtures, NEVER runtime model fallback."""

import json
import random

import pytest

from auto_research.agent_research.memento3 import (
    Hypothesis, Memento3, Trajectory, observation, replay, shortest_plan,
)
from auto_research.agent_research.memento3_python import ProgramError, RestrictedProgram


SOURCE = '''def initialise(observation):
    return {"x": 0}
def step(state, action):
    x = state["x"]
    if action == 0:
        x = min(x + 1, 2)
    else:
        x = max(x - 1, 0)
    return {"x": x}
def observe(state):
    cells = [0, 0, 3]
    cells[state["x"]] = 4
    return {"grid": [cells], "completed": goal(state), "terminated": goal(state)}
def goal(state):
    return state["x"] == 2
'''


def obs(x):
    cells = [0, 0, 3]
    cells[x] = 4
    return {"grid": [cells], "completed": x == 2, "terminated": x == 2}


def fixture_generator(role, prompt):
    return json.dumps({"rulebook": {"rulebook": "Action 0 moves right to column 2; action 1 left; column 2 completes."},
                       "compile": {"source": SOURCE},
                       "faithfulness": {"faithful": True, "reason": "All stated fixture rules implemented."},
                       "reflection": {"choice": "repair_code", "reason": "fixture"},
                       "explore": {"action": 0, "reason": "probe"}}[role])


def test_exact_all_history_replay_and_no_input_mutation():
    program = RestrictedProgram(SOURCE)
    initial = obs(0)
    history = Trajectory(initial, [(0, obs(1)), (0, obs(2))])
    assert replay(program, [history]) == {"x": 2}
    assert initial == obs(0)
    earlier_error = Trajectory(obs(0), [(0, obs(2))])
    with pytest.raises(ProgramError, match="trajectory 0, transition 1"):
        replay(program, [earlier_error, history])


def test_cell_exact_not_average_or_last_frame_check():
    program = RestrictedProgram(SOURCE)
    changed = obs(1)
    changed["grid"][0][0] = 1
    with pytest.raises(ProgramError, match="replay mismatch"):
        replay(program, [Trajectory(obs(0), [(0, changed), (0, obs(2))])])
    changed = obs(1)
    changed["completed"] = True
    with pytest.raises(ProgramError, match="replay mismatch"):
        replay(program, [Trajectory(obs(0), [(0, changed)])])


def test_shortest_plan_executes_generated_model_only():
    program = RestrictedProgram(SOURCE)
    assert shortest_plan(program, {"x": 0}, (0, 1), horizon=4) == (0, 0)
    assert shortest_plan(program, {"x": 0}, (0, 1), horizon=1) is None
    assert shortest_plan(program, {"x": 2}, (0, 1)) == ()


@pytest.mark.parametrize("suffix", [
    "import os", "class Escape: pass", "x = open('secret')", "def evil():\n    return (1).__class__",
    "def evil():\n    return eval('1')", "def evil():\n    return [x for x in range(2)]",
    "def evil():\n    return lambda: 1", "def evil():\n    return __import__('os')",
    "def evil():\n    return 2 ** 9999999", "def evil():\n    yield 1",
    "def evil():\n    global x\n    x = 1", "def evil():\n    return {'a': 1}.get('a')",
])
def test_unknown_syntax_and_escape_attempts_fail_closed(suffix):
    with pytest.raises(ProgramError):
        RestrictedProgram(SOURCE + suffix)


@pytest.mark.parametrize("replacement, message", [
    ("while True:\n        pass", "fuel"),
    ("return step(state, action)", "recursive"),
    ("return [0] * 100000000", "allocation"),
    ("return list(range(100000000))", "range limit"),
    ("return 100000000 + 1", "integer limit"),
])
def test_execution_limits_prevent_hangs_or_large_allocations(replacement, message):
    start = SOURCE.index("def step")
    end = SOURCE.index("def observe")
    source = SOURCE[:start] + "def step(state, action):\n    " + replacement + "\n" + SOURCE[end:]
    program = RestrictedProgram(source, fuel=100)
    with pytest.raises(ProgramError, match=message):
        program.call("step", {"x": 0}, 0)


def test_total_nested_size_guard():
    program = RestrictedProgram(SOURCE)
    huge = [[0] * 4096] * 100
    with pytest.raises(ProgramError, match="total value size"):
        program.call("initialise", huge)


def test_hypothesis_requires_boolean_semantic_judge_and_exact_replay():
    for judge in ({"faithful": False, "reason": "omitted rule"}, {"faithful": "true", "reason": "bad type"}):
        def generate(role, prompt):
            return json.dumps(judge) if role == "faithfulness" else fixture_generator(role, prompt)
        controller = Memento3(generate, (0, 1), population=1, repair_attempts=1)
        controller.start(obs(0))
        controller.update()
        assert controller.members == [None]
        assert any(event["stage"] == "rejected" for event in controller.events)


def test_population_sampling_uniform_over_distinct_plans_not_member_count():
    controller = Memento3(fixture_generator, (0, 1), population=3)
    controller.start(obs(0))
    controller.members = [Hypothesis("fixture", RestrictedProgram(SOURCE), 0) for _ in range(3)]
    # Deliberate injected unit-test plans to isolate the Eq.33 sampling rule.
    controller.plans = lambda remaining: {(0, 0): [0, 1], (1, 1): [2]}
    expected = random.Random(42).choice([(0, 0), (1, 1)])
    assert controller.choose(4) == expected[0]
    assert controller.events[-1]["class_count"] == 2
    assert controller.active[1] == expected[1:]


def test_plan_stays_active_until_falsification_then_invalidates_even_budget_exhausted():
    controller = Memento3(fixture_generator, (0, 1), population=1, repair_attempts=1, revision_budget=1)
    controller.start(obs(0))
    controller.update()
    assert controller.choose(4) == 0
    assert controller.observe(0, obs(1)) is False
    assert controller.choose(3) == 0
    assert controller.observe(0, obs(1)) is True
    assert controller.active is None
    controller.update()
    assert controller.members == [None]
    assert controller.versions  # Earlier accepted versions are not deleted.


def test_no_hidden_environment_or_gold_fields_in_prompts():
    prompts = []
    def generate(role, prompt):
        prompts.append(prompt)
        return fixture_generator(role, prompt)
    controller = Memento3(generate, (0, 1), population=1)
    controller.start(obs(0))
    controller.update()
    assert len(controller.versions) == 1
    assert all(word not in prompt for prompt in prompts for word in ("gold_plan", "transition_table", "env.unwrapped"))
    assert json.loads(controller._context(None))["history"][0] == {
        "initial": obs(0), "transitions": []}


def test_observation_rejects_boolean_cells_and_ragged_grids():
    with pytest.raises(ProgramError):
        observation({"grid": [[True]], "completed": False, "terminated": False})
    with pytest.raises(ProgramError):
        observation({"grid": [[1], [1, 2]], "completed": False, "terminated": False})


def test_no_action_when_llm_exploration_invalid_not_handwritten_fallback():
    controller = Memento3(lambda role, prompt: '{"action":99}', (0, 1), population=1)
    controller.start(obs(0))
    assert controller.choose(4) is None
    assert controller.events[-1]["stage"] == "exploration_failed"
