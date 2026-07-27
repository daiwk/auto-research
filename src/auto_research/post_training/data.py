from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import numpy as np

from ..datasets import gsm8k


@dataclass(frozen=True)
class CandidateGroup:
    features: np.ndarray
    rewards: np.ndarray
    gold: int


@dataclass(frozen=True)
class PostTrainingData:
    train: tuple[CandidateGroup, ...]
    validation: tuple[CandidateGroup, ...]
    feature_names: tuple[str, ...]
    reward_names: tuple[str, ...]
    source: str


FEATURE_NAMES = (
    "bias", "signed_value", "magnitude", "integer", "concise",
    "has_equation", "step_count", "self_check",
)
REWARD_NAMES = ("outcome", "format", "reasoning", "brevity")


def load_post_training_data(
    dataset: str,
    root: Path,
    allow_network: bool,
    maximum_examples: int,
    seed: int,
) -> PostTrainingData:
    if dataset == "gsm8k-candidate":
        rows = gsm8k(root, allow_network)
        train = _gsm_groups(rows["train"][:maximum_examples], seed)
        validation = _gsm_groups(
            rows["test"][: max(32, maximum_examples // 4)], seed + 1
        )
        source = "OpenAI GSM8K official train/test JSONL"
    else:
        rng = np.random.default_rng(seed)
        train = tuple(_arithmetic_group(rng) for _ in range(maximum_examples))
        validation = tuple(
            _arithmetic_group(rng) for _ in range(max(64, maximum_examples // 4))
        )
        source = "deterministic arithmetic smoke suite"
    return PostTrainingData(train, validation, FEATURE_NAMES, REWARD_NAMES, source)


def _arithmetic_group(rng: np.random.Generator) -> CandidateGroup:
    a, b = int(rng.integers(2, 80)), int(rng.integers(2, 80))
    operation = int(rng.integers(0, 3))
    gold = (a + b, a - b, a * b)[operation]
    offsets = np.asarray((0, 1, -1, 2, -3, 5), dtype=float)
    rng.shuffle(offsets)
    candidates = gold + offsets
    gold_index = int(np.flatnonzero(offsets == 0)[0])
    process = np.clip(
        1.0 - np.abs(offsets) / 5.0 + rng.normal(0, 0.12, len(offsets)), 0, 1
    )
    self_check = np.clip(process + rng.normal(0, 0.08, len(offsets)), 0, 1)
    features = np.vstack(
        [
            _features(float(value), process[i], self_check[i], i % 3 + 1)
            for i, value in enumerate(candidates)
        ]
    )
    rewards = np.column_stack(
        (
            (offsets == 0).astype(float),
            np.ones(len(offsets)),
            process,
            1.0 / (1.0 + np.arange(len(offsets)) % 3),
        )
    )
    return CandidateGroup(features, rewards, gold_index)


def _gsm_groups(rows: list[dict[str, str]], seed: int) -> tuple[CandidateGroup, ...]:
    rng = np.random.default_rng(seed)
    result = []
    for row in rows:
        match = re.search(r"####\s*(-?[\d,]+(?:\.\d+)?)", row["answer"])
        if not match:
            continue
        gold = float(match.group(1).replace(",", ""))
        scale = max(1.0, abs(gold) * 0.06)
        offsets = np.asarray((0, -3, -1, 1, 2, 5), dtype=float) * scale
        rng.shuffle(offsets)
        values = gold + offsets
        gold_index = int(np.flatnonzero(offsets == 0)[0])
        # Candidate-ranking keeps generation cheap while retaining an exact,
        # verifiable GSM8K outcome reward. Process signals are noisy verifiers,
        # not the gold label itself.
        process = np.clip(
            1.0 - np.abs(offsets) / (5 * scale) + rng.normal(0, 0.18, 6), 0, 1
        )
        checks = np.clip(process + rng.normal(0, 0.12, 6), 0, 1)
        features = np.vstack(
            [_features(value, process[i], checks[i], i % 4 + 1) for i, value in enumerate(values)]
        )
        rewards = np.column_stack(
            (
                (offsets == 0).astype(float),
                np.asarray([float(value.is_integer()) for value in values]),
                process,
                1.0 / (1.0 + np.arange(6) % 4),
            )
        )
        result.append(CandidateGroup(features, rewards, gold_index))
    return tuple(result)


def _features(value: float, process: float, self_check: float, steps: int) -> np.ndarray:
    return np.asarray(
        [
            1.0,
            np.tanh(value / 100.0),
            np.tanh(abs(value) / 100.0),
            float(value.is_integer()),
            1.0 / steps,
            float(steps > 1),
            min(steps / 4.0, 1.0),
            self_check,
        ],
        dtype=np.float64,
    )
