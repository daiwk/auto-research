"""Extracted unchanged from auto_research.agent_research.latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def flowright_hierarchical_credit(workflow, outcome: float, validity):
    """Allocate FloWright credit along workflow structure and valid roles."""
    children = {role: [] for role in workflow}
    for role, spec in workflow.items():
        for parent in spec.get("parents", ()):
            children.setdefault(parent, []).append(role)
    weights = {}
    for role, spec in workflow.items():
        structural = 1.0 + len(children.get(role, ()))
        weights[role] = structural * float(validity.get(role, 0.0))
    total = sum(weights.values())
    if total <= 0:
        return {role: 0.0 for role in workflow}
    return {role: outcome * weight / total for role, weight in weights.items()}
