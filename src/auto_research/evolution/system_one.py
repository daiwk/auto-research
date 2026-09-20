"""Executable System One evolution over a public Banking77 protocol."""

from __future__ import annotations

from dataclasses import replace
import random
import time
from pathlib import Path

import numpy as np

from ..system_one.benchmark import evaluate_examples, load_banking77
from ..system_one.local import LocalDecisionModel, LocalSystemOneProvider
from .models import EvolutionTrial, Genome


OPERATORS = (
    "system-one:bilinear-ce",
    "system-one:rival-ce",
    "system-one:rival-brier",
    "system-one:rival-hybrid",
)


class SystemOneEvolutionEvaluator:
    executable_operators = OPERATORS

    def __init__(self, config, project_dir: Path) -> None:
        if config.dataset != "banking77":
            raise ValueError("system-one evolve currently supports Banking77")
        self.config = config
        self.train, self.validation, self.test_rows = load_banking77(
            (project_dir / config.dataset_dir / "system-one").resolve(),
            allow_network=config.allow_network,
            maximum_train_examples=config.maximum_examples * 4,
            maximum_eval_examples=config.maximum_examples,
        )
        self.steps = config.steps
        self.seeds = config.seeds

    def summary(self) -> dict:
        return {
            "source": "PolyAI Banking77",
            "license": "CC BY 4.0",
            "evaluation_tier": "l2_public_dataset",
            "promotion_eligible": True,
            "train_examples": len(self.train),
            "validation_examples": len(self.validation),
            "test_examples": len(self.test_rows),
            "genome_axes": ["dynamic candidate scorer", "proper scoring objective"],
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
        return replace(
            parent,
            architecture=architecture,
            dimensions=dimensions,
            learning_rate=learning_rate,
        ), (
            f"System One 控制变量：{architecture}；dimensions={dimensions}；"
            f"learning_rate={learning_rate}"
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
