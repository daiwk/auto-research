from __future__ import annotations

from auto_research.runtime import device_for

import random
import time
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import require_backend
from ..llm_rec_data import binary_auc


@dataclass(frozen=True)
class GenRankConfig:
    dimensions: int = 48
    heads: int = 4
    layers: int = 2
    history: int = 16
    batch_size: int = 64
    steps: int = 120
    learning_rate: float = 5e-4
    maximum_train: int = 8000
    maximum_test: int = 2000


def build_model(item_count: int, config: GenRankConfig, packed: bool):
    torch, nn = require_backend()

    class Ranker(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count + 1, config.dimensions, padding_idx=0)
            self.action = nn.Embedding(4, config.dimensions)
            self.time = nn.Embedding(32, config.dimensions)
            maximum = 2 * config.history + 1 if not packed else config.history + 1
            self.position = nn.Embedding(maximum, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.transformer = nn.TransformerEncoder(layer, config.layers)
            self.head = nn.Sequential(nn.LayerNorm(config.dimensions), nn.Linear(config.dimensions, 1))

        def forward(self, items, actions, times, candidate):
            if packed:
                hidden = self.item(items) + self.action(actions) + self.time(times)
            else:
                item_tokens = self.item(items) + self.time(times)
                action_tokens = self.action(actions)
                hidden = torch.stack((item_tokens, action_tokens), dim=2).flatten(1, 2)
            hidden = torch.cat((hidden, self.item(candidate).unsqueeze(1)), dim=1)
            positions = torch.arange(hidden.shape[1], device=hidden.device)
            hidden = hidden + self.position(positions)
            causal = torch.triu(torch.ones(hidden.shape[1], hidden.shape[1], device=hidden.device, dtype=torch.bool), 1)
            return self.head(self.transformer(hidden, mask=causal)[:, -1]).squeeze(-1)

    return Ranker()


def train_evaluate(model, train, test, config: GenRankConfig, seed: int):
    torch, _ = require_backend()
    device = device_for(torch)
    torch.manual_seed(seed)
    model.to(device).train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    for _ in range(config.steps):
        batch = [train[rng.randrange(len(train))] for _ in range(config.batch_size)]
        tensors = _batch(batch, config, device, torch)
        labels = tensors.pop("labels")
        loss = torch.nn.functional.binary_cross_entropy_with_logits(model(**tensors), labels)
        optimizer.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    model.eval(); labels, scores, elapsed = [], [], 0.0
    with torch.inference_mode():
        for start in range(0, len(test), config.batch_size):
            batch = test[start:start + config.batch_size]
            tensors = _batch(batch, config, device, torch)
            labels.extend(tensors.pop("labels").cpu().tolist())
            tick = time.perf_counter(); logits = model(**tensors)
            if device.type == "cuda": torch.cuda.synchronize(device)
            elif device.type == "mps": torch.mps.synchronize()
            elapsed += time.perf_counter() - tick
            scores.extend(torch.sigmoid(logits).cpu().tolist())
    return {
        "auc": binary_auc(labels, scores), "examples": len(test),
        "milliseconds_per_example": 1000 * elapsed / len(test),
        "initial_loss": float(np.mean(losses[:20])), "final_loss": float(np.mean(losses[-20:])),
    }


def _batch(rows, config, device, torch):
    items = torch.zeros((len(rows), config.history), dtype=torch.long, device=device)
    actions = torch.zeros_like(items); times = torch.zeros_like(items)
    for index, row in enumerate(rows):
        width = min(config.history, len(row.items))
        items[index, -width:] = torch.tensor(row.items[-width:], device=device) + 1
        actions[index, -width:] = torch.tensor(row.actions[-width:], device=device) + 1
        times[index, -width:] = torch.tensor(row.time_buckets[-width:], device=device)
    return {
        "items": items, "actions": actions, "times": times,
        "candidate": torch.tensor([row.candidate for row in rows], device=device) + 1,
        "labels": torch.tensor([row.label for row in rows], dtype=torch.float32, device=device),
    }
