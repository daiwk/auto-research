from __future__ import annotations

import numpy as np

from ..p0_2026_common import normalized


def train_id_proxy(data):
    content = data.sequences.features.astype(np.float64)
    id_space = np.concatenate((data.transition, data.transition.T), axis=1)
    u, singular, _ = np.linalg.svd(id_space, full_matrices=False)
    id_target = u[:, :32] * singular[:32]
    id_target /= np.maximum(np.linalg.norm(id_target, axis=1, keepdims=True), 1e-9)
    projection = np.linalg.solve(
        content.T @ content + 0.05 * np.eye(content.shape[1]),
        content.T @ id_target,
    )
    losses = []
    tau = 0.12
    for _ in range(40):
        proxy = content @ projection
        proxy /= np.maximum(np.linalg.norm(proxy, axis=1, keepdims=True), 1e-9)
        logits = proxy @ id_target.T / tau
        logits -= logits.max(1, keepdims=True)
        probabilities = np.exp(logits)
        probabilities /= probabilities.sum(1, keepdims=True)
        losses.append(float(-np.log(np.maximum(np.diag(probabilities), 1e-12)).mean()))
        gradient = probabilities
        gradient[np.arange(len(content)), np.arange(len(content))] -= 1.0
        gradient /= len(content)
        projection -= 0.08 * content.T @ (gradient @ id_target / tau)
    proxy = content @ projection
    proxy /= np.maximum(np.linalg.norm(proxy, axis=1, keepdims=True), 1e-9)
    alignment = float(np.mean(np.sum(proxy * id_target, axis=1)))

    def scorer(history):
        representation = proxy[list(history[-8:])].mean(0)
        coarse = proxy @ representation
        multi_layer = 0.6 * coarse + 0.4 * np.tanh(2 * coarse)
        gate = 1 / (1 + np.exp(-4 * (alignment - 0.2)))
        return gate * normalized(multi_layer) + (1 - gate) * data.transition[history[-1]]

    return scorer, {
        "proxy_alignment_cosine": alignment,
        "contrastive_initial_loss": losses[0],
        "contrastive_final_loss": losses[-1],
        "contrastive_steps": len(losses),
        "coarse_contrastive_alignment": True,
        "multi_layer_proxy_adapter": True,
        "residual_gate": True,
    }
