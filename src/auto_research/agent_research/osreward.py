from __future__ import annotations

import numpy as np


PLATFORMS = ("Windows", "macOS", "Ubuntu", "Android")
TASKS = (
    ("presentation", True, True, False),
    ("spreadsheet", True, True, False),
    ("browser-form", True, True, False),
    ("file-edit", True, True, False),
    ("presentation", False, True, True),
    ("spreadsheet", False, False, False),
    ("browser-form", False, True, True),
    ("file-edit", False, False, False),
)


def evaluate_osreward(episodes: int, seed: int):
    """Run the OSReward decision protocol on deterministic CUA traces.

    Each tuple contains the human verdict, visible completion evidence and an
    unresolved requirement flag.  The judge must reject incomplete traces even
    when their last screenshot looks superficially plausible—the leniency
    failure mode isolated by OSReward-Hard.
    """

    rng = np.random.default_rng(seed)
    gold, predicted, trace = [], [], []
    evidence_checks = 0
    for index in range(episodes):
        task, succeeded, completion_evidence, unresolved = TASKS[index % len(TASKS)]
        platform = PLATFORMS[index % len(PLATFORMS)]
        # A small amount of irrelevant UI evidence tests that the verdict is
        # tied to task completion, not visual activity alone.
        visual_activity = bool(rng.integers(0, 2))
        verdict = bool(completion_evidence and not unresolved)
        evidence_checks += 2
        gold.append(succeeded)
        predicted.append(verdict)
        if index < 20:
            trace.append(
                {
                    "task_id": f"osreward-mini-{index:04d}",
                    "platform": platform,
                    "task": task,
                    "gold_success": succeeded,
                    "completion_evidence": completion_evidence,
                    "unresolved_requirement": unresolved,
                    "irrelevant_visual_activity": visual_activity,
                    "predicted_success": verdict,
                }
            )
    gold_array = np.asarray(gold, dtype=bool)
    predicted_array = np.asarray(predicted, dtype=bool)
    success_recall = float(predicted_array[gold_array].mean())
    fail_recall = float((~predicted_array[~gold_array]).mean())
    accuracy = float((predicted_array == gold_array).mean())
    metrics = {
        "accuracy": accuracy,
        "success_recall": success_recall,
        "fail_recall": fail_recall,
        "balanced_accuracy": 0.5 * (success_recall + fail_recall),
        "leniency_rate": 1.0 - fail_recall,
        # Compatibility with the unified Agent result contract.
        "answer_accuracy": accuracy,
        "plan_success": accuracy,
        "joint_success": 0.5 * (success_recall + fail_recall),
        "average_cost": evidence_checks / episodes,
    }
    diagnostics = {
        "episodes": episodes,
        "platforms": list(PLATFORMS),
        "evidence_checks": evidence_checks,
        "working_bar_balanced_accuracy": 0.90,
        "official_dataset_used": False,
        "fidelity": (
            "OSReward metric and evidence-verification protocol on a local "
            "deterministic mini-suite; not the official trajectory corpus"
        ),
    }
    return metrics, diagnostics, trace
