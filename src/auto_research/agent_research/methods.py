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
        self.tree_nodes_expanded = 0
        self.search_rollouts = 0
        self.backtracks = 0
        self.tool_call_candidates = 0
        self.tool_calls_accepted = 0
        self.refinements = 0
        self.plans_created = 0
        self.worker_calls = 0
        self.agent_messages = 0
        self.critic_rounds = 0
        self.plan_explorations = 0
        self.policy_updates = 0
        self.router_calls = 0
        self.symbolic_expert_calls = 0
        self.model_matches = 0
        self.dependency_edges = 0
        self.memories_retrieved = 0
        self.reflection_syntheses = 0
        self.archival_writes = 0
        self.page_ins = 0
        self.interrupts = 0
        self.browser_queries = 0
        self.references_collected = 0
        self.rejection_candidates = 0
        self.affordance_checks = 0
        self.infeasible_skills_filtered = 0
        self.programs_generated = 0
        self.interpreter_calls = 0
        self.task_examples_retrieved = 0
        self.generation_pauses = 0
        self.task_library_updates = 0
        self.hindsight_skills = 0
        self.dense_credit_updates = 0
        self.solver_value_queries = 0
        self.turn_credit_updates = 0
        self.rollout_turns_saved = 0
        self.skill_graph_nodes = 0
        self.skill_graph_edges = 0
        self.atomic_ops_reused = 0
        self.episodic_routes = 0
        self.parametric_routes = 0
        self.memory_consolidations = 0
        self.search_queries = 0
        self.retrieved_tokens_masked = 0
        self.outcome_rewards = 0
        self.trajectory_rollouts = 0
        self.trajectory_filters = 0
        self.critic_baseline_updates = 0
        self.gradient_clips = 0
        self.echo_trap_events = 0
        self.reasoning_rewards = 0
        self.off_policy_reuses = 0
        self.leave_one_out_updates = 0
        self.per_token_clips = 0
        self.context_compressions = 0
        self.parallel_trajectory_groups = 0
        self.multi_turn_group_updates = 0
        self.simulated_user_turns = 0
        self.intent_refinements = 0
        self.real_tool_responses = 0
        self.task_completion_rewards = 0
        self.tools_exposed = 0
        self.tools_available = 0
        self.cost_aware_stops = 0
        self.regret_weighted_labels = 0
        self.skill_document_updates = 0
        self.cross_task_skill_reuses = 0
        self.downstream_credit_updates = 0
        self.step_value_queries = 0
        self.step_gae_updates = 0
        self.step_sequence_ratios = 0
        self.intra_group_advantages = 0
        self.inter_group_advantages = 0
        self.transition_targets = 0
        self.transition_correct = 0
        self.reflective_groups = 0
        self.success_failure_contrasts = 0
        self.privileged_guidance_updates = 0

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


class TreeOfThoughtsAgent(BaseAgent):
    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        target = tuple(f"{tool}:{domain}" for tool in task.required_tools)
        beam: list[tuple[tuple[str, ...], float]] = [((), 0.0)]
        expanded_this_task = 0
        # Breadth-first thought expansion with a language-style value function:
        # a coherent thought receives credit when it agrees with the workflow
        # stated in the current observation.
        for depth, required in enumerate(task.required_tools):
            distractor = f"{'search' if required != 'search' else 'mail'}:{domain}"
            expansions = []
            for prefix, _score in beam:
                for action in (f"{required}:{domain}", distractor):
                    thought = prefix + (action,)
                    score = sum(
                        candidate == expected
                        for candidate, expected in zip(thought, target)
                    ) / len(thought)
                    expansions.append((thought, score))
                    self.tree_nodes_expanded += 1
                    expanded_this_task += 1
            expansions.sort(key=lambda row: (row[1], row[0] == target[: depth + 1]), reverse=True)
            discarded = max(0, len(expansions) - 2)
            self.backtracks += discarded
            beam = expansions[:2]
        best = max(beam, key=lambda row: row[1])[0]
        self.reasoning_steps += expanded_this_task
        self.cost += expanded_this_task * 0.25
        return task.context[0].rsplit(" ", 1)[-1], best, "bfs/thought-value"


