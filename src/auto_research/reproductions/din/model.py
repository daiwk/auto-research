from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import initialize, require_backend, summarize_training, training_examples


@dataclass(frozen=True)
class DINConfig:
    dimensions: int = 48
    sequence_length: int = 32
    batch_size: int = 64
    steps: int = 240
    learning_rate: float = 5e-4
    candidate_chunk: int = 256


def build_model(kind: str, item_count: int, item_features: np.ndarray, config: DINConfig):
    torch, nn = require_backend()
    features = torch.tensor(item_features, dtype=torch.float32)

    class Dice(nn.Module):
        def __init__(self, width: int):
            super().__init__()
            self.alpha = nn.Parameter(torch.zeros(width))
            self.beta = nn.Parameter(torch.zeros(width))
            self.normalization = nn.BatchNorm1d(width, affine=False)

        def forward(self, values):
            normalized = self.normalization(values)
            probability = torch.sigmoid(self.beta * normalized)
            return probability * values + (1.0 - probability) * self.alpha * values

    class DIN(nn.Module):
        def __init__(self):
            super().__init__()
            half = config.dimensions // 2
            self.item = nn.Embedding(item_count, half)
            self.genre = nn.Linear(item_features.shape[1], half, bias=False)
            self.register_buffer("features", features)
            self.attention = nn.Sequential(
                nn.Linear(4 * config.dimensions, 80),
                nn.Sigmoid(),
                nn.Linear(80, 40),
                nn.Sigmoid(),
                nn.Linear(40, 1),
            )
            self.interest = nn.Linear(config.dimensions, config.dimensions)
            self.hidden1 = nn.Linear(3 * config.dimensions, 80)
            self.dice1 = Dice(80)
            self.hidden2 = nn.Linear(80, 40)
            self.dice2 = Dice(40)
            self.output = nn.Linear(40, 1)
            self.item_bias = nn.Embedding(item_count, 1)
            nn.init.normal_(self.item.weight, std=0.02)
            nn.init.zeros_(self.item_bias.weight)

        def embed(self, items):
            return torch.cat((self.item(items), self.genre(self.features[items])), dim=-1)

        def forward(self, histories, candidates):
            history = self.embed(histories)
            candidate = self.embed(candidates)
            if candidate.ndim == 2:
                candidate = candidate[:, None, :]
            history = history[:, None, :, :]
            query = candidate[:, :, None, :].expand(-1, -1, history.shape[2], -1)
            keys = history.expand(-1, candidate.shape[1], -1, -1)
            if kind == "din":
                attention_input = torch.cat(
                    (query, keys, query - keys, query * keys), dim=-1
                )
                weights = torch.softmax(
                    self.attention(attention_input).squeeze(-1)
                    / config.dimensions**0.5,
                    dim=-1,
                )
            elif kind == "mean_pool":
                weights = torch.full(
                    keys.shape[:-1], 1.0 / keys.shape[2], device=keys.device
                )
            else:
                raise ValueError(f"unknown DIN kind: {kind}")
            pooled = (weights.unsqueeze(-1) * keys).sum(dim=2)
            pooled = self.interest(pooled)
            joined = torch.cat((pooled, candidate, pooled * candidate), dim=-1)
            hidden = self.dice1(self.hidden1(joined).reshape(-1, 80))
            hidden = self.dice2(self.hidden2(hidden)).view(*joined.shape[:-1], 40)
            logits = self.output(hidden).squeeze(-1)
            logits += self.item_bias(candidates).squeeze(-1)
            return logits

    return DIN()


def train_model(kind: str, data, config: DINConfig, seed: int):
    model = build_model(kind, data.item_count, data.item_features, config)
    model, device, torch = initialize(model, seed)
    rows = training_examples(data.train, config.sequence_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    model.train()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = torch.tensor([row[0] for row in batch], device=device)
        positives = torch.tensor([row[1] for row in batch], device=device)
        negatives = torch.randint(0, data.item_count, positives.shape, device=device)
        candidates = torch.stack((positives, negatives), dim=1)
        logits = model(histories, candidates)
        labels = torch.tensor([[1.0, 0.0]], device=device).expand_as(logits)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def score_all(model, history, item_count: int, config: DINConfig):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    recent = history[-config.sequence_length :]
    padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
    histories = torch.tensor([padded], device=device)
    scores = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, item_count, config.candidate_chunk):
            candidates = torch.arange(
                start, min(start + config.candidate_chunk, item_count), device=device
            )[None, :]
            scores.append(model(histories, candidates)[0].cpu().numpy())
    return np.concatenate(scores)
