"""Extracted unchanged from auto_research.agent_research.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def local_suffix_edit(plan, failed_index, replacement):
    """Preserve completed SAGE prefix and regenerate only the failed suffix."""
    if not 0 <= failed_index < len(plan):
        raise IndexError("failed action is outside plan")
    return list(plan[:failed_index]) + list(replacement)
