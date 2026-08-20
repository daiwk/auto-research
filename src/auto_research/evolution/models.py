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
    maximum_examples: int = 512
    agent_episodes: int = 120
    vocab_size: int = 4096
    llm_dimensions: int = 384
    llm_layers: int = 6
    llm_batch_size: int = 4
    llm_sequence_length: int = 128
    benchmark_suite: str = "public"
    fitness_metric: str = "primary"
    device: str = "auto"
    cpu_threads: int | None = None
    resume_dir: Path | None = None
    evaluation_tier: str = "l2_public_dataset"
    promotion_min_seeds: int = 1
    confidence_z: float = 1.0
    retries: int = 1
    gpu_slots: int = 1
    trial_timeout_seconds: int = 3600
    gpu_memory_per_trial_mb: int | None = None
    candidate_generator_command: tuple[str, ...] = ()
    candidate_timeout_seconds: int = 300
    checkpoint_model_id: str = "HuggingFaceTB/SmolVLM2-256M-Video-Instruct"
    checkpoint_path: Path | None = None
    checkpoint_revision: str = "main"
    checkpoint_annotations: Path | None = None
    checkpoint_image_root: Path | None = None
    reasoning_model_id: str = "HuggingFaceTB/SmolLM2-135M-Instruct"
    reasoning_model_revision: str = "12fd25f77366fa6b3b4b768ec3050bf629380bac"
    reasoning_checkpoint_path: Path | None = None

    def validate(self) -> None:
        from .providers import get_provider
        provider = get_provider(self.model)
        if self.dataset not in provider.datasets:
            raise ValueError(f"dataset {self.dataset!r} is incompatible with model {self.model!r}")
        if min(self.generations, self.population, self.steps, self.workers) < 1:
            raise ValueError("generations, population and steps must be positive")
        if not self.seeds:
            raise ValueError("at least one seed is required")
        if self.cpu_threads is not None and self.cpu_threads < 1:
            raise ValueError("cpu threads must be positive")
        if min(
            self.promotion_min_seeds, self.gpu_slots, self.trial_timeout_seconds,
            self.candidate_timeout_seconds,
        ) < 1 or self.retries < 0:
            raise ValueError("promotion_min_seeds/gpu_slots must be positive and retries non-negative")
        if self.gpu_memory_per_trial_mb is not None and self.gpu_memory_per_trial_mb < 1:
            raise ValueError("gpu_memory_per_trial_mb must be positive")
        if min(self.maximum_examples, self.agent_episodes) < 1:
            raise ValueError("maximum examples and agent episodes must be positive")
        if self.benchmark_suite not in {"core", "public", "unirank"}:
            raise ValueError("benchmark suite must be core, public or unirank")
        if self.model in {"micro-llm", "micro-vlm", "vlm-checkpoint"} and self.benchmark_suite == "unirank":
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
        if self.model in {"micro-llm", "micro-vlm"}:
            if min(self.vocab_size, self.llm_dimensions, self.llm_layers,
                   self.llm_batch_size, self.llm_sequence_length) < 1:
                raise ValueError("micro model size parameters must be positive")
            if self.llm_dimensions % 4:
                raise ValueError("micro model dimensions must be divisible by 4 attention heads")
        if self.model == "vlm-checkpoint":
            if self.checkpoint_annotations is None or self.checkpoint_image_root is None:
                raise ValueError(
                    "vlm-checkpoint requires --checkpoint-annotations and "
                    "--checkpoint-image-root"
                )
        if self.model == "reasoning-checkpoint" and self.maximum_examples < 1:
            raise ValueError("reasoning checkpoint requires at least one example")


@dataclass(frozen=True)
class PaperInspiration:
    arxiv_id: str
    title: str
    url: str
    published: str
    architecture: str | None
    method: str
    source: str
    candidate_origin: str = "retrieved-paper"
    executable: bool = False

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
    group_size: int = 4
    agent_memory: str = "none"
    agent_planner: str = "long-context"
    agent_tool_policy: str = "direct"
    agent_critic: str = "none"
    memory_size: int = 24
    multimodal_objective: str = "cross_entropy"
    checkpoint_prompt_style: str = "direct"
    checkpoint_use_hint: bool = True
    checkpoint_image_size: int = 0
    checkpoint_max_new_tokens: int = 16
    reasoning_samples: int = 1
    reasoning_max_new_tokens: int = 96
    reasoning_stop_consensus: float = 1.0
    reasoning_verifier: str = "self-consistency"

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
    verification_records: list[dict[str, Any]] = field(default_factory=list)
    research_memory: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "schema_version": 2,
            "config": {
                **asdict(self.config),
                "dataset_dir": str(self.config.dataset_dir),
                "output_dir": str(self.config.output_dir),
                "resume_dir": str(self.config.resume_dir) if self.config.resume_dir else None,
                "checkpoint_path": str(self.config.checkpoint_path) if self.config.checkpoint_path else None,
                "checkpoint_annotations": str(self.config.checkpoint_annotations) if self.config.checkpoint_annotations else None,
                "checkpoint_image_root": str(self.config.checkpoint_image_root) if self.config.checkpoint_image_root else None,
                "reasoning_checkpoint_path": str(self.config.reasoning_checkpoint_path) if self.config.reasoning_checkpoint_path else None,
                "seeds": list(self.config.seeds),
            },
            "papers": [paper.to_dict() for paper in self.papers],
            "trials": [trial.to_dict() for trial in self.trials],
            "champion_id": self.champion_id,
            "baseline_test": self.baseline_test,
            "champion_test": self.champion_test,
            "rounds": self.rounds,
            "dataset_summary": self.dataset_summary,
            "verification_records": self.verification_records,
            "research_memory": self.research_memory,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any], config: EvolutionConfig | None = None) -> "EvolutionResult":
        raw_config = dict(payload["config"])
        raw_config["dataset_dir"] = Path(raw_config["dataset_dir"])
        raw_config["output_dir"] = Path(raw_config["output_dir"])
        raw_config["resume_dir"] = Path(raw_config["resume_dir"]) if raw_config.get("resume_dir") else None
        for key in (
            "checkpoint_path", "checkpoint_annotations", "checkpoint_image_root",
            "reasoning_checkpoint_path",
        ):
            raw_config[key] = Path(raw_config[key]) if raw_config.get(key) else None
        raw_config["seeds"] = tuple(raw_config["seeds"])
        raw_config["candidate_generator_command"] = tuple(
            raw_config.get("candidate_generator_command", ())
        )
        loaded_config = config or EvolutionConfig(**raw_config)
        result = cls(
            payload["run_id"], loaded_config,
            papers=[PaperInspiration(**item) for item in payload.get("papers", [])],
            trials=[EvolutionTrial(
                item["trial_id"], item["generation"], item.get("parent_id"),
                Genome(**item["genome"]), item["validation"], item["training"],
                tuple(item.get("source_papers", ())), item["rationale"],
                item["duration_seconds"], item.get("status", "completed"), item.get("error"),
            ) for item in payload.get("trials", [])],
            champion_id=payload.get("champion_id"),
            baseline_test=payload.get("baseline_test"),
            champion_test=payload.get("champion_test"),
            rounds=payload.get("rounds", []),
            dataset_summary=payload.get("dataset_summary", {}),
            verification_records=payload.get("verification_records", []),
            research_memory=payload.get("research_memory", {}),
        )
        return result
