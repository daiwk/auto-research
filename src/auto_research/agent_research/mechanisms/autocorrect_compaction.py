"""Extracted unchanged from auto_research.agent_research.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def autocorrect_compaction(decision, summary, next_action, judge):
    """Execute judge-corrected compaction fields, not the flawed originals."""
    proposed = {"decision": decision, "summary": summary, "next_action": next_action}
    corrected = {**proposed, **judge(proposed)}
    return corrected, {key: corrected[key] != proposed[key] for key in proposed}
