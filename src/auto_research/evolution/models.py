from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EvolutionConfig:
    model: str
    dataset: str
    direction: str = ""
    dataset_dir: Path = Path("data")
    output_dir: Path = Path("runs/evolution")
    query: str | None = None
    generations: int = 3
    population: int = 4
    max_papers: int = 8
    steps: int = 100
    seeds: tuple[int, ...] = (42,)
    allow_network: bool = True
    workers: int = 1
    maximum_users: int | None = None
    maximum_items: int | None = None
    evaluation_users: int | None = 1000

    def validate(self) -> None:
        if self.model not in {"rankmixer", "hyformer"}:
            raise ValueError("model must be rankmixer or hyformer")
        if self.dataset not in {"movielens-100k", "movielens-1m"}:
            raise ValueError("dataset must be movielens-100k or movielens-1m")
        if min(self.generations, self.population, self.steps, self.workers) < 1:
            raise ValueError("generations, population and steps must be positive")
        if not self.seeds:
            raise ValueError("at least one seed is required")


@dataclass(frozen=True)
class PaperInspiration:
    arxiv_id: str
    title: str
    url: str
    published: str
    architecture: str | None
    method: str
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Genome:
    architecture: str = "rankmixer_dense"
    dimensions: int = 64
    layers: int = 2
    learning_rate: float = 3e-4
    optimizer: str = "adamw"
    batch_size: int = 48
    experts: int = 4
    interval_residual: int = 2
    auxiliary_weight: float = 0.15

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvolutionTrial:
    trial_id: str
    generation: int
    parent_id: str | None
    genome: Genome
    validation: dict[str, float]
    training: dict[str, Any]
    source_papers: tuple[str, ...]
    rationale: str
    duration_seconds: float
    status: str = "completed"
    error: str | None = None

    @property
    def fitness(self) -> float:
        return self.validation["ndcg_at_10"]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["fitness"] = self.fitness
        return payload


@dataclass
class EvolutionResult:
    run_id: str
    config: EvolutionConfig
    papers: list[PaperInspiration] = field(default_factory=list)
    trials: list[EvolutionTrial] = field(default_factory=list)
    champion_id: str | None = None
    baseline_test: dict[str, float] | None = None
    champion_test: dict[str, float] | None = None
    rounds: list[dict[str, Any]] = field(default_factory=list)
    dataset_summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "config": {**asdict(self.config), "dataset_dir": str(self.config.dataset_dir), "output_dir": str(self.config.output_dir), "seeds": list(self.config.seeds)},
            "papers": [paper.to_dict() for paper in self.papers],
            "trials": [trial.to_dict() for trial in self.trials],
            "champion_id": self.champion_id,
            "baseline_test": self.baseline_test,
            "champion_test": self.champion_test,
            "rounds": self.rounds,
            "dataset_summary": self.dataset_summary,
        }
