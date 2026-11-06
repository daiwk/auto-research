"""CPU reference for GINGER's nested TurboQuant core (Sections 3.1–3.2).

Inputs are already rotated by a common orthogonal transform. This module
checks scalar codebooks, split streams, and reference inner products, not
graph navigation, the production rotation, or the Highway SIMD kernels.
"""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Sequence
from dataclasses import dataclass
from functools import lru_cache
import math
import random
from statistics import NormalDist


REQUIRES_GPU_VALIDATION = False
_SQRT_2 = math.sqrt(2)
_SQRT_2PI = math.sqrt(2 * math.pi)
_NORMAL = NormalDist()


def _tail(x: float) -> float:
    return 0.5 * math.erfc(x / _SQRT_2)


def _density(x: float) -> float:
    return math.exp(-0.5 * x * x) / _SQRT_2PI


def _moments(left: float, right: float) -> tuple[float, float, float]:
    """Unnormalized 0th, 1st and 2nd moments under N(0,1)."""
    mass = _tail(left) - _tail(right)
    phi_l, phi_r = _density(left), _density(right)
    upper = right * phi_r if math.isfinite(right) else 0.0
    return mass, phi_l - phi_r, mass + left * phi_l - upper


def _thresholds(centroids: tuple[float, ...]) -> tuple[float, ...]:
    return tuple((a + b) / 2 for a, b in zip(centroids, centroids[1:]))


def _lloyd_max(left: float, right: float, size: int) -> tuple[float, ...]:
    lo_tail, hi_tail = _tail(left), _tail(right)
    centers = tuple(
        -_NORMAL.inv_cdf(lo_tail - (lo_tail - hi_tail) * (i + 0.5) / size)
        for i in range(size)
    )
    for _ in range(12_000):
        edges = (left, *_thresholds(centers), right)
        moments = [_moments(a, b) for a, b in zip(edges, edges[1:])]
        next_centers = tuple(first / mass for mass, first, _ in moments)
        if max(abs(a - b) for a, b in zip(centers, next_centers)) < 1e-11:
            return next_centers
        centers = next_centers
    raise ArithmeticError("bounded Lloyd–Max solver did not converge")


def _distortion(centers: tuple[float, ...], edges: tuple[float, ...]) -> float:
    # Double the positive-half integral because the signed code is symmetric.
    moments = [_moments(a, b) for a, b in zip(edges, edges[1:])]
    return 2 * math.fsum(
        second - 2 * center * first + center * center * mass
        for center, (mass, first, second) in zip(centers, moments, strict=True)
    )


@dataclass(frozen=True)
class Codebook:
    refinement_bits: int
    coarse: tuple[float, ...]
    coarse_thresholds: tuple[float, ...]
    fine: tuple[tuple[float, ...], ...]
    fine_thresholds: tuple[tuple[float, ...], ...]
    coarse_distortion: float
    fine_distortion: float


def build_codebook(refinement_bits: int = 2) -> Codebook:
    """Fit Gaussian cells with a fixed 4-bit prefix; support 1–4 extra bits."""
    if type(refinement_bits) is not int or not 1 <= refinement_bits <= 4:
        raise ValueError("reference supports 1–4 refinement bits")
    return _codebook(refinement_bits)


@lru_cache(maxsize=4)
def _codebook(bits: int) -> Codebook:
    coarse = _lloyd_max(0.0, math.inf, 8)
    cuts = _thresholds(coarse)
    edges = (0.0, *cuts, math.inf)
    fine = tuple(_lloyd_max(a, b, 1 << bits) for a, b in zip(edges, edges[1:]))
    fine_cuts = tuple(_thresholds(row) for row in fine)
    return Codebook(
        bits, coarse, cuts, fine, fine_cuts, _distortion(coarse, edges),
        math.fsum(
            _distortion(row, (left, *thresholds, right))
            for row, thresholds, left, right in zip(
                fine, fine_cuts, edges[:-1], edges[1:], strict=True,
            )
        ),
    )


def _pack(codes: Sequence[int], bits: int) -> bytes:
    out = bytearray()
    buffer = used = 0
    for code in codes:
        buffer |= code << used
        used += bits
        if used >= 8:
            out.append(buffer & 255)
            buffer >>= 8
            used -= 8
    if used:
        out.append(buffer)
    return bytes(out)


def _unpack(data: bytes, bits: int, size: int) -> tuple[int, ...]:
    if len(data) != (bits * size + 7) // 8:
        raise ValueError("wrong stream length")
    mask = (1 << bits) - 1
    if (used := (bits * size) % 8) and data[-1] >> used:
        raise ValueError("nonzero padding bits")
    out = []
    buffer = ready = cursor = 0
    for _ in range(size):
        if ready < bits:
            buffer |= data[cursor] << ready
            ready += 8
            cursor += 1
        out.append(buffer & mask)
        buffer >>= bits
        ready -= bits
    return tuple(out)


@dataclass(frozen=True)
class NavigationCode:
    dimension: int
    packed: bytes
    scale: float


@dataclass(frozen=True)
class NestedCode:
    navigation: NavigationCode
    refinement: bytes
    refinement_bits: int
    scale: float


