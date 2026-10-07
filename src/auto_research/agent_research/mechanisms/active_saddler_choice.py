"""Extracted unchanged from auto_research.agent_research.latest_20261002; stable mechanism boundary."""
from __future__ import annotations

import math

def active_saddler_choice(arms, unseen, *, iteration: int, exploration: float = 1.0):
    """Choose a changing failure-pattern arm or explore an unseen scenario."""
    if iteration < 1 or exploration < 0:
        raise ValueError("invalid curriculum state")
    if unseen and (not arms or iteration % (len(arms) + 1) == 0):
        return "draw", unseen[0], {"reason": "discover-new-failure-pattern"}
    if not arms:
        raise ValueError("curriculum has neither arms nor unseen scenarios")
    scores = {
        arm.name: arm.value + exploration * math.sqrt(math.log(iteration + 1) / (arm.pulls + 1))
        for arm in arms
    }
    selected = max(arms, key=lambda arm: (scores[arm.name], arm.name))
    return "pull", selected.name, scores
