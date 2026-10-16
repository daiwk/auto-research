"""Causal two-byte novelty patching (arXiv:2610.22100, Section 3).

The future-looking LZ target is a *training label*, never an online feature.
This module is a patch-boundary component, not a trained BLT reproduction.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Iterable

import numpy as np


def novelty_targets(data: bytes, *, window: int = 128, cap: int = 16) -> np.ndarray:
    """Return -longest matching prefix starting within the preceding window.

    As in the paper's LZ77 definition, the earlier match may overlap the
    current position. Matching cannot extend beyond the supplied document.
    This function deliberately has no role in inference.
    """
    if not isinstance(data, bytes) or window < 1 or cap < 1:
        raise ValueError("expected bytes and positive window/cap")
    result = np.zeros(len(data), dtype=np.float64)
    for t in range(1, len(data)):
        low, high = 0, min(cap, len(data) - t)
        while low < high:
            length = (low + high + 1) // 2
            # end makes the latest eligible *start* t-1, allowing LZ overlap.
            if data.find(data[t:t + length], max(0, t - window), t + length - 1) >= 0:
                low = length
            else:
                high = length - 1
        result[t] = -low
    return result


def _documents(documents: bytes | Iterable[bytes]) -> tuple[bytes, ...]:
    docs = (documents,) if isinstance(documents, bytes) else tuple(documents)
    if not docs or any(not isinstance(doc, bytes) or not doc for doc in docs):
        raise ValueError("nonempty byte documents are required")
    return docs


def document_fingerprint(documents: bytes | Iterable[bytes]) -> str:
    """Length-framed hash preserves document boundaries, including UTF-8 bytes."""
    digest = hashlib.sha256()
    for doc in _documents(documents):
        digest.update(len(doc).to_bytes(8, "big"))
        digest.update(doc)
    return digest.hexdigest()


@dataclass(frozen=True)
class NoveltyTable:
    two_byte: np.ndarray
    one_byte: np.ndarray
    two_byte_counts: np.ndarray
    one_byte_counts: np.ndarray
    global_mean: float
    min_count: int
    window: int
    cap: int
    training_fingerprint: str

    def next_score(self, past: bytes) -> float:
        """Score the boundary *after* past; no current/future byte is accepted."""
        if not isinstance(past, bytes):
            raise ValueError("past must be bytes")
        if len(past) >= 2:
            return float(self.two_byte[past[-2] * 256 + past[-1]])
        if past:
            return float(self.one_byte[past[-1]])
        return self.global_mean

    def scores(self, data: bytes) -> np.ndarray:
        """Boundary at t reads only data[:t], including for t=0 and t=1."""
        if not isinstance(data, bytes):
            raise ValueError("data must be bytes")
        out = np.full(len(data), self.global_mean, dtype=np.float64)
        byte = np.frombuffer(data, dtype=np.uint8).astype(np.int64)
        if len(data) > 1:
            out[1] = self.one_byte[byte[0]]
        if len(data) > 2:
            out[2:] = self.two_byte[byte[:-2] * 256 + byte[1:-1]]
        return out

    def boundaries(self, data: bytes, threshold: float) -> np.ndarray:
        if math.isnan(threshold):
            raise ValueError("threshold must not be NaN")
        return self.scores(data) > threshold


def fit_novelty_table(documents: bytes | Iterable[bytes], *, min_count: int = 20,
                      window: int = 128, cap: int = 16) -> NoveltyTable:
    """Fit two-byte means, backing off to one byte then the global mean.

    Input must be a training split. Document boundaries reset the 128-byte
    history; low-frequency means are not used, exactly as in Section 3.
    """
    if min_count < 1:
        raise ValueError("min_count must be positive")
    docs = _documents(documents)
    counts2 = np.zeros(65536, dtype=np.int64)
    sums2 = np.zeros(65536, dtype=np.float64)
    counts1 = np.zeros(256, dtype=np.int64)
    sums1 = np.zeros(256, dtype=np.float64)
    total, count = 0., 0
    for data in docs:
        target = novelty_targets(data, window=window, cap=cap)
        byte = np.frombuffer(data, dtype=np.uint8).astype(np.int64)
        contexts2 = byte[:-2] * 256 + byte[1:-1]
        counts2 += np.bincount(contexts2, minlength=65536)
        sums2 += np.bincount(contexts2, weights=target[2:], minlength=65536)
        counts1 += np.bincount(byte[:-1], minlength=256)
        sums1 += np.bincount(byte[:-1], weights=target[1:], minlength=256)
        total += float(target.sum())
        count += len(data)
    mean = total / count
    one = np.full(256, mean)
    np.divide(sums1, counts1, out=one, where=counts1 >= min_count)
    two = one[np.arange(65536) % 256].copy()
    np.divide(sums2, counts2, out=two, where=counts2 >= min_count)
    return NoveltyTable(two, one, counts2, counts1, mean, min_count, window, cap,
                        document_fingerprint(docs))


@dataclass(frozen=True)
class ThresholdCalibration:
    threshold: float
    target_rate: float
    achieved_rate: float
    training_bytes: int
    training_fingerprint: str


def calibrate_threshold(table: NoveltyTable, training_documents: bytes | Iterable[bytes],
                        target_rate: float = .1) -> ThresholdCalibration:
    """Choose the closest *realizable* rate under strict score > threshold.

    A table has tied scores, so an arbitrary target need not be attainable.
    We report that mismatch rather than use future bytes/random tie breaking.
    No validation or test bytes are required or accessed by this procedure.
    """
    if not math.isfinite(target_rate) or not 0 <= target_rate <= 1:
        raise ValueError("target_rate must be in [0,1]")
    docs = _documents(training_documents)
    score = np.concatenate([table.scores(doc) for doc in docs])
    values, counts = np.unique(score, return_counts=True)
    rates = np.r_[1., 1. - np.cumsum(counts) / len(score)]
    # For ties in calibration error prefer the smaller rate (lower compute).
    order = np.lexsort((rates, np.abs(rates - target_rate)))
    chosen = int(order[0])
    threshold = float(np.nextafter(values[0], -np.inf)) if chosen == 0 else float(values[chosen - 1])
    return ThresholdCalibration(threshold, target_rate, float(rates[chosen]), len(score),
                                document_fingerprint(docs))
