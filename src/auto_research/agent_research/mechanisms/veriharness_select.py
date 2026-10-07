"""Extracted unchanged from auto_research.agent_research.latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def veriharness_select(rollouts, evidence_checker):
    """Resolve disagreement and challenge consensus against evidence."""
    if not rollouts:
        raise ValueError("at least one rollout is required")
    scored = []
    claims = [set(item["claims"]) for item in rollouts]
    consensus = set.intersection(*claims) if claims else set()
    for item, item_claims in zip(rollouts, claims):
        supported = sum(bool(evidence_checker(claim)) for claim in item_claims)
        contradicted_consensus = sum(
            not bool(evidence_checker(claim)) for claim in consensus
        )
        score = supported - contradicted_consensus - len(item_claims) * 1e-6
        scored.append((score, item["id"]))
    score, selected = max(scored)
    return selected, {"score": score, "consensus_claims_challenged": len(consensus)}