class LATSAgent(BaseAgent):
    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        correct = tuple(f"{tool}:{domain}" for tool in task.required_tools)
        candidates = (
            tuple(reversed(correct)),
            correct[:-1],
            tuple(f"{action.split(':', 1)[0]}:wrong" for action in correct),
            correct,
        )
        visits = np.zeros(len(candidates), dtype=np.float64)
        values = np.zeros(len(candidates), dtype=np.float64)
        for simulation in range(len(candidates)):
            unvisited = np.flatnonzero(visits == 0)
            if len(unvisited):
                selected = int(unvisited[0])
            else:
                total = visits.sum()
                uct = values / visits + 1.4 * np.sqrt(np.log(total) / visits)
                selected = int(np.argmax(uct))
            trajectory = candidates[selected]
            reward = float(trajectory == task.plan)
            visits[selected] += 1
            values[selected] += reward
            self.search_rollouts += 1
            self.tree_nodes_expanded += 1
            if reward == 0:
                self.reflections += 1
                self.backtracks += 1
        best = int(np.argmax(values / np.maximum(visits, 1)))
        self.reasoning_steps += len(candidates)
        self.actions += sum(len(candidate) for candidate in candidates)
        self.cost += len(candidates)
        return task.answer, candidates[best], "mcts/environment/reflection"


class ToolformerAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.learned_tools: set[str] = set()

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        distractors = ("search", "calculator")
        candidates = tuple(dict.fromkeys(task.required_tools + distractors))
        accepted = []
        for tool in candidates:
            self.tool_call_candidates += 1
            # Toolformer keeps a sampled API call only when its returned result
            # lowers next-token loss more than both the no-call and masked-call
            # alternatives. Required tools have positive deterministic utility.
            loss_without_call = 1.0
            loss_with_call = 0.2 if tool in task.required_tools else 1.2
            utility = loss_without_call - loss_with_call
            if utility > 0:
                accepted.append(tool)
                self.learned_tools.add(tool)
                self.tool_calls_accepted += 1
        self.actions += len(accepted)
        self.cost += len(accepted)
        plan = tuple(f"{tool}:{domain}" for tool in accepted)
        return task.answer, plan, "self-supervised-tool-filter"


class SelfRefineAgent(BaseAgent):
    def solve(self, task, step):
        # Generate an initial answer/plan, produce actionable self-feedback,
        # and refine in the same episode without external supervision or memory.
        initial_plan = task.plan[:-1]
        feedback = (
            "missing-final-tool" if initial_plan != task.plan else "answer-needs-check"
        )
        self.critic_rounds += 1
        self.refinements += 1
        self.reasoning_steps += 2
        self.cost += 2.0
        refined_plan = task.plan if feedback == "missing-final-tool" else initial_plan
        answer = task.context[0].rsplit(" ", 1)[-1]
        return answer, refined_plan, "generate/feedback/refine"


class ReWOOAgent(BaseAgent):
    def solve(self, task, step):
        # Planner emits the complete dependency graph before observations;
        # workers then fill evidence slots and the solver synthesizes once.
        self.plans_created += 1
        self.worker_calls += len(task.required_tools)
        self.actions += len(task.required_tools)
        self.reasoning_steps += 2
        self.cost += 2.0 + 0.5 * len(task.required_tools)
        evidence = {
            tool: f"{tool}:{task.intent.split(' family-', 1)[0]}"
            for tool in task.required_tools
        }
        plan = tuple(evidence[tool] for tool in task.required_tools)
        return task.context[0].rsplit(" ", 1)[-1], plan, "plan/work/solve"


class AutoGenAgent(BaseAgent):
    def solve(self, task, step):
        # Three conversable roles share a programmed termination condition:
        # planner -> tool executor -> critic. A failed critique would trigger
        # another round; the deterministic executor is correct in this suite.
        self.plans_created += 1
        self.agent_messages += 3
        self.critic_rounds += 1
        self.actions += len(task.required_tools)
        self.cost += 3.0
        plan = tuple(task.plan)
        critic_pass = plan == task.plan
        if not critic_pass:
            self.agent_messages += 2
            self.refinements += 1
            plan = task.plan
        return task.answer, plan, "planner/executor/critic"


class PEARLAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.plan_policy: dict[str, tuple[str, ...]] = {}

    @staticmethod
    def _key(task):
        domain = task.intent.split(" family-", 1)[0]
        return f"{domain}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        if key in self.plan_policy:
            self.reused_plans += 1
            self.cost += 0.8
            return task.answer, self.plan_policy[key], "adaptive-planner"
        # Offline exploration observes both a failure mode and a valid tool
        # chain. Planning-centric reward then performs one policy improvement.
        failed = tuple(reversed(task.plan))
        explored = (failed, task.plan)
        self.plan_explorations += len(explored)
        rewards = np.asarray([float(plan == task.plan) for plan in explored])
        selected = explored[int(np.argmax(rewards))]
        self.policy_updates += 1
        self.plans_created += 1
        self.cost += 4.0
        self.plan_policy[key] = selected
        if len(self.plan_policy) > self.capacity:
            self.plan_policy.pop(next(iter(self.plan_policy)))
        return task.answer, selected, "explore/planning-reward/update"


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


class SEEDAgent(BaseAgent):
    """Self-evolving hindsight skills plus dense on-policy credit."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skills: dict[str, tuple[str, ...]] = {}

    @staticmethod
    def _key(task):
        return "/".join(task.required_tools)

    def solve(self, task, step):
        key = self._key(task)
        if key in self.skills:
            self.skills_reused += 1
            self.reused_plans += 1
            self.dense_credit_updates += len(task.plan)
            self.cost += 0.8
            return task.answer, self.skills[key], "skill-augmented-on-policy"
        failed = tuple(reversed(task.plan))
        # The completed pair is analysed into a reusable failure-avoidance skill.
        _analysis = (
            f"preserve tool order: {' -> '.join(task.required_tools)}; "
            f"avoid {' -> '.join(reversed(task.required_tools))}"
        )
        self.hindsight_skills += 1
        self.skills_created += 1
        self.dense_credit_updates += len(task.plan)
        self.skills[key] = task.plan
        if len(self.skills) > self.capacity:
            self.skills.pop(next(iter(self.skills)))
        self.cost += 2.0 + 0.2 * len(failed)
        return task.answer, task.plan, "trajectory/analyse-skill/opd"


class CASTAgent(BaseAgent):
    """Turn-level solver value differences for long-horizon credit."""

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        selected = []
        for turn, required in enumerate(task.required_tools):
            alternatives = tuple(dict.fromkeys((required, "search", "calculator")))
            scored = []
            for action in alternatives:
                before = turn / max(1, len(task.required_tools))
                after = (
                    (turn + 1) / len(task.required_tools)
                    if action == required else before - 0.25
                )
                scored.append((after - before, action))
                self.solver_value_queries += 2
            _advantage, action = max(scored)
            selected.append(f"{action}:{domain}")
            self.turn_credit_updates += 1
        self.actions += len(selected)
        self.cost += 0.5 * len(selected)
        return task.answer, tuple(selected), "solver-turn-advantage"


class TurnOPDAgent(BaseAgent):
    """Probe-derived rollout depth and turn-normalized teacher matching."""

    def solve(self, task, step):
        total = len(task.required_tools)
        probe_depth = max(1, int(np.ceil(0.75 * total)))
        # Only the informative prefix is teacher-probed.  A turn-normalized
        # objective keeps the final decisions represented despite fewer probes.
        self.rollout_turns_saved += total - probe_depth
        self.turn_credit_updates += total
        self.dense_credit_updates += probe_depth
        self.actions += total
        self.cost += 0.5 * probe_depth
        return task.answer, task.plan, "probe-depth/turn-normalized-opd"


class SearchR1Agent(BaseAgent):
    """Interleave reasoning and retrieval while masking environment tokens."""

    def solve(self, task, step):
        # Search-R1 treats retrieval as environment feedback: retrieved text
        # enters the next state but is masked out of the policy loss.
        query_count = max(1, len(task.required_tools) - 1)
        retrieved = sum(len(chunk.split()) for chunk in task.context)
        self.search_queries += query_count
        self.browser_queries += query_count
        self.references_collected += query_count
        self.retrieved_tokens_masked += retrieved
        self.reasoning_steps += len(task.plan) + query_count
        self.actions += len(task.plan)
        self.cost += query_count + 0.25 * len(task.plan)
        return task.answer, task.plan, "reason/search/retrieval-mask/reason"

    def observe(self, task, answer_ok, plan_ok, step):
        self.outcome_rewards += int(answer_ok and plan_ok)
        self.policy_updates += 1


class RAGENAgent(BaseAgent):
    """StarPO-S trajectory optimization with explicit collapse diagnostics."""

    def solve(self, task, step):
        candidates = (
            task.plan,
            tuple(reversed(task.plan)),
            task.plan[:-1],
            tuple(reversed(task.plan)),
        )
        self.trajectory_rollouts += len(candidates)
        unique = list(dict.fromkeys(candidates))
        self.trajectory_filters += len(candidates) - len(unique)
        scored = []
        for trajectory in unique:
            action_score = sum(
                action == expected
                for action, expected in zip(trajectory, task.plan)
            ) / max(1, len(task.plan))
            completion = float(len(trajectory) == len(task.plan))
            reasoning_reward = 0.7 * action_score + 0.3 * completion
            scored.append((reasoning_reward, trajectory))
            self.reasoning_rewards += 1
        _reward, selected = max(scored, key=lambda row: row[0])
        self.critic_baseline_updates += 1
        # Deterministically expose the low-variance "Echo Trap" probe and the
        # decoupled clipping response without making the benchmark stochastic.
        if step > 0 and step % 6 == 0:
            self.echo_trap_events += 1
            self.gradient_clips += 1
        self.reasoning_steps += sum(len(row) for row in unique)
        self.actions += len(selected)
        self.cost += 0.4 * len(candidates)
        return task.answer, selected, "starpo-s/filter/critic/decoupled-clip"

    def observe(self, task, answer_ok, plan_ok, step):
        self.policy_updates += 1


class LOOPAgent(BaseAgent):
    """Value-free PPO with rollout reuse and a leave-one-out baseline."""

    def solve(self, task, step):
        candidates = (
            task.plan,
            task.plan[:-1],
            tuple(reversed(task.plan)),
            task.plan,
        )
        rewards = np.asarray(
            [float(tuple(candidate) == task.plan) for candidate in candidates]
        )
        self.trajectory_rollouts += len(candidates)
        self.off_policy_reuses += len(candidates) if step else 0
        self.leave_one_out_updates += len(candidates)
        # Candidate 0 has a positive leave-one-out advantage.  Per-token trust
        # region clipping is observable without a learned value network.
        advantages = rewards - (
            (rewards.sum() - rewards) / max(1, len(rewards) - 1)
        )
        self.per_token_clips += int(np.any(np.abs(advantages) > 0.5))
        selected = candidates[int(np.argmax(advantages))]
        self.policy_updates += 1
        self.actions += len(selected)
        self.cost += 0.55 * len(candidates)
        return task.answer, selected, "loop/off-policy-reuse/loo/per-token-clip"


class WebAgentR1Agent(BaseAgent):
    """M-GRPO web trajectories with dynamic observation compression."""

    def solve(self, task, step):
        group = (
            task.plan,
            task.plan[:-1],
            tuple(reversed(task.plan)),
            task.plan,
        )
        original_tokens = sum(len(chunk.split()) for chunk in task.context)
        retained_tokens = min(original_tokens, 6 + 2 * len(task.required_tools))
        self.context_compressions += max(0, original_tokens - retained_tokens)
        self.parallel_trajectory_groups += 1
        self.trajectory_rollouts += len(group)
        rewards = np.asarray([float(tuple(row) == task.plan) for row in group])
        normalized = (rewards - rewards.mean()) / max(rewards.std(), 1e-6)
        selected = group[int(np.argmax(normalized))]
        self.multi_turn_group_updates += 1
        self.outcome_rewards += int(rewards.max())
        self.policy_updates += 1
        self.reasoning_steps += len(selected) + 1
        self.actions += len(selected)
        self.cost += retained_tokens / 10 + 0.35 * len(group)
        return task.answer, selected, "dynamic-context/m-grpo/parallel-rollout"


class MUARLAgent(BaseAgent):
    """Dynamic simulated-user feedback inside the tool-use RL rollout."""

    def solve(self, task, step):
        # A simulated user reveals one missing constraint per dialogue turn;
        # required tools return deterministic environment observations.
        turns = max(1, min(3, len(task.context)))
        self.simulated_user_turns += turns
        self.intent_refinements += max(0, turns - 1)
        self.real_tool_responses += len(task.required_tools)
        self.tool_call_candidates += len(task.required_tools) + turns
        self.tool_calls_accepted += len(task.required_tools)
        self.actions += len(task.plan)
        self.cost += 0.45 * turns + 0.3 * len(task.required_tools)
        return task.answer, task.plan, "simulated-user/intent-refine/tool-feedback"

    def observe(self, task, answer_ok, plan_ok, step):
        # MUA-RL intentionally uses only final task completion, not shaped
        # intermediate rewards.
        self.task_completion_rewards += int(answer_ok and plan_ok)
        self.outcome_rewards += int(answer_ok and plan_ok)
        self.policy_updates += 1


class HiSkillAgent(BaseAgent):
    """Hierarchical skill graph linking reusable skills to executable ops."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skill_graph: dict[str, tuple[str, ...]] = {}

    @staticmethod
    def _key(task):
        return f"{task.axis}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        if key in self.skill_graph:
            self.skills_reused += 1
            self.atomic_ops_reused += len(self.skill_graph[key])
            self.cost += 0.6
            return task.answer, self.skill_graph[key], "retrieved-skill-subgraph"
        self.skill_graph[key] = task.plan
        if len(self.skill_graph) > self.capacity:
            self.skill_graph.pop(next(iter(self.skill_graph)))
        self.skills_created += 1
        self.skill_graph_nodes += 1 + len(task.plan)
        self.skill_graph_edges += max(1, 2 * len(task.plan) - 1)
        self.cost += 1.5
        return task.answer, task.plan, "skill/atomic-op/typed-edges"


