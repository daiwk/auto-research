from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from ..reproductions.hyformer.model import HyFormerConfig, build_model
from ..reproductions.industrial_ranking import evaluate_model, train_supervised
from ..reproductions.rec_utils import load_movielens_1m_sequences, load_movielens_sequences
from .models import EvolutionTrial, Genome
from .rankmixer import _evaluation_cohort, _limit, _mean_metrics


class HyFormerEvaluator:
    def __init__(self, dataset_dir: Path, dataset: str, steps: int, seeds: tuple[int, ...], maximum_users=None, maximum_items=None, evaluation_users=1000):
        loader = load_movielens_1m_sequences if dataset == "movielens-1m" else load_movielens_sequences
        self.data = _limit(loader(dataset_dir), maximum_users, maximum_items)
        self.evaluation_data = _evaluation_cohort(self.data, evaluation_users)
        self.steps, self.seeds = steps, seeds

    def summary(self):
        return {"users": len(self.data.train), "items": self.data.item_count, "train_events": sum(map(len, self.data.train)), "evaluation_users": len(self.evaluation_data.train)}

    def evaluate(self, trial_id, generation, parent_id, genome, source_papers, rationale):
        started = time.monotonic()
        validations, trainings = [], []
        for seed in self.seeds:
            config = self._config(genome)
            model = build_model(genome.architecture, self.data, config)
            model, training = train_supervised(model, self.data, config, seed)
            validations.append(evaluate_model(model, self.evaluation_data, config, target="validation"))
            trainings.append(training)
        return EvolutionTrial(
            trial_id, generation, parent_id, genome, _mean_metrics(validations),
            {"initial_loss": float(np.mean([x["initial_loss"] for x in trainings])),
             "final_loss": float(np.mean([x["final_loss"] for x in trainings])),
             "parameters": int(np.mean([x["parameters"] for x in trainings])), "seeds": list(self.seeds)},
            source_papers, rationale, time.monotonic() - started,
        )

    def test(self, genome):
        runs = []
        for seed in self.seeds:
            config = self._config(genome)
            model, _ = train_supervised(build_model(genome.architecture, self.data, config), self.data, config, seed)
            runs.append(evaluate_model(model, self.evaluation_data, config, target="test"))
        return _mean_metrics(runs)

    def _config(self, genome):
        return HyFormerConfig(
            dimensions=genome.dimensions, heads=4, layers=genome.layers,
            sequence_length=64, batch_size=genome.batch_size, steps=self.steps,
            learning_rate=genome.learning_rate, optimizer=genome.optimizer,
        )
