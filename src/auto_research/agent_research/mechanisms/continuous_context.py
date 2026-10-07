"""Extracted unchanged from auto_research.agent_research.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def continuous_context(task, memory, observation, *, memory_budget: int):
    """CCM prompt contains task, bounded memory and newest observation only."""
    if memory_budget < 1:
        raise ValueError("memory budget must be positive")
    retained = tuple(memory)[-memory_budget:]
    return {"task": task, "memory": retained, "observation": observation}
