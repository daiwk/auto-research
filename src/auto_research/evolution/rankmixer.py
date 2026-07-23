from __future__ import annotations

import time
from pathlib import Path

import numpy as np

from ..reproductions.rankmixer.model import RankMixerConfig, train_model
from ..reproductions.rec_utils import load_movielens_1m_sequences, load_movielens_sequences
from .models import EvolutionTrial, Genome
from .benchmarks import recommendation_benchmark


class RankMixerEvaluator:
    def __init__(
        self,
        dataset_dir: Path,
        dataset: str,
        steps: int,
        seeds: tuple[int, ...],
        maximum_users=None,
        maximum_items=None,
        evaluation_users=1000,
        benchmark_suite="public",
        fitness_metric="primary",
    ):
        loader = load_movielens_1m_sequences if dataset == "movielens-1m" else load_movielens_sequences
        self.data = loader(dataset_dir)
        self.data = _limit(self.data, maximum_users, maximum_items)
        self.evaluation_data = _evaluation_cohort(self.data, evaluation_users)
        self.steps = steps
        self.seeds = seeds
        self.benchmark_suite = benchmark_suite
        self.fitness_metric = fitness_metric

    def summary(self):
        return {
            "users": len(self.data.train),
            "items": self.data.item_count,
            "train_events": sum(map(len, self.data.train)),
            "evaluation_users": len(self.evaluation_data.train),
            "benchmark_suite": self.benchmark_suite,
            "public_slices": (
                [
                    "overall",
                    "long_history",
                    "tail_target",
                    "recent_only",
                    "restricted_features",
                ]
                if self.benchmark_suite == "public"
                else ["overall"]
            ),
        }

    def evaluate(self, trial_id: str, generation: int, parent_id: str | None, genome: Genome,
                 source_papers: tuple[str, ...], rationale: str) -> EvolutionTrial:
        started = time.monotonic()
        validation_runs, training_runs = [], []
        for seed in self.seeds:
            config = self._config(genome)
            model, training = train_model(genome.architecture, self.data, config, seed)
            validation_runs.append(
                recommendation_benchmark(
                    model,
                    self.evaluation_data,
                    config,
                    target="validation",
                    suite=self.benchmark_suite,
                    restricted_path=True,
                )
            )
            training_runs.append(training)
        validation = _mean_metrics(validation_runs)
        validation["fitness"] = validation[
            "public_composite" if self.fitness_metric == "public_composite" else "primary"
        ]
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
            runs.append(
                recommendation_benchmark(
                    model,
                    self.evaluation_data,
                    config,
                    target="test",
                    suite=self.benchmark_suite,
                    restricted_path=True,
                )
            )
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


def _limit(data, maximum_users, maximum_items):
    """Optional smoke-test limits; defaults always retain the complete public split."""
    if maximum_users is None and maximum_items is None:
        return data
    from ..reproductions.rec_utils import MovieLensSequences
    users = min(maximum_users or len(data.train), len(data.train))
    selected = set(np.argsort(-data.popularity)[: maximum_items or data.item_count].tolist())
    rows = []
    for history, validation, test in zip(data.train, data.validation, data.test):
        sequence = [item for item in (*history, validation, test) if item in selected]
        if len(sequence) >= 5:
            rows.append(sequence)
        if len(rows) >= users:
            break
    items = sorted({item for row in rows for item in row})
    mapping = {item: index for index, item in enumerate(items)}
    encoded = [[mapping[item] for item in row] for row in rows]
    return MovieLensSequences(
        tuple(tuple(row[:-2]) for row in encoded), tuple(row[-2] for row in encoded),
        tuple(row[-1] for row in encoded), len(items), data.item_features[items], data.popularity[items],
    )


def _evaluation_cohort(data, maximum_users):
    if maximum_users is None or maximum_users <= 0 or len(data.train) <= maximum_users:
        return data
    from ..reproductions.rec_utils import MovieLensSequences
    indices = np.linspace(0, len(data.train) - 1, maximum_users, dtype=int)
    return MovieLensSequences(
        tuple(data.train[i] for i in indices), tuple(data.validation[i] for i in indices),
        tuple(data.test[i] for i in indices), data.item_count, data.item_features, data.popularity,
    )
