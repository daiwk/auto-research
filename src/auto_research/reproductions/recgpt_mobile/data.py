from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..precise.data import load_precise_data


@dataclass(frozen=True)
class IntentExample:
    history: tuple[int, ...]
    target: int


@dataclass(frozen=True)
class MobileIntentData:
    train: tuple[IntentExample, ...]
    validation: tuple[IntentExample, ...]
    test: tuple[IntentExample, ...]
    item_texts: tuple[str, ...]
    item_genres: tuple[tuple[str, ...], ...]
    genres: tuple[str, ...]


def load_mobile_intent_data(root: Path, maximum_users: int = 300) -> MobileIntentData:
    raw = load_precise_data(root, maximum_users)
    item_genres = tuple(_genres(text) for text in raw.item_texts)
    genres = tuple(sorted({genre for values in item_genres for genre in values}))
    train = []
    validation = []
    test = []
    for sequence, target in zip(raw.targeted, raw.test_targets):
        if len(sequence) < 5:
            continue
        for index in range(3, len(sequence) - 1):
            train.append(IntentExample(tuple(sequence[max(0, index - 8):index]), sequence[index]))
        validation.append(IntentExample(tuple(sequence[-8:-1]), sequence[-1]))
        test.append(IntentExample(tuple(sequence[-7:] + (sequence[-1],)), target))
    return MobileIntentData(tuple(train), tuple(validation), tuple(test), raw.item_texts, item_genres, genres)


def _genres(text: str) -> tuple[str, ...]:
    values = text.split("Genres: ", 1)[1].rstrip(".")
    return tuple(value.strip() for value in values.split(","))
