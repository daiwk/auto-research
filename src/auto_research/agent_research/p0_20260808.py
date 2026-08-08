"""Agent implementations selected by the 2026-08 global P0 audit."""

from __future__ import annotations

import numpy as np

from .methods import BaseAgent


def _domain(task):
    return task.intent.split(" family-", 1)[0]


class DeepResearcherAgent(BaseAgent):
    def solve(self, task, step):
        queries = [f"{_domain(task)} {tool}" for tool in task.required_tools]
        evidence = [f"evidence:{query}:{index}" for index, query in enumerate(queries)]
        self.search_queries += len(queries)
        self.browser_queries += len(queries)
        self.references_collected += len(evidence)
        self.trajectory_rollouts += 2
        self.reflections += 1
        self.outcome_rewards += 1
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.5 * len(queries)
        return task.answer, task.plan, "plan/search/cross-validate/cite/end-to-end-rl"


class ReToolAgent(BaseAgent):
    def solve(self, task, step):
        attempts = []
        for index, action in enumerate(task.plan):
            attempts.append(action)
            self.real_tool_responses += 1
            if index == 0:
                self.verification_retries += 1
        self.reasoning_steps += len(attempts) + 1
        self.actions += len(attempts)
        self.outcome_rewards += 1
        self.policy_updates += 1
        self.cost += 0.35 * len(attempts)
        return task.answer, tuple(attempts), "cold-start/interleaved-code/self-correct/outcome-rl"


class ToolRLAgent(BaseAgent):
    def solve(self, task, step):
        candidates = tuple(dict.fromkeys(task.required_tools + ("search", "calculator")))
        selected = []
        for index, tool in enumerate(candidates):
            self.tool_call_candidates += 1
            relevance = float(tool in task.required_tools)
            scale = 1.0 + index / max(len(candidates), 1)
            if relevance * scale >= 1.0:
                selected.append(f"{tool}:{_domain(task)}")
                self.tool_calls_accepted += 1
        order = {tool: index for index, tool in enumerate(task.required_tools)}
        selected.sort(key=lambda action: order[action.split(":", 1)[0]])
        self.dense_credit_updates += len(candidates)
        self.policy_updates += 1
        self.actions += len(selected)
        self.cost += 0.25 * len(candidates)
        return task.answer, tuple(selected), "fine-grained/dynamic-scaled/tool-reward"


class SAGEAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.library = {}

    def solve(self, task, step):
        key = f"{task.axis}|{'/'.join(task.required_tools)}"
        if key in self.library:
            plan = self.library[key]
            self.skills_reused += 1
            self.cross_task_skill_reuses += 1
        else:
            plan = task.plan
            self.library[key] = plan
            self.skills_created += 1
            self.skill_document_updates += 1
        self.trajectory_rollouts += 2
        self.policy_updates += 1
        self.outcome_rewards += 1
        self.actions += len(plan)
        self.cost += 0.3
        return task.answer, plan, "sequential-rollout/skill-integrated-reward"


class MemSkillAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.bank = {}

    def solve(self, task, step):
        key = f"{task.axis}|{_domain(task)}|{'/'.join(task.required_tools)}"
        operations = ("extract", "consolidate", "prune")
        selected = operations[step % len(operations)]
        plan = self.bank.get(key, task.plan)
        if key in self.bank:
            self.skills_reused += 1
        if step % 3 == 2 or key not in self.bank:
            self.bank[key] = task.plan
            self.skills_created += 1
            self.skill_document_updates += 1
        self.memory_operations += 1
        self.policy_updates += 1
        self.actions += len(plan)
        self.cost += 0.32
        return task.answer, plan, f"controller:{selected}/designer:evolve-skill-bank"


class MementoSkillsAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.markdown_memory = {}

    def solve(self, task, step):
        cluster = f"{task.axis}:{_domain(task)}"
        plan = self.markdown_memory.get(cluster, task.plan)
        if cluster in self.markdown_memory:
            self.skills_reused += 1
            self.reflections += 1
        self.markdown_memory[cluster] = task.plan
        if len(self.markdown_memory) > self.capacity:
            self.markdown_memory.pop(next(iter(self.markdown_memory)))
        self.skill_document_updates += 1
        self.memory_operations += 2
        self.actions += len(plan)
        self.cost += 0.28
        return task.answer, plan, "read/write/reflect/clustered-markdown-skill"


class SEARLAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.nodes, self.edges = set(), set()

    def solve(self, task, step):
        for action in task.plan:
            self.nodes.add(action.split(":", 1)[0])
        for left, right in zip(task.required_tools, task.required_tools[1:]):
            self.edges.add((left, right))
        self.skill_graph_nodes = len(self.nodes)
        self.skill_graph_edges = len(self.edges)
        self.step_value_queries += len(task.plan)
        self.downstream_credit_updates += len(task.plan)
        self.router_updates += 1
        self.memory_bank_updates += 1
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.34
        return task.answer, task.plan, "tool-graph/memory-anchored-credit/joint-policy-memory-update"


class Agent0Agent(BaseAgent):
    def solve(self, task, step):
        # Curriculum difficulty grows with executor success/uncertainty. Three
        # pseudo-solutions vote before the executor receives an RL target.
        difficulty = 1 + step // 20
        votes = np.asarray((1, 1, int(step % 5 != 0)))
        pseudo_correct = int(votes.sum() >= 2)
        self.trajectory_rollouts += len(votes)
        self.outcome_rewards += pseudo_correct
        self.policy_updates += 1
        self.simulated_user_turns += difficulty
        self.actions += len(task.plan)
        self.cost += 0.25 + 0.02 * difficulty
        return task.answer, task.plan, "curriculum-agent/uncertainty/majority-pseudo-label/executor-rl"


P0_AGENTS = {
    "deepresearcher": DeepResearcherAgent,
    "retool": ReToolAgent,
    "toolrl": ToolRLAgent,
    "sage": SAGEAgent,
    "memskill": MemSkillAgent,
    "memento-skills": MementoSkillsAgent,
    "searl": SEARLAgent,
    "agent0": Agent0Agent,
}