def encode(rotated_vector: Sequence[float], book: Codebook) -> NestedCode:
    """Encode a nonzero Rx; navigation bytes do not depend on fine precision."""
    vector = tuple(rotated_vector)
    norm = math.hypot(*vector)
    if not norm or not math.isfinite(norm):
        raise ValueError("rotated vector must have finite, nonzero norm")
    coarse, fine = [], []
    coarse_values, fine_values = [], []
    for value in vector:
        coord = abs(value / norm) * math.sqrt(len(vector))
        u = bisect_right(book.coarse_thresholds, coord)
        v = bisect_right(book.fine_thresholds[u], coord)
        coarse.append(u | (8 if value < 0 else 0))
        fine.append(v)
        coarse_values.append(book.coarse[u])
        fine_values.append(book.fine[u][v])
    coarse_scale = norm / (math.sqrt(1 - book.coarse_distortion) * math.hypot(*coarse_values))
    fine_scale = norm / (math.sqrt(1 - book.fine_distortion) * math.hypot(*fine_values))
    if not all(math.isfinite(scale) and scale > 0 for scale in (coarse_scale, fine_scale)):
        raise ValueError("vector scale is not representable")
    return NestedCode(
        NavigationCode(len(vector), _pack(coarse, 4), coarse_scale),
        _pack(fine, book.refinement_bits), book.refinement_bits, fine_scale,
    )


def decode_navigation(code: NavigationCode, book: Codebook) -> tuple[float, ...]:
    """Decode the 4-bit stream and its own scale, without reading refinement."""
    return tuple(
        (-1 if nibble & 8 else 1) * code.scale * book.coarse[nibble & 7]
        for nibble in _unpack(code.packed, 4, code.dimension)
    )


def decode_refined(code: NestedCode, book: Codebook) -> tuple[float, ...]:
    """Decode the nested representation into the rotated space for reranking."""
    if code.refinement_bits != book.refinement_bits:
        raise ValueError("code and refinement codebook must use the same bit width")
    base = _unpack(code.navigation.packed, 4, code.navigation.dimension)
    extra = _unpack(code.refinement, book.refinement_bits, code.navigation.dimension)
    return tuple(
        (-1 if n & 8 else 1) * code.scale * book.fine[n & 7][v]
        for n, v in zip(base, extra, strict=True)
    )


def inner_product(rotated_query: Sequence[float], reconstructed: Sequence[float]) -> float:
    """Section 3.1 full-precision query score; not the int8/AVX-512 kernel."""
    if not rotated_query or len(rotated_query) != len(reconstructed):
        raise ValueError("query and reconstruction must have the same nonzero dimension")
    score = math.fsum(q * x for q, x in zip(rotated_query, reconstructed, strict=True))
    if not math.isfinite(score):
        raise ValueError("inner product must be finite")
    return score


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("GINGER reference is CPU-only")
    book = build_codebook(2)
    other = build_codebook(1)
    rng = random.Random(seed)
    count, dimension = 192, 31
    vectors = [tuple(rng.gauss(0, 1) for _ in range(dimension)) for _ in range(count)]
    mse4 = mse6 = 0.0
    same_prefix = True
    for vec in vectors:
        code = encode(vec, book)
        same_prefix &= code.navigation == encode(vec, other).navigation
        coarse, fine = decode_navigation(code.navigation, book), decode_refined(code, book)
        mse4 += math.fsum((a - b) ** 2 for a, b in zip(vec, coarse, strict=True))
        mse6 += math.fsum((a - b) ** 2 for a, b in zip(vec, fine, strict=True))
    mse4 /= count * dimension
    mse6 /= count * dimension
    edges = (0.0, *book.coarse_thresholds, math.inf)
    nested = all(
        left < row[0] and row[-1] < right and tuple(sorted(row)) == row
        for row, left, right in zip(book.fine, edges[:-1], edges[1:], strict=True)
    )
    sample = encode((2.0, -2.0), book)
    u = bisect_right(book.coarse_thresholds, 1.0)
    v = bisect_right(book.fine_thresholds[u], 1.0)
    expected = 2.0 * book.fine[u][v] * sample.scale
    observed = inner_product((1.0, -1.0), decode_refined(sample, book))
    hand_error = abs(observed - expected)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "vectors": count, "dimension": dimension, "refinement_bits": book.refinement_bits,
            "gaussian_distortion_4bit": book.coarse_distortion,
            "gaussian_distortion_6bit": book.fine_distortion,
            "synthetic_mse_4bit": mse4, "synthetic_mse_6bit": mse6,
            "hand_score_absolute_error": hand_error,
            "navigation_bytes_per_vector": len(code.navigation.packed),
            "refinement_bytes_per_vector": len(code.refinement),
        },
        "checks": {
            "fine_cells_stay_in_coarse_interval": nested,
            "prefix_independent_of_refinement": same_prefix,
            "two_signed_nibbles_match_hand_pack": sample.navigation.packed == bytes([u | ((u | 8) << 4)]),
            "two_refinement_indices_match_hand_pack": sample.refinement == bytes([v | (v << 2)]),
            "full_precision_query_score_matches_hand": hand_error < 1e-12,
            "gaussian_refinement_reduces_distortion": 0 < book.fine_distortion < book.coarse_distortion < 1,
            "gaussian_probe_refinement_reduces_mse": 0 < mse6 < mse4,
        },
    }
