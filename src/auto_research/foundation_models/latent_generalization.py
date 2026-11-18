"""Semantic-structure set metrics from 2604.01430 §3.3.

This is a completed-output evaluator, not Gemini knowledge acquisition, teacher
bootstrapping, REINFORCE training, or semantic judging.
"""
from __future__ import annotations

import numpy as np

from .thinking_to_recall import pass_at_k

REQUIRES_GPU_VALIDATION = False


def score_completion(predicted: set[str], all_answers: set[str], heldout: set[str], primary: str) -> dict[str, float]:
    """Exact strings, set semantics. Primary must be a designated held-out answer."""
    if any(not isinstance(v, set) or any(not isinstance(x, str) or not x for x in v) for v in [predicted, all_answers, heldout]) or not all_answers or not heldout or not heldout <= all_answers or primary not in heldout:
        raise ValueError("nonempty all/heldout answer sets, subset relation, and heldout primary required")
    exposed = all_answers - heldout
    tp = len(predicted & all_answers)
    precision = tp / len(predicted) if predicted else 0.
    recall = tp / len(all_answers)
    return {"overall_precision": precision, "overall_recall": recall,
            "overall_f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.,
            "train_recall": len(predicted & exposed) / len(exposed) if exposed else 0.,
            "heldout_recall": len(predicted & heldout) / len(heldout),
            "exact_set_match": float(predicted == all_answers), "primary_reference_inclusion": float(primary in predicted)}


def exact_set_pass_at_n(completions: list[set[str]], all_answers: set[str], n: int) -> float:
    if not completions or not all_answers:
        raise ValueError("completed independent attempts and nonempty gold set required")
    return pass_at_k(sum(p == all_answers for p in completions), len(completions), n)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU evaluator only")
    rng = np.random.default_rng(seed)
    correct = {"A", "B", "C"}; heldout = {"C"}
    partial = score_completion({"A", "B"}, correct, heldout, "C")
    over = score_completion(correct | {"false"}, correct, heldout, "C")
    samples = [correct.copy() if x < .5 else {"A"} for x in rng.random(10)]
    return {"seed": seed, "device": device, "metrics": {**partial, "exact_set_pass_at_2": exact_set_pass_at_n(samples, correct, 2)},
            "checks": {"exposed_recall_can_hide_heldout_failure": partial["train_recall"] == 1 and partial["heldout_recall"] == 0,
                       "false_inclusion_invalidates_exact_match": over["exact_set_match"] == 0 and over["heldout_recall"] == 1,
                       "primary_is_separate_from_overall": partial["primary_reference_inclusion"] == 0 and partial["overall_f1"] > 0},
            "diagnostic_only": True, "evaluation_tier": "l1_mechanism"}
