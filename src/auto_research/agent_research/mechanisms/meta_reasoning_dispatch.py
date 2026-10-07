"""Extracted unchanged from auto_research.agent_research.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



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
