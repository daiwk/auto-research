from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..prompt_generation.data import PGDataset, PGExample, load_office_dataset


SID = re.compile(r"<([abc])_(\d+)>")
TASKS = ("JustForYou", "Query", "Category", "Longtail", "Discover", "Season", "Holiday")


@dataclass(frozen=True)
class SigmaExample:
    history: tuple[int, ...]
    target: int
    task: str
    instruction: str


@dataclass(frozen=True)
class SigmaData:
    train: tuple[SigmaExample, ...]
    validation: tuple[SigmaExample, ...]
    test: tuple[SigmaExample, ...]
    titles: tuple[str, ...]
    codes: np.ndarray
    visual_vectors: np.ndarray
    collaborative_vectors: np.ndarray
    grounding_pairs: tuple[tuple[str, int, int], ...]
    popularity: np.ndarray
    source: Path


def load_sigma_data(root: Path, train_rows: int, eval_users: int, seed: int) -> SigmaData:
    raw = load_office_dataset(root, train_limit=train_rows)
    count = len(raw.items)
    titles = tuple(str(raw.items[item].get("title", "")) for item in range(count))
    codes = np.zeros((count, 3), dtype=np.int64)
    for item, value in raw.item_sids.items():
        parsed = {level: int(token) for level, token in SID.findall(value)}
        codes[item] = parsed["a"], parsed["b"], parsed["c"]
    vectors = np.load(
        raw.source / "index" / "Office_Products.emb-qwen-td.npy", mmap_mode="r"
    )
    rng = np.random.default_rng(seed)
    projection = rng.normal(
        0, 1 / np.sqrt(vectors.shape[1]), size=(vectors.shape[1], 64)
    ).astype(np.float32)
    visual = np.asarray(vectors, dtype=np.float32) @ projection
    visual /= np.linalg.norm(visual, axis=1, keepdims=True).clip(1e-8)
    collaborative, adjacent = _collaborative(raw, count, seed)
    popularity = np.ones(count, dtype=np.float32)
    for row in raw.train:
        popularity[row.target_id] += 1
    pairs = _grounding_pairs(raw, visual, adjacent, seed)
    train = tuple(
        _example(raw, row, TASKS[index % len(TASKS)], popularity, codes)
        for index, row in enumerate(raw.train)
    )
    return SigmaData(
        train=train,
        validation=_select(raw, raw.validation, eval_users, seed, popularity, codes),
        test=_select(raw, raw.test, eval_users, seed + 1, popularity, codes),
        titles=titles,
        codes=codes,
        visual_vectors=visual,
        collaborative_vectors=collaborative,
        grounding_pairs=tuple(pairs),
        popularity=popularity,
        source=raw.source,
    )


def _collaborative(raw: PGDataset, count: int, seed: int):
    rng = np.random.default_rng(seed)
    basis = rng.normal(size=(count, 64)).astype(np.float32)
    aggregate = np.zeros_like(basis)
    degrees = np.ones((count, 1), dtype=np.float32)
    adjacent = []
    for row in raw.train:
        sequence = (*row.history_ids[-8:], row.target_id)
        for left, right in zip(sequence, sequence[1:]):
            aggregate[left] += basis[right]
            aggregate[right] += basis[left]
            degrees[left] += 1
            degrees[right] += 1
            adjacent.append((left, right))
    output = aggregate / degrees + 0.1 * basis
    output /= np.linalg.norm(output, axis=1, keepdims=True).clip(1e-8)
    return output, adjacent


def _grounding_pairs(raw, visual, adjacent, seed):
    rng = np.random.default_rng(seed)
    pairs = [("collaborative", left, right) for left, right in adjacent[:20000]]
    brands: dict[str, list[int]] = defaultdict(list)
    for item in range(len(raw.items)):
        brand = str(raw.items[item].get("brand", "")).strip().lower()
        if brand:
            brands[brand].append(item)
    for values in brands.values():
        if len(values) > 1:
            for item in values[:32]:
                other = values[(values.index(item) + 1) % len(values)]
                pairs.append(("semantic", item, other))
    anchors = rng.choice(len(visual), min(512, len(visual)), replace=False)
    similarities = visual[anchors] @ visual.T
    similarities[np.arange(len(anchors)), anchors] = -np.inf
    neighbors = similarities.argmax(1)
    pairs.extend(("visual", int(left), int(right)) for left, right in zip(anchors, neighbors))
    for item in range(min(2048, len(visual))):
        cluster = int(np.argmax(visual[item, :8]))
        candidate = int((item + cluster * 37 + 1) % len(visual))
        pairs.append(("knowledge", item, candidate))
    rng.shuffle(pairs)
    return pairs


def _select(raw, rows, count, seed, popularity, codes):
    ordered = sorted(
        rows,
        key=lambda row: hashlib.sha256(
            f"{seed}:{row.user_id}:{row.target_id}".encode()
        ).digest(),
    )
    return tuple(
        _example(raw, row, TASKS[index % len(TASKS)], popularity, codes)
        for index, row in enumerate(ordered[:count])
    )


def _example(raw, row: PGExample, task, popularity, codes):
    title = str(raw.items[row.target_id].get("title", ""))
    words = [word.strip(",.:;()[]").lower() for word in title.split() if len(word) > 3]
    keyword = words[0] if words else "office"
    prefix = int(codes[row.target_id, 0])
    quantile = "low-frequency" if popularity[row.target_id] <= np.median(popularity) else "popular"
    instructions = {
        "JustForYou": "Recommend the next product for this user.",
        "Query": f"Recommend products relevant to query '{keyword}'.",
        "Category": f"Recommend within semantic category {prefix}.",
        "Longtail": f"Explore a {quantile} product with precise relevance.",
        "Discover": "Discover a useful product beyond repeated history patterns.",
        "Season": f"Recommend for season bucket {prefix % 4}.",
        "Holiday": f"Recommend for holiday theme {prefix % 6}.",
    }
    return SigmaExample(
        history=row.history_ids[-8:],
        target=row.target_id,
        task=task,
        instruction=instructions[task],
    )
