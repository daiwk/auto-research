from __future__ import annotations

from auto_research.runtime import device_for

import random
import time
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import require_backend
from ..llm_rec_data import binary_auc
from ..tiger.model import residual_kmeans


@dataclass(frozen=True)
class SaviorConfig:
    dimensions: int = 48
    codebooks: int = 3
    codebook_size: int = 16
    encoder_steps: int = 160
    ranker_steps: int = 180
    batch_size: int = 64
    learning_rate: float = 6e-4
    maximum_train: int = 8000
    maximum_test: int = 2000


def train_behavior_encoder(features, positive_pairs, config: SaviorConfig, seed: int):
    torch, nn = require_backend()
    torch.manual_seed(seed)
    rng = random.Random(seed)
    device = device_for(torch)
    values = torch.tensor(features, dtype=torch.float32, device=device)
    encoder = nn.Sequential(
        nn.Linear(features.shape[1], 2 * config.dimensions), nn.GELU(),
        nn.Linear(2 * config.dimensions, config.dimensions), nn.LayerNorm(config.dimensions),
    ).to(device)
    optimizer = torch.optim.AdamW(encoder.parameters(), lr=1e-3)
    losses = []
    for _ in range(config.encoder_steps):
        batch = [positive_pairs[rng.randrange(len(positive_pairs))] for _ in range(config.batch_size)]
        left = torch.tensor([row[0] for row in batch], device=device)
        right = torch.tensor([row[1] for row in batch], device=device)
        z_left = torch.nn.functional.normalize(encoder(values[left]), dim=-1)
        z_right = torch.nn.functional.normalize(encoder(values[right]), dim=-1)
        logits = z_left @ z_right.T / 0.07
        labels = torch.arange(len(batch), device=device)
        loss = (torch.nn.functional.cross_entropy(logits, labels) + torch.nn.functional.cross_entropy(logits.T, labels)) / 2
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    with torch.inference_mode():
        aligned = encoder(values).cpu().numpy()
    codes = residual_kmeans(aligned, config.codebooks, config.codebook_size, seed + 31)
    return aligned.astype(np.float32), codes, {
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
    }


def build_ranker(item_count, aligned, codes, config: SaviorConfig, use_savior: bool):
    torch, nn = require_backend()
    code_tensor = torch.tensor(codes, dtype=torch.long)

    class Ranker(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.register_buffer("aligned", torch.tensor(aligned))
            self.register_buffer("codes", code_tensor)
            self.content = nn.Linear(aligned.shape[1], config.dimensions)
            self.mba = nn.ParameterList([
                nn.Parameter(torch.zeros(config.codebook_size, config.dimensions))
                for _ in range(config.codebooks)
            ])
            self.target_attention = nn.MultiheadAttention(config.dimensions, 4, batch_first=True)
            self.history_attention = nn.MultiheadAttention(config.dimensions, 4, batch_first=True)
            self.score = nn.Sequential(
                nn.Linear(4 * config.dimensions, 2 * config.dimensions), nn.GELU(),
                nn.Linear(2 * config.dimensions, 1),
            )

        def semantic(self, items):
            content = self.content(self.aligned[items])
            if not use_savior:
                return content
            residual = sum(table[self.codes[items, level]] for level, table in enumerate(self.mba))
            return content + residual

        def forward(self, histories, candidates):
            history = self.item(histories) + self.semantic(histories)
            target = self.item(candidates) + self.semantic(candidates)
            if use_savior:
                target_query = target.unsqueeze(1)
                target_view, _ = self.target_attention(target_query, history, history)
                target_tokens = target.unsqueeze(1).expand(-1, history.shape[1], -1)
                history_view, _ = self.history_attention(history, target_tokens, target_tokens)
                user = (history + history_view).mean(1)
                target = target + target_view.squeeze(1)
            else:
                user = history.mean(1)
            return self.score(torch.cat((user, target, user * target, (user - target).abs()), dim=-1)).squeeze(-1)

    return Ranker()


def train_ranker(model, train, test, item_frequency, config: SaviorConfig, seed: int):
    torch, _ = require_backend()
    torch.manual_seed(seed)
    rng = random.Random(seed)
    device = device_for(torch)
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rows = train[: config.maximum_train]
    losses = []
    started = time.perf_counter()
    for _ in range(config.ranker_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        width = max(len(row.items) for row in batch)
        histories = torch.tensor([((row.items[0],) * (width - len(row.items)) + row.items) for row in batch], device=device)
        candidates = torch.tensor([row.candidate for row in batch], device=device)
        labels = torch.tensor([row.label for row in batch], dtype=torch.float32, device=device)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(model(histories, candidates), labels)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    labels, scores, cold_labels, cold_scores = [], [], [], []
    threshold = float(np.quantile(item_frequency[item_frequency > 0], 0.25))
    model.eval()
    with torch.inference_mode():
        for row in test[: config.maximum_test]:
            history = torch.tensor([row.items], device=device)
            candidate = torch.tensor([row.candidate], device=device)
            score = float(torch.sigmoid(model(history, candidate)).cpu())
            labels.append(row.label)
            scores.append(score)
            if item_frequency[row.candidate] <= threshold:
                cold_labels.append(row.label)
                cold_scores.append(score)
    return {
        "auc": binary_auc(labels, scores),
        "cold_auc": binary_auc(cold_labels, cold_scores),
        "cold_examples": len(cold_labels),
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
        "seconds": time.perf_counter() - started,
        "mba_l2": float(sum(table.square().sum() for table in model.mba).sqrt().detach().cpu()),
    }