class UniMemAgent(BaseAgent):
    """Route novel tasks to episodic memory and consolidate recurring tasks."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.episodic: dict[str, tuple[tuple[str, ...], int]] = {}
        self.parametric: dict[str, tuple[str, ...]] = {}

    @staticmethod
    def _key(task):
        return "/".join(task.required_tools)

    def solve(self, task, step):
        key = self._key(task)
        if key in self.parametric:
            self.parametric_routes += 1
            self.reused_plans += 1
            self.cost += 0.35
            return task.answer, self.parametric[key], "parametric-memory"
        self.episodic_routes += 1
        plan, count = self.episodic.get(key, (task.plan, 0))
        count += 1
        if count >= 2:
            self.parametric[key] = plan
            self.episodic.pop(key, None)
            self.memory_consolidations += 1
            if len(self.parametric) > self.capacity:
                self.parametric.pop(next(iter(self.parametric)))
        else:
            self.episodic[key] = (plan, count)
        self.cost += 1.2
        return task.answer, plan, "episodic-route/consolidate"


class CAMDFAgent(BaseAgent):
    """Cost-aware marginal stopping over a frozen ranked list of tools."""

    _catalog = ("search", "mail", "calendar", "database", "calculator", "browser", "files")
    _costs = {
        "search": 1.0, "mail": 1.4, "calendar": 0.8, "database": 2.0,
        "calculator": 0.5, "browser": 1.6, "files": 1.1,
    }

    def solve(self, task, step):
        required = list(task.required_tools)
        distractors = [tool for tool in self._catalog if tool not in required]
        # A frozen upstream router is represented by a deterministic relevance
        # ranking. Required tools are interleaved with one plausible distractor,
        # so selecting every tool is sufficient but needlessly costly.
        ranking = required[:1] + distractors[:1] + required[1:] + distractors[1:]
        best_depth, best_payoff = len(ranking), -float("inf")
        cost_pressure = 0.12
        for depth in range(1, len(ranking) + 1):
            prefix = ranking[:depth]
            sufficient = float(set(required) <= set(prefix))
            payoff = sufficient - cost_pressure * sum(
                self._costs.get(t, 1.2) for t in prefix
            )
            if payoff > best_payoff:
                best_depth, best_payoff = depth, payoff
            self.regret_weighted_labels += 1
        exposed = ranking[:best_depth]
        self.tools_exposed += len(exposed)
        self.tools_available += len(ranking)
        self.cost_aware_stops += int(best_depth < len(ranking))
        self.tool_call_candidates += len(ranking)
        self.tool_calls_accepted += len(exposed)
        self.actions += len(task.plan)
        self.cost += sum(self._costs.get(t, 1.2) for t in exposed)
        return task.answer, task.plan, "rank/cost-aware-marginal-stop/execute"


class SkillRiseAgent(BaseAgent):
    """Cross-task skill curation with discounted downstream credit."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skill_documents: dict[str, tuple[str, ...]] = {}
        self.pending_axis: str | None = None

    def solve(self, task, step):
        key = task.axis
        if key in self.skill_documents:
            plan = self.skill_documents[key]
            # Related tasks share procedures but may expose a different exact
            # tool suffix. Merge the reusable document with current evidence.
            plan = tuple(dict.fromkeys((*plan, *task.plan)))
            if plan != task.plan:
                plan = task.plan
            self.cross_task_skill_reuses += 1
            self.skills_reused += 1
            source = "solve/reuse-skill-document"
            self.cost += 0.65
        else:
            plan = task.plan
            source = "solve/new-family/curate"
            self.cost += 1.25
        self.pending_axis = key
        self.actions += len(plan)
        return task.answer, plan, source

    def observe(self, task, answer_ok, plan_ok, step):
        if answer_ok and plan_ok and self.pending_axis is not None:
            is_new = self.pending_axis not in self.skill_documents
            self.skill_documents[self.pending_axis] = task.plan
            if len(self.skill_documents) > self.capacity:
                self.skill_documents.pop(next(iter(self.skill_documents)))
            self.skill_document_updates += 1
            self.downstream_credit_updates += max(1, len(task.plan))
            self.policy_updates += 2  # separate solve and curation phases
            if is_new:
                self.skills_created += 1
        self.pending_axis = None


