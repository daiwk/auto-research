from __future__ import annotations

import numpy as np

from ..industrial_2026 import context_matrix, ridge


def train_harness(data, seed: int):
    """Three phases: rich teacher, L2 student alignment, contrastive refinement."""
    contexts, targets = context_matrix(data)
    item_features = data.sequences.features.astype(np.float64)
    # Phase 1: the document tower gets offline collaborative SVD plus content.
    cooccurrence = data.transition + data.transition.T
    u, s, _ = np.linalg.svd(cooccurrence, full_matrices=False)
    collaborative = u[:, :16] * np.sqrt(s[:16])
    teacher_docs = np.concatenate([item_features, collaborative], axis=1)
    teacher_docs /= np.maximum(np.linalg.norm(teacher_docs, axis=1, keepdims=True), 1e-9)
    oracle = np.concatenate([contexts, item_features[targets]], axis=1)
    teacher_query_map = ridge(oracle, teacher_docs[targets])
    teacher_queries = oracle @ teacher_query_map
    teacher_queries /= np.maximum(np.linalg.norm(teacher_queries, axis=1, keepdims=True), 1e-9)
    # Phase 2: deployable query features align directly into frozen teacher space.
    student_map = ridge(contexts, teacher_queries)
    aligned = contexts @ student_map
    alignment_before = float(np.mean((np.pad(contexts, ((0, 0), (0, teacher_docs.shape[1] - contexts.shape[1]))) - teacher_queries) ** 2))
    alignment_after = float(np.mean((aligned - teacher_queries) ** 2))
    # Phase 3: frozen document embeddings; update query projection with InfoNCE gradients.
    rng = np.random.default_rng(seed)
    reference = student_map.copy()
    losses = []
    for _ in range(80):
        ids = rng.choice(len(contexts), min(64, len(contexts)), replace=False)
        query = contexts[ids] @ student_map
        query /= np.maximum(np.linalg.norm(query, axis=1, keepdims=True), 1e-9)
        logits = query @ teacher_docs.T / 0.08
        probabilities = np.exp(np.clip(logits - logits.max(1, keepdims=True), -40, 0))
        probabilities /= probabilities.sum(1, keepdims=True)
        expected = probabilities @ teacher_docs
        gradient = contexts[ids].T @ (expected - teacher_docs[targets[ids]]) / len(ids)
        student_map -= 0.08 * gradient + 1e-4 * (student_map - reference)
        losses.append(float(-np.log(np.maximum(probabilities[np.arange(len(ids)), targets[ids]], 1e-12)).mean()))
    return teacher_docs, student_map, {"teacher": "content + collaborative SVD with oracle target genre", "alignment_mse_before": alignment_before, "alignment_mse_after": alignment_after, "contrastive_loss_initial": losses[0], "contrastive_loss_final": losses[-1], "frozen_document_index": True}


def score_harness(data, teacher_docs, student_map, history):
    context = np.mean(data.sequences.features[list(history[-8:])], axis=0)
    query = context @ student_map
    query /= max(np.linalg.norm(query), 1e-9)
    return query @ teacher_docs.T


def score_small(data, history):
    query = np.mean(data.sequences.features[list(history[-8:])], axis=0)
    return query @ data.sequences.features.T
