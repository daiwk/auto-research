"""Extracted unchanged from auto_research.agent_research.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def symbolic_gate(actions, state, preconditions):
    """SAGE verify-before-execute gate with typed failure reasons."""
    accepted, blocked = [], []
    current = set(state)
    for action in actions:
        required, effects = preconditions[action]
        missing = sorted(set(required) - current)
        if missing:
            blocked.append({"action": action, "reason": "missing_precondition", "missing": missing})
            break
        accepted.append(action)
        current.update(effects)
    return accepted, blocked
