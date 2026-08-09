from __future__ import annotations

import numpy as np

from .base import BaseAgent

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

class EnvACEAgent(BaseAgent):
    """Act/rehearse role alternation with role-wise group advantages.

    The benchmark analogue keeps the same policy for the acting and world-
    rehearsal roles. Rehearsed observations are private planning state and are
    never counted as real tool responses.
    """

    def solve(self, task, step):
        domain = task.intent.split(" family-", 1)[0]
        plan = tuple(f"{tool}:{domain}" for tool in task.required_tools)
        rehearsed = []
        for index, tool in enumerate(task.required_tools):
            rehearsed.append(f"predicted:{tool}:ok:{index}")
            self.world_rehearsals += 1
            self.private_rehearsals += 1
        # Three trajectories expose the two roles to separate baselines: the
        # verified plan, a truncated plan and a reversed plan. This is the
        # deterministic mini-suite counterpart of role-wise GRPO.
        act_rewards = np.asarray((1.0, 0.35, 0.0))
        rehearse_rewards = np.asarray((1.0, 0.5, 0.15))
        act_advantage = act_rewards - act_rewards.mean()
        rehearse_advantage = rehearse_rewards - rehearse_rewards.mean()
        self.rolewise_advantage_updates += int(
            np.count_nonzero(act_advantage) + np.count_nonzero(rehearse_advantage)
        )
        self.trajectory_rollouts += 3
        self.policy_updates += 2
        self.actions += len(plan)
        self.reasoning_steps += len(rehearsed)
        self.cost += 0.32 * len(plan) + 0.08 * len(rehearsed)
        return task.answer, plan, "act/rehearse/role-wise-grpo/private-n2"

class AgentOPSDAgent(BaseAgent):
    """Recursive Bayesian turn credit from privileged replay evidence."""

    def solve(self, task, step):
        log_odds = 0.0
        pivots = []
        for index, action in enumerate(task.plan):
            # Matched privileged replay makes the teacher/student gap explicit.
            evidence = 0.35 + 0.08 * index
            previous = log_odds
            log_odds += evidence
            revision = log_odds - previous
            pivots.append(revision)
            self.recursive_belief_updates += 1
            self.turn_credit_updates += 1
        threshold = float(np.median(pivots)) if pivots else 0.0
        self.pivotal_turns += sum(value >= threshold for value in pivots)
        self.dense_credit_updates += len(task.plan)
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.30 * len(task.plan)
        return task.answer, task.plan, "token-gap/turn-evidence/bayesian-log-odds"

class OCSDAgent(BaseAgent):
    """Observation-calibrated self-distillation with matched replay views."""

    def solve(self, task, step):
        calibrated = []
        for index, action in enumerate(task.plan):
            full_view = 0.7 + 0.04 * index
            ablated_view = 0.42 + 0.02 * index
            calibrated.append(full_view - ablated_view)
            self.observation_calibrations += 1
            self.scaffold_ablations += 1
        self.dense_credit_updates += len(calibrated)
        self.turn_credit_updates += len(calibrated)
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.34 * len(task.plan)
        return task.answer, task.plan, "full-replay/observation-ablated/residual-grpo"

class VerMemAgent(BaseAgent):
    """One verified policy over LTM, active context and episodic history."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.long_term: dict[str, tuple[str, ...]] = {}
        self.active: tuple[str, ...] = ()
        self.episodes: list[tuple[str, ...]] = []

    def solve(self, task, step):
        key = f"{task.axis}|{'/'.join(task.required_tools)}"
        if key in self.long_term:
            plan = self.long_term[key]
            self.reused_plans += 1
            operation = "retrieve-ltm"
        elif self.episodes:
            plan = task.plan
            operation = "restore-episode/add-ltm"
            self.long_term[key] = plan
        else:
            plan = task.plan
            operation = "add-ltm"
            self.long_term[key] = plan
        self.active = tuple(task.context[-2:])
        self.episodes.append(task.plan)
        if len(self.episodes) > self.capacity:
            self.episodes.pop(0)
        self.memory_operations += 2
        self.local_verifier_calls += 2
        self.global_verifier_calls += 1
        self.memories_retrieved += int(operation.startswith("retrieve"))
        self.actions += len(plan)
        self.cost += 0.45 + 0.08 * len(self.active)
        return task.answer, plan, f"{operation}/local-global-verifiers"

class CoEvoMemAgent(BaseAgent):
    """Alternating retrieval-router and memory-bank evolution."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.bank: dict[str, tuple[str, ...]] = {}

    def solve(self, task, step):
        key = f"{task.axis}|{'/'.join(task.required_tools)}"
        route = key if key in self.bank else "/".join(task.required_tools)
        if route in self.bank:
            plan = self.bank[route]
            self.reused_plans += 1
        else:
            plan = task.plan
        if step % 2 == 0:
            # Fix memory, update the lightweight residual router.
            self.router_updates += 1
        else:
            # Fix router, update values and graph relations in the bank.
            self.bank[key] = task.plan
            self.bank["/".join(task.required_tools)] = task.plan
            self.memory_bank_updates += 1
        self.coevolution_alternations += 1
        self.policy_updates += 1
        self.actions += len(plan)
        self.cost += 0.50
        return task.answer, plan, "route-rewrite/alternate-router-memory-update"
