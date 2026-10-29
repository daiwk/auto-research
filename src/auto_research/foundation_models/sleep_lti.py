"""Sleep v2 Eqs.3–4 reward kernel only; no semantic judge, CMS or model.

Inputs are already tokenized continuations. The semantic label is supplied by
an external frozen judge, not guessed from lexical overlap or gold actions.
"""
from __future__ import annotations

import math
import random
from collections.abc import Sequence


def edit_distance(left: Sequence[int], right: Sequence[int]) -> int:
    for sequence in (left, right):
        if (not isinstance(sequence, (list, tuple)) or not 1 <= len(sequence) <= 2048
                or any(type(token) is not int or token < 0 for token in sequence)):
            raise ValueError("nonempty bounded token-id lists required; empty/empty is undefined in Eq4")
    previous = list(range(len(right) + 1))
    for i, a in enumerate(left, 1):
        current = [i]
        for j, b in enumerate(right, 1):
            current.append(min(current[-1] + 1, previous[j] + 1,
                               previous[j - 1] + (a != b)))
        previous = current
    return previous[-1]


def lti_reward(student_tokens: Sequence[int], teacher_tokens: Sequence[int], *,
               semantic_match: int, gamma: float, threshold: int) -> dict:
    """Inclusive absolute edit-count threshold, normalized by max length.

    Semantic and lexical branches are independent; a threshold failure must
    NOT zero an externally established semantic match. No judge is implemented.
    """
    if (type(semantic_match) is not int or semantic_match not in (0, 1) or isinstance(gamma, bool)
            or not math.isfinite(gamma) or not 0 <= gamma <= 1
            or type(threshold) is not int or not 0 <= threshold <= 2048):
        raise ValueError("binary frozen semantic label, gamma in [0,1], integer edit-count threshold required")
    distance = edit_distance(student_tokens, teacher_tokens)
    lexical = 1 - distance / max(len(student_tokens), len(teacher_tokens)) if distance <= threshold else 0.
    return {"reward": gamma * semantic_match + (1 - gamma) * lexical,
            "semantic_reward": semantic_match, "absolute_reward": lexical,
            "edit_distance": distance}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("this string/token contract is CPU-only, not a CUDA path")
    rng = random.Random(seed)
    reference = [rng.randrange(50) for _ in range(6)]
    changed = reference.copy()
    changed[2] = 100
    result = lti_reward(changed, reference, semantic_match=1, gamma=.4, threshold=1)
    threshold_fail = lti_reward(changed, reference, semantic_match=1, gamma=.4, threshold=0)
    insert = lti_reward(reference + [100], reference, semantic_match=0, gamma=.4, threshold=1)
    exact = lti_reward(reference, reference, semantic_match=0, gamma=.4, threshold=0)
    return {"seed": seed, "metrics": {"single_edit_reward": result["reward"],
             "over_threshold_reward": threshold_fail["reward"],
             "insertion_absolute_reward": insert["absolute_reward"],
             "exact_lexical_without_semantic": exact["reward"]},
            "checks": {"inclusive_threshold": result["edit_distance"] == 1 and abs(result["absolute_reward"] - 5/6) < 1e-12,
                       "semantic_branch_survives": threshold_fail["reward"] == .4,
                       "max_length_normalizer": abs(insert["absolute_reward"] - 6/7) < 1e-12,
                       "lexical_not_semantic_proxy": exact["semantic_reward"] == 0 and exact["reward"] == .6,
                       "distance_symmetry": edit_distance(reference, changed) == edit_distance(changed, reference)}}
