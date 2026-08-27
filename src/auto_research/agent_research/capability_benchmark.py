from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Literal

import numpy as np

from .capability_models import CapabilityObservation, ToolFeedback, ToolSpec


CapabilitySplit = Literal["train", "validation", "test"]
SAFE_TOOLS = (
    "search", "database", "calculator", "calendar", "maps", "weather",
    "files", "validator", "catalog", "resolver",
)
RISKY_TOOLS = ("publish", "delete")
TOOL_NAMES = (*SAFE_TOOLS, *RISKY_TOOLS)
TOOL_TAGS = tuple(f"T{index:02d}" for index in range(len(TOOL_NAMES)))
FAMILIES = {
    "train": ("travel", "finance", "retail", "support"),
    "validation": ("logistics", "education", "media", "health"),
    "test": ("science", "legal", "security", "operations"),
}
AXES = ("clean", "transient", "ambiguous", "fallback", "irreversible", "combined")
DEPTHS = {"train": (3, 4), "validation": (4, 5), "test": (5, 6)}


@dataclass(frozen=True)
class _CapabilityTask:
    """Evaluator-private task. Policies only receive ``observation``."""

    observation: CapabilityObservation
    allowed_steps: tuple[frozenset[str], ...]
    canonical_route: tuple[str, ...]
    answer: str
    axis: str
    transient_steps: frozenset[int]
    fallback_tools: tuple[tuple[int, str], ...]
    irreversible_decoys: tuple[tuple[int, str], ...]
    ambiguous_tag: str = ""

    @property
    def fallback_map(self) -> dict[int, str]:
        return dict(self.fallback_tools)

    @property
    def irreversible_map(self) -> dict[int, str]:
        return dict(self.irreversible_decoys)


def _tag(tool: str) -> str:
    return TOOL_TAGS[TOOL_NAMES.index(tool)]


def _tool_specs() -> tuple[ToolSpec, ...]:
    rows = []
    for index, (name, tag) in enumerate(zip(TOOL_NAMES, TOOL_TAGS)):
        risky = name in RISKY_TOOLS
        rows.append(ToolSpec(
            name=name,
            tag=tag,
            description=(
                f"{name} resolves evidence labelled {tag}; "
                f"{'irreversible side effects' if risky else 'read-only and reversible'}"
            ),
            reliability=0.78 + 0.02 * ((index * 7) % 10),
            reversible=not risky,
            cost=1.4 if risky else 0.8 + 0.08 * (index % 4),
        ))
    return tuple(rows)


def _family_route(split: CapabilitySplit, family_index: int, depth: int) -> tuple[str, ...]:
    split_offset = {"train": 0, "validation": 2, "test": 4}[split]
    return tuple(
        SAFE_TOOLS[(split_offset + family_index * 3 + offset * 7) % len(SAFE_TOOLS)]
        for offset in range(depth)
    )


def build_capability_tasks(
    episodes: int,
    seed: int,
    split: CapabilitySplit = "test",
) -> tuple[_CapabilityTask, ...]:
    """Build disjoint L2.1 tasks with harder held-out validation/test routes."""

    if split not in FAMILIES:
        raise ValueError(f"unsupported capability split: {split}")
    offset = {"train": 0, "validation": 10_000, "test": 20_000}[split]
    rng = np.random.default_rng(seed + offset)
    specs = _tool_specs()
    modes = np.resize(np.arange(len(AXES)), episodes)
    rng.shuffle(modes)
    tasks = []
    families = FAMILIES[split]
    depths = DEPTHS[split]
    for index in range(episodes):
        family_index = index % len(families)
        family = families[family_index]
        depth = depths[index % len(depths)]
        route = _family_route(split, family_index, depth)
        allowed = [frozenset({tool}) for tool in route]
        mode = int(modes[index])
        axis = AXES[mode]
        transient = frozenset({1}) if axis in {"transient", "combined"} else frozenset()
        fallback_tools: list[tuple[int, str]] = []
        if axis in {"fallback", "combined"}:
            fallback = next(tool for tool in SAFE_TOOLS if tool != route[1])
            fallback_tools.append((1, fallback))
            allowed[1] = frozenset({route[1], fallback})
        irreversible: list[tuple[int, str]] = []
        ambiguous_tag = ""
        if axis in {"ambiguous", "irreversible", "combined"}:
            if axis == "irreversible":
                decoy = RISKY_TOOLS[index % len(RISKY_TOOLS)]
                irreversible.append((1, decoy))
            else:
                choices = [tool for tool in SAFE_TOOLS if tool not in allowed[1]]
                decoy = choices[(family_index + offset) % len(choices)]
            ambiguous_tag = _tag(decoy)
        shuffled_specs = list(specs)
        rng.shuffle(shuffled_specs)
        tasks.append(_CapabilityTask(
            observation=CapabilityObservation(
                task_id=f"toolroute-l21-{split}-{seed}-{index:04d}",
                split=split,
                family=family,
                request=(
                    f"Resolve held-out {family} case {index:04d}. Follow returned evidence "
                    "tags, avoid irreversible distractors, and return only the resolved value."
                ),
                start_tags=(_tag(route[0]),),
                tools=tuple(shuffled_specs),
            ),
            allowed_steps=tuple(allowed),
            canonical_route=route,
            answer=f"{family}-{int(rng.integers(1000, 9999))}",
            axis=axis,
            transient_steps=transient,
            fallback_tools=tuple(fallback_tools),
            irreversible_decoys=tuple(irreversible),
            ambiguous_tag=ambiguous_tag,
        ))
    return tuple(tasks)


