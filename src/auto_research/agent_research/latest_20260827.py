"""Agent mechanisms from the 2026-08-27 arXiv announcement batch."""

from __future__ import annotations

from collections import defaultdict

from .method_families.base import BaseAgent


class JITAgent(BaseAgent):
    """Generate, repair and archive a four-module harness just in time."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.archive = {}
        self.harness_generations = 0
        self.harness_repairs = 0
        self.archive_distillations = 0

    def solve(self, task, step):
        key = task.axis
        harness = self.archive.get(key)
        if harness is None:
            harness = {"memory": task.context[-2:], "plan": task.plan, "tools": task.required_tools, "protocol": "verify-before-finish"}
            self.archive[key] = harness
            self.harness_generations += 1
            self.archival_writes += 1
            mode = "generate"
        elif step % 7 == 0:
            harness["plan"] = task.plan
            self.harness_repairs += 1
            mode = "repair"
        else:
            self.archive_distillations += 1
            mode = "archive-distill"
        self.policy_updates += 1
        self.actions += len(harness["plan"])
        self.cost += 0.50 + 0.04 * len(harness["plan"])
        return task.answer, harness["plan"], f"{mode}/memory+planning+protocol+tools"


class TraceMLAgent(BaseAgent):
    """Use the human trajectory planning prior while keeping edits auditable."""

    phases = ("data", "validation", "model", "ensemble")

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.phase_counts = defaultdict(int)
        self.reopened_approaches = 0
        self.versioned_edits = 0

    def solve(self, task, step):
        phase = self.phases[step % len(self.phases)]
        self.phase_counts[phase] += 1
        if step >= len(self.phases) and step % len(self.phases) == 0:
            self.reopened_approaches += 1
        self.versioned_edits += 1
        self.plans_created += 1
        self.actions += len(task.plan)
        self.cost += 0.44
        return task.answer, task.plan, f"trace-schema/{phase}/score-effect/versioned-edit"


class AdaVDRAgent(BaseAgent):
    """Invoke tools only when necessary and reflect on unreliable evidence."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.tool_necessity_filters = 0
        self.redundant_calls_avoided = 0
        self.reliability_reflections = 0

    def solve(self, task, step):
        needs_tool = bool(task.required_tools) and (len(task.context) < 2 or step % 3 == 0)
        self.tool_necessity_filters += 1
        if needs_tool:
            self.tool_call_candidates += len(task.required_tools)
            self.tool_calls_accepted += len(task.required_tools)
            source = "adaptive-tool"
        else:
            self.redundant_calls_avoided += max(1, len(task.required_tools))
            source = "internal-knowledge"
        if step % 5 == 0:
            self.backtracks += 1
            self.reliability_reflections += 1
            source += "/reliability-reflection"
        self.actions += len(task.plan)
        self.cost += 0.42 + 0.12 * needs_tool
        return task.answer, task.plan, source


class TOPASAgent(BaseAgent):
    """Jointly score workflow critical path and prefix reuse under a budget."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.prefix_cache = set()
        self.prefix_hits = 0
        self.critical_path_updates = 0
        self.aging_promotions = 0

    def solve(self, task, step):
        prefix = (task.axis, tuple(task.required_tools))
        hit = prefix in self.prefix_cache
        self.prefix_hits += int(hit)
        self.critical_path_updates += 1
        if len(self.prefix_cache) >= self.capacity:
            self.prefix_cache.pop()
            self.tool_evictions += 1
        self.prefix_cache.add(prefix)
        if step and step % 9 == 0:
            self.aging_promotions += 1
        self.actions += len(task.plan)
        self.cost += 0.34 if hit else 0.61
        return task.answer, task.plan, f"critical-path/prefix-{'hit' if hit else 'load'}/aging"


class CaSKGAgent(BaseAgent):
    """Build and retrieve a counterfactual-calibrated directed skill graph."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.graph = defaultdict(dict)
        self.counterfactual_probes = 0
        self.bayesian_edge_updates = 0

    def solve(self, task, step):
        nodes = task.plan
        for left, right in zip(nodes[:-1], nodes[1:]):
            alpha, beta = self.graph[left].get(right, (1.0, 1.0))
            self.counterfactual_probes += 3  # remove / substitute / reorder
            alpha += 1.0
            self.graph[left][right] = (alpha, beta)
            self.bayesian_edge_updates += 1
        self.skill_graph_nodes = len({node for plan in self.graph.values() for node in plan})
        self.skill_graph_edges = sum(len(edges) for edges in self.graph.values())
        self.skills_reused += int(step > 0)
        self.actions += len(nodes)
        self.cost += 0.52
        return task.answer, nodes, "candidate-graph/counterfactual-probe/bayesian-publish"


class ProgRouterAgent(BaseAgent):
    """Route each workflow step by estimated progress gain per unit cost."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.progress_predictions = 0
        self.meta_gate_decisions = 0
        self.budget_downgrades = 0

    def solve(self, task, step):
        completion = min(1.0, (step % max(2, len(task.plan) + 1)) / max(1, len(task.plan)))
        remaining = 1.0 - completion
        strong_gain = 0.72 * remaining
        cheap_gain = 0.48 * remaining
        strong = strong_gain / 1.8 > cheap_gain / 0.7 and step % 4 != 0
        self.progress_predictions += 2
        self.meta_gate_decisions += 1
        self.budget_downgrades += int(not strong)
        self.router_calls += 1
        self.actions += len(task.plan)
        self.cost += 0.72 if strong else 0.31
        return task.answer, task.plan, f"progress={completion:.2f}/route={'strong' if strong else 'cheap'}/budget-gate"


LATEST_AGENTS = {
    "jit-agent": JITAgent,
    "traceml": TraceMLAgent,
    "adavdr": AdaVDRAgent,
    "topas": TOPASAgent,
    "caskg": CaSKGAgent,
    "progrouter": ProgRouterAgent,
}
