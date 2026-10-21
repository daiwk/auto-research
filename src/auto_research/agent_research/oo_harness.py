"""OO-Harness inheritance, discovery acceptance and frozen routing primitives.

Reference: arXiv:2610.28380v1, sections 3.2--3.5. Callers supply trusted
Python subclasses, an actor and tools. This is neither a code sandbox nor an
implementation of the paper's LLM evolution agent or benchmark environments.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Callable


@dataclass(frozen=True)
class PublicTask:
    task_id: str
    instruction: str

    def __post_init__(self):
        if any(not isinstance(value, str) or not value.strip()
               for value in (self.task_id, self.instruction)):
            raise ValueError("nonempty public task identifier and instruction required")


@dataclass(frozen=True)
class ToolObservation:
    tool: str
    content: str
    mutated: bool = False

    def __post_init__(self):
        if (not isinstance(self.tool, str) or not self.tool
                or not isinstance(self.content, str) or type(self.mutated) is not bool):
            raise ValueError("typed public tool observation required")


@dataclass(frozen=True)
class Action:
    kind: str
    payload: str
    tool: str = ""

    def __post_init__(self):
        if (self.kind not in ("tool", "finish") or not isinstance(self.payload, str)
                or not isinstance(self.tool, str)
                or (self.kind == "tool" and not self.tool)
                or (self.kind == "finish" and self.tool)):
            raise ValueError("a tool action or a tool-free finish action required")


@dataclass(frozen=True)
class ActorContext:
    task: PublicTask
    system_prompt: str
    available_tools: tuple[str, ...]
    observations: tuple[ToolObservation, ...]


@dataclass(frozen=True)
class PublicRun:
    task_id: str
    final_answer: str | None
    observations: tuple[ToolObservation, ...]
    actor_calls: int
    finish_rejections: int


Actor = Callable[[ActorContext], Action]
ToolExecutor = Callable[[str, str], ToolObservation]


class Harness:
    """One executable instance; inherited hooks do not spawn ancestor runs."""

    def system_prompt(self, task: PublicTask) -> str:
        return "Use public observations and available tools to complete the task."

    def tool_names(self) -> tuple[str, ...]:
        return ("read", "write")

    def verify_before_finish(self, task: PublicTask,
                             observations: tuple[ToolObservation, ...]) -> str | None:
        return None

    def run(self, task: PublicTask, *, actor: Actor, tools: ToolExecutor,
            max_turns: int = 16) -> PublicRun:
        if (not isinstance(task, PublicTask) or not callable(actor) or not callable(tools)
                or type(max_turns) is not int or not 1 <= max_turns <= 256):
            raise ValueError("public task, callbacks and bounded turn budget required")
        names = self.tool_names()
        prompt = self.system_prompt(task)
        if (type(names) is not tuple or not names or len(set(names)) != len(names)
                or any(not isinstance(name, str) or not name or name == "__finish_guard__"
                       for name in names) or not isinstance(prompt, str)):
            raise ValueError("valid harness tools and prompt required")
        observations: list[ToolObservation] = []
        rejections = 0
        for turn in range(1, max_turns + 1):
            action = actor(ActorContext(task, prompt, names, tuple(observations)))
            if not isinstance(action, Action):
                raise ValueError("actor must return a typed Action")
            if action.kind == "finish":
                reminder = self.verify_before_finish(task, tuple(observations))
                if reminder is None:
                    return PublicRun(task.task_id, action.payload, tuple(observations), turn, rejections)
                if not isinstance(reminder, str) or not reminder.strip():
                    raise ValueError("finish guard must return nonempty text or None")
                observations.append(ToolObservation("__finish_guard__", reminder))
                rejections += 1
                continue
            if action.tool not in names:
                raise ValueError("actor selected an unavailable tool")
            observation = tools(action.tool, action.payload)
            if not isinstance(observation, ToolObservation) or observation.tool != action.tool:
                raise ValueError("tool callback returned an invalid public observation")
            observations.append(observation)
        return PublicRun(task.task_id, None, tuple(observations), max_turns, rejections)


def _fingerprint(harness_type: type[Harness]) -> str:
    """Detect method replacement between freeze and use, not hostile Python state."""
    digest = hashlib.sha256()
    for cls in harness_type.__mro__:
        if not issubclass(cls, Harness):
            continue
        digest.update((cls.__module__ + "." + cls.__qualname__).encode())
        for name, member in sorted(vars(cls).items()):
            if callable(member) and hasattr(member, "__code__"):
                digest.update(name.encode())
                code = member.__code__
                digest.update(code.co_code)
                digest.update(repr((code.co_consts, code.co_names, code.co_varnames,
                    code.co_argcount, code.co_kwonlyargcount)).encode())
    return digest.hexdigest()


@dataclass(frozen=True)
class HarnessDescription:
    key: str
    parent_key: str | None
    mechanism: str


@dataclass(frozen=True)
class RoutingContext:
    task: PublicTask
    base_run: PublicRun
    catalogue: tuple[HarnessDescription, ...]
    lessons: tuple[str, ...]


@dataclass(frozen=True)
class DeploymentResult:
    selected_key: str
    run: PublicRun
    base_reused: bool
    total_actor_calls: int


@dataclass(frozen=True)
class CandidateOutcome:
    key: str
    parent_key: str
    cluster: str
    score: float
    previous_score: float
    checks_passed: bool
    accepted: bool


class HarnessDiscovery:
    """Cluster-local acceptance; scores remain outside the deployment view.

    The caller obtains scores from a discovery-only grader. Scores do not enter
    actor/router contexts. This module does not invent clusters or author code.
    """

    def __init__(self, base: type[Harness], *, discovery_task_ids: tuple[str, ...],
                 heldout_task_ids: tuple[str, ...], mechanism: str = "base harness"):
        self._validate_class(base)
        for ids in (discovery_task_ids, heldout_task_ids):
            if (type(ids) is not tuple or not ids or len(set(ids)) != len(ids)
                    or any(not isinstance(key, str) or not key.strip() for key in ids)):
                raise ValueError("distinct nonempty task identifier tuples required")
        if set(discovery_task_ids) & set(heldout_task_ids):
            raise ValueError("discovery and held-out task identifiers must be disjoint")
        self._discovery_ids = frozenset(discovery_task_ids)
        self._heldout_ids = heldout_task_ids
        self._types = {"base": base}
        self._descriptions = {"base": HarnessDescription("base", None, mechanism)}
        self._clusters: dict[str, tuple[str, float]] = {}
        self._outcomes: list[CandidateOutcome] = []
        self._attempted = {"base"}

    @staticmethod
    def _validate_class(cls):
        if not isinstance(cls, type) or not issubclass(cls, Harness):
            raise ValueError("trusted executable Harness subclass required")

    @staticmethod
    def _score(score):
        if type(score) not in (int, float) or not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError("finite discovery score in [0, 1] required")
        return float(score)

    def add_cluster(self, key: str, base_score: float, *, task_ids: tuple[str, ...]):
        if not isinstance(key, str) or not key.strip() or key in self._clusters:
            raise ValueError("new nonempty cluster identifier required")
        if (type(task_ids) is not tuple or not task_ids or len(set(task_ids)) != len(task_ids)
                or not set(task_ids) <= self._discovery_ids):
            raise ValueError("a cluster may contain only distinct discovery task identifiers")
        self._clusters[key] = ("base", self._score(base_score))

    def consider(self, key: str, candidate: type[Harness], *, parent_key: str,
                 cluster: str, score: float, checks_passed: bool,
                 mechanism: str) -> CandidateOutcome:
        self._validate_class(candidate)
        if (not isinstance(key, str) or not key.strip() or key in self._attempted
                or parent_key not in self._types or cluster not in self._clusters
                or self._types[parent_key] not in candidate.__bases__
                or type(checks_passed) is not bool
                or not isinstance(mechanism, str) or not mechanism.strip()):
            raise ValueError("new subclass of a registered parent and valid cluster required")
        value = self._score(score)
        previous = self._clusters[cluster][1]
        accepted = value > previous and checks_passed
        outcome = CandidateOutcome(key, parent_key, cluster, value, previous, checks_passed, accepted)
        self._attempted.add(key)
        self._outcomes.append(outcome)
        if accepted:
            self._types[key] = candidate
            self._descriptions[key] = HarnessDescription(key, parent_key, mechanism)
            self._clusters[cluster] = (key, value)
        return outcome

    @property
    def outcomes(self) -> tuple[CandidateOutcome, ...]:
        return tuple(self._outcomes)

    def freeze(self, *, routing_lessons: tuple[str, ...] = ()) -> FrozenHarnessLibrary:
        if (type(routing_lessons) is not tuple
                or any(not isinstance(item, str) or not item.strip() for item in routing_lessons)):
            raise ValueError("immutable nonempty routing lesson strings required")
        # Retain ancestors for inherited code, but route only to active cluster
        # assignments and base (section 3.5), not every historical specialist.
        active = {"base", *(value[0] for value in self._clusters.values())}
        return FrozenHarnessLibrary(
            tuple((key, cls, _fingerprint(cls)) for key, cls in self._types.items()),
            tuple(value for key, value in self._descriptions.items() if key in active),
            tuple(routing_lessons),
            self._heldout_ids,
        )


@dataclass(frozen=True)
class FrozenHarnessLibrary:
    _entries: tuple[tuple[str, type[Harness], str], ...]
    catalogue: tuple[HarnessDescription, ...]
    lessons: tuple[str, ...]
    _heldout_ids: tuple[str, ...]

    def deploy(self, task: PublicTask, *, actor: Actor,
               tool_factory: Callable[[], ToolExecutor],
               router: Callable[[RoutingContext], str], max_turns: int = 16) -> DeploymentResult:
        if not callable(router) or not callable(tool_factory):
            raise ValueError("router and fresh task-environment factory required")
        if not isinstance(task, PublicTask) or task.task_id not in self._heldout_ids:
            raise ValueError("deployment requires a predeclared held-out task")
        if any(_fingerprint(cls) != fingerprint for _, cls, fingerprint in self._entries):
            raise ValueError("harness methods changed after freezing")
        types = {key: cls for key, cls, _ in self._entries}
        base = types["base"]().run(task, actor=actor, tools=tool_factory(), max_turns=max_turns)
        selected = router(RoutingContext(task, base, self.catalogue, self.lessons))
        if not isinstance(selected, str) or selected not in {item.key for item in self.catalogue}:
            raise ValueError("router must select an active frozen harness identifier")
        if selected == "base":
            return DeploymentResult(selected, base, True, base.actor_calls)
        result = types[selected]().run(task, actor=actor, tools=tool_factory(), max_turns=max_turns)
        return DeploymentResult(selected, result, False, base.actor_calls + result.actor_calls)
