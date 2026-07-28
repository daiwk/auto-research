from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ALGORITHMS = (
    "dpo",
    "kto",
    "orpo",
    "grpo",
    "dapo",
    "gspo",
    "ppo-rlhf",
    "rloo",
    "remax",
    "lightning-opd",
    "gprl",
    "tcr",
)


@dataclass(frozen=True)
class PostTrainingConfig:
    algorithm: str
    dataset: str = "arithmetic-smoke"
    dataset_dir: Path = Path("data")
    output_dir: Path = Path("runs/post-training")
    steps: int = 100
    learning_rate: float = 0.08
    group_size: int = 4
    seed: int = 42
    allow_network: bool = True
    maximum_examples: int = 512

    def __post_init__(self) -> None:
        if self.algorithm not in ALGORITHMS:
            raise ValueError(f"algorithm must be one of {', '.join(ALGORITHMS)}")
        if self.dataset not in {"arithmetic-smoke", "gsm8k-candidate"}:
            raise ValueError("dataset must be arithmetic-smoke or gsm8k-candidate")
        if self.steps < 1 or self.maximum_examples < 8:
            raise ValueError("steps must be positive and maximum-examples must be >= 8")
        if self.learning_rate <= 0 or self.group_size < 2:
            raise ValueError("learning-rate must be positive and group-size must be >= 2")


@dataclass
class PostTrainingResult:
    algorithm: str
    dataset: str
    baseline: dict[str, float]
    final: dict[str, float]
    training: dict[str, Any]
    history: list[dict[str, float]] = field(default_factory=list)

    @property
    def relative_accuracy(self) -> float:
        initial = self.baseline["accuracy"]
        return (self.final["accuracy"] - initial) / max(initial, 1e-12)
