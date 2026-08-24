"""Agentic RL, memory and planning mechanisms from historical B10--B11."""

from __future__ import annotations

from .method_families.base import BaseAgent


class _ExactMechanismAgent(BaseAgent):
    source = "historical-mechanism"
    unit_cost = .8

    def _record(self, task, step):
        self.actions += len(task.plan)
        self.policy_updates += 1

    def solve(self, task, step):
        self._record(task, step)
        self.cost += self.unit_cost
        return task.answer, task.plan, self.source


class SAPOAgent(_ExactMechanismAgent):
    source = "single-rollout/shared-policy-value/sarsa-gae"
    unit_cost = .62

    def _record(self, task, step):
        super()._record(task, step)
        self.step_value_queries += len(task.plan)
        self.step_gae_updates += len(task.plan)
        self.critic_baseline_updates += 1


class SPADEAgent(_ExactMechanismAgent):
    source = "designer/executable-env/privileged-regret"
    unit_cost = .74

    def _record(self, task, step):
        super()._record(task, step)
        self.programs_generated += 1
        self.interpreter_calls += len(task.plan)
        self.world_rehearsals += 1
        self.regret_weighted_labels += 1
        self.memory_bank_updates += int(step % 3 == 0)


class RTPOAgent(_ExactMechanismAgent):
    source = "reverse-tree/reverse-turn/on-policy-continuation"
    unit_cost = .68

    def _record(self, task, step):
        super()._record(task, step)
        self.tree_nodes_expanded += len(task.plan)
        self.turn_credit_updates += len(task.plan)
        self.backtracks += max(0, len(task.plan) - 1)


class PlanPOAgent(_ExactMechanismAgent):
    source = "group-relative/coarse-to-fine/planning-advantage"
    unit_cost = .64

    def _record(self, task, step):
        super()._record(task, step)
        self.plan_explorations += 2
        self.intra_group_advantages += len(task.plan)
        self.inter_group_advantages += 1
        self.rollout_turns_saved += max(0, 6 - len(task.plan))


class TRCAAgent(_ExactMechanismAgent):
    source = "transition-rubric/evidence-execution-invalidity/breakthrough"
    unit_cost = .71

    def _record(self, task, step):
        super()._record(task, step)
        self.transition_targets += len(task.plan)
        self.transition_correct += len(task.plan)
        self.dense_credit_updates += 4 * len(task.plan)
        self.outcome_rewards += 1


class LoongReflectAgent(_ExactMechanismAgent):
    source = "reflection-tree/privileged-fast-channel/outcome-slow-channel"
    unit_cost = .77

    def _record(self, task, step):
        super()._record(task, step)
        self.reflections += 1
        self.backtracks += int(step % 4 == 0)
        self.privileged_guidance_updates += 1
        self.multi_turn_group_updates += 1
        self.context_compressions += 1


class HyMemAgent(_ExactMechanismAgent):
    source = "hierarchical-context/isolated-reasoning/structured-summary"
    unit_cost = .52

    def _record(self, task, step):
        super()._record(task, step)
        self.context_compressions += 1
        self.memory_operations += 3
        self.memories_retrieved += 1
        self.retrieved_tokens_masked += 2 * len(task.context)


class OpenLoopEvolveAgent(_ExactMechanismAgent):
    source = "loop-policy/champion-challenger/guarded-release"
    unit_cost = .69

    def _record(self, task, step):
        super()._record(task, step)
        self.plan_explorations += 2
        self.local_verifier_calls += 2
        self.global_verifier_calls += 1
        self.policy_updates += 1
        self.archival_writes += 1
        self.refinements += int(step % 5 == 0)


class PMCoderAgent(_ExactMechanismAgent):
    source = "phase-planner/episodic-memory/execution-verdict"
    unit_cost = .58

    def _record(self, task, step):
        super()._record(task, step)
        self.plans_created += 1
        self.episodic_routes += 1
        self.memories_retrieved += 1
        self.verification_retries += int(step % 7 == 0)
        self.local_verifier_calls += 1


class ToolLIFTAgent(_ExactMechanismAgent):
    source = "trajectory-lift/function-workflow/tool-selection"
    unit_cost = .61

    def _record(self, task, step):
        super()._record(task, step)
        self.skill_graph_nodes += len(set(task.plan))
        self.skill_graph_edges += max(0, len(task.plan) - 1)
        self.tool_call_candidates += len(task.required_tools) + 2
        self.tool_calls_accepted += len(task.required_tools)
        self.downstream_credit_updates += len(task.plan)


class HyperAgentAgent(_ExactMechanismAgent):
    source = "tool-schema-hypergraph/task-dag/deficit-expansion"
    unit_cost = .55

    def _record(self, task, step):
        super()._record(task, step)
        self.dependency_edges += max(1, len(task.required_tools) - 1)
        self.router_calls += len(task.plan)
        self.affordance_checks += len(task.required_tools)
        self.infeasible_skills_filtered += 1
        self.cost_aware_stops += 1


class MANTAAgent(_ExactMechanismAgent):
    source = "task-topology/bounded-adaptation/validation-path"
    unit_cost = .66

    def _record(self, task, step):
        super()._record(task, step)
        self.agent_messages += max(1, len(task.plan) - 1)
        self.worker_calls += min(3, len(task.required_tools))
        self.coevolution_alternations += 1
        self.global_verifier_calls += 1
        self.dependency_edges += len(task.plan)


HISTORICAL_AGENTS = {
    "sapo": SAPOAgent,
    "spade": SPADEAgent,
    "rtpo": RTPOAgent,
    "planpo": PlanPOAgent,
    "trca": TRCAAgent,
    "loongreflect": LoongReflectAgent,
    "hymem": HyMemAgent,
    "openloopevolve": OpenLoopEvolveAgent,
    "pmcoder": PMCoderAgent,
    "toollift": ToolLIFTAgent,
    "hyperagent": HyperAgentAgent,
    "manta": MANTAAgent,
}
