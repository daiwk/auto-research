from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..prompt_generation.data import PGExample, load_office_dataset


SID = re.compile(r"<([abc])_(\d+)>")


@dataclass(frozen=True)
class UniVAData:
    train: tuple[tuple[tuple[int, ...], int], ...]
    validation: tuple[tuple[tuple[int, ...], int], ...]
    test: tuple[tuple[tuple[int, ...], int], ...]
    semantic_codes: np.ndarray
    commercial_codes: np.ndarray
    bids: np.ndarray
    ecpm: np.ndarray
    popularity: np.ndarray
    item_count: int
    commercial_stats: dict[str, float | int]
    source: Path


def load_univa_data(
    root: Path,
    train_limit: int,
    evaluation_users: int,
    commercial_budget: int,
    seed: int,
) -> UniVAData:
    raw = load_office_dataset(root, train_limit=train_limit)
    semantic = np.zeros((len(raw.item_sids), 3), dtype=np.int64)
    for item, value in raw.item_sids.items():
        parsed = {level: int(token) for level, token in SID.findall(value)}
        semantic[item] = (parsed["a"], parsed["b"], parsed["c"])
    popularity = np.ones(len(semantic), dtype=np.float64)
    for example in raw.train:
        popularity[example.target_id] += 1
    embeddings = np.load(
        raw.source / "index" / "Office_Products.emb-qwen-td.npy", mmap_mode="r"
    )
    attributes, bids = _commercial_attributes(raw.items, popularity, embeddings, seed)
    commercial, stats = commercial_sid(attributes, bids, commercial_budget)
    commercial_codes = np.column_stack((semantic[:, :2], commercial))
    ecpm = np.log1p(popularity) * (0.7 + 0.3 * _unit_scale(bids))
    ecpm /= max(float(ecpm.max()), 1e-12)
    return UniVAData(
        train=tuple((_history(row), row.target_id) for row in raw.train),
        validation=_select(raw.validation, evaluation_users, seed),
        test=_select(raw.test, evaluation_users, seed + 1),
        semantic_codes=semantic,
        commercial_codes=commercial_codes,
        bids=bids,
        ecpm=ecpm,
        popularity=popularity,
        item_count=len(semantic),
        commercial_stats=stats,
        source=raw.source,
    )


def commercial_sid(
    attributes: np.ndarray, bids: np.ndarray, budget: int
) -> tuple[np.ndarray, dict[str, float | int]]:
    keys = [tuple(int(value) for value in row) for row in attributes]
    grouped: dict[tuple[int, ...], list[int]] = {}
    for index, key in enumerate(keys):
        grouped.setdefault(key, []).append(index)
    if len(grouped) > budget:
        raise ValueError("commercial vocabulary budget is smaller than attribute keys")
    bins = {key: 1 for key in grouped}
    remaining = budget - len(grouped)
    while remaining:
        candidates = [key for key, rows in grouped.items() if bins[key] < min(8, len(rows))]
        if not candidates:
            break
        selected = max(candidates, key=lambda key: len(grouped[key]) / bins[key])
        bins[selected] += 1
        remaining -= 1
    tokens = np.zeros(len(keys), dtype=np.int64)
    offset = 0
    entropy = 0.0
    for key in sorted(grouped):
        indices = np.asarray(grouped[key], dtype=np.int64)
        order = indices[np.argsort(bids[indices], kind="stable")]
        partitions = np.array_split(order, bins[key])
        for local, partition in enumerate(partitions):
            tokens[partition] = offset + local
            probability = len(partition) / len(indices)
            if probability:
                entropy -= (len(indices) / len(attributes)) * probability * np.log(probability)
        offset += bins[key]
    return tokens, {
        "attribute_keys": len(grouped),
        "vocabulary_size": offset,
        "weighted_entropy": float(entropy),
    }


def path_bid_dispersion(codes: np.ndarray, bids: np.ndarray) -> dict[str, float]:
    groups: dict[tuple[int, ...], list[float]] = {}
    for code, bid in zip(codes, bids):
        groups.setdefault(tuple(int(value) for value in code), []).append(float(bid))
    stds = [float(np.std(values)) for values in groups.values() if len(values) > 1]
    ranges = [float(max(values) - min(values)) for values in groups.values() if len(values) > 1]
    return {
        "mean_std": float(np.mean(stds)) if stds else 0.0,
        "p75_std": float(np.percentile(stds, 75)) if stds else 0.0,
        "mean_range": float(np.mean(ranges)) if ranges else 0.0,
        "p75_range": float(np.percentile(ranges, 75)) if ranges else 0.0,
    }


def _commercial_attributes(items, popularity, embeddings, seed):
    brands = [str(items[index].get("brand", "")).strip().lower() for index in range(len(items))]
    counts: dict[str, int] = {}
    for brand in brands:
        counts[brand] = counts.get(brand, 0) + 1
    top = {brand: index for index, (brand, _) in enumerate(sorted(counts.items(), key=lambda row: (-row[1], row[0]))[:3])}
    goals = np.asarray([top.get(brand, 3) for brand in brands], dtype=np.int64)
    roi_edges = np.quantile(popularity, (1 / 3, 2 / 3))
    roi = np.digitize(popularity, roi_edges, right=True).astype(np.int64)
    rng = np.random.default_rng(seed)
    projection = rng.normal(size=(embeddings.shape[1], 8)).astype(np.float32)
    reduced = np.asarray(embeddings, dtype=np.float32) @ projection
    industry = _kmeans(reduced, 4, seed)
    semantic_value = _unit_scale(reduced[:, 0])
    bids = np.log1p(popularity) * (0.8 + 0.4 * semantic_value)
    return np.column_stack((goals, roi, industry)), bids


def _kmeans(values, clusters, seed, iterations=20):
    rng = np.random.default_rng(seed)
    centers = values[rng.choice(len(values), clusters, replace=False)].copy()
    labels = np.zeros(len(values), dtype=np.int64)
    for _ in range(iterations):
        labels = ((values[:, None] - centers[None]) ** 2).sum(-1).argmin(-1)
        for index in range(clusters):
            members = values[labels == index]
            if len(members):
                centers[index] = members.mean(0)
    return labels


def _select(rows: tuple[PGExample, ...], count: int, seed: int):
    ordered = sorted(
        rows,
        key=lambda row: hashlib.sha256(
            f"{seed}:{row.user_id}:{row.target_id}:{len(row.history_ids)}".encode()
        ).digest(),
    )
    return tuple((_history(row), row.target_id) for row in ordered[:count])


def _history(row: PGExample) -> tuple[int, ...]:
    return row.history_ids[-20:]


def _unit_scale(values):
    values = np.asarray(values, dtype=np.float64)
    return (values - values.min()) / max(float(values.max() - values.min()), 1e-12)
