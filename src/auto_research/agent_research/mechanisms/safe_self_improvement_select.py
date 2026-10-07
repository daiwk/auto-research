"""Extracted unchanged from auto_research.agent_research.latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def safe_self_improvement_select(candidates, validator, *, founder):
    """Validate what runs now and fall back to the founder when none pass."""
    audited = []
    valid = []
    for candidate in candidates:
        result = validator(candidate)
        audited.append({"name": candidate["name"], **result})
        if result.get("safe") and result.get("correct"):
            valid.append(candidate)
    if not valid:
        return founder, {"rollback": True, "audited": audited}
    return max(valid, key=lambda item: (item.get("score", 0.0), item["name"])), {
        "rollback": False,
        "audited": audited,
    }
