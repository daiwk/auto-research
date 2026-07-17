from __future__ import annotations

from auto_research.runtime import device_for

import random
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np


@dataclass(frozen=True)
class NeuralRankingConfig:
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
            "This reproduction trains neural ranking models; install with "
            "`pip install -e '.[neural-recs]'`."
        ) from exc
    return torch, nn


def training_examples(sequences, length: int):
    rows = []
    for sequence in sequences:
        for position in range(1, len(sequence)):
            history = sequence[max(0, position - length) : position]
            padded = (history[0],) * (length - len(history)) + history
            rows.append((padded, sequence[position]))
    return tuple(rows)


def initialize(model, seed: int):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = device_for(torch)
    return model.to(device), device, torch


def train_supervised(
    model: Any,
    data,
    config: NeuralRankingConfig,
    seed: int,
    rows=None,
    steps: int | None = None,
    output: Callable[[Any], Any] | None = None,
):
    model, device, torch = initialize(model, seed)
    rows = rows or training_examples(data.train, config.sequence_length)
    rng = random.Random(seed)
    optimizers = {
        "adamw": torch.optim.AdamW,
        "adam": torch.optim.Adam,
        "adagrad": torch.optim.Adagrad,
    }
    optimizer_name = getattr(config, "optimizer", "adamw")
    optimizer = optimizers[optimizer_name](model.parameters(), lr=config.learning_rate)
    losses: list[float] = []
    model.train()
    for _ in range(config.steps if steps is None else steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = torch.tensor(
            [row[0] for row in batch], dtype=torch.long, device=device
        )
        targets = torch.tensor(
            [row[1] for row in batch], dtype=torch.long, device=device
        )
        optimizer.zero_grad(set_to_none=True)
        values = model(histories)
        logits = output(values) if output else values
        loss = torch.nn.functional.cross_entropy(logits, targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def summarize_training(model, losses, device: str):
    return {
        "initial_loss": float(np.mean(losses[: min(20, len(losses))])),
        "final_loss": float(np.mean(losses[-min(20, len(losses)) :])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device,
    }


def evaluate_model(
    model: Any, data, config: NeuralRankingConfig, output=None, target: str = "test"
):
    torch, _ = require_backend()
    device = next(model.parameters()).device

    def scorer(history):
        recent = history[-config.sequence_length :]
        padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
        with torch.inference_mode():
            values = model(
                torch.tensor([padded], dtype=torch.long, device=device)
            )
            logits = output(values) if output else values
        return logits[0].detach().cpu().numpy()

    from .rec_utils import ranking_metrics

    model.eval()
    return ranking_metrics(data, scorer, target=target)
