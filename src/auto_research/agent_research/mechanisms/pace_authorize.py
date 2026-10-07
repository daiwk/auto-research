"""Extracted unchanged from auto_research.agent_research.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def pace_authorize(tool_call, authority, provenance):
    """Enforce request-derived capabilities immediately before side effects."""
    required = set(tool_call.get("effects", ()))
    allowed = set(authority.get(tool_call["tool"], ()))
    tainted = any(source not in provenance.get("trusted_sources", ()) for source in tool_call.get("influenced_by", ()))
    return required <= allowed and not tainted, {
        "required_effects": tuple(sorted(required)),
        "allowed_effects": tuple(sorted(allowed)),
        "tainted": tainted,
    }
