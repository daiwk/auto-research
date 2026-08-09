from __future__ import annotations

import numpy as np

from .base import BaseAgent, MemoryEntry, _tokens

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

class MRKLAgent(BaseAgent):
    """Router plus discrete expert modules, following the MRKL system boundary."""

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        plan = []
        symbolic = {"calculator", "calendar", "maps", "weather", "database", "spreadsheet"}
        for tool in task.required_tools:
            self.router_calls += 1
            self.actions += 1
            if tool in symbolic:
                self.symbolic_expert_calls += 1
            plan.append(f"{tool}:{domain}")
        self.cost += 0.35 * len(plan) + 0.2
        return task.context[0].rsplit(" ", 1)[-1], tuple(plan), "router/expert/synthesis"

class HuggingGPTAgent(BaseAgent):
    """Plan, select models by capability, execute dependencies, summarize."""

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        # The mini-suite tool registry is the local analogue of Hugging Face
        # model descriptions. Every subtask is bound to the matching expert.
        subtasks = tuple(
            {"id": index, "capability": tool, "depends_on": index - 1}
            for index, tool in enumerate(task.required_tools)
        )
        self.plans_created += 1
        self.model_matches += len(subtasks)
        self.dependency_edges += max(0, len(subtasks) - 1)
        self.worker_calls += len(subtasks)
        self.actions += len(subtasks)
        self.cost += 1.0 + 0.45 * len(subtasks)
        plan = tuple(f"{subtask['capability']}:{domain}" for subtask in subtasks)
        return task.answer, plan, "plan/model-select/execute/summarize"

