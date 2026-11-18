"""GSLM2 v1 §2.2/C.1.6 alignment and transition scoring, not a speech model."""

from collections.abc import Sequence
from dataclasses import dataclass
import itertools
import math
import random

REQUIRES_GPU_VALIDATION = False

Frames = Sequence[Sequence[int]]


@dataclass(frozen=True)
class RetainedUnits:
    frame_indices: tuple[int, ...]
    units: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class TransitionScore:
    mean_log_probability: float
    per_stream_log_probability: tuple[float, ...]
    per_stream_transitions: tuple[int, ...]


def _validated_frames(frames: Frames) -> tuple[tuple[int, ...], ...]:
    rows = tuple(tuple(row) for row in frames)
    if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("expected a nonempty rectangular frame-by-stream matrix")
    if any(type(unit) is not int or unit < 0 for row in rows for unit in row):
        raise ValueError("unit IDs must be nonnegative integers")
    return rows


def cross_stream_deduplicate(frames: Frames) -> RetainedUnits:
    """Keep frame zero and each change point in the union across aligned streams."""
    rows = _validated_frames(frames)
    indices = (0, *(t for t in range(1, len(rows)) if rows[t] != rows[t - 1]))
    return RetainedUnits(indices, tuple(rows[t] for t in indices))


def transition_log_score(
    units: Frames, target_log_probabilities: Sequence[Sequence[float]],
) -> TransitionScore:
    """Macro-average selected target log probabilities, including each first unit.

    Input rows must already be cross-stream deduplicated. Each column holds
    the stream-specific head's log probability of the observed target unit,
    conditioned on preceding *multi-stream* tuples. This routine does not
    compute logits, read correctness labels, or replace the generative head.
    """
    rows = _validated_frames(units)
    n_streams = len(rows[0])
    scores = tuple(tuple(row) for row in target_log_probabilities)
    if len(scores) != len(rows) or any(len(row) != n_streams for row in scores):
        raise ValueError("log probability shape must match retained units")
    if any(
        type(value) not in {int, float} or not math.isfinite(value) or value > 0
        for row in scores for value in row
    ):
        raise ValueError("expected finite, nonpositive target log probabilities")
    if any(a == b for a, b in itertools.pairwise(rows)):
        raise ValueError("units must already be cross-stream deduplicated")
    counts = [0] * n_streams
    for t, row in enumerate(rows):
        for stream, unit in enumerate(row):
            counts[stream] += t == 0 or unit != rows[t - 1][stream]
    per_stream = tuple(
        math.fsum(
            scores[t][stream] / counts[stream] for t, row in enumerate(rows)
            if t == 0 or row[stream] != rows[t - 1][stream]
        )
        for stream in range(n_streams)
    )
    return TransitionScore(
        math.fsum(value / n_streams for value in per_stream), per_stream, tuple(counts),
    )


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Deterministic synthetic controls; no checkpoint, audio, GPU or API."""
    if device != "cpu":
        raise ValueError("this reference component supports CPU only")
    rng = random.Random(seed)
    frames = [tuple(rng.randrange(5) for _ in range(3)) for _ in range(24)]
    frames = [row for row in frames for _ in range(rng.randrange(1, 4))]
    retained = cross_stream_deduplicate(frames)
    group_lengths = [sum(1 for _ in group) for _, group in itertools.groupby(frames)]
    expected_indices = tuple(itertools.accumulate((0, *group_lengths[:-1])))
    scores = [tuple(-rng.uniform(0.1, 7.0) for _ in row) for row in retained.units]
    result = transition_log_score(retained.units, scores)
    expected = []
    for stream, column in enumerate(zip(*retained.units, strict=True)):
        changes = tuple(itertools.accumulate(
            (0, *(sum(1 for _ in g) for _, g in itertools.groupby(column))),
        ))[:-1]
        expected.append(sum(scores[t][stream] for t in changes) / len(changes))
    error = abs(result.mean_log_probability - sum(expected) / len(expected))

    # Known unequal event counts: scoring all retained positions or taking a
    # micro-mean over events changes the intended answer.
    control = ((0, 0), (0, 1), (0, 2), (0, 3))
    control_scores = ((-4, -1), (-60, -2), (-50, -3), (-40, -4))
    macro = transition_log_score(control, control_scores)
    altered = transition_log_score(control, ((-4, -1), (-1, -2), (-1, -3), (-1, -4)))
    reverse = transition_log_score(
        tuple(row[::-1] for row in retained.units), tuple(row[::-1] for row in scores),
    )
    micro = (-4 - 1 - 2 - 3 - 4) / 5
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "retained_frames": len(retained.units),
            "raw_frames": len(frames),
            "macro_log_probability_reference_error": error,
            "macro_micro_control_gap": abs(macro.mean_log_probability - micro),
        },
        "checks": {
            "union_of_change_points": retained.frame_indices == expected_indices,
            "independent_stream_reference": error < 1e-12,
            "first_and_equal_stream_weight": macro.per_stream_transitions == (1, 4)
            and macro.mean_log_probability == -3.25,
            "ignored_repetitions": macro == altered,
            "stream_permutation": result.mean_log_probability == reverse.mean_log_probability,
        },
    }
