"""Extracted unchanged from auto_research.agent_research.latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def premature_disclosure_rate(turns, private_fields):
    """Audit whether a simulated user reveals a private field before it is requested."""
    requested: set[str] = set()
    violations = 0
    disclosures = 0
    for turn in turns:
        requested.update(turn.get("requested_fields", ()))
        for field in turn.get("disclosed_fields", ()):
            if field not in private_fields:
                continue
            disclosures += 1
            violations += field not in requested
    return {"premature_disclosures": violations, "private_disclosures": disclosures, "rate": violations / max(1, disclosures)}