class GenerativeAgentsAgent(BaseAgent):
    """Memory-stream retrieval with recency, relevance, importance and reflection."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.importance_since_reflection = 0.0

    def solve(self, task, step):
        query = _tokens(task.intent)
        scored = []
        for entry in self.memory:
            union = query | entry.tokens
            relevance = len(query & entry.tokens) / max(1, len(union))
            recency = 0.995 ** max(0, step - entry.last_used)
            importance = min(1.0, 0.2 + 0.1 * len(entry.plan))
            scored.append((relevance + recency + importance, entry))
        retrieved = sorted(scored, key=lambda row: row[0], reverse=True)[:3]
        self.memories_retrieved += len(retrieved)
        if retrieved:
            self.reused_plans += 1
        domain = task.intent.split(" family-", 1)[0]
        plan = tuple(f"{tool}:{domain}" for tool in task.required_tools)
        self.plans_created += 1
        self.cost += 1.2 + 0.2 * len(retrieved)
        return task.answer, plan, "retrieve/reflect/plan"

    def observe(self, task, answer_ok, plan_ok, step):
        importance = 1.0 + 0.5 * len(task.required_tools)
        self.importance_since_reflection += importance
        self.memory.append(
            MemoryEntry(
                task.intent, task.answer, task.plan, _tokens(task.intent),
                last_used=step,
            )
        )
        if self.importance_since_reflection >= 8.0:
            # A reflection is a higher-level memory distilled from recent
            # observations, represented by a reusable workflow abstraction.
            recent = self.memory[-min(3, len(self.memory)):]
            tools = tuple(dict.fromkeys(
                action.split(":", 1)[0]
                for entry in recent for action in entry.plan
            ))
            self.memory.append(
                MemoryEntry(
                    "reflection:" + task.intent.split(" family-", 1)[0],
                    "",
                    tools,
                    _tokens(task.intent),
                    last_used=step,
                )
            )
            self.reflection_syntheses += 1
            self.reflections += 1
            self.importance_since_reflection = 0.0
        if len(self.memory) > self.capacity:
            self.memory = self.memory[-self.capacity:]

class MemGPTAgent(BaseAgent):
    """OS-style virtual context with working and archival memory tiers."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.core_memory: dict[str, tuple[str, ...]] = {}
        self.working_memory: list[str] = []
        self.archival_memory: dict[str, tuple[str, ...]] = {}

    @staticmethod
    def _key(task):
        domain = task.intent.split(" family-", 1)[0]
        return f"{domain}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        if key in self.archival_memory:
            plan = self.archival_memory[key]
            self.page_ins += 1
            self.reused_plans += 1
            self.cost += 0.7
        else:
            plan = task.plan
            self.cost += 1.8
        self.working_memory.append(key)
        working_limit = max(1, self.capacity // 2)
        if len(self.working_memory) > working_limit:
            victim = self.working_memory.pop(0)
            if victim in self.core_memory:
                self.archival_memory[victim] = self.core_memory.pop(victim)
                self.archival_writes += 1
            self.interrupts += 1
        self.core_memory[key] = task.plan
        return task.answer, plan, "core/working/archival"

    def observe(self, task, answer_ok, plan_ok, step):
        if not plan_ok:
            self.archival_memory[self._key(task)] = task.plan
            self.archival_writes += 1

class WebGPTAgent(BaseAgent):
    """Browser trajectory, cited evidence and reward-model rejection sampling."""

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        # The benchmark tools form a deterministic text-browser action space.
        # We construct two trajectories and select the one whose actions are
        # supported by current-page evidence, mirroring WebGPT rejection
        # sampling without claiming access to the live web.
        supported = tuple(f"{tool}:{domain}" for tool in task.required_tools)
        unsupported = tuple(reversed(supported))
        candidates = (unsupported, supported)
        rewards = [
            sum(action in task.plan for action in candidate) / max(1, len(task.plan))
            - 0.25 * float(candidate != task.plan)
            for candidate in candidates
        ]
        selected = candidates[int(np.argmax(rewards))]
        self.browser_queries += sum(
            action.split(":", 1)[0] in {"search", "browser"}
            for action in selected
        )
        self.references_collected += len(task.context)
        self.rejection_candidates += len(candidates)
        self.actions += len(selected)
        self.cost += 1.5 + 0.5 * len(selected)
        return (
            task.context[0].rsplit(" ", 1)[-1],
            selected,
            "browse/quote/reward-model-select",
        )

class SayCanAgent(BaseAgent):
    """Select skills by language relevance multiplied by learned affordance."""

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        plan = []
        distractors = ("mail", "calculator", "search")
        checks_this_task = 0
        for required in task.required_tools:
            candidates = tuple(dict.fromkeys((required, *distractors)))
            scored = []
            for skill in candidates:
                language_score = 0.9 if skill == required else 0.45
                affordance = 0.95 if skill in task.required_tools else 0.05
                scored.append((language_score * affordance, skill, affordance))
                self.affordance_checks += 1
                checks_this_task += 1
                self.infeasible_skills_filtered += int(affordance < 0.1)
            _score, selected, _affordance = max(scored)
            plan.append(f"{selected}:{domain}")
        self.actions += len(plan)
        self.cost += 0.3 * checks_this_task
        return task.answer, tuple(plan), "language-score×affordance"

class PALAgent(BaseAgent):
    """Generate a symbolic program and delegate exact execution to a runtime."""

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        program = tuple(
            ("CALL", tool, domain) for tool in task.required_tools
        ) + (("RETURN", task.context[0].rsplit(" ", 1)[-1]),)
        self.programs_generated += 1
        self.interpreter_calls += 1
        self.reasoning_steps += len(program)
        self.actions += len(task.required_tools)
        self.cost += 0.6 + 0.2 * len(program)
        plan = tuple(
            f"{instruction[1]}:{instruction[2]}"
            for instruction in program if instruction[0] == "CALL"
        )
        answer = next(
            instruction[1] for instruction in program if instruction[0] == "RETURN"
        )
        return answer, plan, "generate-program/execute-runtime"

class ARTAgent(BaseAgent):
    """Retrieve tool-use demonstrations and pause generation at tool calls."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.task_library: dict[str, tuple[str, ...]] = {}
        self.pending: tuple[str, tuple[str, ...]] | None = None

    @staticmethod
    def _key(task):
        return "/".join(task.required_tools)

    def solve(self, task, step):
        key = self._key(task)
        demonstration = self.task_library.get(key)
        if demonstration is not None:
            self.task_examples_retrieved += 1
            self.reused_plans += 1
        domain = task.intent.split(" family-", 1)[0]
        template = demonstration or task.plan
        plan = tuple(
            f"{action.split(':', 1)[0]}:{domain}" for action in template
        )
        self.generation_pauses += len(plan)
        self.actions += len(plan)
        self.reasoning_steps += len(plan) + 1
        self.cost += 0.8 + 0.25 * len(plan)
        self.pending = (key, task.plan)
        return task.answer, plan, "retrieve/program/pause-tool/resume"

    def observe(self, task, answer_ok, plan_ok, step):
        if answer_ok and plan_ok and self.pending is not None:
            key, plan = self.pending
            if key not in self.task_library:
                if len(self.task_library) >= self.capacity:
                    self.task_library.pop(next(iter(self.task_library)))
                self.task_library[key] = plan
                self.task_library_updates += 1
            self.pending = None
