from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..datasets import movielens_100k


@dataclass(frozen=True)
class ActionSequenceData:
    train_items: tuple[tuple[int, ...], ...]
    train_actions: tuple[tuple[int, ...], ...]
    validation_items: tuple[int, ...]
    validation_actions: tuple[int, ...]
    test_items: tuple[int, ...]
    test_actions: tuple[int, ...]
    item_count: int
    item_features: np.ndarray


@dataclass(frozen=True)
class ActionCTRRow:
    items: tuple[int, ...]
    actions: tuple[int, ...]
    time_buckets: tuple[int, ...]
    candidate: int
    label: int


def load_action_sequences(root: Path) -> ActionSequenceData:
    ratings = movielens_100k(root)
    raw_items = sorted({item for _, item, _, _ in ratings})
    item_ids = {item: index for index, item in enumerate(raw_items)}
    by_user: dict[int, list[tuple[int, int, int]]] = {}
    for user, item, rating, timestamp in ratings:
        by_user.setdefault(user, []).append(
            (timestamp, item_ids[item], _action(rating))
        )
    train_items, train_actions, validation_items, validation_actions = [], [], [], []
    test_items, test_actions = [], []
    for events in by_user.values():
        events.sort()
        if len(events) < 7:
            continue
        items = tuple(row[1] for row in events)
        actions = tuple(row[2] for row in events)
        train_items.append(items[:-2])
        train_actions.append(actions[:-2])
        validation_items.append(items[-2])
        validation_actions.append(actions[-2])
        test_items.append(items[-1])
        test_actions.append(actions[-1])
    return ActionSequenceData(
        tuple(train_items), tuple(train_actions), tuple(validation_items),
        tuple(validation_actions), tuple(test_items), tuple(test_actions),
        len(raw_items), _features(root, raw_items),
    )


def load_action_ctr(root: Path, history_length: int = 16):
    ratings = movielens_100k(root)
    raw_items = sorted({item for _, item, _, _ in ratings})
    item_ids = {item: index for index, item in enumerate(raw_items)}
    by_user: dict[int, list[tuple[int, int, int]]] = {}
    for user, item, rating, timestamp in ratings:
        by_user.setdefault(user, []).append(
            (timestamp, item_ids[item], _action(rating))
        )
    train, test = [], []
    for events in by_user.values():
        events.sort()
        split = max(2, int(0.8 * len(events)))
        for position in range(2, len(events)):
            history = events[max(0, position - history_length):position]
            current = events[position]
            gaps = [min(31, max(0, (current[0] - row[0]).bit_length() - 1)) for row in history]
            row = ActionCTRRow(
                tuple(value[1] for value in history),
                tuple(value[2] for value in history), tuple(gaps), current[1],
                int(current[2] >= 1),
            )
            (train if position < split else test).append(row)
    return tuple(train), tuple(test), len(raw_items)


def _action(rating: float) -> int:
    return 2 if rating >= 5 else 1 if rating >= 4 else 0


def _features(root: Path, raw_items: list[int]) -> np.ndarray:
    path = root / "ml-100k" / "u.item"
    rows = {}
    with path.open(encoding="latin-1") as stream:
        for line in stream:
            fields = line.rstrip().split("|")
            rows[int(fields[0])] = np.asarray(fields[5:24], dtype=np.float32)
    return np.stack([rows[item] for item in raw_items])
