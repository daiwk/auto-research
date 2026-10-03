"""Agent mechanisms selected from the 2026-10-03 intake."""

from __future__ import annotations


def autocorrect_compaction(decision, summary, next_action, judge):
    """Execute judge-corrected compaction fields, not the flawed originals."""
    proposed = {"decision": decision, "summary": summary, "next_action": next_action}
    corrected = {**proposed, **judge(proposed)}
    return corrected, {key: corrected[key] != proposed[key] for key in proposed}


def update_belief_state(previous, observations, unresolved_requirements):
    """Maintain explicit world facts and unresolved requirements for PoS."""
    facts = dict(previous.get("facts", {}))
    facts.update(observations)
    unresolved = tuple(item for item in unresolved_requirements if not facts.get(item))
    progress = len(previous.get("unresolved", ())) - len(unresolved)
    return {"facts": facts, "unresolved": unresolved}, progress <= 0


def pace_authorize(tool_call, authority, provenance):
    """Enforce request-derived capabilities immediately before side effects."""
    required = set(tool_call.get("effects", ()))
    allowed = set(authority.get(tool_call["tool"], ()))
    tainted = any(source not in provenance.get("trusted_sources", ()) for source in tool_call.get("influenced_by", ()))
    return required <= allowed and not tainted, {
        "required_effects": tuple(sorted(required)),
        "allowed_effects": tuple(sorted(allowed)),
        "tainted": tainted,
    }


def rule_evolve_select(pool, mutations, evaluator):
    """Mutate a rule pool and retain only validation-improving variants."""
    candidates = list(pool) + list(mutations)
    scored = [(evaluator(rule), rule) for rule in candidates]
    score, selected = max(scored, key=lambda item: item[0])
    return selected, {"evaluated": len(scored), "validation_score": score}


def jev_spawn(probabilities, actions, feedback, *, branches: int):
    """Spawn finite actions, revise their probabilities and retain alternatives."""
    import torch

    posterior = probabilities * torch.exp(torch.as_tensor(feedback, dtype=probabilities.dtype))
    posterior = posterior / posterior.sum().clamp_min(1e-12)
    indices = torch.topk(posterior, min(branches, len(actions))).indices.tolist()
    return tuple(actions[index] for index in indices), posterior


class MemFitStore:
    """Append-only turns with LLM-free lexical/semantic retrieval hooks."""

    def __init__(self):
        self.turns = []

    def append(self, text, *, segment):
        self.turns.append({"text": text, "segment": segment})

    def retrieve(self, query_terms, semantic_scores, *, limit):
        rows = []
        for index, turn in enumerate(self.turns):
            lexical = sum(term.lower() in turn["text"].lower() for term in query_terms)
            rows.append((lexical + semantic_scores.get(index, 0), turn))
        return tuple(turn for _, turn in sorted(rows, key=lambda row: row[0], reverse=True)[:limit])
