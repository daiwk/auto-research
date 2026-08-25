from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


ALGORITHMS = (
    "dpo",
    "kto",
    "orpo",
    "grpo",
    "reco-grpo",
    "dapo",
    "gspo",
    "ppo-rlhf",
    "rloo",
    "remax",
    "gkd",
    "minillm",
    "opsd",
    "dash",
    "distilled-rl",
    "u-opsd",
    "rp-opsd",
    "pcsd",
    "adrs",
    "mopd",
    "opd-lm",
    "beta-opsd",
    "opcd",
    "flux-opd",
    "lightning-opd",
    "gprl",
    "tcr",
    "ipo",
    "simpo",
    "luspo",
    "coba-rl",
    "constitutional-ai",
    "rrhf",
    "raft",
    "slic-hf",
    "steerlm",
    "spin",
    "seed",
    "relay-opd",
    "cast",
    "turn-opd",
    "cort",
    "ripo",
    "tis",
    "icepop",
    "online-icepop",
    "kpop",
    "gppo",
    "dr-grpo",
    "armor",
    "reinforce-plus",
    "taco",
    "chord",
    "vapo",
    "vad",
    "rlaif",
    "process-supervision",
    "math-shepherd",
    "self-rewarding",
    "luffy",
    "ttrl",
    "absolute-zero",
    "intuitor",
    "cispo",
    "spiral",
    "conspo",
    "minirl",
    "missing-old-logits",
    "stare",
    "rrc",
    "rail",
    "specroll",
    "pto",
    "c2-dpo",
    "gcpo",
    "r2-opd",
    "sr-opsd",
    "opd2",
    "causal-opd",
    "smopd",
    "rstg",
    "sa-mrpo",
    "rubric-dropout",
    "erils",
    "crpo",
    "serpo",
    "iso-rlvr",
    "srpo",
    "erpo",
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
    seeds: tuple[int, ...] = ()
    teacher_model_id: str | None = None
    teacher_revision: str = "7ae557604adf67be50417f59c2c2f167def9a775"
    teacher_checkpoint_path: Path | None = None
    teacher_cache: Path | None = None
    boundary_cache: Path | None = None
    boundary_samples: int = 8
    teacher_max_new_tokens: int = 96
    teacher_input_cost_per_million: float = 0.0
    teacher_output_cost_per_million: float = 0.0

    def __post_init__(self) -> None:
        if self.algorithm not in ALGORITHMS:
            raise ValueError(f"algorithm must be one of {', '.join(ALGORITHMS)}")
        if self.dataset not in {
            "arithmetic-smoke", "gsm8k-candidate",
            "arithmetic-generate", "gsm8k-generate",
        }:
            raise ValueError(
                "dataset must be arithmetic-smoke, gsm8k-candidate, "
                "arithmetic-generate or gsm8k-generate"
            )
        if self.algorithm in {"ipo", "simpo", "luspo", "coba-rl"} and not self.dataset.endswith("-generate"):
            raise ValueError(f"{self.algorithm} requires a free-generation dataset")
        if self.steps < 1 or self.maximum_examples < 8:
            raise ValueError("steps must be positive and maximum-examples must be >= 8")
        if self.learning_rate <= 0 or self.group_size < 2:
            raise ValueError("learning-rate must be positive and group-size must be >= 2")
        if self.seeds and len(set(self.seeds)) != len(self.seeds):
            raise ValueError("seeds must be unique")
        if self.teacher_model_id and self.algorithm != "coba-rl":
            raise ValueError("a real teacher is only supported by coba-rl")
        if self.teacher_model_id and not self.dataset.endswith("-generate"):
            raise ValueError("CoBA-RL teacher requires a free-generation dataset")
        if min(self.boundary_samples, self.teacher_max_new_tokens) < 1:
            raise ValueError("teacher and boundary sampling limits must be positive")
        if min(
            self.teacher_input_cost_per_million,
            self.teacher_output_cost_per_million,
        ) < 0:
            raise ValueError("teacher token costs cannot be negative")


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
