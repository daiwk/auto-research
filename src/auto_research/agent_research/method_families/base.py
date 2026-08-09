from __future__ import annotations

from dataclasses import dataclass
import re

import numpy as np

from ..models import AgentTask


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
        self.world_rehearsals = 0
        self.rolewise_advantage_updates = 0
        self.private_rehearsals = 0
        self.recursive_belief_updates = 0
        self.pivotal_turns = 0
        self.observation_calibrations = 0
        self.scaffold_ablations = 0
        self.local_verifier_calls = 0
        self.global_verifier_calls = 0
        self.memory_operations = 0
        self.coevolution_alternations = 0
        self.router_updates = 0
        self.memory_bank_updates = 0

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
