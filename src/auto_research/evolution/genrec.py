from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np

from ..reproductions.genrec_netflix.data import GenRecData, load_genrec_data
from .models import EvolutionTrial, Genome
from .statistics import mean_with_std


class GenRecEvolutionEvaluator:
    """Full-catalog generative-recommendation search on public MovieLens-1M.

    The evaluator intentionally uses a small trainable catalog model so a full
    population can run locally.  It still executes the consequential GenRec
    choices: history construction, catalog-aware head, per-example reward and
    teacher distillation.  Every metric ranks the complete retained catalog;
    sampled-softmax results are never used for promotion.
    """

    def __init__(
        self,
        dataset_dir: Path,
        steps: int,
        seeds: tuple[int, ...],
        allow_network: bool,
        maximum_users: int | None,
        maximum_items: int | None,
    ):
        self.steps = steps
        self.seeds = seeds
        self.data = load_genrec_data(
            dataset_dir,
            maximum_users=maximum_users or 600,
            maximum_items=maximum_items or 1000,
            allow_network=allow_network,
        )

    def summary(self) -> dict:
        return {
            "dataset": "MovieLens-1M",
            "users": len(self.data.train),
            "items": len(self.data.item_texts),
            "train_events": sum(map(len, self.data.train)),
            "catalog_evaluation": "full retained catalog",
            "seeds": list(self.seeds),
            "genome_axes": ["context", "catalog_head", "reward", "distillation"],
            "selection": "NDCG@10 - 0.02 * head_share@10",
            "baseline": "recent context + ID catalog + uniform CE",
        }

    def evaluate(
        self, trial_id, generation, parent_id, genome, source_papers, rationale,
    ) -> EvolutionTrial:
        started = time.monotonic()
        rows, training = [], []
        for seed in self.seeds:
            model, diagnostics = _train(self.data, genome, self.steps, seed)
            values = _evaluate(self.data, model, genome, target="validation")
            values["primary"] = values["ndcg_at_10"] - 0.02 * values["head_share_at_10"]
            rows.append(values)
            training.append(diagnostics)
        validation = mean_with_std(rows)
        validation["fitness"] = validation["primary"]
        validation["fitness_std"] = validation["primary_std"]
        return EvolutionTrial(
            trial_id,
            generation,
            parent_id,
            genome,
            validation,
            {
                "seeds": list(self.seeds),
                "fitness_by_seed": [float(row["primary"]) for row in rows],
                "steps": self.steps,
                "catalog_items": len(self.data.item_texts),
                "full_catalog": True,
                "axes": {
                    "context": genome.genrec_context,
                    "head": genome.genrec_head,
                    "reward": genome.genrec_reward,
                    "distillation": genome.genrec_distillation,
                },
                "seed_diagnostics": training,
            },
            source_papers,
            rationale,
            time.monotonic() - started,
        )

    def test(self, genome: Genome) -> dict[str, float]:
        rows = []
        for seed in self.seeds:
            model, _ = _train(self.data, genome, self.steps, seed + 10_000)
            values = _evaluate(self.data, model, genome, target="test")
            values["primary"] = values["ndcg_at_10"] - 0.02 * values["head_share_at_10"]
            rows.append(values)
        return mean_with_std(rows)


def _genre_features(data: GenRecData) -> np.ndarray:
    labels = sorted({label for row in data.item_genres for label in row})
    index = {label: offset for offset, label in enumerate(labels)}
    features = np.zeros((len(data.item_texts), len(labels)), dtype=np.float64)
    for item, genres in enumerate(data.item_genres):
        for label in genres:
            features[item, index[label]] = 1.0
    normalizer = np.linalg.norm(features, axis=1, keepdims=True)
    return features / np.maximum(normalizer, 1.0)


def _initial_catalog(data: GenRecData, genome: Genome, rng) -> np.ndarray:
    dimensions = max(8, genome.dimensions)
    learned = rng.normal(0.0, 0.12, (len(data.item_texts), dimensions))
    features = _genre_features(data)
    projection = rng.normal(0.0, 1 / math.sqrt(dimensions), (features.shape[1], dimensions))
    semantic = features @ projection
    if genome.genrec_head == "semantic-catalog":
        return semantic
    if genome.genrec_head == "hybrid-catalog":
        return learned + semantic
    return learned


