from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class MixFormerConfig:
    dimensions: int = 64
    heads: int = 4
    layers: int = 2
    sequence_length: int = 32
    batch_size: int = 64
    steps: int = 240
    learning_rate: float = 3e-4


def require_backend():
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError(
            "MixFormer trains real neural baselines and needs PyTorch; install "
            "with `pip install -e '.[neural-recs]'`."
        ) from exc
    return torch, nn


def build_model(kind: str, item_features: np.ndarray, config: MixFormerConfig):
    torch, nn = require_backend()
    feature_values = torch.tensor(item_features, dtype=torch.float32)
    item_count, feature_count = feature_values.shape

    class StackedModel(nn.Module):
        """Conventional independently-parameterized sequence/dense towers."""

        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count + 1, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.sequence = nn.TransformerEncoder(layer, config.layers)
            self.dense = nn.Sequential(
                nn.Linear(feature_count, config.dimensions), nn.GELU(),
                nn.Linear(config.dimensions, config.dimensions),
            )
            self.fuse = nn.Linear(2 * config.dimensions, config.dimensions)
            self.register_buffer("features", feature_values)

        def encode_user(self, history):
            positions = torch.arange(history.shape[1], device=history.device)
            tokens = self.item(history + 1) + self.position(positions)
            sequence = self.sequence(tokens)[:, -1]
            dense = self.dense(self.features[history].mean(dim=1))
            return self.fuse(torch.cat((sequence, dense), dim=-1))

        def item_vectors(self):
            ids = torch.arange(item_count, device=self.item.weight.device)
            return self.item(ids + 1) + self.dense(self.features)

        def forward(self, history):
            return self.encode_user(history) @ self.item_vectors().T

    class UnifiedModel(nn.Module):
        """Feature-split dense tokens and sequence tokens share every block."""

        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count + 1, config.dimensions)
            self.feature_columns = nn.Parameter(
                torch.randn(feature_count, config.dimensions) * 0.02
            )
            self.position = nn.Embedding(
                config.sequence_length + config.heads, config.dimensions
            )
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.backbone = nn.TransformerEncoder(layer, config.layers)
            self.item_projection = nn.Linear(
                config.dimensions + feature_count, config.dimensions
            )
            self.register_buffer("features", feature_values)

        def _dense_tokens(self, history):
            profile = self.features[history].mean(dim=1)
            chunks = torch.chunk(profile, config.heads, dim=-1)
            columns = torch.chunk(self.feature_columns, config.heads, dim=0)
            return torch.stack(
                [part @ weight for part, weight in zip(chunks, columns, strict=True)],
                dim=1,
            )

        def encode_user(self, history):
            dense = self._dense_tokens(history)
            sequence = self.item(history + 1)
            tokens = torch.cat((dense, sequence), dim=1)
            positions = torch.arange(tokens.shape[1], device=history.device)
            encoded = self.backbone(tokens + self.position(positions))
            return encoded[:, : config.heads].mean(dim=1) + encoded[:, -1]

        def item_vectors(self):
            ids = torch.arange(item_count, device=self.item.weight.device)
            return self.item_projection(
                torch.cat((self.item(ids + 1), self.features), dim=-1)
            )

        def forward(self, history):
            # User encoding is computed once and reused for all candidate items.
            return self.encode_user(history) @ self.item_vectors().T

    if kind == "stacked":
        return StackedModel()
    if kind == "unified":
        return UnifiedModel()
    raise ValueError(f"unknown MixFormer model kind: {kind}")


def train_model(kind: str, data, seed: int, config: MixFormerConfig):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = build_model(kind, data.item_features, config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    examples = training_examples(data.train, config.sequence_length)
    rng = random.Random(seed)
    losses: list[float] = []
    model.train()
    for _ in range(config.steps):
        batch = [examples[rng.randrange(len(examples))] for _ in range(config.batch_size)]
        histories = torch.tensor([row[0] for row in batch], dtype=torch.long, device=device)
        targets = torch.tensor([row[1] for row in batch], dtype=torch.long, device=device)
        optimizer.zero_grad(set_to_none=True)
        loss = torch.nn.functional.cross_entropy(model(histories), targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def training_examples(sequences, length: int) -> tuple[tuple[tuple[int, ...], int], ...]:
    examples = []
    for sequence in sequences:
        for position in range(1, len(sequence)):
            history = sequence[max(0, position - length) : position]
            padded = (history[0],) * (length - len(history)) + history
            examples.append((padded, sequence[position]))
    return tuple(examples)


def evaluate_model(model: Any, data, config: MixFormerConfig) -> dict[str, float]:
    torch, _ = require_backend()
    device = next(model.parameters()).device

    def scorer(history):
        recent = history[-config.sequence_length :]
        padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
        with torch.inference_mode():
            values = model(
                torch.tensor([padded], dtype=torch.long, device=device)
            )[0]
        return values.detach().cpu().numpy()

    from ..rec_utils import ranking_metrics

    model.eval()
    return ranking_metrics(data, scorer)
