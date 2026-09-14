"""Executable, observation-only mechanisms from the 2026-09-11 agent batch.

These classes exercise the papers' state transitions on the public mini-suite.
They never inspect ``AgentTask.answer`` or ``AgentTask.plan`` before acting and
must therefore remain mechanism diagnostics rather than capability claims.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import math

from .latest_20260907 import ObservationAgent, PublicObservation, read_evidence
from .method_families.base import _tokens


class COBRASkillsAgent(ObservationAgent):
    """Contextual-UCB allocation over an evolving, evidence-grounded skill set."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skill_trials = Counter()
        self.skill_rewards = Counter()
        self.skill_plans: dict[str, tuple[str, ...]] = {}
        self.pending_skill = ""
        self.bandit_allocations = self.skill_evolutions = 0

    def _key(self, intent):
        tokens = sorted(_tokens(intent))
        return tokens[0] if tokens else "default"

    def solve_observation(self, observation, step):
        answer, observed = read_evidence(observation)
        context = _tokens(observation.intent)
        candidates = list(self.skill_plans)
        if candidates:
            total = 1 + sum(self.skill_trials.values())
            scored = []
            for key in candidates:
                overlap = int(key in context)
                mean = self.skill_rewards[key] / max(1, self.skill_trials[key])
                bonus = math.sqrt(math.log(total + 1) / (1 + self.skill_trials[key]))
                scored.append((overlap + mean + bonus, key))
            _, selected = max(scored)
            self.pending_skill = selected
            self.bandit_allocations += 1
            plan = observed or self.skill_plans[selected]
        else:
            self.pending_skill = self._key(observation.intent)
            plan = observed
        if observed and self.skill_plans.get(self.pending_skill) != observed:
            self.skill_plans[self.pending_skill] = observed
            self.skill_evolutions += 1
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "contextual-ucb/evidence-grounded-skill-evolution"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        if self.pending_skill:
            self.skill_trials[self.pending_skill] += 1
            self.skill_rewards[self.pending_skill] += int(answer_ok and plan_ok)


class EcdysisAgent(ObservationAgent):
    """Batch recurring-failure diagnosis before accepting a harness repair."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.failure_signatures = Counter()
        self.pending_signature = ""
        self.cross_instance_failures = self.fdcr_repairs = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        self.pending_signature = ":".join(sorted(_tokens(observation.intent))[:2])
        if self.failure_signatures[self.pending_signature] >= 2:
            self.fdcr_repairs += 1
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "cross-instance-failure-aggregation/fdcr-moderation"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        if not (answer_ok and plan_ok):
            self.failure_signatures[self.pending_signature] += 1
            self.cross_instance_failures += 1


class GroundedMemoryAgent(ObservationAgent):
    """Least-privilege curation that admits facts only after public re-probing."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.probes = Counter()
        self.curated: dict[str, str] = {}
        self.environment_probes = self.memory_admissions = self.stale_rejections = 0

    def solve_observation(self, observation, step):
        del step
        for fact in observation.context:
            key = " ".join(sorted(_tokens(fact))[:4])
            self.probes[(key, fact)] += 1
            self.environment_probes += 1
            prior = self.curated.get(key)
            if prior and prior != fact:
                self.stale_rejections += 1
                continue
            if self.probes[(key, fact)] >= 2 and prior is None:
                self.curated[key] = fact
                self.memory_admissions += 1
        evidence = tuple(observation.context) + tuple(self.curated.values())
        answer, plan = read_evidence(PublicObservation(
            observation.task_id, observation.intent, evidence
        ))
        self.actions += len(plan)
        self.cost += len(evidence)
        return answer, plan, "read-only-probe/scope-refresh/curation-gate"


class ToolGradAgent(ObservationAgent):
    """Answer-first tool-plan construction followed by textual-gradient edits."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.answer_first_generations = self.textual_gradient_edits = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        self.answer_first_generations += 1
        # The desired answer is decoded from public evidence first.  A textual
        # gradient then removes duplicate operations from the observed route;
        # it never receives the benchmark's hidden plan.
        refined = tuple(dict.fromkeys(plan))
        self.textual_gradient_edits += int(refined != plan)
        self.actions += len(refined)
        self.cost += len(observation.context)
        return answer, refined, "answer-first/textual-gradient/tool-trajectory"


class PROMPTSAgent(ObservationAgent):
    """Profiler bottleneck ranking and conservative configuration proposal."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.profile_bottlenecks = self.sharding_proposals = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        costs = Counter(token for fact in observation.context for token in _tokens(fact))
        if costs:
            self.profile_bottlenecks += 1
            # Proposals are limited to an observed executable route; no invented
            # shell or distributed-runtime action is executed by this fixture.
            self.sharding_proposals += int(bool(plan))
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "profile-evidence/bottleneck-rank/config-proposal"


class SearchAtlasAgent(ObservationAgent):
    """Evidential query graph from public queries, observations and answer."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.evidence_graph_edges = self.unsupported_answer_flags = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        evidence = [fact for fact in observation.context if "resolves to" in fact]
        self.evidence_graph_edges += len(plan) + len(evidence)
        self.unsupported_answer_flags += int(bool(answer) and not evidence)
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "query-evidence-answer-graph/process-audit"


class SkillRetentionAgent(ObservationAgent):
    """Replay-anchored skill router that retains observed real-task routes."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.anchors: dict[str, tuple[str, ...]] = {}
        self.anchor_penalties = self.replay_retrievals = 0

    def solve_observation(self, observation, step):
        answer, observed = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2])
        prior = self.anchors.get(key)
        if observed:
            if prior and prior != observed:
                self.anchor_penalties += 1
            self.anchors[key] = observed
        elif prior:
            self.replay_retrievals += 1
        plan = observed or prior or ()
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "real-route-anchor/replay/forgetting-penalty"


class T1TerminalAgent(ObservationAgent):
    """Exact-token/route replay audit for long-horizon terminal RL traces."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.tito_tokens = self.routing_replays = self.turn_boundary_repairs = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        token_ids = tuple(hash(token) & 0xFFFF for action in plan for token in action.split())
        self.tito_tokens += len(token_ids)
        self.routing_replays += len(plan)
        self.turn_boundary_repairs += sum(not action.strip() for action in plan)
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "tito-exact-token/turn-boundary-repair/routing-replay"


LATEST_AGENTS = {
    "cobra-skills": COBRASkillsAgent,
    "ecdysis": EcdysisAgent,
    "grounded-memory": GroundedMemoryAgent,
    "toolgrad": ToolGradAgent,
    "prompts": PROMPTSAgent,
    "searchatlas": SearchAtlasAgent,
    "skill-retention": SkillRetentionAgent,
    "t1-terminal-rl": T1TerminalAgent,
}
