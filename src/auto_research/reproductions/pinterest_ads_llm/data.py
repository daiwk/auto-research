from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..prompt_generation.data import PGDataset, PGExample, load_office_dataset


@dataclass(frozen=True)
class AdsExample:
    user_id: str
    history: tuple[int, ...]
    target_item: int
    target_advertiser: int
    prompt: str


@dataclass(frozen=True)
class AdsData:
    train: tuple[AdsExample, ...]
    validation: tuple[AdsExample, ...]
    test: tuple[AdsExample, ...]
    advertiser_names: tuple[str, ...]
    item_advertisers: np.ndarray
    item_vectors: np.ndarray
    item_popularity: np.ndarray
    source: Path


def load_ads_data(
    root: Path,
    train_limit: int,
    evaluation_users: int,
    advertiser_count: int,
    seed: int,
) -> AdsData:
    raw = load_office_dataset(root, train_limit=train_limit)
    target_counts = Counter(_brand(raw, row.target_id) for row in raw.train)
    names = tuple(
        name for name, _ in target_counts.most_common(advertiser_count) if name
    )
    name_to_id = {name: index for index, name in enumerate(names)}
    item_advertisers = np.asarray(
        [name_to_id.get(_brand(raw, item), -1) for item in range(len(raw.items))],
        dtype=np.int64,
    )
    popularity = np.ones(len(raw.items), dtype=np.float32)
    for row in raw.train:
        popularity[row.target_id] += 1
    vectors = np.load(
        raw.source / "index" / "Office_Products.emb-qwen-td.npy", mmap_mode="r"
    )
    rng = np.random.default_rng(seed)
    projection = rng.normal(
        0, 1 / np.sqrt(vectors.shape[1]), size=(vectors.shape[1], 64)
    ).astype(np.float32)
    item_vectors = np.asarray(vectors, dtype=np.float32) @ projection
    item_vectors /= np.linalg.norm(item_vectors, axis=1, keepdims=True).clip(1e-8)
    train = tuple(
        _convert(raw, row, item_advertisers, names)
        for row in raw.train
        if item_advertisers[row.target_id] >= 0
    )
    validation = _select(raw.validation, raw, item_advertisers, names, evaluation_users, seed)
    test = _select(raw.test, raw, item_advertisers, names, evaluation_users, seed + 1)
    return AdsData(
        train=train,
        validation=validation,
        test=test,
        advertiser_names=names,
        item_advertisers=item_advertisers,
        item_vectors=item_vectors,
        item_popularity=popularity,
        source=raw.source,
    )


def _select(rows, raw, item_advertisers, names, count, seed):
    eligible = [row for row in rows if item_advertisers[row.target_id] >= 0]
    eligible.sort(
        key=lambda row: hashlib.sha256(
            f"{seed}:{row.user_id}:{row.target_id}".encode()
        ).digest()
    )
    return tuple(_convert(raw, row, item_advertisers, names) for row in eligible[:count])


def _convert(raw: PGDataset, row: PGExample, item_advertisers, names) -> AdsExample:
    history = row.history_ids[-12:]
    active = []
    for item in reversed(history):
        advertiser = int(item_advertisers[item])
        if advertiser >= 0 and names[advertiser] not in active:
            active.append(names[advertiser])
    titles = [str(raw.items[item].get("title", ""))[:72] for item in history[-5:]]
    digest = int(hashlib.sha256(row.user_id.encode()).hexdigest()[:8], 16)
    profile = f"age_band={18 + digest % 5 * 10}, gender={'F' if digest % 2 else 'M'}"
    prompt = (
        "You are an ad-matching assistant. Predict the next advertiser most likely to convert.\n"
        f"Profile: {profile}\n"
        f"Active advertisers with past conversions: {', '.join(active[:6]) or 'none'}\n"
        f"Recent product activity: {' | '.join(titles)}\n"
        f"Preset advertiser pool: {', '.join(names)}\n"
    )
    return AdsExample(
        user_id=row.user_id,
        history=history,
        target_item=row.target_id,
        target_advertiser=int(item_advertisers[row.target_id]),
        prompt=prompt,
    )


def _brand(raw: PGDataset, item: int) -> str:
    return " ".join(str(raw.items[item].get("brand", "")).strip().lower().split())
