from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from auto_research.datasets import movielens_1m


@dataclass(frozen=True)
class PinEqualizerData:
    train: tuple[tuple[int, ...], ...]
    validation: tuple[int, ...]
    test: tuple[int, ...]
    genres: np.ndarray
    popularity: np.ndarray
    fresh: np.ndarray
    underexplored: np.ndarray
    user_profiles: np.ndarray
    exploration_corpus: np.ndarray

    @property
    def users(self) -> int:
        return len(self.train)

    @property
    def items(self) -> int:
        return len(self.popularity)


def load_data(root: Path, minimum_rating: float = 3.0) -> PinEqualizerData:
    ratings = movielens_1m(root)
    raw_items = sorted({item for _, item, _, _ in ratings})
    item_ids = {item: index for index, item in enumerate(raw_items)}
    genres = _genres(root, raw_items)
    by_user: dict[int, list[tuple[int, int]]] = {}
    first_seen = np.full(len(raw_items), np.iinfo(np.int64).max, dtype=np.int64)
    for user, item, rating, timestamp in ratings:
        if rating < minimum_rating:
            continue
        encoded = item_ids[item]
        by_user.setdefault(user, []).append((timestamp, encoded))
        first_seen[encoded] = min(first_seen[encoded], timestamp)

    train, validation, test = [], [], []
    for events in by_user.values():
        sequence = tuple(item for _, item in sorted(events))
        if len(sequence) >= 5:
            train.append(sequence[:-2])
            validation.append(sequence[-2])
            test.append(sequence[-1])
    popularity = np.zeros(len(raw_items), dtype=np.float32)
    for sequence in train:
        np.add.at(popularity, np.asarray(sequence), 1)
    valid_first = first_seen[first_seen < np.iinfo(np.int64).max]
    fresh_cutoff = np.quantile(valid_first, 0.8)
    fresh = first_seen >= fresh_cutoff
    fresh_popularity = popularity[fresh]
    underexplored = fresh & (popularity <= np.median(fresh_popularity))
    profiles = np.stack([
        genres[list(sequence)].mean(axis=0) for sequence in train
    ]).astype(np.float32)
    profiles /= np.maximum(np.linalg.norm(profiles, axis=1, keepdims=True), 1e-8)
    exploration = _build_exploration_corpus(
        popularity, genres, fresh, underexplored
    )
    return PinEqualizerData(
        tuple(train),
        tuple(validation),
        tuple(test),
        genres,
        popularity,
        fresh,
        underexplored,
        profiles,
        exploration,
    )


def _build_exploration_corpus(popularity, genres, fresh, underexplored):
    impressions = 10.0 + 5.0 * popularity
    engagements = popularity
    genre_counts = genres.sum(axis=0).clip(min=1)
    genre_prior = genres @ (
        (genres.T @ (engagements / impressions)) / genre_counts
    )
    genre_prior /= np.maximum(genres.sum(axis=1), 1)
    strength = 20.0
    posterior = (strength * genre_prior + engagements) / (strength + impressions)
    graduated = popularity >= np.quantile(popularity[fresh], 0.75)
    eligible = np.flatnonzero(fresh & underexplored & ~graduated)
    keep = max(1, len(eligible) // 2)
    selected = eligible[np.argsort(posterior[eligible])[-keep:]]
    output = np.zeros(len(popularity), dtype=bool)
    output[selected] = True
    return output


def _genres(root: Path, raw_items: list[int]) -> np.ndarray:
    mapping = {}
    vocabulary = set()
    with (root / "ml-1m" / "movies.dat").open(encoding="latin-1") as stream:
        for line in stream:
            item, _, labels = line.rstrip().split("::")
            mapping[int(item)] = tuple(labels.split("|"))
            vocabulary.update(mapping[int(item)])
    columns = {label: index for index, label in enumerate(sorted(vocabulary))}
    matrix = np.zeros((len(raw_items), len(columns)), dtype=np.float32)
    for row, item in enumerate(raw_items):
        for label in mapping[item]:
            matrix[row, columns[label]] = 1.0
    matrix /= np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1.0)
    return matrix
