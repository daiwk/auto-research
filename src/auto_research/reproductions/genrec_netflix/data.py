from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ...datasets import movielens_1m


@dataclass(frozen=True)
class GenRecData:
    train: tuple[tuple[int, ...], ...]
    validation: tuple[int, ...]
    test: tuple[int, ...]
    item_texts: tuple[str, ...]
    item_genres: tuple[tuple[str, ...], ...]
    popularity: np.ndarray


def load_genrec_data(
    root: Path, *, maximum_users: int = 240, maximum_items: int = 500,
    allow_network: bool = True,
) -> GenRecData:
    ratings = [
        row for row in movielens_1m(root, allow_network=allow_network)
        if row[2] >= 3.0
    ]
    counts: dict[int, int] = {}
    for _, item, _, _ in ratings:
        counts[item] = counts.get(item, 0) + 1
    selected_items = {
        item for item, _ in sorted(counts.items(), key=lambda row: (-row[1], row[0]))[:maximum_items]
    }
    by_user: dict[int, list[tuple[int, int]]] = {}
    for user, item, _, timestamp in ratings:
        if item in selected_items:
            by_user.setdefault(user, []).append((timestamp, item))
    rows = []
    for events in by_user.values():
        sequence = [item for _, item in sorted(events)]
        if len(sequence) >= 10:
            rows.append(sequence)
        if len(rows) >= maximum_users:
            break
    raw_items = sorted({item for row in rows for item in row})
    item_ids = {item: index for index, item in enumerate(raw_items)}
    encoded = [[item_ids[item] for item in row] for row in rows]
    metadata = _movie_metadata(root)
    popularity = np.zeros(len(raw_items), dtype=np.float32)
    for row in encoded:
        for item in row[:-2]:
            popularity[item] += 1
    return GenRecData(
        train=tuple(tuple(row[:-2]) for row in encoded),
        validation=tuple(row[-2] for row in encoded),
        test=tuple(row[-1] for row in encoded),
        item_texts=tuple(metadata[item][0] for item in raw_items),
        item_genres=tuple(metadata[item][1] for item in raw_items),
        popularity=popularity,
    )


def _movie_metadata(root: Path) -> dict[int, tuple[str, tuple[str, ...]]]:
    values = {}
    path = root / "ml-1m" / "movies.dat"
    for line in path.read_text(encoding="latin-1").splitlines():
        item, title, genres = line.split("::")
        labels = tuple(genres.split("|"))
        values[int(item)] = (
            f"Title: {title}. Genres: {', '.join(labels)}.",
            labels,
        )
    return values


def verbalize(history: tuple[int, ...], data: GenRecData, maximum_events: int) -> str:
    selected = history[-maximum_events:]
    events = "\n".join(
        f"{index + 1}. watched {data.item_texts[item]}"
        for index, item in enumerate(selected)
    )
    return (
        "Rank the Netflix-like catalog for this member. Recent history, oldest to newest:\n"
        f"{events}\nRecommend the next title."
    )


def training_rows(data: GenRecData, maximum_history: int):
    rows = []
    for sequence in data.train:
        for index in range(3, len(sequence)):
            rows.append((tuple(sequence[max(0, index - maximum_history):index]), sequence[index]))
    return rows
