from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from ..reproductions.industrial_2026 import load_industrial_data
from ..reproductions.industrial_ranking import evaluate_model
from ..reproductions.rankmixer.model import RankMixerConfig, train_model
from .models import EvolutionTrial, Genome


class RankMixerEvaluator:
    def __init__(self, dataset_dir: Path, steps: int, seeds: tuple[int, ...]):
        self.data = load_industrial_data(dataset_dir, maximum_users=220, maximum_items=360).sequences
        self.steps = steps
        self.seeds = seeds

    def evaluate(self, trial_id: str, generation: int, parent_id: str | None, genome: Genome,
                 source_papers: tuple[str, ...], rationale: str) -> EvolutionTrial:
        started = time.monotonic()
        validation_runs, training_runs = [], []
        for seed in self.seeds:
            config = self._config(genome)
            model, training = train_model(genome.architecture, self.data, config, seed)
            validation_runs.append(evaluate_model(model, self.data, config, target="validation"))
            training_runs.append(training)
        validation = _mean_metrics(validation_runs)
        training = {
            "initial_loss": float(np.mean([row["initial_loss"] for row in training_runs])),
            "final_loss": float(np.mean([row["final_loss"] for row in training_runs])),
            "parameters": int(np.mean([row["parameters"] for row in training_runs])),
            "seeds": list(self.seeds),
        }
        return EvolutionTrial(trial_id, generation, parent_id, genome, validation, training, source_papers, rationale, time.monotonic() - started)

    def test(self, genome: Genome) -> dict[str, float]:
        runs = []
        for seed in self.seeds:
            config = self._config(genome)
            model, _ = train_model(genome.architecture, self.data, config, seed)
            runs.append(evaluate_model(model, self.data, config, target="test"))
        return _mean_metrics(runs)

    def _config(self, genome: Genome) -> RankMixerConfig:
        return RankMixerConfig(
            dimensions=genome.dimensions,
            heads=4,
            layers=genome.layers,
            batch_size=genome.batch_size,
            steps=self.steps,
            learning_rate=genome.learning_rate,
            optimizer=genome.optimizer,
            experts=genome.experts,
            interval_residual=genome.interval_residual,
            auxiliary_weight=genome.auxiliary_weight,
            sequence_length=24,
            negatives=15,
        )


def _mean_metrics(rows):
    return {key: float(np.mean([row[key] for row in rows])) for key in rows[0]}
