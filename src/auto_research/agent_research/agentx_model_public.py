"""Small, measured MovieLens-1M graph for AgentX-Model public replay.

The graph is deliberately *not* the paper's unpublished production graph.
Every node trains an executable logistic recommendation variant on the same
chronological split. Selection uses validation only; test is read once for the
final selected implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..datasets import movielens_1m
from ..reproductions.llm_rec_data import binary_auc
from .agentx_model import (
    Action, Context, Experiment, ModelAgent, Replay, ResearchAgent, Round, run_replay,
)


VARIANTS: dict[str, tuple[int, ...]] = {
    "baseline": (0, 1, 2, 3),
    "rating-cross": (0, 1, 2, 3, 4),
    "genre-match": (0, 1, 2, 3, 5),
    "cross-followup": (0, 1, 2, 3, 4, 6),
    "composition": (0, 1, 2, 3, 4, 5),
    "composition-followup": (0, 1, 2, 3, 4, 5, 6),
}


@dataclass(frozen=True)
class Split:
    train: np.ndarray
    validation: np.ndarray
    test: np.ndarray
    train_y: np.ndarray
    validation_y: np.ndarray
    test_y: np.ndarray
    counts: dict[str, int]


def _genre_matrix(root: Path, item_count: int) -> np.ndarray:
    genres: dict[int, tuple[str, ...]] = {}
    vocabulary: set[str] = set()
    with (root / "ml-1m" / "movies.dat").open(encoding="latin-1") as stream:
        for line in stream:
            item, _, labels = line.rstrip().split("::")
            genres[int(item)] = tuple(labels.split("|"))
            vocabulary.update(genres[int(item)])
    names = {name: index for index, name in enumerate(sorted(vocabulary))}
    matrix = np.zeros((item_count, len(names)), dtype=np.float64)
    for item, labels in genres.items():
        for name in labels:
            matrix[item, names[name]] = 1
    return matrix


def load_public_split(root: Path, seed: int, *, users: int = 800, train_cap: int = 18000) -> Split:
    """Chronological holdout, train-only aggregates and leave-one-out train rates."""
    rows = movielens_1m(root, allow_network=False)
    rng = np.random.default_rng(seed)
    available_users = np.array(sorted({r[0] for r in rows}))
    chosen_users = set(rng.choice(available_users, min(users, len(available_users)), replace=False).tolist())
    histories: dict[int, list[tuple[int, int, int]]] = {}
    for user, item, rating, timestamp in rows:
        if user in chosen_users:
            histories.setdefault(user, []).append((timestamp, item, int(rating >= 4)))
    train_rows: list[tuple[int, int, int]] = []
    val_rows: list[tuple[int, int, int]] = []
    test_rows: list[tuple[int, int, int]] = []
    for user, history in histories.items():
        history.sort(key=lambda x: (x[0], x[1]))
        if len(history) < 8:
            continue
        train_rows.extend((user, item, label) for _, item, label in history[:-2])
        val_rows.append((user, history[-2][1], history[-2][2]))
        test_rows.append((user, history[-1][1], history[-1][2]))
    if len(train_rows) > train_cap:
        indices = rng.choice(len(train_rows), train_cap, replace=False)
        train_rows = [train_rows[int(i)] for i in indices]
    train = np.asarray(train_rows, dtype=np.int64)
    val = np.asarray(val_rows, dtype=np.int64)
    test = np.asarray(test_rows, dtype=np.int64)
    if any(len(x) == 0 for x in (train, val, test)):
        raise ValueError("MovieLens split has no usable records")
    item_count = max(max(r[1] for r in rows), 1) + 1
    user_count = max(available_users) + 1
    genre = _genre_matrix(root, item_count)
    user_n = np.bincount(train[:, 0], minlength=user_count).astype(float)
    item_n = np.bincount(train[:, 1], minlength=item_count).astype(float)
    user_positive = np.bincount(train[:, 0], weights=train[:, 2], minlength=user_count)
    item_positive = np.bincount(train[:, 1], weights=train[:, 2], minlength=item_count)
    positive_genres = genre[train[:, 1]] * train[:, 2, None]
    user_genres = np.zeros((user_count, genre.shape[1]), dtype=float)
    np.add.at(user_genres, train[:, 0], positive_genres)

    def features(records: np.ndarray, *, leave_one_out: bool) -> np.ndarray:
        u, i, y = records[:, 0], records[:, 1], records[:, 2].astype(float)
        minus = 1 if leave_one_out else 0
        u_count = np.maximum(user_n[u] - minus, 0)
        i_count = np.maximum(item_n[i] - minus, 0)
        u_rate = (user_positive[u] - y * minus) / np.maximum(u_count, 1)
        i_rate = (item_positive[i] - y * minus) / np.maximum(i_count, 1)
        profiles = user_genres[u] - genre[i] * (y * minus)[:, None]
        overlap = np.sum(profiles * genre[i], axis=1) / np.maximum(np.linalg.norm(profiles, axis=1) * np.linalg.norm(genre[i], axis=1), 1)
        return np.column_stack((u_rate, i_rate, np.log1p(u_count), np.log1p(i_count),
                                u_rate * i_rate, overlap, (u_rate * i_rate) ** 2))

    return Split(features(train, leave_one_out=True), features(val, leave_one_out=False),
                 features(test, leave_one_out=False), train[:, 2].astype(float),
                 val[:, 2].astype(float), test[:, 2].astype(float),
                 {"train": len(train), "validation": len(val), "test": len(test), "users": len(val_rows)})


def _fit(x: np.ndarray, y: np.ndarray, steps: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = x.mean(axis=0)
    scale = np.maximum(x.std(axis=0), 1e-6)
    standardized = (x - mean) / scale
    design = np.column_stack((np.ones(len(x)), standardized))
    weights = np.zeros(design.shape[1])
    for _ in range(steps):
        predictions = 1 / (1 + np.exp(-np.clip(design @ weights, -20, 20)))
        gradient = design.T @ (predictions - y) / len(y)
        gradient[1:] += 0.001 * weights[1:]
        weights -= 0.2 * gradient
    return weights, mean, scale


def _predict(x: np.ndarray, fitted: tuple[np.ndarray, np.ndarray, np.ndarray]) -> np.ndarray:
    weights, mean, scale = fitted
    design = np.column_stack((np.ones(len(x)), (x - mean) / scale))
    return 1 / (1 + np.exp(-np.clip(design @ weights, -20, 20)))


def build_measured_graph(split: Split, seed: int) -> tuple[Replay, dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]]]:
    """Train actual candidate variants; retain weights for champion-only test."""
    context = Context("MovieLens-1M", f"chronological-last-two/seed-{seed}", "rating>=4", "AUC", "public-logistic-v1")
    fitted: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    rounds: dict[str, tuple[Round, ...]] = {}
    for name, columns in VARIANTS.items():
        x_train = split.train[:, columns]
        x_val = split.validation[:, columns]
        measured: list[Round] = []
        for steps in (40, 80):
            implementation = f"{name}@{steps}"
            model = _fit(x_train, split.train_y, steps)
            fitted[implementation] = model
            scores = _predict(x_val, model)
            measured.append(Round(implementation, binary_auc(split.validation_y, scores),
                                  float(split.validation_y.mean() / max(scores.mean(), 1e-8))))
        rounds[name] = tuple(measured)
    baseline_auc = max(r.auc for r in rounds["baseline"])
    baseline_round = max(rounds["baseline"], key=lambda r: r.auc)
    fitted["business-baseline"] = fitted[baseline_round.implementation]
    # Diagnosis estimates a single correction factor on train predictions; it
    # is deliberately not ranked as an immediate AUC gain in the replay.
    source = max(rounds["rating-cross"], key=lambda r: r.auc)
    model = fitted[source.implementation]
    train_scores = _predict(split.train[:, VARIANTS["rating-cross"]], model)
    factor = split.train_y.mean() / max(train_scores.mean(), 1e-8)
    val_scores = _predict(split.validation[:, VARIANTS["rating-cross"]], model)
    calibrated = np.clip(val_scores * factor, 1e-6, 1 - 1e-6)
    diagnostic = Round("rating-cross+train-calibration", binary_auc(split.validation_y, calibrated),
                       float(split.validation_y.mean() / max(calibrated.mean(), 1e-8)))
    specs = (
        ("r-cross", Action.REPRODUCE, (), "add user-item rating interaction", "rating-cross"),
        ("r-genre", Action.REPRODUCE, (), "add train-history genre overlap", "genre-match"),
        ("f-cross", Action.FOLLOW_UP, ("r-cross",), "refine interaction with squared term", "cross-followup"),
        ("d-calibration", Action.DIAGNOSE, ("r-cross",), "measure and correct PCOC using train-only factor", None),
        ("c-combine", Action.COMPOSITION, ("r-cross", "r-genre"), "combine distinct interaction and genre features", "composition"),
        ("f-combine", Action.FOLLOW_UP, ("c-combine",), "refine combined features with squared interaction", "composition-followup"),
    )
    graph = [Experiment(key, action, parents, change, context,
                        (diagnostic,) if variant is None else rounds[variant])
             for key, action, parents, change, variant in specs]
    return Replay(graph, baseline_auc), fitted


def run_public_benchmark(root: Path, *, seed: int = 42, budget: int = 2) -> dict[str, object]:
    split = load_public_split(root, seed)
    policies: dict[str, object] = {}
    for policy in ("fixed", "random", "parent-greedy"):
        replay, fitted = build_measured_graph(split, seed)
        result = run_replay(replay, policy=policy, budget=budget, seed=seed)
        name = ("baseline" if result.best_implementation == "business-baseline"
                else result.best_implementation.split("@")[0])
        model = fitted.get(result.best_implementation)
        test_auc = (binary_auc(split.test_y, _predict(split.test[:, VARIANTS[name]], model))
                    if model is not None else None)
        policies[policy] = {
            "best_validation_auc": result.best_auc,
            "selected_implementation": result.best_implementation,
            "selected_test_auc": test_auc,
            "target_reached_at": result.target_at,
            "selections": result.selections,
        }
    diagnostic_replay, _ = build_measured_graph(split, seed)
    researcher = ResearchAgent()
    modeler = ModelAgent()
    first = next(x for x in diagnostic_replay.available() if x.key == "r-cross")
    modeler.investigate(researcher.propose(first, diagnostic_replay.seen,
                                           diagnostic_replay.baseline_auc), diagnostic_replay)
    diagnose = next(x for x in diagnostic_replay.available() if x.key == "d-calibration")
    observed = modeler.investigate(researcher.propose(diagnose, diagnostic_replay.seen,
                                                      diagnostic_replay.baseline_auc), diagnostic_replay)
    before = diagnostic_replay.seen["r-cross"].best
    diagnostic = {
        "source": "r-cross",
        "validation_pcoc_before": before.pcoc,
        "validation_pcoc_after": observed.best.pcoc,
        "validation_auc_after": observed.best.auc,
        "training_only_correction": True,
    }
    return {
        "schema_version": 2,
        "diagnostic_only": True,
        "paper": "2609.30001",
        "dataset": "MovieLens-1M",
        "seed": seed,
        "split": "per-user chronological last two; training subsample only; validation selection; champion-only test",
        "counts": split.counts,
        "budget": budget,
        "baseline_validation_auc": replay.baseline_auc,
        "policies": policies,
        "diagnose": diagnostic,
        "boundary": "Rule-based roles and public measured six-node graph; not the private 473-node agent replay or online A/B.",
    }
