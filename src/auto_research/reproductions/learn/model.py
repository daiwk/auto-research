from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..industrial_ranking import initialize, require_backend, summarize_training
from ..rec_utils import ranking_metrics
from ..sequence_training import padded_windows


@dataclass(frozen=True)
class LEARNConfig:
    model_name: str = "prajjwal1/bert-tiny"
    dimensions: int = 64
    heads: int = 4
    layers: int = 2
    sequence_length: int = 24
    batch_size: int = 64
    steps: int = 140
    learning_rate: float = 4e-4


def content_embeddings(titles, root: Path, config: LEARNConfig):
    try:
        import torch
        from transformers import AutoModel, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("LEARN requires `pip install -e '.[plum]'`.") from exc
    cache = root / "learn" / "bert-tiny-content.npy"
    if cache.exists():
        values = np.load(cache)
        if values.shape[0] == len(titles): return values
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    model = AutoModel.from_pretrained(config.model_name)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device).eval(); rows = []
    with torch.inference_mode():
        for start in range(0, len(titles), 128):
            encoded = tokenizer(list(titles[start:start + 128]), padding=True, truncation=True, max_length=32, return_tensors="pt").to(device)
            hidden = model(**encoded, return_dict=True).last_hidden_state
            mask = encoded["attention_mask"].unsqueeze(-1)
            rows.append(((hidden * mask).sum(1) / mask.sum(1).clamp_min(1)).cpu().numpy())
    values = np.concatenate(rows).astype(np.float32)
    cache.parent.mkdir(parents=True, exist_ok=True); np.save(cache, values)
    return values


def build_model(content: np.ndarray, config: LEARNConfig):
    torch, nn = require_backend()

    class LEARN(nn.Module):
        def __init__(self):
            super().__init__(); self.register_buffer("content", torch.tensor(content))
            self.content_adapter = nn.Sequential(nn.Linear(content.shape[1], config.dimensions), nn.GELU(), nn.Linear(config.dimensions, config.dimensions))
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            layer = nn.TransformerEncoderLayer(config.dimensions, config.heads, 4 * config.dimensions, batch_first=True, norm_first=True, dropout=0.0)
            self.pch = nn.TransformerEncoder(layer, config.layers)
            self.online_projection = nn.Linear(config.dimensions, config.dimensions)

        def item_vectors(self):
            return torch.nn.functional.normalize(self.content_adapter(self.content), dim=-1)

        def forward(self, items):
            positions = torch.arange(items.shape[1], device=items.device)
            hidden = self.content_adapter(self.content[items]) + self.position(positions)
            causal = torch.triu(torch.ones(items.shape[1], items.shape[1], device=items.device, dtype=torch.bool), 1)
            users = torch.nn.functional.normalize(self.online_projection(self.pch(hidden, mask=causal)), dim=-1)
            return users @ self.item_vectors().T

    return LEARN()


def train_model(model, data, config: LEARNConfig, seed: int):
    model, device, torch = initialize(model, seed)
    rows = padded_windows(data.train, config.sequence_length); rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate); losses = []
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        inputs = torch.tensor([row[0] for row in batch], device=device)
        targets = torch.tensor([row[1] for row in batch], device=device)
        valid = torch.tensor([row[2] for row in batch], device=device)
        logits = model(inputs)
        token_loss = torch.nn.functional.cross_entropy(logits.flatten(0, 1), targets.flatten(), reduction="none").reshape_as(valid)
        loss = (token_loss * valid).sum() / valid.sum()
        optimizer.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step(); losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def evaluate_semantic_mean(content, data, config):
    normalized = content / np.maximum(np.linalg.norm(content, axis=1, keepdims=True), 1e-8)
    def scorer(history):
        user = normalized[list(history[-config.sequence_length:])].mean(0)
        return normalized @ user
    return ranking_metrics(data, scorer)


def evaluate_learn(model, data, config):
    torch, _ = require_backend(); device = next(model.parameters()).device
    def scorer(history):
        recent = history[-config.sequence_length:]
        padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
        with torch.inference_mode(): return model(torch.tensor([padded], device=device))[0, -1].cpu().numpy()
    model.eval(); return ranking_metrics(data, scorer)
