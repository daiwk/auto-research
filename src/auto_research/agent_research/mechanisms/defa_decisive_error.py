"""Extracted unchanged from auto_research.agent_research.latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def defa_decisive_error(events, dependencies):
    """Trace a DeFA failure-propagation graph back to its decisive event."""
    by_id = {event["id"]: event for event in events}
    violated = {event["id"] for event in events if event.get("violates", False)}
    frontier = list(violated)
    implicated = set(violated)
    while frontier:
        node = frontier.pop()
        for parent in dependencies.get(node, ()):
            if parent not in implicated:
                implicated.add(parent)
                frontier.append(parent)
    candidates = [by_id[node] for node in implicated if by_id[node].get("error_score", 0) > 0]
    decisive = max(candidates, key=lambda item: (item["error_score"], -item["step"]))
    return decisive, {"propagation_nodes": tuple(sorted(implicated))}
