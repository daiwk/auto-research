"""Extracted unchanged from auto_research.foundation_latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def splash_select_layout(costs, previous: str | None, transition_costs, *, remaining_steps: int):
    """Choose the layout with transition cost amortized over remaining steps."""
    if remaining_steps < 1 or not costs:
        raise ValueError("invalid scheduling inputs")
    effective = {}
    for layout, step_cost in costs.items():
        switch = 0.0 if previous in (None, layout) else float(transition_costs.get((previous, layout), 0.0))
        effective[layout] = float(step_cost) + switch / remaining_steps
    return min(effective, key=lambda key: (effective[key], key)), effective
