"""Extracted unchanged from auto_research.agent_research.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def rule_evolve_select(pool, mutations, evaluator):
    """Mutate a rule pool and retain only validation-improving variants."""
    candidates = list(pool) + list(mutations)
    scored = [(evaluator(rule), rule) for rule in candidates]
    score, selected = max(scored, key=lambda item: item[0])
    return selected, {"evaluated": len(scored), "validation_score": score}
