"""Executable Agent and RSI mechanisms from the 2026-10-02 intake."""

from __future__ import annotations

from dataclasses import dataclass, field
import math


@dataclass
class CurriculumArm:
    name: str
    value: float = 0.0
    pulls: int = 0
    examples: tuple[str, ...] = ()


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


def safe_self_improvement_select(candidates, validator, *, founder):
    """Validate what runs now and fall back to the founder when none pass."""
    audited = []
    valid = []
    for candidate in candidates:
        result = validator(candidate)
        audited.append({"name": candidate["name"], **result})
        if result.get("safe") and result.get("correct"):
            valid.append(candidate)
    if not valid:
        return founder, {"rollback": True, "audited": audited}
    return max(valid, key=lambda item: (item.get("score", 0.0), item["name"])), {
        "rollback": False,
        "audited": audited,
    }


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


@dataclass
class NonDestructiveMemory:
    """Mem++-style full-document store with time-aware hybrid retrieval."""

    documents: list[dict] = field(default_factory=list)

    def write(self, *, text: str, date: str, author: str) -> None:
        self.documents.append({"text": text, "date": date, "author": author})

    def retrieve(self, query_terms, semantic_scores, *, as_of: str, limit: int = 3):
        terms = {str(term).lower() for term in query_terms}
        eligible = [item for item in self.documents if item["date"] <= as_of]
        ranked = []
        for item in eligible:
            lexical = sum(term in item["text"].lower() for term in terms)
            semantic = float(semantic_scores.get(item["text"], 0.0))
            ranked.append((lexical + semantic, item["date"], item))
        return [item for _, _, item in sorted(ranked, reverse=True)[:limit]]


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


def flowright_hierarchical_credit(workflow, outcome: float, validity):
    """Allocate FloWright credit along workflow structure and valid roles."""
    children = {role: [] for role in workflow}
    for role, spec in workflow.items():
        for parent in spec.get("parents", ()):
            children.setdefault(parent, []).append(role)
    weights = {}
    for role, spec in workflow.items():
        structural = 1.0 + len(children.get(role, ()))
        weights[role] = structural * float(validity.get(role, 0.0))
    total = sum(weights.values())
    if total <= 0:
        return {role: 0.0 for role in workflow}
    return {role: outcome * weight / total for role, weight in weights.items()}
