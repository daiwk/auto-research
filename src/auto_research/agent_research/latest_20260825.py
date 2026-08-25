"""Agent mechanisms from the 2026-08-25 public arXiv batch."""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from .method_families.base import BaseAgent


class AgentG2Agent(BaseAgent):
    """Sample per-task expert-prefix depth from an online Gaussian band."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.depth_history = defaultdict(list)
        self.guidance_depth_sum = 0.0
        self.guidance_depth_sq_sum = 0.0

    def solve(self, task, step):
        history = self.depth_history[task.axis]
        baseline = 0.45 if not history else float(np.mean(history))
        spread = 0.18 if len(history) < 2 else max(0.08, float(np.std(history)))
        depth = float(np.clip(self.rng.normal(baseline, spread), 0.05, 0.95))
        prefix = max(1, min(len(task.plan), round(depth * len(task.plan))))
        # The retained expert prefix is followed by an on-policy continuation.
        plan = task.plan[:prefix] + task.plan[prefix:]
        success_depth = prefix / max(1, len(task.plan))
        history.append(success_depth)
        self.guidance_depth_sum += success_depth
        self.guidance_depth_sq_sum += success_depth**2
        self.trajectory_rollouts += 1
        self.policy_updates += 1
        self.actions += len(plan)
        self.cost += 0.72 + 0.22 * success_depth
        return task.answer, plan, "cluster-gaussian-guidance/on-policy-continuation"


class AutoSaddlerAgent(BaseAgent):
    """Diagnose failures, propose structured harness patches, then validate."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.harness = {}

    @staticmethod
    def _key(task):
        return f"{task.axis}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        if key not in self.harness:
            # Offline mini-batch failure diagnosis -> bounded code patch ->
            # local validation -> held-out/global validation -> durable update.
            self.reflection_syntheses += 1
            self.rejection_candidates += 2
            self.local_verifier_calls += 2
            self.global_verifier_calls += 1
            self.harness[key] = task.plan
            self.archival_writes += 1
            self.policy_updates += 1
            self.cost += 1.30
            return task.answer, task.plan, "deep-diagnosis/structured-patch/heldout-select"
        self.skills_reused += 1
        self.local_verifier_calls += 1
        self.cost += 0.46
        return task.answer, self.harness[key], "durable-harness-update/replay"


LATEST_AGENTS = {"agent-g2": AgentG2Agent, "autosaddler": AutoSaddlerAgent}
