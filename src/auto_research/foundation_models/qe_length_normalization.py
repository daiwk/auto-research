"""2510.22028 section 4.2: train on error density, rescale at inference.

This is a target/protocol component, not a pretrained translation evaluator.
The paper does not fix a tokenizer for |h|; callers must declare one unit and
reuse it at training and inference. Dividing a frozen metric is not debiasing.
"""
from __future__ import annotations

import math
from collections.abc import Sequence

REQUIRES_GPU_VALIDATION = False


def _vector(values: Sequence[float], *, positive: bool = False) -> tuple[float, ...]:
    result = tuple(float(v) for v in values)
    if not result or not all(math.isfinite(v) and (not positive or v > 0) for v in result):
        raise ValueError("nonempty finite values and positive lengths required")
    return result


def density_targets(ratings, lengths, *, length_unit: str):
    if not isinstance(length_unit, str) or not length_unit.strip():
        raise ValueError("explicit consistent hypothesis-length unit required")
    ratings, lengths = _vector(ratings), _vector(lengths, positive=True)
    if len(ratings) != len(lengths):
        raise ValueError("one length per rating required")
    return tuple(r / n for r, n in zip(ratings, lengths))


def restore_ratings(predicted_densities, lengths, *, length_unit: str):
    if not isinstance(length_unit, str) or not length_unit.strip():
        raise ValueError("explicit consistent hypothesis-length unit required")
    values, lengths = _vector(predicted_densities), _vector(lengths, positive=True)
    if len(values) != len(lengths):
        raise ValueError("one length per prediction required")
    return tuple(d * n for d, n in zip(values, lengths))


def controlled_passages(segments: Sequence[str], prefix_token_counts: Sequence[int], *, token_cap: int = 500):
    """Section 3.2: five consecutive same-document prefixes, whole-group cap.

    Counts must be computed by the caller on each concatenated prefix using the
    fixed tokenizer. Summing independent segment token counts is not equivalent.
    """
    if len(segments) < 5 or len(prefix_token_counts) != 5 or type(token_cap) is not int or token_cap <= 0:
        raise ValueError("five prefix token counts and at least five segments required")
    if any(not isinstance(x, str) or not x.strip() for x in segments[:5]):
        raise ValueError("nonempty ordered same-document segments required")
    if any(type(n) is not int or n <= 0 for n in prefix_token_counts):
        raise ValueError("positive tokenizer-derived counts required")
    if any(a > b for a, b in zip(prefix_token_counts, prefix_token_counts[1:])):
        raise ValueError("prefix counts must be nondecreasing")
    if prefix_token_counts[-1] > token_cap:
        return ()
    return tuple(" ".join(segments[:i]) for i in range(1, 6))


def within_document_differences(scores):
    values = _vector(scores)
    if len(values) != 5:
        raise ValueError("the five controlled passage scores are required")
    return tuple(value - values[0] for value in values)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU protocol execution required")
    ratings, lengths = (-1., -5., -7.), (10., 25., 35.)
    density = density_targets(ratings, lengths, length_unit="caller-fixed tokens")
    restored = restore_ratings(density, lengths, length_unit="caller-fixed tokens")
    passages = controlled_passages(["one", "two", "three", "four", "five"], [1, 2, 3, 4, 5])
    drift = within_document_differences([0., -1., -2., -3., -4.])
    checks = {"training_target_round_trip": restored == ratings,
              "whole_document_prefixes": passages[-1] == "one two three four five",
              "whole_group_rejected_above_cap": controlled_passages(["x"] * 5, [1, 2, 3, 4, 501]) == (),
              "bias_is_within_document": drift == (0., -1., -2., -3., -4.)}
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"max_round_trip_error": max(abs(a-b) for a, b in zip(ratings, restored)),
                        "controlled_passages": len(passages), "pretrained_model_calls": 0}, "checks": checks}
