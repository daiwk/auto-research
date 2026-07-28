from __future__ import annotations

from dataclasses import dataclass
import re

import numpy as np

from .models import AgentTask


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9-]+", text.lower()))


@dataclass
class MemoryEntry:
    key: str
    answer: str
    plan: tuple[str, ...]
    tokens: set[str]
    successes: float = 1.0
    failures: float = 1.0
    last_used: int = 0


class BaseAgent:
    def __init__(self, capacity: int, rng: np.random.Generator):
        self.capacity, self.rng = capacity, rng
        self.memory: list[MemoryEntry] = []
        self.cost = 0.0
        self.tool_evictions = 0
        self.reused_plans = 0
        self.reasoning_steps = 0
        self.actions = 0
        self.reflections = 0
        self.skills_created = 0
        self.skills_reused = 0
        self.verification_retries = 0

    def solve(self, task: AgentTask, step: int) -> tuple[str, tuple[str, ...], str]:
        raise NotImplementedError

    def observe(self, task: AgentTask, answer_ok: bool, plan_ok: bool, step: int) -> None:
        pass

    def _best(self, task: AgentTask) -> tuple[MemoryEntry | None, float]:
        query = _tokens(task.intent)
        scored = []
        for entry in self.memory:
            union = query | entry.tokens
            similarity = len(query & entry.tokens) / max(1, len(union))
            scored.append((similarity, entry))
        return max(scored, default=(0.0, None), key=lambda pair: pair[0])[::-1]


class LongContextAgent(BaseAgent):
    def solve(self, task, step):
        # Full current context is accurate, but grows linearly and has no
        # reusable procedural abstraction.
        self.cost += len(task.context) + len(self.memory)
        return task.answer, task.plan, "current-context"

    def observe(self, task, answer_ok, plan_ok, step):
        self.memory.append(
            MemoryEntry(task.intent, task.answer, task.plan, _tokens(task.intent), last_used=step)
        )


class ReActAgent(BaseAgent):
    def solve(self, task, step):
        # Each tool call is preceded by an explicit reasoning step and followed
        # by an observation. The deterministic suite makes the observation
        # available in the current context rather than through an external API.
        for _tool in task.required_tools:
            self.reasoning_steps += 1
            self.actions += 1
            self.cost += 1.0
        answer = task.context[0].rsplit(" ", 1)[-1]
        domain = task.intent.split(" family-", 1)[0]
        plan = tuple(f"{tool}:{domain}" for tool in task.required_tools)
        return answer, plan, "thought/action/observation"


class ReflexionAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.episodic_reflections: dict[str, str] = {}

    def solve(self, task, step):
        if task.intent not in self.episodic_reflections:
            # The first attempt exposes a plausible planning error. Feedback is
            # converted to language memory by observe(), without weight updates.
            self.reasoning_steps += 1
            self.cost += 2.0
            return task.context[1], task.plan[:-1], "first-attempt"
        self.reasoning_steps += 1
        self.reused_plans += 1
        self.cost += 1.0
        answer = task.context[0].rsplit(" ", 1)[-1]
        return answer, task.plan, "episodic-reflection"

    def observe(self, task, answer_ok, plan_ok, step):
        if not (answer_ok and plan_ok):
            self.episodic_reflections[task.intent] = (
                "Read the current case result and execute every required tool in order."
            )
            self.reflections += 1
            if len(self.episodic_reflections) > self.capacity:
                self.episodic_reflections.pop(next(iter(self.episodic_reflections)))


class VoyagerAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skills: dict[str, tuple[str, ...]] = {}
        self.pending_skill: tuple[str, tuple[str, ...]] | None = None

    @staticmethod
    def _key(task):
        domain = task.intent.split(" family-", 1)[0]
        return f"{domain}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        if key in self.skills:
            self.skills_reused += 1
            self.reused_plans += 1
            self.cost += 0.8
            return task.answer, self.skills[key], "skill-library"
        # Iterative prompting uses execution feedback and self-verification
        # before admitting executable code (represented here by the tool plan)
        # into the skill library.
        self.reasoning_steps += len(task.required_tools)
        self.actions += len(task.required_tools)
        self.verification_retries += 1
        self.cost += 4.0
        self.pending_skill = (key, task.plan)
        return task.answer, task.plan, "curriculum/execute/verify"

    def observe(self, task, answer_ok, plan_ok, step):
        if answer_ok and plan_ok and self.pending_skill is not None:
            key, plan = self.pending_skill
            if key not in self.skills:
                if len(self.skills) >= self.capacity:
                    self.skills.pop(next(iter(self.skills)))
                self.skills[key] = plan
                self.skills_created += 1
            self.pending_skill = None


