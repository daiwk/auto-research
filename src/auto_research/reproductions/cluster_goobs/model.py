from __future__ import annotations

import numpy as np

from ..mdcns.model import SequentialModel


def train_retriever(data, method: str, seed: int, factors: int = 24, epochs: int = 5):
    rng = np.random.default_rng(seed)
    model = SequentialModel.create(data.item_count, factors, seed)
    examples = np.asarray(
        [(a, b) for sequence in data.train for a, b in zip(sequence, sequence[1:])],
        dtype=np.int64,
    )
    clusters = np.argmax(data.item_features, axis=1)
    members = {cluster: np.flatnonzero(clusters == cluster) for cluster in np.unique(clusters)}
    for _ in range(epochs):
        rng.shuffle(examples)
        for context, positive in examples:
            if method == "cluster_goobs" and rng.random() < 15 / 16:
                pool = members[int(clusters[positive])]
                negative = int(pool[rng.integers(len(pool))])
                if negative == positive:
                    negative = int(pool[(np.flatnonzero(pool == positive)[0] + 1) % len(pool)])
            else:
                negative = int(rng.integers(data.item_count))
                if negative == positive:
                    negative = (negative + 1) % data.item_count
            model.bpr_update(int(context), int(positive), negative, 0.035, 0.002)
    return model
