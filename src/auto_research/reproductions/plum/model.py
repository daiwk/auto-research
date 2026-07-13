from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

from ...datasets import movielens_1m


SID_END = "<sid_end>"


@dataclass(frozen=True)
class SemanticIDIndex:
    """Multi-level residual-quantized item identifiers."""

    codes: np.ndarray
    cardinalities: tuple[int, ...]
    training_metrics: dict[str, float] | None = None

    def tokens(self, item: int) -> tuple[str, ...]:
        return tuple(
            f"<sid_{level}_{int(code)}>"
            for level, code in enumerate(self.codes[item])
        )

    def text(self, item: int) -> str:
        return "".join((*self.tokens(item), SID_END))

    def vocabulary(self) -> tuple[str, ...]:
        return tuple(
            f"<sid_{level}_{code}>"
            for level, size in enumerate(self.cardinalities)
            for code in range(size)
        ) + (SID_END,)

    def items_by_code(self) -> dict[tuple[int, ...], tuple[int, ...]]:
        groups: dict[tuple[int, ...], list[int]] = {}
        for item, row in enumerate(self.codes):
            groups.setdefault(tuple(int(x) for x in row), []).append(item)
        return {key: tuple(value) for key, value in groups.items()}

    @property
    def uniqueness(self) -> float:
        groups = self.items_by_code()
        return sum(len(items) == 1 for items in groups.values()) / len(self.codes)


@dataclass(frozen=True)
class MovieMetadata:
    titles: tuple[str, ...]
    genres: tuple[tuple[str, ...], ...]


class TokenTrie:
    """Prefix tree used to prevent the decoder from hallucinating invalid SIDs."""

    def __init__(self, sequences: Iterable[tuple[int, ...]]):
        self.root: dict[int, dict] = {}
        for sequence in sequences:
            node = self.root
            for token in sequence:
                node = node.setdefault(int(token), {})

    def allowed(self, prefix: tuple[int, ...]) -> tuple[int, ...]:
        node = self.root
        for token in prefix:
            if token not in node:
                return ()
            node = node[token]
        return tuple(node)

    def contains(self, sequence: tuple[int, ...]) -> bool:
        node = self.root
        for token in sequence:
            if token not in node:
                return False
            node = node[token]
        return not node


def load_movie_metadata(dataset_dir: Path) -> MovieMetadata:
    rows: dict[int, tuple[str, tuple[str, ...]]] = {}
    path = dataset_dir / "ml-1m" / "movies.dat"
    with path.open(encoding="latin-1") as stream:
        for line in stream:
            raw_item, title, raw_genres = line.rstrip().split("::")
            rows[int(raw_item)] = (title, tuple(raw_genres.split("|")))
    rated_items = sorted({item for _, item, _, _ in movielens_1m(dataset_dir)})
    ordered = [rows[item] for item in rated_items]
    return MovieMetadata(
        titles=tuple(row[0] for row in ordered),
        genres=tuple(row[1] for row in ordered),
    )


def build_semantic_ids(
    data,
    metadata: MovieMetadata,
    cardinalities: tuple[int, ...] = (512, 256, 128),
    seed: int = 42,
    checkpoint_dir: Path | None = None,
) -> SemanticIDIndex:
    """Train SID-v2-style RQ-VAE IDs with content and behavioral alignment.

    MovieLens has text and genres rather than YouTube video/audio embeddings. We
    use title and genre as the two public modalities, while adjacent watches
    supply the paper's co-occurrence contrastive objective.
    """

    title = _hashed_title_features(metadata.titles, dimensions=96)
    genres = np.asarray(data.item_features, dtype=np.float64)
    cooccurrences = np.asarray(
        [pair for sequence in data.train for pair in zip(sequence, sequence[1:])],
        dtype=np.int64,
    )
    from .rqvae import train_rqvae

    codes, metrics = train_rqvae(
        title.astype(np.float32),
        genres.astype(np.float32),
        cooccurrences,
        cardinalities,
        seed,
        checkpoint_dir=checkpoint_dir,
    )
    return SemanticIDIndex(
        codes=codes, cardinalities=cardinalities, training_metrics=metrics
    )


def residual_kmeans(
    features: np.ndarray,
    cardinalities: tuple[int, ...],
    seed: int = 42,
    iterations: int = 30,
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """Greedy residual quantization with decreasing-resolution codebooks."""

    residual = np.asarray(features, dtype=np.float64).copy()
    assignments: list[np.ndarray] = []
    codebooks: list[np.ndarray] = []
    for level, cardinality in enumerate(cardinalities):
        centers, labels = _kmeans(
            residual, min(cardinality, len(residual)), seed + level, iterations
        )
        assignments.append(labels)
        codebooks.append(centers)
        residual = residual - centers[labels]
    return np.stack(assignments, axis=1), tuple(codebooks)


def _kmeans(
    values: np.ndarray, clusters: int, seed: int, iterations: int
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    # k-means++ seeding keeps the hierarchy stable on sparse MovieLens features.
    indices = [int(rng.integers(len(values)))]
    distances = np.sum((values - values[indices[0]]) ** 2, axis=1)
    for _ in range(1, clusters):
        total = float(distances.sum())
        index = int(rng.integers(len(values))) if total == 0 else int(
            rng.choice(len(values), p=distances / total)
        )
        indices.append(index)
        distances = np.minimum(
            distances, np.sum((values - values[index]) ** 2, axis=1)
        )
    centers = values[indices].copy()
    labels = np.full(len(values), -1, dtype=np.int64)
    for _ in range(iterations):
        squared_distances = (
            np.sum(values * values, axis=1, keepdims=True)
            + np.sum(centers * centers, axis=1)[None, :]
            - 2.0 * values @ centers.T
        )
        next_labels = np.argmin(squared_distances, axis=1)
        if np.array_equal(labels, next_labels):
            break
        labels = next_labels
        for cluster in range(clusters):
            members = values[labels == cluster]
            if len(members):
                centers[cluster] = members.mean(axis=0)
    return centers, labels


def _hashed_title_features(titles: tuple[str, ...], dimensions: int) -> np.ndarray:
    matrix = np.zeros((len(titles), dimensions), dtype=np.float64)
    document_frequency = np.zeros(dimensions, dtype=np.float64)
    for row, title in enumerate(titles):
        seen: set[int] = set()
        for word in re.findall(r"[a-z0-9]+", title.lower()):
            digest = hashlib.blake2b(word.encode(), digest_size=8).digest()
            column = int.from_bytes(digest, "little") % dimensions
            matrix[row, column] += 1.0
            seen.add(column)
        document_frequency[list(seen)] += 1.0
    matrix *= np.log((1.0 + len(titles)) / (1.0 + document_frequency))[None, :]
    return matrix / np.maximum(np.linalg.norm(matrix, axis=1, keepdims=True), 1.0)


def ranking_from_beams(
    beams: list[tuple[tuple[int, ...], float]],
    code_to_items: dict[tuple[int, ...], tuple[int, ...]],
    history: tuple[int, ...],
    popularity: np.ndarray,
    top_k: int = 10,
) -> tuple[int, ...]:
    scored: list[tuple[float, float, int]] = []
    seen = set(history)
    for code, score in beams:
        for item in code_to_items.get(code, ()):
            if item not in seen:
                collision_penalty = math.log(max(1, len(code_to_items[code])))
                scored.append((score - collision_penalty, popularity[item], item))
    scored.sort(reverse=True)
    return tuple(item for _, _, item in scored[:top_k])
