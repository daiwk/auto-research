from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ...datasets import movielens_100k
from ..llm_rec_data import GENRES


@dataclass(frozen=True)
class CTRRow:
    user: int
    history: tuple[int, ...]
    candidate: int
    label: float


@dataclass(frozen=True)
class AKTData:
    train: tuple[CTRRow, ...]
    validation: tuple[CTRRow, ...]
    test: tuple[CTRRow, ...]
    sequences: tuple[tuple[int, ...], ...]
    titles: tuple[str, ...]
    genres: tuple[tuple[str, ...], ...]
    item_activity: np.ndarray
    user_activity: np.ndarray

    @property
    def item_count(self):
        return len(self.titles)

    @property
    def user_count(self):
        return len(self.sequences)


def load_akt_data(root: Path, seed: int, maximum_users: int = 320) -> AKTData:
    ratings = movielens_100k(root)
    raw_items = sorted({item for _, item, _, _ in ratings})
    item_ids = {item: index for index, item in enumerate(raw_items)}
    metadata = {}
    with (root / "ml-100k" / "u.item").open(encoding="latin-1") as stream:
        for line in stream:
            fields = line.rstrip().split("|")
            metadata[int(fields[0])] = (
                fields[1],
                tuple(name for name, flag in zip(GENRES, fields[5:24]) if flag == "1"),
            )
    by_user = {}
    for user, item, rating, timestamp in ratings:
        if rating >= 4:
            by_user.setdefault(user, []).append((timestamp, item_ids[item]))
    ordered = [
        tuple(item for _, item in sorted(events))
        for _, events in sorted(by_user.items())
        if len(events) >= 7
    ][:maximum_users]
    rng = random.Random(seed)
    item_activity = np.zeros(len(raw_items), dtype=np.float32)
    for sequence in ordered:
        item_activity[list(sequence[:-2])] += 1
    probabilities = item_activity + 1.0
    probabilities /= probabilities.sum()
    splits = {"train": [], "validation": [], "test": []}
    for user, sequence in enumerate(ordered):
        cut = max(3, len(sequence) - 2)
        for position in range(2, cut):
            _append_pair(splits["train"], user, sequence[:position], sequence[position], rng, probabilities)
        _append_pair(splits["validation"], user, sequence[:cut], sequence[cut], rng, probabilities)
        _append_pair(splits["test"], user, sequence[: cut + 1], sequence[cut + 1], rng, probabilities)
    values = [metadata[item] for item in raw_items]
    return AKTData(
        train=tuple(splits["train"]),
        validation=tuple(splits["validation"]),
        test=tuple(splits["test"]),
        sequences=tuple(ordered),
        titles=tuple(value[0] for value in values),
        genres=tuple(value[1] for value in values),
        item_activity=item_activity,
        user_activity=np.asarray([len(row[:-2]) for row in ordered], dtype=np.float32),
    )


def _append_pair(rows, user, history, positive, rng, probabilities):
    rows.append(CTRRow(user, tuple(history[-20:]), positive, 1.0))
    negative = rng.choices(range(len(probabilities)), weights=probabilities, k=1)[0]
    seen = set(history) | {positive}
    while negative in seen:
        negative = rng.choices(range(len(probabilities)), weights=probabilities, k=1)[0]
    rows.append(CTRRow(user, tuple(history[-20:]), negative, 0.0))
