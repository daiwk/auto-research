"""Extracted unchanged from auto_research.post_training.latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def oasis_select_scaffold(rollouts):
    """Choose the shortest verified rollout and a distinct same-problem context."""
    verified = [item for item in rollouts if item["verified"]]
    if not verified:
        return None
    scaffold = min(verified, key=lambda item: (len(item["tokens"]), item["id"]))
    alternatives = [item for item in rollouts if item["id"] != scaffold["id"]]
    if not alternatives:
        raise ValueError("OASIS requires a distinct same-problem context")
    unverified = [item for item in alternatives if not item["verified"]]
    context = min(unverified or alternatives, key=lambda item: item["id"])
    return scaffold, context