def _context(history, catalog, mode: str, maximum: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = np.asarray(history, dtype=np.int64)
    if mode == "recent":
        values = values[-max(2, maximum // 2):]
        weights = np.ones(len(values))
    elif mode == "longer-compressed":
        values = values[-max(4, maximum * 2):]
        # Log-like compression: older events remain visible with lower weight.
        ages = np.arange(len(values), 0, -1, dtype=np.float64)
        weights = 1.0 / np.sqrt(ages)
    else:  # full
        weights = np.linspace(0.5, 1.0, len(values), dtype=np.float64)
    weights /= weights.sum()
    return (catalog[values] * weights[:, None]).sum(0), values, weights


def _reward(data: GenRecData, history, target: int, name: str) -> float:
    if name == "novelty":
        return 0.5 + 1.0 - float(data.popularity[target]) / max(float(data.popularity.max()), 1.0)
    if name == "content-discovery":
        seen = {genre for item in history for genre in data.item_genres[item]}
        target_genres = set(data.item_genres[target])
        return 0.75 + len(target_genres - seen) / max(len(target_genres), 1)
    return 1.0


def _teacher(data: GenRecData, history, mode: str) -> np.ndarray | None:
    if mode == "popularity-teacher":
        scores = np.log1p(data.popularity.astype(np.float64))
    elif mode == "semantic-teacher":
        features = _genre_features(data)
        scores = features @ features[np.asarray(history[-8:], dtype=np.int64)].mean(0)
    else:
        return None
    scores -= scores.max()
    probabilities = np.exp(scores / 0.7)
    return probabilities / probabilities.sum()


def _train(data: GenRecData, genome: Genome, steps: int, seed: int):
    rng = np.random.default_rng(seed)
    catalog = _initial_catalog(data, genome, rng)
    examples = [
        (sequence[:index], sequence[index])
        for sequence in data.train
        for index in range(3, len(sequence))
    ]
    losses = []
    scale = math.sqrt(catalog.shape[1])
    learning_rate = min(max(genome.learning_rate, 1e-4), 0.05)
    for _ in range(steps):
        history, target = examples[int(rng.integers(len(examples)))]
        user, items, weights = _context(
            history, catalog, genome.genrec_context, genome.sequence_length,
        )
        logits = catalog @ user / scale
        logits -= logits.max()
        probabilities = np.exp(logits)
        probabilities /= probabilities.sum()
        teacher = _teacher(data, history, genome.genrec_distillation)
        gradient = probabilities.copy()
        gradient[target] -= 1.0
        if teacher is not None:
            gradient = 0.8 * gradient + 0.2 * (probabilities - teacher)
        weight = _reward(data, history, target, genome.genrec_reward)
        gradient *= weight
        catalog_before = catalog.copy()
        user_gradient = gradient @ catalog_before / scale
        catalog -= learning_rate * np.outer(gradient, user) / scale
        catalog[items] -= learning_rate * weights[:, None] * user_gradient[None, :]
        losses.append(float(-weight * np.log(max(probabilities[target], 1e-12))))
    return catalog, {
        "initial_loss": float(np.mean(losses[: min(10, len(losses))])),
        "final_loss": float(np.mean(losses[-min(10, len(losses)):])),
        "parameters": int(catalog.size),
        "seed": seed,
    }


def _evaluate(data, catalog, genome, *, target):
    labels = data.validation if target == "validation" else data.test
    histories = data.train if target == "validation" else tuple(
        (*history, validation)
        for history, validation in zip(data.train, data.validation)
    )
    hits = ndcg = reciprocal = 0.0
    recommended = []
    head = set(np.argsort(-data.popularity)[: max(1, len(catalog) // 10)])
    for history, label in zip(histories, labels):
        user, _, _ = _context(history, catalog, genome.genrec_context, genome.sequence_length)
        scores = catalog @ user / math.sqrt(catalog.shape[1])
        scores[np.asarray(tuple(set(history)), dtype=np.int64)] = -np.inf
        order = np.argsort(-scores)
        top = order[:10]
        recommended.extend(top.tolist())
        position = np.flatnonzero(order == label)
        if position.size:
            rank = int(position[0])
            reciprocal += 1.0 / (rank + 1)
            if rank < 10:
                hits += 1
                ndcg += 1.0 / math.log2(rank + 2)
    count = max(len(labels), 1)
    return {
        "hit_at_10": hits / count,
        "ndcg_at_10": ndcg / count,
        "mrr": reciprocal / count,
        "head_share_at_10": sum(item in head for item in recommended) / max(len(recommended), 1),
    }
