from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from ..llm_rec_data import GENRES
from ...datasets import movielens_100k


@dataclass(frozen=True)
class RetrievalData:
    titles: tuple[str, ...]
    genres: tuple[tuple[str, ...], ...]
    train: tuple[tuple[int, ...], ...]
    validation: tuple[int, ...]
    test: tuple[int, ...]

    @property
    def items(self) -> int:
        return len(self.titles)


def load_retrieval_data(
    root: Path, maximum_users: int = 180, maximum_items: int = 240
) -> RetrievalData:
    ratings = movielens_100k(root)
    positives: dict[int, list[tuple[int, int]]] = {}
    popularity: dict[int, int] = {}
    for user, item, rating, timestamp in ratings:
        if rating >= 4:
            positives.setdefault(user, []).append((timestamp, item))
            popularity[item] = popularity.get(item, 0) + 1
    selected = {
        item
        for item, _ in sorted(
            popularity.items(), key=lambda row: (-row[1], row[0])
        )[:maximum_items]
    }
    sequences = []
    for user in sorted(positives):
        sequence = [item for _, item in sorted(positives[user]) if item in selected]
        sequence = list(dict.fromkeys(sequence))
        if len(sequence) >= 5:
            sequences.append(sequence)
        if len(sequences) >= maximum_users:
            break
    used = sorted({item for sequence in sequences for item in sequence})
    item_ids = {item: index for index, item in enumerate(used)}
    metadata: dict[int, tuple[str, tuple[str, ...]]] = {}
    with (root / "ml-100k" / "u.item").open(encoding="latin-1") as stream:
        for line in stream:
            fields = line.rstrip().split("|")
            item = int(fields[0])
            if item in item_ids:
                labels = tuple(
                    name for name, flag in zip(GENRES, fields[5:24]) if flag == "1"
                )
                metadata[item] = (fields[1], labels)
    encoded = [[item_ids[item] for item in sequence] for sequence in sequences]
    ordered = [metadata[item] for item in used]
    return RetrievalData(
        titles=tuple(row[0] for row in ordered),
        genres=tuple(row[1] for row in ordered),
        train=tuple(tuple(sequence[:-2]) for sequence in encoded),
        validation=tuple(sequence[-2] for sequence in encoded),
        test=tuple(sequence[-1] for sequence in encoded),
    )


def creative(title: str, genres: tuple[str, ...], shadow: bool = False) -> str:
    value = title
    if shadow:
        value = re.sub(r"\((\d{4})\)", r", released \1", title).replace("  ", " ")
    return f"Title: {value}. Product categories: {', '.join(genres)}."
