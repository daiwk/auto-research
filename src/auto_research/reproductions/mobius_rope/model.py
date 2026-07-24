from __future__ import annotations

import numpy as np

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.runtime import device_for


def build_variant(name: str, vocab_size: int):
    architecture = {"Standard RoPE": "llama_modern", "Hybrid Möbius RoPE": "mobius_rope"}[name]
    config = MicroLMConfig(
        vocab_size=vocab_size,
        dimensions=96,
        layers=3,
        heads=4,
        sequence_length=64,
        expansion=3,
    )
    return build_micro_lm(architecture, config), config


def retrieval_examples(vocab_size: int, length: int, count: int, seed: int):
    """Generate causal key/value retrieval rows with depth-controlled needles."""
    rng = np.random.default_rng(seed)
    rows, targets, depths = [], [], []
    reserved = min(64, max(16, vocab_size // 8))
    for index in range(count):
        key = 4 + index % (reserved // 2)
        value = 4 + reserved // 2 + index % (reserved // 2)
        row = rng.integers(reserved + 4, vocab_size, size=length, dtype=np.int64)
        position = 2 + index % max(1, length - 10)
        row[position:position + 4] = (1, key, value, 2)
        row[-4:] = (3, key, 2, value)
        rows.append(row)
        targets.append(value)
        depths.append((length - position) / length)
    return np.stack(rows), np.asarray(targets), np.asarray(depths)


def train_mixed(model, train_tokens, config, seed: int, torch, steps: int = 90):
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    device = device_for(torch)
    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=7e-4)
    retrieval, retrieval_targets, _ = retrieval_examples(
        config.vocab_size, config.sequence_length + 1, 512, seed + 9
    )
    losses = []
    model.train()
    for step in range(steps):
        offsets = rng.integers(
            0, len(train_tokens) - config.sequence_length - 1, size=8
        )
        selected = np.stack([
            train_tokens[offset:offset + config.sequence_length + 1]
            for offset in offsets
        ])
        batch = torch.tensor(selected, dtype=torch.long, device=device)
        logits = model(batch[:, :-1])
        language_loss = torch.nn.functional.cross_entropy(
            logits.reshape(-1, config.vocab_size), batch[:, 1:].reshape(-1)
        )
        retrieval_indices = rng.choice(len(retrieval), 16, replace=False)
        retrieval_batch = torch.tensor(
            retrieval[retrieval_indices, :-1], dtype=torch.long, device=device
        )
        retrieval_labels = torch.tensor(
            retrieval_targets[retrieval_indices], dtype=torch.long, device=device
        )
        retrieval_loss = torch.nn.functional.cross_entropy(
            model(retrieval_batch)[:, -1], retrieval_labels
        )
        loss = language_loss + 0.5 * retrieval_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "steps": steps,
        "initial_loss": float(np.mean(losses[:10])),
        "final_loss": float(np.mean(losses[-10:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def evaluate_retrieval(model, config, seed: int, torch):
    rows, targets, depths = retrieval_examples(
        config.vocab_size, config.sequence_length, 192, seed + 101
    )
    device = next(model.parameters()).device
    predictions = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(rows), 32):
            batch = torch.tensor(rows[start:start + 32, :-1], dtype=torch.long, device=device)
            predictions.extend(model(batch)[:, -1].argmax(-1).cpu().tolist())
    correct = np.asarray(predictions) == targets
    far = depths >= np.median(depths)
    return {
        "needle_accuracy": float(correct.mean()),
        "far_needle_accuracy": float(correct[far].mean()),
        "near_needle_accuracy": float(correct[~far].mean()),
        "examples": len(rows),
    }