class UMemAgent(BaseAgent):
    def solve(self, task, step):
        query = _tokens(task.intent)
        scored = []
        for entry in self.memory:
            union = query | entry.tokens
            semantic = len(query & entry.tokens) / max(1, len(union))
            thompson = self.rng.beta(entry.successes, entry.failures)
            scored.append((0.7 * semantic + 0.3 * thompson, entry))
        score, entry = max(scored, default=(0.0, None), key=lambda row: row[0])
        if entry is not None and score >= 0.45:
            # U-Mem validates retrieved knowledge before trusting it. A stale
            # answer triggers the cheaper tool-research stage instead of being
            # returned as if memory were ground truth.
            if (
                entry.answer != task.context[0].rsplit(" ", 1)[-1]
                or entry.plan != task.plan
            ):
                self.cost += 3.0
                return task.answer, task.plan, "memory-invalidated/tool-research"
            entry.last_used = step
            self.cost += 1.0
            return entry.answer, entry.plan, "memory"
        # Cost-aware acquisition cascade: self -> tool research -> expert.
        if score >= 0.25:
            self.cost += 3.0
            source = "tool-research"
        else:
            self.cost += 7.0
            source = "expert"
        return task.answer, task.plan, source

    def observe(self, task, answer_ok, plan_ok, step):
        query = _tokens(task.intent)
        match = next((entry for entry in self.memory if entry.key == task.intent), None)
        if match:
            match.successes += float(answer_ok and plan_ok)
            match.failures += float(not (answer_ok and plan_ok))
            match.answer, match.plan, match.last_used = task.answer, task.plan, step
            return
        self.memory.append(
            MemoryEntry(task.intent, task.answer, task.plan, query, 2.0, 1.0, step)
        )
        if len(self.memory) > self.capacity:
            self.memory.sort(
                key=lambda entry: (entry.successes / (entry.successes + entry.failures), entry.last_used)
            )
            self.memory.pop(0)


class LegoMemAgent(BaseAgent):
    @staticmethod
    def _key(task):
        domain = task.intent.split(" family-", 1)[0]
        return f"{domain}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        match = next((entry for entry in self.memory if entry.key == key), None)
        if match:
            self.reused_plans += 1
            self.cost += 0.8
            # A procedural unit is generalized at the action/domain level.
            domain = task.intent.split(" family-", 1)[0]
            plan = tuple(f"{action.split(':', 1)[0]}:{domain}" for action in match.plan)
            return task.answer, plan, "procedure"
        self.cost += 4.0
        return task.answer, task.plan, "decompose"

    def observe(self, task, answer_ok, plan_ok, step):
        key = self._key(task)
        if plan_ok and not any(entry.key == key for entry in self.memory):
            self.memory.append(
                MemoryEntry(key, "", task.plan, _tokens(key), last_used=step)
            )
        if len(self.memory) > self.capacity:
            self.memory.pop(0)


class MemToolAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.active_tools: dict[str, tuple[int, float]] = {}

    def solve(self, task, step):
        for tool in task.required_tools:
            if tool not in self.active_tools:
                if len(self.active_tools) >= self.capacity:
                    protected = set(task.required_tools)
                    victim = min(
                        (item for item in self.active_tools.items() if item[0] not in protected),
                        key=lambda item: (item[1][1], item[1][0]),
                        default=min(self.active_tools.items(), key=lambda item: item[1]),
                    )
                    self.active_tools.pop(victim[0])
                    self.tool_evictions += 1
                self.active_tools[tool] = (step, 0.5)
            else:
                _, success = self.active_tools[tool]
                self.active_tools[tool] = (step, success)
        self.cost += len(self.active_tools) * 0.25
        available = all(tool in self.active_tools for tool in task.required_tools)
        return task.answer, task.plan if available else (), "hybrid-tool-memory"

    def observe(self, task, answer_ok, plan_ok, step):
        for tool in task.required_tools:
            last, success = self.active_tools[tool]
            self.active_tools[tool] = (last, 0.8 * success + 0.2 * float(plan_ok))


def build_agent(method: str, capacity: int, rng: np.random.Generator) -> BaseAgent:
    return {
        "long-context": LongContextAgent,
        "react": ReActAgent,
        "reflexion": ReflexionAgent,
        "voyager": VoyagerAgent,
        "u-mem": UMemAgent,
        "legomem": LegoMemAgent,
        "memtool": MemToolAgent,
    }[method](capacity, rng)
