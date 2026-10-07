"""Extracted unchanged from auto_research.agent_research.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def update_belief_state(previous, observations, unresolved_requirements):
    """Maintain explicit world facts and unresolved requirements for PoS."""
    facts = dict(previous.get("facts", {}))
    facts.update(observations)
    unresolved = tuple(item for item in unresolved_requirements if not facts.get(item))
    progress = len(previous.get("unresolved", ())) - len(unresolved)
    return {"facts": facts, "unresolved": unresolved}, progress <= 0
