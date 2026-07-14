from __future__ import annotations

import random
import time

import numpy as np

from ..industrial_batch import device_for, padded_histories, require_torch, training_pairs
from ..tiger.model import residual_kmeans


def ua_sid(data, seed: int):
    content = np.column_stack((data.features, np.log1p(data.popularity)[:, None]))
    codes = residual_kmeans(content.astype(np.float32), 3, 8, seed, iterations=20)
    return np.column_stack((codes, np.arange(data.item_count) % 16)).astype(np.int64)


def build_dlrm(data):
    torch, nn = require_torch()
    class DLRM(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, 40)
        def forward(self, histories):
            return self.item(histories).mean(1) @ self.item.weight.T
    return DLRM()


def build_lazy(data, codes):
    torch, nn = require_torch()
    tokens = torch.tensor(codes, dtype=torch.long)
    cardinalities = (8, 8, 8, 16)
    class LazyAR(nn.Module):
        def __init__(self):
            super().__init__()
            self.register_buffer("codes", tokens)
            self.item = nn.Embedding(data.item_count, 48)
            self.level = nn.Embedding(4, 48)
            self.heads = nn.ModuleList([nn.Linear(48, size) for size in cardinalities])
        def state(self, histories):
            return self.item(histories).mean(1)
        def level_logits(self, histories):
            state = self.state(histories)
            return [head(state + self.level.weight[level]) for level, head in enumerate(self.heads)]
        def forward(self, histories):
            logits = [torch.log_softmax(value, -1) for value in self.level_logits(histories)]
            return sum(value[:, self.codes[:, level]] for level, value in enumerate(logits))
    return LazyAR()


def train_dlrm(data, seed, steps):
    return _train(data, build_dlrm(data), seed, steps, value_aware=False, rspo=False)


def train_gr4ad(data, codes, seed, steps):
    return _train(data, build_lazy(data, codes), seed, steps, value_aware=True, rspo=True)


def _train(data, model, seed, steps, value_aware, rspo):
    torch, _ = require_torch()
    torch.manual_seed(seed)
    device = device_for(torch)
    model.to(device)
    rows = training_pairs(data)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    values = torch.tensor(np.log1p(data.popularity) / max(np.log1p(data.popularity).max(), 1e-6), device=device)
    losses = []
    started = time.perf_counter()
    for step in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(48, len(rows)))]
        histories = padded_histories([row[0] for row in batch], 20, device, torch)
        targets = torch.tensor([row[1] for row in batch], device=device)
        scores = model(histories)
        per_row = torch.nn.functional.cross_entropy(scores, targets, reduction="none")
        loss = (per_row * (1 + values[targets]) if value_aware else per_row).mean()
        if rspo and step >= steps // 2:
            negatives = torch.randint(0, data.item_count, (len(batch), 15), device=device)
            candidates = torch.cat((targets[:, None], negatives), 1)
            candidate_scores = scores.gather(1, candidates)
            relevance = torch.cat((torch.ones((len(batch), 1), device=device), 0.2 * values[negatives]), 1)
            target_distribution = torch.softmax(relevance / 0.2, -1)
            loss = loss + 0.35 * -(target_distribution * torch.log_softmax(candidate_scores, -1)).sum(-1).mean()
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:])), "seconds": time.perf_counter() - started}


def scorer(model):
    torch, _ = require_torch()
    device = next(model.parameters()).device
    model.eval()
    def score(history):
        with torch.inference_mode():
            return model(padded_histories([history], 20, device, torch))[0].cpu().numpy()
    return score

