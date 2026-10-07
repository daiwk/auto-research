"""Extracted unchanged from auto_research.agent_research.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def compact_artifact_state(previous, new_artifacts, *, keep: int):
    """Persist artifacts while carrying only a bounded compact run state."""
    if keep < 1:
        raise ValueError("keep must be positive")
    memory = dict(previous.get("memory", {}))
    for artifact in new_artifacts:
        memory[artifact["id"]] = dict(artifact)
    frontier = tuple(item["id"] for item in new_artifacts[-keep:])
    return {"memory": memory, "frontier": frontier, "artifact_count": len(memory)}
