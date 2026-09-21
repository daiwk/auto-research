"""Executable System One evolution over a public Banking77 protocol."""

from __future__ import annotations

from dataclasses import replace
import gc
import random
import time
from pathlib import Path

import numpy as np

from ..system_one.benchmark import evaluate_examples, load_banking77
from ..system_one.local import LocalDecisionModel, LocalSystemOneProvider
from ..system_one.public_suite import (
    evaluate_public_decisions,
    load_public_decisions,
    split_public_decisions,
)
from .models import EvolutionTrial, Genome


LOCAL_OPERATORS = (
    "system-one:bilinear-ce",
    "system-one:rival-ce",
    "system-one:rival-brier",
    "system-one:rival-hybrid",
)


class SystemOneEvolutionEvaluator:
    def __init__(self, config, project_dir: Path) -> None:
        self.config = config
        self._provider_cache = {}
        if config.dataset == "banking77":
            self.train, self.validation, self.test_rows = load_banking77(
                (project_dir / config.dataset_dir / "system-one").resolve(),
                allow_network=config.allow_network,
                maximum_train_examples=config.maximum_examples * 4,
                maximum_eval_examples=config.maximum_examples,
            )
            self.executable_operators = LOCAL_OPERATORS
        elif config.dataset == "system-one-public":
            rows = load_public_decisions(config.system_one_public_data)
            self.validation, self.test_rows = split_public_decisions(rows)
            self.train = ()
            operators = []
            for name, path in (
                ("nanojev", config.system_one_nanojev_checkpoint),
                ("nimble", config.system_one_nimble_checkpoint),
                ("laya", config.system_one_laya_checkpoint),
            ):
                if path is not None:
                    operators.append(f"system-one:{name}")
            self.executable_operators = tuple(operators)
        else:
            raise ValueError("system-one evolve supports banking77 or system-one-public")
        self.steps = config.steps
        self.seeds = config.seeds

    def summary(self) -> dict:
        return {
            "source": "PolyAI Banking77" if self.config.dataset == "banking77" else "human-labeled public decision JSONL",
            "license": "CC BY 4.0" if self.config.dataset == "banking77" else "per-source licenses",
            "evaluation_tier": "l2_public_dataset",
            "promotion_eligible": True,
            "train_examples": len(self.train),
            "validation_examples": len(self.validation),
            "test_examples": len(self.test_rows),
            "genome_axes": [
                "dynamic candidate scorer", "proper scoring objective",
                "checkpoint backend", "temperature", "selective threshold",
            ],
            "seeds": list(self.seeds),
        }

    def propose(
        self,
        parent: Genome,
        generation: int,
        index: int,
        architectures: list[str],
        rng: random.Random,
        model: str,
    ) -> tuple[Genome, str]:
        del model
        architecture = (
            architectures[index % len(architectures)]
            if generation == 1
            else rng.choice(architectures)
        )
        dimensions = parent.dimensions
        learning_rate = parent.learning_rate
        if generation > 1:
            dimensions = rng.choice((64, 128, 256, 384))
            learning_rate = rng.choice((0.03, 0.08, 0.15, 0.25))
        temperature = parent.system_one_temperature
        threshold = parent.system_one_confidence_threshold
        if self.config.dataset == "system-one-public":
            dimensions, learning_rate = parent.dimensions, parent.learning_rate
            temperature = rng.choice((0.7, 1.0, 1.3))
            threshold = rng.choice((0.6, 0.7, 0.8, 0.9))
        return replace(
            parent,
            architecture=architecture,
            dimensions=dimensions,
            learning_rate=learning_rate,
            system_one_temperature=temperature,
            system_one_confidence_threshold=threshold,
        ), (
            f"System One 控制变量：{architecture}；dimensions={dimensions}；"
            f"learning_rate={learning_rate}；temperature={temperature}；"
            f"confidence_threshold={threshold}"
        )

    def evaluate(
        self,
        trial_id,
        generation,
        parent_id,
        genome,
        source_papers,
        rationale,
    ) -> EvolutionTrial:
        started = time.monotonic()
        if self.config.dataset == "system-one-public":
            provider = self._external_provider(genome)
            metrics = evaluate_public_decisions(
                provider, self.validation, genome.system_one_confidence_threshold
            )
            metrics["fitness"] = _fitness(metrics)
            return EvolutionTrial(
                trial_id, generation, parent_id, genome, metrics,
                {
                    "external_checkpoint": True,
                    "dataset": "system-one-public",
                    "test_read_during_selection": False,
                },
                source_papers, rationale, time.monotonic() - started,
            )
        rows, training_rows = [], []
        for seed in self.seeds:
            model, training = self._fit(genome, seed)
            metrics = evaluate_examples(
                LocalSystemOneProvider(model), self.validation, 0.8
            )
            metrics["fitness"] = _fitness(metrics)
            rows.append(metrics)
            training_rows.append(training)
        validation = _mean(rows)
        validation["fitness"] = _fitness(validation)
        validation["fitness_std"] = validation.get("fitness_std", 0.0)
        return EvolutionTrial(
            trial_id,
            generation,
            parent_id,
            genome,
            validation,
            {
                "initial_loss": float(np.mean([row["initial_loss"] for row in training_rows])),
                "final_loss": float(np.mean([row["final_loss"] for row in training_rows])),
                "fitness_by_seed": [float(row["fitness"]) for row in rows],
                "seeds": list(self.seeds),
                "dataset": "Banking77",
                "test_read_during_selection": False,
            },
            source_papers,
            rationale,
            time.monotonic() - started,
        )

    def test(self, genome: Genome) -> dict[str, float]:
        if self.config.dataset == "system-one-public":
            result = evaluate_public_decisions(
                self._external_provider(genome), self.test_rows,
                genome.system_one_confidence_threshold,
            )
            result["fitness"] = _fitness(result)
            return result
        rows = []
        for seed in self.seeds:
            model, _ = self._fit(genome, seed)
            rows.append(evaluate_examples(LocalSystemOneProvider(model), self.test_rows, 0.8))
        result = _mean(rows)
        result["fitness"] = _fitness(result)
        return result

    def _fit(self, genome: Genome, seed: int):
        architecture, objective = _operator_parts(genome.architecture)
        model = LocalDecisionModel(
            genome.dimensions,
            architecture=architecture,
            objective=objective,
            seed=seed,
        )
        training = model.fit(
            self.train,
            steps=self.steps,
            learning_rate=genome.learning_rate,
            seed=seed,
        )
        model.calibrate_temperature(self.validation)
        return model, training

    def _external_provider(self, genome: Genome):
        key = (genome.architecture, genome.system_one_temperature)
        if key not in self._provider_cache:
            # Keep only one checkpoint resident: Nimble plus another 7B/9B
            # backend can exceed a single A30 even though every operator fits
            # independently. Reloading is slower, but makes the advertised
            # multi-backend search executable on both supported accelerators.
            self._provider_cache.clear()
            gc.collect()
            try:
                import torch
            except ImportError:  # pragma: no cover - optional GPU dependency
                pass
            else:
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            self._provider_cache[key] = self._load_external_provider(
                genome.architecture, genome.system_one_temperature
            )
        return self._provider_cache[key]

    def _load_external_provider(self, operator: str, temperature: float):
        from ..system_one import LayaProvider, NanoJevProvider, NimbleProvider

        device = self.config.device if str(self.config.device).startswith("cuda") else "cuda:0"
        common = {"allow_download": self.config.allow_network, "device": device}
        if operator == "system-one:nanojev":
            return NanoJevProvider.from_checkpoint(
                self.config.system_one_nanojev_checkpoint,
                temperature=temperature, **common,
            )
        if operator == "system-one:nimble":
            return NimbleProvider.from_checkpoint(
                self.config.system_one_nimble_checkpoint,
                base_model_dir=self.config.system_one_nimble_base,
                temperature=temperature, **common,
            )
        if operator == "system-one:laya":
            return LayaProvider.from_checkpoint(
                self.config.system_one_laya_checkpoint,
                temperature_scale=temperature, **common,
            )
        raise ValueError(f"unknown executable System One checkpoint operator: {operator}")


def _operator_parts(operator: str) -> tuple[str, str]:
    mapping = {
        "system-one:bilinear-ce": ("bilinear", "cross_entropy"),
        "system-one:rival-ce": ("rival_attention", "cross_entropy"),
        "system-one:rival-brier": ("rival_attention", "brier"),
        "system-one:rival-hybrid": ("rival_attention", "hybrid"),
    }
    try:
        return mapping[operator]
    except KeyError as exc:
        raise ValueError(f"unknown System One operator: {operator}") from exc


def _fitness(metrics: dict[str, float]) -> float:
    return float(metrics["accuracy"] - 0.20 * metrics["brier"] - 0.20 * metrics["ece"])


def _mean(rows: list[dict[str, float]]) -> dict[str, float]:
    result = {}
    for key in rows[0]:
        values = np.asarray([row[key] for row in rows], dtype=np.float64)
        result[key] = float(values.mean())
        result[f"{key}_std"] = float(values.std())
    return result
