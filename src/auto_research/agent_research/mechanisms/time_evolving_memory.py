"""Extracted unchanged from auto_research.agent_research.latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def time_evolving_memory(interactions, *, chunk_size: int, memory_budget: int, update):
    """ReMem Eq. (3): bounded, sequential memory updates over history chunks.

    ``update`` receives only the previous memory and current history chunk.  It
    cannot inspect the final recommendation label, preserving the inference
    boundary used by the paper.
    """
    if chunk_size < 1 or memory_budget < 1:
        raise ValueError("chunk_size and memory_budget must be positive")
    memory: tuple[str, ...] = ()
    trace = []
    for start in range(0, len(interactions), chunk_size):
        chunk = tuple(interactions[start:start + chunk_size])
        proposed = tuple(update(memory, chunk))
        memory = proposed[-memory_budget:]
        trace.append({"chunk_start": start, "chunk_size": len(chunk), "memory": memory})
    return memory, trace
