from __future__ import annotations

import numpy as np


def _unit(values: np.ndarray) -> np.ndarray:
    return values / np.maximum(np.linalg.norm(values, axis=1, keepdims=True), 1e-12)


def paired_views(data) -> tuple[np.ndarray, np.ndarray]:
    """Build public content and collaborative modalities for the same items."""
    content = _unit(data.features.astype(np.float64))
    cooccurrence = np.full((data.item_count, data.item_count), 1e-4, dtype=np.float64)
    for sequence in data.train:
        recent = tuple(sequence[-32:])
        for left in recent:
            for right in recent:
                if left != right:
                    cooccurrence[left, right] += 1.0
    u, singular, _ = np.linalg.svd(cooccurrence, full_matrices=False)
    collaborative = _unit(u[:, : min(32, len(singular))] * np.sqrt(singular[:32]))
    return content, collaborative


def align_views(content: np.ndarray, collaborative: np.ndarray, dimension: int = 16):
    rank = min(dimension, content.shape[1], collaborative.shape[1])
    left, _, right = np.linalg.svd(content.T @ collaborative, full_matrices=False)
    content_embedding = _unit(content @ left[:, :rank])
    collaborative_embedding = _unit(collaborative @ right.T[:, :rank])
    return content_embedding, collaborative_embedding


def refine_with_cross_scale_teacher(content_embedding, collaborative_embedding):
    """Curated relevance + cross-scale teacher refinement used by WeMM stage 2."""
    teacher = _unit(content_embedding + collaborative_embedding)
    return (
        _unit(0.72 * content_embedding + 0.28 * teacher),
        _unit(0.72 * collaborative_embedding + 0.28 * teacher),
    )


def retrieval_metrics(left: np.ndarray, right: np.ndarray) -> dict[str, float]:
    similarity = left @ right.T
    order = np.argsort(-similarity, axis=1)
    targets = np.arange(len(left))
    recall1 = np.mean(order[:, 0] == targets)
    recall10 = np.mean([target in order[index, :10] for index, target in enumerate(targets)])
    ranks = np.argmax(order == targets[:, None], axis=1) + 1
    return {"recall_at_1": float(recall1), "recall_at_10": float(recall10), "mrr": float(np.mean(1.0 / ranks))}
