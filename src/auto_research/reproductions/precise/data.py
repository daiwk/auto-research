from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ...datasets import movielens_1m


@dataclass(frozen=True)
class PreciseData:
    universal: tuple[tuple[int, ...], ...]
    targeted: tuple[tuple[int, ...], ...]
    test_targets: tuple[int, ...]
    item_texts: tuple[str, ...]
    train_frequency: tuple[int, ...]


def load_precise_data(root: Path, maximum_users: int = 300) -> PreciseData:
    ratings = movielens_1m(root)
    selected = sorted({row[0] for row in ratings})[:maximum_users]
    by_user = {user: [] for user in selected}
    for user, item, rating, timestamp in ratings:
        if user in by_user:
            by_user[user].append((timestamp, item, rating))

    raw_rows = []
    for events in by_user.values():
        events.sort()
        positives = [event for event in events if event[2] >= 3]
        target_positions = [index for index, event in enumerate(positives) if event[2] >= 4]
        if len(target_positions) < 4:
            continue
        test_position = target_positions[-1]
        universal = positives[:test_position]
        targeted = [event for event in universal if event[2] >= 4]
        if len(universal) >= 4 and len(targeted) >= 3:
            raw_rows.append((universal, targeted, positives[test_position]))

    # Match the paper's protocol: a held-out item must have appeared in the
    # global training set, so this is not an open-catalog cold-start test.
    training_items = {event[1] for row in raw_rows for part in row[:2] for event in part}
    raw_rows = [row for row in raw_rows if row[2][1] in training_items]
    raw_items = sorted(training_items)
    item_ids = {item: index for index, item in enumerate(raw_items)}
    universal = tuple(tuple(item_ids[event[1]] for event in row[0]) for row in raw_rows)
    targeted = tuple(tuple(item_ids[event[1]] for event in row[1]) for row in raw_rows)
    tests = tuple(item_ids[row[2][1]] for row in raw_rows)
    frequencies = [0] * len(raw_items)
    for sequence in universal:
        for item in sequence:
            frequencies[item] += 1
    return PreciseData(universal, targeted, tests, _movie_texts(root, raw_items), tuple(frequencies))


def _movie_texts(root: Path, raw_items: list[int]) -> tuple[str, ...]:
    values = {}
    for line in (root / "ml-1m" / "movies.dat").read_text(encoding="latin-1").splitlines():
        item, title, genres = line.split("::")
        values[int(item)] = f"Title: {title}. Genres: {genres.replace('|', ', ')}."
    return tuple(values[item] for item in raw_items)
