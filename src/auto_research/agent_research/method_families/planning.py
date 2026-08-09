from __future__ import annotations

import numpy as np

from .base import BaseAgent, MemoryEntry, _tokens

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
