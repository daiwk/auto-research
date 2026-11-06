"""Scalar CPU reference for the decoded-byte score/top-K slice of PiPNN II."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
import heapq
import math
import random


REQUIRES_GPU_VALIDATION = False


def _i8_row(values: Sequence[int]) -> tuple[int, ...]:
    row = tuple(values)
    if not row or any(type(value) is not int or not -128 <= value <= 127 for value in row):
        raise ValueError("a nonempty row of decoded signed bytes is required")
    return row


def _positive_scale(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("scale must be a finite positive number")
    try:
        value = float(value)
    except OverflowError as exc:
        raise ValueError("scale must be a finite positive number") from exc
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError("scale must be a finite positive number")
    return value


def _corrected_dot(query: tuple[int, ...], database: tuple[int, ...], bias: int) -> int:
    if len(query) != len(database):
        raise ValueError("query and database dimensions must agree")
    unsigned_signed = sum((value + 128) * q for q, value in zip(query, database, strict=True))
    return unsigned_signed - bias


def corrected_dot(query: Sequence[int], database: Sequence[int]) -> int:
    """Apply the §4.1 u8 offset correction to one pair of decoded i8 rows."""
    q, db = _i8_row(query), _i8_row(database)
    return _corrected_dot(q, db, 128 * sum(q))


def fused_quantized_topk(
    query: Sequence[int],
    query_scale: float,
    database: Iterable[tuple[Sequence[int], float]],
    *,
    k: int,
) -> tuple[tuple[int, float], ...]:
    """Apply Algorithm 2's score epilogue and retain the smallest K scores.

    Database rows are read once. Only K pairs remain in the heap, with ties
    broken by input position. This is scalar reference arithmetic using
    decoded bytes, not a TurboQuant decoder, SIMD/AMX kernel or graph build.
    """
    if type(k) is not int or k <= 0:
        raise ValueError("k must be a positive integer")
    q, sigma_q = _i8_row(query), _positive_scale(query_scale)
    bias = 128 * sum(q)
    heap: list[tuple[float, int]] = []
    for index, (row, scale) in enumerate(database):
        dot = _corrected_dot(q, _i8_row(row), bias)
        score = -dot * _positive_scale(scale) * sigma_q
        if not math.isfinite(score):
            raise ValueError("rescaled score is outside finite floating-point range")
        item = (-score, -index)
        if len(heap) < k:
            heapq.heappush(heap, item)
        elif item > heap[0]:
            heapq.heapreplace(heap, item)
    if len(heap) != k:
        raise ValueError("k must not exceed the number of database rows")
    return tuple((-index, -score) for score, index in sorted(heap, reverse=True))


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Compare the score stream against independent signed-dot dense ranking."""
    if device != "cpu":
        raise ValueError("PiPNN II decoded-byte reference is CPU-only")
    rng = random.Random(seed)
    dimension, count, k = 11, 23, 4
    query = [rng.randrange(-128, 128) for _ in range(dimension)]
    sigma_q = 0.125
    rows = [([rng.randrange(-128, 128) for _ in range(dimension)], rng.randrange(1, 9) / 16)
            for _ in range(count)]
    dense_dots = [sum(q * d for q, d in zip(query, row, strict=True)) for row, _ in rows]
    reference = sorted(
        ((i, -dense_dots[i] * sigma_d * sigma_q) for i, (_, sigma_d) in enumerate(rows)),
        key=lambda pair: (pair[1], pair[0]),
    )[:k]
    actual = fused_quantized_topk(query, sigma_q, iter(rows), k=k)
    error = max(abs(a[1] - b[1]) for a, b in zip(actual, reference, strict=True))
    dot_error = max(abs(corrected_dot(query, row) - target)
                    for (row, _), target in zip(rows, dense_dots, strict=True))
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "integer_dot_max_error": dot_error,
            "topk_score_max_error": error,
            "database_rows_scored": count,
            "candidates_retained": len(actual),
        },
        "checks": {
            "offset_correction_matches_signed_dot": dot_error == 0,
            "streaming_topk_matches_dense_reference": actual == tuple(reference),
            "nonzero_bias_matters": corrected_dot([1], [3]) == 3 and (3 + 128) * 1 != 3,
            "rescaling_affects_rank": fused_quantized_topk([1], 1.0, [([3], 0.5), ([2], 1.0)], k=1)
            == ((1, -2.0),),
            "ties_use_input_position": fused_quantized_topk([1], 1.0, [([3], 1.0)] * 3, k=2)
            == ((0, -3.0), (1, -3.0)),
        },
    }
