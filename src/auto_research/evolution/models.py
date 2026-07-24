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
    maximum_train_tokens: int | None = None
    maximum_eval_tokens: int | None = 100_000
    vocab_size: int = 4096
    llm_dimensions: int = 384
    llm_layers: int = 6
    llm_batch_size: int = 4
    llm_sequence_length: int = 128
    benchmark_suite: str = "public"
    fitness_metric: str = "primary"
    device: str = "auto"
    cpu_threads: int | None = None

    def validate(self) -> None:
        if self.model not in {"rankmixer", "hyformer", "micro-llm"}:
            raise ValueError("model must be rankmixer, hyformer or micro-llm")
        expected = {"wikitext-2"} if self.model == "micro-llm" else {"movielens-100k", "movielens-1m"}
        if self.dataset not in expected:
            raise ValueError(f"dataset {self.dataset!r} is incompatible with model {self.model!r}")
        if min(self.generations, self.population, self.steps, self.workers) < 1:
            raise ValueError("generations, population and steps must be positive")
        if not self.seeds:
            raise ValueError("at least one seed is required")
        if self.cpu_threads is not None and self.cpu_threads < 1:
            raise ValueError("cpu threads must be positive")
        if self.benchmark_suite not in {"core", "public", "unirank"}:
            raise ValueError("benchmark suite must be core, public or unirank")
        if self.model == "micro-llm" and self.benchmark_suite == "unirank":
            raise ValueError("the UniRank suite is only available to recommendation models")
        allowed_fitness = {"primary", "public_composite", "unirank_composite"}
        if self.fitness_metric not in allowed_fitness:
            raise ValueError(
                f"fitness metric must be one of {sorted(allowed_fitness)}"
            )
        if self.fitness_metric == "public_composite" and self.benchmark_suite != "public":
            raise ValueError("public_composite fitness requires the public benchmark suite")
        if self.fitness_metric == "unirank_composite" and self.benchmark_suite != "unirank":
            raise ValueError("unirank_composite fitness requires the unirank benchmark suite")
        if self.model == "micro-llm":
            if min(self.vocab_size, self.llm_dimensions, self.llm_layers,
                   self.llm_batch_size, self.llm_sequence_length) < 1:
                raise ValueError("micro-llm size parameters must be positive")
            if self.llm_dimensions % 4:
                raise ValueError("micro-llm dimensions must be divisible by 4 attention heads")


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
    heads: int = 4
    kv_heads: int = 4
    sequence_length: int = 128
    expansion: int = 4
    data_recipe: str = "wikitext"
    data_mix_ratio: float = 0.2
    post_training: str = "none"
    neftune_alpha: float = 0.0
    post_steps: int = 0

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
        return self.validation.get("fitness", self.validation.get("ndcg_at_10", -1.0))

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
