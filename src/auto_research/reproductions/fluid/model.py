from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes


def build_lucid(data, seed: int, levels: int = 3, width: int = 8):
    """Cross-domain content proxy -> slice/room RQ codes -> prefix IDs."""
    content = data.sequences.features.astype(np.float64)
    collaborative = data.transition @ content
    popularity = data.popularity[:, None]
    fused = np.concatenate((content, collaborative, popularity), axis=1)
    fused /= np.linalg.norm(fused, axis=1, keepdims=True).clip(1e-9)
    rng = np.random.default_rng(seed)
    slices = np.stack([
        fused + rng.normal(0, 0.025 + 0.01 * index, fused.shape)
        for index in range(4)
    ], axis=1)
    flat_codes = hierarchical_codes(slices.reshape(-1, slices.shape[-1]), levels, width, seed)
    slice_codes = flat_codes.reshape(len(fused), len(slices[0]), levels)
    room_codes = np.empty((len(fused), levels), dtype=np.int64)
    for item in range(len(fused)):
        for level in range(levels):
            room_codes[item, level] = np.bincount(slice_codes[item, :, level], minlength=width).argmax()
    current_slice = slice_codes[:, -1]
    return fused, prefix_ids(current_slice, width), prefix_ids(room_codes, width), slice_codes


def prefix_ids(codes: np.ndarray, width: int) -> np.ndarray:
    result = np.zeros_like(codes)
    for level in range(codes.shape[1]):
        result[:, level] = codes[:, level]
        if level:
            result[:, level] += width * result[:, level - 1]
    return result


def train_prefix_tables(data, prefix: np.ndarray):
    tables = []
    for level in range(prefix.shape[1]):
        size = int(prefix[:, level].max()) + 1
        table = np.ones((size, size), dtype=np.float64) * 1e-3
        for sequence in data.sequences.train:
            for left, right in zip(sequence, sequence[1:]):
                table[prefix[left, level], prefix[right, level]] += 1.0
        table /= table.sum(axis=1, keepdims=True)
        tables.append(table)
    return tuple(tables)


def lucid_score(data, fused, slice_prefix, room_prefix, slice_tables, room_tables, history, use_room: bool):
    recent = list(history[-8:])
    content = fused @ fused[recent].mean(axis=0)
    slice_score = np.zeros(data.item_count)
    room_score = np.zeros(data.item_count)
    for level, table in enumerate(slice_tables):
        slice_score += np.mean(table[slice_prefix[recent, level]], axis=0)[slice_prefix[:, level]]
    if use_room:
        for level, table in enumerate(room_tables):
            room_score += np.mean(table[room_prefix[recent, level]], axis=0)[room_prefix[:, level]]
    slice_score /= len(slice_tables)
    room_score /= max(len(room_tables), 1)
    return 0.35 * content + (0.40 if use_room else 0.65) * slice_score + (0.25 * room_score if use_room else 0.0)
