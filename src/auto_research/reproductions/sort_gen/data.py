from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ...datasets import movielens_1m
from ..rec_utils import load_movielens_1m_sequences


@dataclass(frozen=True)
class Slate:
    items: np.ndarray
    user: np.ndarray
    prior: np.ndarray
    click: np.ndarray
    pay: np.ndarray
    gmv: np.ndarray


@dataclass(frozen=True)
class SortData:
    train: tuple[Slate, ...]
    evaluation: tuple[Slate, ...]
    features: np.ndarray


def load_sort_data(root: Path, maximum_users=420, maximum_items=620, list_size=8, candidate_size=20):
    raw = load_movielens_1m_sequences(root, minimum_rating=0.0)
    ratings = movielens_1m(root)
    raw_items = sorted({item for _, item, _, _ in ratings}); raw_map = {item: index for index, item in enumerate(raw_items)}
    selected = set(np.argsort(-raw.popularity)[:maximum_items].tolist())
    users = {}
    for user, item, rating, timestamp in ratings:
        encoded = raw_map[item]
        if encoded in selected:
            users.setdefault(user, []).append((timestamp, encoded, rating))
    items = sorted(selected); mapping = {item: index for index, item in enumerate(items)}
    features = raw.item_features[items].astype(np.float32)
    popularity = raw.popularity[items].astype(np.float32); popularity = np.log1p(popularity); popularity /= max(float(popularity.max()), 1.0)
    train = []; evaluation = []
    for events in users.values():
        events.sort(); events = [(mapping[item], rating) for _, item, rating in events if item in mapping]
        if len(events) < candidate_size + list_size:
            continue
        history = events[:-candidate_size]
        user_vector = features[[item for item, _ in history]].mean(0)
        for start in range(0, max(0, len(history) - list_size + 1), list_size):
            window = history[start:start + list_size]
            if len(window) == list_size:
                train.append(_slate(window, user_vector, features, popularity))
        evaluation.append(_slate(events[-candidate_size:], user_vector, features, popularity))
        if len(evaluation) >= maximum_users:
            break
    return SortData(tuple(train), tuple(evaluation), features)


def _slate(events, user, features, popularity):
    items = np.asarray([item for item, _ in events], dtype=np.int64)
    ratings = np.asarray([rating for _, rating in events], dtype=np.float32)
    similarity = features[items] @ user / max(float(np.linalg.norm(user)), 1e-6)
    similarity = (similarity - similarity.min()) / max(float(np.ptp(similarity)), 1e-6)
    prior_click = 0.7 * similarity + 0.3 * popularity[items]
    prior_pay = 0.85 * similarity + 0.15 * popularity[items]
    prior_gmv = prior_pay * (0.5 + 0.5 * ratings / 5)
    return Slate(items, user.astype(np.float32), np.stack((prior_click, prior_pay, prior_gmv), 1).astype(np.float32), (ratings >= 3).astype(np.float32), (ratings >= 4).astype(np.float32), ((ratings >= 4) * ratings).astype(np.float32))
