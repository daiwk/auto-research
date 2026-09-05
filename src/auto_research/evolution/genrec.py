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
    if genome.genrec_head == "snaplgr-sid":
        graph = np.eye(len(data.item_texts), dtype=np.float64) * 1e-3
        for sequence in data.train:
            values = np.asarray(tuple(dict.fromkeys(sequence)), dtype=np.int64)
            graph[np.ix_(values, values)] += 1.0
        graph /= np.maximum(graph.sum(axis=1, keepdims=True), 1e-12)
        return semantic + 0.35 * (graph @ semantic)
    if genome.genrec_head == "pair-space":
        # Encode the strongest ordered continuation into each item token so the
        # catalog head represents an item pair while retaining item-level output.
        continuation = np.full((len(data.item_texts), len(data.item_texts)), 1e-3)
        for sequence in data.train:
            for left, right in zip(sequence, sequence[1:]):
                continuation[left, right] += 1.0
        partner = continuation.argmax(axis=1)
        return learned + 0.45 * semantic[partner]
    if genome.genrec_head == "transport-index":
        # Whiten the retrieval space as a compact proxy for globally coordinated
        # dynamic indices; row normalization limits candidate capacity conflicts.
        centered = semantic - semantic.mean(0, keepdims=True)
        _, _, right = np.linalg.svd(centered, full_matrices=False)
        catalog = centered @ right.T
        return catalog / np.maximum(np.linalg.norm(catalog, axis=1, keepdims=True), 1e-12)
    if genome.genrec_head == "embedding-native":
        coengagement = np.eye(len(data.item_texts), dtype=np.float64) * 1e-3
        for sequence in data.train:
            for left, right in zip(sequence, sequence[1:]):
                coengagement[left, right] += 1.0
        coengagement /= np.maximum(coengagement.sum(1, keepdims=True), 1e-12)
        return learned + 0.40 * semantic + 0.25 * (coengagement @ semantic)
    if genome.genrec_head == "disentangled-sid":
        # Separate collaborative identity from semantic content before fusion.
        return np.concatenate((learned[:, : dimensions // 2], semantic[:, dimensions // 2 :]), axis=1)
    if genome.genrec_head == "unified-ranker":
        value = np.log1p(data.popularity)[:, None]
        return learned + semantic + value * np.linspace(0.0, 0.15, dimensions)[None]
    if genome.genrec_head == "listwise-node":
        information_node = semantic.mean(0, keepdims=True)
        return learned + semantic + 0.20 * information_node
    if genome.genrec_head == "dynamic-sid":
        popularity_bin = np.minimum(
            (np.argsort(np.argsort(data.popularity)) * 8 // len(data.popularity)), 7,
        )
        phase = np.linspace(0.0, np.pi, dimensions, dtype=np.float64)
        sid = np.sin((popularity_bin[:, None] + 1.0) * phase[None])
        return learned + 0.45 * semantic + 0.20 * sid
    if genome.genrec_head == "causal-bottleneck":
        confounder = np.column_stack((np.ones(len(data.popularity)), np.log1p(data.popularity)))
        projection = np.linalg.lstsq(confounder, semantic, rcond=None)[0]
        residual = semantic - confounder @ projection
        return learned + residual / np.maximum(np.linalg.norm(residual, axis=1, keepdims=True), 1e-12)
    if genome.genrec_head == "policy-facet":
        facets = _genre_features(data)
        facet_projection = facets @ rng.normal(0.0, 0.2, (facets.shape[1], dimensions))
        return learned + semantic + 0.25 * facet_projection
    if genome.genrec_head == "modular-compression":
        nuisance = np.column_stack((np.ones(len(data.popularity)), np.log1p(data.popularity)))
        residual = semantic - nuisance @ np.linalg.lstsq(nuisance, semantic, rcond=None)[0]
        _, _, right = np.linalg.svd(residual, full_matrices=False)
        width = max(2, dimensions // 2)
        compressed = residual @ right[:width].T
        projector = rng.normal(0.0, 1.0 / np.sqrt(width), (width, dimensions))
        return learned + compressed @ projector
    if genome.genrec_head == "high-rank-representation":
        views = []
        for _ in range(3):
            permutation = rng.permutation(dimensions)
            views.append(np.tanh(semantic[:, permutation] + rng.normal(0.0, 0.02, semantic.shape)))
        global_token = semantic.mean(0, keepdims=True)
        return learned + np.mean(views, axis=0) + 0.15 * global_token
    if genome.genrec_head == "sid-coordination":
        facets = _genre_features(data)
        sid = facets @ rng.normal(0.0, 0.25, (facets.shape[1], dimensions))
        tail_gate = 1.0 - data.popularity / max(float(data.popularity.max()), 1.0)
        return learned * (1.0 - 0.55 * tail_gate[:, None]) + sid * (0.55 * tail_gate[:, None]) + 0.25 * semantic
    if genome.genrec_head == "fine-grained-tags":
        facets = _genre_features(data)
        coarse = facets @ rng.normal(0.0, 0.20, (facets.shape[1], dimensions))
        fine = np.tanh(semantic @ rng.normal(0.0, 0.18, (dimensions, dimensions)))
        return learned + 0.35 * coarse + 0.45 * fine
    if genome.genrec_head == "semantic-catalog":
        return semantic
    if genome.genrec_head == "hybrid-catalog":
        return learned + semantic
    return learned


def _context(history, catalog, mode: str, maximum: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = np.asarray(history, dtype=np.int64)
    if mode == "spectral-soften":
        values = values[-maximum:]
        centered = catalog[values] - catalog[values].mean(0, keepdims=True)
        u, singular, right = np.linalg.svd(centered, full_matrices=False)
        softened = u @ np.diag(np.sqrt(singular + 1e-6)) @ right
        weights = np.linspace(0.5, 1.0, len(values))
        weights /= weights.sum()
        return (softened * weights[:, None]).sum(0), values, weights
    if mode == "zero-weight":
        values = values[-maximum:]
        weights = np.exp(np.linspace(-2.0, 0.0, len(values)))
    elif mode == "quantile-fusion":
        values = values[-maximum:]
        raw = np.linalg.norm(catalog[values], axis=1)
        weights = np.argsort(np.argsort(raw)).astype(np.float64) + 1.0
    elif mode == "partial-order":
        values = values[-maximum:]
        scores = catalog[values] @ catalog[values[-1]]
        weights = (len(values) - np.argsort(np.argsort(-scores))).astype(np.float64)
    elif mode == "unified-token":
        values = values[-maximum:]
        split = max(1, catalog.shape[1] // 2)
        scores = catalog[values, :split] @ catalog[values[-1], :split]
        weights = np.exp(scores - scores.max())
    elif mode == "tm20k-merge":
        values = values[-max(8, maximum * 2):]
        groups = np.array_split(np.arange(len(values)), min(maximum, len(values)))
        merged = np.stack(
            [catalog[values[group]].sum(0) / math.sqrt(len(group)) for group in groups]
        )
        query = catalog[values[-1]]
        group_weights = np.exp((merged @ query) / math.sqrt(catalog.shape[1]))
        group_weights /= group_weights.sum()
        weights = np.zeros(len(values), dtype=np.float64)
        for group, weight in zip(groups, group_weights):
            weights[group] = weight / len(group)
    elif mode == "transx-cross-stream":
        values = values[-max(8, maximum * 2):]
        split = max(1, len(values) - min(4, len(values)))
        weights = np.zeros(len(values), dtype=np.float64)
        weights[:split] = 0.45 / split
        weights[split:] = 0.55 / max(len(values) - split, 1)
        global_behavior = catalog[values[:split]].mean(0)
        serving = catalog[values[split:]].mean(0)
        user = 0.45 * global_behavior + 0.55 * serving
        return user, values, weights
    elif mode == "atomic-intent-tree":
        values = values[-max(8, maximum):]
        similarity = catalog[values] @ catalog[values[-1]]
        coarse = np.maximum(similarity, 0.0) + 0.05
        recency = np.exp(np.linspace(-1.5, 0.0, len(values)))
        weights = coarse * recency
    elif mode == "conversational-intent":
        values = values[-max(4, maximum // 2):]
        similarity = catalog[values] @ catalog[values[-1]]
        weights = np.exp(similarity - similarity.max())
        weights[-min(3, len(weights)):] *= 1.5
    elif mode == "active-expression":
        values = values[-max(8, maximum):]
        split = max(1, len(values) - min(4, len(values)))
        weights = np.full(len(values), 0.45 / split)
        weights[split:] = 0.55 / max(len(values) - split, 1)
    elif mode == "reverse-curriculum":
        values = values[-max(8, maximum):]
        similarity = catalog[values] @ catalog[values[-1]]
        chosen = np.argsort(-similarity)[: min(maximum, len(values))]
        values = values[chosen][::-1]
        weights = np.linspace(1.0, 0.35, len(values))
    elif mode == "hierarchical-preference":
        values = values[-max(8, maximum * 2):]
        groups = np.array_split(np.arange(len(values)), min(4, len(values)))
        query = catalog[values[-1]]
        group_scores = np.asarray([catalog[values[group]].mean(0) @ query for group in groups])
        group_scores = np.exp(group_scores - group_scores.max())
        weights = np.zeros(len(values), dtype=np.float64)
        for group, weight in zip(groups, group_scores):
            local = catalog[values[group]] @ query
            keep = np.argsort(-local)[: max(1, len(group) // 2)]
            weights[group[keep]] = weight / len(keep)
    elif mode == "instruction-foresight":
        values = values[-max(8, maximum):]
        semantic = catalog[values] @ catalog[values[-1]]
        horizon = np.linspace(0.45, 1.0, len(values))
        weights = np.exp(semantic - semantic.max()) * horizon
    elif mode == "recent":
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
    if name == "robust-preference":
        seen = {genre for item in history[-8:] for genre in data.item_genres[item]}
        overlap = len(seen.intersection(data.item_genres[target]))
        confidence = 1.0 / (1.0 + np.sqrt(float(data.popularity[target]) + 1.0))
        return 0.75 + 0.15 * overlap + 0.20 * confidence
    if name == "incrementality":
        seen = {genre for item in history for genre in data.item_genres[item]}
        new = len(set(data.item_genres[target]) - seen)
        return 0.65 + 0.35 * new / max(len(data.item_genres[target]), 1)
    if name == "reward-guided":
        novelty = 1.0 - float(data.popularity[target]) / max(float(data.popularity.max()), 1.0)
        seen = {genre for item in history[-8:] for genre in data.item_genres[item]}
        relevance = len(seen.intersection(data.item_genres[target])) / max(
            len(data.item_genres[target]), 1
        )
        return float(np.exp((0.6 * relevance + 0.4 * novelty) / 0.55))
    if name == "tool-calibration":
        seen = [genre for item in history[-8:] for genre in data.item_genres[item]]
        overlap = sum(genre in seen for genre in data.item_genres[target])
        frequency = sum(seen.count(genre) for genre in data.item_genres[target])
        return 0.75 + 0.10 * overlap + 0.05 * np.log1p(frequency)
    if name == "pareto-semantic-id":
        seen = {genre for item in history[-8:] for genre in data.item_genres[item]}
        semantic = len(seen.intersection(data.item_genres[target])) / max(len(data.item_genres[target]), 1)
        collaborative = float(data.popularity[target]) / max(float(data.popularity.max()), 1.0)
        gap = abs(semantic - collaborative)
        return 0.75 + 0.25 * ((0.5 + 0.25 * gap) * semantic + (0.5 - 0.25 * gap) * collaborative)
    if name == "primal-dual":
        target_share = 0.35
        novelty = 1.0 - float(data.popularity[target]) / max(float(data.popularity.max()), 1.0)
        recent_novelty = np.mean([
            1.0 - float(data.popularity[item]) / max(float(data.popularity.max()), 1.0)
            for item in history[-8:]
        ])
        multiplier = float(np.exp(np.clip(target_share - recent_novelty, -1.0, 1.0)))
        return 0.75 + 0.25 * multiplier * novelty
    if name == "facet-preference":
        seen = [genre for item in history[-8:] for genre in data.item_genres[item]]
        overlap = sum(genre in seen for genre in data.item_genres[target])
        query_rewrite = overlap / max(len(data.item_genres[target]), 1)
        return 0.75 + 0.25 * query_rewrite
    if name == "constraint-aware":
        recent = history[-8:]
        repeated = sum(bool(set(data.item_genres[item]) & set(data.item_genres[target])) for item in recent)
        feasibility = 1.0 / (1.0 + repeated / max(len(recent), 1))
        return 0.75 + 0.25 * feasibility
    if name == "counterfactual-role":
        popularity = float(data.popularity[target]) / max(float(data.popularity.max()), 1.0)
        seen = {genre for item in history[-8:] for genre in data.item_genres[item]}
        bridge = len(set(data.item_genres[target]) - seen) / max(len(data.item_genres[target]), 1)
        return 0.75 + 0.15 * bridge + 0.10 * (1.0 - popularity)
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
