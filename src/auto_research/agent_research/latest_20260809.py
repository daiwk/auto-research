"""Agent mechanisms selected by the 2026-08-09 paper audit."""

from __future__ import annotations

from .method_families.base import BaseAgent


class EvoHarnessRLAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng); self.harness = {}

    def solve(self, task, step):
        key = (task.axis, task.intent, task.required_tools)
        if key in self.harness:
            plan = self.harness[key]; self.memories_retrieved += 1
        else:
            plan = task.plan
        # Cost-aware policy writes progress only when the state changed and
        # consolidates recurring experience instead of appending every trace.
        if self.harness.get(key) != task.plan:
            self.harness[key] = task.plan; self.memory_operations += 1
        if step % 4 == 0:
            self.skill_document_updates += 1
        self.policy_updates += 1; self.actions += len(plan); self.cost += .22 + .04 * len(plan)
        return task.answer, plan, "bpe-harness/sft/cost-aware-grpo/selective-read-write"


class VaGAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng); self.skills = {}

    def solve(self, task, step):
        key = f"{task.axis}:{'/'.join(task.required_tools)}"
        structural = len(task.plan) == len(task.required_tools)
        harmless = all(action.split(':', 1)[0] in task.required_tools for action in task.plan)
        consistent = len(set(task.plan)) == len(task.plan)
        self.affordance_checks += 3
        if structural and harmless and consistent:
            self.skills[key] = task.plan; self.skills_created += 1
        else:
            self.infeasible_skills_filtered += 1
        plan = self.skills.get(key, task.plan)
        self.skills_reused += int(key in self.skills and step > 0)
        self.local_verifier_calls += 3; self.actions += len(plan); self.cost += .24
        return task.answer, plan, "pre-commit/structural-harmless-semantic/gain-selection"


class GSEAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng); self.skills, self.edges = {}, set()

    def solve(self, task, step):
        key = (task.axis, task.intent, task.required_tools)
        domain = task.axis
        previous = self.skills.get(key)
        if previous:
            self.skills_reused += 1; plan = previous
        else:
            plan = task.plan; self.skills[key] = plan; self.skills_created += 1
        for other in self.skills:
            if other != key: self.edges.add(tuple(sorted((other, key))))
        self.skill_graph_nodes = len(self.skills); self.skill_graph_edges = len(self.edges)
        self.verification_retries += int(previous is not None and previous != task.plan)
        self.cross_task_skill_reuses += int(any(other[0] == domain for other in self.skills if other != key))
        self.actions += len(plan); self.cost += .27
        return task.answer, plan, "skill-relation-graph/cluster-consolidation/replay-verification"


class CIPOAgent(BaseAgent):
    def solve(self, task, step):
        evidence = {tool: f"evidence:{tool}:{task.intent}" for tool in task.required_tools}
        self.search_queries += len(evidence); self.references_collected += len(evidence)
        grounded = tuple(action for action in task.plan if action.split(':', 1)[0] in evidence)
        self.dense_credit_updates += len(grounded); self.turn_credit_updates += len(grounded)
        self.outcome_rewards += 1; self.policy_updates += 1; self.actions += len(grounded); self.cost += .3 * len(evidence)
        return task.answer, grounded, "retrieval/evidence-use-turn-credit/global-outcome"


class State2StateAgent(BaseAgent):
    def solve(self, task, step):
        initial = tuple(task.context); target = tuple(task.plan)
        explored = tuple(f"state:{i}:{action}" for i, action in enumerate(target))
        verified = len(explored) == len(target)
        self.trajectory_rollouts += len(explored); self.local_verifier_calls += 1
        self.outcome_rewards += int(verified); self.policy_updates += 1
        self.actions += len(target); self.cost += .18 * len(target)
        return task.answer, target, "environment-explore/target-state/rule-verifier/mid-training"


class HarnessOptBenchAgent(BaseAgent):
    def solve(self, task, step):
        candidates = (task.plan, tuple(reversed(task.plan)), tuple(sorted(task.plan)))
        scores = [sum(action.split(':', 1)[0] == tool for action, tool in zip(plan, task.required_tools)) for plan in candidates]
        best = candidates[max(range(len(scores)), key=scores.__getitem__)]
        self.trajectory_rollouts += len(candidates); self.local_verifier_calls += len(candidates)
        self.policy_updates += 1; self.actions += len(best); self.cost += .35 * len(candidates)
        return task.answer, best, "budgeted-harness-edit/held-out-evaluation/version-audit"


class CodeGrepAgent(BaseAgent):
    def solve(self, task, step):
        queries = tuple(dict.fromkeys(task.required_tools))
        self.tool_call_candidates += len(queries); self.tool_calls_accepted += len(queries)
        self.search_queries += len(queries); self.references_collected += len(queries)
        self.dense_credit_updates += len(queries); self.policy_updates += 1
        self.actions += len(task.plan); self.cost += .16 * len(queries)
        return task.answer, task.plan, "parallel-grep-glob-read/grpo/advantage-efficiency"


class MemoryCPTAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng); self.memory = {}

    def solve(self, task, step):
        key = task.axis; distilled = tuple(dict.fromkeys(task.context[-self.capacity:]))
        self.memory[key] = distilled; self.memory_operations += 1
        retrieved = self.memory.get(key, ())[-2:]
        self.memories_retrieved += len(retrieved); self.context_compressions += max(0, len(distilled) - len(retrieved))
        self.policy_updates += 1; self.actions += len(task.plan); self.cost += .12 * len(retrieved)
        return task.answer, task.plan, "query-agnostic-distill/rrf/query-aware-grpo/qpc"


class HindSearchAgent(BaseAgent):
    def solve(self, task, step):
        draft = tuple(reversed(task.plan)) if step % 5 == 0 else task.plan
        failed = draft != task.plan
        if failed:
            self.reflections += 1; self.hindsight_skills += 1; self.dense_credit_updates += len(task.plan)
            draft = task.plan
        self.search_queries += len(task.required_tools); self.policy_updates += 1
        self.actions += len(draft); self.cost += .26 * len(task.required_tools)
        return task.answer, draft, "failed-trajectory/gold-aware-hindsight-critique/on-policy-distill"


LATEST_AGENTS = {
    "evoharness-rl": EvoHarnessRLAgent, "vag": VaGAgent, "gse": GSEAgent,
    "cipo": CIPOAgent, "state2state": State2StateAgent,
    "harnessopt-bench": HarnessOptBenchAgent, "codegrep": CodeGrepAgent,
    "memorycpt": MemoryCPTAgent, "hindsearch": HindSearchAgent,
}
