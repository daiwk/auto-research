"""Agent mechanisms from the Sep-30 closure."""

from __future__ import annotations


def rubric_process_credit(history_support, new_support):
    """Dr.Credit counts new, partial rubric support rather than repeated evidence."""
    import numpy as np

    history = np.asarray(history_support, dtype=np.float64)
    current = np.asarray(new_support, dtype=np.float64)
    if history.shape != current.shape or np.any((current < 0) | (current > 1)):
        raise ValueError("rubric support must align and lie in [0,1]")
    credit = np.maximum(current - history, 0)
    return credit, {"new_support": float(credit.sum()), "covered_rubrics": int((current > 0).sum())}


def continuous_context(task, memory, observation, *, memory_budget: int):
    """CCM prompt contains task, bounded memory and newest observation only."""
    if memory_budget < 1:
        raise ValueError("memory budget must be positive")
    retained = tuple(memory)[-memory_budget:]
    return {"task": task, "memory": retained, "observation": observation}


def symbolic_gate(actions, state, preconditions):
    """SAGE verify-before-execute gate with typed failure reasons."""
    accepted, blocked = [], []
    current = set(state)
    for action in actions:
        required, effects = preconditions[action]
        missing = sorted(set(required) - current)
        if missing:
            blocked.append({"action": action, "reason": "missing_precondition", "missing": missing})
            break
        accepted.append(action)
        current.update(effects)
    return accepted, blocked


def local_suffix_edit(plan, failed_index, replacement):
    """Preserve completed SAGE prefix and regenerate only the failed suffix."""
    if not 0 <= failed_index < len(plan):
        raise IndexError("failed action is outside plan")
    return list(plan[:failed_index]) + list(replacement)


def bootstrap_error_certificate(task_errors, *, budget: float, confidence: float = 0.95, samples: int = 2000, seed: int = 0):
    """Task-cluster bootstrap upper error bound for selective automation."""
    import numpy as np

    errors = [np.asarray(values, dtype=np.float64) for values in task_errors]
    if not errors or not 0 < confidence < 1 or not 0 <= budget <= 1:
        raise ValueError("invalid clustered errors or certificate parameters")
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(samples):
        selected = rng.integers(0, len(errors), len(errors))
        values = np.concatenate([errors[index] for index in selected])
        means.append(values.mean())
    upper = float(np.quantile(means, confidence))
    return {"upper_error": upper, "certified": upper <= budget, "tasks": len(errors)}


def mnemon_view(records, query_terms, *, budget: int):
    """System-1 record judgments build a bounded raw-record view for answering."""
    if budget < 1:
        raise ValueError("budget must be positive")
    terms = {term.casefold() for term in query_terms}
    scored = []
    for index, record in enumerate(records):
        text = record["text"].casefold()
        score = sum(term in text for term in terms)
        scored.append((score, record.get("date", ""), -index, record))
    selected = [item[-1] for item in sorted(scored, reverse=True)[:budget] if item[0] > 0]
    return selected, {"records_scanned": len(records), "view_size": len(selected), "budget": budget}
