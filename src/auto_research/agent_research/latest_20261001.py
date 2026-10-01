"""Executable Agent/RSI reference kernels from the Oct-1 intake batch."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class ProposedAction:
    name: str
    expected_value: float
    cost: int
    context: tuple[str, ...] = ()


def meta_reasoning_dispatch(actions, *, remaining_budget: int):
    """Evaluate then dispatch the highest value-per-call feasible action."""
    feasible = [a for a in actions if 0 < a.cost <= remaining_budget]
    if not feasible:
        return None, {"stopped": True, "remaining_budget": remaining_budget}
    selected = max(feasible, key=lambda a: (a.expected_value / a.cost, a.expected_value, -a.cost))
    return selected, {
        "stopped": False,
        "selected": selected.name,
        "budget_after": remaining_budget - selected.cost,
        "context_items": len(selected.context),
    }


def compact_artifact_state(previous, new_artifacts, *, keep: int):
    """Persist artifacts while carrying only a bounded compact run state."""
    if keep < 1:
        raise ValueError("keep must be positive")
    memory = dict(previous.get("memory", {}))
    for artifact in new_artifacts:
        memory[artifact["id"]] = dict(artifact)
    frontier = tuple(item["id"] for item in new_artifacts[-keep:])
    return {"memory": memory, "frontier": frontier, "artifact_count": len(memory)}


def apply_context_file(context: str, edits, *, maximum_characters: int):
    """CLM context-as-a-file: unrestricted replace/append with an explicit budget."""
    if maximum_characters < 1:
        raise ValueError("maximum_characters must be positive")
    value = context
    for edit in edits:
        operation = edit["operation"]
        if operation == "replace":
            old = edit["old"]
            if old not in value:
                raise ValueError("replace target is absent from context")
            value = value.replace(old, edit["new"], 1)
        elif operation == "append":
            value += edit["text"]
        else:
            raise ValueError(f"unknown context edit: {operation}")
    if len(value) > maximum_characters:
        value = value[-maximum_characters:]
    return value


def suffix_cache_reuse(previous_tokens, current_tokens):
    """Return the longest reusable prefix and unmatched CLM suffix."""
    matched = 0
    for left, right in zip(previous_tokens, current_tokens):
        if left != right:
            break
        matched += 1
    return matched, tuple(current_tokens[matched:])


@dataclass
class MetaSkillBank:
    """Development-only meta-skill refinement; test tasks can only read the bank."""

    skills: dict[str, dict] = field(default_factory=dict)

    def revise(self, outcomes):
        for item in outcomes:
            name = item["skill"]
            current = self.skills.setdefault(name, {"when": set(), "provide": set(), "use": set(), "score": 0.0})
            weight = float(item["reward"])
            current["score"] += weight
            if weight > 0:
                for field_name in ("when", "provide", "use"):
                    current[field_name].update(item.get(field_name, ()))

    def select(self, task_tags, *, limit: int):
        tags = set(task_tags)
        ranked = []
        for name, skill in self.skills.items():
            overlap = len(tags & set(skill["when"]))
            ranked.append((overlap, skill["score"], name))
        return tuple(name for overlap, _, name in sorted(ranked, reverse=True)[:limit] if overlap)


def update_branch_subsets(branch_scores):
    """Retain cases solved more often by one branch and drop globally solved cases."""
    branches = sorted(branch_scores)
    cases = sorted({case for scores in branch_scores.values() for case in scores})
    retained = {branch: [] for branch in branches}
    for case in cases:
        values = {branch: float(branch_scores[branch].get(case, 0.0)) for branch in branches}
        if values and all(value >= 1.0 for value in values.values()):
            continue
        best = max(values.values(), default=0.0)
        for branch, value in values.items():
            if value == best and value > 0:
                retained[branch].append(case)
    return {branch: tuple(cases) for branch, cases in retained.items()}


def route_branch(features, router_weights):
    """Choose a development-selected branch head without reading test outcomes."""
    scores = {
        branch: sum(float(features.get(key, 0.0)) * float(weight) for key, weight in weights.items())
        for branch, weights in router_weights.items()
    }
    if not scores:
        raise ValueError("router requires at least one branch")
    return max(scores, key=lambda branch: (scores[branch], branch)), scores
