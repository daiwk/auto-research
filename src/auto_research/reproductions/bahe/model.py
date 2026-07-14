from __future__ import annotations

import copy
import random
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..llm_rec_data import TextCTRData, binary_auc


@dataclass(frozen=True)
class BAHEConfig:
    model_name: str = "prajjwal1/bert-tiny"
    history_items: int = 12
    maximum_length: int = 128
    batch_size: int = 32
    steps: int = 100
    learning_rate: float = 5e-4
    maximum_train: int = 5000
    maximum_test: int = 1000


def require_backend():
    try:
        import torch
        from torch import nn
        from transformers import AutoModel, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("BAHE requires `pip install -e '.[plum]'`.") from exc
    return torch, nn, AutoModel, AutoTokenizer


def atomic_behavior_embeddings(
    data: TextCTRData, root: Path, config: BAHEConfig
) -> np.ndarray:
    torch, _, AutoModel, AutoTokenizer = require_backend()
    cache = root / "bahe" / "bert-tiny-atomic-behaviors.npy"
    if cache.exists():
        values = np.load(cache)
        if values.shape[0] == len(data.titles):
            return values
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    backbone = AutoModel.from_pretrained(config.model_name)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    backbone.to(device).eval()
    outputs = []
    with torch.inference_mode():
        for start in range(0, len(data.titles), 128):
            encoded = tokenizer(
                list(data.titles[start:start + 128]), padding=True, truncation=True,
                max_length=32, return_tensors="pt",
            ).to(device)
            hidden = backbone.embeddings(input_ids=encoded["input_ids"])
            mask = (1.0 - encoded["attention_mask"][:, None, None, :].to(hidden.dtype)) * -10000.0
            hidden = backbone.encoder.layer[0](hidden, attention_mask=mask)[0]
            weights = encoded["attention_mask"].unsqueeze(-1)
            pooled = (hidden * weights).sum(1) / weights.sum(1).clamp_min(1)
            outputs.append(pooled.cpu().numpy())
    values = np.concatenate(outputs).astype(np.float32)
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.save(cache, values)
    return values


def build_bahe(atomic: np.ndarray, config: BAHEConfig):
    torch, nn, AutoModel, _ = require_backend()
    backbone = AutoModel.from_pretrained(config.model_name)
    upper = copy.deepcopy(backbone.encoder.layer[-1])

    class BAHEModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.register_buffer("atomic", torch.tensor(atomic))
            self.cls = nn.Parameter(torch.zeros(atomic.shape[1]))
            self.upper = upper
            self.head = nn.Sequential(
                nn.Linear(atomic.shape[1], atomic.shape[1]), nn.GELU(),
                nn.Linear(atomic.shape[1], 1),
            )

        def forward(self, histories, lengths, candidates):
            history = self.atomic[histories]
            candidate = self.atomic[candidates].unsqueeze(1)
            cls = self.cls.expand(len(histories), 1, -1)
            hidden = torch.cat((cls, history, candidate), dim=1)
            positions = torch.arange(history.shape[1], device=history.device)[None, :]
            valid_history = positions >= history.shape[1] - lengths[:, None]
            valid = torch.cat(
                (torch.ones((len(histories), 1), device=history.device, dtype=torch.bool),
                 valid_history,
                 torch.ones((len(histories), 1), device=history.device, dtype=torch.bool)),
                dim=1,
            )
            attention = (1.0 - valid[:, None, None, :].to(hidden.dtype)) * -10000.0
            hidden = self.upper(hidden, attention_mask=attention)[0]
            return self.head(hidden[:, 0]).squeeze(-1)

    return BAHEModel()


def build_full_text(config: BAHEConfig):
    torch, nn, AutoModel, AutoTokenizer = require_backend()
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    backbone = AutoModel.from_pretrained(config.model_name)
    for parameter in backbone.parameters():
        parameter.requires_grad = False
    for parameter in backbone.encoder.layer[-1].parameters():
        parameter.requires_grad = True

    class FullTextModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.backbone = backbone
            self.head = nn.Linear(backbone.config.hidden_size, 1)

        def forward(self, encoded):
            hidden = self.backbone(**encoded, return_dict=True).last_hidden_state[:, 0]
            return self.head(hidden).squeeze(-1)

    return FullTextModel(), tokenizer


def train_model(model, tokenizer, data, rows, config: BAHEConfig, seed: int, bahe: bool):
    torch, _, _, _ = require_backend()
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device).train()
    parameters = [value for value in model.parameters() if value.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    started = time.perf_counter()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        logits = _forward(model, tokenizer, data, batch, config, device, torch, bahe)
        labels = torch.tensor([row.label for row in batch], device=device, dtype=torch.float32)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(parameters, 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
        "seconds": time.perf_counter() - started,
        "trainable_parameters": sum(value.numel() for value in parameters),
        "device": device.type,
    }


def evaluate(model, tokenizer, data, rows, config: BAHEConfig, bahe: bool):
    torch, _, _, _ = require_backend()
    device = next(model.parameters()).device
    labels, scores, elapsed = [], [], 0.0
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(rows), config.batch_size):
            batch = rows[start:start + config.batch_size]
            tick = time.perf_counter()
            logits = _forward(model, tokenizer, data, batch, config, device, torch, bahe)
            if device.type == "mps":
                torch.mps.synchronize()
            elapsed += time.perf_counter() - tick
            scores.extend(torch.sigmoid(logits).cpu().tolist())
            labels.extend(row.label for row in batch)
    return {
        "auc": binary_auc(labels, scores),
        "milliseconds_per_example": 1000 * elapsed / len(rows),
        "examples": len(rows),
    }


def _forward(model, tokenizer, data, batch, config, device, torch, bahe):
    if not bahe:
        encoded = tokenizer(
            [data.prompt(row, config.history_items) for row in batch],
            padding=True, truncation=True, max_length=config.maximum_length,
            return_tensors="pt",
        ).to(device)
        return model(encoded)
    histories = torch.zeros((len(batch), config.history_items), dtype=torch.long, device=device)
    lengths = []
    for index, row in enumerate(batch):
        values = row.history[-config.history_items:]
        if values:
            histories[index, -len(values):] = torch.tensor(values, device=device)
        lengths.append(len(values))
    return model(
        histories, torch.tensor(lengths, device=device),
        torch.tensor([row.candidate for row in batch], device=device),
    )