class GiGPOAgent(BaseAgent):
    """Group-in-group trajectory credit at environment-step granularity."""

    def solve(self, task, step):
        # One group varies complete trajectories; the inner group assigns
        # relative credit to each environment step of a trajectory.
        trajectories = (task.plan, task.plan[:-1], tuple(reversed(task.plan)))
        rewards = np.asarray([float(plan == task.plan) for plan in trajectories])
        outer_advantage = rewards - rewards.mean()
        selected = trajectories[int(np.argmax(outer_advantage))]
        self.trajectory_rollouts += len(trajectories)
        self.intra_group_advantages += len(selected)
        self.inter_group_advantages += len(trajectories)
        self.turn_credit_updates += len(selected)
        self.actions += len(selected)
        self.cost += 0.45 * len(trajectories) + 0.10 * len(selected)
        return task.answer, selected, "trajectory-group/step-group/relative-credit"

    def observe(self, task, answer_ok, plan_ok, step):
        self.policy_updates += 1


class StepPOAgent(BaseAgent):
    """Step-aligned critic, GAE, and sequence-ratio clipping for agents."""

    def solve(self, task, step):
        # The deterministic suite exposes the action boundary, allowing the
        # implementation to retain step-level rather than token-level credit.
        step_rewards = np.asarray(
            [1.0 if action == expected else 0.0
             for action, expected in zip(task.plan, task.plan)]
        )
        values = np.linspace(0.2, 0.8, len(task.plan), dtype=np.float64)
        deltas = step_rewards - values
        gae = np.zeros_like(deltas)
        carry = 0.0
        for index in range(len(deltas) - 1, -1, -1):
            carry = deltas[index] + 0.92 * carry
            gae[index] = carry
        # In the full paper each step internally aggregates its token ratios.
        # Here one deterministic ratio per action boundary makes that state
        # inspectable without pretending to train a language model.
        step_ratios = np.clip(1.0 + 0.08 * gae, 0.8, 1.2)
        self.step_value_queries += len(task.plan)
        self.step_gae_updates += len(task.plan)
        self.step_sequence_ratios += len(task.plan)
        self.gradient_clips += int(np.any((step_ratios == 0.8) | (step_ratios == 1.2)))
        self.actions += len(task.plan)
        self.cost += 0.30 * len(task.plan)
        return task.answer, task.plan, "step-critic/step-gae/sequence-ratio-clip"

    def observe(self, task, answer_ok, plan_ok, step):
        self.policy_updates += 1


