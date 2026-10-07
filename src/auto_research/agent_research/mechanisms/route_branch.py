"""Extracted unchanged from auto_research.agent_research.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def route_branch(features, router_weights):
    """Choose a development-selected branch head without reading test outcomes."""
    scores = {
        branch: sum(float(features.get(key, 0.0)) * float(weight) for key, weight in weights.items())
        for branch, weights in router_weights.items()
    }
    if not scores:
        raise ValueError("router requires at least one branch")
    return max(scores, key=lambda branch: (scores[branch], branch)), scores
