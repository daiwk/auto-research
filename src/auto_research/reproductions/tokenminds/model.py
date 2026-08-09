from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TokenMindsConfig:
    dimensions: int = 32
    maximum_history: int = 32
    sid_levels: int = 2
    sid_cardinality: int = 16
    steps: int = 120
    batch_size: int = 64
    learning_rate: float = 8e-4
    sid_loss_weight: float = 0.30


def build_semantic_codes(features: np.ndarray, config: TokenMindsConfig) -> np.ndarray:
    """Build hierarchical public-data SIDs with residual quantization.

    The paper reuses PLUM's RQ-VAE codes.  MovieLens exposes genre vectors rather
    than YouTube multimodal embeddings, so the local adapter applies the same
    coarse-to-fine residual-code principle with deterministic residual k-means.
    """

    from ..plum.model import residual_kmeans

    cardinalities = (config.sid_cardinality,) * config.sid_levels
    codes, _ = residual_kmeans(np.asarray(features, dtype=np.float64), cardinalities)
    return codes.astype(np.int64)


def build_model(data, codes: np.ndarray, config: TokenMindsConfig, *, dual_output: bool):
    import torch
    from torch import nn

    features = torch.tensor(data.features, dtype=torch.float32)
    code_tensor = torch.tensor(codes, dtype=torch.long)

    class TokenMindsModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.dual_output = dual_output
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.content = nn.Linear(features.shape[1], config.dimensions, bias=False)
            self.encoder = nn.GRU(config.dimensions, config.dimensions, batch_first=True)
            self.register_buffer("features", features)
            self.register_buffer("item_codes", code_tensor)
            if dual_output:
                self.sid_heads = nn.ModuleList(
                    nn.Linear(config.dimensions, config.sid_cardinality)
                    for _ in range(config.sid_levels)
                )
                self.sid_embeddings = nn.ModuleList(
                    nn.Embedding(config.sid_cardinality, config.dimensions)
                    for _ in range(config.sid_levels)
                )
                # Start from the parameter-matched dense path and learn how much
                # discrete user-token signal to add.  This mirrors a safe feature
                # launch: the new representation cannot destroy the dense feature
                # before the downstream model has learned to use it.
                self.token_gate = nn.Parameter(torch.tensor(-3.0))

        def item_values(self):
            return self.item.weight + self.content(self.features)

        def encode(self, histories):
            values = self.item(histories) + self.content(self.features[histories])
            dense = self.encoder(values)[0][:, -1]
            if not self.dual_output:
                return dense, ()
            sid_logits = tuple(head(dense) for head in self.sid_heads)
            # Soft token decoding keeps the generated user-token path differentiable.
            token = sum(
                torch.softmax(logits, -1) @ embedding.weight
                for logits, embedding in zip(sid_logits, self.sid_embeddings)
            ) / config.sid_levels
            return dense + torch.sigmoid(self.token_gate) * token, sid_logits

        def forward(self, histories):
            user, sid_logits = self.encode(histories)
            return user @ self.item_values().T, sid_logits

    return TokenMindsModel()
