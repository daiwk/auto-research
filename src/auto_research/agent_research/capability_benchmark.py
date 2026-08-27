from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json

import numpy as np

from .capability_models import CapabilityObservation, ToolFeedback, ToolSpec


TOOL_NAMES = (
    "search", "database", "calculator", "calendar",
    "maps", "weather", "files", "validator",
)
TOOL_TAGS = tuple(f"T{index}" for index in range(len(TOOL_NAMES)))
FAMILIES = ("travel", "finance", "research", "ops", "shopping", "support")


@dataclass(frozen=True)
class _CapabilityTask:
    """Evaluator-private labels; this type is never passed to a policy."""

    observation: CapabilityObservation
    route: tuple[str, ...]
    answer: str
    axis: str
    transient_steps: frozenset[int]
    ambiguous_steps: frozenset[int]
    ambiguous_correct_first: bool


def _family_route(family_index: int) -> tuple[str, ...]:
    depth = 3 + family_index % 2
    return tuple(
        TOOL_NAMES[(family_index * 3 + offset * 5) % len(TOOL_NAMES)]
        for offset in range(depth)
    )


def build_capability_tasks(episodes: int, seed: int) -> tuple[_CapabilityTask, ...]:
    rng = np.random.default_rng(seed)
    specs = tuple(
        ToolSpec(name, tag, f"{name} resolves evidence labelled {tag}")
        for name, tag in zip(TOOL_NAMES, TOOL_TAGS)
    )
    tasks = []
    modes = np.resize(np.arange(4), episodes)
    rng.shuffle(modes)
    for index in range(episodes):
        family_index = index % len(FAMILIES)
        family = FAMILIES[family_index]
        route = _family_route(family_index)
        route_tags = tuple(TOOL_TAGS[TOOL_NAMES.index(tool)] for tool in route)
        mode = int(modes[index])
        transient = frozenset({1}) if mode in {1, 3} else frozenset()
        ambiguous = frozenset({1}) if mode in {2, 3} else frozenset()
        axis = ("clean", "transient", "ambiguous", "combined")[mode]
        answer = f"{family}-{int(rng.integers(1000, 9999))}"
        tools = list(specs)
        rng.shuffle(tools)
        start_tags = (route_tags[0],)
        tasks.append(_CapabilityTask(
            observation=CapabilityObservation(
                task_id=f"toolroute-l2-{seed}-{index:04d}",
                family=family,
                request=(
                    f"Resolve case {index:04d}. Start from evidence tag {route_tags[0]}; "
                    "follow tool feedback and return only the final resolved value."
                ),
                start_tags=start_tags,
                tools=tuple(tools),
            ),
            route=route,
            answer=answer,
            axis=axis,
            transient_steps=transient,
            ambiguous_steps=ambiguous,
            ambiguous_correct_first=bool(rng.integers(0, 2)),
        ))
    return tuple(tasks)


class CapabilityEnvironment:
    """Stateful tool API that reveals evidence only after a policy calls a tool."""

    def __init__(self, task: _CapabilityTask):
        self.__task = task
        self.__position = 0
        self.__transient_seen: set[int] = set()
        self.calls: list[str] = []
        self.successful_tools: list[str] = []
        self.invalid_calls = 0
        self.guide_calls = 0
        self.tool_budget = len(task.route) + 1

    def call(self, tool: str) -> ToolFeedback:
        self.calls.append(tool)
        task = self.__task
        if tool == "guide":
            self.guide_calls += 1
            expected = task.route[min(self.__position, len(task.route) - 1)]
            tag = TOOL_TAGS[TOOL_NAMES.index(expected)]
            return ToolFeedback("hint", "Verifier returned the current evidence tag.", (tag,))
        action_calls = len(self.calls) - self.guide_calls
        if action_calls > self.tool_budget or self.__position >= len(task.route):
            return ToolFeedback("budget_exhausted", "No tool budget remains.")
        expected = task.route[self.__position]
        if tool != expected:
            self.invalid_calls += 1
            return ToolFeedback("wrong_tool", "Tool produced no relevant evidence.")
        if (
            self.__position in task.transient_steps
            and self.__position not in self.__transient_seen
        ):
            self.__transient_seen.add(self.__position)
            return ToolFeedback("transient_error", "Temporary tool failure; retry is allowed.")
        self.successful_tools.append(tool)
        self.__position += 1
        if self.__position == len(task.route):
            return ToolFeedback("ok", "Final evidence resolved.", answer=task.answer)
        next_tool = task.route[self.__position]
        next_tag = TOOL_TAGS[TOOL_NAMES.index(next_tool)]
        next_tags = (next_tag,)
        if self.__position in task.ambiguous_steps:
            decoy = TOOL_TAGS[(TOOL_TAGS.index(next_tag) + 3) % len(TOOL_TAGS)]
            next_tags = (
                (next_tag, decoy) if task.ambiguous_correct_first else (decoy, next_tag)
            )
        return ToolFeedback("ok", "Evidence accepted; continue with returned tag.", next_tags)

    @property
    def cost(self) -> float:
        return float(len(self.calls) + 0.5 * self.guide_calls)


def _lcs_length(left: list[str], right: tuple[str, ...]) -> int:
    table = [[0] * (len(right) + 1) for _ in range(len(left) + 1)]
    for i, lvalue in enumerate(left, start=1):
        for j, rvalue in enumerate(right, start=1):
            table[i][j] = (
                table[i - 1][j - 1] + 1
                if lvalue == rvalue
                else max(table[i - 1][j], table[i][j - 1])
            )
    return table[-1][-1]


def evaluate_episode(
    task: _CapabilityTask,
    answer: str,
    environment: CapabilityEnvironment,
) -> dict[str, float | bool | str]:
    actions = [call for call in environment.calls if call != "guide"]
    overlap = _lcs_length(actions, task.route)
    step_f1 = 2 * overlap / max(1, len(actions) + len(task.route))
    answer_ok = answer == task.answer
    plan_ok = tuple(environment.successful_tools) == task.route
    return {
        "task_id": task.observation.task_id,
        "axis": task.axis,
        "answer_ok": answer_ok,
        "plan_ok": plan_ok,
        "joint_ok": answer_ok and plan_ok,
        "plan_step_f1": step_f1,
        "has_failure": bool(task.transient_steps),
        "tool_calls": float(len(actions)),
        "invalid_calls": float(environment.invalid_calls),
        "cost": environment.cost,
    }


def capability_dataset_fingerprint(episodes: int, seeds: tuple[int, ...]) -> str:
    rows = []
    for seed in seeds:
        for task in build_capability_tasks(episodes, seed):
            rows.append({
                "task_id": task.observation.task_id,
                "family": task.observation.family,
                "route": task.route,
                "axis": task.axis,
                "answer": task.answer,
                "transient_steps": sorted(task.transient_steps),
                "ambiguous_steps": sorted(task.ambiguous_steps),
                "ambiguous_correct_first": task.ambiguous_correct_first,
            })
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()
