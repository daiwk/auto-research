from __future__ import annotations

import math
import random

import numpy as np

from auto_research.runtime import device_for


def seed_everything(seed: int, torch) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def sample_batch(tokens, batch_size: int, length: int, rng, device, torch):
    starts = rng.integers(0, len(tokens) - length - 1, size=batch_size)
    rows = np.stack([tokens[start : start + length + 1] for start in starts])
    values = torch.tensor(rows, dtype=torch.long, device=device)
    return values[:, :-1], values[:, 1:]


def train_language_model(model, tokens, *, steps: int, batch_size: int, length: int,
                         learning_rate: float, seed: int, torch) -> dict:
    seed_everything(seed, torch)
    device = device_for(torch)
    model.to(device).train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    rng = np.random.default_rng(seed)
    losses = []
    for _ in range(steps):
        inputs, labels = sample_batch(tokens, batch_size, length, rng, device, torch)
        optimizer.zero_grad(set_to_none=True)
        logits = model(inputs)
        loss = torch.nn.functional.cross_entropy(logits.reshape(-1, logits.shape[-1]), labels.reshape(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[: min(5, len(losses))])),
        "final_loss": float(np.mean(losses[-min(5, len(losses)) :])),
        "parameters": sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad),
        "device": device.type,
    }


def evaluate_language_model(model, tokens, *, length: int, batches: int, torch) -> dict:
    device = next(model.parameters()).device
    model.eval()
    losses = []
    with torch.inference_mode():
        for start in range(0, min(len(tokens) - length - 1, length * batches), length):
            values = torch.tensor(tokens[start : start + length + 1], dtype=torch.long, device=device)
            logits = model(values[:-1][None])
            loss = torch.nn.functional.cross_entropy(logits[0], values[1:])
            losses.append(float(loss.cpu()))
    loss = float(np.mean(losses))
    return {"loss": loss, "perplexity": math.exp(min(loss, 20.0)), "batches": len(losses)}


def require_torch():
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError("this LLM reproduction requires pip install -e '.[llm-evolution]'") from exc
    return torch
