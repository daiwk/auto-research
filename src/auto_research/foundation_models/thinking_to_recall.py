"""Offline conditional-expectation analysis, not an oracle actor (2603.09906 §5.4).

Truth annotations are consumed only after external generations have finished.
No function selects/returns a trace, prompt, action or training candidate.
"""
from __future__ import annotations

from math import comb

import numpy as np

REQUIRES_GPU_VALIDATION = False


def pass_at_k(correct: int, samples: int, k: int) -> float:
    if any(isinstance(v, bool) or not isinstance(v, int) for v in [correct, samples, k]) or not 0 <= correct <= samples or not 1 <= k <= samples:
        raise ValueError("integer counts with 0<=correct<=samples and 1<=k<=samples required")
    return 1. if samples - correct < k else 1. - comb(samples - correct, k) / comb(samples, k)


def conditional_expected_accuracy(answer_correct: np.ndarray, has_facts: np.ndarray,
                                  all_facts_correct: np.ndarray, *, samples_per_question: int = 100) -> dict:
    """Paper protocol: common nonempty-question mask, then question-macro means.

    All-facts-correct is vacuously true on empty-fact traces; intersecting with
    has_facts is essential. Dropped questions are reported, never silently scored.
    """
    arrays = [np.asarray(a) for a in [answer_correct, has_facts, all_facts_correct]]
    a, f, c = arrays
    if any(v.dtype != bool or v.ndim != 2 or v.shape != a.shape for v in arrays) or not a.shape[0] or a.shape[1] != samples_per_question or samples_per_question < 1:
        raise ValueError("matching nonempty boolean question×sample arrays required")
    masks = [np.ones_like(f), f, f & c]
    keep = np.logical_and.reduce([m.any(axis=1) for m in masks])
    if not keep.any():
        raise ValueError("no question has every required nonempty trace subset")
    rates = [((a & m).sum(axis=1)[keep] / m.sum(axis=1)[keep]).mean() for m in masks]
    return {"all_expected_accuracy": float(rates[0]), "factual_expected_accuracy": float(rates[1]),
            "correct_factual_expected_accuracy": float(rates[2]), "retained_questions": int(keep.sum()),
            "dropped_questions": int((~keep).sum()), "samples_per_question": samples_per_question,
            "offline_oracle_analysis": True, "runtime_selector_implemented": False}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU evaluator only")
    rng = np.random.default_rng(seed)
    correct = rng.random((3, 100)) < .5
    facts = np.ones_like(correct); facts[2] = False
    verified = correct.copy()
    result = conditional_expected_accuracy(correct, facts, verified)
    return {"seed": seed, "device": device, "metrics": {k: v for k, v in result.items() if isinstance(v, (int, float)) and not isinstance(v, bool)},
            "checks": {"shared_retained_questions": result["retained_questions"] == 2 and result["dropped_questions"] == 1,
                       "oracle_condition_is_explicit": result["offline_oracle_analysis"], "no_runtime_selector": not result["runtime_selector_implemented"],
                       "unbiased_passk_example": abs(pass_at_k(1, 2, 1) - .5) < 1e-12},
            "diagnostic_only": True, "evaluation_tier": "l1_mechanism"}
