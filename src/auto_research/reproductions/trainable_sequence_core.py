from __future__ import annotations

from dataclasses import dataclass
import random

import numpy as np

from .industrial_ranking import require_backend
from .rec_utils import batched_ranking_metrics
from ..runtime import device_for


@dataclass(frozen=True)
class SequenceTrainConfig:
    history_length: int = 32
    dimensions: int = 32
    batch_size: int = 48
    steps: int = 90
    learning_rate: float = 8e-4
    evaluation_batch_size: int = 32


def _context_rows(data, history_length: int):
    rows = []
    for sequence in data.train:
        for end in range(2, len(sequence)):
            rows.append((sequence[max(0, end - history_length):end], sequence[end]))
    return rows


def _pad(histories, length: int, pad: int):
    values, masks = [], []
    for history in histories:
        recent = tuple(history[-length:])
        missing = length - len(recent)
        values.append((pad,) * missing + recent)
        masks.append((False,) * missing + (True,) * len(recent))
    return values, masks


def train_pairwise(model, data, config: SequenceTrainConfig, seed: int):
    torch, _ = require_backend()
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    device = device_for(torch)
    model.to(device)
    rows = _context_rows(data, config.history_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=1e-4)
    losses = []
    model.train()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories, positives = zip(*batch)
        negatives = []
        for positive in positives:
            negative = rng.randrange(data.item_count)
            if negative == positive:
                negative = (negative + 1) % data.item_count
            negatives.append(negative)
        padded, masks = _pad(histories, config.history_length, data.item_count)
        history = torch.tensor(padded, dtype=torch.long, device=device)
        mask = torch.tensor(masks, dtype=torch.bool, device=device)
        positive = torch.tensor(positives, dtype=torch.long, device=device)
        negative = torch.tensor(negatives, dtype=torch.long, device=device)
        pos_score = model(history, mask, positive)
        neg_score = model(history, mask, negative)
        loss = torch.nn.functional.softplus(-(pos_score - neg_score)).mean()
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {
        "initial_loss": losses[0],
        "final_loss": losses[-1],
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
        "steps": config.steps,
    }


def evaluate_pairwise(model, data, config: SequenceTrainConfig, target: str = "test"):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    candidates = torch.arange(data.item_count, dtype=torch.long, device=device)

    def scorer(histories):
        padded, masks = _pad(histories, config.history_length, data.item_count)
        history = torch.tensor(padded, dtype=torch.long, device=device)
        mask = torch.tensor(masks, dtype=torch.bool, device=device)
        with torch.inference_mode():
            rows = []
            for start in range(0, data.item_count, 256):
                block = candidates[start:start + 256]
                rows.append(model.score_catalog(history, mask, block))
            return torch.cat(rows, dim=1).cpu().numpy()

    model.eval()
    return batched_ranking_metrics(
        data, scorer, config.evaluation_batch_size, target=target
    )
