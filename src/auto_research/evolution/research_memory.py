from __future__ import annotations

import math


def verify_trial(trial, parent=None):
    """NOVA-style verification cascade for every executable evolve trial."""
    validation = trial.validation
    numeric = [
        value for value in validation.values()
        if isinstance(value, (int, float))
    ]
    gates = {
        "L1_contract": bool(trial.trial_id and trial.genome.architecture),
        "L2_execution": trial.status == "completed",
        "L3_numerical": bool(numeric) and all(math.isfinite(float(value)) for value in numeric),
        "L4_offline": trial.fitness > -1e8,
    }
    if parent is not None:
        gates["improves_parent"] = trial.fitness > parent.fitness
    return {
        "trial_id": trial.trial_id,
        "architecture": trial.genome.architecture,
        "passed": all(value for key, value in gates.items() if key != "improves_parent"),
        "gates": gates,
        "error": trial.error,
    }


def update_research_memory(memory, parent, children, champion, verification):
    """EvoRec-style persistent methodology distilled from completed trials."""
    successful, failed = memory.setdefault("successful_skills", []), memory.setdefault("forbidden_directions", [])
    gradients = memory.setdefault("architecture_gradients", [])
    for child in children:
        record = next(item for item in verification if item["trial_id"] == child.trial_id)
        delta = child.fitness - parent.fitness
        gradients.append({
            "trial_id": child.trial_id,
            "architecture": child.genome.architecture,
            "fitness_delta": delta,
            "passed_verification": record["passed"],
        })
        if record["passed"] and delta > 0:
            successful.append({
                "architecture": child.genome.architecture,
                "fitness_delta": delta,
                "source_trial": child.trial_id,
            })
        elif not record["passed"]:
            failed.append({
                "architecture": child.genome.architecture,
                "error": child.error or "verification cascade rejected candidate",
                "source_trial": child.trial_id,
            })
    memory["current_champion"] = champion.trial_id
    memory["generations_observed"] = max(
        int(memory.get("generations_observed", 0)), champion.generation
    )
    return memory


def methodology_order(architectures, memory):
    """Use learned skills to bias proposal order without hiding other candidates."""
    preferred = [
        item["architecture"]
        for item in reversed(memory.get("successful_skills", []))
    ]
    forbidden = {
        item["architecture"]
        for item in memory.get("forbidden_directions", [])
    }
    ordered = []
    for name in [*preferred, *architectures]:
        if name not in ordered and name not in forbidden:
            ordered.append(name)
    return ordered or list(architectures)
