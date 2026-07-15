from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..prompt_generation.data import PGDataset, PGExample, load_office_dataset


SID = re.compile(r"<([abc])_(\d+)>")
ASPECT_VALUES = (
    np.asarray([-1.0, -0.5, 0.0, 0.5, 1.0], dtype=np.float32),
    np.asarray([0.0, 0.5, 1.0], dtype=np.float32),
    np.asarray([0.0, 0.5, 1.0], dtype=np.float32),
)
ASPECT_NAMES = ("profile", "future", "novelty")


@dataclass(frozen=True)
class SGreCExample:
    user_id: str
    history: tuple[int, ...]
    target: int


@dataclass(frozen=True)
class AspectExample:
    history: tuple[int, ...]
    candidate: int
    labels: tuple[int, int, int]


@dataclass(frozen=True)
class PairExample:
    history: tuple[int, ...]
    preferred: int
    rejected: int


@dataclass(frozen=True)
class SGreCData:
    train: tuple[SGreCExample, ...]
    validation: tuple[SGreCExample, ...]
    test: tuple[SGreCExample, ...]
    aspects: tuple[AspectExample, ...]
    pairs: tuple[PairExample, ...]
    titles: tuple[str, ...]
    codes: np.ndarray
    vectors: np.ndarray
    popularity: np.ndarray
    source: Path


def load_sgrec_data(root: Path, train_rows: int, eval_users: int, seed: int) -> SGreCData:
    raw = load_office_dataset(root, train_limit=train_rows)
    item_count = len(raw.items)
    titles = tuple(str(raw.items[item].get("title", "")) for item in range(item_count))
    codes = _codes(raw, item_count)
    vectors = np.asarray(
        np.load(raw.source / "index" / "Office_Products.emb-qwen-td.npy", mmap_mode="r"),
        dtype=np.float32,
    )
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True).clip(1e-8)
    popularity = np.ones(item_count, dtype=np.float32)
    for row in raw.train:
        popularity[row.target_id] += 1
    train = tuple(_example(row) for row in raw.train)
    validation = _select(raw.validation, eval_users, seed)
    test = _select(raw.test, eval_users, seed + 1)
    aspects, pairs = _annotations(train, vectors, seed)
    return SGreCData(
        train=train,
        validation=validation,
        test=test,
        aspects=aspects,
        pairs=pairs,
        titles=titles,
        codes=codes,
        vectors=vectors,
        popularity=popularity,
        source=raw.source,
    )


def aspect_prompt(data: SGreCData, row: AspectExample) -> str:
    history = " | ".join(data.titles[item][:64] for item in row.history[-6:])
    return (
        "Score an Office product recommendation on profile relevance, future interest, "
        "and novelty using the user's behavior.\n"
        f"History: {history}\nCandidate: {data.titles[row.candidate][:96]}\n"
        "Aspect evidence:"
    )


def user_prompt(data: SGreCData, history: tuple[int, ...]) -> str:
    titles = " | ".join(data.titles[item][:64] for item in history[-8:])
    return (
        "Infer this user's relative importance weights for profile relevance, future "
        f"interest, and novelty.\nHistory: {titles}\nImportance levels:"
    )


def labels_to_values(labels) -> np.ndarray:
    return np.asarray(
        [ASPECT_VALUES[index][int(label)] for index, label in enumerate(labels)],
        dtype=np.float32,
    )


def _codes(raw: PGDataset, count: int) -> np.ndarray:
    output = np.zeros((count, 3), dtype=np.int64)
    for item, value in raw.item_sids.items():
        parsed = {level: int(token) for level, token in SID.findall(value)}
        output[item] = parsed["a"], parsed["b"], parsed["c"]
    return output


def _annotations(train, vectors, seed):
    rng = np.random.default_rng(seed)
    aspects: list[AspectExample] = []
    pairs: list[PairExample] = []
    count = len(vectors)
    similarity = vectors @ vectors.T
    nearest = np.argpartition(similarity, -32, axis=1)[:, -32:]
    for row in train:
        history = row.history[-12:]
        if not history:
            continue
        excluded = set(history) | {row.target}
        negative = int(rng.integers(count))
        while negative in excluded:
            negative = int(rng.integers(count))
        hard_pool = nearest[row.target]
        if rng.random() < 0.5:
            choices = [int(value) for value in hard_pool if int(value) not in excluded]
            if choices:
                negative = choices[int(rng.integers(len(choices)))]
        for candidate in (row.target, negative):
            aspects.append(
                AspectExample(history, candidate, _aspect_labels(history, candidate, vectors))
            )
        pairs.append(PairExample(history, row.target, negative))
    return tuple(aspects), tuple(pairs)


def _aspect_labels(history, candidate, vectors):
    history_vectors = vectors[list(history)]
    profile = float(vectors[candidate] @ history_vectors.mean(0))
    future = float(vectors[candidate] @ history_vectors[-min(2, len(history)) :].mean(0))
    closest = float((history_vectors @ vectors[candidate]).max())
    profile_label = int(np.digitize(profile, [0.70, 0.76, 0.82, 0.90]))
    future_label = int(np.digitize(future, [0.75, 0.85]))
    novelty_label = int(np.digitize(1.0 - closest, [0.10, 0.24]))
    return profile_label, future_label, novelty_label


def _select(rows: tuple[PGExample, ...], count: int, seed: int):
    ordered = sorted(
        rows,
        key=lambda row: hashlib.sha256(
            f"{seed}:{row.user_id}:{row.target_id}".encode()
        ).digest(),
    )
    return tuple(_example(row) for row in ordered[:count])


def _example(row: PGExample) -> SGreCExample:
    return SGreCExample(row.user_id, row.history_ids[-20:], row.target_id)
