from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..datasets import movielens_100k


GENRES = (
    "unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
    "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western",
)


@dataclass(frozen=True)
class CTRExample:
    user: int
    history: tuple[int, ...]
    candidate: int
    label: int


@dataclass(frozen=True)
class TextCTRData:
    train: tuple[CTRExample, ...]
    test: tuple[CTRExample, ...]
    titles: tuple[str, ...]
    genres: tuple[tuple[str, ...], ...]
    users: int

    def prompt(self, row: CTRExample, history_items: int = 8) -> str:
        history = " ; ".join(self.titles[item] for item in row.history[-history_items:])
        return (
            f"User liked: {history}. Candidate: {self.titles[row.candidate]}. "
            "Will the user click this candidate?"
        )


def load_text_ctr_data(root: Path, maximum_users: int | None = None) -> TextCTRData:
    ratings = movielens_100k(root)
    raw_items = sorted({item for _, item, _, _ in ratings})
    item_ids = {item: index for index, item in enumerate(raw_items)}
    metadata: dict[int, tuple[str, tuple[str, ...]]] = {}
    with (root / "ml-100k" / "u.item").open(encoding="latin-1") as stream:
        for line in stream:
            fields = line.rstrip().split("|")
            labels = tuple(name for name, flag in zip(GENRES, fields[5:24]) if flag == "1")
            metadata[int(fields[0])] = (fields[1], labels)
    raw_users = sorted({user for user, _, _, _ in ratings})
    if maximum_users:
        raw_users = raw_users[:maximum_users]
    user_ids = {user: index for index, user in enumerate(raw_users)}
    events: dict[int, list[tuple[int, int, float]]] = {user: [] for user in raw_users}
    for user, item, rating, timestamp in ratings:
        if user in events:
            events[user].append((timestamp, item_ids[item], rating))
    train: list[CTRExample] = []
    test: list[CTRExample] = []
    for raw_user, values in events.items():
        history: list[int] = []
        rows: list[CTRExample] = []
        for _, item, rating in sorted(values):
            if history and rating != 3:
                rows.append(CTRExample(user_ids[raw_user], tuple(history), item, int(rating >= 4)))
            if rating >= 4:
                history.append(item)
        if len(rows) >= 5:
            split = max(1, int(0.8 * len(rows)))
            train.extend(rows[:split])
            test.extend(rows[split:])
    ordered = [metadata[item] for item in raw_items]
    return TextCTRData(
        tuple(train), tuple(test), tuple(row[0] for row in ordered),
        tuple(row[1] for row in ordered), len(raw_users),
    )


def binary_auc(labels, scores) -> float:
    labels = np.asarray(labels, dtype=np.int64)
    scores = np.asarray(scores, dtype=np.float64)
    order = np.argsort(scores, kind="stable")
    ranks = np.empty(len(order), dtype=np.float64)
    ranks[order] = np.arange(1, len(order) + 1)
    positives = labels == 1
    p = int(positives.sum())
    n = len(labels) - p
    if not p or not n:
        return 0.5
    return float((ranks[positives].sum() - p * (p + 1) / 2) / (p * n))