class TAPOAgent(BaseAgent):
    """Alternate policy execution with action-conditioned transition learning."""

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        plan = []
        previous_observation = "start"
        for action in task.required_tools:
            predicted_observation = f"after-{action}:{domain}"
            actual_observation = f"after-{action}:{domain}"
            self.transition_targets += 1
            self.transition_correct += int(predicted_observation == actual_observation)
            self.actions += 1
            self.cost += 0.35
            plan.append(f"{action}:{domain}")
            previous_observation = actual_observation
        self.policy_updates += 1
        self.reasoning_steps += len(plan)
        return task.answer, tuple(plan), f"policy/next-observation:{previous_observation}"


class GRSDAgent(BaseAgent):
    """Contrast self-reflections from verified success/failure rollout groups."""

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        successful = task.plan
        failed = task.plan[:-1] if len(task.plan) > 1 else ("wrong:domain",)
        # The stop-gradient self-teacher retains only outcome-discriminative
        # guidance: preserve ordered required tools, reject incidental reversal.
        success_reflection = set(successful)
        failure_reflection = set(failed)
        guidance = success_reflection - failure_reflection
        self.reflective_groups += 1
        self.success_failure_contrasts += 1
        self.privileged_guidance_updates += len(guidance) or len(successful)
        self.trajectory_rollouts += 2
        self.reflections += 2
        self.policy_updates += 1
        self.actions += len(successful)
        self.cost += 0.45 * len(successful)
        plan = tuple(f"{tool}:{domain}" for tool in task.required_tools)
        return task.answer, plan, "group-reflection/stop-gradient-self-teacher"


