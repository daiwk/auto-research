from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

import numpy as np

from .industrial_ranking import initialize, require_backend, summarize_training
from .rec_utils import ranking_metrics


@dataclass(frozen=True)
class SequenceModelConfig:
    dimensions: int = 64
    heads: int = 2
    layers: int = 2
    sequence_length: int = 32
    batch_size: int = 64
    steps: int = 240
    learning_rate: float = 3e-4
    dropout: float = 0.1


def padded_windows(sequences, length: int):
    rows = []
    for sequence in sequences:
        for end in range(2, len(sequence) + 1):
            window = sequence[max(0, end - length - 1) : end]
            inputs, targets = window[:-1], window[1:]
            padding = length - len(inputs)
            rows.append(
                (
                    (inputs[0],) * padding + inputs,
                    (targets[0],) * padding + targets,
                    (0.0,) * padding + (1.0,) * len(targets),
                )
            )
    return tuple(rows)


def train_sequence_model(
    model: Any,
    data,
    config: SequenceModelConfig,
    seed: int,
    loss_kind: str,
):
    model, device, torch = initialize(model, seed)
    rows = padded_windows(data.train, config.sequence_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses: list[float] = []
    model.train()
    for _ in range(config.steps):
        selected = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        inputs = torch.tensor([row[0] for row in selected], device=device)
        targets = torch.tensor([row[1] for row in selected], device=device)
        valid = torch.tensor([row[2] for row in selected], device=device)
        logits = model(inputs)
        if loss_kind == "sampled_softmax":
            token_loss = torch.nn.functional.cross_entropy(
                logits.reshape(-1, data.item_count),
                targets.reshape(-1),
                reduction="none",
            ).reshape_as(valid)
        elif loss_kind == "bce":
            positive = logits.gather(-1, targets.unsqueeze(-1)).squeeze(-1)
            negatives = torch.randint(
                0, data.item_count, targets.shape, device=device
            )
            negative = logits.gather(-1, negatives.unsqueeze(-1)).squeeze(-1)
            token_loss = -torch.nn.functional.logsigmoid(positive)
            token_loss -= torch.nn.functional.logsigmoid(-negative)
        else:
            raise ValueError(f"unknown sequence loss: {loss_kind}")
        loss = (token_loss * valid).sum() / valid.sum()
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def evaluate_sequence_model(model, data, config: SequenceModelConfig, target="test"):
    torch, _ = require_backend()
    device = next(model.parameters()).device

    def scorer(history):
        recent = history[-config.sequence_length :]
        padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
        with torch.inference_mode():
            logits = model(torch.tensor([padded], device=device))
        return logits[0, -1].detach().cpu().numpy()

    model.eval()
    return ranking_metrics(data, scorer, target=target)