class CapabilityEnvironment:
    """Stateful tool API with no answer/plan/route introspection endpoint."""

    def __init__(self, task: _CapabilityTask):
        self.__task = task
        self.__position = 0
        self.__transient_seen: set[int] = set()
        self.__fallback_required = False
        self.__terminal = False
        self.calls: list[str] = []
        self.successful_tools: list[str] = []
        self.invalid_calls = 0
        self.irreversible_errors = 0
        self.tool_budget = (
            len(task.allowed_steps)
            + len(task.transient_steps)
            + len(task.fallback_tools)
        )
        self._specs = {spec.name: spec for spec in task.observation.tools}

    def call(self, tool: str) -> ToolFeedback:
        self.calls.append(tool)
        task = self.__task
        if tool not in self._specs:
            self.invalid_calls += 1
            return ToolFeedback("unknown_tool", "Unknown tool; no evaluator hints are available.")
        if self.__terminal:
            return ToolFeedback("terminal", "The episode has already terminated.", terminal=True)
        if len(self.calls) > self.tool_budget or self.__position >= len(task.allowed_steps):
            self.__terminal = True
            return ToolFeedback("budget_exhausted", "No tool budget remains.", terminal=True)
        irreversible = task.irreversible_map.get(self.__position)
        if tool == irreversible:
            self.irreversible_errors += 1
            self.__terminal = True
            return ToolFeedback(
                "irreversible_error", "An irreversible distractor terminated the episode.",
                terminal=True,
            )
        fallback = task.fallback_map.get(self.__position)
        primary = task.canonical_route[self.__position]
        if fallback and tool == primary and not self.__fallback_required:
            self.__fallback_required = True
            return ToolFeedback(
                "permanent_error",
                "Primary tool is unavailable; use the returned read-only fallback.",
                (_tag(fallback),),
            )
        expected = frozenset({fallback}) if self.__fallback_required else task.allowed_steps[self.__position]
        if tool not in expected:
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
        self.__fallback_required = False
        if self.__position == len(task.allowed_steps):
            self.__terminal = True
            return ToolFeedback("ok", "Final evidence resolved.", answer=task.answer, terminal=True)
        next_tags = [_tag(task.canonical_route[self.__position])]
        if task.ambiguous_tag and self.__position == 1:
            task_index = int(task.observation.task_id.rsplit("-", 1)[-1])
            if task_index % 2:
                next_tags.insert(0, task.ambiguous_tag)
            else:
                next_tags.append(task.ambiguous_tag)
        return ToolFeedback("ok", "Evidence accepted; continue with returned tags.", tuple(next_tags))

    @property
    def completed(self) -> bool:
        return self.__position == len(self.__task.allowed_steps)

    @property
    def cost(self) -> float:
        fallback = ToolSpec("unknown", "", "")
        return float(sum(self._specs.get(tool, fallback).cost for tool in self.calls))


def _ordered_step_overlap(actions: list[str], task: _CapabilityTask) -> int:
    position = 0
    fallback_map = task.fallback_map
    for action in actions:
        if position >= len(task.allowed_steps):
            break
        allowed = set(task.allowed_steps[position])
        if position in fallback_map:
            allowed.add(fallback_map[position])
        if action in allowed:
            position += 1
    return position


def evaluate_episode(
    task: _CapabilityTask,
    answer: str,
    environment: CapabilityEnvironment,
) -> dict[str, float | bool | str]:
    actions = list(environment.calls)
    overlap = _ordered_step_overlap(environment.successful_tools, task)
    step_f1 = 2 * overlap / max(1, len(actions) + len(task.allowed_steps))
    answer_ok = answer == task.answer
    plan_ok = environment.completed and environment.invalid_calls == 0
    return {
        "task_id": task.observation.task_id,
        "split": task.observation.split,
        "axis": task.axis,
        "answer_ok": answer_ok,
        "plan_ok": plan_ok,
        "joint_ok": answer_ok and plan_ok,
        "plan_step_f1": step_f1,
        "has_failure": bool(task.transient_steps or task.fallback_tools),
        "tool_calls": float(len(actions)),
        "invalid_calls": float(environment.invalid_calls),
        "irreversible_errors": float(environment.irreversible_errors),
        "cost": environment.cost,
    }


def capability_dataset_fingerprint(episodes: int, seeds: tuple[int, ...]) -> str:
    rows = []
    for split in ("train", "validation", "test"):
        for seed in seeds:
            for task in build_capability_tasks(episodes, seed, split):
                rows.append({
                    "task_id": task.observation.task_id,
                    "split": split,
                    "family": task.observation.family,
                    "route": task.canonical_route,
                    "allowed_steps": [sorted(step) for step in task.allowed_steps],
                    "axis": task.axis,
                    "answer": task.answer,
                    "transient_steps": sorted(task.transient_steps),
                    "fallback_tools": task.fallback_tools,
                    "irreversible_decoys": task.irreversible_decoys,
                })
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()
