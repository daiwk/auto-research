from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class OrchestraDecision:
    action: str
    operation: str | None
    confidence: float


ACTIONS = ("drop", "untouched", "clean")
OPERATIONS = ("normalize", "deduplicate", "wiki", "repair")


def text_features(block: str) -> np.ndarray:
    characters = max(len(block), 1)
    words = re.findall(r"\b\w+\b", block)
    lines = [line for line in block.splitlines() if line.strip()]
    unique = len(set(words)) / max(len(words), 1)
    alpha = sum(character.isalpha() for character in block) / characters
    repeated = 1 - len(set(lines)) / max(len(lines), 1)
    markup = sum(block.count(mark) for mark in ("=", "[", "]", "{", "}", "  "))
    punctuation = sum(block.count(mark) for mark in ".!?") / characters
    return np.asarray(
        [
            min(characters / 1200, 1),
            min(len(words) / 200, 1),
            unique,
            alpha,
            repeated,
            min(markup / 20, 1),
            min(punctuation * 30, 1),
            float(block.strip().startswith("=")),
        ],
        dtype=np.float32,
    )

def programmatic_teacher(block: str) -> tuple[int, int]:
    features = text_features(block)
    if features[0] < 0.04 or features[3] < 0.45:
        return 0, 0
    noisy = features[4] > 0.2 or features[5] > 0.25
    if not noisy and features[2] > 0.55 and features[3] > 0.72:
        return 1, 0
    if features[4] > 0.2:
        operation = 1
    elif features[7] or features[5] > 0.35:
        operation = 2
    elif features[6] < 0.12:
        operation = 3
    else:
        operation = 0
    return 2, operation


def build_orchestrator(feature_width: int):
    import torch
    from torch import nn

    class Orchestrator(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(feature_width, 32),
                nn.GELU(),
                nn.Linear(32, 24),
                nn.GELU(),
            )
            self.action = nn.Linear(24, len(ACTIONS))
            self.operation = nn.Linear(24, len(OPERATIONS))

        def forward(self, values):
            hidden = self.encoder(values)
            return self.action(hidden), self.operation(hidden)

    return Orchestrator()


def apply_operation(block: str, operation: str) -> str:
    if operation == "normalize":
        return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", block)).strip()
    if operation == "deduplicate":
        seen, lines = set(), []
        for line in block.splitlines():
            normalized = re.sub(r"\s+", " ", line).strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                lines.append(normalized)
        return "\n".join(lines)
    if operation == "wiki":
        value = re.sub(r"^\s*=+\s*(.*?)\s*=+\s*$", r"\1.", block, flags=re.MULTILINE)
        value = re.sub(r"\[\[([^]|]+\|)?([^]]+)\]\]", r"\2", value)
        return re.sub(r"\s+", " ", value).strip()
    if operation == "repair":
        value = re.sub(r"\s+", " ", block).strip()
        return value if not value or value[-1] in ".!?" else value + "."
    raise ValueError(f"unknown cleaning operation: {operation}")


def decide(model, block: str, torch) -> OrchestraDecision:
    device = next(model.parameters()).device
    values = torch.tensor(text_features(block)[None], device=device)
    model.eval()
    with torch.inference_mode():
        action_logits, operation_logits = model(values)
        probabilities = torch.softmax(action_logits, -1)[0]
        action_index = int(probabilities.argmax())
        operation_index = int(operation_logits[0].argmax())
    return OrchestraDecision(
        action=ACTIONS[action_index],
        operation=OPERATIONS[operation_index] if action_index == 2 else None,
        confidence=float(probabilities[action_index].cpu()),
    )
