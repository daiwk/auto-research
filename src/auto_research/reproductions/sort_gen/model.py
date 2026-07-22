from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from auto_research.runtime import device_for
from ..llm_training import require_torch


@dataclass(frozen=True)
class SortConfig:
    dimensions: int = 48
    heads: int = 4
    layers: int = 2
    list_size: int = 8
    training_steps: int = 180
    batch_size: int = 48
    learning_rate: float = 6e-4


def build_model(features: np.ndarray, config: SortConfig):
    torch = require_torch(); nn = torch.nn
    feature_tensor = torch.tensor(features, dtype=torch.float32)

    class SORT(nn.Module):
        def __init__(self):
            super().__init__(); self.register_buffer("features", feature_tensor)
            self.item = nn.Linear(features.shape[1], config.dimensions)
            self.user = nn.Linear(features.shape[1], config.dimensions)
            self.prior = nn.Linear(3, config.dimensions)
            self.position = nn.Embedding(config.list_size, config.dimensions)
            layer = nn.TransformerEncoderLayer(config.dimensions, config.heads, 4 * config.dimensions, batch_first=True, norm_first=True, dropout=0.0)
            self.encoder = nn.TransformerEncoder(layer, config.layers)
            self.click = nn.Linear(config.dimensions, config.list_size)
            self.pay = nn.Linear(config.dimensions, config.list_size)

        def forward(self, items, users, prior):
            positions = torch.arange(items.shape[1], device=items.device)
            hidden = self.item(self.features[items]) + self.user(users).unsqueeze(1) + self.prior(prior) + self.position(positions)
            causal = torch.triu(torch.ones(items.shape[1], items.shape[1], dtype=torch.bool, device=items.device), diagonal=1)
            hidden = self.encoder(hidden, mask=causal)
            return self.click(hidden), self.pay(hidden)

    return SORT()


def ordered_targets(values, thresholds: int, torch):
    counts = values.cumsum(1).long()
    levels = torch.arange(1, thresholds + 1, device=values.device)
    return (counts.unsqueeze(-1) >= levels).float()


def train(model, data, config: SortConfig, seed: int):
    torch = require_torch(); torch.manual_seed(seed); random.seed(seed)
    device = device_for(torch); model.to(device); rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate); losses = []
    model.train()
    for _ in range(config.training_steps):
        rows = [data.train[rng.randrange(len(data.train))] for _ in range(config.batch_size)]
        items = torch.tensor(np.stack([row.items for row in rows]), dtype=torch.long, device=device)
        users = torch.tensor(np.stack([row.user for row in rows]), device=device)
        prior = torch.tensor(np.stack([row.prior for row in rows]), device=device)
        click = torch.tensor(np.stack([row.click for row in rows]), device=device)
        pay = torch.tensor(np.stack([row.pay for row in rows]), device=device)
        click_logits, pay_logits = model(items, users, prior)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(click_logits, ordered_targets(click, config.list_size, torch)) + torch.nn.functional.binary_cross_entropy_with_logits(pay_logits, ordered_targets(pay, config.list_size, torch))
        optimizer.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:20])), "final_loss": float(np.mean(losses[-20:])), "steps": config.training_steps, "device": device.type}


def formula_greedy(row, size: int):
    scores = 5 * row.prior[:, 0] + row.prior[:, 1] + row.prior[:, 2]
    return np.argsort(-scores)[:size]


def mask_driven_generate(model, row, features, config: SortConfig, mmr_lambda: float):
    torch = require_torch(); device = next(model.parameters()).device
    queues = np.stack([np.argsort(-row.prior[:, objective])[:config.list_size] for objective in range(3)])
    items = torch.tensor(row.items[queues], dtype=torch.long, device=device)
    users = torch.tensor(np.repeat(row.user[None], 3, 0), device=device)
    prior = torch.tensor(row.prior[queues], device=device)
    model.eval()
    with torch.inference_mode():
        click, pay = model(items, users, prior)
        values = (5 * torch.sigmoid(click).sum(-1) + torch.sigmoid(pay).sum(-1)).cpu().numpy()
    pointers = [0, 0, 0]; selected = []; calls = 1
    while len(selected) < config.list_size:
        choices = []
        for queue in range(3):
            while pointers[queue] < config.list_size and int(queues[queue, pointers[queue]]) in selected:
                pointers[queue] += 1
            if pointers[queue] >= config.list_size:
                continue
            index = pointers[queue]; candidate = int(queues[queue, index]); value = float(values[queue, index])
            if selected:
                similarity = float(np.max(features[row.items[selected]] @ features[row.items[candidate]]))
            else:
                similarity = 0.0
            choices.append((mmr_lambda * value - (1 - mmr_lambda) * similarity, queue, candidate))
        if not choices: break
        _, queue, candidate = max(choices); selected.append(candidate); pointers[queue] += 1
    return np.asarray(selected, dtype=np.int64), calls


def evaluate(rows, generator, features, size: int):
    click = pay = gmv = diversity = calls = 0.0
    for row in rows:
        generated = generator(row); order, model_calls = generated if isinstance(generated, tuple) else (generated, 0)
        click += row.click[order].sum(); pay += row.pay[order].sum(); gmv += row.gmv[order].sum(); calls += model_calls
        vectors = features[row.items[order]]; similarity = vectors @ vectors.T
        diversity += 1 - (similarity.sum() - np.trace(similarity)) / max(len(order) * (len(order) - 1), 1)
    count = len(rows)
    return {"click_per_slate": float(click / count), "pay_per_slate": float(pay / count), "gmv_proxy_per_slate": float(gmv / count), "ilad": float(diversity / count), "model_calls_per_slate": float(calls / count)}