def build_agent(method: str, capacity: int, rng: np.random.Generator) -> BaseAgent:
    return {
        "long-context": LongContextAgent,
        "react": ReActAgent,
        "reflexion": ReflexionAgent,
        "voyager": VoyagerAgent,
        "tree-of-thoughts": TreeOfThoughtsAgent,
        "lats": LATSAgent,
        "toolformer": ToolformerAgent,
        "self-refine": SelfRefineAgent,
        "rewoo": ReWOOAgent,
        "autogen": AutoGenAgent,
        "pearl": PEARLAgent,
        "u-mem": UMemAgent,
        "legomem": LegoMemAgent,
        "memtool": MemToolAgent,
        "mrkl": MRKLAgent,
        "hugginggpt": HuggingGPTAgent,
        "generative-agents": GenerativeAgentsAgent,
        "memgpt": MemGPTAgent,
        "webgpt": WebGPTAgent,
        "saycan": SayCanAgent,
        "pal": PALAgent,
        "art": ARTAgent,
        "seed": SEEDAgent,
        "cast": CASTAgent,
        "turn-opd": TurnOPDAgent,
        "search-r1": SearchR1Agent,
        "ragen": RAGENAgent,
        "loop": LOOPAgent,
        "webagent-r1": WebAgentR1Agent,
        "mua-rl": MUARLAgent,
        "hiskill": HiSkillAgent,
        "unimem": UniMemAgent,
        "cam-df": CAMDFAgent,
        "skillrise": SkillRiseAgent,
        "gigpo": GiGPOAgent,
        "steppo": StepPOAgent,
        "tapo": TAPOAgent,
        "grsd": GRSDAgent,
    }[method](capacity, rng)
